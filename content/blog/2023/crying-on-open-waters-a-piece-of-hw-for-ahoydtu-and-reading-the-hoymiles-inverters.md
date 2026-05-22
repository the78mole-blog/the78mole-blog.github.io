---
title: Crying on Open Waters - A Piece of HW for AhoyDTU and Reading the Hoymiles
  Inverters
date: '2023-09-12'
description: ''
categories:
- ESP32
- Renewable Energy
- Smart Home
- Solar Energy
- Hardware
- DIY
tags:
- ahoyDTU
- DTU
- ESP32
- hoymiles
- solar
- inverter
- energy
- monitoring
image: /images/blog/2023/09/PXL_20230805_092751600.jpg
---

It's quite some time ago, I wrote my last blog post. But I had a lot to do and there have been quite action, creating some material for new posts. My father decided to build solar on his roof and he decided to go bold. The result will be a 8 kWp solar and 14,4 kWh battery. To even harvest the sun in the shadow efficiently and just because it CAN be done, he also decided to add two micro inverters with four panels, 425 Wp each. And he wants to get real-time readings from this two micro inverters.

So i decided to go with hoymiles, because the radio protocol is already reverse engineered and there are two projects supporting it on ESP32 with low-cost HW. But instead of buying something ready2run, I want to go with an own design. I already built a "wire-hedgehog" to test it out and it seems to work beatifully.

![](/images/blog/2023/09/image-1024x857.png)

And you can already access the WebUI of AhoyDTU. But you can also put OpenDTU on it.

![](/images/blog/2023/09/image-2.png)

Thats great, but I want to go with something that has a better handling than the wired up version. So I designed an own board.

![](/images/blog/2023/09/image-1.png)

I'll order this together with a new batch of my [Buderus KM271 WiFi Clone](https://the78mole.de/reverse-engineering-the-buderus-km217/). It will possibly available also on tindie, when I assembled and tested it extensively.

You can find the sources (KiCad) im my [moles-Integ-DTU-HW GitHub repository](https://github.com/the78mole/moles-integ-dtu-hw).

If you want to integrate it into Victron VRM, you can find a solution here: <https://github.com/henne49/dbus-opendtu>

Stay tuned to get some updates and keep digging ;-)
