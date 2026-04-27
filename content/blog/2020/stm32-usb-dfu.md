---
title: STM32 USB-DFU
date: '2020-06-16'
description: ''
categories:
- STM32
tags:
- Bootloader
- DFU
- firmware upgrade
- USB
---

I'm not sure, if I'm simply a problem magnet or why some stuff does not work as described... Here is another case. The tool I tend to use can be found [here at STM's site](https://www.st.com/en/development-tools/stsw-stm32080.html).

When I connected a piece of custom designed hardware with my laptops USB port with BOOT0 tied to VCC, it immediately showed up a new USB-Device called "STM32 Bootloader" in group "USB Devices". I was really happy about that and started the DFuSe Demo Software from STM. But hey, it could not find an appropriate device. What the heck???

After some digging through the web, I found different suggestions and problem solutions, but none of it worked.The simple solution was, to uninstall the device's driver in "Device Manager", unconnect and reconnet again. A different device showed up just a goup above the previous one: "USB Controller".

![](/images/blog/2020/06/image-7.png)

Welp, as soon as the device showed up, also the DFuSe Demo Software recognized the device and stepped into life.

![](/images/blog/2020/06/image-8.png)

To create a DFU file is well described in all the other resources on the web. Just use the DFU file manager that was installed along with the DFuSe Demo Software to create a DFU file out of e.g. a hex file.

Then press the lower "Choose..." button to select the generated DFU file and press "Upgrade"... That's all. Your device has a new Firmware on it.

![](/images/blog/2020/06/image-9.png)

Have fun!
