---
title: Installing BigBlueButton on Your Dedicated Server
date: '2020-04-21'
description: ''
categories:
- Linux
- Server
- Tools
tags:
- BigBlueButton
- Dedicated Server
- Greenlight
- Hetzner
- Ubuntu 16.04
- Video Conference
- videoconferencing
- open-source
- ubuntu
- server
---

## Introduction

After struggling with a dedicated server from Strato Webhosting, running ubuntu 18.04 and playing around with schroot to get some ubuntu 16.04 environment, I gave up with this solution. The systemd hurdle was much to high to be taken within the available time I currently have.

### Finding the right server

The first act was to find a suitable dedicated server throughout various providers from cheap to expensive. There have been only a few but hard requirements: German location, 4+ Cores, 8+ GB RAM, 100+ GB SSD, 400+ MBit internet connection, 1+ TB Traffic. And the hardest requirement: **Ubuntu 16.04**

At [hetzner](https://www.hetzner.com) I found a german provider. A bit expensive in general, but there is also some server auction section where you could find really valuable servers with great support and a nice price tag. They start at around 30€/month and they include almost everything you could dream about.

Long story short, I ordered a dedicated server from hetzner, located in Germany (Falkenstein, FSN1), and installed some ubuntu 16.04 using the rescue system. The automated installer of the rescue console offers (possibly) all available Linux derivatives. From the Hetzner Robot you can get already a hand full of supported distributions, but through the rescue system, there are many supported distros more to be chosen, not talking about the available unsupported ones.

The whole procedure took around 20-30 minutes from customer registration through ordering the server to get it running. The hetzner-wiki is crystal clear, the installer is easy, the whole stuff is rock stable.

## TL;DR

### Setting up the server

To setup the server, you usually need to wait a few minutes, until the server shows up in the so-called Hetzner Robot. Here you can choose to start the rescue system with your SSH pubkey to be deployed ([details at hetzner wiki](https://wiki.hetzner.de/index.php/Hetzner_Rescue-System))...

![](/images/blog/2020/04/image-6.png)

...and then do an automated reset.

![](/images/blog/2020/04/image-7.png)

Then log in the rescue system with SSH and enter `installimage`.

This command issued, a menu will appear and guide you through the install procedure of the operationg system of your choice (for BigBlueButton you need ubuntu-16-04-minimal). Amazingly, there is a ton of hetzner supported systems, but a megaton of unsupported but available derivatives.

Welp, this menuconfig-style tool is a bit old-school, but it serves it's purpose so well... I'm really fascinated. And within 5 minutes, the system is poured on your server's hard disk. When finished, type `reboot` and the server will boot the new operating system.

### Setting up BigBlueButton...

...with Let's Entcrypt SSL, Greenlight and (almost) the whole configuration.

Just do a system update/upgrade...

```
apt update
apt upgrade
```

... and then you can start over installing bbb...

```
wget -qO- https://ubuntu.bigbluebutton.org/bbb-install.sh |\
    bash -s -- -v xenial-220 -s bbb.example.com \
    -e info@example.com -g
```

That's it... When you change your Greenlight config in `~/greenlight/.env` (e.g. for enabling Google OAuth2), just follow this procedure:

```
cd ~/greenlight
vi .env   # do there what you want or need
docker-compose down
docker-compose up -d
```

If you see a 404 Error when loading your page (https://bbb.example.com), just give it 30 seconds (or more if you did not follow the system requirements :-) ) to come up and enjoy your conferences.

## My first real world experiences

After some days, I had a "real world" video conference with 20 attendees, all using audio and 14 of them video. It was the first virtual classroom meeting of my daughter, related to my [School's out post](https://blog.the78mole.de/schools-out-how-to-tame-your-children/). Most of the attendees had been crystal clear without interruptions. Some of them had minor audio and/or video stuttering and two of them I could hardly understand. OK, there have been a few that had problems with their own hardware (video and audio), but this was not related to BBB.

The stuttering connection originates mainly from WiFi connections, loosing and delaying data packets. So, if you don't have a chance to get wired, get as close as you can to your WiFi hotspot. There can also be a big difference between cheap consumer equipment and the professional one. I run some UniFi based installation from ubiquity networks that simply outperforms the FritzBox WiFi in every aspect (speed, reliability, configurability, VLAN capability, ... and so on)

Also watching htop for a while gives some interesting insights what BBB expects from your server. With 20 attendees and many having the microphone turned on and talking, the load rises astonishingly. My quad-core core-i7 (8 virtual HT CPUs, see [server details](https://www.hetzner.de/dedicated-rootserver/ex42-nvme)) was pushed up to 30% per cpu during this meeting. This mostly originated from freeswitch and kurento-media-server:

![](/images/blog/2020/04/image-12-1024x560.png)

This means two things:

1. It takes quite a lot of power to mix audio in realtime.
2. The freeswitch code seems to make very efficient use of multiple processors

That's both, good and bad news for large installations. Bigger hardware with more cores is a constructive solution. But honestly, if you are planning to put more than 100 concurrent users on a server in a production environment, you should think about high-availabilty solutions (keywords: AWS Elastic Load Balancer, AWS RDS with failover and availability zones,...). But then, the bbb-install.sh approach get's to it's limits. However, it serves well as a starting point to get up a test system and to understand BBB's and Greenlight's architecture.

## Some words about the client

When you know Zoom Meetings, which is a bit bullheaded about installing an executable and you need to rick it to get the browser version of the client, you will find BBB a real pleasure.

To use the BBB server, there is nothing needed beside a web browser. It supports audio, video and screen sharing (screen or application based) and it supports uploading a presentation or watching a web video (youtube, vimeo,..) together while the moderator controls the content. I tested it already with a few friends and we found out, that it works best with Chrome and Firefox on Windows and Linux. But even on smartphones it runs fine, as long as you have a high quality internet connection.

## What next?

BigBlueButton advises to not install any other stuff beside BBB (and maybe Greenlight) on the Server because of the realtime audio processing in FreeSwitch, every little delay can destroy the user experience of your video conference.

In fact, if you have enough cores and RAM and running on a NVMe-RAID 1, you can for sure install other web applications on your server, if you don't do heavy number crunching. If you can live with the risk, that the other applications potentially influence the conference quality, there is no technical reason not to do so.

The configuration of nginx looks very clear and straight forward. You should be able to add another site (in /etc/nginx/sites-available) and activate it (soft-link it to /etc/nginx/sites-enabled/). The only thing I would advise is to run it on another subdomain (otherapp.example.com). For more encapsulation and also with a bit more effort, you can go with a second IP or whatever you like...

### Backup thoughts

With a dedicated server, you should keep your backup always in mind. It is not simply creating a snapshot like in virtualized environments. If you build up on e.g. ext4, your backup might brake. If you want to create an online snapshot backup of your system block devices, better stick with an LVM base for your block devices or, if you like the bleeding edge, with btrfs.

#### Doing it the safe way

The safest way for sure is to stop all services and take a snapshot then. The most secure is to boot some rescue system, fetch the raw disk image snapshot and then boot back in the system. This is safe, but it could mean, that you need to do it manually. Hetzner is providing information for its Robot-API (the one that Hetzner Robot is using), but it could mean quite some work to implement it... and you need a second server (or a RaspberryPi at your home) that steers the backup process using the Robot-API and SSH commands (intersting thought BTW, maybe I'll try it and write some new post about it one day)...

#### Doing it the less safe way

But there is also a quite safe way of doing your backup with all services running. There are five different parts to be considered.

1. The system environment (e.g. /boot --> block device based)
2. The Home Directores (e.g. /root --> file based)
3. The static system files (e.g. /usr/share --> file based)
4. The variable system files (e.g. /var/lib --> file based)
5. The database directories (dynamic --> dump based)

With this said, the process should be quite clear.

Firstly, you should backup your whole system (finished installing your services) on block device level using a rescue system, just to make sure, you can easily revert to a running state or bind-mount the block device snapshot to compare with your file based backups.

Secondly, dump your database files to place a like root's home directory, so the content gets somewhat like static content. Usually transaction based databases dump a consistent state. It depends on the software, how well the transactions are formed, but usually this should at least keep the database itself intact.

Thirdly, backup the files from all other directories (exluding temporary ones) using a efficient approach (e.g. rsync, rsnapshot or [borg](https://borgbackup.readthedocs.io/en/stable/)) over to a safe place.

And last but not least, check your backup consientiously, or better, try a restore. For a production environment, a regular and automated restore test is indispensable. Being honestly, for a real production environment with hundreds of users, a simple dedicated server is not the right way to go.

#### Doing it the Chuck Norris way

A quite risky, but mostly working way, is to run a snapshot tool simply on the running system. As it is stated on the borg page, most directories are stable enough to be backed up using an rsync approach. If you do your first backup (that takes quite long) with all services stopped and then only do incremental backups (being lightning fast), there is a low chance of e.g. a home directory changing during the backup process. To avoid getting inconsistent databases, just do a new dump of your databases beforehand (e.g. to backup user's home). You can even prevent more of the risky parts (using LVM, btrfs) to lower the chance for unexpected changes. And moreover you can stop the relevant services.

For the docker containers (postgres and greenlight), you need to keep in mind, that it is a good practice for docker services to store their data in a bind mount that is kept in the host system. This means, that the thoughts on the database dumps can not be relaxed and may get even more complicated.

### Installing Moodle on the BBB-Server

Next step is to install Moodle on this server and migrate all the users and courses from the old one (see my [post](https://blog.the78mole.de/schools-out-how-to-tame-your-children/) about it's installation) to the new one (stay tuned).

Have fun with BBB and Greenlight :-)
