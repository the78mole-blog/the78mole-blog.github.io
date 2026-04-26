---
title: Getting Started Embedded - Part I - The Toolchain
date: '2018-08-16'
description: ''
categories:
- ARM
- STM32
tags: []
---

## Introduction

For getting started with any embedded development, the most important piece is the toolchain.

Many people suggest to use Keil, IAR, or some other fancy, professional, rocket-sience (and very expensive) IDE. In my opinion, that is just rubbish.

In former days, when tiny embedded controllers just have not been designed with compilers in mind, it was good to have some highly optimized compilers that could transfer a piece of C code to the ASM of these devices.

Nowadays, processors are designed with compilers in mind. Therefore, I would highly recommend to use GCC not only because of its low price tag (0 $), but because of its stunning community and active development. Since the community and many companies still putting so much effort into this piece of software, no single company can compete with an own closed source product.

## Installing the ARM toolchain

[![](/images/blog/2018/08/gccegg-65.png)](https://gcc.gnu.org/)

There are many possible sources, where you can get GCC and all the tools you need to start. You can compile ARM-GCC yourself using your platform GCC, download the one from [ARM directly](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm), take a release from [GNU MCU Eclipse](https://github.com/gnu-mcu-eclipse/arm-none-eabi-gcc/releases) and many many more...

Don't know what to do? Just get kickstarted, and give XPM (a node/npm module) a try. Download and install [node.js](https://nodejs.org/en/). The version does not matter too much. If you are not developing with node.js itself, better stick to the stable version.

When node.js is installed, install xpm and the ARM GCC toolchain (same for Windows, Linux & macOS):

```
me@diggerVM:~$ npm install xpmme@diggerVM:~$ xpm install --global @gnu-mcu-eclipse/arm-none-eabi-gccme@diggerVM:~$ arm-none-eabi-gcc -v
```

OK, that was easy... If this worked, you maybe need some supporting tools. Best practice differs a bit, depending on your platform. For Linux, just install the build-essentials package (Debian dn ubuntu call it like this).

```
me@diggerVM:~$ sudo apt-get install build-essentials
```

For Windows (would also work for Linux, but I prefer the OS provided package), you can use xpm again:

```
C:\Users\me\>xpm install --global @gnu-mcu-eclipse/windows-build-tools
```

After this has finished, you possibly need to add the build tools to your PATH environment. You will find it in %APPDATA%\xPacks\@gnu-mcu-eclipse\windows-build-tools\2.11.1-1\.content\bin.

## Testing your Toolchain

To test your setup, just clone, download,... the [STM32 example project](https://github.com/the78mole/stm32-example). Open a command line prompt, cd to the project directory and fire make:

```
me@diggerVM:~/GIT/stm32-example$ make
```

If this worked without errors, you have your toolchain up and running. Congratulations!

## What's next...

The next post will explain, how to setup STM32CubeMX and the Eclipse IDE to start developing own embedded applications effectively. Until now, there is not much difference to commercial IDEs and Toolchains from a workflow point of view. But don't worry, we still have automation in mind and the goal is to have a CI-Pipeline running soon.

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+getting-started-embedded-part-i-the-toolchain&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
