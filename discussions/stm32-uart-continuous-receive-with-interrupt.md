---
title: "Kommentare: STM32 UART Continuous Receive with Interrupt"
category: General
wp_url: https://the78mole.de/stm32-uart-continuous-receive-with-interrupt/
blog_url: /blog/2019/stm32-uart-continuous-receive-with-interrupt
content_file: content/blog/2019/stm32-uart-continuous-receive-with-interrupt.md
total_comments: 1
discussion_id: D_kwDOSNCPls4Al_ST
discussion_number: 20
---

## Kommentare (1)

**themole** – 2020-12-10

> I got some question by Email, asking the following:
> Hey there, doing something similiar now. I will probably switch to LL before it's to late, but I am just interested:
> In USART3_IRQHandler, you say CallMyCodeHere();, but where do you access the received data? Thank you!
>
> Here my answer:
> Since the IRQ was triggered, there will be at least a char and you can  
> simply poll it with HAL_UART_Receive() in your own function.

---
