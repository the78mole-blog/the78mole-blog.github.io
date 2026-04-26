---
title: How To Debug Hardware-Faults on Your Dedicated Server
date: '2020-04-19'
description: ''
categories:
- Linux
- Server
tags:
- Debugging
- Dedicated Server
- Serial Console
---

While installing some stuff on a dedicated server at Strato, I encountered a problem with the server two times. While having no clue what happened during the first time, I was prepared during the second. I kept a connection to the serial port proxy of my provider open, to see the most low level messages (kprints).

And you won't believe, after 13295 seconds of uptime (3 hours 41 minutes), the kernel had a panic:

![](/images/blog/2020/04/Hardware_Error_Dedicated_Server-1024x657.png)

This is a great indication to run a Hardware-Test and to address the support of your hosting provider.

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+how-to-debug-hardware-faults-on-your-dedicated-server&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
