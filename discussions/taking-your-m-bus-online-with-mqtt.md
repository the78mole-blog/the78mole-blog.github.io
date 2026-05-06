---
title: "Kommentare: Taking Your M-Bus To The Next Level... MQTT"
category: General
wp_url: https://the78mole.de/taking-your-m-bus-online-with-mqtt/
blog_url: /blog/2021/taking-your-m-bus-online-with-mqtt
content_file: content/blog/2021/taking-your-m-bus-online-with-mqtt.md
total_comments: 14
discussion_id: D_kwDOSNCPls4Al_SV
discussion_number: 22
---

## Kommentare (14)

**Joël Stauber** – 2021-07-27

> **⭐⭐⭐⭐⭐**
> *Taking Your M-Bus To The Next Level… MQTT article*
>
> Hi,
>
> I have successfully integrated your approach (Taking Your M-Bus To The Next Level… MQTT article) to read data from my water meter, only when launching the read_send_meters_mqtt.sh script does the reading of the information take place not. I think my credentials are wrong. What value should I enter under MQTT_Host? This is the IP address of the broker with which I will receive the data (here Jeedom in a virtual machine) or is it the IP address of the Raspberry Pi with which I read the Mbus values? Same, which MQTT_User and MQTT_Pass values should I enter?
>
> Thanks,
> Joël

---

**Fernando** – 2022-01-07

> **⭐⭐⭐⭐⭐**
> *Great tutorial!*
>
> I never thought I could read 8 M-bus meters in Homeassistant.
> Thank you very much for this great job.

---

**Martin** – 2022-01-26

> **⭐⭐⭐⭐⭐**
> *Tolle Einführung, die mir sehr geholfen hat*
>
> Ich habe mir erlaubt, dein Script etwas zu erweitern:
> #!/bin/bash
>
> # Code Basis stammt von https://the78mole.de/taking-your-m-bus-online-with-mqtt/
> # Ich habe es nur ergänzt um alle Datenfelden flexibel zum MQTT Server zu übertragen
> # Getestet nur mit einem Wärmezähler. Ich hoffe es felxibel genug auch für andere Geräte
>
>
> ADDRESS_FILE="./addresses.txt"
> BAUDRATE=2400
> DEVICE=/dev/ttyAMA0
> MQTT_HOST=HOSTNAME
> MQTT_USER=MQTT_USER
> MQTT_PASS=MQTT_PASSWORT
> MQTT_TOPIC=MQTT_TOPIC
>
> #Basis Informationen
> modbus_array[0]=.MBusData.SlaveInformation.Id
> modbus_array[1]=.MBusData.SlaveInformation.Manufacturer
> modbus_array[2]=.MBusData.SlaveInformation.Version
> modbus_array[3]=.MBusData.SlaveInformation.Status
>
> #----------------------------------------------------------
>
>
>
>
>
> while read ameter
> do
> echo -n "Getting data from $ameter..."
>     # The sed is for replacing the @ with _ to be able to match on it in HASS templates
>      METER_DATA=$(mbus-serial-request-data-multi-reply -b $BAUDRATE $DEVICE $ameter | xq . | sed -e 's/@/_/')
>       /usr/bin/mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS
>         -t $MQTT_TOPIC/$ameter -m "${METER_DATA}"
>
>  BYTCNT=$(echo "$METER_DATA" | wc -c)
>     echo "  $BYTCNT bytes sent"
>
>
> # Basis Parameter auslesen
> for Parameter in "${modbus_array[@]}"
> do
>   ausgabe=$(echo $METER_DATA | jq "$Parameter" )
>   #Punkte in / konvertieren für mqtt
>   Parameter=$(echo $Parameter | sed -e 's!.!/!g')
>   /usr/bin/mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS -t $MQTT_TOPIC/$ameter$Parameter -m "$ausgabe"
>   #Ausgabe des MQTT Pfades und Wertes
>   echo "$MQTT_TOPIC/$ameter$Parameter -> $ausgabe"
>
> done
>
> #Schleife über alle Data Records
> for row in $(echo $METER_DATA | jq '.MBusData.DataRecord | keys'); do
>
> 	#Leere Datenfelder am Anfang und Ende abfangen
> 	if [[ ${row} != "[" ]] && [[ ${row} != "]" ]]
> 	then
> 	 #Das Komma am Ende entfernen
> 	 id=$(echo "${row}" | sed -e 's/,//')
>
> 	 #Einen Int Wert daraus machen
> 	 nummer=$(("$id"+0))
>
> 	  #Alle Keys (Datenpunkte) auslesen
> 		for name in $(echo $METER_DATA | jq ".MBusData.DataRecord[$nummer] | keys"); do
>
> 			#Leere Datenfelder am Anfang und Ende abfangen
> 			if [[ ${name} != "[" ]] && [[ ${name} != "]" ]]
> 			then
>
> 				# Ein paar Sonderzeichen aus dem Pfad entfernen
> 				pfad=".MBusData.DataRecord[$nummer].${name}"
> 				pfad=$(echo $pfad |  sed 's/"//g')
> 				pfad=$(echo $pfad |  sed 's/,//g')
>
> 				#Den richtigen Wert aus dem json holen
> 				wert=$(echo $METER_DATA | jq $pfad)
>
> 				#Umformatieren für eine MQTT Pfad
> 				pfad=$(echo $pfad |  sed 's/.///g')
> 				pfad=$(echo $pfad |  sed 's/[/_/g')
> 				pfad=$(echo $pfad |  sed 's/]//g')
> 				#Zum MQTT Server senden
> 				/usr/bin/mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS -t $MQTT_TOPIC/$ameter$pfad -m "$wert"
> 				echo "$MQTT_TOPIC/$ameter$pfad --> $wert"
>
> 			fi
>
> 		done
>
>
> 	fi
>
> done
>
>
>
> done < <(cat $ADDRESS_FILE)

