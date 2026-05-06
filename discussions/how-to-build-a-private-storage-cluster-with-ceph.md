---
title: "Kommentare: How to Build A Private Storage Cluster (with Ceph)"
category: General
wp_url: https://the78mole.de/how-to-build-a-private-storage-cluster-with-ceph/
blog_url: /blog/2019/how-to-build-a-private-storage-cluster-with-ceph
content_file: content/blog/2019/how-to-build-a-private-storage-cluster-with-ceph.md
total_comments: 2
discussion_id: D_kwDOSNCPls4Al_R6
discussion_number: 15
---

## Kommentare (2)

**Oli** – 2021-01-22

> Hi,
>
> interesting blog post. I'm also trying to get CEPH octopus working on the ODROID HC2. I tried different options, compiling, which is really painful. But then I noticed that there is a very up to date version of ceph 15.2.7 available for armbian focal. However I didn't succeed in configuring the HC2 as an OSD node. I asked for help on the ceph mailinglist and also on ubuntu launchpad as it seems to be an issue with the package. Until now no solution. :( If you want to give this a try yourself...

↳ **themole** – 2021-01-23

>> Hi Oli,
>>
>> when I was trying to get Ceph running on ARM32, there have been pack packages of Ceph, but for some quite old version. I tend to believe, going for 64 bit is the right choice to get a somehow up-to-date version of ceph in the future. This also has to to with the 32 bit memory limit of 3 GB for a single process. The recommandation is, to have 1 GB of RAM for every TB of disk available.
>> I'm currently designing some Raspberry Pi CM4 based solution, similar to the ODROID HC1/2. I'm yet not sure, when I will finish this, but staying tuned to my blog and you will be one of the first to know :-)
>>
>> Regards,
>> Daniel

---
