---
title: Intensive Underground Metering - An RJ45 Breakout for Connecting Your Meters
  Through Ethernet Cabling
date: '2023-06-01'
description: ''
categories:
- Bus Systems
- ModBus
- Smart Home
- Hardware
- DIY
tags:
- Isolated ModBus
- ModBus
- RS485
- networking
- metering
image: /images/blog/2023/06/MBRJ45BO2-Front.png
---

Again, I quickly developed a gadget to ease my life as a data collecting mole. ModBus adapters mostly have three drawbacks. Firstly, they have open wires, secondly, if you route them over RJ45, you waste many wires (ModBus usually needs 2-4 wires) and termination is a mess. OK, you can easily stick to Victron's solution, as their MK3 already has RJ45 as a plug, but still, you can not simply break out an RJ45 wire for meters, distributed accross your house.

Also, if you try to solve it with the common break out solutions for RJ45 e.g.,

- [Delock 66992 (Reichelt)](https://www.reichelt.de/de/de/shop/produkt/rj45_buchse_terminalblock_hutschiene-347936)
- [Delock 66993 (Reichelt)](https://www.reichelt.de/de/de/shop/produkt/rj45_buchse_terminalblock_hutschiene_gewinkelt-347937)
- [Delock 65527 (Reichelt)](https://www.reichelt.de/de/de/shop/produkt/modular-kupplung_rj45_buchse_terminalblock-148849)
- [Delock 66948](https://www.reichelt.de/de/de/shop/produkt/rj45_buchse_terminalblock_mit_drucktaster_adapter-327001)
- and many more...

you will end up with an expensive, very fragile solution and still need to have a converter from USB to ModBus/RS485, not speaking of termination.

The solution I want to present makes these challenges a bit more easy. It contains a dual USB-serial converter, isolated or non-isolated RS485 transceivers, jumpers for termination and many other assembly options. If you only populate the connectors (and a few chicken feed parts), you have a passive break out. If you populate a single transceiver and the wire connectors, you get mostly a default USB ModBus converter and if you populate everything, you have a gateway to your meter system.

And here are some of the pictures:

![](/images/blog/2023/06/IMG_MBRJ45BO2_Full_Case_Open-1024x576.jpg)

![](/images/blog/2023/06/IMG_MBRJ45BO2_Full_Bottom-1024x780.jpg)

![](/images/blog/2023/06/IMG_MBRJ45BO2_Full_Case-1024x576.jpg)

### Initial Bring-Up of the Prototype

When bringing up the fully populated device, I realized, that I had two issues in the HW:

1. The signals of the isolated RS485 transceiver have been swapped (A ↔ B)
2. The RX not-enable needs to be joined with TX enable for modbus clients/masters to work properly, beacuse these SW seems not to be able to mask the bus echo, that happens on a half-duplex RS485 bus

A fixed version of pre-1.0.0 looks as follows :-)

![](/images/blog/2023/06/IMG_MBRJ45BO2_Full_Case_Open-Fixed-1024x576.jpg)

You can find all sources for the fixed board on [GitHub](https://github.com/the78mole/ModBus-RJ45-Breakout-2) as a KiCad project and also Gerber files for production.

## The Software Sauce

To evaluate the functionality of the board, I connected a standard USB-RS485-converter to the same bus, where my breakout and a WAGO Energy Meter (MID) 879-3000, configured (using Bluetooth) to have the Bus ID 100 and a ModBus rate of 115200 Baud. For remotely accessing the USB-RS485-converter, I installed ser2net on a linux PC and made the serial interface available on a TCP port. As the terminal to access it, I used CoolTerm, since it is one of the few, that support connecting to a TCP serial without nasty Virtual COM port drivers (see my [post about serial debugging over network](https://the78mole.de/the-remote-serial-debugging-nightmare/)).

When I now execute the following line on the linux device connected to my breakout board...

```bash
mbpoll -m rtu -P none -b 115200 -a 100 -t 4:hex -r 0x4001 -c 2 /dev/ttyUSB2 -v -1
```

...I can see the response...

![](/images/blog/2023/06/image.png)

...and what the debug probe sees in CoolTerm...

![](/images/blog/2023/06/image-1.png)

`mbpoll` has some bug, I believe. If you request address 0x4000 with count 2, it will request 0x3FFF and 0x4000. This is, why in the examle above I requested 0x4001, to get the correct data of register 0x4000. I already added my 2 cents to an issue on the mbpoll Github project.
