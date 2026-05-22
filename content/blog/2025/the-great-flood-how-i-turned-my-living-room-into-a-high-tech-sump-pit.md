---
title: The Great Flood - How I Turned My Living Room into a High-Tech Sump Pit
date: '2025-07-13'
description: ''
categories:
- BThome
- ESPhome
- Smart Home
- DIY
tags:
- arduino
- BThome
- BThomeV2
- clay
- ESP32
- platform.io
- soil
- sensor
- iot
- home-assistant
- diy
image: /images/blog/2025/07/image-2-scaled.png
---

Or: Why Flower Power and Clay Soil Don't Mix – A Mole's Tale of Moisture, Microcontrollers, and Minor Excavations

They say moles love the damp. That may be true out in the field, but when your *living room* starts feeling like a boggy marsh, it’s time to bring in the tech (and a shovel).  
Now, I know rewetting peatlands is all the rage these days for climate protection – and rightly so! – but I don’t think my neighbor had that in mind when she started watering her flowerbeds. For four to five hours. Every day. For **three weeks**. On clay soil.  
The result? A surprise indoor wetland, right beneath my feet.

Now, here in Claylandia (™), water doesn't politely drain away. It *lurks*, seeps, and eventually invades. My cozy underworld was slowly turning into a bathtub. So what’s a Mole to do?

## Step 1: Dig, Mole, Dig!

I excavated a modest pit: 50 cm deep, 30 cm wide, and 40 cm long. Right in the **boiler room** – or as I now call it, *the technical spa*. In went a sturdy basket, a submersible pump, and a sense of growing control.

![](/images/blog/2025/07/image-1024x576.png)

## Step 2: Enter the ESP32-S3

Because this is not just any molehill. I installed an ultrasonic sensor pointing down into the pit, connected to an ESP32-S3, prototyped it with ESPhome. This was crazy fast, just using seven lines of yaml code in ESPhome (not counting the boilerplate to connect the device)

```yaml
sensor:
  - platform: ultrasonic
    id: drain_distance
    trigger_pin: 9
    echo_pin: 8
    name: "Drain Water Distance"
    update_interval: 10s
```

![](/images/blog/2025/07/image-1-1024x576.png)

With a powerbank lifetime of just 2-3 days, just after one week this drove me nervous. So I started over running PlatformIO, speaking fluent [BTHome](https://bthome.io/) (on [Home Assistant Integration](https://www.home-assistant.io/integrations/bthome/)). The sensor continuously monitors the distance to the water surface – precision mole tech!

![](/images/blog/2025/07/image-2-1024x576.png)

![](/images/blog/2025/07/image-3-1024x576.png)

![](/images/blog/2025/07/image-4-1024x576.png)

![](/images/blog/2025/07/image-5-1024x576.png)

![](/images/blog/2025/07/image-7-1024x743.png)

All code and 3D-Model files can be found on Github: [the78mole/BThome-US-Ranging](https://github.com/the78mole/BThome-US-Ranging)

## Step 3: Integration is Everything

The ESP32 reports directly to my Home Assistant setup. The only thing neeed is a bluetooth proxy device somewhere around in your house, that can fetch the messages out of thin air. You can use a ESPhome device for that purpose or one of the supported Shellys (many Pro and Plus devices support this).

The data shows up alongside the usual suspects: temperature, humidity, battery level... and now **aquatic threat level**. I've even added an automation to send a Pushover alert if the water rises above a critical value (25 cm blow floor level). That means I can take action *before* my sofa learns to swim.

## Step 4: Make it Pretty

To keep things neat and paw-safe, as you can see in the above pictures, I designed and 3D-printed custom enclosure, flush-mounted into a cover plate. It hides the pit, protects the electronics, and keeps the place from looking like a science experiment gone wrong.

## Step 5: Protection for the Blind Underground Folk

Now, we all know that the subterranean world is full of hazards — unexpected floods, loose cables, and curious creatures with paws. But it’s not just about electronics and moisture: sometimes, it’s about *safety and aesthetics*.

To ensure that no mice, hedgehogs (or worse: moles) stumble into my sensor-pit of doom, I welded a sturdy steel frame from plain black steel. This angular monument to overengineering got lovingly embedded into the screed with mortar, just like grandma used to do.

![](/images/blog/2025/07/image-8-1024x576.png)

Inside the frame sits a robust two-layered phenolic resin board (some call it “Siebdruckplatte”, I call it *waterproof magic*), precisely cut to host the ultrasonic sensor housing. The whole thing is flush with the floor (not now, but when I added plates to the floor after kicking out the fossil burning stove), strong enough to survive stampedes, and still allows perfect measurements.

![](/images/blog/2025/07/image-9-1024x576.png)

Functionally invisible. Structurally paranoid. Just how we like it in the underworld.

## Conclusion

What started as an accidental water feature is now a smart, almost invisible early-warning system. And all thanks to a bit of digging, some ESP-wrangling, and the desire *not* to grow mold in my moldings. Additionly, I had a lot of fun welding the frame myself at [ZAM](https://zam.haus) :-)

Moral of the story? Always check what your neighbors are watering – and never underestimate clay soil.

Stay dry,  
**The Mole**
