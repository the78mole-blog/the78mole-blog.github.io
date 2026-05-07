---
title: Kathrein EXIP 418 - Getting It Back To Work on Ubiquity Networks
date: '2021-06-20'
description: ''
categories:
- Networking
tags:
- exip
- exip 418
- kathrein
- satip
- ubiquity
- unifi
image: /images/blog/2021/06/PF_SIP_EXIP418_Front_600x600-e1624186422390.jpg
---

I've installed a Kathrein Sat>IP-Server from Kathrein quite some time ago and it worked more or less flawlessly in the beginning. Also my Sat>IP-Receiver, I bought a few month ago is working well. But when I try to connect with VLC, I encounter a nasty problem:

![](/images/blog/2021/06/image.png)

So I checked, what is available on the given URL... In fact, www.satip.info list many playlists, but this exact address gives a 404 HTTP-Error. OK, so I downloaded the ASTRA 19.2E-Playlist and now I had the problem, that the hostnames within the playlists refer to sat.ip... Now I had two options:

1. Search/replace the sat.ip hostnames with the IP address of my EXIP or
2. The more elegant way, to configure my DNS forwarder to resolve it with the EXIP's IP address

I decided to do the second option. Since I have a Ubiquity UniFi networking here, it is not as easy to set a static DNS record. Therefore, you need to log in to your USG by SSH and set this entry on command line. You need to know the credentials you can adjust in UniFi networking (with new UI) through Settings -> System Settings -> Controller-Configuration -> Device SSH Authentication.

![](/images/blog/2021/06/image-4-1024x544.png)

Here is a [forum post](https://community.ui.com/questions/Setting-up-local-DNS-Unifi-Security-Gateway/bb853549-aaa5-48b0-89dc-3a3755d5b016) explaining it on the command line. In short, do the following:

![](/images/blog/2021/06/image-1.png)

That was all (at first)... When I now ping sat.ip on my local machine, it directly accesses the EXIP 418 on IP address 172.22.2.101

![](/images/blog/2021/06/image-3.png)

OK, fine... No just use the channels playlist you downloaded on <https://www.satip.info/resources/channel-lists/>, open it with VLC and things will magically work :-P

#### If Things Do Not Persist...

If this does not persist the settings (for me it work the second time magically), you need to put it in some JSON config and place it on the UniFi Network Controller, to get provisioned by default. This can be done as described [here](https://web.archive.org/web/20210412001638/https://help.ui.com/hc/en-us/articles/215458888-UniFi-USG-Advanced-Configuration-Using-config-gateway-json) and [here](https://community.ui.com/questions/Static-DNS-entry/0a0265a7-ec31-4091-8304-9787da328367).
