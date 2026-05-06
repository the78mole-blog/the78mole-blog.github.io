---
title: "Kommentare: KM271-WiFi - HowTo"
category: General
wp_url: https://the78mole.de/projects/km271-wifi-howto/
blog_url: /pages/km271-wifi-howto
content_file: content/pages/km271-wifi-howto.md
total_comments: 12
discussion_id: D_kwDOSNCPls4Al_R9
discussion_number: 18
---

## Kommentare (12)

**Petr Novotný** – 2023-05-03

> Hi Daniel,
> I received the KM271-wifi board from you, connected it to the Logamatic unit. I'm having trouble connecting to Fallback Hotspot. I try the password "Z8z....." but I always get the message "Unable to connect to this network". Interestingly, after that I don't even see the Fallback Hotspot SSID anymore, I have to reboot the power to make it appear again. I tried it from iPhone and also from PC. What could be the problem?
>
> Thanks
> Petr Novotný

---

**Johann Gerner** – 2023-06-08

> Hallo,
> Den KM271 Adapter betreibe ich an einer Buderus Logomatik R2107 (Atmosphärischer Gasbrenner). Gibt es eine Begrenzung für die Belastbarkeit der 5V Quelle auf dem Adapter? Ich würde gerne noch drei 18b20 und eine Relaisplatine damit ansteuern... und auf eine zusätzliche 5V-Versorgung verzichten. Gibt es da Erkenntnisse?
> Schöne Grüße aus dem Bayerischen Wald

↳ **themole** – 2023-06-08

>> Hallo Johann,
>>
>> bei den 1-wire-Sensoren sehe ich da keine Probleme, die brauchen praktisch keinen Strom. Ich würde aber eher mit den 3,3V versorgen, da die ESP32-IOs nicht 5V-tolerant sind. Bei dem Relais bin ich da schon etwas skeptischer. Grundsätzlich ist die Versorgung von der Buderus anscheinend etwas schwachbrüstig und streut sehr stark. Es gibt ein paar Berichte von meinen Nutzern, dass es nicht mal ausreicht, den ESP32 stabil zu versorgen, während andere anscheinend absolut keine Probleme haben. Ich vermute, es hängt stark davon ab, welche originalen Zusatz-Module von Buderus selbst noch verbaut sind.
>>
>> Ich würde empfehlen, es einfach zu versuchen und die 5V z.B. bei aktiviertem Relais und im WiFi-Betrieb zu messen (das Relais aber über einen Transistor entkoppeln, die IOs des ESP32 sind definitiv dafür nicht ausgelegt und die Freilaufdiode nicht vergessen, sonst ist alles ganz schnell Schrott). Bricht die 5V-Versorgung zu stark ein, kannst Du ja noch immer auf USB-Versorgung ausweichen oder ein Solid-State-Relais verwenden.
>>
>> Grüße,
>> der Maulwurf

↳ **Johann Gerner** – 2023-06-08

>> *Antwort auf **themole**:*
>> > Hallo Johann,
>> > 
>> > bei den 1-wire-Sensoren sehe ich da keine Probleme, die brauchen praktisch keinen Strom. Ich würde aber eher mit den 3,3V versorgen, da die ESP32-IOs nicht 5V-tolerant sind. Bei dem Relais bin ich da schon etwas skeptischer. Grundsätzlich ist die Versorgung von der Buderus anscheinend etwas schwachbrüstig und streut sehr stark. Es gibt ein paar Berichte von meinen Nutzern, dass es nicht mal ausreicht, den ESP32 stabil zu versorgen, während andere anscheinend absolut keine Probleme haben. Ich vermute, es hängt stark davon ab, welche originalen Zusatz-Module von Buderus selbst noch verbaut sind.
>> > …
>>
>>
>> Danke für die sehr schnelle Antwort.
>> Dass die Versorgung aus dem Buderus etwas schwachbrüstig ist, sieht man an den 4,77 Volt die Dein Board mißt. Ich bau mir in der Konsequenz eine Art USB-Netzzeil ins Buderus-Gehäuse ein. Das mit dem Relais... ich benutze fertig aufgebaute Relais-Board mit Optokoppler, Freilaufdiode usw... was man halt so braucht damit die Spule nicht "zurückschlägt".
>> Nun bin ich jedoch auf ein Problem gestoßen. Ich habe den ersten 18b20 angeschlossen und er funktioniert auch, wird mit seiner Adresse erkannt und ich bekomme den Temperaturwert auch in HA angezeigt. Die weiteren 18b20 werden jedoch nicht gelistet. Ist da im Code eine Grenze eingetragen die am OW (R66 habe ich natürlich eingelötet) die Nutzung von nur einem Sensor ermöglicht?
>>
>> Schöne Grüße
>> Johann

