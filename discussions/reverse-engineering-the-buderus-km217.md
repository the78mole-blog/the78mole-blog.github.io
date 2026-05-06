---
title: "Kommentare: Reverse Engineering the Buderus KM271 - And Making It WiFi-Flying on ESPhome and Home Assistant"
category: General
wp_url: https://the78mole.de/reverse-engineering-the-buderus-km217/
blog_url: /blog/2021/reverse-engineering-the-buderus-km217
content_file: content/blog/2021/reverse-engineering-the-buderus-km217.md
total_comments: 113
discussion_id: D_kwDOSNCPls4Al_SA
discussion_number: 19
---

## Kommentare (113)

**Simon** – 2021-12-02

> **⭐⭐⭐⭐⭐**
> *Mutig ...*
>
> Du hast da einen kleinen aber feinen Zahlendreher ... KM271 und nicht KM217! :)
>
> Ein eigenes PCB zu designen ist schon echt Mutig vor allem wenn man bedenkt, dass das Ding im Herzen der Zentralheizung steckt.  Wär mir dann doch etwas riskant ... dann doch lieber die günstige Variante der KM271 von Bosch direkt (80€) + RS232 USB-Kabel + RasPi 3a+ mit seperater Stromversorgung und das KM271-Modul in FHEM drauf laufen lassen (3m entfernt) und per MQTT wohin auch immer schicken ... ist zwar etwas unhandlicher / größer aber deutlich komfortabler.
>
> https://fhem.de/commandref_modular.html#KM271
>
> Wie löst du das Problem mit der Abschirmung des WLAN-Signals durch das Blech?
>
> "raising an error from the flame sensor ... often once peer week"
>
> Das klingt aber nicht normal.
>
> Hast du irgendein Muster ausgemacht? Tritt das nur auf wenn dein Ölstand einen gewissen Pegel erreicht?
>
> Schau mal deinen Ölfilter an, wenn da zuviele Bläschen rausgedrückt werden dann liegt es daran dass er bei deinen Tanks irgendwo Luft zieht.
>
> Entweder die Dichtungen gehören gewechselt, und/oder aber die Ansaugstutzen in den Öltanks sind mit den Jahren porös geworden - alternativ ist die Leitung irgendwo undicht (müsste man aber sehen). Kann auch einfach nur Ölschlamm sein ... damals wurden meistens noch Tanks verbaut die Ansaugstutzen hatten die keinen Schwimmer integriert hatten - sprich Schläuche - deswegen auch die Frage nach dem Ölpegel.
>
> Wenn das ausgeschlossen ist würde ich mich mal dem Brenner widmen ... die Anlage ist eigentlich der VW Golf 1 der Ölheizungen (laut meinem Heizungsfachmann) zickt aber wenn ein paar Dinge nicht passen / verbraucht sind. Wurde allerdings deswegen oftmals auch so gut wie nie gewartet (auch von den Vorbesitzern bei unserem Haus nicht).
>
> p.s.: Deine Kommentarfunktion geht nicht ...

↳ **the78mole** – 2021-12-02

