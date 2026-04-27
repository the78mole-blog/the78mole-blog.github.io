---
title: OrangePi 2G-IOT Android 4.4 SDK
date: '2018-12-10'
description: ''
categories:
- Android
- ARM
tags: []
---

## Getting the Android SDK

Since I just struggled getting the Android SDK for my little OrangePi 2G-IOT, I felt responsible to share it using bittorrent. The main problems have been, to download all that stuff from mega.nz (it raises limits for users not paying a monthly fee) and another one was, to concat all 7 files to a working tar.gz. I think, the wildcard they use in the OrangePi's user manual does not expand the filesnames of the parts in the right order. But then, wired errors occur.

If you encounter problems with not being able to create symbolic links when unpacking, just use a real file system as the base for your unpacked archive (e.g. ext4, btrfs, ..., but NOT NTFS or FAT).

Here you can find the torrent:

<https://downloads.the78mole.de/OrangePi_2G-IOT.tar.gz.torrent>

## Getting the toolchain

Another dangling point of OrangePi's SDK is the lack of a toolchain. They have a large download, but it does not contain a toolchain. So just download the correct one from [linaro](https://releases.linaro.org/components/toolchain/binaries/latest-5/arm-linux-gnueabi/) (take the appropriate one for your system, mine is x86\_64), unpack it inside the folder where the empty folder *toolchain* is (here it's *~/somewhere/OrangePi* in the example) located, remove this toolchain folder (rmdir should succeed with a fresh unpack, when it is already a link, use rm) and set a symbolic link to the fresh linaro one.

```
$ cd ~/somewhere/OrangePi/$ wget https://releases.linaro.org/components/toolchain/binaries/latest-5/arm-linux-gnueabi/gcc-linaro-5.5.0-2017.10-x86_64_arm-linux-gnueabi.tar.xz$ rmdir toolchain$ ln -s gcc-linaro-5.5.0-2017.10-x86_64_arm-linux-gnueabi toolchain
```

## Running the kernel build

Just stick to your User's guide again and do:

```
$ ./build.sh
```
