---
title: wmBus Meters And How To Get It Into Home Assistant
date: '2021-07-13'
description: ''
categories:
- Bus Systems
- Home Assistant
- Smart Home
- wmBus
tags: []
image: /images/blog/2021/07/MBusWirelessLogo.jpg
---

Recently, I decided to switch over to Home Assistant due to instability of iobroker. Maybe I had too many adapters, slaves or what else... Somehow it did not function properly anymore. Also the UI of Home Assistant and its performance is much better than iobroker in my opinion. So I gave it a try and most of my stuff was quickly integrated, especially the HomeMatic stuff with some Paspberry Pi 3 used as the CCU.

But one problem came up again... How to get my wmBus and M-Bus meter readings in. As I wrote in some [p](https://blog.the78mole.de/integrating-wmbus-devices-into-iobroker/)[revious post about wmBus](https://blog.the78mole.de/integrating-wmbus-devices-into-iobroker/), I could not find a software able to decode the Messhelden (manufacturer code AAA) heat cost allocators correctly outside of iobroker (the working software was: <https://github.com/ISFH/ioBroker.wmbus>). So I gave [wmbusmeters](https://github.com/weetmuts/wmbusmeters) a second try to publish the read values via MQTT.

After quite some work with updatigng my (really outdated) codebase, fixing stuff, integrating my two new meters, documenting, how to add a new meter and a help of the really active maintainer of wmbusmeters, I managed to get everything done. Take some Raspberry Pi, put the wmBus-Stick in place (I use IMST iM871A-USB) and move on with the software.

Just do the relevant steps: Cloning, building, installing, configuring enjoying:

```bash
pi@wmbuscollector:~ $ mkdir GIT
pi@wmbuscollector:~ $ cd GIT
pi@wmbuscollector:~ $ git clone https://github.com/weetmuts/wmbusmeters.git
pi@wmbuscollector:~ $ cd wmbusmeters
pi@wmbuscollector:~ $ ./configure
pi@wmbuscollector:~ $ make
pi@wmbuscollector:~ $ sudo make install
```

Configuration can bea easily done by editing the file /etc/wmbusmeters.conf:

```bash
loglevel=debug
device=/dev/ttyUSB0:t1
logtelegrams=true
format=json
meterfiles=/var/log/wmbusmeters/meter_readings
meterfilesaction=overwrite
meterfilesnaming=name-id
# meterfilestimestamp=day
logfile=/var/log/wmbusmeters/wmbusmeters.log
shell=HOME=/home/wmbusmeters/ /usr/bin/mosquitto_pub -h 172.22.2.137 -u mqtt -P mypass -t wmbusmeters/$METER_ID -m "$METER_JSON"
json_address=Elfenstrasse 12
json_city=Bruchsaal
```

Now start wmbusmeters with the following command and watch it fetching packets:

```bash
pi@wmbuscollector:~ $ wmbusmeters --useconfig=/
```

Now you simply need to add meters that shall be collected and published on MQTT. This is done by placing a single file per meter in /etc/wmbusmeters.d

```vim
name=NBEGGLWS
type=aventieshca
id=60900128
key=FFD16C9C361B0B7E094A2AED3DCA1B58
```

The keys is only needed, if your meter sends encrypted data and you should have received the key from your manufacturer/seller of the meter.

My meters' data now gets transferred via MQTT and my Home Assistant simply fetches it and puts it into is history store (sqlite & influxdb in my case). The appropriate YAML in Home Assistant looks like this:

```yaml
sensor: 
 - platform: mqtt
   name: "HCA NBEG WS"
   unique_id: wmbus.60900128
   state_topic: "wmbusmeters/60900128"
   unit_of_measurement: "hca"
   value_template: "{{ value_json.current_consumption_hca }}"
   json_attributes_topic: "wmbusmeters/60900128" 
```

All attributes (other sensor values) simply get packed into the attributes of the new sensor.

![](/images/blog/2021/07/image-6.png)

Happy metering!

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+wmbus-meters-and-how-to-get-it-into-home-assistant&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
