---
title: Angular Web App on ESP32
date: '2021-01-22'
description: ''
categories:
- ESP32
- Embedded
- Dev
tags:
- angular
- ESP-IDF
- ESP32
- platform.io
- vscode
- web
- iot
- microcontroller
image: /images/blog/2021/01/esp_angular_platformio-2.png
---

In progress...

[TL;DR](#TLDR) (take me to the battle field)

## Introduction and Motivation

In some recent project, we added some ESP32 to replace wired communication with a BLE solution. Additionally, the customer wants to have some administrative web application to configure the device more easily and to get more detailed information in service.

Creating a simple web ab is not a hard task for an embedded C developer. But to create a beatiful or at least not shitty looking web application is just another game. When you look more closely on the available space on some ESP32, you will realize, that there is at most 16 MB of space to live with.

If you create a simple WiFi AP on some ESP32 4MB version with ESP-IDF, you can easily see, that there is not much left for BLE and APP.

![](/images/blog/2021/01/image-17.png)

Build statistics for a simple WiFi AP with only a hello world index.html on some lolin32 board

Unfortunately, I only have the 4 MB version available, which complicates the task even more. And no, I can not simply change to 16MB, since a few hundred units are already in operation, waiting for some firmware update to provide WiFi service. You know how this works... Deliver the hardware as early as possible and hand features in later :-P

But this means, there is much headroom for optimization and not much space for resources and code. If you have a look at web application frameworks (e.g. react) and build some basic apps, they all come with megabytes of resources in the production build output folder. If you build a very basic hello-world angular application, you will find a few 100 kilobytes of resources after building it, to be deployed on a static web space. This is also just small enough, to be fitted in the flash.

Now, let's talk about the solution...

## Prerequisites

First of all, you will need to create an angular and an ESP-IDF project. This is easily done, if you already [installed Visual Studio Code with PlatformIO](https://blog.the78mole.de/esp32-evb-platformio-and-esp-idf-yet-another-esp32-tutorial/).

To create an angular project, just follow the [official guide](https://angular.io/guide/setup-local). If you installed npm correctly, you can issue the commands in your Visual Studio Code Terminal, to fire up the project.

```
ng new esp-on-angular
```

After these steps, you have two separate projects. You can easily setup a script to copy the angular production build over to the ESP project, do it manually or link it in using git submodules. But this is not part of this tutorial. We simply copy over the website content manually from the angular project output folder.

In addition to npm, VSCode and PlatformIO, you could need some basic Linux system, when working on Windows, if you intend to use the automation script I'l provide later. On my machine, I use [MSYS2/MinGW](https://www.msys2.org/) to get the CLI tools I need: bash, find, gzip, stat

## Getting Started

### Firmware Web Content Integration

While it is quite easy to simply handling incoming requests and responding to it, like you would do for some RESTful Web Service (which is the usual case for IoT stuff like the ESP32), integrating plain files is usually a more complex task. Thanks to the ESP-IDF, this is not the case.

In general, there are two options. Adding the files to a [SPIFFS partition](https://docs.platformio.org/en/latest/platforms/espressif32.html#partition-tables) and reading it from there. Another solution is to [embed the files in your firmware object](https://docs.platformio.org/en/latest/platforms/espressif32.html#embedding-binary-data). The latter one is what we will use in this tutorial, since it is more dense (in terms of size), althought it is less flexible and requires a bit more lumber in your config.

For it to work, simply add the files to `board_build.embed_files` environment in your platform.ini file of your ESP project. I usually put these ressource files into a separate folder called `res`.

```
board_build.embed_txtfiles = 
    res/index.html
board_build.embed_files =
    res/logo.png
```

When you did so, you can link the content easily with the following lines in your code, PlatformIO will care for it to be a valid symbol and to be linked in:

```
extern const uint8_t index_html_start[] asm("_binary_index_html_start");
extern const uint8_t index_html_end[]   asm("_binary_index_html_end");
extern const uint8_t logo_start[] asm("_binary_logo_png_start");
extern const uint8_t logo_end[]   asm("_binary_logo_png_end");
```

When you want to use that data in your http handler, just use the pointers declared above:

```
httpd_resp_set_type(httpRequest, "text/html");
httpd_resp_send(httpRequest, (const char*) 
    index_html_start, HTTPD_RESP_USE_STRLEN);
```

...or for your png image file...

```
httpd_resp_set_type(httpRequest, "image/png");
httpd_resp_send(httpRequest, (const char*) 
    logo_start, logo_start - logo_end);
```

I personally use only the binary version, since it can also process text files and makes the code more universal. You will later see, that there will not be much of a text left :-)

The symbols of your file object (the part in the asm function) is built by concatenating `_binary_` with the name of your file with all special chars replaced by underscores `_` and the suffix `_start` and `_end` respectively. In short: `_binary_<FILENAMEREPL>_start` and `_binary_<FILENAMEREPL>_end`.

Welp, that is quite fine, but the files still take up quite some space and we do not have a lot. When using the 4M version of the ESP32, we simply can not allow it to do so. So, what can we do further to reduce the size of our resources?

You could ask: Why not push the images and fonts to a publically accessible location in the wolrd wide web? Because some of us want to make it self contained. The reason for me have been simply the security and safety requirements of the project: Keep the system closed to the outside world, provide some WiFi Access Point and serve all files that are needed yourself. Do not depend on internet in general. If you have other requirements, kick your ESP in your local WiFi and access it from there or use the AP/Client mode, where the ESP connects to a wifi as a client, provides a WiFi AP and acts as a router between these two networks. But be warned, don't expect too much performance from the latter option.

Welp, back to the size problem... What to do to make it fit?

### Some quirks to shrink it down

Optimizing the ESP-IDF libraries and build scripts to free up some flash, is maybe quite an intensive task and needs a deep understanding of the IDF internals. So, we will first try to find some other quirks, to reduce the size of our own big blobs.

#### Angular - Stripping the unneeded

While angular itself is really tiny, it links in some fonts from google (Remeber, we want to be self contained). This is usually not needed, because devices nowadays have some replacement fonts installed, we can easily delete the links from the generated index.html and rely on the local resources of the client.

```
<link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

#### Zero Effort Zipping

While Angular already minimizes most of it's output files, it would be really awesome to compress the resources somehow. But integrating a compression library and using it, stacks up again...

Then I had an flash of thought. Once upon a time, web speed analyzis tools started to raise warnings, when your website content was not delivered in a compressed format. Nowadays, webspace providers enable brotli and/or gzip compresson by default and there are plenty of tutorials available about Wordpress and how to enable compression. All modern web browsers support gzip compression by default and offer it as a supported content encoding sheme.

Welp, but what this has to do with my web application content. Shall the ESP compress all content ahead of the transfer? Of course not! We simply compress all files ahead of linking the firmware and simply fake the content type to be the original while setting the content encoding to gzip. This way, the ESP is completely liberated from compression and we can reduce the size of our firmware as much as possible.

Do I need to compress all files manually and somehow save the original content type? Not really. I wrote a simple bash script, that does most of the work for you and creates some header with a look-up table (LUT) for the code to access it easily. A tiny URI-router will search it within the LUT and pick all information it needs from it.

### Putting the pieces together

#### The Angular Project

#### The ESP Project

After we created the ESP project as described in my other post, we will start implementing a simple web service. This is done with
