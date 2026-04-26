---
title: STM32 UART Continuous Receive with Interrupt
date: '2019-09-06'
description: ''
categories:
- ARM
- STM32
- USART
tags:
- HAL
- STM32
- UART
---

My last post is quite some time ago, due to vacations and high workload. But now I encountered some problem within an embedded project, I want to share the solution with you. Continuously receive data using interrupts on UART is complicated (or even impossible) in HAL. Most approaches I found crawling the internet are using the LL library to achieve this and many discussions around HAL do not end in satisfaction. Some work around the problems with dirty approaches (e.g. changing the HAL code itself), other step back from interrupt and use a polling approach.

To be honest, the high levels of HAL do not offer such a solution. Instead, it offers functions to receive a special amount of data using a non-blocking interrupt approach, handling all the difficulties with tracking the state in the instance stucture (huartX) and entering a callback for the diverse states of the reception/transmission, e.g.   
`void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)` or  
`void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart)`

### Using HAL\_UART\_Receive\_IT (not recommended)

A nearby approach without touching HAL code itself is, to call `HAL_UART_Receive_IT(&huart3, &rxbuf, 1)` once after initalization and at the end of the RxCpltCallback, to retrigger the reception, but this leads to some undesired lock (possibly a HAL-Bug), when transmitting data using `HAL_StatusTypeDef HAL_UART_Transmit_IT(UART_HandleTypeDef *huart, uint8_t *pData, uint16_t Size)`, which could also not be the desired behaviour and the beginning of endless debug sessions and frustration.

### Simply Enable the IRQ

The best solution in my opinion instead is really simple. Don't use the high level receive functions at all for the continuous RX behaviour, since you do not want to receive a special amount of data but be called at each reception. So, configure the UART with interrupt in CubeMX and after it's initalization, enable the interrupt itself, never calling the HAL\_UART\_Receive\_IT or any other UART receive function (it will disable the IT after finishing).

In the section of the appropriate instance in `void HAL_UART_MspInit(UART_HandleTypeDef* uartHandle)`, add the following line of code:

`__HAL_UART_ENABLE_IT(&huartX, UART_IT_RXNE);`

In stm32xxx\_it.c do:

```
void USART3_IRQHandler(void)  {    
    /* USER CODE BEGIN USART3_IRQn 0 */
    CallMyCodeHere();
    return;  // To avoid calling the handler at all 
             // (in case you want to save the time)
    /* USER CODE END USART3_IRQn 0 */
    HAL_UART_IRQHandler(&huart3);
    /* USER CODE BEGIN USART3_IRQn 1 */
    /* USER CODE END USART3_IRQn 1 */ 
}
```

The return statement will avoid calling the HAL IRQ handler. I did not try during transmit, but it seems not disturbing anything. If you plan to use the HAL\_UART\_Receive\_IT functions in parallel, you could try to put your code below the handler. I did not test it, but there is a good chance that it works.

Since this approach only touches the user code functions, none of your code will be destroyed by code re-generation of CubeMX.

This is all you need... Happy UART processing ;-)

### If Timestamping is Needed

#### Simple Millisecond Timestamps

If you want to trigger on inactive time durations (some serial protocols use it as a synchronisation condition), save a timestamp (e.g. `HAL_GetTick()`) within the UART-RX-Interrupt and look at the difference to the previous one (subtract the duration of a byte to get the real inactive time).

#### High Resolution Timestamps

If sub-milli-second resolution is required, run a timer with a prescaler of desired resolution and take the counter value of the timer instead of the tick counter. (you can get it with `__HAL_TIM_GET_COUNTER(&htimX)`).

Hope this helps in your next project using UART :-)

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+stm32-uart-continuous-receive-with-interrupt&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
