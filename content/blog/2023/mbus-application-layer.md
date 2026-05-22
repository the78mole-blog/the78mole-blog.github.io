---
title: MBus application layer
date: '2023-01-16'
description: ''
categories:
- M-Bus
tags:
- m-bus
- protocol
- metering
- specification
- networking
---

# Introduction

[Previously](/blog/2023/reading-a-meter-speaking-mbus) on this series, a payload was obtained from a meter over the EN13757 protocol.
[Chapter 6.3](https://m-bus.com/documentation-wired/06-application-layer), in a nutshell, means a variable-sized array of data blocks. Each block is a number with flags attached and you evaluate the flags when mapping to 'sensors'. If your data sink desires a power reading, you look for function field set to 'Instant' and quantity 'Power'. If you, on the other hand, desire to know when you had it flowin', you look for function 'Maximum' and quantities 'Power' & 'DateTime'.
This implies a variable type for the payload field and this is what it boils down to. Do yourself a favor and don't [stringly-type](https://wiki.c2.com/?StringlyTyped) it. A moral equivalent to *Variant<Null, DateTime, Real, Integer, Byte[]>* works well in practice.

# Parser overview

Inband communication, that is no dedicated control characters. Unsurprising for a binary protocol. On the flipside, every data block tells you how long it is so you always know when the next starts.
Every data block consists of a **d**ata **i**nformation **b**lock, a **v**alue **i**nformation **b**lock and a payload. Both the DIB and VIB consist of a **d**ata/**v**alue **i**nformation **f**ield 'starter' byte, as well as up to 10 extension bytes. Each highest bit indicates an extension byte following so you can easily pick the DIB and VIB from the front.

# DIB

Start chopping bytes off the front of the buffer and putting them onto the dissection table. Is the highest bit set? Continue chopping & putting. If not, the DIB's on your table and time's to dissect.
The DIB tells you

- The **payload length**, which is invaluable for decoding this whole thing in the first place.
- The **payload type**, which also helps in encoding.
- The **function**, which can be Instant, Maximum, Minimum, or Error (along the line of 'Cumulative energy during some error conditions').
- The **unit** is a number. Imagine having a power meter with 1 main and 2 auxiliary instruments. Those would get mapped to units 0 (main device) to 2.
- The **tariff** is supposed to be what it says on the tin, if there's different registers to fill when usage is high than when it's low (or, y'know, get creative), that's the field to look for.
- The **storage number** tends to get used for historical purposes. If you, let's say, got an energy reading from each of the last 24 months, they have to differ somehow. So the current reading gets a value of 0, the last month 1 and so on.

Extract all the information there is from the DIF (first byte of the DIB) and pile all the other ones on top as applicable. I won't go into details as [chapter 6.3.2](https://m-bus.com/documentation-wired/06-application-layer) does so already. Pay the following chapter a visit as well, that's the last-frame marker I've talked about [previously](/blog/2023/reading-a-meter-speaking-mbus).
All that unless it's one of those special functions 0x1F and 0x0F. Those denote a manufacturer-specific area following. Sans a length, this ranges from the next byte til the very end of the buffer. Skip the next 2 sections.

# VIB

The basic flow is the same, you chop off bytes until you got the whole thing and then you dissect it. You can of course dissect while chopping, but that aproach yields a terrible debugging experience. The VIB denotes

- The **quantity** is an actual physical measurable quantity, such as your total energy spent in this month. Could also be an abstract number such as the meter's serial number and a couple other things.
- The **modifier** (or orthogonal extension if you like it fancy) is another quanity which extends the previous one.
- The **unit**, as in 'actual physical unit'. I personally prefer a null-like value for this field for timestamps (software correctness & stuff), otherwise it could be something like J, m³ or h. Or gallons or MBTUs which are aktually kilo-BTUs (1MBTU = 1000BTU, Brits are weird) or whatnot. Were it for me, there would be plain & simple SI units there and billing systems would convert this stuff but hey, it's not like we sent man to moon with the SI or something...
- The **exponent** is what it says on the tin, that x you put into 10xto multiply the payload to the apropriate scale. Somewhat similar to [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754-1985) in spirit and easy to implement.

Decoding the VIB is a mess of tables described in [chapter 8.4.3ff](https://m-bus.com/documentation-wired/08-appendix). Start with the primary table and put the first byte in there. If you get a final answer, grab yourself a tee, a beer or whatever it is you grab to celebrate something nice happening. What about a cat?
You may also get a referral to another table. There's a couple of them, I can't say it's structured in any sensible manner, using tables (switch expressions, if you can afford them, are neat) for control flow is the way to go here. Someday, somehow, you'll reach a final answer, and then you can [grab a cat](https://stray.game/).
Or maybe not because you may still have VIFEs (**e**xtensions) left after the last table ended. That's because there are orthogonal extensions. Those may change quantities & units (energy -> power) or introduce modifiers, such as the previous timestamp example. Another one would be a negative modifier to idincate, let's say, volume from times with negative flow.
Then there's weird stuff such as the actual VIB being encoded in an ASCII string following the binary VIB. And don't get me started on the compact profile...

# Payload

After swaths of bit manipulations, the rest is straightforward. You take however many bytes indicated by the DIB and parse it accordingly. I personally don't see the point of BCD values when binary integers do the job just fine but [Moore's law](https://en.wikipedia.org/wiki/Moore%27s_law) & stuff.
Depending on the quantity, you may have to massage the preliminary result some more. Classically, physical readings will get delivered with an exponent so you have to scale accordingly, likely requiring a real number in the process. Things like serial numbers, on the other hand, get used in integer form obtained in the first step. And if it's something fancy, such as manufacturer-specific error flags, you may very well keep the buffer as-is and delegate post-processing this mess to a higher layer.
Well, I lied about bit stuff being over. You may get a timestamp in a type F, G or I. [Chapter 8.2](https://m-bus.com/documentation-wired/08-appendix) isn't exactly helpful, a code example is about to follow.

# Manufacturer-specific data

An important function this area serves is the last-frame marker. A DIB of 0x1F means there's more frames following, an 0x0F means you can stop.
Otherwise, not much to say here, really. Here be dragons. If you are a better shot at reverse-engineering than I am (which isn't a high bar to clear), you may have some fun with this but I'd go to the manufacturer for documentation.

# Wrap-up

There's a couple ways to proceed from here. One is to iterate through all the data blocks, inspecting flags as you go. My preferred one is outlined in the example above, that is starting with the gauges I want to feed and picking the right flags from the dataset.
In my experience, decoding those data blocks and visualizing them in the debugger with relevant properties pinned is an effective way to aproach data mapping.
