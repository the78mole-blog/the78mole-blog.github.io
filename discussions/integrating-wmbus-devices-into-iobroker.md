---
title: "Kommentare: Integrating wmBus devices into iobroker"
category: General
wp_url: https://the78mole.de/integrating-wmbus-devices-into-iobroker/
blog_url: /blog/2019/integrating-wmbus-devices-into-iobroker
content_file: content/blog/2019/integrating-wmbus-devices-into-iobroker.md
total_comments: 4
discussion_id: D_kwDOSNCPls4Al_R7
discussion_number: 16
---

## Kommentare (4)

**Gabriel** – 2020-06-09

> Hi, why would you say the encryption of wmBus has some weaknesses?

↳ **themole** – 2020-06-16

>> Hi Gabriel,
>>
>> here you will find a very detailed analysis on the weaknesses:
>> https://hackinparis.com/data/slides/2014/CyrillBrunschwiler.pdf
>>
>> BUT: The main weakness of wmBus lies not in the specification. It is quite some effort to break the encryption, if possible at all. Many property management companies tend to use unencrypted transfers (I see at least 100 unencrypted water meters around my home from Techem) or use a single encryption key for all of their meters or one for a house to save some effort during installation/configuration. I think, they simply lag an automated process for key deployment :-)
>>
>> Hope this is what you asked for.
>>
>> Regards,
>> Daniel

↳ **Gabriel** – 2020-06-25

>> *Antwort auf **themole**:*
>> > Hi Gabriel,
>> >
>> > here you will find a very detailed analysis on the weaknesses:
>> > …
>>
>>
>> Thanks for your answer. Techem is quite weird because the telegram that they send has a header that specifies the data is not encrypted, but just by looking at the data....it looks encrypted. Do you have some telegram examples from Techem? You can send them to arnautug7@gmail.com.
>>
>> Thanks,
>> Gabriel

---

**themole** – 2020-06-26

> Hi Gabriel,
>
> as I already replied by Email, I can not provide some raw telegrams easily. But when I inspect the data in iobroker, it seems plausible. Some hot water meter shows 21 m³ for the current billing period and heat meters show Wh in a range that makes sense... I guess, your client does simply not interpret the data correctly. My experience is also with some of my own meters, that I could not decode it manually after decryption (when I tried to write some client code), but the wmBus library seems to do a better job here. It extracts even data that never made sense when I looked at the raw values.
>
> Hope that helps a bit.
>
> Regards,
> Daniel

---
