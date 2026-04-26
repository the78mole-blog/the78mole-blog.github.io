---
title: Ultrasound Distance Module Overview
date: '2021-10-12'
description: ''
categories:
- Uncategorized
tags:
- ESP32
- ESPhome
- Ultrasonic
- Ultrasound
image: /images/blog/2021/10/US-ranging-modules.png
---

I just thought about implemententing a small ESPhome based ultrasound water level module, when I realized, that I have none of my modules left. Maybe I gave the last one away to a friend of mine, so there was no chance to look-up which one I had... Nothing easier than ordering a bunch of new ones, but this task got a little more complicated, since the variants of cheap US distance modules is just overwhelming: HY-SRF04, HY-SRF05, HC-SR04 (5V,2H), HC-SR04 (5V, 4H), HC-SR04 (3-5V, 4H), HC-SR04+ (3-5.5V, 4H), US-100, US-015, US-016, US-026, UNS-016, UNS-100, IOE-SR05, RCWL-1601. So I decided to collect some of the infos at a central place...

| Module Name | Supply  min (V) | Supply max (V) | Range min (cm) | Range max. (cm) | Supply  current (mA) | Accu-racy (mm) | ESP home | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRF04-HY | 4.5 | 5.5 |  | 300 |  |  | ![](/images/blog/2021/10/check_micro.png) |  |
| [SRF05-HY](https://the78mole.de/wp-content/uploads/2021/10/SRF05-HY.pdf) | 4.5 | 5.5 |  | 400 |  |  | ![](/images/blog/2021/10/check_micro.png) |  |
| [HC-SR04](https://the78mole.de/wp-content/uploads/2021/10/HCSR04.pdf) | 3 (4.5) | 5.5 | 2 | 300 | 15 |  | ![](/images/blog/2021/10/check_micro.png) | minimal voltage depends on board variant |
| HC-SR04+ | 3 | 5.5 | 2 (?) | 300 (?) |  |  | ![](/images/blog/2021/10/check_micro.png) |  |
| [US-100](https://the78mole.de/wp-content/uploads/2021/10/4019_Web.pdf) | (3) 4.5 | 5.5 | 2 | 450 |  | 3|1% | ![](/images/blog/2021/10/check_micro.png) | HC-SR04 & Serial UART-Mode |
| [US-015](https://the78mole.de/wp-content/uploads/2021/10/3822-US-015-High-Accuracy-Ultrasonic-Sensor.pdf) | 4.5 | 5.5 | 2 | 400 | ~2 | 1|1% | ![](/images/blog/2021/10/check_micro.png) |  |
| US-016 | (?) | (?) | (?) | (?) | (?) | (?) |  |  |
| US-026 | (?) | (?) | (?) | (?) | (?) | (?) |  |  |
| UNS-016 | (?) | (?) | (?) | (?) | (?) | (?) |  |  |
| UNS-100 | (?) | (?) | (?) | (?) | (?) | (?) |  |  |
| IOE-SR05 | (?) | (?) | (?) | (?) | (?) | (?) |  |  |
| [RCWL-1601](https://the78mole.de/wp-content/uploads/2021/10/4007_Web.pdf) | 3 | 5.5 | 2  (10) | 450  (250) | 2.2 | (?) | ![](/images/blog/2021/10/check_micro.png) | HC-SR04 compatible |
|  |  |  |  |  |  |  |  |  |

As you can see, for some modules, you will even not find data... So better stick with the known ones.

To integrate it into ESPhome, most of them easily can be used, maybe with minor adjustments.

If you have additional datasheets available and also links to shops that can provide them, feel free to send it over to me.

I ordered already a bunch of it and as soon as my modules arrive, I'll write some follow up here and I'll also provide the shopping links, if I'm satisfied with it.

### Usage of Ultrasonic Distance Measument

Now you could ask, for what the ultrasonic distance measumentnt can be used and why not use any other technology like infrared time-of-flight (IR-ToF, like the [ST ToF sensors](https://www.st.com/en/imaging-and-photonics-solutions/time-of-flight-sensors.html)) or laser distance meters like they are used in various meters e.g. from [bosch professional](https://www.bosch-professional.com/de/de/laser-entfernungsmesser-101300-ocs-c/).

The answer is quite easy. At first, ultrasonic distance meters can detect transparent obstacles or levels, like water surface and secondly the modules are dead cheap. For sure, the detection is limited to the capability to reflect the sound, light is even more complicated to reflect back to the origin.

Welp, for what it can be used as an example? I personally like to use it for measuring the filling level of tanks e.g. oil and water. Also for filling level measurements, there exist more sophisticated principles like pressure difference, even with small air pumps to compensate for various errors, but in total, they are much less accurate than a simple ultrasonic distance measurement.

One single drawback of the ultrasonic principle is, that it measures the distance from top of the tank to the surface of the liquid and not the height of the liquid directly. But to be honest, the shape of the tank will not change too much over time and the mathematical operation is a simple subtraction. A bit more complexity comes into play, when the tank hat not a rectangular or at least a simple geometric shape.

But there exist different compensation techniques, if you want to measure the consumption e.g. of oil by also measuring the flow or the run-time of the oil bruner. If you are interested in more details, write me a comment and I'll continue on that... But now to the meat of this article.

## Testing the performance

The modules arrived and now it is time, to test their performance. For this, I'll setup a test bench, that keeps al parameters identical for the individual modules. But we need to keep in mind that only testing a single module of each model, we have no statistical evidence of the performance. Nevertheless, we have an indication, if they meet the datasheet promises.

Here is a schema of my testbench:

![](/images/blog/2022/05/US-Distance-Testbench.drawio.png)

Happy tindering!

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+ultrasound-distance-module-overview&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