>> Hallo Simon,
>>
>> Danke für die Sterne...
>>
>> KM271... Mist, einmal falsch abgetippt und dann immer "kopiert"...
>>
>> Naja, mutig... PCB-Design ist bei mir Tagesgeschäft (gewesen bis August). Ist ja nicht so, dass ich das zum ersten Mal mache.... Ich sehe daran nichts Riskantes, es sind einfach elektrische Signale, nicht mehr und nicht weniger. Ich habe schon darauf geachtet, dass es keine Kurzschlüsse verursacht und die übrigen Signale genügend hochohmig angebunden sind, dass man nichts kaputt machen kann. Ich bin ja schließlich kein Laie sondern Elektrotechnik-Profi (Dipl.-Ing.) seit über 10 Jahren, gelernter Energieelektroniker Fachrichtung Betriebstechnik seit 20 Jahren und Elektronik-Bastler seit über 30 Jahren. Nur dass ich mittlerweile (seit August eben) Projektleitung in der Produktentwicklung mache und selbst beruflich kein Schaltungsdesign mehr.
>>
>> Ehrlich gesagt finde ich die Lösung mit dem ESP32 die einfachste und schickste Variante und die vielen Anfragen, die ich bekomme, geben mir da Recht. Hab schon einige Bausätze bzw. fertige Module verschickt...
>>
>> Das Problem mit dem Blech löst sich dadurch, dass der Deckel original aus Kunststoff ist und deswegen eine relativ gute WLAN-Anbindung sogar durch meine Kellerdecke hindurch gegeben ist. Der ESP berichtet -58 dBm, ab -85 dBm reißt der Empfang so langsam ab, also fast 30 dB Luft nach unten...
>>
>> Wenn Du wüsstest, was ich an meinem Brenner schon alles gereinigt und getauscht habe. Ich habe auch einen Schwimmer, der Filter und das Öl sehen absolut klar aus (null-komma-null Schmutz oder Schwebstoffe), keine Bläschen, nichts... Das Öl kommt perfekt an der Pumpe an. Vom Filter bis zum Rückschlagventil über die Düse bis hin zum Tausch der Ölpumpe, inkl. Zerlegung des ganzen Brenners in Einzelteile und deren Reinigung. Auch die Brennkammer und die Wärmetauschrippen schon öfter sauber gemacht. Nichts, was ich nciht versucht habe. Nur den Flammsensor selbst habe ich noch nicht ausgetauscht, allerdings reagiert er korrekt auf Flammbildänderungen, wenn man das Signal und das Flammbild durchs Schauglas vergleicht. Auch Flammgeräusche und Flammsensorsignal passen "gut" zusammen (wenn man z.B. an der Luftzufuhr "spielt". Auch Fachleute waren da nach mehrmaligem Handanlegen ratlos. Die Werte am Messgerät des Schlotfegers sind traumhaft gut und zeigen keine Auffälligkeiten... Naja, das Ding weicht früher oder später ohnehin einer Wärmepumpe. Jetzt zum Beispiel läuft er schon wieder seit über einem Monat problemlos durch :-(
>>
>> Kommentarfunktion ist moderiert, sonst steht da Massenweise Spam. Dauert nur manchmal, bis ich die Kommentare bemerke und frei gebe :-P
>>
>> Aber Danke für die Hinweise. Rückmeldung und Ideen sind immer gut.

---

**Benedikt** – 2021-12-03

> **⭐⭐⭐⭐⭐**
> *Great Project - I was looking for this!*
>
> I'm using FHEM right at the moment, but I like to switch to HA. The is a working implementation also for write the data. In fact, I can edit my heat programms.
>
> https://fhem.de/commandref_modular.html#KM271

---

**Gires** – 2021-12-20

> **⭐⭐⭐⭐⭐**
> *Kamstrup Multical21*
>
> Hello,
>
> Great article! Do you think I will be able to read data from my water meter Multical21 to Home Assistant by using the same approach?
>
> Thank you.
>
> Kind regards

---

**Manfred** – 2022-01-20

> **⭐⭐⭐⭐⭐**
> *Super Sache ................*
>
> .... kann man so ein fertiges Modul auch erwerben ?
> Bin grad so in das Thema Smart Home mit NodeRed eingestiegen und
> meine (ur-) alte Heizung wär natürlich schon ein interessantes Thema ...

↳ **the78mole** – 2022-01-20

>> Ja klar, schicke mir doch bitte eine Email an me@the78mole.de. Bausatz ginge Recht flott, für eine fertig aufgebaute Platine musst Du mit ein paar Tage Zeit geben...

---

**Eberhard** – 2022-04-25

> habe Interesse am kauf  einer fertig aufgebauten Platine. Leider kann ich die Bestellung nicht aufgeben da einige Bauteile nicht zur Verfügung sind.

---

**Alexander Kusnezov** – 2022-09-28

> **⭐⭐⭐⭐⭐**
> *Nur Monitoring oder Steuerung?*
>
> Kann man damit die Werte nur ablesen, oder kann man auch Steuern (Temperatur, Warmwasser, etc.)?

---

**Ralph** – 2022-09-29

> **⭐⭐⭐⭐⭐**
> *Genau das, was ich suche*
>
> Moin!
> Ich habe Interesse an einer fertigen Platine. Eigentlich wollte ich so etwas auf Basis einer NodeMCU selbst bauen, aber ein fertiges Gerät wäre natürlich besser - und schneller. Meine SMD-Lötkenntnisse sind allerdings nicht besonders.
>
> Ist die FW auch allgemein für MQTT/FHEM/OpenHAB geeignet?

---

**Henry** – 2022-10-23

> **⭐⭐⭐⭐⭐**
> *Tolles Projekt.......*
>
> Hallo Daniel,
>
> Durch Zufall bin ich auf Deinen sehr interessanten Blog gestossen. Möchte auch meine Logamatic aus der Ferne auslesen. Hast Du noch eine alte REV der Platine übrig (brauche "nur" seriell, kein WLAN) oder muss ich auf die Neulieferung warten ?
> Danke und Grüße
> Henry

↳ **the78mole** – 2022-10-23

>> Hallo Henry,
>>
>> leider ist alles an Bestand weg...
>>
>> Ohne WLAN-Modul ist schwierig, da ich nur SMD-bestückte PCBs bestellt habe und keine unbestückten. Man könnte theoretisch natürlich einfach einen USB-serial-TTL-Konverter (5V-Pegel) an die Stiftleiste anhängen und die Spannungsversorgung der restlichen Schaltung nicht freischalten, aber das wäre eigentlich Verschwendung. Man kann aber auch ganz einfach den seriellen Port des ESP über TCP verfügbar machen: https://github.com/AlphaLima/ESP32-Serial-Bridge
>>
>> Für den ESP8266 (leider nicht direkt für den ESP32) gibt es z.B. dieses Projekt hier: https://github.com/jeelabs/esp-link
>>
>> Auch in ESPhome ist das ganz easy. Einen Blogpost zu genau dem Thema habe ich ja auch schon erstellt: https://the78mole.de/the-remote-serial-debugging-nightmare/
>> So fällt dann auch das ganze Rumgekabele mit der seriellen Schnittstelle weg.
>>
>> Ich schreibe Dich auch nochmal über Email an bzgl. Adress-Austausch.
>>
>> Grüße,
>> Daniel

---

**Anton** – 2022-11-02

> **⭐⭐⭐⭐⭐**
> *Super Projekt!*
>
> Hallo!
>
> Ich finde das Projekt super und würde auch gerne eine der neuen Platinen erwerben. Bitte melde Dich gerne bei mir! Danke!
>
> Gibt es Plände auch Parameter zurück zu schreiben, bspw. Warmwassersolltemperatur oder andere, so dass man grundsätzlich die Regelung der 2107 beliebig dynamisch gestalten könnte?
>
> Viele Grüße!

---

**Jan** – 2022-12-04

> **⭐⭐⭐⭐⭐**
> *Mega Sache*
>
> ... Freu mich total dass du das hier angegangen bist und ich aufgrund meiner Anhaltenden "Brenner-Störung" auf Google suche war. Hab bei dir bestellt und freue mich total aufs testen und einbinden in HomeAssistant

---

**Stephan Linkel** – 2022-12-07

> **⭐⭐⭐⭐⭐**
> *Doku zur Jumper Row?*
>
> Erstmal vielen Dank für deine Arbeit!
> Eine Kleinigkeit, nachdem ich grade alles zusammengelötet hab: welche Jumper müssen denn gesetzt sein? auf Fotos seh ich bei dir mal 5V, GND, P4, RX, TX und P8, aber auch mal P9 bis P12...
> Gibts irgendwo Infos, welche wofür da sind?

↳ **the78mole** – 2022-12-07

>> Hallo Stephan,
>>
>> also die Minimalkonfiguration, damit die Funktionalität gegeben ist, lautet 5V, GND, P4, RX, TX, P8. Die anderen Jumper schleifen nur Signale zum ESP durch, deren Funktion ich (noch) nicht kenne.
>>
>> Hoffe, das hilft Dir weiter...
>>
>> Grüße,
>> Daniel (der freundlich, elektrisierte Maulwurf von Nebenan)

---

**Denis** – 2022-12-21

> **⭐⭐⭐⭐⭐**
> *Abwarten*
>
> Also aufgrund mehrere gleichen Probleme wie bei dir bin ich auf eine Seite gekommen. Ich hab immer wieder Brenner Fehler und der Heizungsmensch war schon 10 mal da und hat schon alles mögliche getauscht und findet nichts... doof natürlich wenn ich nicht daheim bin und der Fehler passiert und meine Frau nicht weis wie man es behebt mit dem Reset.... deshalb will ich das aus der Ferne machen können und benachrichtigt werden wenn es auftritt. Hab mich in deinem Shop mal auf die Warteliste setzen lassen und bin mega gespannt wann die neue Lieferung kommt und ob ich damit zurecht komme ! Vielen Dank auf alle Fälle mal das du da so hinterher bist !

---

**Ralph** – 2023-01-16

> **⭐⭐⭐**
> *Tolle Arbeit*
>
> Vor einiger Zeit wollte ich so etwas mal selbst basteln, aber diese Lösung ist viel besser als das, was ich mal geplant hatte - super!
> Die Platine läuft bei mir jetzt schon ein paar Wochen mit meiner Logamatic 2105 und FHEM/MQTT.
> Was mir jetzt noch fehlt ist eine BFU-Emulation, um die Raumtemperatur per MQTT zu setzen (ich möchte keine Kabel verlegen). Irgendwie könnte das ja klappen, schließlich läßt sich ja auch die Uhrzeit einstellen. Gibt es zum Setzen von Parametern irgendwelche Unterlagen oder Erkenntnisse?
> Alternativ gäbe es vielleicht noch die Möglichkeit, einen externen Raumsensor über ein Digipot (DS3502?) an einer vorhandenen BFU zu emulieren. Dazu wäre das Herausführen der I2C-Leitungen auf eine Steckleiste ggf. vorteilhaft.
>
> Viele Grüße,
>
> Ralph

↳ **the78mole** – 2023-01-16

>> Hallo Ralph,
>>
>> schade, dass Du nur 3 Sterne gibts :-(
>>
>> Tatsächlich ist gerade eine neue Version in der Mache, die auch I2C herausführt. Das mit der BFU-Emulation wird aber schwierig. Habe da mal etwas recherchiert und relativ bald wieder aufgehört zu graben. Die ESPhome-Firmware kann dank JensG und QSchneider aber bereits jede Menge Parameter setzen. Die Raumtemperatur geht aber meines Wissens nicht über die interne Schnittstelle zu setzen. Allerdings darf man das nicht zu oft tun, da einige der Parameter dazu führen, dass die Steuerung diese ins EEPROM schreibt und das hat eine begrenzte Anzahl Schreibzyklen (100K bis 1M). Stündliches Schreiben sollte aber z.B. kein Problem sein, dann hält die Kiste noch 10 Jahre (8760 h/Jahr). Öfter wird dann schnell desaströs :-)
>>
>> Grüße,
>> Daniel (Maulwurf)

---

**Gernot** – 2023-01-16

> **⭐⭐⭐⭐⭐**
> *Extraordinary Engineering*
>
> Hello Daniel,
> your initiative went alredy quit far together with an interested team of co-fighters. That is so good to see what can be achieved if a community takes the callenges to work together on such a complex project.
> The WiFi-KM217 module will be a very interesting part for all owners of a Buderus Logamatic that are doing smart home automation.
> As i am having a Buderus Ecomatic 4000 (HS4201) i was following your blog a few weeks now to figure out if your solution would be fitting for me as well.
> I also would like to integrate my Ecomatic 4000 heating system to my Home Assistant smart home contoller via ESPHome, but it does not work with the KM271.
> But i will get an original Buderus M404 KM 2.0 module. This is the communication module (with RS232 and RS485 interfaces) for the Ecomatic 4000.
> I wonder if you or the community might be interested in a similar reverse engineering project to create an "Ecomatic Smart-Home WiFi module" based on the knowledge from the "Logamatic KM217 wiFi module".
> What do you think?
> Gernot

↳ **the78mole** – 2023-01-16

>> Hi Gernot,
>>
>> thanks for all the flowers :-)
>>
>> I already answered on the mikrocontroller.net forum... but to make it complete, I'll my answer here will be more complete.
>>
>> It could be possible to do the reverse engineering, but I would like to first get the low hanging fruits and see, if your unit talks a (mostly) similar protocol on the serial interface. Afterwards you could attach a bread-board version of the ESP32 to the RS485 or the RS232 interface and try, if my ESPhome component is able to talk the dialect of your Buderus control unit. If all works fine, I would be willing to support in designing a PCB for/with you.
>> The major problem is, that I can not put my own hands on the hardware at yours and I don't know anybody that has such a controller.
>>
>> Regards,
>> Daniel (the78mole)

---

**Ralph** – 2023-01-18

> **⭐⭐⭐⭐⭐**
> *Tolle Arbeit, 6 Sterne von mir*
>
> Moin Dankel,
>
> es sollten eigentlich 5 Sterne sein. Ich hatte aber ein Problem mit meinem Browser, die Bewertung überhaupt abzugeben und habe mehrere Versuche benötigt. Dabei wurde die Bewertung von mir unbemerkt auf 3 zurückgesetzt - Sorry!

↳ **the78mole** – 2023-01-18

>> OK, vielen Dank! Jetzt passt es ja :-P

---

**Sven** – 2023-01-21

> **⭐⭐⭐⭐⭐**
> *Vorfreude und Reservierung für eine 0.0.6 Platine*
>
> Hi Daniel,
> vielen Dank das du dir die Arbeit machst und die Platine nochmals erweiterst!
> Ich melde hiermit schon mal Bedarf an einem neuen Exemplar an :-)
> Grüße Sven

↳ **the78mole** – 2023-01-21

>> Hi Sven,
>> Das freut mich :-) Allerdings werde ich noch etwas brauchen. Ich will vorher noch testen, ob das mit dem I2C und SPI sauber funktioniert, habe aber gerade noch einige andere sehr dringende ToDos auf der Agenda.
>> Du könntest Dich ggf. bei Tindie in die Waitlist oder die Watchlist setzen, dann bekommst Du auch mit, wenn es neue Hardware gibt.
>> Grüße,
>> Daniel

