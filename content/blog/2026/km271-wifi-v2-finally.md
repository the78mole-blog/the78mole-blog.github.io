---
title: "Finally! KM271-WiFi v2.0 Digs Its Way Out of the Drawing Board"
date: '2026-11-25'
description: 'After years of "next revision, I promise", the KM271-WiFi gets a step-down converter, an ESP32-S3, flashing over USB, a simulated and reworked ground return and a parts list that no longer makes my wallet cry. Here is what changed and why.'
image: /images/blog/2026/11/km271-wifi-v2-title.jpg
categories:
  - Hardware
  - ESP32
  - Heating
  - Smart Home
tags:
  - KM271
  - KM271-WiFi
  - Buderus
  - Logamatic 2107
  - ESP32-S3
  - TPS62162
  - CP2102N
  - JLCPCB
  - KiCad
  - power supply
  - EMC
  - PCB layout
---

Some projects you finish. Others just stop bothering you for a while and then come back every time someone opens an issue titled *"ESP32 keeps resetting"*. The KM271-WiFi is firmly in the second group. Since I [first dug into the Buderus KM271](/blog/2021/reverse-engineering-the-buderus-km217) in 2021, the little board in the heating controller slot has gone through a long string of revisions (0.0.1 to 0.1.0), and the README carried the same two ToDo items for years: *flash over USB without an external programmer* and *replace the LDO by a step-down converter*.

Both of them are now crossed out. The **KM271-WiFi v2.0** is redesigned, the schematic is clean (ERC 0, DRC 0, no unconnected items), and the zero series is about to go into production. Finally.

![3D render of the KM271-WiFi v2.0 with ESP32-S3, mini USB socket and the new step-down converter](/images/blog/2026/11/km271-wifi-v2-iso.jpg)

## What Changed at a Glance

For the impatient surface-dwellers, here is the short version. The 0.1.0 column is the board you can find in quite a few Buderus basements by now.

| | 0.1.0 | v2.0 |
|---|---|---|
| MCU | ESP32-WROOM-32D | ESP32-S3-WROOM-1-N8R2 |
| 3.3 V supply | AZ1117 LDO | TPS62162 step-down (1 A, 2.25 MHz) |
| Power source | jumper J3 selects USB *or* Buderus 5 V | USB and Buderus 5 V diode-OR'ed (D8/D9), both at once |
| Input protection | – | SMAJ5.0A TVS on the Buderus 5 V |
| Flashing | external USB-serial adapter on the debug header | directly over USB (S3 native USB, CP2102N as option) |
| USB ESD | – | SRV05-4 TVS array |
| Bulk caps | 100 µF aluminium electrolytics | 220 µF low-ESR polymer |
| OneWire | via DS2484 bridge (optional) | directly on the MCU, populated by default |
| Ground return | – | simulated and reworked: one slot under the bus instead of four, about 18 % less ground resistance |
| Gone | I²C EEPROM, DS2484, test points, J3 | |

![The KM271-WiFi 0.1.0 with the PWRSEL jumper, the debug header and the ESP32-WROOM-32D](/images/blog/2026/11/km271-wifi-0.1.0-photo.jpg)

## 1. Goodbye LDO, Hello Buck

