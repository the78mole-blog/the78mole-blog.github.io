---
title: The Magic Of Absolute Humidity
date: '2021-07-10'
description: ''
categories:
- ESP32
- ESPhome
- Home Assistant
- Smart Home
tags:
- Absolute Humidity
- ESPhome
image: /images/blog/2021/07/IMG_20210708_231201.jpg
---

## Introduction

When we moved from our flat to our house back in 2015, I soon realized, that the old part of the house (built in the fifties) has some problems with moisture in the basement. The walls are made of natural sand stone and they are by far not well insulated from the outside. This means, that water is pressing in over time and the surface is wet and susceptible to mildew (de: Schimmelpilz).

The previous owner of the house simply used a humidity controlled circuit breaker (humidistat) and some ventilation that is pumping air from the basement (draw from the ground floor) to the outside, as soon as the relative humidity is exceeding a certain value. A ridiculous side fact is, that the air was draw from the ground floor, directly adjacent to the bath room and the kitchen. Sounds good? NO, IN FACT NOT! Let me explain why. First of all, outside air is generally more dry than inside air (especially the air from kitchen and bathroom). But even outside air has some season depending properties. In winter time, when relative humidity is high outside, it is generally a good idea to pump it into the basement, because when the (relatively humid) cold air heats up, humidity vanishes mostly. In summer time, when relative humidity is low, but temperature is high, the air that enters the basement cools down and gets humid. But how to decide correctly, if it is a good idea to start ventilation, when the relative humidity in the basement is not a good measure. So the previous guy made two errors: Pushing out cold and sucking in warm and humid air, controlling on relative humidity inside only.

Welp, the magic simply is the absolute humidity (and pull air directly from the outside, not through inside rooms). Absolute humidity is not measured in %, it is measured in g/m³. Hmmm, can we buy some sensor that measures absolute humidity. The correct answer is yes and no. Physically, you could, with quite some effort. Usually (at least with the most common technique in meterology) this is done by cooling down a plate until water condenses. This gives you the dew point and from it, you can "easily" calculate the absolute humidity. To measure it more directly, it would need a certain volume of air, seperated from the ambient air, cooling it down much below 0°C and measure the volume/weight of the condensed water. Very impractical...

But math and physics can do the trick more easily (with only a few restrictions). You can calculate the absolute humidity from temperature, relative humidity and pressure. This approach has some problems with common sensors for this three physical values, but we will talk about the affection on our intent later.

## What Is Relative Humidity?

Before we start with any calculation, let's define, what relative humidity is. To understand relative humidity, just imagine what perfect dry air and totally humid air is. If you think about 100% humidity, it does not mean, that you are below water level. It just means, the air is fully saturated with water and if you put any more water (vapor) in, you will observe mist, getting denser and denser, the more water is trown in. Perfect dry air does not contain any water molecules. And everything in between is "simply" mapped to a value between 0 and 100%.

But why are we so interested in the relative humidity? It simply is, because we, as humans, are humidity sources. Our loungs' trachea need to be wet on their surface and as we breathe, this water evaporates and get's lost from our body. Also the temperture regulation depends on a certain (lower) humidty by evaporating sweat. This means, to control the temperature, the humidity shall be below a certain point, to not loose to much water (feel well), but humidity should not exceed a certain value to still be able to control your body's temperature. The comfort range is around 50% humidity. Speaking truely, it ranges much higher, but as we live in buildings suceptible to mildew, there comes in another limit, that should not be exceeded (for a longer period of time). Generally saying, the humidity should never exceed 80% for a longer period and if you already have problems with mildew, you should keep it below 60%.

When you dive any deeper in building physics, you will see problematic zones especially in outer corners of non-well insulated houses. There you can also get mildew problems with relative humidities below 50%. Water will condense there easily, because of much lower temperatures of the wall itself. And if you switch on a heater to make the air more dry, you mostly achieve the oppsite, because you give the air the opportunity to collect even more water in other regions of the room. So, building physics is not an easy task, with simple rules of thumb... But back to our problem: How to decide, if outside air is suited to reduce basement (absolute & relative) humidity?