---

**Mike** – 2023-02-07

> **⭐⭐⭐⭐⭐**
> *Super!*
>
> Ich freue mich darauf, meine bald kaufen zu können.  Hope wird bald verfügbar sein.

↳ **the78mole** – 2023-02-07

>> Hi Mike,
>> noch habe ich nicht bestellt. Muss noch ein paar Tests und ein detailiertes Review machen, bin aber gerade sehr ausgelastet. Ich hoffe,  ich komme die nächsten Tage dazu.
>> Grüße,
>> Daniel

---

**Ralph** – 2023-02-19

> **⭐⭐⭐⭐⭐**
> *I2C Nutzung*
>
> Moin Daniel,
> ich habe bei Deiner älteren Version des Boards I2C jetzt über den leeren EEPROM Anschluß realisiert. Dort läßt sich leicht ein geeigneter JST-Stecker anlöten. Damit läßt sich z.B. ein Digipot anschließen, mit dem man einen externen Sensor der optionalen BFU simulieren kann.
> Danke für die Super-Vorarbeit!

↳ **the78mole** – 2023-02-19

>> Hallo Ralph,
>> ja, genau das gleiche habe ich auch gemacht. In der neuen Version, die wahrscheinlich in der zweiten März-Hälfte verfügbar auf Tindie ist, gibt es einerseits einen 2x5-pol Pin-Header für I2C und SPI und zudem auch einen Anschluss für One-Wire-Sensoren.
>> Grüße,
>> Daniel

---

**Sebastian** – 2023-02-28

> **⭐⭐⭐⭐⭐**
> *Neuling mit IT Background im Home Assistant Wahn*
>
> Hallo Daniel,
>
> ich habe vor kurzem erst angefangen mich mit Smart Home zu beschäftigen. Nun will ich alles was einen Netzwerk-Stecker hat in Home Assistant integrieren und auch Beleuchtung und Co einbinden. Aber jetzt hänge ich an der Heizung. Habe nen Gas-Kessel Gb192i mit dem KM100 Web-Modul. Außerdem das RC310 im Wohnzimmer an der Wand.
> Aber offenbar gibts da nix um die Anlage so in Home Assistant zu integrieren. Zumindest dachte ich das, bis ich auf deine Seite gekommen bin.
> Habe ich das richtig verstanden, dass deine Entwicklung direkt an die Heizung angeschlossen wird und dann per WLAN eingebunden wird?
> So ganz habe ich das noch nicht begriffen... Vielleicht kannst du es mir mit ein paar wenigen Worten erklären (zb. Was ist der Maintenance Jack?). Wie gesagt, ich bin IT'ler und kenn mich mit IT-Infrastruktur, sprich Server, Firewalls, VMWare, Switching und Co bestens aus. Aber das hier ist Neuland für mich.
> Vielen Dank im Voraus.
>
> Beste Grüße aus Hessen
> Sebastian

↳ **the78mole** – 2023-02-28

>> Hallo Sebastian,
>>
>> mein Modul belegt den Erweiterungs-Slot in der Logamatic und ersetzt eine optionale KM271 von Buderus. Der Stecker sieht so ähnlich aus, wie ein verkümmerter ISA-Steckplatz in den alten IBM-PCs (nennt man Card-Edge-Verbinder). Das KM100 wird aber extern angeschlossen. Leider habe ich absolut keine Ahnung, wie man das in den Home Assistant integrieren könnte. Leider habe ich aktuell wenig Zeit, Dich dabei zu unterstützen. Ein erster Google-Schuss fördert aber schonmal einen Thread aus der Homematic-Community zu Tage, der vielversprechend aussieht. Anders als der Titel vermuten lässt, wird da auch was über die KM100 gesagt: https://community.home-assistant.io/t/buderus-web-gateway-km200-support/25432/54
>>
>> Einfach mal ein wenig einlesen und schauen, ob es jemand über eine HACS-Komponente oder so geschafft hat. Wenn dem so ist, dann vermutlich über eine HTTP-Schnittstelle, die auch die Buderus App Easy Control oder das Bosch-Counterpart benutzt. Wie gesagt, einfach mal ein wenig Googeln, da wird man meistens schlauer und wenn es noch nichts fertiges gibt, dann bekommt man im Community-Forum häufig schon zielgerichtete Hilfe, um selbst was starten zu können. Das einzige was man braucht ist ein wenig Durchhaltevermögen, Technikaffinität und Zeit.
>>
>> Viel Erfolg :-)
>>
>> Grüße,
>> Dein Maulwurf

---

**Larry** – 2023-03-01

> **⭐⭐⭐⭐⭐**
> *OMG pizza*
>
> What the fuuuuck!!! Apparently my boiler is hacker worthy. Nice job on the solution to many problems.

↳ **the78mole** – 2023-03-01

>> Hi Larry,
>>
>> Apparently... but never say never. 5 years ago, I would also not believe, that this boiler will ever be integrated into any smart home :-P
>>
>> Regards,
>> the mole from your neighborhood :-P

---

**Christian** – 2023-03-23

> **⭐⭐⭐⭐⭐**
> *perfekt!!!*
>
> Hallo,
>
> grade ist die neue Platine angekommen, eingebaut, wlan konfiguriert und schon hat man alle Heizungsparameter in HomeAssistant! Besser wie von vielen großen Herstellern, danke!!!
>
> Gruß Christian

↳ **the78mole** – 2023-03-23

>> Danke Christian!
>> ICh bin selbst begeistert, wie gut das funktioniert :-)

---

**Oliver** – 2023-03-28

> **⭐⭐⭐⭐⭐**
> *LÄUFT - und dazu noch perfekter Service - 1A mit Sternchen*
>
> Habe im Rahmen meiner "Spielereien" zufällig dieses Projekt gefunden. Hersteller steht mit allerhand Info und Service zur Seite! DANKE!
> Achja, Board eingesteckt, läuft, nur ESPHome installieren und es wird erkannt ohne großes zutun. Alle Sensoren in HA. So muss es sein.

↳ **the78mole** – 2023-03-28

>> Vielen Dank für die Bewertung...
>> Aber da sind noch viel mehr Sensoren in der Buderus versteckt :-) Sind nur nicht alle im YAML eingetragen, damit der Mensch vor dem Bildschirm nicht den Info-Overflow bekommt... Einfach mal ein wenig durch den SSource-Code der Komponente auf GitHub browsen (z.B. die const.py und die sensor.py), da tun sich unendliche Weiten auf.

---

**Denis** – 2023-04-08

> **⭐⭐⭐⭐⭐**
> *Kein wifi*
>
> Habe meine PCB erhalten habe sie voll ausgestattet gekauft mit der Software etc. Nachdem ich sie nun eingebaut habe - erschien kein wifi was kann ich denn hier nun tun?

↳ **the78mole** – 2023-04-08

>> Hallo Denis,
>>
>> es dauert ein bis zwei Minuten, bis der Fallback-AP auftaucht. Währenddessen blinkt die grüne LED etwa im 2-Sekunden-Takt. Blinkt diese nicht, liegt entweder ein Problem mit der Spannungsversorgung vor (Jumper-Einstellungen prüfen, wenn PWRSEL und USB bestückt) oder ein Problem mit der FW (sehr unwahrscheinlich)
>>
>> Frohe Ostern, Dein
>> Maulwurf

---

**Jan** – 2023-04-20

> **⭐⭐⭐⭐⭐**
> *Funzt*
>
> Respekt! Funktioniert einwandfrei und macht mega Laune das ganze in Home Assistant einzublenden. Sehr sehr geil die alte Buderus in Wifi einzubinden.

↳ **the78mole** – 2023-04-20

>> Hallo Jan,
>>
>> ja, das gleiche Gefühl hatte ich auch, als ich es geschafft hatte. Ohne die Unterstützung meiner kleinen Community wäre das niemals möglich gewesen (die Firmware habe ich zum größten Teil von Jens zugeliefert bekommen) und ich war schlicht begeistert und dachte: "Sehr cool, so eine geniale Einbindung schaffen nicht einmal die neuesten Heizungen, die es derzeit zu kaufen gibt und das Ding ist gut 20 Jahre alt!"
>>
>> Grüße,
>> Dein Maulwurf :-)

---

**Alex Kusnezov** – 2023-04-28