The old board fed its 3.3 V rail from an AZ1117 LDO, powered by the 5 V that the Logamatic hands out on its card edge connector. That works, mostly. But "mostly" is exactly the word that shows up in bug reports. A few users saw brown-out resets, and the reports in [dewenni's firmware repo](https://github.com/dewenni/ESP_Buderus_KM271/issues/57) mention spikes of several hundred millivolts on the supply during WiFi bursts.

Before throwing parts at the problem, I wanted to know *why*. So I modelled the Buderus 5 V as a source with an internal resistance Ri and simulated both supplies in ngspice with WiFi-like load steps (60 mA base load, +300 mA burst). The results:

- At **Ri = 1 Ω** both designs survive. The LDO's input sags to 4.64 V, the 3.3 V rail dips by about 60 mV. Not great, not terrible.
- But the LDO has little reserve. It needs roughly 4.4 V at its input to stay in regulation, so from about **1.8 Ω** it drops out, below **2.5 Ω** the rail is under the ESP32's 3.0 V minimum, and at about **4 Ω** it hits brown-out.
- The **TPS62162 buck** regulates cleanly up to about **3 Ω** and doesn't reach brown-out even at 6 Ω. The dip at the load step is below 5 mV.
- And because a buck converts voltage instead of burning it, it pulls **292 mA instead of 365 mA** from the Buderus for the same load. Less current means less voltage drop across Ri, even after paying ~0.38 V for the new input diode.

![Minimum 3.3 V rail voltage over the internal resistance of the Buderus 5 V supply: old LDO versus new buck, with 300 mA and 400 mA load steps](/images/blog/2026/11/km271-wifi-v2-ri-sweep.png)

So 1 Ω alone doesn't explain the resets. What does is everything that makes Ri bigger in a real basement: an aged electrolytic on the Logamatic's power board, mains ripple pulling its own regulator out of regulation in the troughs, an oxidised card edge contact (re-plugging the board fixed it for [at least one user](https://github.com/dewenni/ESP_Buderus_KM271/issues/99)), or the ESP32's RF calibration at boot drawing up to ~500 mA. The buck gives about 0.5 V more headroom against all of these, because it keeps regulating down to roughly 3.85 V at the connector.

The old LDO footprint is still on the board, by the way. U2 is now DNP, and a 0 Ω resistor (R78 for the buck, R79 for the LDO) selects which one feeds the rail. Old moles never burn all their tunnels behind them.

## 2. An ESP32-S3, and Why the Supply Had to Grow With It

The new board carries an **ESP32-S3-WROOM-1-N8R2**. The S3 has native USB, which is the key to the next section, but it also transmits with up to 1 dB more power and pulls peaks of about **355 mA** while doing so (the datasheet values aren't directly comparable to the old ESP32's, which are given at 50 % duty cycle). With CPU and peripherals on top, 400 to 420 mA is realistic.

With the old LDO, that would have been a step backwards: its Ri limit would shrink from 1.7 Ω to about 1.4 Ω. With the buck, I simulated the S3 worst case with a **+400 mA** step. The rail stays at 3.29 V at 1 Ω, the board draws 386 mA from the Buderus (about what the old board drew with the smaller ESP32 load), and brown-out only arrives at around 4.6 Ω. If someone's Logamatic is really weak, `output_power` in ESPHome can still trim the transmit peaks.

The first buck candidate, a TPS62203, only delivered 300 mA. That was tight for an ESP32 and plainly too small for an S3, so it got swapped for the **TPS62162** (1 A, fixed 3.3 V, WSON-8, 3 to 17 V input).

## 3. Flashing Over USB, at Last

Every board I've sold so far came with the same small ritual: grab a USB-serial adapter, wire it to the debug header, hold BOOT, press RESET, pray. The 0.1.0 had a USB socket, but it only delivered power.

On v2.0 the mini USB socket finally carries data. The S3's native USB (GPIO19/20) sits directly behind it, so the board shows up as a serial port and can be flashed straight from the browser with the [KM271-WiFi WebTools](https://the78mole.github.io/ESPhome-KM271-WiFi/). No adapter, no jumper wires, no third hand.

For recovery, there is a **CP2102N** USB-serial converter with the classic two-transistor auto-reset circuit on EN and IO0, plus TX/RX LEDs. Which path the USB data lines take is decided purely by population: R69/R70 (2.2 Ω, populated by default) route D+/D- to the S3, R87/R88 (DNP) to the CP2102N. Never both. An S3-only build can leave the CP2102N, the transistors and their resistors off the board entirely.

The 2.2 Ω series resistors are there for EMC and to limit the current through the ESD diodes of the SRV05-4. That part, incidentally, taught me a lesson during layout: it is *not* a flow-through device. The data lines now connect to both pins of each channel directly behind the connector, instead of passing "through" the chip as I had initially routed them.

And since the board now diode-ORs USB and Buderus power, the PWRSEL jumper J3 is gone. You can plug in a laptop while the board sits in the heating controller and nothing fights anybody.

## 4. Things I Took Out

Redesigns are as much about removing as adding. Out went the I²C EEPROM, which nobody used, the DS2484 I²C-to-OneWire bridge, and the test points TP1 to TP4. OneWire now runs directly on a GPIO with a 1 kΩ pull-up and is populated by default, so you can hang a DS18B20 on the board without ordering anything special.

## 5. Making It Cheap Enough to Build

A board that only I can afford to build isn't much of a product. So the last round of work went into the parts list, with JLCPCB's assembly service in mind:

- All 32 symbols and 24 footprints moved into a **project library**, so the KiCad project builds the same anywhere.
- The buttons became XKB TS-1187A (JLC basic part), the TVS array a SRV05-4, the bulk caps 220 µF/16 V Yunxing polymer caps with low ESR.
- The inductor **L1** went from a Würth WE-MAPI 4020 at 1.73 USD to a cjiang FTC252012S2R2MBCA at **0.035 USD**, with two second sources listed. That swap alone saves almost 17 USD per ten boards. Before swapping, I simulated both inductors in the TPS62162 circuit, first with my own switching model and then cross-checked against TI's PSpice model. In operation they're indistinguishable; the higher DCR of the cheap one costs 5.5 mW at 460 mA, about 0.3 percentage points of efficiency.
- A script (`scripts/export-jlc-bom.sh`) now generates the JLC BOM directly from the schematic. The hand-made one before it had a nasty habit: grouping parts by value and footprint only, so a single DNP part could quietly mark a whole group as unpopulated.

The result: about **15 USD in parts per board** for a ten-board run, including JLC's extended-part fees. PCB, assembly and shipping are on top, but that's a lot better than where I started.

The ESP32-S3 module is by far the biggest single item at around 4 USD, followed by the mini USB socket. Everything else is pocket change.

## 6. Where Does the Ground Current Actually Go?

With the schematic settled, I spent a whole night on something no BOM will ever show: the ground return path.

The KM271-WiFi has a shape dictated by its burrow. At the bottom sits the card edge J1 that plugs into the Logamatic, and next to it are two slots for the guide rail. So the left half with the power supply (buck, USB, CP2102N) and the right half with the ESP32-S3 are only joined by a bridge of roughly 25 × 25 mm above the card edge. Everything has to squeeze through there: the bus with 3.3 V, 5 V, USB, UART and reset, the lines to the Logamatic, and the entire ground return current between supply and radio.

![Board overview: supply on the left, ESP32-S3 on the right, and only a 25 × 25 mm bridge above the card edge in between](/images/blog/2026/11/km271-wifi-v2-gnd-overview.png)

My first EMC review had filed this as "ground bottleneck, medium priority". The obvious way to check it is to cut across the board at many places and add up how many millimetres of ground copper (F.Cu plus B.Cu) are left. Worst case: 15.4 mm, on B.Cu partly below 6 mm. Scary. Also partly wrong: two of the cut lines ran exactly along vertical traces. A trace like that eats a lot of the cut line but hardly hinders a current flowing across it from right to left. A cross-section tells you how much copper there is, not how well it conducts.

### Simulating the return current

So I computed the current itself, kept deliberately simple:

- Both ground layers are rasterised from the KiCad file (filled zones, GND pads, GND traces) on a 0.1 mm grid.
- Each cell is 35 µm copper, about 0.49 mΩ per square. The 349 GND vias connect the layers with about 1.5 mΩ each.
- 1 A goes in at the GND pads of the ESP32-S3 and comes out at the buck converter and its input capacitors. A second load case runs from the ground on J1 to the ESP.

That's a resistor network (a discrete Laplace equation) with about 800,000 nodes, solved in Python with `scipy` and `pyamg` in a few seconds.

![Current density of the ground return in F.Cu and B.Cu, 1 A from the ESP32-S3 to the buck converter](/images/blog/2026/11/km271-wifi-v2-gnd-current-density.png)

The heatmap shows where the current crowds: in the narrow strip directly above the row of 0 Ω bridges R33 to R44 at the card edge, at the corner of the left slot and along the top edge. In the middle of the bridge, F.Cu is taken by the bus and B.Cu is chopped into pieces.

### The real culprit: four slots under the bus

Why is B.Cu so chopped up? The exhaust gas sensor circuitry (C11, C12, R11, R17, R32) sits at the top next to its connector J5. Its four lines to J1 ran straight down on B.Cu to the bridges R35, R36, R39 and R40, right underneath the whole bus. So every bus line crossed **four slots** in its reference ground.

![B.Cu seen from above before the rework: the four exhaust gas lines (red) cross the bus (purple, dashed) at four places](/images/blog/2026/11/km271-wifi-v2-gnd-slots-before.png)

The model makes it cheap to try variants before touching the layout:

| Variant | ESP → buck | J1 → ESP |
|---|---|---|
| As drawn | 6.1 mΩ | 4.7 mΩ |
| Exhaust gas lines bundled into one slot | 5.5 mΩ | 3.9 mΩ |
| plus the B.Cu seam near J6 closed | 5.2 mΩ | 3.7 mΩ |
| B.Cu in the bridge completely free (theoretical limit) | 4.6 mΩ | 3.2 mΩ |

Bundling gets more than half of what is possible at all. Closing the seam near J6 and the level shifters U4/U5 adds only about 4 %, so that one stays as it is.

How bad is it in absolute terms? Harmless for function: the bridge contributes about 1.7 mΩ and roughly 5 to 8 nH, so the WiFi current steps produce a ground offset of a few millivolts. For EMC, the slots matter more than the cross-section. High-frequency return current wants to flow directly underneath its trace, and every slot forces a detour that enlarges the loop which radiates and picks up noise. Since USB is only used for flashing and as a backup supply, and the other bus lines are slow, the rating went down from "medium" to "low to medium". But a mole who has the simulator running doesn't stop at "low to medium".

### One night at the layout

With the model, every layout change can be re-checked in minutes. So I reworked the layout in several rounds and regenerated the heatmap after every save:

- **All four exhaust gas lines bundled.** C12 and R32 moved next to C11 and D5. Under the bus there is now one slot instead of four.
- **D5 out of the bottleneck.** Its line ran diagonally through the busy strip above the bridge row and cut off the GND pad of R34. Now it runs straight down next to C11.
- **Shorter Q1/Q2 emitter stubs.** The two auto-reset lines switch to F.Cu earlier, leaving shorter stubs on B.Cu.
- **More vias around the ESP module.** Over 30 extra GND vias around the module brought the biggest single jump.
- **Wider ground at the top edge.** C1 and C14 moved down by 0.8 mm to widen the GND strip along the edge.

![B.Cu after the rework: all four exhaust gas lines cross the bus as one bundle](/images/blog/2026/11/km271-wifi-v2-gnd-slots-after.png)

![Ground return resistance over the saved layout states of that night](/images/blog/2026/11/km271-wifi-v2-gnd-progress.png)

| State | ESP → buck | J1 → buck | J1 → ESP | of which bridge | of which module edge |
|---|---|---|---|---|---|
| Start | 6.08 mΩ | 1.76 mΩ | 4.71 mΩ | 2.26 mΩ | 1.18 mΩ |
| Final | 4.99 mΩ | 1.58 mΩ | 3.96 mΩ | 1.95 mΩ | 0.92 mΩ |
| Change | −18 % | −10 % | −16 % | −14 % | −22 % |

The funny part: bundling the exhaust lines barely moved the DC numbers, because the strip trapped between the four slots hardly carried any current anyway. For EMC it's still the most important step, since every bus line now crosses one slot instead of four and its return current can flow right underneath it everywhere else.

### The second bottleneck

Only the heatmap of the whole board revealed that there was a second narrow tunnel. At the left edge of the ESP32-S3 module, F.Cu is almost completely taken by the bus and B.Cu by a field of traces. The return current only gets out of the module through a narrow F.Cu strip along the top edge and around a row of parts. That section alone contributes 0.92 mΩ, almost half as much as the bridge everyone was worried about.

![Heatmap of the whole board in its final state, with both bottlenecks marked](/images/blog/2026/11/km271-wifi-v2-gnd-final.png)

The lesson I'm taking down into the burrow: a cross-section can make a bottleneck look worse or better than it is. Computing the current distribution costs a few lines of Python and a few minutes, and it shows directly where the current really flows and which change is worth the effort. Here it wasn't the card edge itself, but the exhaust gas lines running across under the bus.

## 7. A Side Excavation: The Exhaust Gas Sensor

While I had the simulator warmed up, I also checked a long-standing note in the schematic: *"Do not populate D5 to allow temperatures < 80 °C to be recognized."* D5 is a 5.1 V Zener on the exhaust gas sensor input. Using the NTC curve digitised from the Logamatic 2107 service manual, the simulation confirms it: with D5 fitted, the soft Zener knee starts pulling the voltage down below about 80 °C, and the Logamatic would show exhaust temperatures that are too high, by about 4 K at 50 °C and over 40 K at 0 °C. Above 80 °C the diode does nothing. So D5 stays DNP, now with numbers to back it up.

## What's Next

All the analyses, plots and scripts live in the [km271-wifi repository](https://github.com/the78mole/km271-wifi) under `DOC/` if you want to dig deeper, and the [how-to page](/pages/km271-wifi-howto) will get a v2.0 section once the first boards are in my paws.

Before the zero series goes to the fab, there's one more tunnel to finish: the **extension board** still needs its assembly data and maybe a few optimisations of its own. Once that's done, both go into production together. When the first v2.0 boards come back, I'll test them in my own Logamatic 2107 M and report here, including whether the brown-outs are really gone or whether I've just moved them to a deeper level of the burrow.
