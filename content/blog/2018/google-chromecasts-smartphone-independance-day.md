---
title: Google ChromeCast's (Smartphone) Independance Day
date: '2018-11-05'
description: ''
categories:
- Uncategorized
tags: []
---

Have you ever been upset about your chromecast heavy depency on a smarthphone. So, nor do I, but my wife complained, since she always drops her phone somewhere else around the house... What could you do about it? Chromecast hardly has other input options and writing against it's API is not an easy task.

I'd not be an embedded electronics engineer, if I would not have a solution to that... My house currently runs an [EQ-3](https://www.eq-3.com/start.html) (former part of ELV, now two somehow independent companies) homematic smart home and around 80 nodes connected to it, anything from simple wireless switches to RGBW-Led-Stripes. If you put an [Odroid HC-x](https://www.hardkernel.com/main/products/prdt_info.php?g_code=G150229074080) beside with iobroker running on it, connecting the world is not enough :-). But EQ-3 also offers nice modules for makers like the [HM-MOD-EM-8](https://www.elv.de/homematic-8-kanal-sendemodul.html) for just a few bucks. Equipped with that module and some Bread-Board, there is nothing as easy as building a 8-Button HMI. Since it is not a hard task (only a few wires and some buttons), I decided to give [ALLPCB](https://www.allpcb.com/setinvite.aspx?inviteid=41374&url=https://www.allpcb.com/) a try, sketched a shematic and a PCB within KiCAD (for my first time) and ordered it from ALLPCB. Since I plan to distribute some more of these gadgets around my house, I ordered 30 for just $1.50/piece.

Here is the result:

![](/images/blog/2018/11/IMG_20181105_192130.jpg)

Now, just install the iobroker.scenes and iobroker.chromecast plugin and feel free to connect your buttons to scenes. Your Chomecast is now free like Willi ;-)

And here are the KiCad-Design files:

[hm-mod-em-8-switcher](https://blog.the78mole.de/wp-content/uploads/2018/11/hm-mod-em-8-switcher-master@e4c62484a59.zip)[Download](https://blog.the78mole.de/wp-content/uploads/2018/11/hm-mod-em-8-switcher-master@e4c62484a59.zip)
