---
title: "Kommentare: STM32CubeMX and SDRAM"
category: General
wp_url: https://the78mole.de/stm32cubemx-and-sdram/
blog_url: /blog/2020/stm32cubemx-and-sdram
content_file: content/blog/2020/stm32cubemx-and-sdram.md
total_comments: 2
discussion_id: D_kwDOSNCPls4Al_SU
discussion_number: 21
---

## Kommentare (2)

**Tim Howe** – 2021-01-05

> Thanks for this.
> The BSP for the STM32F429-DISCO board has a BSP_SDRAM_Init function that does this last part of the setup. Unfortunately the recent CubeMX tools generate code that works on the newer STM32F429I-DISC1 board but not the old STM32F429I-DISCO.
> I have spent a day and still dont know why the older board does not work!!! :o)

↳ **themole** – 2021-01-05

>> Hi Tim,
>> thanks for your comment.
>> You are totally right! I had the same experience than you. For the boards that got some HW update, CubeMX does not generate working code in some cases. I'm not sure, why they do not provide the ability to select the correct board in CubeMX. At least, they could raise a warning, when selecting one of those boards. But since we both now know the problem, we can cope with it ;-)
>> Regards,
>> Daniel

---
