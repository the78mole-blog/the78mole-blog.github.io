---
title: STM32 BLDC Motor Control
date: '2019-10-09'
description: ''
categories:
- Motor Control
- STM32
tags:
- BLDC
- Motor Control
image: /images/blog/2019/10/STM-Motor-Control.png
---

## Introduction

ST offers quite a broad BLDC controller portfolio, but the most interesting to me seems the STSPIN family of controllers. They include mostly anything except the MOSFETs to drive a BLDC, including a ST32 Microcontroller, a DC/DC-Converter (with external passives), the MOSFET drivers,...

## Steps of designing a BLDC control circuit with STM32

First step is to find one or some BLDC motors for your specific need. The available motors range from cheap no-name motors (~4000 rpm) to high performance high turn ratio (>60000 rpm) and from a few watts up to kilo-watts of power. For CNC applications, you can find HF spindles with 2200W and 30000 rpm.

When you have your BLDC, it's time to find the right controller for your application. When you go with STSPIN, you should think about getting the STEVAL-SPIN320x for prototyping your application, but additionally, you should always get the NUCLEO board with an appropriate BLDC driver hat. Why? Because the STM Motor Profiler Tool only runs with a few specific boards. To find the right board, install the ST Motor Control SDK and open the Motor Profiler Tool. Then you can browse through the supported kits to do Motor Profiling.

![](/images/blog/2019/10/image.png)

For further hands-on example, I will use a "Generic BLDC Motor" with very poor documentation and quite low performance. It looks like a stepper motor and has the following (known) performance characteristics:

- 8 pole pairs
- 4000 rpm
- 24V

We also measures some characteristics that have not been given by the specs, most important: The winding resistance. Set your power supply to current limiting mode with approx 5% of the nominal current of the motor. Then connect it to two wires of the motor. In our example, the power supply showed 0,36V / 0,3A = 1,2 Ohms, this gives, taking the circuit of three windings in star configuration (we have a simple series configuration of two windings) into account, 0,6 Ohm (1,2 Ohm / 2 = 0.6). Applied with above power, you can easily determine the pole-pair count by turning the shaft a full turn counting the ripples, you should feel the while turning. It will be easier to use a pen to mark the positions. Apply the power only for a minute, otherwise, you could damage the motor...

With above data, you can select the appropriate BLDC controller board. For smaller motors, the [X-NUCLEO-IHM16M1](https://www.st.com/en/ecosystems/x-nucleo-ihm16m1.html) should serve well. For larger types, the [X-NUCLEO-IHM08M1](https://www.st.com/en/ecosystems/x-nucleo-ihm08m1.html) is a good choice. But always be aware, that for every power hat board, there is only a limited set of compatible nucleos.

To be continued...

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+stm32-bldc-motor-control&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