## Calculate The Absoulte Humidity

What do we need for perfect calculation of absolute humidity when we use measurements and data we have available. Remember, we want the amount/weight of water in the air...

- Gas constituent parts (-> N2, O2, CO2, CO, He, Ar, Kr, Xe,...)
- Temperature
- Pressure

And we need some other constants or relationships:

- Gas constants
- Saturation vapor
- ...

Uh, can we simplify this a bit? Yes and no. Let's step back to the initial intention... We can assume, that the gas mixture in the outer air is the same as in our basement (ignoring Radon perspirations, the CO2 increase due to breathing,...). And we also assume, that the pressure is identical (at least when the ventilation is not running). So, we can assume, that relative humidity and temperature is sufficient to calculate the absolute humidity while errors due to the mentioned differences will compensate itself.

In my very first approach, I tried to establish a formula, that is totally correct, including pressure and temperature over the full range: -50...200°C, ~0...2000 mBar. But that got really complicated. The corner cases ~0°C and ~100°C lead to some problems and since the aggragate transistion (especially the vapor point at 100°C) moves with pressure, it... got complicated.

So, I decided to go with 0.1% accuracy within the range -30...+35°C. The basement itself is really constant around +16..20°C if the radiator is not turned on (yes, the previous owner installed radiators in the basement). The formula, to calculate the absoulte humidity quite accurately in the range from -30...+35°C is

