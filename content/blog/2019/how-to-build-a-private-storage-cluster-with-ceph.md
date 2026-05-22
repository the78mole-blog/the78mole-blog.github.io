---
title: How to Build A Private Storage Cluster (with Ceph)
date: '2019-01-07'
description: ''
categories:
- ARM
- Ceph
- Storage
tags:
- ceph
- cluster
- storage
- diy
- odroid
- arm
- linux
- distributed-storage
---

Finally, I did not succeed in getting Ceph running on a 32 bit ARM. There have been to many issues in the code (especially incompatible datatypes) and issues with GCC and the 3 GB RAM limit for 32 bit platforms. I'm now focusing on using a 64 bit ARM and developing a dedicated HW for it. So, stay tuned...

Since my NAS (a QNAP TS-419P II) get more and more buggy, especially with non-working Windows shares and the painfully low processing power of the integrated ARM single core, wished something like a SAN for myself. But SAN is quite expensive, the peripherial hardware (Switches, UPS,...) not included. So I decided to skip a few levels and build up a NAS 2.0 storage cluster based on open source ceph using low-budget [ODROID HC2](https://web.archive.org/web/20191202144520/https://www.hardkernel.com/shop/odroid-hc2-home-cloud-two/) (Octa-Core 4 x Cortex-A15 + 4 x Cortex-A7) from [Hardkernel](https://www.hardkernel.com/) as the work horse to create storage nodes. To make it even more dense, you can use the [ODROID HC1](https://web.archive.org/web/20251113103351/https://www.hardkernel.com/shop/odroid-hc1-home-cloud-one/) that is just the same but for 2.5" disks (be aware of the power supply: HC2 = 12V, HC1 = 5V !!!).

If you don't need a SATA drive (e.g. for the controlling nodes of the cluster: mgr, metadata, nfs, cifs,...), you can use the MC1, MC1 solo, XU4 or XU4Q.

If you want to go with x86 instead of ARM, the [ODROID H2](https://www.hardkernel.com/shop/odroid-h2/) looks like a great alternative, but it will also be a bit more expensive (e.g. RAM is not included).

In fact, installing ceph will be much less pain, going for 64-bit x86 than going with ARM 32 bit. I decided to go with ARM 32, because I want to build up the most energy efficient cluster, to maximize scale out capabilities also in sense of my private budget.

To build up the cluster, I currently use 4 x ODRID HC2 with WD Red 4 TB drives (WD40EFRX), also installing the ceph non-OSD-services distributed accross this little cluster. The BOM for my test cluster is as follows:

- 4 x ODROID HC2
- 4 x WD40EFRX (4 TB WD Red 3,5" HDD)
- 4 x [16 GB MicroSD-card](https://web.archive.org/web/20251115155419/https://www.hardkernel.com/shop/16gb-microsd-uhs-1-xu4-linux/) (Linux preinstalled)
- 4 x [DC Plug Cable](https://www.hardkernel.com/shop/dc-plug-cable-assembly-5-5mm-l-type/)
- 1 x [12V/8,5A Power Supply](https://www.reichelt.de/schaltnetzteil-geschlossen-100-w-12-v-8-5-a-mw-lrs-100-12-p202974.html?)

If powering up the cluster in sequence (not all at once), you could reduce the power requirements of the supply component a lot (currently 12V/2A per node, 5V/4A for HC1). I will dive into this topic a bit deeper in future. I think, it can be done in software by delaying the spin up through some bootarg. Nevertheless, an optimum solution would be to have a power distribution unit for switching and measuring the supply current and also providing some UPS capabilities on the low voltage path. Additionally, current measuments could give you the ability to regulate the power through e.g. cpufreq to optimize the efficiency of the cluster and the power supply.

To generate the debian packages for installing ceph on the nodes, follow the instructions [here](https://blog.the78mole.de/compile-ceph-mimic-on-arm-32-bit/). When you have built the debian packages, move them over to some http(s) server, to be easily accessible by your nodes.

### Your Own Debian Package Repository

To be accessible, a Debian Package Repository needs to be placed in a webserver's directory accessible at least in your own network. It is best practice to secure this repository with SSL, since Debian APT more or less expects this... So first we start with creating a (self signed CA). Later, if needed, you can easily replace the certifciate by an official one or let an authorithy also sign your server certificate.

#### Generating a CA for SSL

This part is based on the tutorial [here](https://gist.github.com/Soarez/9688998). First, we will simply use self signed certificates, since it is much easier and faster than using officially signed certificates. We will then place the CA in the cert storage of our linux OS, to make it trust ourself. ;-)

```
mkdir ~/CAcd ~/CA# Generate the CA keyopenssl genrsa -out ca.key 4096# Generate the CA certificate, here, you can leave the CN emptyopenssl req -new -x509 -key ca.key -days 366 -out ca.crt# Make it unaccessible by other userschmod 700 ca.key# Generate a certificate configurationwget https://raw.githubusercontent.com/the78mole/scripts/master/templates/configs/ssl/cert.conf -O example.org.conf# Edit the configurationvi example.org.conf# Create a server certificate key and the signing request (not the yet cert)openssl req -new -out example.org.csr -config example.org.conf# Create the public keyopenssl rsa -in example.org.key -pubout -out example.org.pubkey# Sign the CSR with your CA and create the certificateopenssl x509 -req -in example.org.csr -CA ca.crt -CAkey ca.key -CAcreateserial -extensions my_extensions -extfile example.org.conf -days 366 -out example.org.crt
```

To get the alternative DNS names and IPs added to the certificate, you need to specify the config file as an extensions and point to the config section, where the extensions are located. This is because the extensions in the CSR get ignored by openssl when signing and you need to specify it explicitly.

After generating the certificate, you need to import it, where you need it to be accepted (Browser, APT). For testing, it is best to try with a browser. Some tutorial can be found [here](https://thomas-leister.de/ca-zertifikat-importieren-linux-windows/) (it's german, so use google translator, to read in english) and [here](https://manuals.gfi.com/en/kerio/connect/content/server-configuration/ssl-certificates/adding-trusted-root-certificates-to-the-server-1605.html). Use the shell of your desktop Debian system.

```
scp <CA_HOST>:/<PATH_TO_CA>/ca.crt example_ca.pemsudo cp example_ca.pem /usr/local/share/ca-certificates/sudo update-ca-certificates
```

To add the certificate to your browser, e.g. chromium

```
sudo apt install libnss3-toolscertutil -A -n "Example Company CA" -t "TCu,Cu,Tu" -i example_ca.pem -d ~/.pki/nssdb
```

Note: Maybe this does not work correctly... Then, in Chromium, use Settings --> Privacy and Security --> Manage Certificates --> Import --> Select the CA --> Check all boxes.

Now we need the CA's and the server's certificate along with the server key for securing webserver traffic.

#### Install and Configure the Webserver

Welp, we will use nginx as our webserver. Feel free to use any other, it does not really matter. In fact, every further step (e.g. the let's encrypt tutorial) will be based on nginx.

```
sudo apt install nginxcd /etc/nginxcp snippets/snakeoil.conf snippets/ssl_example.org.confmkdir -p ssl/pubmkdir -p ssl/privsudo chown -R root:www-data sslsudo chmod -R 0755 ssl/pubsudo chmod -R 0750 ssl/privcp ~/CA/ca.crt ~/CA/example.org.crt cp ~/CA/example.org.key# Edit the ssl config file to your needsvi snippets/ssl_example.org.conf# Now adjust the nginx configuration to use SSLvi sites-enabled/default# Ensure following lines are added and not commented out# listen 443 ssl default_server# listen [::]:443 ssl default_server# include snippets/ssl_example.org.confservice nginx restart
```

When everything is OK, use your desktop web browser and point it to the location https://example.org. Your should get the page without an error. Thos means, you have setup a CA you can use to sign server certificates and they get trusted.

If you plan to use the Debian package repository on many of your linux hosts, then you should add your CA certificate to the certificate store on all the machines.

#### Generating GnuPG Key-Pair

To sign a file, email, hash, debian package, repository,... you often need GnuPG. To be able to sign something, you need to first generate your own key, that get trusted from at least the receiving party. All this works again with asymmetric encraption, like the signing of certificates does. An in depth tutorial with links to even deeper knowledge can be found [here](https://wiki.debian.org/DebianRepository/SetupWithReprepro).

First we should install a tool to gather some entropy, otherwise gnupg may be not able to generate a key on a headless system (no real user input,... --> very few entropy sources).

```
apt install rng-tools
```

IF it can not find a hw-rng, you can still try to get randomsound working (if you have a soundcard...)

```
apt install randomsound
```

Run this in a seperate window, when gpg is collecting entropy for too long. It will abort after some time, if it can not generate the key.

```
arecord -l # Do you have any soundcard?randomsound -v
```

If all fails, you can still pipe some data into /dev/random to feed the entropy pool, e.g. with (also in a seperate window when gpg gen-key is running.

```
sudo dd if=/dev/sda of=/dev/random status=progress
```

You can watch the entropy-pool with:

```
watch -n 0.5 cat /proc/sys/kernel/random/entropy_avail
```

To finally generate a GPG-key, simply follow the instructions below:

```
apt install gnupg# Create the .gnupg directory easily and add a secure configurationgpg --list-keys --fingerprintwget https://raw.githubusercontent.com/the78mole/scripts/master/templates/configs/gnupg/gpg.conf -O ~/.gnupg/gpg.confgpg --full-gen-key# Select: #   Key type  : RSA and RSA#   Keysize   : 4096#   Expiration: 1y# Then enter your name and email, but don't include a comment# Skipping the password makes CI much easier, but less secure...# It will take some time (maybe minutes) to generate the key
```

#### Creating the debian repository (reprepro)

make-debs already created a debian repository, but we will create one, that is more general, also serving well for other software packages. make-deps

.... to be continued ...

**Coming soon**: To add some real NAS features, we could use just another embedded board with e.g. FreeNAS or NextCloud installed to mount the cluster file system and using the cluster as the storage backend. We already have the nginx SSL configured, so we easily can add reverse proxy targets... (for HTTPS-HTTPS-proxy, see [here](https://reinout.vanrees.org/weblog/2017/05/02/https-behind-proxy.html))