> **⭐⭐⭐⭐⭐**
> *ESPHome und EEPROM*
>
> Funktioniert richtig gut!
> Da ich damit HK1 und HK2(Fußboden) betriebe habe ich mir mal einfach das hier mit allen Reglern geflashed: https://github.com/the78mole/esphome_components/blob/main/components/km271_wifi/km271-for-friends.yaml
>
> In Github schreibst du:
> "MORE CAUTION: If you plan to change settings, please take care not to change settings too frequently. Devices such as these heaters typically use so called EEPROM chips to store settings. Such chips only support a certain number of write operations before breaking down. You should be safe for some years if you don't write more 20 values per day - but there is no guarantee. Maybe someone can dig out some documentation about this to make sure."
>
> Was meinst du mit "beraking down"? Gehen kaputt oder stürzen ab und man muss manuell neustarten?
>
> Ich habe vor damit ab un zu ca. 2x Mal die Woche HK1 und HK2 Betriebsmodus zu ändern,
> Warmwassersolltemperatur Tag - bei Bedarf 3-4 Mal (da ich mit Holz heize, warte ich bis der Pufferspeicher voll ist und dreh dann hoch)
> HK1 & HK2 Raumsolltemperatur - 2-3 Mal am Tag, ebenfalls abhängig von der Pufferspeichertemperatur
>
> Das alles mache ich manuell schon die ganze Zeit, belastet das auch den EEPROM?
>
> Noch eine kleine Frage:
> Direkt am Gerät habe ich die Temperatur für die beiden Heizkreise synchron verändern können, hier habe ich die Möglichkeit diese unabhängig voneinander zu verändern. Kann man das wirklich so machen, oder ist das nur visuell?
>
> Ansonsten bin ich echt sehr sehr begesitert davon was du da auf die Beine gestellt hast und bin auch sowas von stolz ein Teil davon zu sein!
> Danke!

↳ **the78mole** – 2023-04-28

>> Hallo Alex,
>>
>> zuerst einmal, wenn das EEPROM kaputt geht, weiß ich tatsächlich nciht, was genau passiert. Ich kann ja nicht in die Firmware von Buderus schauen, sondern nur vermuten, wie ich es implementiert hätte. Sehr wahrscheinlich ist aber, dass dann entweder alles zu spinnen anfängt oder, dass die Heizung einfach mit einem Fehler den Diesnt quittiert oder einen Fehler anzeigt und in einem Notprogramm läuft.
>>
>> Fakt ist aber, dass zwei Schreibvorgänge am Tag absolut OK sind. Bei mir sind es ca. 3 Änderungen des WW-Betriebsmodus am Tag. Andere Einstellungen verändere ich eher selten (z.B. die Auslegungstemperatur), da ich mittlerweile den passenden Betriebspunkt gefunden habe.
>>
>> Was Du mich da bzgl. der beiden Heizkreise fragst, kann ich leider nicht beantworten. Bei mir ist nur ein Heizkreis. Zudem gibt es mehrere Temperaturen, die Du meinen könntest. Tatsächlich sind einige Parameter "doppelt" vorhanden, beziehen sich aber meines Wissens auf die gleiche Größe. Also egal, wo Du sie änderst, es ändern sich immer beide.
>>
>> Kannst es ja mal testen und zurück schreiben.
>>
>> Und ich bin auch begeistert, wie viele Leute sich über mein KM271 freuen. Anfangs dachte ich, das sind vielleicht ein Duzend "Chaoten", die genau so verrückt sind wie ich, aber tatsächlich sind es schon deutlich über 100. Einfach unglaublich.
>>
>> Und vielen Dank für die tolle Bewertung :-)
>>
>> Grüße,
>> Daniel (der freundliche Maulwurf aus Deinem Vorgarten :-P)

---

**Harry** – 2023-05-01

> **⭐⭐⭐⭐⭐**
> *Super Arbeit!*
>
> Habe die Platine erhalten/geflasht/eingebaut und es funktioniert! Bin begeistert! Danke! Nun hab ich versucht den Abgasfühler (FG) zu ergänzen und komme mit der Beschaltung nicht weiter - müssen alle Bauteile (R17/R11/R35/R39) drauf, oder ist das optional je nach Fühlertyp? Weiss jemand welcher Fühlertyp das genau sein soll? Bei Buderus finde ich Hinweise auf PT1000 und NTC100k..

↳ **the78mole** – 2023-05-01

>> Hallo Harry,
>>
>> bei dem Abgsfühler kann ich wenig helfen. Die Schaltung habe ich lediglich von einem Kollegen übernommen. Welcher Sensor-Typ das ist, weiß ich auch leider nicht. Buderus hat wohl beide Varianten (PT1000 und NTC 10k) im Angebot. Ich frage mal bei Michael nach, der hat das Teil anscheinend in Betrieb...
>>
>> Grüße,
>> Daniel (der freundliche Maulwurf aus Deinem Vorgarten)

---

**Fillip** – 2023-06-22

> **⭐⭐⭐⭐⭐**
> *Super Projekt*
>
> Super Projekt hier. Bin gerade dabei von FHEM auf HA umzusteigen. In FHEM habe ich die Originale KM271 genutzt, kann ich diese denn so auch weiter nutzen mit deiner Methode? Habe einmal ESPHome mit der "km217-for-friends.yaml" geflasht, dann die KM271 mit einem TTL Adapter an den ESP32 gehängt, jedoch kommen keine Werte an, klappt das so nicht?

↳ **the78mole** – 2023-06-22

>> Hallo Fillip,
>> eigentlich sollte das funktionieren. Evtl. RX &amp; TX vertauscht? GND nicht angeschlossen? Ansonsten fällt mir nur ein, dass im Sommer nur sehr wenige Daten von der Steuerung gesendet werden, wenn man nicht einen kompletten Datensatz von der Steuerung über das Log-Command anfordert,
>>
>> Hoffe, das hilft...
>> Dein Maulwurf

---

**Das Q** – 2023-06-23

> **⭐⭐⭐⭐⭐**
> *Super umgesetzt und Dokumentiert*
>
> Cool wie du hier alles schön sauber dokumentiert hast. Fotos hätte ich zwar auch und auch etliches zu dokumentieren, aber ich bin ein Stick fauler Hund und Optik spielt bei mir nur eine untergeordnete Rolle.
> Gefällt mir sehr gut wieviel Mühe du dir hier machst und wie akribische du deine Probleme löst.
>
> Nicht das ich deine Platine dringend bräuchte, aber die wird allein wegen dem Must have Faktor geordert.
>
> Ggf können wir uns ja ein kleinwenig unterstützen und ergänze. In unseren ideen

↳ **the78mole** – 2023-06-23

>> Hallo das Q,
>>
>> vielen Dank für die Blumen :-)
>>
>> Ganz altruistisch ist das nicht. Ich dokumentiere auch für mich selbst :-)
>>
>> Grüße,
>> Dein Maulwurf.

---

**Erich** – 2023-07-02

> **⭐⭐⭐⭐⭐**
> *Stark !!! Wenn's jetzt noch einen Adpater für ioBroker gäbe*
>
> Bin zufällig auf Deine Seite gestossen. Ich habe das KM271 vor Jahren in die Finger bekommen und auch das Kommunikationsprotokoll analysiert um damit die Zirkulation zu steuern.
> Respekt vor Deiner Arbeit
> l.f.

↳ **the78mole** – 2023-07-02

>> Lieber Erich,
>>
>> Du kannst den Konjunktiv streichen. Dwennis Fimrware ist MQTT basiert und verträgt sich hervorragend mit dem iobroker.
>>
>> https://github.com/dewenni/ESP_Buderus_KM271
>>
>> Grüße,
>> Dein Maulwurf

---

**Kai Schneider** – 2023-08-20

> **⭐⭐⭐⭐⭐**
> *Tolles Projekt / Abgastemperaturfühler*
>
> Hallo Zusammen,
>
> ein tolles Projekt. Ich hoffe das noch genügent Leute für eine weitere Bestellung zusammen kommen. BTW: Der Abgastemeraturfühler ist ein NTC100k. Habe ich selber im Einsatz.
>
> LG,
> Kai

↳ **the78mole** – 2023-08-20

>> Hallo Kai,
>>
>> hättest Du da zufällig eine Artikelnummer oder einen Link zu einem Shop, wo man den beziehen kann?
>>
>> Beste Grüße,
>> Daniel

---

**Günther** – 2023-11-11

> **⭐⭐⭐⭐⭐**
> *Ich bin so froh über dieses Projekt!*
>
> Habe das Modul seit ein paar Monaten im Einsatz. Es funktioniert problemlos mit Home Assistant und meldet mir die Brennerstörung, die in der Übergangszeit gerne mal vorkommt.
> Da ich nicht so tief in der Elektronik stecke: wäre es möglich, einen digitalen Ausgang des ESP 32 für ein Relais zu verwenden? Ist da noch was frei? Damit würde ich gerne mit Hilfe eines aktuators die Störung quittieren.
> Meine Alternative ist natürlich ein weiterer ESP, es wäre aber doch schöner, gleich den schon vorhandenen ESP zu verwenden.
>
> Vielen Dank für die Arbeit!

↳ **the78mole** – 2023-11-11

