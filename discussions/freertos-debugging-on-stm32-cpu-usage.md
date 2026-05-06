---
title: "Kommentare: FreeRTOS debugging on STM32 - CPU usage"
category: General
wp_url: https://the78mole.de/freertos-debugging-on-stm32-cpu-usage/
blog_url: /blog/2020/freertos-debugging-on-stm32-cpu-usage
content_file: content/blog/2020/freertos-debugging-on-stm32-cpu-usage.md
total_comments: 2
discussion_id: D_kwDOSNCPls4Al_Ro
discussion_number: 13
---

## Kommentare (2)

**Marc Lindahl** – 2020-07-28

> One detail I would like to point out.  For the interrupt, it is more in line with the way the STM libraries work to replace the weak function HAL_TIM_PeriodElapsedCallback() with one in main.c and put your timer code in there.  Usually there is one already when using FreeRTOS, to avoid conflict with FreeRTOS using sysTick. For example:
>
> /**
>  * @brief  Period elapsed callback in non blocking mode
>  * @note   This function is called  when TIM6 interrupt took place, inside
>  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
>  * a global variable "uwTick" used as application time base.
>  * @param  htim : TIM handle
>  * @retval None
>  */
> void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
> {
>  /* USER CODE BEGIN Callback 0 */
>
>  /* USER CODE END Callback 0 */
>  if (htim-&gt;Instance == TIM6) {
>    HAL_IncTick();
>  }
>  /* USER CODE BEGIN Callback 1 */
>
>  /* USER CODE END Callback 1 */
> }
>
> So you would just add another test for instance TIM13 in your example and update your variable in HAL_TIM_PeriodElapsedCallback(). Thus only main.c need to be edited.  I hope this makes sense and is useful.   Again, than you so much for your post!

↳ **themole** – 2020-09-06

>> Hi Marc,
>>
>> sorry for my late reply and the dealy in accepting your comment. It depends on the project settings in CubeMX, where the weak function gets replaced. In my generated code, it is in ..._it.c. But you are completely right, if you put in in main.c, the extarnal statement would not be necessary. In my opinion, both is quite clean.
>>
>> Regrads,
>> Daniel

---
