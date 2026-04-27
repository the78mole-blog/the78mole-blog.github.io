---
title: Penmount PCI Touch Controllers And I2C - Lost In Space
date: '2020-05-21'
description: ''
categories:
- STM32
tags:
- penmount
- PM2204
- touch controller
- touch screen
---

## Forword

I would suggest to use UART to talk to the Penmount Touch. This works much better since you can simply trigger on some UART interrupt (6 Byte and timeout fits well). But after collecting some experience, I would strongly suggest to check touch functionality from time to time by requesting the version of the touch controller. We had a batch of touches working well for a long time across but the latest batch seems to hang sometimes.

## Introduction

After I worked quite a lot with Touchnetix touch controllers some month ago, I now had a project using a PM2204 from Pemount (Salt). The datasheet of Touchnetix controllers (disclosed only with NDA) consists of several hundred pages defining a huge amount of objects for configuration and infromation retrieval purposes. In the end, you access these objects through dynamic register sets... But this is another story. This is a story about simplicity :-P

## TL;DR

With penmount, you get the direct opposite of the Touchnetix. No documentation anywhere and only 6 bytes of data through UART or I2C. Yes, thats right. And its a one way communication (Edit: It can be 2-way, but even the linux kernel driver for UART ignores this fact.). Nothing to configure, nothing you can do wrong... With I2C, you send a read request to the address of the PM2204 and you will receive 6 bytes, when there has been a touch event. If not, you will receive 6 times 0xEE.

So, the best approach is, to watch out for an interrupt and when it occurs, polling these 6 bytes. They contain the event (1 byte), the position (2 x 2 byte) and a checksum (1 byte). And here is the piece for decoding it (some spices for error checking HAL should be added...):

```
uint32_t total;
uint8_t buf;

HAL_I2C_Master_Receive(&i2c1, 0x70, buf, 6, 100);

btn = buf & 0x40;
xpos = ((buf << 8) | buf) * SCREEN_X_SIZE / 2048;
ypos = ((buf << 8) | buf) * SCREEN_Y_SIZE / 2048;
checksum = buf;

for (int i = 0; i < 5; i++) 
  total += buf; 

if (checksum == (unsigned char) ~(total & 0xff))
  DO_SUCCESS_STUFF;
else
  RAISE_AN_ERROR;
```

How I digged through it? I found the linux driver using UART communication [here](https://github.com/torvalds/linux/blob/master/drivers/input/touchscreen/penmount.c) and just tried, if I2C behaves the same... after hours of trying to access registers like on a memory device.... :-(

Stay tuned for Penmount-Touch and UART, which is working best for us...

Thats all. Have fun with Penmount!