>> Hallo Günther,
>>
>> Danke für die Blumen :-)
>>
>> Natürlich kann man da noch einen Ausgang für ein Relais verwenden. Allerdings hängt es etwas davon ab, welche Version der Platine Du einsetzt. Bei der 0.0.6 ist das relativ einfach möglich, besonders, wen der Sensor-Header bereits aufgelötet ist. Einziges Problem könnte tatsächlich die Spannungsversorgung und die Treiberfähigkeit sein. Notfalls einfach über einen NPN-Transistor treiben lassen.
>> Ein möglicher digitalen Ausgang wäre z.B. an Pin 6 des Sensor Headers (Beschriftet mit CH5). Solltest Du das nicht alleine schaffen, dann kann ich Dir gerne eine Schaltung per Email zuschicken.
>> Hast Du denn schon geschaut, wie man die Störung mittels Reilais quittieren kann? Da müsste man sicher das Geräuse des Flammwächters aufschrauben, oder? Ich hab mir das noch nicht so im Detail angeschaut, weil der Fehler bei mir mittlerweile nur sehr selten auftritt.
>>
>> Grüße,
>> Daniel

---

**Dennis** – 2023-11-16

> **⭐⭐⭐⭐⭐**
> *richtig cooles Projekt*
>
> Ich bin sehr begeistert über die Qualität und Professionalität des Moduls und der Software. Habe es in HA eingebunden und bin da dort dann noch einmal von den unzähligen Aktoren und Sensoren überrascht worden. Sehr interessante Daten und mittels Verlauf und Diagrammen gut geeignet für Optimierungen.
> Ich wollte mir etwas Ähnliches selbst bauen und bin beim KM271 Research auf dieses Projekt gestoßen. Euer Projekt hat mir unzählige Stunden Arbeit abgenommen und es ist noch dazu viel besser umgesetzt, als ich es je hätte selbst bauen können. Danke

↳ **the78mole** – 2023-11-16

>> Hi Dennis,
>>
>> danke für die gute Bewertung... Ja, das Modul hat nun einige Schönheitskorrekturen erfahren. Das erste Modell hatte noch ein paar häßliche Drahtbrücken auf der Platine. Die aktuelle version 0.0.7 ist natürlich mittlerweile wirklich gut ausgereift.
>> Viel Spaß mit den Optimierungen :-)
>>
>> Wenn du den Energieverbrauch im HA Energy Dashboard einbauen möchtest (als Gasverbrauch, Öl kennt er nicht :-) ), dann könnten folgende Zeilen helfen:
>>
>> sensor:
>>   - platform: km271_wifi
>>     boiler_runtime_1:
>>       name: "Brennerlaufzeit 1"
>>       id: runtime1_minutes
>>   - platform: template
>>     name: "Oil Energy Equivalent"
>>     unit_of_measurement: kWh
>>     device_class: energy
>>     state_class: total_increasing
>>     entity_category: diagnostic
>>     accuracy_decimals: 3
>>     lambda: !lambda |-
>>       if(id(runtime1_minutes).state) {
>>         return id(runtime1_minutes).state * (21.0 / 0.95) / 60.0;
>>       }
>>       return NAN;
>>
>>     filters:
>>       - debounce: 1s
>>
>> Grüße,
>> Daniel

---

**Bernd** – 2023-12-21

> **⭐⭐⭐⭐⭐**
> *Tolles Teil*
>
> Hallo Daniel,
> nachdem ich ESPHome aus 2023.12 aktualisiert habe, fehlen folgende Sensoren oder sind vertauscht.
>     heating_circuit_1_curve_p10:
>       name: "HK1 Heizkurve +10 °C"  hier wird der -10 Grad angezeigt
>     heating_circuit_1_curve_0:
>       name: "HK1 Heizkurve 0 °C"
>     heating_circuit_1_curve_n10:
>       name: "HK1 Heizkurve -10 °C"  ist nicht mehr verfügbar
>
> Ich vermute, dass es Probleme mit dem Minus Zeichen gibt
>
> MfG
> Bernd

↳ **the78mole** – 2023-12-21

>> Mir ist da auch irgendwas aufgefalen, vermutlich ausgelöst durch ein ESPhome-Addon-Update. Habe die Anzeigelemente im Dashboard neu zugeordnet und es passt wieder...

---

**jim** – 2023-12-24

> **⭐⭐⭐⭐⭐**
> *Hervorragendes Projekt.*
>
> Im HS 2105 eingesteckt, WiFi angepasst, läuft! Was will man mehr?
>
> Nach gut 20 Jahre des laienhaften Rätselns, fange ich jetzt endlich an zu begreifen, wie meine Heizung angesteuert wird.
> Das Ersatz-KM271 ist jeden Cent seines bescheidenen Preises wert.
>
> Super Sache, danke vielmals &#x1f44d;&#x1f44f;

---

**Michael** – 2024-01-02

> **⭐⭐⭐⭐⭐**
> *Frage*
>
> Ich habe da auch eine Frage: Ich möchte 2 potentialfreie Relaiseingänge zusätzlich einlesen und über MQTT übertragen.
> (Über ralais ausgekoppelte Brenner in Betrieb und Flammstörung)
>
> Version ist die 0.0.7 mit der MQTT Firmware.
>
> Lässt sich dieses so realisieren ?
>
> Gruss, Michael

↳ **the78mole** – 2024-01-02

>> Hallo Michael,
>> entschuldige die späte Antwort, ich habe Dein Review gerade erst entdeckt...
>> Leider weiß ich zu wenig über dewennis Firmware, um Dir das umfassend beantworkten zu können. Aus Hardwaresicht kannst Du die aber relativ einfach am Sensor-Header anschließen. Die Analogeingänge CH5..7 einfach mit dem potenzialfreien Kontakt gegen GND ziehen. Auf meinem KM271 sollten die einen Pull-Up nach 3V3 besitzen. Bedeutet also, die Eingänge sind dann Low-Aktiv.
>> Hoffe, das hilft Dir weiter.
>> Grüße,
>> Daniel

---

**Michael** – 2024-01-02

> **⭐⭐⭐⭐⭐**
> *Sehr gut aber noch eine Frage*
>
> Ich habe da auch eine Frage: Ich möchte 2 potentialfreie Relaiseingänge zusätzlich einlesen und über MQTT übertragen.
> (Über ralais ausgekoppelte Brenner in Betrieb und Flammstörung)
>
> Version ist die 0.0.7 mit der MQTT Firmware.
>
> Lässt sich dieses so realisieren ?
>
> Gruss, Michael

↳ **the78mole** – 2024-01-02

>> Hallo Michael,
>> das ließe sich so realisieren. Du könntest die potenzialfreien Kontakte an den Sensor-Header (J6) oder auch an den Extension-Header (J7) anschließen. Beim Sensor-Header würde es sich anbieten, Pin 6-3 und Pin 4-3 über den potenzialfreien Kontakt zu brücken. Das zieht dann den ADC1_CH5 bzw. ADC1_CH6 des ESP32 gegen Masse. Allerdings sollten Dir die Zustände auch schon über die Parameter zur Verfügung stehen, die über den Bus gesammelt werden...
>> Beste Grüße,
>> Daniel

---

**Michael** – 2024-01-05

> **⭐⭐⭐⭐⭐**
> *Rückmeldungen.*
>
> Hi, ich weiss dass diese Betrieb und div störmeldungen auch über den Bus kommen. Bei einer Ölheizung hat dies aber einen Haken. Über den Bus kommt brenner Betrieb mit anziehen des Relais wenn T1 T2 Signal an den feuerungsauromaten gibt. Dann startet aber erstmal ölvorwärmung. Erst dann kommt luftumwälzung brennraum, Einspritzung und Zündung. Erst dann gibt der feuerungsautomat famme stabil als Betrieb zurück. Dies wertet die logamatk aber nicht aus. Auch direkte Störung feuerungsautomat aufgrund fall ignition oder Flame cut kriegt die logamatik nicht direkt mit [230v Signale aus dem feuerungsautomaten] deshalb bei mir die koppelrelais. Von mir stammte 2016 die python Variante mit km271 für die logamatik und die Fehler bekam ich nur extern hardwaremässig erfasst

↳ **the78mole** – 2024-01-05

>> Hallo Michael,
>> OK, so genau hatte mir das noch nicht angeschaut. Ich weiß nur, dass die Brennerstörung in meinem SmartHome korrekt ankommt und dieses mir dann eine Nachricht schickt.
>> Grüße,
>> Daniel

---

**D.R.** – 2024-01-10

> **⭐⭐⭐⭐⭐**
> *Perfekt!*
>
> Was soll ich sagen, ausgepackt, eingesteckt, Wlan ausgewählt und es funktioniert.
> Auch perfekt mit der Logomatic 2107 "ohne M".
> Vielen Dank sp spare ich mir  den ständigen Weg in den Keller :-)

---

**Markus** – 2024-02-04

> **⭐⭐⭐⭐⭐**
> *Danke, eine Frage zum flashen*
>
> Kann man auch über den eigebauten USB Stecker flashen oder braucht man die Pins auf dem Board+ CP2102 USB zu TTL Konverter?
> Danke
> Markus

↳ **the78mole** – 2024-02-04

>> Hallo Markus,
>> die USB-Buchse ist ausschließlich für die optionale Stromversorgung (wenn man ein Montagsmodell der Buderus hat, dessen Spannungsversorgung schlapp ist). Flashen muss man mit einem USB-seriell-Konverter. Da man eigentlich nur einmal flasht (bzw. kommt das Modul schon fertig geflasht) und weitere Updates ohnehin über OTA (WiFi) gehen, macht es keinen Sinn, da noch Platz und Geld Geld auf jedem Board zu versenken. Das wäre auch relativ schwierig mit zwei Layern gewesen.
>> Grüße,
>> Daniel