![](https://carnotcycle.files.wordpress.com/2014/09/ah1.jpg)

Taken from [Carnotcycle](https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/) - rh = relative humidity (%), T = temperature (°C)  
rh is in the range 0...100 (not 0.0...1.0)

This gives an error of 0.1%, which is much better than the accuracy of most sensors for temperature and humidty. So we go with this and ignore the fact, that temperature above 35°C can occur for the outside. When it goes above 35°C, we can be sure that the absolute humidity is way above absolute humidity in the basement, believe me :-P

## Smart Home Implementation

Now we simply need to implement this in our smart home system. The most complicated part is the exponential function, that needs a full math library and can not be easily integrated within a micro controller. Since I want every temperature and humidity sensor to also calculate the absolute humidity. Since I started with Home Assistant and ESPhome, I want to integrate this into the low-cost temperatrue/humidity sensors running on some NodeMCU (ESP8266) or some LOLIN32 (ESP32) board.

![](https://lh3.googleusercontent.com/FgJH1j7d5tS7oVSEElZBficoWvpiQMikaWA7NsLCsWwJIR_Jf-Zp6vUjYiLOtkpWe-PNDhO8KdSFnPLnex1rzMQ0xf0Y9-YZHKnYAX5eHaK3QYiTl0C0m88w7zQueHn8GmUvhkzg73vCLnLatAQDMHB7AAUEXBibDt_HOEPvAwcXVG3IucfhwHR1FM9vK3Mkrjq9c1Tzb612LPwmUP1whTjXrjDuwQHw-tBJqVc5sdSwcMpqrKaQLEojZ5btGy5oR7gIlnMnl6RApk4bEIxXh6h3jtYDPhvCOEljtdTbMElxLVOtCUtWzJhjgBaw1FNx_Bs8AjJzS5ZJ-xkjLRHJfjvncmgeCJFN2rTvuvqwPmNFN3tEOn_rTPIlIGBaqfvMqPr_x6E231QEnpDsdnhwieTshaoYt27a8WSfAsM0MfU9wdgfznivIBgY-z8tK0NrQMT_LnptHVY5N2NajUaRI5jJC4P8ZcrM2P1FJlPIYaWoDwLtkxB5EEAeaBbIDQzyvl7eJ1NP0lf24PGKPVgprNHoS1UZlgbqk1wjcEtj8xQfAfpaChm3DQrEakDvjzRexXUiDR48ryEuA58EXlru2qTEqLOQiUosEXEpQA4ieHlm0f2IHRZdwbQhGm6BgKV0JGbvrFd7crZ-_SbEzmkNQF7AuOLuoHhw9NGLmSi0inUHK-4xGfQeRdY0xK02c-0uLmCd0IwyangcyelcupIPsDUPnQ=w422-h948-no?authuser=0)

An AM2320 temp-humidity-sensor hedgehog-wired to some LOLIN32 (V1.0.0, ESP32) with some old dyson li-ion battery as an energy source, running ESPhome. It also measures the battery voltage via some 1:2 (2 x 1MOhm) resistor divider.

If we look at the possible filters of the Sensor Core Component, we can see, that it is not capable of handling exponential functions :-( You can play around with the function [here](https://www.desmos.com/calculator/ada5eexikw) (x = temperature, R = relative humidity, y = absolute humidity in g/m³).

So, what would an engineer do? That's easy, interpolating the exponential function, because ESPhome has a [calibrate\_polynomial filter](https://esphome.io/components/sensor/index.html#calibrate-polynomial). So what is the polynomial approximation for e^(17.67 × T)/(T+243.5)???

What an easy task nowadays... We use some online tool for that again. First we extract some tabular values from the function (see [here](https://www.desmos.com/calculator/a0gk5rmejj)). Then we put it into an [online curve fitter](https://mycurvefit.com/). (If you find an online cuve fitter, that ist taking a function as input, let me know in the comments).

![](/images/blog/2021/07/image-2.png)

Put this in the curve fitter table and you get the following:

![](/images/blog/2021/07/image-3.png)

This gives us the satisfaction, that a quadratic polynomial is OK for fitting.If you coose the third order poly, you can observe quite a large error at the low negative temperatures. The ESPhome polynomial calibration just takes the order of the polynomial fit and a list of measured and real values. With putting it in ESPhome's yaml, it woud look like this:

```yaml
filters:
  - calibrate_polynomial:
     degree: 4
     datapoints:
      # Map 0.0 (from sensor) to 0.0 (true value)
       - -30.0 -> 0.08350039
       - -20.0 -> 0.20572642
       - -10.0 -> 0.46919108
       -   0.0 -> 1
       -   5.0 -> 1.4269413
       -  10.0 -> 2.0078039
       -  15.0 -> 2.788039
       -  20.0 -> 3.8235391
       -  25.0 -> 5.1823126
       -  30.0 -> 6.9462949
       -  35.0 -> 9.2132837
```

But this is only a small part of the formula... And I don't want the sensor node to do a polynomial fit every time I need to convert a measurement to another value... So, we better use a lambda function for that purpose and calculate the full value for a new virtual, so called [Template Sensor](https://esphome.io/components/sensor/template.html). Lambda functions in ESPhome are simply C++ code that get's copied over to the sensor class implementation and compiled into the ESPhome firmware image to be flashed on your node. Here is the heavy lifting part (the boilerplate code is up to you :-P ):

```yaml
sensor:
  - platform: am2320
    i2c_id: bus_a
    setup_priority: -100
    #address: 0x5C
    temperature:
      name: "ESP32 NBKG Side - Temperature"
      id: esp32_nbkg_side_temperature
    humidity:
      name: "ESP32 NBKG Side - Humidity"
      id: esp32_nbkg_side_rel_humidity
      on_value:
      then:
        - component.update: basement_tmp_exponential_approx
    update_interval: 30s
  - platform: template
    id: basement_tmp_exponential_approx
    internal: true
    # it is forcefully updated by the am2320
    update_interval: never
    lambda: |-
      float senstemp, result;
      senstemp = id(esp32_nbkg_side_temperature).state;
      result = 1.006133;
      result += 0.07152097 * senstemp;
      result += 0.002276316 * senstemp * senstemp;
      result += 0.00004773119 * senstemp * senstemp * senstemp;
      result += 0.0000005750658 * senstemp * senstemp * senstemp * senstemp;
      return float(result); 
    on_value:
      then:
      - logger.log:
          format: "Temperature: %.1f, humidity %.1f, tmp: %.1f"
          args: [ 'id(esp32_nbkg_side_temperature).state', \
                  'id(esp32_nbkg_side_rel_humidity).state', \
                  'id(basement_tmp_exponential_approx).state' ]
      - component.update: esp32_nbkg_side_abs_humidity
  - platform: template
    name: "ESP32 NBKG Side - Absolute Humidity"
    unit_of_measurement: "g/m³"
    id: esp32_nbkg_side_abs_humidity
    # it is forcefully updated by basement_tmp_exponential_approx
    update_interval: never 
    lambda: |-
      float tmp_exp, result, humid, temp;
      tmp_exp = id(basement_tmp_exponential_approx).state;
      temp = id(esp32_nbkg_side_temperature).state;
      humid = id(esp32_nbkg_side_rel_humidity).state;
      result = 13.247 * tmp_exp * humid / (273.15 + temp);
      return float(result);
    on_value:
      then:
        - logger.log:
            format: "Temperature: %.1f, humidity %.1f, tmp: %.1f, abs: %.1f"
            args: [ 'id(esp32_nbkg_side_temperature).state', \
                    'id(esp32_nbkg_side_rel_humidity).state', \
                    'id(basement_tmp_exponential_approx).state', \
                    'id(esp32_nbkg_side_abs_humidity).state' ] 
```

If you want to prove the results, [here](https://rolfb.ch/projects/humidity-table/) you can find a table and a tool to calculate absolute humidity for tempreature vs. relative humidity. Here are some actual values of my sensor:

![](/images/blog/2021/07/image-4.png)

And here is some graph (the absolute value has a different time span because the virtual sensor is brand new!!!)

![](/images/blog/2021/07/image-5.png)

BTW: The temperature of the sensor rises, because the ESP32 deep sleep is defeated for debugging purposes and therefore it heats up the sensor a bit. For absolute humidity, this should not affect the value (at least not very much) and you can observe, that it only differs around one gramm.

Since temperature and humidity do not change quickly, we only take measuements every 30 minutes to not drain the battery to much and also to get correct temperatrue readings. If you now do the same for the outside sensor and compare it with inside absolute humidity, you can easily decide, if it is a good idea to turn on the ventilation.

## On The Errors...

This part gets really short. Above, we talked about the imperfections of the exponential approximation. It is around 0.1% ranging from -30 to +35°C. And the polynomial fit tells, at least for the data points, the fit is 100%. Even if the fit is only correct to about 5%, the relative humidity error of common sensors is around 3%, which gives us an error of up to 6% when comparing two humidity values. The temperature uncertainty is quite low (usually <1%) and what adds up is the huge relative error when it comes to low temperatures. In fact, the absolute humidiy is close to zero gramms.

How will it affect our humidity control? We can simply ignore it. Since the temperature of the room, the humidity is to be controlled, is quite high (>15°C) the error in this region is neglegtible. If you look at the spot to be controlled (50%) and the gradient of the curve, there is no need to worry. If your descision has some offset (e.g. outside humidity needs 5 gramms less of moisture compared to inside, then you are always fine. The error will not exceed the offset of 5 gramms in reality.

BTW: The AM2320 is really a shitty sensor and often simply stops to respond. Better use one of the DHT-types or a Bosch BME280.

Have fun!

## Links

- Wikipedia [Luftfeuchtigkeit](https://de.wikipedia.org/wiki/Luftfeuchtigkeit#Abh%C3%A4ngigkeit_der_S%C3%A4ttigungskonzentration_von_Umgebungseinfl%C3%BCssen) (de),
- Wikipedia [Humidity](https://en.wikipedia.org/wiki/Humidity) (en),
- [Carnotcycle Blog](https://carnotcycle.wordpress.com/2012/08/04/how-to-convert-relative-humidity-to-absolute-humidity/)
- [rolfb](https://rolfb.ch/projects/humidity-table/) ([Online tool](https://rolfb.ch/tools/thtable.php?tmin=-20&tmax=50&tstep=2.5&hmin=5&hmax=100&hstep=5&acc=2&calculate=calculate) for absolute humidity calculation)
