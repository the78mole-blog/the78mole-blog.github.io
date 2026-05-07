---
title: Code Red on Fire - Or Heat-Metering with Node-Red
date: '2023-04-19'
description: ''
categories:
- Heating
- M-Bus
- M-Bus
- node-red
- Smart Home
tags:
- heat meter
- mbus
- nodered
- PiXtend
- PLC
image: /images/blog/2023/04/M-Bus-Flow.png
---

OK, guys, as you may have noticed when reading my post about [my new heating system](https://the78mole.de/moles-heating-system/), I have three heat meters installed that have M-Bus connectivity. I also wrote some posts about [M-Bus and how to push the data with MQTT](https://the78mole.de/taking-your-m-bus-online-with-mqtt/), [reading M-Bus devices in general](https://the78mole.de/reading-a-meter-speaking-mbus/) or a more [basic M-Bus post](https://the78mole.de/some-thoughs-on-the-m-bus/)...

OK, I just realized, that I'm using a bus that I personally don't favour, way to much...

So, Why the F\*\*\* again M-bus? Because I did not yet manage to implement my BLE-Module for this type of heat meters. The Bluetooth-Module will also speak some sort of M-Bus-protocol internally with the main meter microcontroller, so I ordered the M-Bus variant to have it correctly parametrized in the very beginning. And to be honest, I did NOT rip an opto-head from my previous employer to do the parametrization.

The hardware part of the BLE-Metering-Module is already finished (and will soon become open source), but without a working software, this is just useless. So I decided to give the M-Bus a try with node red and write some post about it.

## The Hardware

OK, first things first. The hardware I'm using is a PiXtend controller, but every other Pi, Pi Clone, PC, Server, Data Center,.. will do, if there is some USB port (or serial port with another adapter) available. I got my [USB-M-Bus-Adapter from aliexpress](https://de.aliexpress.com/item/32742104471.html). I then wired the remainder of my installation. I had most of the cables already running in ducts and only need to screw the wire into the terminals of the adapter.

![](/images/blog/2023/04/image-1024x576.png)

This is my PiXtend V2 -S-, some little Pi-based PLC controller, running node red. I completely refuse to use CODESYS, even if I did some PLC programming in my younger days. This stuff is even to dirty for moles (I hate closed source) :-P

![](/images/blog/2023/04/image-2.png)

On the left, you can see the Landis+Gyr Ultraheat T230 ([technical description](https://www.landisgyr.eu/product/ultraheat-t230/?download=282397&filename=/webfoo/wp-content/uploads/2025/04/T230_Technical_Description_EN_g.pdf), [user manual](https://www.landisgyr.eu/product/ultraheat-t230/?download=397362&filename=/webfoo/wp-content/uploads/2012/09/T230_Operating_and_Installation_Instruction_EN_m.pdf)) with a composite flow tube Qp=1,5 m³/h and an M-Bus module installed. The four wires on the bottom are (from left to right) flow measurment sensors, return temperature sensor, forward temperature sensor and the M-Bus cable. On the right side, you can see a heating water pump Grundfos Alpha 3, that has bluetooth integrated. From this pump I hope to get some flow, pressure and electical values (stay tuned to read about it).

## The Software Part

### Getting Your Device Right

Back to the tindering stuff... After connecting the USB-M-Bus-Adapter, dmesg showed it was found and attached as `/dev/ttyUSB0`:

```bash
pi@pixtendheat:~ $ dmesg | tail -n 13
 usb 1-1.1.3: new full-speed USB device number 5 using dwc_otg
 usb 1-1.1.3: New USB device found, idVendor=0403, idProduct=6001, bcdDevice= 6.00
 usb 1-1.1.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
 usb 1-1.1.3: Product: FT232R USB UART
 usb 1-1.1.3: Manufacturer: FTDI
 usb 1-1.1.3: SerialNumber: AQ02CG2X
 usbcore: registered new interface driver usbserial_generic
 usbserial: USB Serial support registered for generic
 usbcore: registered new interface driver ftdi_sio
 usbserial: USB Serial support registered for FTDI USB Serial Device
 ftdi_sio 1-1.1.3:1.0: FTDI USB Serial Device converter detected
 usb 1-1.1.3: Detected FT232RL
 usb 1-1.1.3: FTDI USB Serial Device converter now attached to ttyUSB0
```

To make life easier, especially when connecting other USB-serial adapters (which I will certainly do in future for connecting ModBus devices) there is a chance, that device names will swap one time. Also when replacing an adapter, you would need to change all your software settings. Therefore, I got used to fix the names of such devices and make them easily customizable using udev.

For this, you need to create a udev rules file. Take the serial from above output, in my case `AQ02CG2X` and run:

```
pi@pixtendheat:~# udevadm info --name=/dev/ttyUSB0 --attribute-walk | grep AQ02CG2X
    ATTRS{serial}=="AQ02CG2X"
```

Now create a new udev rule with this pieces to symlink a new device `/dev/usb-mbus`. You can also use `vi` to create/edit the file :-)

```bash
pi@pixtendheat:~# echo SUBSYSTEM=="tty", ATTRS{serial}=="AQ02CG2X", SYMLINK+="usb-mbus" | sudo tea /etc/udev/rules.d/50-usb-tty-mbus.rules
```

...refreshing udev...

```bash
sudo udevadm trigger
```

If you now list the contens of `/dev`, you will see a symlink `usb-mbus` pointing to `ttyUSB0`. This will happen always automatically, when plugging in this specific USB device. If you need to replace it, just find the serial number again with `dmesg` (after plugging in) and replace it in your udev rule.

### Powering Up Node-Red

If everything was OK, let's pull it into node-red. The description of the module I'm using is called [node-red-contrib-m-bus](https://flows.nodered.org/node/node-red-contrib-m-bus). After installing this module to the palette, you need to restart your node-red. On my PiXtend this is easily achieved by issuing the command `systemctl restart nodered.service` on the shell.

All you get for your efforts are two lousy new nodes:

![](/images/blog/2023/04/image-3.png)

And just a remark from my side, the M-Bus module needs some improvements... Maybe I'll contribute to it in the near future. It needs a command that processes the list of devices and reads their values without scanning for secondary addresses...

To get anything from the meter, you first need to find it on the bus. If you only have one meter connected, chances are high, that is has the default address 1 or simply responds to broadcasts. "Unfortunately", in my case there are four meters conected and more will follow with every upgrade of the heating circuits.

The settings of the controller node are quite easy. Place the controller node in your flow, double-click it and click on the pencil icon in the properties view, then add a new client:

![](/images/blog/2023/04/image-6.png)

When saved, the resulting main properties view of the control node should look like this:

![](/images/blog/2023/04/image-5.png)

As soon as you deploy your program, the nodes will show scanning. Be patient, this can take a minute or two. M-Bus is not known for ultra-fast scanning and data transmission.

![](/images/blog/2023/04/image-4.png)

The reward for all this efforts is a simple line of log :-)

![](/images/blog/2023/04/image-7.png)

The second node will now start to emit (many) messages with data from each meter. It will continuously retrieve this from the meters as long as you have "Auto scan and read" enabled in the client of the controller node. Following is only a tiny fraction of the data from the first meter in the list:

![](/images/blog/2023/04/image-11.png)

[...]

![](/images/blog/2023/04/image-9.png)

![](/images/blog/2023/04/image-10.png)

There are many more values, like the min and max temperatures for flow and return, flow rate maximum value,... Everything you would like to know from the meter :-)

### Optimizing Communication

Since MID heat meters need to be calibrated (or exchanged) every five years, there is a good chance, that secondary addresses will change sooner or later. Therefore, it is a good practice, to assign a primary address to each meter and use this for communication. When you then need to exchange the meter with a new one, you can simply assign the same primary address as the old meter had before. Your whole software then needs no change at all, only sending the "setPrimary" command, containing the following data and you can simply use an inject node to craft the message:

![](/images/blog/2023/04/image-13.png)

The whole content of the payload field is as follows:

![](/images/blog/2023/04/image-12.png)

Then connect the inject node to the controller node, deploy your flow and press the inject button.

![](/images/blog/2023/04/image-16.png)

![](/images/blog/2023/04/image-15.png)

Now, you only need to do this for all your meters and use the setDevices command to hand over an array of meters that should be updated in the auto scan and read loop (this was a default setting in your controllers client config). Therefore, create another inject node, generating the appropriate command.

![](/images/blog/2023/04/image-19.png)

![](/images/blog/2023/04/image-18.png)

The resulting message from the controller was:

![](/images/blog/2023/04/image-20.png)

Now everything should be a bit faster and way better for maintenance :-)

### Improving The Flow

Coming soon...

### Getting The Values into Home Assistant (or on MQTT)

Coming soon...
