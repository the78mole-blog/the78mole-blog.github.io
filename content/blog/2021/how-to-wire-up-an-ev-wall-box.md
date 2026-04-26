---
title: How to Wire an EV Wall-Box (the economic perspective)
date: '2021-05-18'
description: ''
categories:
- Electric Car
tags:
- BEV
- DoTheMath
- Electric Car
- Electric Vehicle
- Wall-Box
image: /images/blog/2021/05/openwb.jpg
---

Have you ever planned to install some wall-box for your new electric car? You have some technical/electrical skills but you are not sure, which wire to run from your building connection to the place where your wall-box will be installed? Then you found the right place to get some deeper thoughts about your intent.

In germany, there is currently some [promotional program](https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Ladestationen-f%C3%BCr-Elektroautos-Wohngeb%C3%A4ude-(440)/) to get 900 € when you install some private wall-box to charge electric cars. There are also some constraints to get the money from government:

- location shall be in germany and at some residential building
- the total price (wall-box + installation) needs to be at least 900 €
- installation needs to be done by an expert (running a business and can hand out an official invoice)
- the power shall be 11 kW (at least limited by firmware)
- the wall-box neds to be smart (capable to be controlled by network operator)
- the wall-box needs to be on the [KFW440 list](https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Ladestationen-f%C3%BCr-Elektroautos-Wohngeb%C3%A4ude-(440)/#)

I will assume, you already know, that you need an RCD Type B, if no DC fault current protection is integrated into your wall-box and all that other safety stuff. Nevertheless, in germany you will need an expert to get the sponsorship.

First of all, you should decide, if you want a software or hardware limited 11 kW equipment. In my opinion, even 3,7 kW will suffice, because you usually charge your car over night or during the day and for ultra-fast charging you will end up at some HPC station near some highway...

For further calculations, I'll assume, the cable run length from your building-connection to your wall-box is 10 meters and the wall-boy is of 11 kW type (not more). This means, you have 3 current carrying wires (3-phase) and 16A of current per phase. If you now simply look at some tabluar overview of DIN VDE 0298-4:2013-06, it says, you need at least 2.5mm² for this current (regardless where you run the wires, since 2.5 mm² can carry 24 A at least if used inside a protective tube).

OK, we are done, run NYM-J 5G2.5, that's all...

For sure, not! Let's take a little time to think about losses. 11 kW and 3 x 16A is a huge amount of power that is running through your wires and the maximum current from the standards just takes the self heating into account. If you intend to keep your pavement free of ice in wintertime, this is what you are searching for. Run the 2.5mm² wire up and down your pavement and you are done with it.

But now lets calculate the losses:

- Copper wire (0.0171 Ω\*mm²/m) of 2.5 mm² has a resistance of 6.84 mΩ/m
- 10m@16A => P = R \* I² => 10 m \* 0.00684 Ω \* 16² A = 17,5 W per Phase => 52,5 W losses

Compared with 11 kW, 52W seem not much, but let's continue. Assume, our car has 50 kWh of capacity and the battery has a lifetime of 2500 (0-100%) cycles. This means, we have a lifetime charge of 125 MWh. If we cycle it with 11 kW, it is equal to 11,364 hours of charging. Multiply this with 52,5 W and you get 593 kWh of losses. With a price tag of 0,30 €/kWh, this means 178 € of useless heat (for your first car..., second car adds the same price tag for heat only). We can normalize this back to 17,8 €/m of wire. I know, the losses will not go into your battery, and need to be supplied additionally, but it's just a first order approximation. It will be a bit worse in reality. The losses also do not mean a lot, but you can easily find a sweet spot with common wire gauges. Let's build up a little table for them:

|  |  |  |  |
| --- | --- | --- | --- |
| Wire Gauge | [Wire price](https://www.zaehlerschrank24.de/kabel-leitungen/mantelleitungen-nym-nhxmh.html)  (NYM-J 5Gxxx €/m) | Losses  €/m | Total €/m |
| 2.5 mm² | 2.40 | 17.78 | 20.18 |
| 4 mm² | 3.23 | 11.11 | 14.34 |
| 6 mm² | 5.00 | 7.41 | 12.41 |
| 10 mm² | 7.42 | 4.44 | 11.86 |
| 16 mm² | 11.89 | 2.78 | 14.67 |
| 25 mm² | 18.21 | 1.78 | 19.99 |
| 35 mm² | 29.19 | 1.27 | 30.46 |

Material and lifetime cost for different wire gauges per meter of length

Just for completeness, the NYY-J type (this one can be put into ground without protective tubes) has approximately the same price tag (2.20 €/m@2.5mm², 6.83 €/m@10mm²). Did you expect, that the 10 mm² cable has the best economic efficieny? OK, how long it will take to cycle the battery 2500 times? If you estimate 20 kWh/100km, we can run 625,000 km on this battery.

I did not yet dig the wire (yes, this is what moles do) below earth and also did not buy a wall-box (it's hard to get some electrician around my hometown), but I will decide on the 10 mm². This also gives headroom for some 22 kW wall-box after the minimum run time at 11 kW, given by the sponsorship rules.

Now have fun to dig the wires and give me some feedback on this article.

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+how-to-wire-up-an-ev-wall-box&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
