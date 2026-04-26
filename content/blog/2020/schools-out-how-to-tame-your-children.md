---
title: School's out - How to Tame Your Children
date: '2020-04-03'
description: ''
categories:
- Corona Virus
- Linux
tags:
- corona
- covid-19
- digital classroom
- pandemic
- pandemie
- sars-cov-2
- school
- virus
---

## Introduction - Historic Reasons for this Post

Here in Germany, executive decided to lock all public life down to a minimum (only system relevant shops are allowed to be opened and for each state in germany , there are different exceptions) and it seems, that all countries do the same. This means, many people need to work in their home office and if you have kids, they "join you at work". And as if that's not enough, they refuse to learn anything for school. Parents are simply not made to guide their kids through school stuff.

After some days of lock down the teacher of my daughter sent around a voicemail, telling the kids she misses all of them and they should do some tasks at least until easter holidays (from 2020-04-04 to 2020-04-19) start. I was completely excited, how my little girl changed. She stopped every activity and listened to the teacher as she would never listen to me, telling her the tasks she needs to do. But as soon as it came, the magic was over...

Welp, what can I do as an engineer to help myself and my girl out of this...? Right! Help the school to raise a digital classroom. Technically no problem, but in germany, most problems are not technical. Most problems arise due to privacy protection and simply the reluctance of official employees to deal with the work. But this shall not be the topic of this post. The solution is, to be very bullheaded and try to explain the situation based on sience. ([Corona is just now starting](https://youtu.be/3z0gnXgK8Do), german video).

Short side notice: In Bavaria we have a system called Mebis that was intended to complement the daily school with digital information and courses. Teachers even can collect tasks and share courses. Unfortunately, there are no means of communication for whole classes or at least a simple video and/or audio distribution. The highest level of group communication is a chat for 6 persons at max. So, the system needs to be steered by the parents for the little ones (grade one to four).

This means, that all information for our children was distributed by Email or some WhatsApp group (inofficially, because of the privacy laws). Lately, the teacher also has setup a class in Anton-App. But even this is not a good solution for the little ones...

## Then, WHAT Would be the Solution?

So, what would you do as a technician, if you expect this lockdown to continue after the easter holidays (as it is a logical conclusion from the above video)? Right! Evaluate what exists out there and find a solution that fulfills the requirements for the low grade scholars:

- Audio/Video communication (virtual class room)
- Distribution and collection of task sheets/images (not digital courses, little ones can not operate the keyboard efficiently)
- Easy to setup courses
- Complies with GDPR (DSGVO) --> Runs on own server or in a german cloud
- Easy to use
- Cheap or free to use

## TL;DR

![](/images/blog/2020/04/512px-Moodle-logo.svg_.png) I quickly found a digital classroom soultion that fulfills the requirements: [Moodle](https://moodle.org/?lang=de) (BTW: there is also [moodlecloud](https://moodlecloud.com/), but this does not comply with GDPR). I decided to run it on my home server (HP Proliant Gen 7 + 100M DSL). So the architecture is quite simple: Reverse Proxy VM as exposed host and Moodle VM connected to internal proxy net (10.0.0.0/16).

My proxy it using Nginx in a very minimal configuration and Moodle is protected and accessed through the proxy from the outside world. The proxy net is also only connected to the services that shall connect to the public internet.

The installation of Moodle is straight forward and following the [how-to](https://docs.moodle.org/38/en/Installing_Moodle) ([German how-to](https://docs.moodle.org/38/de/Installation_von_Moodle)) leads to the the expected results. As database I used MariaDB and Nginx as the webserver.

Beside MariaDB and Nginx, you need to install php-fpm. Which additional php modules you will need is perfectly evaluated during moodle web setup and you should simply keep a console open to run `sudo apt install <required-module>`.

If you want to run all this through a reverse proxy, don't delay its configuration to a point in time after the moodle web setup. The setup will determine the url it was accessed and you will need to change this somewhere in the config afterwards...

One of the problems was, to get Moodle running smoothly through the reverse proxy. It had some minor problems to resolve the CSS, JS and all PHP indirectly served files. Here is my proxy configuration to make it work (I assume you already did your SSL config and certificates correctly, hint: wildcard certificates for your domain make everything much easier).

#### Nginx proxy config (for reverse proxying the Moodle host)

```
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;
  server_name moodle.<mydomain>;
  include snippets/my_ssl.conf; 
  include snippets/ssl-params.conf; 
  root /var/www/html/; 
  location / { 
    proxy_set_header X-Forwarded-Host $host:$server_port; 
    proxy_set_header X-Forwarded-Server $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
    proxy_pass http://10.0.2.20:80; 
    client_max_body_size 100M;
    proxy_set_header Host $host; 
  }
}
```

#### Nginx conf on Moodle host

```
server {
  listen 80 default_server;
  listen [::]:80 default_server; 
  root /var/www/html; 
  index index.html index.htm index.nginx-debian.html index.php;
  server_name _; 
  location / { 
    try_files $uri $uri/ =404; 
  }
  location ~ \.php/.*$ { 
    include snippets/fastcgi-php.conf;
    fastcgi_pass unix:/var/run/php/php7.3-fpm.sock; 
  } 
  location ~ \.php$ { 
    include snippets/fastcgi-php.conf; 
    fastcgi_pass unix:/var/run/php/php7.3-fpm.sock; 
  }
}
```

You only need to unzip a Moodle distro package to /var/www/html and as soon as you point to https://moodle.<your-domain>, it will show up the setup process. Now follow the guide and install the packages Moodle needs.

If you keep everything at the default values, it will only be possible to upload files up to 2M in size. This is not sufficient, if you expect parents to upload photos of the completed task sheets and also sometimes too less for PDFs or images you want to share. Therefore, you need to raise the limit for Nginx and php-fpm. This is done on Debian 10 buster in:

- /etc/php/7.3/fpm/php.ini
  - upload\_max\_filesize = 50M
  - post\_max\_size
- /etc/nginx/nginx.conf (section http)
  - client\_max\_body\_size 50M;

On the proxy, this is already included in above config.

## Lessons Learned

Some of the dependencies, moodle and it's plugins have are not hard during installation, but they will show up when you use moodle for a while. If you just don't want to know, why these dependencies are needed, you simply need to do (as root or with sudo)

```
apt install unoconv ghostscript graphviz 
```

A bug in the onuconv release 0.7 (which is deployed by debian 10) prevent the unoconv to create it's own listener and to create some tempfiles. To circumvent this, we simply create a little wrapper script:

```
vi /usr/bin/unoconv_wrapper.sh
```

Put in the following content:

```
#!/bin/bash
HOME=/tmp /usr/bin/unoconv $@
```

And make it executable.

```
chmod 0755 /usr/bin/unoconv_wrapper.sh
```

Now enable unoconv and adjust the path settings in the moodle unoconv configuration to point to the wrapper `/usr/bin/unoconv_wrapper.sh`

![](/images/blog/2020/04/image-9-1024x135.png)

![](/images/blog/2020/04/image-8.png)

And afterwards, enable the unoconv document converter in website administration (search for unoconv to get the settings).

If you want to use the PDF annotation for all supported file formatts, you need to celect it in Feedback-Types of the Activity

![](/images/blog/2020/04/image-11.png)

You can also select it in the default settings, so you don't need to change it for every activity you add to a course. Unoconv then converts different types of files to PDF, and as a trainer, you can simply annotate these PDFs online. If you don't use unoconv, you need to download e.g. each and every image or other document to your PC and send back your comments in a different way to the student/scholar. Also as a file upload or as a textual comment.

## Happy teaching

As soon as your nginx runs, you possibly wish to use your Moodle. One of the first things I did is installing the BigBlueButton-addon for video conferencing. Blindsidenetworks is thankfully providing a free conferencing server for moodle. This means, that all the audio and video traffic is not flooding your server (this is, why I can run it at home). If you wish to use an own on-premise solution, I would give [OpenMeetings](https://moodle.org/plugins/mod_openmeetings) a try.

## Conclusion

The setup of Moodle is quite simple, even if there are little pitfalls with reverse proxy configuration. It also needs some time to get up and running, using the system. But creating simple courses and putting in some PDF files is really dead easy. The higher levels are to concentrate the results (trainer task) and to add little extra candy (e.g. Badges) to motivate children to learn.

All this said, I wish you happy teaching and I would be happy to receive comments on it.

Here a little hint, how a course could look like with content (Tasks in PDFs and a place to put the pictures of the task sheet in).

![](/images/blog/2020/04/image-1.png)

## Update

### KW 17 - Three weeks after introducing Moodle

After three weeks and a (partly) official video conference using BigBlueButton (see my other [post about installing BBB](https://blog.the78mole.de/installing-bigbluebutton-on-your-dedicated-server/)), More and more children tend to register for this platform. And it seems to be the only available platform, where all that stuff is organized well, corrections can be easily done and even rating is possible. Additionally, with the moodle android and iOS app, the camera can be easily used to commit the scholars/students work within seconds. No scanning, not transportation of finished tasks,...

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+schools-out-how-to-tame-your-children&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
