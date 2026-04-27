---
title: ESP32-EVB, PlatformIO And Arduino - Yet Another ESP32 tutorial
date: '2020-06-02'
description: ''
categories:
- ESP32
- Uncategorized
tags:
- arduino
- ESP32
- ESP32-EVB
- Olimex
- pio
- platform.io
image: /images/blog/2020/06/ESP32-EVB.jpg
---

What the heck? Aren't there enough toturials out there about ESP32? I believe: Yes, too many. And there are too many that struggle with setting up the arduino environment for non-arduino hardware. But there is a straight-forward solution that works out of the box: platform.io or also known as PIO.

And there are enought tutorials about [installing platform.io](https://platformio.org/install/ide?install=vscode). It is as easy as you can think. Install Visual Studio Code from Microsoft and install the PIO plugin in VSCode.

Then create a new project VSCode -> New Project and select Olimex ESP32-EVB with Arduino Platform. After PIO downloaded all dependencies and configured your project, we are ready to go!

## Hello World - Relay Toggle

Open main.cpp and edit it, so it will look like that:

```
#include <Arduino.h>

const int relay1pin = 32;

void setup() {
  pinMode(relay1pin, OUTPUT);
}

void loop() {
  digitalWrite(relay1pin, HIGH);
  delay(10000);
  digitalWrite(relay1pin, LOW);
  delay(10000);
}
```

...connect your Olimex ESP32-EVB and hit the upload button:

![](/images/blog/2020/06/image.png)

Done! Your Relay should toogle every 10 seconds.

The pin numbers are simply the GPIO numbers you can find in the schematics of your board, in this case, it is 32.

![](/images/blog/2020/06/image-1.png)

## printf-Debugging

Despite the fact, that printf debugging is somewhat frowned upon, it is a very practical first step. And with platform.io and evaluation boards like this one, it is as easy as pressing a button. No additional wiring, no hassle with pins, ports or blown up code.

Extend your code to look like this:

```
#include <Arduino.h>

const int relay1pin = 32;

void setup() {
  Serial.begin(115200);
  pinMode(relay1pin, OUTPUT);
}

void loop() {
  Serial.printf("Switch on\r\n");
  digitalWrite(relay1pin, HIGH);
  delay(10000);
  Serial.printf("Switch off\r\n");
  digitalWrite(relay1pin, LOW);
  delay(10000);
}
```

Add two lines to your platfromio.ini file. You will find the correct COM port in terminal when uploading the new code to your device.

![](/images/blog/2020/06/image-3.png)

In my case it is COM6 and platformio.ini looks like this:

```
platform = espressif32
board = esp32-evb
framework = arduino
monitor_port = COM6
monitor_speed = 115200
```

Upload your code again after changing the ini file. If it does not print your output automatically to your terminal, start the monitor manually:

![](/images/blog/2020/06/image-2.png)

From now on, you should see the printf output in your terminal every time you upload your code again:

![](/images/blog/2020/06/image-4.png)

OK, that's all. There are many tutorials out there, how to setup a webserver, controlling pins, using SPI or whatever. But now, you have some great arduino IDE without arduino IDE :-P

Have fun coding!
