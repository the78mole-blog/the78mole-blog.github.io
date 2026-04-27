---
title: Compile Ceph (master) on ARM (32-Bit)
date: '2019-01-06'
description: ''
categories:
- ARM
- Ceph
- Storage
- Uncategorized
tags:
- ceph
---

I gave up on getting Ceph run on ARM 32 bit. It was a huge effort to fix the types, that diverge when switching from 64 to 32 bit. The development of Ceph is simply to fast to cope with. Since the developers decided to drop all tests for 32 bit builds, the needed fixes are too many for a single person to hunt after it.

**TODO**: Test this all on a virgin armhf system (raspberry, odroid hc1/2/XU4,…) and complete the TODOs for openssl and phantomjs (and the sass-dependency). Maybe with the new master tree, it is not needed to build it outside the ceph repo.

First install prerequisites:

```
sudo apt install python-pip build-essential libgmp-dev \  libmpfr-dev libmpc-dev reprepro
```

Install nodejs from nodejs.org

```
curl -sL https://deb.nodesource.com/setup_11.x | sudo -E bash - sudo apt-get install -y nodejssudo npm install -g npm
```

Then prepare a swap partition (you will need it ;-) )

```
dd if=/dev/zero of=/<some-hdd-path>/swapfile \  bs=1M count=8192 progress=statusmkswap /<some-hdd-path>/swapfileswapon /<some-hdd-path>/swapfile
```

Then we should install some dependencies

```
sudo apt install libgmp-dev libmpfr-dev libmpc-dev ruby
```

Now install a new GCC that supports C++17.

```
wget https://ftp.gnu.org/gnu/gcc/gcc-8.2.0/gcc-8.2.0.tar.xztar xfJ gcc-8.2.0.tar.xzcd gcc-8.2.0./configure                      # for armhf# ./configure --disable-multilib # for x86_64/arm64make
```

Building ceph with do\_cmake, building a debian package with make-debs.sh or simply build packages using another compiler than the debian default one (6.3.0) requires you to change the default compiler e.g. to gcc-8.2.0 for the whole system:

```
sudo update-alternatives --install /usr/bin/cc cc /usr/local/gcc-8.2/bin/gcc-8.2 50sudo update-alternatives --install /usr/bin/c++ c++ /usr/local/gcc-8.2/bin/g++-8.2 50
```

Checkout OpenSSL-1.0.2-stable (seems also necessary for armhf), PhantomJS, compile and install it:

```
cd /opt/GITgit clone git@github.com:openssl/openssl.gitcd opensslgit checkout OpenSSL-1_0_2-stable...TODO...# Following seems only necessary on arm # (or all platforms wihtout precompiled binary)cd /opt/GITgit clone git@github.com:ariya/phantomjs.gitcd phantomjs...TODO...sudo LD_LIBRARY_PATH=/opt/openssl_build_stable/lib/ \  deploy/package.sh --bundle-libs
```

Add the following to build.py (at L:244, just after PlatformOptions.extend)

```
phantom_openssl = os.getenv("PHANTOM_OPENSSL_PATH", "") if phantom_openssl != "":    openssl = os.putenv("OPENSSL_LIBS", "-L" + phantom_openssl + "/lib -lssl -lcrypto")    openssl_include = "-I" + phantom_openssl + "/include"    openssl_lib = "-L" + phantom_openssl + "/lib"    platformOptions.extend()    print("Using OpenSSL at %s" % phantom_openssl)
```

Then install it to /opt

Build and compile Ceph

```
git clone git@github.com:the78mole/ceph.gitcd cephgit checkout wip-32-bit-arm-fixes./install-deps.sh./do_cmake_arm32.sh   # for armhf# ./do_cmake.sh       # for x86_64/amd64 or arm64cd buildmake -j4# if it gets really slow due to swapping, break an do make -j1 # or use the scheduler-script from link below
```

Here you can find a rudimentary (but working) script that suspends compilers processes based on total compilers memory consumption. Running it through 'watch'-tool you can start e.g. 8 tasks and when memory limit is reached, it will suspend (kill -TSPT) the youngest tasks in sense of user space runtime.  
<https://github.com/the78mole/scripts/blob/master/linux/bash/schedule_compile.sh>

Now do...

```
cd ..   # Back to ceph base dir./make-debs-arm32.sh   # for armhf# ./make-debs.sh       # fox x86_64/amd64 or arm64
```

If you encounter problems with setuptools (Exception --> TypeError: unsupported operand type(s) for -= 'Retry' and 'int') try to get a more recent version of python pip with the following commands and rerun make-debs-arm32.sh.

```
apt-get remove python-pip python3-pipwget https://bootstrap.pypa.io/get-pip.pypython get-pip.pypython3 get-pip.py
```

If I forgot anything to make it work, feel free to write some comment...
