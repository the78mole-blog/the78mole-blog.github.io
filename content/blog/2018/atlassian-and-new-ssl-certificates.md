---
title: Atlassian And New SSL Certificates
date: '2018-10-20'
description: ''
categories:
- Atlassian
- Bashing
- Bitbucket
- Confluence
- JIRA
- Tools
tags:
- atlassian
- bash
- bitbucket
- CA
- certificates
- confluence
- jira
- linux
- SSL
---

## Or How CAs Drain Your Lifetime

When you check my activity, you simply can see, that the past weeks my time for writing was quite limited. Since I had a few very urgent projects, I had no time to care about my blog. But when it can get no worse, your website provider, that previously relied on the Symantec CA, decides to switch it's root CA to some better and quite new CA that 1. is not listed in some JRA distributions' keystore and 2. uses trust chains with intermediate certificates. And this leads to an ugly situation when you run e.g. some Atlassian tool environment where the tools in turn use SSL to connect to each other. I would have not realized the problem so early, nor it would not have been so urgent, when I would not have decided to do all authentication (Bitbucket and Confluence) through JIRA's Crowd-API.

But let's start from the beginning... My provider, where I get my SSL certificate from (namely the german 1&1) used the Symantec CA for years. This CA somehow attracted Google's anger, so Google decided to remove Symantec from the trusted CAs list of it's chrome browser and announced this around beginning of 2018. 1&1 did not find a reason to get in hurry, so they kept their CA until mid of 2018. Then they started to remind their customers to update their SSL certificates, forcing their customers to hurry a lot. I realized, that there is some neccessity to follow their appeal, but I also felt to still have some time and do it, when the certificate expires...

Then the time came and my Chrome browser refused to show my Atlassian pages. So I logged in to my 1&1 Account and my Linux machine where JIRA & Co. runs, ordered a new SSL certificate, copy-pasted it into my Nginx configururation (which I use as an SSL proxy) and everything went fine at the first glance. I could log in to JIRA without a hassle, did not see any JIRA warnings or hovers and my browser also was not shouting at me about the SSL connection. Everything was fine. But then came the surprise... I tried to log into Confluence (no I currently have no SSO :-( ). I let the browser enter my credentials and... got refused. I tried some more times manually with different combinations of users and passwords, checked my password store, checked CAPS LOCK,... but I did not get in. Since I disabled the "local admin" of Confluence (due to being tight on the 10 user limit), I could also not check from inside Confluence.

What happened? After digging (this is what I often do ;-) ) through the settings, I stumbled over the Application Links section, which stated, that the connection could not be established due to SSL errors. Ah, OK, nice that Atlassian is recommending to install the JIRA SSL Add-on that helps with all that suff. Really all? For sure, not! Especially not with problems I encounter :-( . After digging deeper and deeper, I found, that the new chain of trust, 1&1 uses, is not setup in the JIRA keystore, the atlassian tools ship with their JRE. In contrast Chrome's certificate store is updated tightly.

How to fix? First you need to find the Java keystore to add the CA certificate to be trusted. This is quite a bit difficult, if you do not know about the tool's shipped JRE. So don't hassle around with your distributions keystore, step into the folder where your tools are install (/opt/atlassian/ in my case) and do a

```
find . -type f -name cacerts
```

In my case, the list shows as follows:

```
./jira/jre/lib/security/cacerts./confluence/jre/lib/security/cacerts./bitbucket/5.2.2/jre/lib/security/cacerts
```

I know, Bitbucket 5.2.2 is quite old (and the other tools, too), but keeping it up-to-date is quite hard for a spare-time setup. I believe, with an up-to-date installation, the problem would not have encountered. Let's see, when I update... With this knowledge, it is quite easy (and some manual work) to add your cert to the keystore.

To get the certificate from your server, just do a

```
bash$ openssl s_client -showcerts -servername www.example.com -connect www.example.com:443 </dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > ${HOME}/www.example.com.crt
```

Then you can import that certificate into your Java keystore with the following command set (e.g. for confluence):

```
bash$ cd /opt/atlassian/jira/jrebash$ bin/keytool -delete -alias www.example.com \    -keystore lib/securety/cacerts -storepass changeitbash$ bin/keytool -import -alias www.example.com \    -keystore lib/securety/cacerts -storepass changeit \    -noprompt -file ${HOME}/www.example.com.crt
```

After doing that (I didn't even need a restart of the tools), the application connections resurrect and you can log in to your confluence again.

The more convenient way is to write a little bash script that does the job. You can find mine [here on Github](https://github.com/the78mole/scripts/tree/master/linux/bash). Feel free to improve it and issue some pull request if you think it's worth to be shared.

## Lessons learned

1. Alsways keep a local admin account active in each and every Atlassian tool ;-)
2. Better use an automated SSL framework like [Let's encrypt](https://letsencrypt.org/). With it, you need to make the key rolling-update working from the beginning, not when it is too late (OK, this would not have helped me in my situation, nevertheless it is a good idea to do so)
3. Document your problem solutions (which I do with scripts and this blog :-) )
4. Don't document the tool in the tool (e.g. this howto in Confluence), you will shoot both your feet :-)
5. Keep your tools up to date!

---

## Kommentare / Comments

Hast du Fragen oder Anmerkungen zu diesem Artikel? [Erstelle ein GitHub Issue](https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new?title=Kommentar+zu%3A+atlassian-and-new-ssl-certificates&labels=comment) oder starte eine [Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).