---

**Joachim** – 2024-02-14

> **⭐⭐⭐⭐⭐**
> *Problem mit Neustart*
>
> Hallo,
> ich habe die Version 0.0.5 seit in einigen Monaten am laufen. Nur leider kommt es in letzter Zeit vor, das das Modul nicht erreichbar ist und die Heizung sporadisch neu startet. Die Tage war auch die Sicherung auf der Hauptplatine durch. Außerdem kann man beobachten, das die LED´s an der Heizung leicht flackern, wenn das Modul eingesteckt ist!
> Habe wohl ein Montagsmodel oder die Hauptplatine/Stromversorgung hat einen defekt oder zieht das Modul einfach zuviel Strom?
> Was tun, kann ich die 0.0.5 mit einem Netzteil betreiben und wenn ja wo am besten anschließen?
>
> Viel Grüße und super Projekt&#x1f44d;&#x1f3fd;

↳ **the78mole** – 2024-02-14

>> Hallo,
>> tatsächlich scheint es so, dass manche Steuerungen eine sehr schwache Versorgung haben. Eine einfache externe Stromversorgung gibt es erst seit der Version 0.0.6. Demnächst sollte eine neue Charge mit 0.0.7 eintreffen, die kann man dann schön per USB versorgen.
>> Grüße,
>> Daniel

---

**Dustin** – 2024-03-07

> **⭐⭐⭐⭐⭐**
> *Nachschub*
>
> Hi!
>
> Wann meinst Du, wäre eine neue Lieferung bereit?
> Meine Buderus macht während der Heizzeit immer das Warmwasser mit.
> Das macht mich noch wahnsinnig :-D
>
> Grüße

↳ **the78mole** – 2024-03-07

>> Hallo Dustin,
>>
>> aktuell sieht es nach Ende März aus. Die PCBs scheinen fertig zu sein, aber die Bestückung dauert meiner Erfahrung nach immer einige Tage (aktuell bei 5%). Bauteile müssen bestellt und zugordnet, Bestückungsmaschinen eingerichtet, Muster bestückt, Qualität kontrolliert,... und die Produktion durchgeführt werden. Und dann kommt natürlich noch DHL ins Spiel mit Zollabfertigung und so Quatsch...
>>
>> Grüße,
>> Daniel

---

**Pierre Pichery** – 2024-08-25

> **⭐⭐⭐⭐⭐**
> *replace the BFU*
>
> Hello Daniel,
>
> I am very interrested in your KM271 replacement and I would like to install it on my Buderus 2107 (don't know if it is M or not, but I understand it works for both) and to integrate it with my existing Home Assistant set up. I am curently using a Buderus BFU Thernmostat and my quesstions at this point are as follows :
>
> - will I be able to replace the BFU and control the room temperature with Home assistant?
>
> - Can leave the BFU as is or will I need to disconnect it to avoid conflicts?
>
> - or perhaps can I leave the BFU and set it at a very low temprature to keep the contact open?
>
> Thank you for this and all the exellent work you have done on this topic.
>
> Best regards,
>
> Pierre Pichery

↳ **the78mole** – 2024-08-25

>> Hello Pierre,
>>
>> the BFU functionality can not be replaced by the KM271, but it can be installed in parallel. They address different aspects of the heating system. But I have no BFU myself, so I can only tell what I know from other users.
>>
>> Regards,
>> Daniel

---

**Michael** – 2024-09-24

> **⭐⭐⭐⭐⭐**
> *Power-on Reset*
>
> Seit ein paar Wochen schafft das Modul (v0.0.8) keinen power-on Reset mehr. Muss immer manuell resetten. Spannungen sind stabil, versorgt über Buderus. Hat jemand ein ähnliches Verhalten?

↳ **the78mole** – 2024-09-24

>> Hallo Michael,
>>
>> welche Firmware verwendest Du? Ich tippe mal auf Dewenni's FW. Könntest Du bitte im entsprechenden GitHub ein Issue erstellen?
>> Ich vermute, es liegt nicht an der HW.
>>
>> Beste Grüße,
>> Daniel

---

**Fabian** – 2024-09-28

> **⭐⭐⭐⭐⭐**
> *Lieferung verfügbar*
>
> Hallo Daniel, vielen Dank für dieses tolle Projekt. Ich hoffe, damit meine Logamatic 4212 in Home Assistant einbinden zu können. Ist denn geplant, dass man das fertige Board noch einmal bei Dir bestellen kann?

↳ **the78mole** – 2024-09-28

>> Hallo Fabian,
>>
>> üblicherweise warte ich immer, bis 50 Interessenten auf der Warteliste stehen. Dann ordere ich 100 Stück (Lieferzeit etwa 1 Monat) und diese verkaufe ich dann in den nächsten ca. 3 Monaten ab. Allerdings ist die Nachfrage mittlerweile eher Rückläufig, daher erwarte ich, dass es noch 1-2 Monate (oder länger) dauern wird, bis es wieder so weit ist.
>>
>> Grüße,
>> Daniel (der freundliche Maulwurf aus Deinem Blumenbeet... BTW: lecker)

---

**Xaver** – 2024-12-26

> **⭐⭐⭐⭐⭐**
> *Wann gibt's neue Boards?*
>
> Hallo Daniel,
> wirklich ein schönes Projekt, vielen Dank! Kannst du schon abschätzen, wann es wieder neue Boards geben wird? Würde liebend gerne ein Board bei mir verbauen.
> Viele Grüße
> Xaver

↳ **the78mole** – 2024-12-26

>> Hallo Xaver,
>>
>> schwierig zu sagen. Auf Arbeit ging es die Wochen vor Weihnachten sehr heiß her und ich hatte keine Zeit irgendwas nebenher zu machen. Es könnte Februar werden :-(
>>
>> Grüße,
>> Daniel

---

**Sebastian** – 2025-01-09

> **⭐⭐⭐⭐⭐**
> *Tolle Leistung*
>
> Moin,
> das ist ja echt irre, was hier erreicht wurde! Besser als die originale vom Hersteller! Ich bin in den letzten Jahren immer mal wieder versucht für meine Heizung was zu bauen, das Problem ist die HW4201 Steuerung. Ich finde nicht welchen Protokoll-Dialekt die FMEC-Fernbedienung spricht und ob man nicht lieber an den ECO-CAN gehen sollte. Hat hier jemand schon mal eine Lösung gesehen? Danke für eure Hilfe,
> Sebastian

↳ **the78mole** – 2025-01-09

>> Hallo Sebastian,
>> Da kenne ich mich leider nicht aus... Lieber mal ins Mikrocontroller- oder Haustechnik-Dialog-Forum posten...
>> Grüße,
>> Daniel

---

**Sebastian** – 2025-01-13

> **⭐⭐⭐⭐⭐**
> *Neue Lieferung?*
>
> Hallo Daniel,
> sehr cooles Projekt. Kannst du abschätzen, wann es wieder bestellbar ist?
> VG
> Sebastian

↳ **the78mole** – 2025-01-13

>> Hallo Sebastian,
>> neue Lieferung ist in der Mache. Ich kann aktuell schwer einschätzen, wie lange es dauert. Demnächst ist in China wieder ein Feiertags-Block und wie gut das dann am Ende mit der Bauteilbeschaffung, Zoll und Co klappt, weiß man vorher leider auch nicht. Realistisch dürfte Mitte Februar sein...
>> Grüße,
>> Daniel

---

**Gernot** – 2025-01-18

> **⭐⭐⭐⭐⭐**
> *Ecomatic 4000 HS4201 mit KM2.0*
>
> Hallo Daniel,
> basierend auf deiner ESPHome KM271-WIFI Software habe ich für die Buderus Ecomatic HS4201 mit den M404 Modul KM2.0 eine angepasste ESPHome Software erstellt.
> Die ist auf GitHub verfügbar
> https://github.com/GernotAlthammer/buderus_ecomatic4000
>
> Falls jemand fragen sollte kannst Du den Link weitergeben.
> Gruß
> Gernot

↳ **the78mole** – 2025-01-18

>> Hallo Gernot,
>>
>> werde es in den Blog-Post und auf GitHub verlinken :-) Danke für den Hinweis.
>>
>> Grüße,
>> Daniel

---

**Dustin** – 2025-01-20

> **⭐⭐⭐⭐⭐**
> *Fragen*
>
> Hi!
>
> Ich habe das Modul jetzt schon länger im Einsatz und es funktioniert soweit super!
> Nur zwei Dinge... Wenn bei mir mal das WLAN abstürzt, verbindet sich das Modul anscheinend nicht selbstständig wieder mit meinem Router. Ist das bekannt?
> Ich gehe dann immer hin und mach die Heizung einmal aus/an. Dann geht wieder alles...
> Und das umstellen der Gewünschten Warmwasser Temperatur funktioniert irgendwie nicht. Ist bei mir jetzt aber weniger relevant. Hab einen festen Wert genommen und das reicht mir auch :-) - Aber wenn man sich bspw. eine Legionellen Schaltung bauen wollen würde, gäbs evtl. Probleme.
>
> Danke!!

