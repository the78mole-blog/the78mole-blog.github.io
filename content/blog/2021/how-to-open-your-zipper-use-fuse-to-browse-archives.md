---
title: How To Open Your Zipper - Use Fuse To Browse Archives
date: '2021-11-08'
description: ''
categories:
- Bashing
- Linux
- Storage
tags:
- 7zip
- AVFS
- compressed archives
- loop-mount
image: /images/blog/2021/11/7zip-and-fuse.png
---

Since I did many Backups of important folder in former times using 7z (one snapshot had 14 GB), I was searching for a way to access it more easily.

For zip, there is already a package fuse-zip (in a quite old version 0.5.0, but there is no fuse module packaged for 7zip archives. You will find e.g. fuse-7z-ng on Github, but it is quite wired to build it and at the end, compiling fuse-7z-ng fails. But there is also avfs available in raspbian based on debian 10. Since it is quite outdated (1.0.6) and the latest version is 1.1.4, we will build it ourself.

```bash
sudo apt install build-essential liblzma5 liblzma-dev
cd ~
wget -O avfs-1.1.4.tar.bz2 https://sourceforge.net/projects/avf/files/avfs/1.1.4/avfs-1.1.4.tar.bz2/download
tar xfj avfs-1.1.4.tar.bz2
cd avfs-1.1.4
./configure
```

Watch out, if liblzma was recognized correctly:

![](/images/blog/2021/11/image.png)

Then compile the tool:

```bash
make
sudo make install
```

Then execute the mount command

```
mountavfs
cd ~/.avfs
```

Below this path, your whole root filesystem is mirrored. But with the difference, that you can simply `ls` into (mostly) any archive file you find by adding # to the end of the archive file name.

![](/images/blog/2021/11/image-1.png)

You can also cd into it:

![](/images/blog/2021/11/image-2.png)

Unfortunately, it is read only, but you can even access the content with vi or any other tool of your choice.

Have fun browsing to your archives...

### Links

- https://askubuntu.com/questions/94649/how-to-mount-a-zip-file-as-a-file-system
- http://avf.sourceforge.net/
