---
title: ESP32-EVB, PlatformIO And ESP-IDF – Yet Another ESP32 tutorial
date: '2021-01-18'
description: ''
categories:
- ESP32
- FreeRTOS
- Uncategorized
tags:
- ESP-IDF
- ESP32
- ESP32-EVB
- Olimex
- pio
- platform.io
image: /images/blog/2020/06/ESP32-EVB.jpg
---

I already posted a [tutorial](https://blog.the78mole.de/esp32-evb-and-platform-io-yet-another-esp32-tutorial/) on using the ESP32-EVB from olimex with Arduino. This time, I will provide the same with ESP-IDF, the original SDK from Espressif. Why I decided to do this? Because I had a project using it :-P

To install PlatformIO, just follow the [guide](https://platformio.org/install/ide?install=vscode).

As shown in the below screenshots, create a new project `VSCode -> The PIO-Icon -> New Project`, define a project name, select Olimex ESP32-EVB with ESP-IDF framework and press Finish. After PIO downloaded all dependencies and configured your project, we are ready to go!

![](/images/blog/2021/01/image-9-1024x312.png)

![](/images/blog/2021/01/image-8.png)

Now just wait until it finishes...

![](/images/blog/2021/01/image-10.png)

After PIO finished setting up the project, you will find the platformio.ini with its configuration. Add the line serial\_speed = 115200 to the file.

![](/images/blog/2021/01/image-12.png)

After this, run an update on pio (especially useful if you had PlatformIO already installed).

```
pio update
pio upgrade --dev
```

We can also now build the empty application by entering `pio run` in the terminal.

If this succeeds, we will edit the main.c file and create some hello world application.

## Hello World - Relay Toggle

Open `src/main.c` and edit it, so it will look like that:

```
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "driver/gpio.h"

#define RELAY_GPIO      32

void app_main() {

    gpio_pad_select_gpio(RELAY_GPIO); 
    /* Set the GPIO as a push/pull output */ 
    gpio_set_direction(RELAY_GPIO, GPIO_MODE_DEF_OUTPUT); 

    while(1) {
        printf("Test\r\n");
        gpio_set_level(RELAY_GPIO, 0);
        vTaskDelay(pdMS_TO_TICKS(500));
        gpio_set_level(RELAY_GPIO, 1);
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

...connect your Olimex ESP32-EVB and enter `pio run -t upload` in terminal.

Done! Your Relay should toogle twice every second.

The pin numbers are simply the GPIO numbers you can find in the schematics of your board, in this case, it is 32.

![](/images/blog/2020/06/image-1.png)

## printf-Debugging

Despite the fact, that printf debugging is somewhat frowned upon, it is a very practical first step. And with platform.io and evaluation boards like this one, it is as easy as pressing a button. No additional wiring, no hassle with pins, ports or blown up code. We already prepared the test in our code above. It prints "Test" every second on the serial console, just that we can not see it yet. For this to show up, you need to open the serial monitor:

![](/images/blog/2021/01/image-13.png)

From now on, you should see the printf output in your terminal every time you upload your code again:

![](/images/blog/2021/01/image-14.png)

Do not forget to close the serial monitor, when you upload your code next time. The serial is blocked by the monitor, so the uploader can not access this port.

![](/images/blog/2021/01/image-15.png)

After closing the serial monitor, you should drop back to your terminal, where you can start over with `pio run -t upload`.

OK, that's all. There are many tutorials out there, how to setup a webserver, controlling pins, using SPI or bluetooth or whatever. You will find information on all peripherials [here](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/index.html). Just remember to include the header(s) that are mentioned on top of every peripherial page, like we did with `#include "driver/gpio.h"` above in `main.c`.

![](/images/blog/2021/01/image-16-1024x794.png)

Now, you have some great starting point for ESP-IDF :-P

Have fun coding!

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