↳ **the78mole** – 2025-01-20

>> Hallo Dustin,
>>
>> bei mir (mit ESPhome) funktioniert beides (WiFi-Reconnect und Warmwasser) hervorragend. Meine Warmwasser-Solltemperatur wird ständig umgestellt, weil mein Ölbrenner nur als Aushilfe für die Wärmepumpe arbeitet und ich dass alleine über Warmwasser regele.
>> Zudem ist mir nichts bekannt von solchen Problemen.
>> Welche Firmware nutzt Du denn überhaupt? Dewennis oder ESPhome?
>>
>> Beste Grüße,
>> Daniel

---

**Thomas** – 2025-03-28

> **⭐⭐⭐⭐⭐**
> *Frage Einbau*
>
> Moin Daniel,
>
> Erstmal danke fuer deine ganze Arbeit. Hast du irgendwo ein Bild wie oder wo genau man die Platine einbaut. Ich komme aus der Softwareecke, und wer aus der Anleitung von Buderus nicht ganz schlau. Ich konnte die Platine leicht nicht "einfach" einstecken.
>
> MfG
> Thomas

↳ **the78mole** – 2025-03-28

>> Gibt eigentlich nur einen Steckplatz, wo sie schön reinpasst...

---

**Denis** – 2025-03-29

> **⭐⭐⭐⭐⭐**
> *Geniales Upgrade für betagte Steuerung*
>
> Eigentlich hatte ich mich damit abgefunden, dass meine gute alte Buderus 2107 Steuerung aus dem letzten Jahrtausend nicht in Home Assistant eingebunden werden kann. Bis ich durch völligen Zufall auf dieses geniale Modul gestoßen bin.
> Auch wenn die Heizung und Steuerung schon ein paar Jahre auf dem Buckel haben, ist es genial.
>
> Zusätzlich kann ich nun endlich meine Solarthermie-Anlage perfekt mit der Ölheizung in Einklang bringen. Bisher ging das nur über die Sensoren, blöd, wenn morgens schlechtes Wetter ist, die Ölheizung den Speicher aufheizt, die Sonne raus kommt, aber dann kaum Wärme aufgenommen werden kann.
>
> Was noch nicht klappt ist die korrekte Abgastemperatur über HA abzufragen. Die Buderus Steuerung zeigt am Display die Temperatur korrekt an, das Modul liefert scheinbar einen falschen Wert oder kann ihn nicht interpretieren. Hier forsche ich noch.
>
> Ein paar möglicherweise brauchbare Fakten für andere:
> - läuft mit meiner Buderus R2107 S0 Steuerung
> - für OTA Updates muss (zumindest bei mir) extra Strom mittels USB zugeführt werden, sobald das WLAN hier die Daten empfängt, bricht sofort die Stromzufuhr über die Steuerung zusammen und das Modul rebooted
> - bisher scheint auch nachts das Modul mal, vermutlich aufgrund Spannungsabfall, neu gestartet zu haben
> - passt auf die Ports auf der Buderus Platine auf! Es gibt 3 gleiche Ports, welche sich nur durch die Plastikführungen unterscheiden. Es passt eigentlich nur einer. Mit Gewalt oder abgebrochenen Plastiknasen passt das Modul garantiert auch in die anderen Ports
>
> Nochmal vielen, vielen Dank für die Entwicklung des Moduls!

---

**Chris** – 2025-04-12

> **⭐⭐⭐⭐⭐**
> *Versteckte SSID Probleme?*
>
> Hallo, erst mal wirklich super das Projekt, genau das was ich gesucht hab. Werde mich noch ein wenig damit auseinandersetzen müssen, weil ich auch schreibend auf die Logamatik zugreifen will, aber das kommt später :-). Mir ist jetzt folgendes aufgefallen: Ich habe aus verschiedenen Gründen mehrere WLANs (VLANs) und davon auch einige mit versteckter SSID. U.a. auch das WLAN, in das das KM271 Modul rein soll. Solange ich die SSID anzeigen lasse, ist alles prima. Sobald ich diese verstecke, verliert es die Verbindung. Ist das bekannt? Gibt es hier einen Workaround? Accesspoint: Lancom LW600, Firmware Modul = Auslieferungszustand Charge 03/2025 (weiß es grad nicht besser :-) )
>
> Gruß
> Chris

↳ **the78mole** – 2025-04-12

>> Hallo Chris,
>> danke für das positive Review... Zuerst mal wäre es wichtig zu wissen, welche Firmware Du einsetzt. Zum anderen sind solche Fragen auf GitHub (im entsprechenden Projekt) viel besser aufgehoben. Tatsächlich sollte es aber egal sein, ob das WLAN eine öffentliche oder eine verborgene SSID hat. Sobald es einmal eingerichtet ist, sollte die Verbindung stehen. Allerdings verstehe ich nicht ganz, was eine versteckte SSID bringen soll. Zum einen sehen Scanner das WiFi auch, wenn nur normale Daten übertragen werden, dafür sind die Beacons nicht nötig. Wenn das Passwort schwach ist, wird das selbst einen drittklassigen Hacker nicht davon abhalten, das WiFi zu knacken.
>> Grüße,
>> Daniel

---

**Marc** – 2025-05-04

> **⭐⭐⭐⭐⭐**
> *Stromversorgung ?!*
>
> Hallo,
>
> ich hab seit ein paar Wochen das Modul in der Heizung und bin eigentlich begeistert nur gestern ist was "komisches" passiert... Ich hab an der "EDV" gebastelt und der WLan AP für das Modul war ca.1h weg... irgendwann ist dann bei 28°C Außentemperatur der Brenner angesprungen. Grund dafür gabs eigentlich keinen.
>
> Mir ist dann aufgefallen das das LCD Display der Heizungssteuerung "stufenweise" Kontrast verliert wenn das Km271 Modul kein WLAN findet?!? --> siehe Video: https://www.youtube.com/shorts/hDZSB68njl4
>
> Sieht aus wie "Stromversorgung bricht zusammen" und scheinbar hat das dann irgendwie zu dem Brennerstart geführt?!
>
> Gibts ne Möglichkeit irgendwo die Versorgungsspannung abzugreifen um das zu prüfen?

↳ **the78mole** – 2025-05-04

>> Die etwas schwachbrüstige Spannungsversorgung der Buderus-Steuerung ist ein bekanntes Problem. Einige wenige Steuerungen (ich schätze 5%) scheinen da besonders betroffen von zu sein, die meisten garnicht.
>>
>> Direkt am Senosr-Header Pins 1, 3, 5, 7 bieten sich an. Die Belegung steht auch auf der Unterseite des Moduls.
>>
>> Man kann natürlich die Spannungsversorgung abgreifen.
>>
>> Besser wäre das Thema in den GitHub-Discussions zum Modul aufgehoben ;-)

---

**Thorsten** – 2025-05-05

> **⭐⭐⭐⭐⭐**
> *Kurze Frage?*
>
> Kann man einen bzw. 2 OneWire Temperatur Sensor(en) wie DS18B20 direkt an die Platine anschließen?

↳ **the78mole** – 2025-05-05

>> Ja, das geht. Je nachdem, welchen Versionsstand Deine Platine hat, musst Du nicht einmal etwas anpassen. Außerdem ist es noch sinnvoll, sich die Dokumentation (Schaltplan, ESPhome bzw. dewennis GitHub) genauer anzusehen. Support kann ich hier aus Zeitgründen nicht leisten.

---

**Rob** – 2025-05-16

> **⭐⭐⭐⭐⭐**
> *Funktioniert super, danke!*
>
> Vielen Dank für dieses tolle Projekt! Ich habe zwei der Boards gekauft und betreibe sie erfolgreich in Logamatic R2107 S0 Installationen in Kombination mit home Assistant.

↳ **the78mole** – 2025-05-16

>> Vielen Dank für die Rückmeldung. Freut mich, dass es Dir gefällt! Ich wünsche Dir noch viel Spaß mit dem kleinen Modul.

---

**Sebastian** – 2025-07-15

> **⭐⭐⭐⭐⭐**
> *5V Supply bei 44 Volt und Website nicht erreichbar*
>
> Hi,
> ich habe das Modul heute in Betrieb genommen und in Home Assistent integriert. Zwei Sachen wundern mich gerade:
> - die "KM217 5V Supply" wird zwischen 44,4 und 44,7 Volt angezeigt. Ist das nur ein Kommafehler? Dann wäre es aber auch zu wenig mit 4,4 Volt.
> - Das Modul ist über seine IP-Adresse nicht per http erreichbar, also auch keine OTA Update Möglichkeit.
>
> Hast du eine Idee dazu?
>
> Vielen Dank und Grüße

↳ **the78mole** – 2025-07-15

