---
title: STM32 FreeRTOS and printf
date: '2020-06-03'
description: ''
categories:
- ARM
- FreeRTOS
- STM32
- Uncategorized
tags: []
---

After some more coding, I found some more issues with FreeRTOS and printf, not being solved by my fix below. If you need to get it fixed completely, look at that forums post: [ST Community](https://community.st.com/s/question/0D50X0000BB1eL7SQJ/bug-cubemx-freertos-projects-corrupt-memory)  
and the website of Dave Nadler: [newlib and FreeRTOS](http://www.nadler.com/embedded/newlibAndFreeRTOS.html)  
In my current project, I replaced the newlib-nano-printf implementation by adding [github:mpaland/printf](https://github.com/mpaland/printf) as a git submodule to my project and including the printf.h (it overwrites the printf-library function with macro defines) in my topmost header file.

This will be a very short post. If you experience hard faults when using printf (this happens mostly, when using floats) and you already ticked the appropriate settings in the project's properties...

![](/images/blog/2020/06/image-5.png)

...don't waste your time digging through assembler instructions with instruction stepping (like I did) just to realize, that memory management is broken when using FreeRTOS. It is simply a bug in CubeMX-generated source files. Locate your \_sbrk-function (either in syscalls.c or in sysmem.c) and change it to the following:

```
caddr_t _sbrk(int incr)
{
  extern char end asm("end");
  static char *heap_end;
  char *prev_heap_end,*min_stack_ptr;
  if (heap_end == 0) 
    heap_end = &end; prev_heap_end = heap_end; 
  /* Use the NVIC offset register to locate the main stack pointer. */
  /* Locate the STACK bottom address */
  min_stack_ptr = (char*)(*(unsigned int *)*(unsigned int *)0xE000ED08);
  min_stack_ptr -= MAX_STACK_SIZE; 
  if (heap_end + incr > min_stack_ptr) {
    errno = ENOMEM;
    return (caddr_t) -1;
  }
  heap_end += incr; 
  return (caddr_t) prev_heap_end;
}
```

For what \_sbrk does, have a look [here](https://en.wikipedia.org/wiki/Sbrk).

If you want to digg a bit deeper, here are some websites dealing with this problem:

- <https://www.openstm32.org/forumthread353#threadId354>
- <https://www.openstm32.org/forumthread7695>
- <https://bitbucket.org/arminoonk/printf-float-issue/src/master/>
- <https://community.st.com/s/question/0D50X00009XkW7j/hardfault-from-printf>
- <https://community.st.com/s/question/0D50X00009sUA8S/why-is-printf-not-working-with-floating-point-on-the-stm32f407vg-iar-8301>
- <http://www.nadler.com/embedded/newlibAndFreeRTOS.html>

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+stm32-freertos-and-printf-with-floats&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
