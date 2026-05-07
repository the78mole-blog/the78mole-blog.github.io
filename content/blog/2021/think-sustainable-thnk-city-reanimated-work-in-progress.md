---
title: Think Sustainable, TH!NK City (reanimated) - Work in Progress
date: '2021-05-20'
description: Ever heard about the TH!NK City electric car? No? Before I got asked
  to help bringing it to life again, I also didn't. In fact, if you do not count the
  first cars at all, which have been electrical, too, it was one of the first electric
  cars, at least in the 21st century, that entered serial production somehow. Now
  these cars are mostly dead, because the battery died when not used for some time...
categories:
- Electric Car
tags:
- EV-Battery
- TH!NK City
- Think City
image: /images/blog/2021/05/Akku_Think-bg.png
---

This is the first large project, I will document on this blog. Since it is a work in progress, there is no guarantee it will come to a happy end. Stay tuned and also watch the progress on YouTube on my favorite channel [Steve&Julian#IGEMBB](https://www.youtube.com/channel/UCaCaZ-vKtnMG2_FKmEePChQ)...

## What Is It All About?

Ever heard about the TH!NK City electric car? No? Before I got asked to help bringing it to life again, I also didn't. In fact, if you do not count the first cars at all, which have been electrical, too, it was one of the first electric cars, at least in the 21st century, that entered serial production somehow. This happened a few years, before Tesla was born. Now many TH!NK Cities exist, that have been produced around 2010 and now living their dire existence in a corner of some garage. During their past few years without charging and mainteanance, their battery degraded to a state that they could not be brought back to live by a simple repair.

There are already some guys that reanimated the TH!NK City, but there needs to be some easier solution, which can be done by skilled handyman. Here are some of the public projects:

- [Das Projekt TH!NK City - Fingers elektrische Welt](https://www.fingers-welt.de/phpBB/viewtopic.php?f=14&t=9095)
- YouTube: [Think A306 Lion Power Limit Repair](https://youtu.be/AtHaz4wroEg)
- [Arndt's Blog - Mein Think, wie alles begann](https://web.archive.org/web/20250119092402/https://arndt-barop.info/2018/11/30/mein-think-city-wie-alles-begann/)
- YouTube (IGEMBB): [Lässt sich der AKKU noch retten? | TH!NK City | Eine Elektroauto Legende wiederbeleben](https://youtu.be/O9UgFPNdCTU)

https://youtu.be/O9UgFPNdCTU

I'm part of the latter project :-P and you will find design files and documentation in [my GitLab project](https://gitlab.com/the78mole/igembb-elektronik).

## About TH!NK City's Problem and The Energy Storage

The TH!NK City was produced with two types of battery. The first iteration was a ZEBRA battery, made of NaNiCl and has a working temperature of around 300°C. This batteries mostly survived and just need to be heated up. The second iteration was a LiPo-Stack with a 96s4p (mixed from 12p2s blocks) configuration. Many of the packs show degraded cells, going down to only a few mV, which means, the cells are damaged with lasting "effects" and it will not be safe to reanimate them. Nevertheless, it can be done, but it needs special attention and maybe replacement of some of them or a total recombination with less power and energy. In our project, we will first reanimate the defect cells, measure the conditions, decide on what to do and then bring the TH!NK back to life.

To tackle the problem, we will first collect some data about the battery and the individual cells without damaging too much of it all. After disassembling the battery to inidividual modules, we need to get access to the single cells (in fact to the 2p-pairs). Measuring the connector pins and looking at some photos of [Arndt's blog](https://web.archive.org/web/20250119092402/https://arndt-barop.info/2018/11/30/mein-think-city-wie-alles-begann/), we identified the correct pins. A1-A11, B1-B10, A18-A21 and B18-B21 are potential candidates for the thermistors/NTCs. This arises from the pictures of the cell connection foils from Arndt's blog.

![](https://lh3.googleusercontent.com/CzpsuzPl-nXXu5_qBVy-3Ldjb4-oYSAHAT_wIxtc-YNRQHO7KoqzIR8ZbjfCWWTSokXfqTM6k05H_WaJi3cx8xEgRRoS4xUViaj6u3Mp8KXJxNo2fjR9bRaueQMuOVGS5UBbvxVh1BT2YHVYs0lQAHmDv0yxPdTqgSphZcXI_cN1ZOFy21YAJWa7PgDOT8wDoWR4E2-Ncd_rG3_sYniXhP6XzKYIsT-kA2QDuxXlsfTkYLYjRTsE0b36ZvxH3XMHHzEkB3-8vld1B24sQyU0OaTZ-5huGR_XFimtJRF8XAKk7IQfvqToNnV8UKwMpLTn2j6sqGAcx-1bepEbDBaV0BxVyjIqOkPvhzCpDUvjJ63v9MGTSn_xG65SwIfVJXaRMbORUKMQIONERgsuWcEtjEZjnsPoFWBREH7ZhJPKSotRhoUUpt9vPJ8yZEW_0dp6OjPuuGHhV3vs8vKLFCtV-oCM23xiBnTmCV7-19fDMaQG9tAwriiAVdHaWC1AtQbc8yPo15vLGJS0UqPPI6q4tdemfFCrWP9bKoxPdLqZ_-wO0p60JdcUp5oBYT2FveLaIvmY_h8OYhxfZRx_WwEgiUHgPyY_C0lERE_u2AJWnArLanwLGp8_IXCLR8D8nyqHtc0tv-PW4A3bt1atsAb6SXlRSAfnYSeEdY9vVwc-A6WQk6zU0acsrnmvNWlSNzNk_QymxECFVsUfiK6-EKEvriD0dA=w550-h630-no?authuser=0)

Cell taps on the pack's balancing connector

We (in fact it was all Eric) then measured the voltages of all cells in the TH!NK battery and found a bunch of low and zero volt cells. Cells below 2.5V are presumed to be pre-damaged, cells below 2.0V could be counted as dead. But as I told, we try to wake them up for some tests, before we replace them or re-organize the stack.

![](/images/blog/2021/05/image-4.png)

Cell voltages of all battery packs in our walk-in patient

## First Step - Reanimate The Dead

We (again Eric did it) then charged the dead cells through their balancing connector with only a few hundred milli-amps to bring it up to around 3V. After that, we connected an iCharger X12 to charge the packs and pull out some data of the pack and it's cells.

![](https://lh3.googleusercontent.com/4tS0zMErBtz36af8LN4wIzDMWB8y-jbAYlD4uP2RxXnGNCbJrNhP6RqpoH_UCrGTuggG1tlp0_ec06g_klFN_UnPfVzt1R05XaGmTb6bl4ilFJjp-YEz-ZnJaCIF28soIDkFqVNbFtce6rneQ_lIH7kJ4hDLFSWCKKCKzR4py2Nwby7AAj-yOWNpi9r8Hub9yZ7FzU0BS79G4p0d_QDQYKRcPYKl-E_CwHE2HuImLf0Os9lwgbOYdj-R8omHYSXAnlWLHQuSatr62FM7khb0Q-Ey0hDauYrIIIUp4UeWYBRPQwbo8aYAk8JR4r_JotV-TasI23-tWBXilu61oeha8CYTcFcWQuW4c97GZuF5SOu3aeOwPgaH6XVMqu_JWBuwduKrSC90XGP-kMkOUVS112YwPLKZRg1qxiJZLpQT3GoqZw7YqY3gHhN6PBnJ4K5J5PX3MNy3gMQhulIfVRdzasllazcQkaF7-fGLUohZCerK-rR9WcYYpmQvLSMtaZwVWBMn0R2-jrIb_cH811CKJsZTIvviDYgjTvISvERMMZ2UbZ34-g_enSHe8SokHrCsvA4RbsQWIHhvAcfkrAUghW0TLIckzTT3GSLV-d7RT6uIzWZ-MEF9vxa7JbIECHxjfu4WzZ116ZOZLE-laxGGc3ovYz4CHNGehIgjGJtE8NzxJdh-dB3ec9E90yxNJ79kTTcViLoVaY69I43sOjBNQn6Naw=w758-h948-no?authuser=0)

First measurements after precharging the defect cells of one pack showed promising results. Cell 12 was a zero volts candidate.

![](https://lh3.googleusercontent.com/pYIAo_wpI86MUiNb0tWHmEdnGlK17bED_6TQLTwISv4gezcGUZUapiKeMDqGKr534Hfih5fXrS2qv_9BipUfFrDgVCFa5sLt5v8kiAgoXkt8b96VRhSd-66FtrFTKx0Myf31viucjWrEXfEoRtunmT1-NNVJb24wPh7sauH3rNpPAIzYNLNlYyqW9-JH_U839n1Ne_fNyRtgRw6yeOzBtFKz3a4YbsHouf8NdBncHb4Tuh0WlMmxJDs9T1nYFWMQxxuXQ8Wje6z5RuyCdBvfU0cw1tA5LSb3RTzKzNAaaezeYau57SMBwmYGQ5Flv_bOphq1likIahFE23eOUfM-4DZn3iqW-nZQ10cyRPue_IR8aXsb42BFzKHd_eynR0jSK6Jwi7ZZyJkT0P9swLe_OFTNeVVzR50OVsRS6qS0StptRwsP2ZOXStw1sgvPi6SVCrmvkXf4Y7hpoGL4B7tbEbTNHaMQdEjqzzPp7sbJq-eAqvzSJE0tb-Fr5jPBKs1wCg3KfXS2NpM-eVK8D6PNkMsa4lDIUt0BRIAeevAwFVSDvGbjipydiC3XHjCna3KCZAwgDFBuOYXcRlThJ79dWT5T8lk6zEgRnwz5r2YMR5V8d5crbv7m_oWf3U-IFhAEfoBLanict-Pt0a_9u60S1wtRHXjW4TlGY8rLXeBiHAclFGumMFsFCxf7_qt1Zp3KKAhSXcy8E6kEhVQo6NEsRFdgew=w503-h378-no?authuser=0)

![](https://lh3.googleusercontent.com/KZC0wABVB9o5GuOYdUXggJlACTAKBPb3-6PKkhiKL1I9hxnhR8hqvvGN9WIt06IavVP0TMAVcoe5YILLRqSrXISgItgDLa78nsO_oi-VI1jfC-4kgiUvoFJpeTTweBSYKavnf6YX9NNLSU1gQPGwHJKHpA_r2MAZuGMPoC7pEIsy0DDTXnZ3TsxHU1OTMKk391aCYXRVS3SZ-8ZYMP5l2hsGoaRADRwaFsDqGwR_EAcscHoCqEyQYYDPO7fL3sACZYI_wDVwk_FbQ4movyfaoqZ1aT7vieljtAvC1FXyve6J08uLz5BLSF19GM16OQe_pTBUOBQYt7I-Z717-YFtFNM3H_-7Mub0adS2Zy9kowtgtE0kV4zp1o45G7_U9j2B8TUyMzTV93ndvxqtkWZ5be35d-8dJhzKqE8fK7f3s_tph_5CIO_2GTDf8DVlBDqdDKDs_8EIZ56e75pz8bp6QJ1-08VR7__X9OvcDFz0-l_eZPRcKscLPkmpleWMZck3EvYcRt6iCrvs6LIAUh2K3AHHqQa5PCzEVGEEhdJlK3VcVLqESEZjqs57zXs8AYTl8Cu1iFOHiceCpVNj-zlmaZ3M-inxdwie_dNQw5w1m9UDZRwnztJGcUtdlS4A0QDZtXe1ZB9Rx4ZwwVgiMJmbN4qeMS-gbNAt3VzInIhTK_PW62EbsyAqab7-NQCFvSZBcT0qfqlDZpisQBzQuPifpcRhaw=w565-h422-no?authuser=0)

To have an easier access to the pins of the balancer connector (and to lower the risk of short circuits), I designed some adapter to directly connect the iCharger X12 balancer cable (find the design files in the mentiones [GitLab project](https://gitlab.com/the78mole/igembb-elektronik/-/tree/master/Balancer-Adapter)). By having multiple assembly options for the JST-PH ([S13B-PH-K-S](https://www.digikey.de/de/products/detail/jst-sales-america-inc/S13B-PH-K-S/926637?s=N4IgTCBcDaICwFYEFoCMB2AzABmQOQBEQBdAXyA)(SN)/455-1730-ND/926637) or [S13B-PH-SM4-TB](https://www.digikey.de/de/products/detail/jst-sales-america-inc/S13B-PH-K-S/926637?s=N4IgTCBcDaICwFYEFoCMB2AzABmQOQBEQBdAXyA)(SN)/455-1759-1-ND/926856)) balancing connector, we can adapt to different cables (1:1 = mirrored, cross = straight) to fit the polarities correctly. The following image shows the assembly for a crossed cable. The middle connector is mainly to more easily measure the cell voltages or to find the terminals for the temperature sensors. The pin names are the same as on the ELEC unit (the TH!NK BMS) shown in the nect section.

![](https://lh3.googleusercontent.com/EuS0B3AQ_aJVumPCFmYDAlr13m0P9PXrm68gdLshtkqmdZ9MxRN5ydZvF13pv7qGP8IZghpagyAAs0BJ2clXjspfhphfhZJK2f77kyDZM61ZV9RQkua8NxUCWpR6__jftj2Tp0If33WU8ggr4xLmvl7xNDMeFUy1dTZclYXpf9mFHve7q6cRS0dxhosrk3CXz-m8C5oEtpOfUCqX_5vSwRx3blKw81JYZk8BPYZl2tm3cyUOZ28byQtE4Z5C_7vOGdn_n7skgLBQXdLx_Vtu9N6Z_asQP8_8bbJrxW6-nlG2ed9JuY48EGpT8mxoWq5wi_hrhI93XOEgzu0k8uY3fG_BuLD1frrIXSEY9olR5OWEs7udX-3D4TaxMNiRWzo88MUT1z8F36-x-7YBPS5M5LQXs98Hca-cr5hgT1wPw3QcMTINxqXqodwRlwii0wMDIsSaHP2VSjkloObqqYt_FaFj0K3svmju-MJF_EQYD5FzUZrcTkjQyn9gOVbH8StM20MRY4iZ4sc5lh3EbMeerqEry0e_Tfk_Ut9vJso_cm9H9qS0AbVnWpAP2HPHufW-SzjAF56N3POoMTsG4mybg2fQg_hmhlJxS7T73sSTP31NZJFgt71v19Mfmc8c_zR9s65OuBL5Y2PUfN1UQztXtbwxWYa8bP3Ef36FN7hbUdtDKZxvt7cDoqXHOSQg1muOCi8N-sm05PFIlHxofsXnPXjwCg=w1467-h947-no?authuser=0)

![](https://lh3.googleusercontent.com/9lD2Fpv_ZOWZuRyEiW0iBEy_Ses844iqDa7Xb94BX_kEgt5htdZbG218YjwmKs0J0aL_-hRZHpxDGEBU-5p9OgXFJUZm5xV6JCZBiT_y0t56zRqnqSAqOEOBh50Dkgxc0cbam8gW1YddtL7cAfjVlSxivStz0XQ_GnMnsyyNlq6UU6oaubfl4k4jntYEb9Csq9dmeEPWngoUSMJq_IIZOP-uCFIVZrWYVjg1B2Z5eKQLpgeqLQ6fyW2pHaH1eH6PqdJXfMAFR-WJ-Fx-uEt0czCuoUwPbAVlORFOtGkOWZPhaBfVXHPtkXIs2XXroj6Alb15aK3HO5e8OQ2hSVLwO1sJOeZUmxd0dpJ3McpRSxMnpF5qtB-D1v3897NqAxqzGI39nMlwTxmur91oTowBim-xhLIorVa2It3TxxCXZzFCseY2mD-36y87q7cOcSkE0Bkmlv9WV3AFMXssAFmKVR6CM9fa41WoyPdmlg-yKTJq6k5_1kgW1g21gerEqG_VRr---ARnyZoDLos9e9B49mgSRaN3mCvGEygU_vR9ZXbYiv125mjrk9e4Fqir87IovYH7FFOXzaEnIZ1Zxo1mugAj7cyjCRBAZW0E2HPFB1jkVdb0OueR2kkzWAYWMPLuGvQg5kD9vtFlnyTI_f_gFn-mSbkfjYK1Y5XZl3lhp8T5wWnUKO4VytR_EtA_wva13_aKNK05o1hCLeGM_cd2K4s8Gw=w1431-h947-no?authuser=0)

### Update (2021-05-28) - Assembly Notes

When you assemble the 2X21 horizontal connectors, you should lift it a bit. The battery connector is a bit to thick, to accomplish with the 2X21 attached closely to the PCB. Best would be to solder the connector with attached cable and only fix it by the outer pins (A1, B1, A21, B21). Be careful not to short circuit the balancing pins.Then remove the cable and solder the remaining pins.

The JST-PH-Connector could be to narrow. It fits the Balancing port of the X12 exactly. But many Balancing cables have a XH type on the opposite end. This will not fit my adapter. I will soon optimize the adapter and provide an updated BOM.

## Analysis Results of The Full Battery Stack

### Cautious Charging

During our first, cautious charging attempts with one battery pack (12s2p), we observed the zero-cell (the one that had only a few millivolts in the beginning) loosing voltage during phases without charging, while all other cells kept their voltage tightly. Additionally, after having equal voltages across the pack, the balancer had most work on the 0-cell during charging and the capacity counter showed, that it got much less charge than other cells.

![](https://lh3.googleusercontent.com/NNvQMCQ7yVsA731IfkZ85AJyHQ2If0lTp62yciPgi5LSPm4dYI11U-KHzR5J0mtt0WX6VOqzua6jr6Y-B4RjCEGkIlJkwvrHy33oyusHy5A4EtDCn_M-bDo8WQRRf8GLv2HWQn6_68kOHgrCabERmmBs6jRguJZDbDA_3vLwB29_6EanKWXXKwywmKj9XF5Dg1mrY1F2gUXr5VxuuqWGT-X3sFuMx6YtAx8t4pqVtsYaB8yqUkmdqxr8hQZiRD0CBUMbvSrcCc3dScW7ZDg6l0EE0wtuaqyJBSRMZeWBHgbrs6mPVzlV5CHq0Kr895rXwrBn__5HfsexGK2sOcoFGRF7OCetEZJoCLH7EDJ5CTkH0vMZ8QpwmB_qE_G7DnhWmtzjei7SBytQpV6xrp0QAWbAU2WC1WdkSjDgf5hbfSppUfYwS25vbEnNr1ia8JsNJCjRpzWsr9OgNBV9iHldcXDyQmoEk3pIvRgnQLCXL4EvhtIE9Hw6dlK1P-QiilJDMaTjGz-GWLn_wfR8df5YK3lzM6K8q1D4gStJMwdw0ofWviIh7KhqGuqONBxkR_tLRf4QO1cjHs-BYdnNysOZKAr6ptaLv_od5sf4R6UP26eCR69VwIaJJQ9S3mWTiJkIQrdbwnnkFBt_RB0hLyM-AhE2GkLhPvtXXs_bqCWd90fjN2XaPnfV_1hcBqVvTaFOS34T7fKv50gkgVp3qnmIAPR21g=w980-h735-no?authuser=0)

### Getting to Speed - Cycle all Batteries

TO BE DONE...

### Update (2021-05-28) - Zero-Volt Cells Behaviour

Cell 12 of the Pack #4 is discharging itself down to 0V within a few days. This means, we need to somehow get rid of these 0V-Cells. But first finish the inventory of all Cells...

## The Annoying Thing - The ELEC (TH!NK BMS)

The most annoying thing with the TH!NK is it's BMS. The PCB is coated with some plastics preventing you from measuring the signals, components and even make it hard to replace defect parts. If it would only fulfill it's purpose...: Protection against humidity and water... But it seems, that humidity causes the BMS to blow up and discharge the lowest cell or even more of them over time.

If you look at some of the BMS, you will discover blown parts.

![](/images/blog/2021/05/BMS-Blown-Parts_close-up.png)

A detailed analysis of the circuit uncovers a discretely designed balancer circuit, a microcontroller (NXP), an isolated CAN driver and some isolated power supply powered by 12V rails (not from the battery pack).

![](https://gitlab.com/the78mole/igembb-elektronik/-/wikis/uploads/b4db3b14b1c69a976b04be1094ab5ec0/image.png)

![image](https://gitlab.com/the78mole/igembb-elektronik/-/wikis/uploads/1f7ecbbe63b24960ba92a488cbf9ff1a/image.png)

Not yet finished analysing, but this is what could be revealed up to now from one of the balancing stages:

![image](https://gitlab.com/the78mole/igembb-elektronik/-/wikis/uploads/d8616fe877f29620c669f1252cdf0c0f/image.png)

The circuit reveals, that the magician was some enthusiastic analog designer. You can see a MOSFET, connecting the battery to the resistive load and a level shifting cuircuit that drives the gate relative to it's source but keeping the gate voltage within the allowed limits. Most interesting is the common-base amplifier circuit (Q3), I've not seen for a long time. It's most favorable property it the low current and high voltage amplification, also called a current buffer with voltage amplification.

#### Thoughts about repairing or replacing (same or new) the TH!NK BMS

While a repair is the most economic way to bring the TH!NK back to life, it has some major drawbacks. The most important drawback also applies to a spare part: It has a bug that damages the cells (at least when not used/charged for some time). The other major drawback is the low balancing current and it's passiveness. The large difference of the cells renders the good ones mostly useless, since a passive balancer is always limited to the worst cell in a serial string. This leads to a bad overall capacity, when only a few cells degenerate (worst case one 2p-cell-pair in each string).

Another problem is, that it is hard to find the appropriate semiconductors (transistors, diodes,...). You need to pull some good ones off the board, measure it, characterise it and find a good spare part.

An easier solution is to replace the whole BMS. But these are hard to source and since there exists a lot of documentation for the CAN communications (TH!NK A306 Remote Lithium Energy Controller (RLEC) CAN Programmers Guide), we will give it a try to design an own BMS for the TH!NK. We also will advance it's features by optionally adding active cell and pack balancing to compensate for strong variations of the cells. Most TH!NKs nowadays will encounter it.

With passive Balancing, you will only get the performance of the worst cell-twin in a string (96s2p) and all better cells will used only partly. Assume, a single cell has only 17Ah of health left, while 34Ah are nominal. Even if all other cells in the string have 30Ah, they only can provide 17Ah. This means a loss of 50%@34Ah (43%@30Ah) of capacity, even if the string in total has 88% of capacity left.

## Building our own BMS

Nowadays, you can source integrated circuits for LiPo battery monitors/supervison with balancing and various other features for a tiny amount of money. Together with some isolated CAN transceiver, a tiny microcontroller and some bird food, we will build our onw BMS. So our first iteration will be, to build a passive BMS with the option to upgrade to an active one...

TO BE CONTINUED

# THANK YOU GUYS!!!!

I also want to thank the project team members that did most of the work getting the TH!NK to life again. Since I live in Erlangen, Bavaria, Germany and the TH!NK City is located near Berlin/Brandenburg, Germany the guys living there did most of the time consuming work with the car and it's battery. Special thanks go to Eric (charging and analysing the battery packs), Klaus (for providing an appartment when I was in Berlin to support the team), Steve & Julian (which pulled me into this project and for their great YouTube channel) and all other guys for fertile discussions and ideas (DermitdemTiger, Thomas G. & B., Volker J. & S., Henning, Ronald, Reiner, Matthias, Hans, William)