↳ **Johann Gerner** – 2023-06-08

>> *Antwort auf **Johann Gerner**:*
>> > Danke für die sehr schnelle Antwort.
>> > Dass die Versorgung aus dem Buderus etwas schwachbrüstig ist, sieht man an den 4,77 Volt die Dein Board mißt. Ich bau mir in der Konsequenz eine Art USB-Netzzeil ins Buderus-Gehäuse ein. Das mit dem Relais... ich benutze fertig aufgebaute Relais-Board mit Optokoppler, Freilaufdiode usw... was man halt so braucht damit die Spule nicht "zurückschlägt".
>> > Nun bin ich jedoch auf ein Problem gestoßen. Ich habe den ersten 18b20 angeschlossen und er funktioniert auch, wird mit seiner Adresse erkannt und ich bekomme den Temperaturwert auch in HA angezeigt. Die weiteren 18b20 werden jedoch nicht gelistet. Ist da im Code eine Grenze eingetragen die am OW (R66 habe ich natürlich eingelötet) die Nutzung von nur einem Sensor ermöglicht?
>> > …
>>
>>
>> Sorry für meine Anfrage, mein Problem hat sich erledigt, das Board mußte nur neu gestartet werden.... :-)

↳ **themole** – 2023-06-08

>> *Antwort auf **Johann Gerner**:*
>> > Danke für die sehr schnelle Antwort.
>> > Dass die Versorgung aus dem Buderus etwas schwachbrüstig ist, sieht man an den 4,77 Volt die Dein Board mißt. Ich bau mir in der Konsequenz eine Art USB-Netzzeil ins Buderus-Gehäuse ein. Das mit dem Relais... ich benutze fertig aufgebaute Relais-Board mit Optokoppler, Freilaufdiode usw... was man halt so braucht damit die Spule nicht "zurückschlägt".
>> > Nun bin ich jedoch auf ein Problem gestoßen. Ich habe den ersten 18b20 angeschlossen und er funktioniert auch, wird mit seiner Adresse erkannt und ich bekomme den Temperaturwert auch in HA angezeigt. Die weiteren 18b20 werden jedoch nicht gelistet. Ist da im Code eine Grenze eingetragen die am OW (R66 habe ich natürlich eingelötet) die Nutzung von nur einem Sensor ermöglicht?
>> > …
>>
>>
>> Hallo Johann,
>>
>> auf die 4,77V würde ich mich nicht verlassen. Der ADC des ESP32 ist sowas von daneben, speziell wenn man den hochohmig anfährt (ich hab das Design so gemacht, um keine bösen Überraschungen mit hoheren Spannungen/Spannungsspitzen zu erfahren). Also einfach mal mit einem Multimeter nachmessen, dann bist Du auf der sicheren Seite. Speziell die Unterschiede (der Spannungseinbruch) bei Stand-By und WiFi-Aktivität sind da interessant.
>>
>> Bzgl. OneWire: Also ich hatte da schon eine ganze Hand voll Temperatursensoren dran und bisher selten Probleme. Allerdings muss der Pull-Up richtig dimensioniert sein, wenn man keinen Active-Pull-Up hat. Ich nehme mal an, Du benutzt ESPhome als Basis... Wenn Du nur die onewire-Komponente instantiierst (ohne einen Sensor o.ä. der die benutzt), dann solltest Du im Log alle Teilnehmer-Adressen am Bus sehen... (aber Du scheinst es ja schon gelöst zu haben :-P )
>>
>> Grüße,
>> Dein Maulwurf

↳ **Johann Gerner** – 2023-06-08