↳ **the78mole** – 2022-01-26

>> Hallo Martin,
>>
>> schön, dass es Dir geholfen und gefallen hat.
>> Danke auch für die Verbesserungsvorschläge. Die werde ich mir mal genauer anschauen und einpflegen.
>>
>> Grüße,
>> Daniel (the78mole)

---

**Lutz** – 2022-10-11

> Hallo, danke für diese Inspiration. Ich würde das gerne an meinen Gas-Sensor anpassen, aber leider hängt es ein wenig, bei dem angepassten Script aus dem Kommentar.
> So weit bin ich gekommen:
> mbus-serial-request-data-multi-reply -b 2400 /dev/ttyAMA0 10 | xq . | sed -e "s/@/_/"
> {
>   "MBusData": {
>     "SlaveInformation": {
>       "Id": "40867341",
>       "Manufacturer": "ELS",
>       "Version": "37",
>       "ProductName": null,
>       "Medium": "Gas",
>       "AccessNumber": "9",
>       "Status": "00",
>       "Signature": "0000"
>     },
>     "DataRecord": {
>       "_id": "0",
>       "Function": "Instantaneous value",
>       "StorageNumber": "0",
>       "Unit": "Volume (m m^3)",
>       "Value": "1545810",
>       "Timestamp": "2022-10-11T10:56:38Z"
>     }
>   }
> }
> Möglicherweise sind die Leerzeichen in den Werten ein Problem?
> Hier die Debug-Ausgabe:
> mbusmeter/10///////////////////////////////// -&gt; "00"
> ++ echo '{' '"MBusData":' '{' '"SlaveInformation":' '{' '"Id":' '"40867341",' '"Manufacturer":' '"ELS",' '"Version":' '"37",' '"ProductName":' null, '"Medium":' '"Gas",' '"AccessNumber":' '"26",' '"Status":' '"00",' '"Signature":' '"0000"' '},' '"DataRecord":' '{' '"_id":' '"0",' '"Function":' '"Instantaneous' 'value",' '"StorageNumber":' '"0",' '"Unit":' '"Volume' '(m' 'm^3)",' '"Value":' '"1545810",' '"Timestamp":' '"2022-10-11T12:13:13Z"' '}' '}' '}'
> ++ jq '.MBusData.DataRecord | keys'
> + for row in $(echo $METER_DATA | jq '.MBusData.DataRecord | keys')
> + [[ [ != \[ ]]
> + for row in $(echo $METER_DATA | jq '.MBusData.DataRecord | keys')
> + [[ "Function", != \[ ]]
> + [[ "Function", != \] ]]
> ++ echo '"Function",'
> ++ sed -e s/,//
> + id='"Function"'
> + echo '"Function"'
> "Function"
> ./rread_send_mbus_2_mqtt.sh: line 72: "Function"+0: syntax error: operand expected (error token is ""Function"+0")
>
> Für etwas Hilfe wäre ich sehr dankbar.
> Gruss Lutz

↳ **themole** – 2022-10-11

>> Hallo Lutz,
>>
>> mir fehlt da zugegebenermaßen ein wenig Information, z.B. Dein Script rread_send_mbus_2_mqtt.sh, das in Zeile 72 offenbar ein Problem enthält. Das Kommando "keys" sagt mir nichts und ich kann auch nicht erkennen, was das hier tun soll... Stopfe doch Dein komplettes Skript in https://pastebin.com/ und schicke hier den Link. Dann schaue ich es mir gerne mal an.
>>
>> Grüße,
>> Daniel

---

**Bucky2k** – 2022-11-13

> **⭐⭐⭐⭐⭐**
> *Super Start, leider fehlt es noch an ein/zwei Kleinigkeiten bis zum Ziel*
>
> Hi,
>
> nach deiner Anleitung komme ich bis zur Ausführung des bash mit Fehlermeldungen. Als eine erste Anpassung war die SED von: ... | sed -e "s/@/_/) auf  ... | sed -e 's/@/_/') nötig, damit kein Fehlernder quote bemängelt wurde. Aber nun komme ich bis zu dieser Fehlermeldung bei der Ausführung des bash:
>
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 1:
> {
> jq: error: May need parentheses around object key expression at , line 1:
> {
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 2:
>         id          : .MBusData.SlaveInformation.Id,
> jq: error: May need parentheses around object key expression at , line 2:
>         id          : .MBusData.SlaveInformation.Id,
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 3:
>         manufacturer: .MBusData.SlaveInformation.Manufacturer,  
> jq: error: May need parentheses around object key expression at , line 3:
>         manufacturer: .MBusData.SlaveInformation.Manufacturer,  
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 4:
>         medium      : .MBusData.SlaveInformation.Medium,
> jq: error: May need parentheses around object key expression at , line 4:
>         medium      : .MBusData.SlaveInformation.Medium,
> jq: 8 compile errors
> xq: Error running jq: ExpatError: not well-formed (invalid token): line 1, column 0.
> + read ameter
>
>
> Was könnte mir noch zu meinem Glück fehlen?
>
> Danke
>
> Bucky

↳ **the78mole** – 2022-11-13

>> Hi Bucky,
>> bei mir hat tatsächlich das abschließende " gefehlt. In der Shell musst Du aber etwas aufpassen, da sind ' nicht ganz identisch mit ".
>> Versuche es doch bitte nochmal mit sed -e "s/@/_/"
>> Leider kann ich hier in der Antwort keinen Code formatieren... Die Anführungszeichen springen deswegen am Wortanfang nach unten, aber im Artikel ist es jetzt korrekt im Code-Listing drin.
>> Grüße,
>> Daniel (the78mole)

---

**Mariusz** – 2023-02-15

> **⭐⭐⭐⭐⭐**
> *MQTT problem*
>
> Hi
>
> I have a problem with this script:
>
>  Wed 15 Feb 18:02:23 CET 2023
> Sending data to host 192.168.1.151 as user 'mqttbroker' using topic 'mbusmeters/'.
> Getting data from 0025244901061507...  2875 bytes sent
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 1:
> {
> jq: error: May need parentheses around object key expression at , line 1:
> {
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 2:
>         id          : .MBusData.SlaveInformation.Id,
> jq: error: May need parentheses around object key expression at , line 2:
>         id          : .MBusData.SlaveInformation.Id,
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 3:
>         manufacturer: .MBusData.SlaveInformation.Manufacturer,  
> jq: error: May need parentheses around object key expression at , line 3:
>         manufacturer: .MBusData.SlaveInformation.Manufacturer,  
> jq: error: syntax error, unexpected INVALID_CHARACTER (Unix shell quoting issues?) at , line 4:
>         medium      : .MBusData.SlaveInformation.Medium,  
> jq: error: May need parentheses around object key expression at , line 4:
>         medium      : .MBusData.SlaveInformation.Medium,  
> jq: 8 compile errors
> pi@raspberrypi:~/bin $

↳ **the78mole** – 2023-02-15

>> Hi Mariusz,
>>
>> I already andwered this problem in another comment from Bucky (in German)...
>>
>> Try it with: sed -e „s/@/_/“
>>
>> Unfortunately, the quotes here in the comment are low and high. In the script they should both be "
>>
>> Hope this helps.
>>
>> Regards,
>> your mole :-)

---

**Mariusz** – 2023-02-17

> **⭐⭐⭐⭐⭐**
> *Mariusz*
>
> Hi
>
> I was able to run the script that gave me this error replacing ' with " at this point
>
> echo "$METER_DATA" | jq '{
>         id          : .MBusData.SlaveInformation.Id,
>         manufacturer: .MBusData.SlaveInformation.Manufacturer,
>         medium      : .MBusData.SlaveInformation.Medium,
>         records     : .MBusData.DataRecord | length  }'
>
> I don't know if it's correct but it works

↳ **the78mole** – 2023-02-17

>> Hi Mariusz,
>> you mean, the ' after jq?
>> Regards,
>> Daniel

---

**Lucki** – 2026-01-01

> **⭐⭐⭐⭐⭐**
> *Vielen Dank für deine Veröffentlichung :-)*
>
> Hallo Daniel,
>
> folgende Fehlermeldung bekomme ich:
>
> Getting data xxxxxx.../bin/read_send_meters_mqtt.sh: line 23: mbus-serial-request-data-multi-reply: >
> /bin/read_send_meters_mqtt.sh: line 23: xq: command not found
>   1 bytes sent
> /bin/sh: 1: root: not found
>
> Hat du / einer eine Idee??
>
> Vielen Dank vorab......
>
> Gruß Lucki

↳ **the78mole** – 2026-01-01

>> Hallo Lucki,
>> das Problem steht ja im Klartext da, xq ist nicht installiert...
>> Beste Grüße,
>> Daniel

---
