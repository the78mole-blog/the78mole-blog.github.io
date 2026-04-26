---
title: Windows (was) just a pain
date: '2018-09-03'
description: ''
categories:
- Bashing
- OS
- Windows
tags: []
image: /images/blog/2018/09/Gnu-bash-logo.svg_.png
---

Since I use Linux at home and love to develop embedded, backend and (web)-fronteds within a real operating system, I sometimes get crazy at work, when I just search for an alternative to a simple command line... So, what's the alternative in Windows? The Command Prompt, then PowerShell or some specialized, magic, woodoo,... GUI application with the worst design ever seen in the universe and beyond?

OK, I see, you need an example ;-) Here it is one of my favorite: Syncronize a 100-GB-folder from one machine to another when one is at the end of the world, connected by avian carriers (see also [RFC 2549 - IP over avian carriers](https://tools.ietf.org/html/rfc2549)) with a perceived rate of 2 bit per hour. 22 years ago, rsync was invented and serves every (unidirectional or pseude-bidirectional) syncronization desire with a sheer infinite amount of options... But, it is not available (directly) for windows...

Welp, some time ago, there was cygwin, which was driven by Red Hat. OK, it is still being developed, but somehow, I feel it is not serving my desires very well. At least not the desires a developer has. I also found MinGW and MSYS some years ago, but as I ran into trouble with wget and rsync when handling large files, I tested [MSYS2](https://www.msys2.org/) (it already includes MinGW-32 or MinGW-64, whichever you prefer). That was the starting point to test MSYS2 and to my surprise, it is exactly what makes my heart pound faster. All previous POSIX/Linux/Universe/Multiverse/... compatibility layers for Windows had some GUI to select packages, run updates,... But not MSYS2! It uses a pacman port. OK, I didn't use pacman before when I was not forced to (I prefer APT), but it is COMMAND LINE and it runs on Windows (64-bit).

And even better, it did the ssh configuration well (a problem in old MSYS), so that you could generate and use an SSH key, which makes rsync even more powerful...

Hey guys of MSYS2, whenever you pass by in Germany (Erlangen), I will spend you some beer at Steinbach Bräu. This brewery is just to beer, what you are to Windows. Simply the greatest enrichment ;-)

## TL;DR

So, if you would like to use rsync and wget in windows, just install [MSYS2](https://www.msys2.org/), do the obligatory update described on their page and execute the following:

```
pacman -S wget openssh rsync
```

Have fun with Bash, SSH, Rsync and all that other cool Linux tools on Windows!

## An Anthem On Chocolatey

I just bought a new notebook and kept the windows, installed on it up to now. But what I did differently than with any other machine, I startet with [Chocolatey](https://chocolatey.org/) and Chocolatey GUI (you can install the GUI with Choco by typing `choco install chocolatey-gui`) from the very beginning and hey, it's great! Install the tools you use most with just two clicks of your mouse button. No searching for the download page, not nasty clicking through installers... and the upgrades get easy as well, all in one bunch... Try it, you will love it!

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+windows-was-just-a-pain&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
