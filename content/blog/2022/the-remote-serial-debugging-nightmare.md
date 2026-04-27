---
title: The Remote Serial Debugging Nightmare
date: '2022-01-31'
description: ''
categories:
- ESP32
- ESPhome
- Networking
- Windows
tags:
- com2tcp
- ESP32
- Serial2Ethernet
- StreamServer
image: /images/blog/2022/01/serial-device-server.jpg
---

Everybody playing around with hardware that has a serial port and is not located close to the desk will sooner or later run into the problem, that the wire simply gets to long for a serial connection, especially with non EIA-232/RS-232, known as serial-TTL-UART.

Especially for debugging such hardware protocols, it is nice to have a terminal program, that also shows hex output and can understand hex input. Hterm is one of my favorite programs, when it comes to debugging serial stuff from a microcontroller.

Unfortunately, hterm is neither open source, nor does it support TCP-serial-bridges directly. And also many other tools lack some stuff. While Putty can simply use it's telnet protocol, it is missing a hex dump and input.

If you still want to use hterm, you have mostly three options (the latter two are mostly the same but differ in price):

- Using a virtual COM port software (e.g. [com2tcp](https://github.com/u-blox/com2tcp), has an unsigned driver :-( )
- Buying a professional/dedicated seriel2ethernet server (like in the picture of the post)
- Use another ESP32/ESP8266 to create your own serial2ethernet server (quick hint: disable logging with `baud: 0` setting to use the USB serial port for this)

Both solutions are not the best choice in my opinion, because with ESPhome StreamServer Component (using telnet as transport), you already have a serial port over TCP available. To why not connect directly using telnet.

### Tera Term - Not best in class, but all you need

If you install e.g. [StreamServer](https://github.com/oxan/esphome-stream-server) (yes, it is f\*\*\* easy to deploy) on your ESP32 or you use [ESP-Link](https://github.com/jeelabs/esp-link) for ESP8266, you have the serial port you want. Now you need the appropriate terminal program to connect to it.

It perfectly works with putty, if you only want to send and receive ASCII text, just select telnet and enter the IP and port of your ESP.

But when it comes to hex (like in my [Buderus KM271 post](https://the78mole.de/reverse-engineering-the-buderus-km217/)), you are simply lost with putty and you also can not easily connect hterm to it, without using a nasty com2tcp tool, running long wires or using the mentioned helper-ESP.

After configuring tera term appropriately, it seems to work quite well. Not as good as hterm, but better than the other options:

![](/images/blog/2022/01/image-2.png)
