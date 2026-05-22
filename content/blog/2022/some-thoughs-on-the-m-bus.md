---
title: Some Thoughs On The M-Bus
date: '2022-10-04'
description: ''
categories:
- Bus Systems
- M-Bus
tags:
- M-Bus
- metering
- protocol
- rs485
- iot
- networking
image: /images/blog/2021/07/HASS-MBUS-MQTT-1.png
---

After some discussion on the home assistant community forum about ESPhome and the M-Bus and the M-Bus in general, I decided to write a little post about the baiscs of M-Bus. My [previous post on M-Bus](https://the78mole.de/taking-your-m-bus-online-with-mqtt/) used the libmbus on a raspberry just used it to communicate with a meter. For integrating some own master or slave, a deeper understanding is required and this post tries to serve this purpose.

The information you get on <https://www.m-bus.com/documentation> is way to complex to understand, at least in my opinion. So, I'll give it a try :-)

## The Hardware Part

First of all, the electronics is quite easy to understand. The master transmits by modulating the voltage of the bus between around 24 (logic '0' = "space") and 36 (logic '1' = "mark") volts, the slave responds by stimulating it supply current in a range from 11 to 20 mA = '0' = "space" (and <1,5 mA = '1' = "mark"). The M-Bus mentiones also unit-loads of 1,5 mA (usually a slave) that shall keep mostly constant over time. As soon as you reach 5 unit-loads, it get's close to the 10 mA of minimal signalling current and therefore it leads to ambiguity. This makes it difficult to develop master circuits that can handle more than 5 slaves.

Additionally, the current signalling from slave to master makes it a bit difficult to listen (sniff) especially to responds from slaves, because the current can not be easily tapped as you can do with the voltage. To achieve it, the easiest way is to find out the polarity of the wires (M-Bus in general is insensitive to polarity) and then hook up a shunt and connect some simple components to it (the IC is some LM393 from TI):

![](/images/blog/2022/10/image-1.png)

Since M-Bus is by definition unidirectional and always driven by the master, you could also sniff the data with a sinlge USB-serial converter. The circuit shown has some drawbacks:

- It is not isolated and can destroy your converter and your PC
- It must be initially calibrated and re-calibrated when slaves are added and removed

I maybe will create a more sophisticated sniffing circuit in future, that can handle isolation, can emulate a slave, integrates a master with more than 5 slaves,... But currently, this would just be too much for the topic of this post.

## The Protocol Sauce

The M-Bus protocol is quite easy on the lower levels. It just defines a hand full of transmission rates (2400 Baud by default), even parity and one stop bit (2400 8E1).

All telegrams are in general built of a few named fields and possibly data. The meaning of the identifiers is as follows:

- C = Control
- A = Address
- CI = Control Information
- L = Length (one byte, transmitted twice)
- CHKSUM = Checksum = arithmetical sum of specfic parts of the telegram

There are 4 types of telegrams, values for the checksum calculation are in curly braces:

| Telegram Type | Content |
| --- | --- |
| Single Character | 0xE5 |
| Short frames | 0x10 +  { C + A } + CHKSUM +  0x16 |
| Control Frames | 0x68 + 0x03 (L) + 0x03 (L) + 0x68 +  { C + A + CI } + CHKSUM +  0x16 |
| Long Frames | 0x68 + L + L + 0x68 +  { C + A + CI + <USER DATA> } + CHKSUM +  0x16 |

Types of telegrams, parts in curly brackets are relevant for the checksum

Mapped to the so called transmission services, the telegram types show as following (the meaning of the different C-values will be discussed later)

| Name | C-Field | Telegram | Description |
| --- | --- | --- | --- |
| SND\_NKE | 0x40 | Short Frame | Initialization of Slave |
| SND\_UD | 0x53 0x73 | Long/Control Frame | Send User Data to Slave |
| REQ\_UD2 | 0x5B 0x7B | Short Frame | Request for Class 2 Data |
| REQ\_UD1 | 0x5A 0x7A | Short Frame | Request for Class1 Data (see 8.1: Alarm Protocol) |
| RSP\_UD | 0x08 0x18 0x28 0x38 | Long/Control Frame | Data Transfer from Slave to Master after Request |

#### Some Simple Communication Examples

#### Initialization of the Bus (SND\_NKE)

This mostly resets the communication initially for all slaves. It can be used to test, if your M-Bus works in general. If nothing responds with 0xFE (ACK), your M-Bus could be faulty.

| Master Transmit | Slave transmit |
| --- | --- |
| 0x10 (START)  0x40 (SND\_NKE)  0xFE (A)  0x3E (CHKSUM)  0x16 (STOP) | 0xE5 (ACK) |

#### Test for a slave (or more correct, a primary address)

To test for a single primary address (could be more than a single slave), just replace the broadcast with a slave address.

| Master Transmit | Slave transmit |
| --- | --- |
| 0x10 (START)  0x40 (SND\_NKE)  0x01 (A)  0x41 (CHKSUM)  0x16 (STOP) | 0xE5 (ACK) |

### Doing More Complex Stuff

After a first touch with your M-Bus slave, it is time to get a bit more complex. Next thing would be to set a slaves primary address.

#### Setting the primary address of a single slave on the network

If you only have a single slave connected, this task is quite easy to achieve. It uses a control frame to set the primary address to 0x12. This works "best", if you just sent a bus init (SND\_NKE) before. Spoiler: It could fail due to the frame counter (0x53 vs. 0x73) not correctly toggling.

| Master Transmit | Slave transmit |
| --- | --- |
| 0x68 (START)  0x06 (L)  0x06 (L)  0x68 (START2)  0x53 (SND\_UD)  0xFE (A) 0x51 (CI)  0x01 (DIF)  0x7A (VIF)  0x12 (newA)  0x2F (CHKSUM)  0x16 (STOP) | 0xE5 (ACK) |

After this, you should be able to ask for it on the bus and the slave should respond with an ACK:

| Master Transmit | Slave transmit |
| --- | --- |
| 0x10 (START)  0x40 (SND\_NKE)  0x12 (A)  0x52 (CHKSUM)  0x16 (STOP) | 0xE5 (ACK) |
