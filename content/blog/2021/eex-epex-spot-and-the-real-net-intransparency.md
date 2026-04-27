---
title: EEX, EPEX SPOT And The Real Net-(In)transparency
date: '2021-10-16'
description: ''
categories:
- Home Assistant
- node-red
- Smart Home
tags:
- epex
- epex spot
- market data
- node-red
- strombörse
- strompreise
image: /images/blog/2021/10/EPEX-SPOT-Post.png
---

Have you ever been interested in the current EEX or more correctly the EPEX SPOT prices? If so, you quite certainly stumbled over the [EPEX SPOT Home](https://www.epexspot.com/en) or the [Energy Charts](https://energy-charts.info/charts/price_spot_market/chart.htm?l=de&c=DE) from [Fraunhofer ISE](https://www.ise.fraunhofer.de/). Beside the fact, that they are (mostly) way below the prices you pay for your household electricity, there is a nice side fact currently: They climb up to heaven instead of going down to hell...

![](/images/blog/2021/10/image-9-1024x485.png)

Chart of 2021 from [ISE Energy-Charts](https://energy-charts.info/charts/price_spot_market/chart.htm?l=de&c=DE&legendItems=0000100000000&interval=year)

As you can see, the price has been around 5 ct/kWh (50 €/MWh) beginning of the year (and all the years before 2021) and raising around June/July. This mostly has to do with rising gas prices, that also climb up continuously and pushing all other energy prices.

Since the electricity prices are built by a market, the gas power plants dictate the high prices and all other plants (that would be cheaper) get the same money for the energy, they deliver.

So, if you want to do your electricity provider a favor, you could simply draw power, when the prices are low. In fact, it will lower the prices for all customers of your specific region in the future.

But there is a minor problem with that. You can look up the prices one day in advance (it is published around 12:45 for the next day), but you need to do it manually or pay for the API of [EPEX marketdata](https://webshop.eex-group.com/). When you manage to select the appropriate products, you will realize, that it is worth 50 bucks (SFTP) or 100 (API) per month, paid in advance for one year.

![](/images/blog/2021/10/image-10.png)

![](/images/blog/2021/10/image-11.png)

What I do not understand is, that there is no regulation to provide the market data in real time through an API for free. They provide it as a table on their website, but not well readable. So, for the technically skilled person, the table is what is needed, to get it automatically :-P The downer is, that you need to adjust your script, if the page layout (at least the table design) changes.

Here is, how I did it in node-red (palettes needed: node-red-contrib-cron-plus, node-red-contrib-date, node-red-contrib-home-assistant-websocket):

[EPEX-SPOT-Price-Crawler](https://the78mole.de/wp-content/uploads/2021/10/EPEX-SPOT-Price-Crawler.json)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/10/EPEX-SPOT-Price-Crawler.json)

![](/images/blog/2021/10/image-12-1024x452.png)

You need also the [HACS Extension for node-red](https://github.com/zachowj/hass-node-red).

And the result after adding it to one of your dashboards is:

![](/images/blog/2021/10/image-13.png)

![](/images/blog/2021/10/image-15.png)

One way to improve it, is to fetch the whole day ahead prices, store it permanently with some node and only retrieve the new information once a day, instead of once an hour. If someone is willing to improve it, feel free to send me an update.

I also wrote some node-red flow for getting the prices from aWATTar, that give you free access to their API (thanks guys):

[aWATTar\_prices](https://the78mole.de/wp-content/uploads/2021/10/aWATTar_prices.json)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/10/aWATTar_prices.json)

![](/images/blog/2021/10/image-16-1024x298.png)

Have fun with node-red and write me your comments...
