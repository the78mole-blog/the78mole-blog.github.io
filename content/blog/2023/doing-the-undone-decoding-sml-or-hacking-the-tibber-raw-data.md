---
title: Doing the Undone - Decoding SML or Hacking the Tibber Raw Data
date: '2023-05-30'
description: ''
categories:
- Smart Home
- Tibber
- Uncategorized
tags:
- sml
- tibber
image: /images/blog/2023/05/title.png
---

## The Problem I Encountered...

Just after installing the Pulse IR and the Tibber Bridge, I was quite a bit frustrated about the continuity of the Tibber data. This was not caused by a long distance between the Pulse IR and the bridge, it was mostly related to an unstable WiFi. I believe, the root cause was, that the WiFi, the bridge was connected to, is loaded with a lot of traffic, just knocking down the tiny controller of the bridge. So, the first step to improve the situation was to link the bridge in some other WiFi network, that has almost no traffic at all (in my case, it was the WiFi of my Fritz!Box, that is connected to the DMZ, while my real WiFi is behind the Unifi Security Gateway. The bridge moved also to another location, further away from the Pulse, but in close proximity to the FritzBox. And now, everything worked mostly reliable.

Then another problem came up. Home Assitant has a nice tibber integration, but this integration receives the data from the Tibber API by opening a websocket. If the cloud services is not reachable (happens from time to time), you get no data.

Oh mole, how nice would it be, to receive the SML data from the meter as JSON or at least as raw data...

## 1st Step - The Tibber Bridge Webserver

The Tibber bridge opens it's web server only during the initialization pahse. But if you do not connect with your Tibber app but with a standard web browser, you will get way more interesting stuff, like some URL providing the raw SML data. You can find the whole investigation in the [OpenWB community forum](https://openwb.de/forum/viewtopic.php?t=5842&start=60) or on [Wyraz blog](https://blog.wyraz.de/allgemein/a-brief-analysis-of-the-tibber-pulse-bridge/).

To explain it quickly:

- Note down the password, printed on the socket of your tibber bridge (you can only read it, when unplugged). Plug it in again and let it connected for at least a minute.
- Now power-off the bridge two times in a row (approx 2 seconds interval) and wait for the LED to light up green.
- Use a browser to connect to the URL of your bridge: http://tibber\_bridge/data.json?node\_id=1 (maybe you need to use the IP, if your routers DNS resolution does not work)
- Username is `admin` with the passwort you noted down in the beginning.
- Chose the params-tab of the web interface

![](/images/blog/2023/05/image.png)

- Go to the last param `webserver-force-enable` and set it to `true`. Then press `Store params to flash`.

![](/images/blog/2023/05/image-1-1024x139.png)

This enables the webserver even after initialization. When you have finished this, wait half a minute and power-cycle you bridge.

## 2nd Step - Getting SML Data From The Bridge

To retrieve the data from the bridge, just call curl with username `admin` and your password and pipe it through `xxd` (some hexdump converter) to further inspect it with wireshark later on. We will create afolder, we can easily work in below our home directory and then start playing/digging :-)

```bash
cd ~ && mkdir smltest && cd smltest
curl -s -u admin:<PASS> http://tibber_bridge/data.json?node_id=1 | \
  tee sml.raw | \
  xxd -g 1 > sml.hex
cat sml.hex
```

If you see the hex dumped message, containing blocks of `77 07 01`, it is a good indication, that you received a valid SML message.

#### Optional Step - Using Wireshark for Inspection

If you want to use wireshark to quickly have a look into your SML, you can

```bash
text2pcap.exe -4 10.0.0.1,9.9.9.9 -T 1111,2222 -t "%F %T."  \
  sml.hex -a sml.pcap
```

The latter command is to somehow wrap your data into a network packet. This is needed, because wireshark can only analyze network dumps. This is the way to fake a network packet.

When you have done this, start wireshark and open the sml.pcap file.

After opening the file, you will not see it decoded. Therefore, we need to configure the SML protocol to match on the correct port (1111 in our case).

![](/images/blog/2023/05/image-2.png)

Now you should already see a SML field and its data can be expanded

![](/images/blog/2023/05/image-5.png)

That already looks fine, but the decoder of WireShark is not very elaborate... But it is enough to see, if the SML has valid data..

## 3rd Step - Building a Command Line SML-Decoder

Unfortunately, there is not a sinlge SML command line decoder available. The only thing you can get is a library for decoding, called [libsml](https://github.com/volkszaehler/libsml). Recent Debian package repositories unfortunately have a very old version available, so you need to install it manually or using the third party package repository (recommended).

But there is also a python library, that can do already a little more than libsml... It's the python [smllib](https://pypi.org/project/smllib/) from pypi. And there is also some application [sml2mqtt](https://pypi.org/project/sml2mqtt/) that can read SML data from a serial device and send the data to MQTT (I added a feature request to the GitHub project, since this would be an awesome solution). In our application with Pulse IR and Tibber Bridge, we have no serial device. We could create some dummy virtual serial device and post the data to it, but this would be a very nasty solution...

In the meantime (until the feature request is implemented :-) ), we use a tiny python tool, to analyze the SML data, provided by the Tibber Bridge. First of all, we install the smllib:

```bash
pip install smllib
```

Then we create our simple python tool:

```python
import sys
from smllib import SmlStreamReader

stream = SmlStreamReader()
data = sys.stdin.buffer.read()
#stream.add(b'BytesFromSerialPort')
stream.add(data)
sml_frame = stream.get_frame()
if sml_frame is None:
    print('Bytes missing')

# Shortcut to extract all values without parsing the whole frame
obis_values = sml_frame.get_obis()

# return all values but slower
parsed_msgs = sml_frame.parse_frame()
for msg in parsed_msgs:
    # prints a nice overview over the received values
    print(msg.format_msg())
```

We can then simply execute our program

```bash
cat sml.raw | pyhton3 pysmlparser.py
```

You should see a detailed analysis of the SML data. Now you could also retrieve fresh SML data from your Tibber Bridge.

```bash
curl -s -u admin:<PASSWORD> \
  http://tibber_bridge/data.json?node_id=1 | \
  python3 pysmlparser.py
```

## 4th Step - Pushing Your Data to Home Asssitant

Soon I'll continue on how to push the data to your Smart Home. But yet I'm not sure, if I'll do this with MQTT.

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+doing-the-undone-decoding-sml-or-hacking-the-tibber-raw-data&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
