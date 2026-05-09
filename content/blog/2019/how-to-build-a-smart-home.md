---
title: How to build a Smart Home
date: '2019-05-18'
description: ''
categories:
- ARM
- Smart Home
tags: []
---

Since everbody complains about smart homes are vendor lock in, too expensive, giving you data for free to some suspecting cloud provider,... I need to preset my smart home solution to you, that can be completely running inside your "four walls" and does not need any third party, if you do not want it to. Additionally, there is NO vendor lock in. Everything can be open source and connect to almost any existing smart home appliance.

What I'm talking about? It's iobroker.

If you already own a Homematic System from EQ-3 (ELV in older ages), iobroker is a must-have. BTW: If you already own a Charly, you can install iobroker on it without addional hardware, but be advised to install a USB drive with enough storage for the data that accumulates when years pass by. I would not suggest to use a flash based drive, since it needs a tradeoff between amount of data lost when power cuts and the endurance of your drive. Write cycles will be quite often...

Welp, where to start? I would first get some low-power and reliable mini PC. The solution I selected is from hardkernel and called [ODROID HC-1](https://web.archive.org/web/20251113103351/https://www.hardkernel.com/shop/odroid-hc1-home-cloud-one/) (in Germany best bought at [Pollin](https://web.archive.org/web/20241121065741/https://www.pollin.de/p/odroid-hc1-einplatinen-computer-fuer-nas-und-cluster-anwendungen-810766) for 60€). This is a little ARM board running ubuntu linux and providing space for a single 2.5" HDD. I selected a WD Red 1TB drive for that purpose. The linux OS itself needs to be put on a Micro-SD card.

I would suggest to also buy the following:

- Power supply (or a PoE+ adapter if you own a PoE+-capable switch)
- Micro-SD card with at least 8GB (best with ubuntu preinstalled)
- The serial cord from hardkernel
- The Battery (for RTC)
- A hard disk for all the data your smart home will collect and
- A little case against the dust, that definitely will render you appliance as very attractive ;-)

Start installing your software. First you need to install the Ubuntu OS, provided by hardkernel (if not already installed).

When everything arrived, connect it to your network, find out the IP address or use the serial cord and start installing everything you need (supposing, you do all under root, if not, prepend a sudo where needed):

- [node.js](https://nodejs.org/en/)
- [influxdb](https://www.influxdata.com/)
- [go](https://golang.org/)
- [yarn](https://yarnpkg.com/en/docs/install#debian-stable)
- [chronograph](https://github.com/influxdata/chronograf)
- [iobroker](http://www.iobroker.net/)

## Prepare your hard disk

```bash
dmesg  # Find out, which is your HDD, assuming /dev/sda
fdisk /dev/sda
# Create 2 Partitions
# 8 GB with swap
# Remainder with ext4 or something else (I prefer btrfs)
# write partition table with entering 'w'
mkswap /dev/sda1
swapon /dev/sda2
mkfs.ext4 /dev/sda2
mkdir /var/data
blkid /dev/sda2   # Take the UUID-part
echo "UUID=<the-above> /var/data   ext4 errors=remount-ro,noatime 0 1" \
  >> /etc/fstab
mount /var/data
mkdir /var/data/iobroker
mkdir /opt/iobroker /var/lib/influxdb
echo "/opt/iobroker/ /var/data/iobroker  none bind" \
  >> /etc/fstab
echo "/var/data/influxdb/ /var/lib/influxdb none bind" \
  >> /etc/fstab
```

## Installing node.js

```bash
sudo apt-get install python build-essential curl
mkdir src
cd src
wget https://nodejs.org/dist/v10.15.3/node-v10.15.3.tar.gz
tar xzvf node-v10.15.3.tar.gz
cd node-v10.15.3.tar.gz
./configure --without-snapshot
make
./node -v  # If version is returned than 'make' was OK
make install
```

## Installing InfluxDB

```bash
curl -sL https://repos.influxdata.com/influxdb.key | \
```

## Installing Go language

```bash
apt install git golang-go  # needed to build a newer go
cd /usr/lib
git clone https://go.googlesource.com/go
cd go
git checkout go1.12.5
cd src
./all.bash
cd $HOME
cd /usr/bin
rm go
ln -s ../lib/go-1.12 go
cd $HOME
cat >>.profile <<HERE
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
[ -d $GOPATH ] || mkdir $GOPATH
[ -d $GOPATH/bin ] || mkdir $GOPATH/bin
export PATH=$GOPATH/bin:$PATH
HERE
```

## Installing yarn

see: <https://yarnpkg.com/en/docs/install#debian-stable>

## Installing Chronograph

For creating your own querys to InfluxDB (e.g. with node red), it is easiest to have some good InfluxDB interface, best to be used in a browser...

With go and yarn, it is as easy as boiling water:

```bash
go get github.com/influxdata/chronograf
cd $GOPATH/src/github.com/influxdata/chronograf
make
go install github.com/influxdata/chronograf/cmd/chronograf
```

Now you can start chronograph

```bash
./chronograph
```

Now visit the chronograph web interface by browsing to `http://<host>:8888`. A Wizard will welcome you. Enter the appropriate data to access your InfluxDB. Youcan skip the Kapacitor question. After finishing the wizard, you should be able to see the following on chronographs Config tab.

![Chronograph Config tab screenshot](/images/blog/genral/no-mole-sorry.jpeg)

When this is done, issue your first query on the Explore tab (use the datapoint selector on the lower half of the page and select an appropriate date from the date picker in the upper right corner:

![Chronograph Explore tab screenshot](/images/blog/genral/no-mole-sorry.jpeg)

## Install iobroker

COMING SOON...
