---
title: Get Your Personal Oil Well Level - Integrating OilFox Into Home Assistant using
  node-red
date: '2021-10-16'
description: ''
categories:
- Home Assistant
- node-red
- Smart Home
tags:
- home assistant
- node-red
- oilfox
image: /images/blog/2021/10/OilFox.png
---

After migrating from iobroker to Home Assistant, I lost the level of my oil tank in my smart home, being forced to have a look into the smartphone app. That was not satisfying, since I'm planning to calculate exact costs for heating from tracing the heat cost allocators back to the amount of oil burned (taking the way over some heat flow measurement devices). To see, how I got the data from the heat cost allocators, have a look [here](https://the78mole.de/wmbus-meters-and-how-to-get-it-into-home-assistant/), to get the data from the heat flow measument devices, look [here](https://the78mole.de/taking-your-m-bus-online-with-mqtt/).

Now, here is my little node-red flow to get the OilFox data:

![](/images/blog/2021/10/image-17.png)

[OilFox API node-red Flow (JSON)](/uploads/2022/11/OilFox-API.json)

It will retrieve the current OilFox data and put it into two entities of Home Assistant. The liters entity also contains some more attributes to be stored, like the timestamp, the OilFox sent it's data to the cloud and the size of the tank you entered during initial configuration of your OilFox device.

I got my information from this sources:

- [FHEM forums](https://forum.fhem.de/index.php?topic=101637.0)
- [SmartHome-Tricks](https://www.smarthome-tricks.de/software-iobroker/oilfox-2-in-iobroker-integrieren/)
- [ioBroker OilFox-Adapter](https://github.com/iobroker-community-adapters/ioBroker.oilfox)

If you know a way to get the history data from OilFox, let me know... I'll ask the OilFox-Team about it and will post it here, if I get an answer...

As always, have fun playing with your Smart Home.
