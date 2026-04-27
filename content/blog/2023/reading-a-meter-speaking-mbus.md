---
title: Reading a meter speaking MBus
date: '2023-01-16'
description: ''
categories:
- M-Bus
tags: []
---

Good day dudes and dudettes! I'm into software system architecture at least as much as I'm into coding. Otherwise, I could go on forever and a day about myself but the gist is, I'm friends with Mole and work for a company manufacturing metering devies. As such, I'm qualified to provide some insight into the metering bus. Or measurement bus, I'm guessing here.

# Scope of this article

This article assumes the [physical layer](http://the78mole.de/some-thoughs-on-the-m-bus) to be implemented. I'll get into what's needed to retrieve the application layer data. Decoding this data will be handled in another article, same applies to standard configuration options. You should be familiar with the [OSI model](https://en.wikipedia.org/wiki/OSI_model). No need to memorize all of that, the basic concepts suffice.

# Addressing

There's link layer (primary) & network layer (secondary) addresses. The former is a simple byte set in manufacturing or comissioning, the latter incurs a network layer state machine and is only required if you have hundreds of meters in a segment. On the upside, you get automatic address discovery.
Sticking to primary addresses, valid ones range from *1* to *250*. As for magic values,

- 0x00 Fresh meter, null address, so to speak. Should be changed to what you want it to be ASAP.
- 0xFE Broadcast with reply. The easy option if you got exactly one meter to work and/or play with.
- 0xFF Broadcast without reply. The way to go when you, in example, want to set the date/time of 250 meters, don't want to talk to each & every individually and don't want have a cacaphony of 250 ACKs.

# Frame types

The [standard](https://m-bus.com/documentation-wired/05-data-link-layer) defines separate control & long frames whereas in practice, it's the same with or without payload so I'm rolling them into one. Otherwise, let's go!

## Acknowledgement

0xE5
A general way for a slave to say "Yes, I understand you're talking to me". I am serious, it's not an "I confirm I've done what you asked". Not much of an issue in practice but an interesting factoid nonetheless. You can expect this as a response to all standard commands except *REQ\_UD2* (more on that below).

## Short frame

0x10 C A CS 0x16
Sent from master to slave, expecting ACK or a long frame in return.

## Long Frame

0x68 L L 0x68 C A CI Payload (optional) CS 0x16
Sent from slave to master or from master to slave. Latter bears no payload according to the standard, manufacturer-specific extensions with payload exist on the market though. Expecting an ACK or a long frame in return.

# Layers & fields

Both the L and CS fields are concerned with all upper layers. The L field in the long frame is a copy, by the way, not a single datum. You can use that as a quick'n'easy smoke test, just like the redundant header type byte. The checksum is literally what it says: a sum over all the bytes of the upper layers.
The A field is the primary address I've talked about earlier, in the simplest case of exactly one slave on your desk, take 0xFE.
The C and CI fields are a **c**ommand and a **c**ommand **i**dentifier. Or command and subcommand, that's a more logical way to think of this. Details follow.

# Frame control bit

Please don't call it it "FCB bit" :p Bit #5 in the C field shall get flipped upon every (successful) transmission (0x53 <-> 0x73). This is a simple, but rather effective mechanism of ensuring the two of you know you're really talking to each other. Ever noticed how your TV doesn't turn off when you turn it on, keep the power button depressed and (un)cover the transmitter? An FCB is one of the mechanisms used for that!
So basically, flip it every time you sent something (and got a response) and expect the slave to flip theirs as well. You can use this for flow control when reading multiple frames of data. This whole frame stuff is enough to fill an own chapter, which it'll henceforth do.
On the master side of things, you got control over your own FCB. The FCB on the slave(s), you have to reset yourself when establishing communication with an *SND\_NKE* which is a short frame with a C field of 0x40.

# Reading data

## Frames & framesets

Here's where things get really interesting. From a bird's point of view, meters have one or more data frames you can request (and even parse, if you so desire). And here's where the FCB gets really interesting! You see, if the meter got different frames to tell and you're keeping the FCB, the meter will output the same frame over and over again. On the other hand, if the meter doesn't flip its FCB, assume to get the same frame.
If the meter got multiple frames, you should start requesting and keep requesting subsequent frames until you get that desired last-frame marker. That's part of the application layer and I'll get into this later. Right now, the question is what to do when you stop reading prematurely. Got 2 frames and don't want the 3rd the next time? That's what the application reset is for.
An application reset is a long frame with a C field of 0x53 and CI of 0x50. And optional payload, of course, the payload denoting the application (operating/reading mode of the meter) and frame number. Nibble-wise, that is, in case you're into bit banging (which is a [real term](https://en.wikipedia.org/wiki/Bit_banging)). The details of frames & applications vary by manufacturer & device and might yield a ton of ['fun'](http://yosefk.com/blog/fun-at-the-turing-tar-pit.html) but there's a simple rule of thumb: an application reset sans payload resets the meter to some default state, same goes for a reset to 0/0 (so payload 0x00).
Once you've set everything up, you keep sending *REQ\_UD2*s (short frame with C of 0x5B) and decoding what you're getting.

## Data response

A reply to *REQ\_UD2* is an *RSP\_UD* which is a long frame with payload. This payload can exist in a fixed form or a variable one. The former is barely used as far as I know (and rather simple to decode), the latter's I'm very much familiar with and will get into later. Before, we'll get into headers!
The C field is a hard 0x08. The A field denotes the meter's primary address which you may or may not use for, uhm, purposes. The CI field tells us whether there's a header before the data, 0x72 means there is, 0x78 means there isn't. That's little-endian words, by the way. For big-endian, bit #2 is set.
For the header, I'd like to direct you to [chapter 6.3.1](https://m-bus.com/documentation-wired/06-application-layer). What it calls "Ident. Nr." is actually the secondary address so if you wondered, what your meter's is, here it is. The medium is described in [chapter 8.4.1](https://m-bus.com/documentation-wired/08-appendix).
And now, it's off to the [variable data structure](http://the78mole.de/mbus-application-layer/). Fasten your seatbelts, this one's a doozy!
