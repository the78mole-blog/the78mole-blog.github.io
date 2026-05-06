---
title: Headless Rescue System over SSH
date: '2019-09-08'
description: ''
categories:
- Linux
tags:
- Backup
- network-console
- Ploplinux
- squashfs
- SSH
---

Again, I stumbled over some problem... I need to draw some backup disk image of a headless bare metal server, to run a risky update of atlassian tools. And yes, it was one of the old servers in my network, not beeing virtualized.

I tried a lot of different solutions, including debian (and derivatives) with automated installer and it's network-console, but it was not leading to a working ssh access. So I searched a lot and came to [ploplinux](https://www.plop.at/de/ploplinux/index.html). Just put it on a USB-Stick and run it. It will start up with ssh server and a default password for root (root:ploplinux).

To find your server in your network, just do (on another Linux machine):

```
nmap -sn 192.168.1.0/24 | grep ^Nmap > network_snapshot.txt
```

and when ploplinux was booted (its a one-liner...)

```
nmap -sn 192.168.1.0/24 | grep ^Nmap > network_rescue.txt && \
      diff network_snapshot.txt network_rescue.txt | grep ^\>
```

To find the IP address of the running ploplinux. It will show somewhat like:

```
> Nmap scan report for XYZ.fritz.box (192.168.1.30)   # Some other machine
> Nmap scan report for 192.168.1.124                  # This is ploplinux
> Nmap done: 256 IP addresses (39 hosts up) scanned in 7.85 seconds
```

Then I logged in over SSH on 192.168.1.124 as root using `ploplinux` as the password and was able to do what I need.

Mounting a NTFS drive (some large USB drives use it) needed the command `mount.ntfs-3g <drive> <mountpoint>` to work...

### BTRFS-Backup (using squashfs)

Taking a raw image of some partition with BTRFS is not as convenient as it seems. To get some image of the containing filesystem, it is easier, to mount it directly and run `mksquashfs` on it. It then is easily mountable in any linux that supports squashfs. To create the backup, run the following commands, replacing sda1 with the device your filesystem to backup resides in. If you connected a large USB drive for putting your backup on, cd to there...

```
cd <where_some_space_is_available>
mkdir /mnt/tmp
mount -o ro /dev/sda1 /mnt/tmp
mksquashfs /mnt/tmp backup.squashfs
```

To test you backup-image:

```
mkdir /mnt/test
mount -o loop backup.squashfs /mnt/test
```

and examine the contents of your mounted filesystem tree. More information about squashing filesystems can be found [here](https://www.tldp.org/HOWTO/html_single/SquashFS-HOWTO/) or [here](https://blog.hambier.lu/post/space-saving-backup). If everything is fine, the backup is finished... Don't forget to eject your USB drive cleanly, to not corrupt data with unwritten cache. Therefore, unmount your USB drive or use `eject <usb_device>` to do it.

Happy plopping ;-)
