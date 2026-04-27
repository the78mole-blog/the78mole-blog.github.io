---
title: Merging the Contents of Two InfluxDBs
date: '2019-09-25'
description: ''
categories:
- Linux
- Smart Home
tags:
- database
- influxdb
- iobroker
- migration
---

Eveer had the problem that data runs into two different [influx databases](https://www.influxdata.com/) and you want to merge the data into a single one? You wonder, why this can happen? Then just think about migrating some data aquisition project from one server to another without a downtime by spooling the aquired data into both DBs for some time or simply setting up a fresh system after the old one is dying slowly because of low performance. This happened to me with my smart home system, running iobroker and some influxdb on it. The old one ran on a ODROID-HC1 with only 2GB RAM. The new one is a Debian 10.0 VM on my brand new HP Proliant running XCP-NG. (OK, it's not new, it's used HW, but for private use, it is a monster :-) )

For sure, there exist great tools from the influx inventor, but this is way to much for a small project to set up. So I decided to go the easy way of first doing the absolutely necessary (bring up the new system) and later pull in the historical data.

Backing up and restoring iobroker is well documented and works smooth and will not be part of this post. For influx, I just setup a new instance with a copy of the /etc/influx.conf and started the service. Then I started iobroker and everything worked like before, except the availability of the historical data.

After endless searching throughout the web and many tries to export the DB as CSV, JSON,..., I found a [set of scripts from ETZ](https://influxdb.phys.ethz.ch/backup_restore.html), that helpt me half the way up and down the backup-restore-process.

The key to success in the end was, to restore the DB on the new server not as the original one, but to rename it. In my case, I called the new historical DB on the new server iobroker\_old.

Now I had all the data I want to import at least on the new instance, but how could iobroker find it? It won't! I needed to do some internal import within influxdb to migrate the `iobroker_old` into the `iobroker` database.

To export the DB from the old system, just issue (on the old system):

```
$ backup-influxdb
$ scp /var/backups/influxdb/2019.... <myuser>@<newserver>:~
```

On the new server, then do:

```
$ restore-influxdb-database-online \
    ~/2019... \
    iobroker iobroker_old
```

The command to my success was (with help from [GIST](https://gist.github.com/pootzko/e46fe2e0e6e12a6b0dddbb2ed12b15cd), before you run the command, doing a snapshot of the system may be a good advise):

```
$ influx -database iobroker_old -execute \
   'SELECT * INTO "iobroker"."global".:MEASUREMENT FROM "iobroker_old"."global"./.*/ GROUP BY *'
```

To make this succeed, I needed to raise the physical RAM of the VM to 16 GB. With 4 GB it simply swallowed the swap and ran into some timeout. Afterwards, I turned it back to 4 GB and everything runs fine.
