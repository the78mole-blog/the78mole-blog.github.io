---
title: Integrating wmBus devices into iobroker
date: '2019-10-13'
description: ''
categories:
- Bus Systems
- iobroker
- Linux
- Smart Home
- wmBus
tags:
- iobroker
- wmBus
image: /images/blog/2021/07/MBusWirelessLogo-1.jpg
---

Since I've replaced ioBroker with Home Assistant, I also wrote an [article about integrating M-Bus devices](https://blog.the78mole.de/taking-your-m-bus-online-with-mqtt/) via MQTT with HASS. Another post, doing the same with wmBus can be found [in the wmBus Home Assistant integration article](https://the78mole.de/wmbus-meters-and-how-to-get-it-into-home-assistant/).

After my quite expensive MH-Collector (identical with the easy.MUC from solvimus) died (it survived just a little longer that warranty protects), I decided to collect my wmBus devices' data with some home brewn solution. I'm also the owner of a Ubiquity US-24-250W, so the descision to go with PoE supply is quite an easy descision. So what lies closer than using a Raspberry Pi 3B+ with PoE hat and an USB-wmBus stick?

No sooner said than done, I bought the parts, installed raspbian and an iobroker slave. The iobroker master ist now running on a Debian 10 buster VM on my tiny HP Proliant server... How to install the iobroker slave can be found [in the iobroker documentation](https://www.iobroker.net/docu/index-24.htm?page_id=3068&lang=de).

## wmBus Hardware

For me, the appropriate hardware was the [IMST iM871A-USB](https://www.wireless-solutions.de/products/gateways/wirelessadapter.html) (you can buy it directly from IMST or from [tekmodul](https://www.tekmodul.de/produkt/im871a-usb/)). This wmBus stick provides a serial interface (e.g. /dev/ttyUSB0), is quite cheap and supported by most open source wmBus software. But here comes the tricky part. There are quite some paths you can go, but for me, using the Messhelden heat cost allocators, I found myself in a very frustrating situation.

EDIT: As I found out a few days ago, libmbus seems to not pad the encrypted data correctly, so that decryption is wrong, when data is not aligned. In newer versions it seems, that they have zeroed the encrypted data buffer before use and that did the trick. At least, wmbusmeters now works correct in recent versions (checked 2021-07-10).

~~These devices stick to the OMS standard for most of the telegram, but unfortunately do some very shitty stuff at slot 2 and 3, so many decoders fall out of sync just after the first data slot.~~

## wmBus Software

After trying different iobroker adapters (like [iobroker.wm-bus](http://github.com/soef/ioBroker.wm-bus)) and also deamon solutions (like [wmbusmeters](http://github.com/weetmuts/wmbusmeters)), sending the data to some MQTT broker (a server is easy to rise up in iobroker), I ended with the [iobroker.wmbus](https://github.com/ISFH/ioBroker.wmbus) (beware of the dash, it is not the same as above). Somehow the author of this adapter managed to come up with the inconsistencies, I even could not decode manually, looking at each single bit and byte of the wmBus telegram.

EDIT: Yes, because decryption produced crap and crap can not be decoded :-(

After attaching the iM871A-USB stick to the Pi and placing it at some location where it can receive all meters you are interested in, you need to install and configure the iobroker adapter iobroker.wmbus.

## Adapter Configuration

The configuration is also quite easy and should look like the following:

![Adapter configuration screenshot](/images/blog/general/no-mole-sorry.jpeg)

It could also be, that your slaves need other modes to be received. One widespread mod for battery driven devices is also mode C. Unfortunately, a single stick can not receive multiple modes. But usually you only run devices with a single mode. Another important setting is the baud rate. For the IMST device, it needs to be 57600. The stick contains some serial converter that attaches the IMST module with a real serial connection.

## Add Encrypted Meters

After finishing configuration and starting up the adapter, it is time to have a look into the log. There you will see, if the adapter started up correctly. If it did, you soon should see a line that says `Updated device state: <MANUF>-<ID>` or an error saying, that it could not decrypt a telegram due to missing decryption key. If this occurs, go to the adapter configuration again. There you should see a new entry with a key "UNKNOWN". Place the correct key there and push "Save".

![Decrypted device state in object tree](/images/blog/general/no-mole-sorry.jpeg)

The follwoing telegram of that device should be decrypted correctly and a new state will be created within the object tree of iobroker.

If you see other unencrypted devices that pollute your object tree or your log with encryption failed messages, simply put them below "Blocked Devices" tab in the adapters configuration. My Pi can see at least 20 unencrypted Techem water meters and heat cost allocators.

## Let's encrypt (also on wmBus)

I don't know, how they can survive in a time of GDPR (General Data Protection Regulation), but they still have no hurry to encrypt their telegrams with a device-unique key. I think it is a security issue, when burglars can easily find people that do not heat in wintertime or have no water demand currently. But at least, Techem sticks closely to the OMS. If you rent a flat, that still has unencrypted wmBus meters, I would definitely claim to get encrypted meters. Even if encryption of wmBus has some weaknesses, it is by far better than plaintext.
