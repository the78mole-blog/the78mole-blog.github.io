---
title: "The Tunnel I Forgot to Wall Off"
date: '2026-11-08'
description: 'My DMZ looked great on paper. Then I ran curl from inside the Nextcloud container and found a master key to the whole burrow. How I walled it off with a handful of iptables rules, and why that is only the first wall.'
image: /images/blog/2026/11/nextcloud-tunnel-i-forgot-to-wall-off.jpeg
categories:
  - Security
  - Tools
tags:
  - nextcloud
  - docker
  - iptables
  - firewall
  - network-segmentation
  - proxmox
  - dmz
  - self-hosting
  - egress-filtering
---

Every mole who has ever bragged about their burrow knows the moment. You're showing a guest around, you point at the sturdy walls, and the guest leans on one and falls through into the pantry.

Yesterday I wrote about [the Nextcloud break-in that wasn't](/blog/2026/nextcloud-break-in-that-wasnt): 39,000 exploit attempts against the Collabora app, not one working web shell. Near the end I asked the obvious question – what if the shell *had* hatched? – and confidently started typing something about DMZs and segmentation. Then I went to check. This post is about what I found, and about the walls I put up on 7 and 8 November.

| Tunnel | What happened |
|---|---|
| The discovery | One VM in four networks, a firewall that was never switched on |
| The worse discovery | The container could reach every other container's published port |
| The options | Four ways to wall it off, and why I picked the quick one first |
| The fix | Two iptables chains, a fixed bridge name, a systemd drop-in |
| The result | Before/after, tested from where the attacker would stand |

## A DMZ With a Back Door in Every Room

Nextcloud runs as a Docker container on a VM. That VM has its default route in the DMZ, as it should. It also has a leg in the home LAN, one in a services VLAN where the MariaDB lives, and one in the management network of the Proxmox hosts. Four networks. Each of those NICs got added for a good reason at some point, and none of them ever got removed.

The Proxmox firewall should have caught that. Every single NIC had `firewall=1` set. But the firewall was switched off at cluster level, so all those ticked boxes did exactly nothing. The checkbox was on, the main switch was off. I'd love to say I'd never fall for that, but there it was.

So I did what an attacker with a web shell would do: `curl` from inside the Nextcloud container. Everything came back HTTP 200. Both Proxmox web UIs. The Homematic. Home Assistant. The DMZ router. And of course the internet.

## It Gets Worse: The Neighbours

That would have been bad enough. But while digging I found something that no amount of VLANs would ever have fixed.

The same VM runs a whole zoo of other stacks. Each of them publishes its ports on the host. And the Nextcloud container could reach **every published port of every other container**, on every one of the host's IPs. Among them: my secret store, phpMyAdmin, n8n, open-webui. Plus SSH on the host itself.

That's all traffic within one machine. It never touches a switch, a router or a VLAN boundary. Network segmentation can't see it, let alone stop it.

So the honest answer to "what if the shell had hatched?" is: a successful Nextcloud RCE would have been a master key to the whole burrow.

## Four Ways to Wall It Off

| Option | What | Pro | Contra |
|---|---|---|---|
| A | iptables on the Docker VM, only for the Nextcloud bridge (`DOCKER-USER` + `INPUT`) | Quick, only Nextcloud is affected, the other stacks stay untouched | No help after a container escape – same kernel, and the VM is still in four networks |
| B | Proxmox firewall on the VM's NICs | A second layer outside the VM | Only sees the whole VM, not single containers (everything is masqueraded to the VM's IP); switching on the cluster firewall is a great way to lock yourself out |
| C | A dedicated VM for Nextcloud, DMZ only | Real segmentation that survives an escape | Migration, downtime, work |
| D | Egress allowlist (only 80/443/587, DNS and the DB) | Stops reverse shells on exotic ports | Can break app installs in surprising ways |

The decision: **A right now**, D later, and C as the actual fix. A doesn't solve everything, but it closes the biggest hole today instead of in some future weekend.

## Walling Off the Nextcloud Bridge

### Step 1: Know what you're working with

Docker 28.1.1, iptables 1.8.9 with the nf_tables backend. No ufw, no nftables ruleset of my own, no firewalld. `DOCKER-USER` was empty, the `INPUT` policy was ACCEPT without a single rule. A blank slate, in the worst sense.

### Step 2: Find out what Nextcloud actually needs

Before you block things, you list what has to keep working:

- MariaDB in the services VLAN (tcp/3306)
- Redis on the stack's own bridge
- SMTP submission (587)
- App Store and updates (443)
- DNS
- Itself, via the public address. The built-in Collabora calls the WOPI URL through the public hostname, so the hairpin has to work.

DNS was the trap. Docker's built-in resolver at `127.0.0.11` forwards to the host's resolver, and that one sits in the home LAN. Docker sends those queries from the container's network namespace. So a blanket "block the home LAN" would have broken name resolution for the whole stack. The fix is an explicit exception for tcp/udp 53 to exactly that one resolver.

### Step 3: Give the bridge a name that stays

Firewall rules on a Docker bridge need the interface name. Mine was called `br-5c91176c34b8`, and it would have got a new random name on the next `docker compose down`. The rules would have kept matching nothing, silently. That's the worst kind of firewall: the one that looks fine.

So the Compose file now pins the name and the subnet:

```yaml
networks:
  default:
    driver_opts:
      com.docker.network.bridge.name: br-nextcloud
    ipam:
      config:
        - subnet: 172.30.0.0/16
```

Recreating the network cost about five seconds of downtime.

