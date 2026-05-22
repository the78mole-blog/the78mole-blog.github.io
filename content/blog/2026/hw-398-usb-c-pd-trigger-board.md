---
title: One USB-C Charger to Power Them All – The HW-398 PD Trigger Board
date: '2026-05-14'
description: A tiny solder-pad board that tricks any USB-C PD charger into outputting
  9 V, 12 V, 15 V or 20 V – perfect for ridding your burrow of the barrel-jack jungle.
image: /images/blog/2026/05/hw-398-size.jpg
categories:
- DIY
- Hardware
- Embedded
tags:
- USB-C
- PD
- power
- trigger board
- HW-398
- power-delivery
- hardware
- diy
---

Every mole eventually gets tired of the wall behind the workbench. Mine looks like a spaghetti farm: twelve-volt router brick here, nineteen-volt laptop lump there, a nine-volt barrel jack dangling in the corner like a forgotten stalactite. I have more power adapters than sensors, and that is saying something.

Then a batch order from AliExpress arrived. Tucked between a set of USB breakout boards and some random connectors was a strip of tiny PCBs, each no bigger than a postage stamp. Ten of them. Sixty-three euro-cents apiece. They were labelled **HW-398**, and they were about to become the most useful thing in the parts bin.

## What the HW-398 Actually Does

The board sits between a USB-C PD charger and whatever you want to power. It speaks the USB Power Delivery handshake fluently – PD 3.0/2.0, PPS/QC4+, QC 3.0/2.0, FCP and AFC – and convinces the charger that a device requesting a specific voltage is attached. The charger dutifully ramps up its output rail. Your load gets clean power. No laptop in sight.

The four selectable voltages are set by shorting one of the labelled solder pads to the adjacent resistor footprint:

| Pad label | Output voltage | Pad resistor         |
| ---       | ---            | ---                  |
| `9V`      |  9 V           | 51 kΩ (code `513`)   |
| `12V`     | 12 V           | 100 kΩ (code `104`)  |
| `15V`     | 15 V           | 14 Ω (code `140`)    |
| `20V`     | 20 V           | 180 kΩ (code `184`)  |

Leave all pads open and you get 5 V – the USB default, no negotiation required. Useful if you just need 5 V with a better connector than Micro-USB on the bench.

## The Chip Under the Hood

The IC is conspicuously unlabeled – whoever fabbed these boards wasn't feeling generous about their BOM. A little detective work points to the **Fastsoc FS312**: SOP-10 package, supports exactly the protocol list on the product page, and the recommended application circuit from the datasheet matches the board almost perfectly (add one cap and one resistor, connect, done). The setting resistors map cleanly to the FS312 datasheet values.

It is doing real USB protocol work: the handshake is actual USB traffic, reading and writing control registers over the CC line. This is not a simple voltage divider trick.

## Specifications

| Parameter | Value |
| --- | --- |
| Input | USB Type-C (PD) |
| Output voltages | 5 V (default), 9 V, 12 V, 15 V, 20 V |
| Max output current | 5 A (limited by the charger, not the board) |
| Protocols | PD 3.0/2.0, PPS/QC4+, QC 3.0/2.0, FCP, AFC |
| Board size | 23 × 11.5 × 4 mm |
| Indicator | Blue LED (dimmer at lower voltages) |

![HW-398 board next to a 2 € coin for size reference](/images/blog/2026/05/hw-398-size.jpg)

![HW-398 front view showing USB-C connector and pads](/images/blog/2026/05/hw-398-module-front.jpg)

![HW-398 back view showing output pads](/images/blog/2026/05/hw-398-module-back.jpg)

## Using It – The Three-Step Solder

1. **Pick your voltage.** Decide what rail you need. Write it down. A mole who solders the wrong pad at 2 a.m. will regret it.
2. **Short the pad.** Add a blob of solder bridging the labelled pad to the adjacent component. Use a fine tip; the board is tiny.
3. **Wire up the output.** The `+` and `–` pads on the far end accept any thin hookup wire. Solder, heatshrink, done.

![HW-398 voltage selection pads detail](/images/blog/2026/05/hw-398-closeup.jpg)

Plug it into a charger that supports PD and the blue LED lights up. Measure the output before connecting anything expensive – trust but verify.

## The Things That Will Bite You

**12 V is optional in the PD spec.** Many chargers skip it entirely. An Anker 313 (5 V/3 A, 9 V/3 A, 15 V/2 A, 20 V/1.5 A) silently delivers 9 V when asked for 12 V because 12 V is not in its capability list. The board falls back to the next lower supported voltage. That is standards-compliant behaviour – but it will absolutely fry a 12 V router if 9 V isn't enough to keep it happy, or worse, if the downstream circuit has no protection.

The rule: **always measure before connecting a load.** Set the pad, plug in the charger, read the voltage. Then connect the load.

**There is no regulation on board.** Whatever the charger outputs, that is what you get. The ripple and noise are entirely the charger's business. A cheap no-name brick and a premium GaN charger will behave very differently. For noise-sensitive loads, add a small bulk cap (100 µF, rated above your target voltage) close to the output pads.

**The USB-C connector is slightly inset.** The PCB edge overhangs the connector shell a little. Mounting into a panel cutout requires either a recess in the panel or some creative mechanical work. For bare bench use, no problem. For a finished enclosure, plan ahead.

**No LCSC stock on the FS312.** If you want to design the chip into your own boards, be aware that the usual EU PCB assembly houses cannot easily source it. You would need to pre-order the ICs separately.

## Where This Earns Its Place in the Parts Bin

- **Powering routers and access points** from a single USB-C GaN brick instead of a dedicated wall wart
- **Replacing barrel jack adapters** on anything that runs at 9 V, 12 V, 15 V or 20 V
- **LED strip drivers** – 12 V strips from a phone charger, no transformer required
- **Quick bench power** – solder a pad, clip on some probes, done
- **Embedded projects** where the finished device needs to run from whatever USB-C supply is nearby

At €0.63 each in a pack of ten, the risk of buying a dozen and having them in every project box is essentially zero. The mole recommends the 10-pack.

## One Caution Worth Repeating

Because the output voltage depends entirely on what the charger is willing to negotiate, you should treat this board as an **input device**, not a regulator. Always put a proper voltage regulator (LDO or buck converter) between the HW-398 output and anything that cannot tolerate the full PD voltage range. One mismatched charger, one firmware update to a charger that changes its capability advertisement, one well-meaning colleague grabbing the wrong brick – and suddenly your 9 V load sees 15 V.

For casual bench work and single-voltage projects with a known, fixed charger: fine. For anything that ships to a customer or sits unattended: add the regulator.

---

The barrel-jack wall behind my bench has not vanished yet. But there are now three HW-398 boards taped to a short USB-C cable running off the GaN brick that lives on the shelf, and the 9 V router, the 12 V LED strip, and the 20 V project in progress are all fed from the same charger. The stalactite in the corner is gone. Progress.