>> *Antwort auf **themole**:*
>> > Hallo Johann,
>> > 
>> > auf die 4,77V würde ich mich nicht verlassen. Der ADC des ESP32 ist sowas von daneben, speziell wenn man den hochohmig anfährt (ich hab das Design so gemacht, um keine bösen Überraschungen mit hoheren Spannungen/Spannungsspitzen zu erfahren). Also einfach mal mit einem Multimeter nachmessen, dann bist Du auf der sicheren Seite. Speziell die Unterschiede (der Spannungseinbruch) bei Stand-By und WiFi-Aktivität sind da interessant.
>> > …
>>
>>
>> Hallo "Pauli" (der Maulwurf aus Sendung mit der Maus... ja genau so alt bin ich schon), nochmal vielen Dank für Deine Mühe, also genauer gesagt vor allem für die Mühe die Du Dir mit dem Board und der Software gemacht hast. In Sache Elektronik bin ich so eine Art "Schmied"... das Zeug einfach mal zusammengekloppt aus dem Zeug was man so da hat. Den Pull-Up habe ich mit 10 K realisiert (Grenzwertig, ich weis), als Software nehme ich ESPHome, und als "Dallas" Bibliothek "dallasng" (die geht mit Lesefehlern besser um).
>>
>> Das Ziel: meine Warmwasser-Zirkulation "schlau" machen.
>>
>> Also noch mal vielen Dank für Deine Mühe. Mit Deinem Board erspare ich mir ein separates Gehäuse im Keller, kann (so lange ich noch darf) endlich meine Heizung auch vom Büro aus steuern (wenns den Frauen wieder mal zu kalt ist) und könnte rein Theoretisch meine Heizenergie optimiert einsetzen (mal sehen).
>> Uuuuund... es ist auch Hobby.
>>
>> Schönes Wochenende
>> Hans

---

**Hans** – 2023-06-08

> **⭐⭐⭐⭐⭐**
> *Buderus dürfte neidisch werden*
>
> Hallo Maulwurf,
> nochmal: tolle Arbeit. Was würde Buderus für das Teil verlangen (wenn sie es hinbekommen würden?)... ich will mir das nicht ausmalen.
> Bei mir funktionierte die eingebaute Software auf anhieb, und die Erweiterungen (OneWire) scheinen auch zu funktionieren.
> Beste Grüße

---

**Johann Gerner** – 2023-06-11

> Hallo "Maulwurf",
> wo muß ich "drehen" um eine brauchbare Abgasthemperatur (KM271 mit Logomatik 2107R und Home-Assistant) zu bekommen?
> Aktuell steht im kalten Zustand 255. (0) wäre OK, Irgendwo kippt da das "Byte".
>
> Schöne Grüße
> Hans

↳ **themole** – 2023-06-11

>> Hallo Hans,
>>
>> da muss dann der entsprechende Abgassensor drangebaut werden. Das mit dem Werte-Kippen hab ich schon öfter gehört. So lange Deine Heizung normal arbeitet, einfach ignorieren. Ich hab den Wert nicht in meine YAML aufgenommen.
>>
>> Es liegt einfach daran, dass die Original-KM271 neben der RS232 auch einen Anschluss für den Abgassensor bereitstellte. Und die Logamatic denkt ja, dass da das Original drin ist. Das bekomme ich nicht weg. Den Anschluss für den Abgassensor gibt es bei mir auch, nur habe ich den Stecker nicht bestückt (die Komponenten sind aber standardmäßig da) und ich wollte mir auch keinen Sensor einbauen. Evtl. mache ich das noch irgendwann, aber die Original-Sensoren sind mit zu teuer und ich habe gerade andere wichtigere ToDos auf meinem Zettel.
>>
>> Grüße,
>> Dein Maulwurf

---

**Johann Gerner** – 2023-06-11

> Hallo Maulwurf,
> vielen Dank für Deine Infos. Jetzt bin ich schlauer und habe unter:
> https://www.heiz24.de/mediafiles/pdf/6720817828.pdf
> gefunden das der Sensor ein gewöhnlicher PT1000 ist, und sowas hat man standardmäßig im Baselkeller rumliegen. Den werde ich demnächst ausprobieren, ob da was gemeldet wird.
> Danke und schöne Grüße
> Hans

↳ **themole** – 2023-06-12

>> Hallo Hans,
>>
>> musst aber aufpassen, dass der Fühler auch die Temperaturen mitmacht. Speziell die Leitung sollte dafür ausgelegt sein. Bei mir ist die Abgastemperatur nach letzter Schlotfeger-Messung so um die 150°C. Das macht keine normale PVC-Leitung mit. Sollte also irgendwas in der Art Glasfasergeflecht oder so sein. Falls Du den Sensor selbst baust, auch Lötzinn könnte bei erhöhten Abgastemperaturen schon weich werden...
>>
>> Grüße,
>> Daniel

---