### Step 4: The rules

The rules live in an idempotent script with two chains of its own. `NC-EGRESS` handles everything the container sends through the host (jumped to from `DOCKER-USER`), `NC-INPUT` handles everything it sends *to* the host (jumped to from `INPUT`). Both only match traffic coming in on `br-nextcloud`. Shortened, with the addresses replaced by placeholders:

```bash
BRIDGE=br-nextcloud
FWD=NC-EGRESS
INP=NC-INPUT
DB=10.x.x.x       # MariaDB in the services VLAN
DNS=192.168.x.1   # the host's resolver in the home LAN
PRIVATE="10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 169.254.0.0/16 100.64.0.0/10"

# Forwarded traffic from the Nextcloud bridge
ipt -A "$FWD" -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
ipt -A "$FWD" -o "$BRIDGE" -j RETURN
ipt -A "$FWD" -d "$DB"  -p tcp --dport 3306 -j RETURN
ipt -A "$FWD" -d "$DNS" -p udp --dport 53   -j RETURN
ipt -A "$FWD" -d "$DNS" -p tcp --dport 53   -j RETURN
for n in $PRIVATE; do
    ipt -A "$FWD" -d "$n" -m limit --limit 6/min -j LOG --log-prefix "NC-EGRESS-DROP "
    ipt -A "$FWD" -d "$n" -j DROP
done
ipt -A "$FWD" -j RETURN

# Traffic to the host itself, on any of its IPs
ipt -A "$INP" -m conntrack --ctstate ESTABLISHED,RELATED -j RETURN
ipt -A "$INP" -m limit --limit 6/min -j LOG --log-prefix "NC-INPUT-DROP "
ipt -A "$INP" -j DROP

# Hook the chains in only once they're complete
ipt -C DOCKER-USER -i "$BRIDGE" -j "$FWD" 2>/dev/null || ipt -I DOCKER-USER 1 -i "$BRIDGE" -j "$FWD"
ipt -C INPUT -i "$BRIDGE" -j "$INP" 2>/dev/null || ipt -I INPUT 1 -i "$BRIDGE" -j "$INP"
```

What that does, line by line in plain mole:

- Replies to requests coming in from the reverse proxy pass (ESTABLISHED/RELATED).
- The database and the one DNS resolver are allowed.
- Everything to private, link-local and CGNAT ranges gets logged (rate-limited) and dropped.
- The internet stays open – for now, that's option D.
- Everything addressed to the host itself is dropped. That covers SSH and every service bound directly on the host.

The neighbours' published ports are the neat part. A request to `host-ip:port` gets DNAT'ed by Docker to the target container's private IP before it is forwarded. So it ends up in `NC-EGRESS` with a private destination and falls under the RFC1918 drop. No need to list a single port.

The script also has a `--remove` switch that takes everything out again, as the rollback. And it can't lock me out of SSH or management: that traffic never comes in on `br-nextcloud`.

### Step 5: Make it survive a reboot

`iptables-persistent` and Docker don't get along – both want to own the ruleset. So instead the script hangs off `docker.service` via a drop-in:

```toml
[Service]
ExecStartPre=-/usr/local/sbin/nextcloud-egress.sh
ExecStartPost=-/usr/local/sbin/nextcloud-egress.sh
```

`ExecStartPre` closes the window at boot, before dockerd starts any container – remember from the last post that a restart is exactly when things get interesting. `ExecStartPost` applies the rules once more after Docker has built its own chains. The leading `-` means a broken script won't stop Docker from starting. I'd rather have a running Nextcloud without walls than no Nextcloud at all and a 2 a.m. debugging session.

## Before and After

Same `curl` tests, same container, same spot where the attacker would stand:

| Target from inside the container | Before | After |
|---|---|---|
| Proxmox web UIs | 200 | blocked |
| Homematic, Home Assistant | 200 | blocked |
| DMZ router, home router | 200/301 | blocked |
| Secret store, on all four host IPs | 200 | blocked |
| n8n, phpMyAdmin, open-webui, host SSH | open | blocked |
| MariaDB, SMTP, Redis, DNS | open | open |
| App Store, GitHub, my own public URL, Collabora | 200 | 200 |

That's the table I wanted to be able to write yesterday.

## The 503 That Wasn't the Firewall

After recreating the container, Collabora answered with a 503. Of course my first thought was the brand-new firewall. I was already reaching for `--remove`.

It wasn't the firewall. The built-in CODE server keeps its settings file in the container's `/tmp`, and recreating the container had thrown it away. The file only gets written again on the next page load. One page load later, everything worked.

Moral: not every error after a firewall change is the firewall. But you'll always suspect it first.

## What This Wall Doesn't Do

Let's be honest, again:

- **This only protects against a compromised container.** After a container escape, the attacker is on a VM that still sits in four networks and can still reach every app on it. Same kernel, same problem.
- **The real fix is option C:** Nextcloud on its own VM, DMZ only, and the secret store moved away from any VM that hosts internet-facing apps. After that, the Proxmox firewall as a second layer.
- **Egress is still wide open to the internet.** Option D comes next, starting with logging only, so I can see what Nextcloud really talks to before I break the App Store.
- **Found along the way:** Nextcloud's `trusted_proxies` pointed to a subnet that now belongs to a completely different container. That one's on the list.
- **The boot path isn't proven yet.** The drop-in looks right, but I'll only believe it after the next real reboot and a fresh round of `curl` from inside.

The burrow has one new wall now, and a much better idea of where the others should go. Next up: moving a cloud into its own little molehill.
