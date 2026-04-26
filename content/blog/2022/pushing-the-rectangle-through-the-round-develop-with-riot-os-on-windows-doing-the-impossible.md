---
title: Pushing the Rectangle Through the Round - Develop With RIOT OS on Windows -
  Doing The Impossible
date: '2022-01-11'
description: ''
categories:
- ARM
- Bashing
- ESP32
- OS
- STM32
- Windows
tags:
- ESP32
- IoT
- RTOS
- STM32
image: /images/blog/2022/01/riot-os.png
---

Work in progress

As many of you, I also have Windows 10 natively on my Notebook and don't want to switch to Linux, every time, I do some development that relies on the common Linux cross-development-tools but runs inside MSYS. The great advantage is, that recent notebooks are quite comfortably staffed with CPU power and they are always at your hand.

Just to make it a bit more complicated, the toolchain is always a minor issue to link to it correctly and to extend complexity, I'll also give some hints on setting up the MSP430, STM32 and the ESP32 environment. For ARM, it mostly can be done using the [Getting Started Guide](https://doc.riot-os.org/getting-started.html) on RIOT.

## Preparations

Therefore, I decided to give MSYS2 again some try (see [Windows (was) just a pain](https://the78mole.de/windows-was-just-a-pain/) to get up with MSYS2) and try to build RIOT OS on MSYS2.

When MSYS has been installed, you can simply create some SSH key on the MSYS command line using:

```bash
$ ssh-keygen -t ed25519
```

Answer everything with enter, if it is OK for you to not have the key password protected. Check, where your key-pair has been placed (`/c/Users/$USERNAME/.ssh` or `~/.ssh`) and put a ssh config file beside it with e.g. `vim ~/.ssh/config` or any editor of your choice (need to run in MSYS shell) with the following content:

```bash
Host github.com
ForwardAgent yes
User git
IdentityFile /home/<YOUR_USERNAME>/.ssh/id_ed25519
```

As soon as you did this, put your public key into the settings of your GitHub account. You can show the public key with

```bash
$ cat ~/.ssh/id_ed25519.pub
```

Copy the output and paste it as a new key in your GitHub settings.

To be able to compile the RIOT OS for your specific platform, you need to install the appropriate toolchain:

### ARM Cortex

```
$ pacman -S mingw-w64-x86_64-arm-none-eabi-gcc \
            mingw-w64-x86_64-openocd \
            mingw-w64-x86_64-gdb-multiarch \
            make doxygen wget unzip \
            mingw-w64-x86_64-python-pyserial

# Be sure to add the path to the compiler to your PATH environment by adding the following to your ~/.bashrc
$ vim ~/.bashrc

[...]
PATH=${PATH}:/mingw64/bin/
export PATH
```

### ESP32

Download and install ESP-IDF in your Windows environment. Follow the Get Started - ESP32 page (you only need to install the ESP-IDF and optionally the VSCode extensions.

### MSP430/MSP430F

There is only a single board left for this arch... There is a high change, that you need to create your own board definition for a development board using this, including to add some of the forgotton cpu regs...

### General

To find available boards quickly, clone the GIT and run `make info-boards` on the shell.

## Getting the Code

```bash
$ cd ~
$ mkdir GIT
$ git clone git@github.com/RIOT-OS/RIOT.git
```

## Creating the Hello World Application

### Manual creation of application

Since we first want to understand the structure for extending riot, which also applies for modules and drivers, we will first do it manually. We will follow the guide on the [RIOT doc page](https://doc.riot-os.org/creating-an-application.html).

```
$ mkdir hello_world
$ cd hello_world
```

Create a main.c with following content:

```c
#include <stdio.h>

int main(void)
{
    puts("Hello World!");
    return 0;
}
```

Create the file Makefile with following content:

```bash
# Set the name of your application:
APPLICATION = helloworld

#BOARD ?= esp32-wroom-32
#BOARD ?= msb-430h
# We will use the STM32F429-DISC1 for further stuff... In a later blog post, I will also show the ESP32...
BOARD ?= stm32f429i-disc1

# When using ESP32, put the path in, where you installed the ESP-IDF, e.g.
#ESP32_SDK_DIR=/c/Users/the78mole/esp/esp-idf

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../../RIOT

include $(RIOTBASE)/Makefile.include
```

### Generating an Application with riotgen

To generate the base structure of RIOT extensions (applications, boards, modules, drivers, examples packages and tests) easily and efficiently, some can also make use of the [riotgen](https://pypi.org/project/riotgen/) tool, which is available as a python module through a pypi project. To install riotgen, simply execute:

## Starting to build

```bash
$ make info-programmers-supported
```

You should should be informed, that the programming tool is esptool for ESP32, mspdebug for MSP430 and .

If you selected the STM32 board an also added the path to ARM-GCC correctly, you should be able to see the following output:

![](/images/blog/2022/01/image-1.png)

stm32f429i-disc1 would be the correct board... otherwise, serial over ST-Link will not work (just an older screenshot)

## Adding Blinken Lights to Hello World

TODO

## Target specific configs

#### STM32

To be able to run openocd with the stlink command, you need to add some stlink.cfg, that fits your environment. You also need some ST-Link or a discovery board with an integrated ST-Link.

## Flashing Your Target

Flashing with OpenOCD (e.g. for STLink) does not work out of the box in MSYS2 and needs some little push. OpenOCD can not find the stlink.cfg, you should edit the `RIOT/dist/tools/openocd/openocd.sh` and add two lines of code to adjust the absolute path and prepend it with the drive-letter in windows style... OK, a very dirty fix, but at least, it works for the moment :-P

```bash
#!/usr/bin/env bash
#

# Work around a mingw/MSYS2 bug with absolute filenames and linux style drive-letter path
OPENOCD_ADAPTER_INIT=$(echo $OPENOCD_ADAPTER_INIT | sed -e 's/\/\(.\)/\1:/')

[...]

#
# now comes the actual actions
#
do_flash() {
    IMAGE_FILE=$1

    # Another workaround to fix a bad mingw/MSYS2 behaviour
    IMAGE_FILE=$(echo $IMAGE_FILE | sed -e 's/^\/\(.\)/\1:/')
    test_config
    test_imagefile
```

After that, to flash your target, simply execute:

```
make flash
```

...showing somehting like this:

```bash
$ make flash
Building application "helloworld" for "stm32f429i-disc1" with MCU "stm32".

"make" -C /c/GIT/XYZ/RIOT/boards/stm32f429i-disco
"make" -C /c/GIT/XYZ/RIOT/boards/stm32f429i-disc1
"make" -C /c/GIT/XYZ/RIOT/core
"make" -C /c/GIT/XYZ/RIOT/cpu/stm32
"make" -C /c/GIT/XYZ/RIOT/cpu/cortexm_common
"make" -C /c/GIT/XYZ/RIOT/cpu/cortexm_common/periph
"make" -C /c/GIT/XYZ/RIOT/cpu/stm32/periph
"make" -C /c/GIT/XYZ/RIOT/cpu/stm32/stmclk
"make" -C /c/GIT/XYZ/RIOT/cpu/stm32/vectors
"make" -C /c/GIT/XYZ/RIOT/drivers
"make" -C /c/GIT/XYZ/RIOT/drivers/periph_common
"make" -C /c/GIT/XYZ/RIOT/sys
"make" -C /c/GIT/XYZ/RIOT/sys/auto_init
"make" -C /c/GIT/XYZ/RIOT/sys/auto_init/usb
"make" -C /c/GIT/XYZ/RIOT/sys/event
"make" -C /c/GIT/XYZ/RIOT/sys/fmt
"make" -C /c/GIT/XYZ/RIOT/sys/frac
"make" -C /c/GIT/XYZ/RIOT/sys/isrpipe
"make" -C /c/GIT/XYZ/RIOT/sys/luid
"make" -C /c/GIT/XYZ/RIOT/sys/malloc_thread_safe
"make" -C /c/GIT/XYZ/RIOT/sys/newlib_syscalls_default
"make" -C /c/GIT/XYZ/RIOT/sys/pm_layered
"make" -C /c/GIT/XYZ/RIOT/sys/tsrb
"make" -C /c/GIT/XYZ/RIOT/sys/usb/usbus
"make" -C /c/GIT/XYZ/RIOT/sys/usb/usbus/cdc/acm
"make" -C /c/GIT/XYZ/RIOT/sys/ztimer
   text    data     bss     dec     hex filename
  19344     176    4584   24104    5e28 C:/GIT/XYZ/RIOT/hello_world/bin/stm32f429i-disco/helloworld.elf
echo ""

/c/GIT/XYZ/RIOT/dist/tools/openocd/openocd.sh flash /c/GIT/XYZ/RIOT/hello_world/bin/stm32f429i-disco/helloworld.elf
### Flashing Target ###
Open On-Chip Debugger 0.11.0
Licensed under GNU GPL v2
For bug reports, read
        http://openocd.org/doc/doxygen/bugs.html
hla_swd
Info : The selected transport took over low-level target control. The results might differ compared to plain JTAG/SWD
Info : clock speed 2000 kHz
Info : STLINK V2J36M26 (API v2) VID:PID 0483:374B
Info : Target voltage: 2.856743
Info : stm32f4x.cpu: hardware has 6 breakpoints, 4 watchpoints
Info : starting gdb server for stm32f4x.cpu on 0
Info : Listening on port 59743 for gdb connections
    TargetName         Type       Endian TapName            State
--  ------------------ ---------- ------ ------------------ ------------
 0* stm32f4x.cpu       hla_target little stm32f4x.cpu       running

Info : Unable to match requested speed 2000 kHz, using 1800 kHz
Info : Unable to match requested speed 2000 kHz, using 1800 kHz
target halted due to debug-request, current mode: Thread
xPSR: 0x01000000 pc: 0x08000804 msp: 0x20000200
Info : device id = 0x20016419
Info : flash size = 2048 kbytes
Info : Dual Bank 2048 kiB STM32F42x/43x/469/479 found
auto erase enabled
wrote 32768 bytes from file c:/GIT/XYZ/RIOT/hello_world/bin/stm32f429i-disco/helloworld.elf in 1.104519s (28.972 KiB/s)

verified 19520 bytes in 0.184755s (103.177 KiB/s)

Info : Unable to match requested speed 2000 kHz, using 1800 kHz
Info : Unable to match requested speed 2000 kHz, using 1800 kHz
shutdown command invoked
Done flashing
```

This should now execute the make dependencies again (e.g. compiling stuff) and then start OpenOCD to flash your target.

Connecting Seriously To Your Board

OK, seriously serially :-) If you want to connect using the serial interface (of the STLink on Disco Boards), you should first install python serial using pip:

```bash
$ pacman -S mingw64/mingw-w64-x86_64-python-pip
$ # pip install serial # maybe this line is not needed and not working...
$ python -m pip install pyserial
```

After installing, try executing `make term PORT=/dev/ttyS4` (or the port that belongs to the STLink). If your board supports the UART over ST-Link, like the DISC1 does, it should show something like the following and print a new line of `Hello World!` every time you press reset.

```bash
$ make term PORT=/dev/ttyS4
/c/GIT/XYZ/RIOT/dist/tools/pyterm/pyterm -p "/dev/ttyS4" -b "115200"
Twisted not available, please install it if you want to use pyterm's JSON capabilities
2022-01-25 00:03:23,222 # Connect to serial port /dev/ttyS4
Welcome to pyterm!
Type '/exit' to exit.
2022-01-25 00:03:25,685 # main(): This is RIOT! (Version: 2022.01-devel-1577-g2491b)
2022-01-25 00:03:25,686 # Hello World!
2022-01-25 00:03:26,657 # main(): This is RIOT! (Version: 2022.01-devel-1577-g2491b)
2022-01-25 00:03:26,658 # Hello World!
2022-01-25 00:03:27,401 # main(): This is RIOT! (Version: 2022.01-devel-1577-g2491b)
2022-01-25 00:03:27,402 # Hello World!
```

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+pushing-the-rectangle-through-the-round-develop-with-riot-os-on-windows-doing-the-impossible&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
