---
title: In The Heat Of The Night - 1-Wire Temperature Sensor Directly Immersed
date: '2022-10-31'
description: ''
categories:
- ESP32
- ESPhome
- Heating
- Home Assistant
- Smart Home
tags:
- immersive
- onewire
- sleeve
image: /images/blog/2022/10/image-13.png
---

As always, I want to first quickly explain, what brought me to that project... If you look around in different stores and on aliexpress, you can find a ton of 1-wire temperature sensors with stainless steel sleeves. But they are all 6 mm or the are wrapped with a shrinking tube, that avoids to use it as a immersed temperature probe. What I needed was a sleeve with 5 mm (or 5.2 mm) diameter and grooved at the end to be used in standard probe holes like with this [ball valve](https://www.pumpendiscounter.de/ReigaGbR-p9174h1310s1312-Kugelhahn-1-IG-DN-25.html).

The tricky point is, that the default [DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf) in TO-92 case are a bit to fat, to fit in a 5 mm tube. But the DB18B20U is the starving brother and thin enough to fit in, if placed on an appropriate PCB (0,6mm). So, I decided to design one and give it a try...

![](/images/blog/2022/10/image-12-1024x510.png)

![](/images/blog/2022/10/image-10.png)

And after only a few days, my order from PBCway arrived... You will find it on [GitHub](https://github.com/the78mole/Onewire-AGFW-compatible-tempsensor).

![](/images/blog/2022/10/image-11-1024x850.png)

It only took a few minutes to solder the components...

![](/images/blog/2022/10/image-13-1024x310.png)

And after connecting it to some ESP32 that was lying around and adding the config to ESPhome, the sensor quickly showed up in ESPhome.

![](/images/blog/2022/10/image-14-1024x576.png)

```yaml
esphome:
  name: ow-test32

esp32:
  board: esp32dev
  framework:
    type: arduino

# Enable logging
logger:

# Enable Home Assistant API
api:

ota:
  password: "somepass"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Ow-Test32 Fallback Hotspot"
    password: "some-other-pass"

captive_portal:

dallas:
  - pin: 13
    update_interval: 5s

# Individual sensors
sensor:
  - platform: dallas
    address: 0x30000001243bfc28
    name: "Test OWire"
```

![](/images/blog/2022/10/image-16.png)

![](/images/blog/2022/11/image-2-1024x576.png)

That was easy and I already found an appropriate sensor cable and ordered it already. For grooving, I need to build me some tools and I'll share that information.

Update: I'll contact another sensor supplier and ask, if they can provide this sensor.

The best fit steel tubes can be found on [aliexpress](https://de.aliexpress.com/item/33062078044.html).

If you are interested to get some of the PCBs for testing or fully assembled sensors, please let me know :-)

I'll provide an update soon.

Happy digging!