>> Hallo Sebastian,
>>
>> die viel zu hohe Spannung ist Absicht. Man muss den Sensor kalibrieren. Wie das geht... Spannung mit einem Multimeter messen, mit dem angezeigten Wert ins Verhältnis setzen (z.B. 4,95 / 44,5 = 0,111235) und damit den Multiplier im YAML multiplizieren. Der Grund ist, dass der ADC des ESP einfach grottig ist und ich den nicht "ab Werk" sauber kalibrieren kann...
>>
>> OTA-Updates macht man über das HA Add-On "ESPHome Builder". Da taucht dann auch das Modul auf und man kann das YAML-File editieren.
>>
>> Grüße,
>> Daniel

---

**Florian** – 2025-07-18

> **⭐⭐⭐⭐⭐**
> *Bedeutung der Diagnosewerte*
>
> Hi,
>
> habe das Modul nun seit einiger Zeit in Betrieb und funktioniert auch einwandfrei!
> Bei ein paar Werten bin ich mir aber unsicher.
> Was besagt z.B. Burner Runtime 2?
> Wenn ich Runtime 1 umrechne lande ich woanders und das ist dann auch der Wert, der mir am Display angezeigt wird.
> Außerdem kann ich mit einigen Diagnose Werten nichts anfangen wie z.B. Boiler Flow Sensor Alarm oder Boiler Performance Free/ High.
> Hauptsächlich bin ich aber an FBurnerFailure und Burner Alarm interessiert, da meine Heizung öfter einen Fehler wirft und ich so gerne nachvollziehen möchte, wann das denn immer der Fall ist.
> Leider wurde mir der Fehler bisher nie gemeldet, wenn tatsächlich einer angelegen ist.
>
> Gibts da eine Doku, was die Elemente alle bedeuten, die ich vielleicht übersehen habe?
>
> Vielen Dank!

↳ **the78mole** – 2025-07-18

>> Hallo Florian,
>>
>> welche Fehler für was genau stehen weiß wohl nur Buderus selbst. Ich hatte es seinerzeit auch genau wegen häufiger Brennerfehler entwickelt. Nachdem ich aber mein Problem beseitigt habe (die Ölzuleitung war zu straff gespannt und er hat so wohl irgendwie Luft gezogen), kann ich nicht mehr 100% sagen, welcher Parameter es war. Ich glaube aber, mein Fehler entsprach dem Eintrag im YAML:
>>
>>     error_burner_malfunction:
>>       name: "Fehler Brennerstoerung"
>>
>> Wichtig ist die ID "error_burner_malfunction", der Name ist nur Schall und Rauch für die Anzeige im Home Assistant...
>>
>> Bei der Brennerlaufzeit (glaube ich zu wissen), dass das nur Brenner mit mehreren Brennstufen betrifft. Die erste Laufzeit ist Standardbetrieb, die zweite der Betrieb mit veringerter Leistung.
>>
>> Hoffe das klärt alle Deine Fragen ;-)
>>
>> Grüße,
>> Daniel

---

**Johann Gerner** – 2025-07-19

> **⭐⭐⭐⭐⭐**
> *Tolles Projekt*
>
> Hallo "Pauli",
> nachwievor bin ich begeistert von dem KM271 WiFi Modul.
> In letzter Zeit bekomme ich beim Update-Versuch über ESPHome eine Fehlermeldung:
> ...
> Duplicate number entity with name 'Urlaubstemperatur' found. Each entity must have a unique name within its platform across all devices.
>   config_heating_circuit_2_holiday_target_temperature:
>     name: Urlaubstemperatur
> ...
> In der Datei
>  [source /data/packages/040b63aa/components/km271_wifi/km271-for-friends.yaml:306]
> ist die "Urlaubstemperatur" zweimal identisch für die zwei Heizkreise eingetragen.
> Das hat zwar bisher kein Problem dargestellt. Aber die aktuelle Version von ESPHome scheint da etwas empfindlicher zu sein.
> Es wäre nett, wenn Du die "Urlaubstemperatur" für die zwei Heizkreise unterschiedlich benennen könntest.
> Danke und viele Grüße
> Johann Gerner

↳ **the78mole** – 2025-07-19

>> Hallo Johann,
>>
>> ja, da hat sich ein Fehler eingeschlichen. Sollte aber jetzt behoben sein. Hab ich im Repo schon geändert.
>>
>> Siehe dazu auch:
>>
>> https://github.com/the78mole/esphome_components/issues/89
>>
>> Grüße,
>> Daniel

---

**Michael** – 2025-11-06

> **⭐⭐⭐⭐⭐**
> *Sauber geliefert*
>
> Hallo, danke für die schnelle und ordentliche Lieferung.
>
> Meine Frau hat ein wenig Bedenken wegen des Einbaus.
>
> Also effektiv ist es ein Plug and Play System oder? Also einbauen, anschließen und im Home Assistant Spaß haben.
>
> Gibt es evtl. ein paar Einbauanleitungen für ein Buderus Logamatic irgendwo?
>
> Vielen Dank

↳ **the78mole** – 2025-11-06

>> Hallo Michael,
>>
>> ja, meine Frau ist da auch immer etwas zurückhaltend :-)
>>
>> Im Wesentlichen ist es Plug and Play. In jedem Fall musst Du das WiFi korrekt einstellen und bei dewennis Firmware auch noch die GPIOs und ggf. den MQTT-Server passend einrichten.
>>
>> Die wichtigsten Sachen sollten aber im Getting Started Guide stehen (wenn ich ihn nicht vergessen habe, beizulegen)...
>>
>> Beste Grüße,
>> Daniel

---

**Marcus** – 2025-11-15

> **⭐⭐⭐⭐⭐**
> *Gaszähler*
>
> Super Sache das ganze!
> Ich betreibe das Modul ohne Problem mit ESPHome in Homeassistant.
> Jetzt würde ich gerne noch den Gasverbrauch über einen Reedkontakt messen. Wo muss ich den am Board anschließen und wie muss ich den dann in der YAML-Datei einbinden?

↳ **the78mole** – 2025-11-15

>> Hallo Marcus,
>>
>> ich betreibe leider keinen Öl- oder Gaszähler an meinem KM271-WiFi. Aber der Sensor-Header ist schomal der richtige Anschluss. Der Zähler ist meist ein potenzialfreier Kontakt. Hier nutzt man dann einfach einen GPIO mit einem Pull-Up (oder Pull-Down) und lässt diesen vom Zählerkontakt gegen Masse (oder +3V3) schalten.
>>
>> Ich weiß jetzt nicht genau, welche Version der Hardware Du im Einsatz hast. Seit 0.0.6 (und natürlich mit bestücktem Senosr-Header J6) sollte IO34/CH6 mit einem Pull-Up auf 3,3V ausgestattet sein. Dann müsstest Du den Zählerkontakt nur ziwschen Pin 3 (GND) und Pin 4 (CH6) hängen. Mit einem Multimeter könntest Du dann prüfen, ob der Pin in Ruhe auf 3,3V hängt und mit jedem Zählerimpuls kurz gegen Masse gezogen wird.
>>
>> Im ESPhome-YAML kannst Du dann den Pulse Meter verwenden, um das Ganze in eine entsprechende Menge (Energie) und Leistung (Durchfluss) umzurechnen: https://esphome.io/components/sensor/pulse_meter/
>>
>> Mehr kann ich Dir da jetzt leider nicht helfen, da ich selbst Pulse Counter und Pulse Meter noch nicht eingesetzt habe. Das sollte aber nicht allzu schwierig sein.
>>
>> Beste Grüße,
>> Daniel

---

**Hans** – 2026-01-18

> **⭐⭐⭐⭐⭐**
> *Flammensensor Fehler beheben*
>
> Einwandfrei! Sehr cool.
>
> Tip zum Flammensensor: das ist eine photoelektrische Erkennung der Helligkeit der Flamme durch ein Glas. Wenn man dieses putzt, ist der Fehler "keine Flamme erkannt" weg. Habe ich alle paar Jahre mal.

↳ **the78mole** – 2026-01-18

>> Hallo Hans,
>>
>> vielen Dank für den Tip! Bei mir ist es aber tatsächlich die Ölzuleitung, die ein Problem hat und irgendwo ein wenig Luft zieht, wenn die flexiblen Leitungen etwas gespannt sind.
>>
>> Beste Grüße,
>> Daniel

---

**Basti** – 2026-02-15

> **⭐⭐⭐⭐⭐**
> *Klasse Projekt!*
>
> Hallo Daniel,
> kannst du mir kurz sagen, wie ich ESPHome auf die neuste Version aktualisieren kann?
> Ist es mit der aktuellen Version möglich die Tag und Nachttemperaturen einzustellen?
>
> Danke und viele Grüße
> Basti

↳ **the78mole** – 2026-02-15

>> Hallo Basti,
>>
>> in ESPhome geht das bisher nur über kleine Umwege... Ich habe es selbst nie getestet, aber Jens hat hier ein Snippet ins Repo gepusht:
>> https://github.com/the78mole/esphome_components/blob/fe43ca7f51a3715fbe29451a63835fbc52cd3e46/components/km271_wifi/snippets/buderus-km271-set-date-and-time.yaml#L107
>>
>> Ich hoffe, das hilft Dir weiter.
>>
>> Grüße,
>> Daniel

---
