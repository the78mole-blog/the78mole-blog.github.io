---
title: Compiling Software on RAM-limited Multi-Core Systems
date: '2019-01-03'
description: ''
categories:
- Uncategorized
- Dev
- Tools
tags:
- compilation
- build
- arm
- embedded
- linux
- optimization
---

Since I often compile stuff on embedded ARM targets that are well equipped with processing power (Exinos Octa-Core), but are neglected regarding RAM (2G), I often facing the trade-off between running multiple or only a single/few compilation jobs (make -j8 vs. make -j1). If you start too many jobs and if you have large compilation units (e.g. with the [Ceph Project](https://www.github.com/ceph/ceph) sources), the system will feel like jam, as soon as it begins swapping.

I feel, that deciding the job count at the very beginning is (was) a trade-off, I was not willing to accept. Therefore, I decided to write a little script to suspend compile processes, that cross a certain memory limit. This way, the suspended processes get moved to swap and the still runnig processes get a comfortable amount of RAM. This way, the kernel is not forced to move pages around with every scheduling round. Instead, it will move it once on swap for suspended processes, when it needs RAM for the running ones and as soon as the processes with large memory footprint finish, the supended ones get back to live.

Welp, I decided to base the priority on the time the processes ate up user space processing time, so the older ones (often the most memory hungy ones) get processed first. This scheduling scheme proofed to be a optimal descision, that is also not hard to implement as a bash script.

[Here](https://github.com/the78mole/scripts/blob/master/linux/bash/schedule_compile.sh) you can find the little script, that needs to be run within a loop or simply with the watch-tool (maybe with sudo).

```
watch scripts/linux/bash/schedule_compile.sh
```

Happy compiling!
