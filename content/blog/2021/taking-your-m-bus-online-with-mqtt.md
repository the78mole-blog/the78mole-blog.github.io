---
title: Taking Your M-Bus To The Next Level... MQTT
date: '2021-07-06'
description: ''
categories:
- Bus Systems
- M-Bus
- Networking
- Smart Home
tags: []
image: /images/blog/2021/07/HASS-MBUS-MQTT-1.png
---

## Introduction

First of all, why would you do this? Many people own an appartment and want to measure the heat, water, electricity flow to the people living there. Others just want to measure their own consumption a bit more in detail than with their annual bill or writing the numbers down manually. M-Bus is quite a nice bus since it is mostly open source, based on simple serial protocols, supplies your meters (if needed) and there exist quite some cheap interface circuits for it for building it on your own or just buy some USB-mBus-Adapter from [aliexpress](https://de.aliexpress.com/item/32990900096.html) (this is what I did in the end).

![](/images/blog/2021/07/WaveTopSign-MBUS-zu-USB-Master-Modul-1.png)

USB-M-Bus-Adapter

![](https://lh3.googleusercontent.com/3wE5bzMs3WN_Dp9FQeggCtfNXZBiPT3IGM-15-XhVYBxarI0WZOPbAQmeS3NktQgKFXPGIbs3_5rK-X5ecLpWf3vlxUE4JEPXYTezoWuGyE52VuozAQuiiRrji2qH93Lawih11wl0tBhmTlRyaMNmhqBTrmY3_S02YXswrBIzca3-GXBpuj00v-SEL4MrrBlERKLcxYVEfMKB3jareOcOisEIzWUnecjoCwhT3MgyLiXQBH2TV9FoFoNW7WUYOucTFmwfBXHVIUouaGN4mANNZ5zGWNk-ylfchNf-7GsczzFEBNch9TxIjCr3-ExCcPpxiNfrXRzznOoUfl7HUCVJ36VJfQDiHIIFmq3aBmZB8ikj9wkz4z14BywWU0mqZW1DtaOiDeZbQxnOPE1n1XYhXVvgr_HQ-fnvJ9ed7gR5nerJQ-TUhBI0_4aOmRXUApFQyuT6lQEulP2o_t3yBSF2E7lvp1vHuvFAVEHEbNEfKzdt_N20E3qovCmFOlvz5BrYprDPlAgYaNfssLmxdLR23t_dKUMVMEahNj9Sk9sdO4YAiTEeD_vKL1df_IKmxfDL2WNO62QaUZWixXZnj4cm5qSWQIIvDCcspN6kFsX3CHQni3OqerSzLv7Jpn9yLR_P12cP7oxFjXpAJnqrgipQ0h_xGo2QypHu4fYqRJ_2x9GIPhNO8ptH1H_PMZNqCUX2S18NBLcdGCkanwr37RbEpdk=w1685-h948-no?authuser=0)

M-Bus Heat Meter

BTW: To connect my wmBus meters, I used [wmbusmeters](https://github.com/weetmuts/wmbusmeters) from GitHub and also contributed my two Aventies meters (Cold Water Flow and Heat Cost Allocators). You can find the wmbus post [here](https://the78mole.de/wmbus-meters-and-how-to-get-it-into-home-assistant/).

## Prerequisites

One descision you should make in advance is, where to store all this data and how to store it most efficiently. In my case, I have some Home Assistant running. Before I used iobroker and it was easy to connect the adapter with the mbus adapter, but iobroker somehow got crashing over and over... Nevertheless, influxDB is always a good choice to store measument data. Home Assistent and iobroker use different schemas in influx, but they both keep stuff well arranged. This makes it quite easy to analyze or consume your data with Grafana, node-red or python.

To transfer the data of a non-standard-integration, it is always best to use a rock solid network protocol, even if the deamon collecting the data is running on the same machine. In my case I decided to use MQTT as the transport and collect it with Home Assistant MQTT client. But first steps first...

Another thing to do is, to add your user to the dialup group, to be able to access serial devices. Also check, if /dev/ttyUSB0 is owned by the dialup group and has write access.

## M-Bus Reader Software

To read out the mbus, you need some software that understands the M-Bus protocol and can help with addressing. For this purpose, there is some quite old (but rock solid) implementation called [libmbus](https://github.com/rscada/libmbus). This is mainly written to be used as a library for your own software, but it includes some basic command line tools, that server quite well for my purpose, at least for initial bring-up of my network.

Here are the commands to get, compile and install it (best run as user):

```bash
pi@garagepi:~/GIT/libmbus $ git clone https://github.com/rscada/libmbus.git
pi@garagepi:~/GIT/libmbus $ cd libmbus
pi@garagepi:~/GIT/libmbus $ ./build.sh  # Maybe not necessary
pi@garagepi:~/GIT/libmbus $ ./configure
pi@garagepi:~/GIT/libmbus $ make -j4
pi@garagepi:~/GIT/libmbus $ sudo make install
pi@garagepi:~/GIT/libmbus $ sudo ldconfig
```

If you did not see errors, that's all to get started. Now let's test the net...

#### Alternative to libmbus

Some people reported problems with libmbus... So you could try an alternative using python: [pyMeterBus](https://gitlab.com/ganehag/pyMeterBus)

It does not support the full feature set of M-Bus (e.g. Extended VIF codes), but it could help debugging problems with libmbus.

## Searching for meters

For meters to be found, you need to know the appropriate baud rate. In my case the meters talk with 2400 Baud, so you need to provide this to the mbus-serial-scan or mbus serial-scan-secondary. Nowadays, it totally makes sense, to use secondary addressing. Some meters can be configured to have a primary address, using their secondary address for configuration, but the data rate usually needed is so low, that also secondary addressing is way enough. If you are really interested in how to configure the primary address, let me know and I'll find out and extend this post.

```bash
pi@garagepi:~ $ mbus-serial-scan -b 2400 /dev/ttyUSB0 
Collision at address 0
Found a M-Bus device at address 110
pi@garagepi:~ $ mbus-serial-scan-secondary -b 2400 /dev/ttyUSB0
Found a device on secondary address 0000873987050402 
Found a device on secondary address 10223908496A8804 
Found a device on secondary address 35001739496A8804 
Found a device on secondary address 35001740496A8804 
```

As you can see, the primary addresses have collisions, since most M-Bus meters a factory set to address 0. Therefore, you should prefer secondary addressing where every meter has it's unique address.

If you cannot find anything, it totally makes sense to measure the voltage between the two bus lines of the M-Bus. These should show something around 30V and should be stable. If data gets transfered, the voltage will drop a bit and also looks a bit unstable on a standard multimeter until the transfer is finished.

## Getting The Data of Some Meters

As an example, I will show, how to get the data from my electricity meter 0000873987050402 (which I use for my electric car's wall-box since a few weeks).

```bash
pi@garagepi:~/GIT/libmbus $ mbus-serial-request-data -b 2400 /dev/ttyUSB0 0000873987050402
<?xml version="1.0" encoding="ISO-8859-1"?>
<MBusData>
    <SlaveInformation>
        <Id>8739</Id>
        <Manufacturer>ALG</Manufacturer>
        <Version>4</Version>
        <ProductName></ProductName>
        <Medium>Electricity</Medium>
        <AccessNumber>2</AccessNumber>
        <Status>00</Status>
        <Signature>0000</Signature>
    </SlaveInformation>
[...]
    <DataRecord id="16">
        <Function>Instantaneous value</Function>
        <StorageNumber>0</StorageNumber>
        <Tariff>0</Tariff>
        <Device>0</Device>
        <Unit>Manufacturer specific</Unit>
        <Value>0</Value>
        <Timestamp>2021-07-06T12:44:20Z</Timestamp>
    </DataRecord>

    <DataRecord id="17">
        <Function>More records follow</Function>
        <Value></Value>
        <Timestamp>2021-07-06T12:44:20Z</Timestamp>
    </DataRecord>
</MBusData>
```

This already looks fine, but we better could use it, if it is JSON... You could use some XSLT to build your own individual converter, but this would be like taking a nut to crack a sledgehammer. Luckily, there is already a tool for this...: xq (part of yq, using jq) from pyhton pip. We also install mosquitto-clients, since we need it later. To install it, do the following:

```bash
pi@garagepi:~/GIT/libmbus $ sudo apt install mosquitto-clients jq python3-pip
pi@garagepi:~/GIT/libmbus $ sudo pip3 install yq
pi@garagepi:~/GIT/libmbus $ mbus-serial-request-data -b 2400 /dev/ttyUSB0 0000873987050402 | xq .
pi@garagepi:~ $ mbus-serial-request-data -b 2400 /dev/ttyUSB0 0000873987050402 | xq .
 {
   "MBusData": {
     "SlaveInformation": {
       "Id": "8739",
       "Manufacturer": "ALG",
       "Version": "4",
       "ProductName": null,
       "Medium": "Electricity",
       "AccessNumber": "5",
       "Status": "00",
       "Signature": "0000"
     },
     "DataRecord": [
       {
         "@id": "0",
         "Function": "Instantaneous value",
         "StorageNumber": "0",
         "Tariff": "1",
         "Device": "2",
         "Unit": "Manufacturer specific",
         "Value": "1800",
         "Timestamp": "2021-07-06T13:09:09Z"
       },
[...]
      {
        "@id": "16",
        "Function": "Instantaneous value",
        "StorageNumber": "0",
        "Tariff": "1",
        "Device": "0",
        "Unit": "Manufacturer specific",
        "Value": "1707949",
        "Timestamp": "2021-07-06T13:09:09Z"
      },
      {
        "@id": "17",
        "Function": "More records follow",
        "Value": null,
        "Timestamp": "2021-07-06T13:09:09Z"
      }
    ]
  }
}
```

This already looks nice to be transferred to Home Assistant or whatever you want. For the transfer to start in regular intervals, simply create a cronjob and execute a script for all meters to be transferred.

```bash
pi@garagepi:~ $ mkdir bin
pi@garagepi:~ $ cd bin
pi@garagepi:~/bin $ touch read_send_meters_mqtt.sh
pi@garagepi:~/bin $ chmod u+x read_send_meters_mqtt.sh
pi@garagepi:~/bin $ vi read_send_meters_mqtt.sh
```

Now paste the following content into the file, edit it to your needs and you can run it.

```bash
#!/bin/bash

ADDRESS_FILE=~/addresses.txt
BAUDRATE=2400
DEVICE=/dev/ttyUSB0
MQTT_HOST=172.22.2.137
MQTT_USER=mqtt
MQTT_PASS=leonardo
MQTT_TOPIC=mbusmeters

if [ ! -f $ADDRESS_FILE ]; then
    mbus-serial-scan-secondary -b $BAUDRATE $DEVICE \
        | sed -e 's/^.*y address \(\+\) .*$/\1/' > $ADDRESS_FILE
fi

echo -e "\n $(date)"
echo "Sending data to host $MQTT_HOST as user '$MQTT_USER' using topic '$MQTT_TOPIC/'."

while read ameter
do
    echo -n "Getting data from $ameter..."
    # The sed is for replacing the @ with _ to be able to match on it in HASS templates
    METER_DATA=$(mbus-serial-request-data-multi-reply -b $BAUDRATE $DEVICE $ameter | xq . | sed -e "s/@/_/")
    /usr/bin/mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS \
        -t $MQTT_TOPIC/$ameter -m "${METER_DATA}"
    BYTCNT=$(echo "$METER_DATA" | wc -c)
    echo "  $BYTCNT bytes sent"
    echo "$METER_DATA" | jq '{ \
        id          : .MBusData.SlaveInformation.Id, \
        manufacturer: .MBusData.SlaveInformation.Manufacturer, \
        medium      : .MBusData.SlaveInformation.Medium, \
        records     : .MBusData.DataRecord | length  }'
done < <(cat $ADDRESS_FILE)
```

It will create an address.txt file with all meters found. If you added or removed meters, just delete the address.txt and it will be created again.

Here is, what it will output:

![](/images/blog/2021/07/image-1.png)

The data will be published on MQTT. But be aware, some brokers and debug tools (e.g. [MQTT-Explorer](https://github.com/thomasnordquist/MQTT-Explorer)) have limited message sizes. With `mosquitto_sub -t ...` you can always watch the real data. Took me a few minutes to figure out, is was a limitation of MQTT-Explorer.

## Making It Work Autonomously

I decided to fetch the data every 5 minutes. Therefore I installed a crontab by executing `crontab -e` and putting in the following lines:

```bash
PATH=$PATH:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
*/5 * * * *   cd /home/pi && bin/read_send_meters_mqtt.sh >>log/mbus_mqtt.log
```

## Adding It To Home Assistant

Making it work in Home Assistant simply requires to add the following lines to sensors.yaml (or below sensors in configuration.yaml when using a monolythic config):

```yaml
#####################
# MQTT M-Bus meters #
#####################
- platform: mqtt
  name: "Heat Outlet Hot Water"
  unique_id: mbusmeters.10223908496A8804
  state_topic: "mbusmeters/10223908496A8804"
  unit_of_measurement: "kWh"
  value_template: >
    {%- for rec in value_json.MBusData.DataRecord -%}
    {%- if ( 
            ( rec.Function == "Instantaneous value" )
       and  ( rec.StorageNumber == "0" )
       and  ( "kWh" in rec.Unit )
          ) -%}
    {{ rec.Value }}
    {% endif -%}
    {% endfor -%} 
```

If you want all data from your Electric Meter put into the attributes of the Sensor, this is how it works for algodue meters (with Unit, Tariff and Device elements in some objects).

```
- platform: mqtt
  name: "EM Garage ENERGY_COUNTER"
  unique_id: mbusmeters.0000873987050402
  state_topic: "mbusmeters/0000873987050402"
  unit_of_measurement: "kWh"
  value_template: >
    {%- for rec in value_json.MBusData.DataRecord -%}
    {%- if ( 
             ( rec.Function == "Instantaneous value" )
        and  ( rec.StorageNumber == "0" )
        and  ( rec._id == "34" )
        and  ( "Wh" in rec.Unit )
           ) -%}
    {{ rec.Value | float / 10000.0 | round(2) }}
    {% endif -%}
    {% endfor -%}
  json_attributes_topic: "mbusmeters/0000873987050402"
  json_attributes_template: |-
    {
      {% for mbd in value_json.MBusData.SlaveInformation -%}
        "{{ mbd | lower }}" : "{{ value_json.MBusData.SlaveInformation }}",
      {% endfor -%}
      {%- for drec in value_json.MBusData.DataRecord %}
        {%- if not drec.Function == "More records follow" %}
      "{{ drec.Function | replace(' ','_') }}_
          {%- if drec.Unit is defined -%}
    {{ drec.Unit | replace(' ','_') }}_
          {%- endif -%}
          {%- if drec.StorageNumber is defined -%}
    {{ drec.StorageNumber }}_
          {%- endif -%}
          {%- if drec.Tariff is defined -%}
    {{ drec.Tariff }}_
          {%- endif -%}
          {%- if drec.Device is defined -%}
    {{ drec.Device }}_
          {%- endif -%}
    {{ drec._id }}" : "{{ drec.Value }}"
          {%- if not loop.last -%}
    ,
          {%- endif -%}
        {%- endif -%}
      {% endfor %}
    }
```

And this is, how it looks like in Home Assistant algodue electricity meter:

![](/images/blog/2021/10/image.png)

aventies water meter:

![](/images/blog/2021/10/image-1.png)

zenner heat outlet:

![](/images/blog/2021/10/image-5.png)

This config only captures the instant counter value. I will soon add the config to add the history values as attributes and also add the other values like power, temperature/voltage, flow/current,... Stay tuned.

For the [Zenner](https://zenner.de/) Zelsius C5 heat outlet meters, I even have a few more detailed documents, kindly provided by the manufacturer:

[zelsius\_C5\_ZR\_MBus\_Variables\_de](https://the78mole.de/wp-content/uploads/2021/07/zelsius_C5_ZR_MBus_Variables_de.pdf)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/07/zelsius_C5_ZR_MBus_Variables_de.pdf)

[C5 Voll Parameterliste HZ](https://the78mole.de/wp-content/uploads/2021/07/C5-Voll-Parameterliste-HZ.pdf)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/07/C5-Voll-Parameterliste-HZ.pdf)

Also [algodue](http://www.algodue.com/) provided some information about their energy counter:

[Algodue UEM80-D Manual](https://the78mole.de/wp-content/uploads/2021/07/MPIC00129R02_UEC80-UEM80_MULTILINGUA.pdf)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/07/MPIC00129R02_UEC80-UEM80_MULTILINGUA.pdf)

[M-BUS-protocol\_User-manual-v009\_E](https://the78mole.de/wp-content/uploads/2021/07/M-BUS-protocol_User-manual-v009_E.pdf)[Herunterladen](https://the78mole.de/wp-content/uploads/2021/07/M-BUS-protocol_User-manual-v009_E.pdf)

## Troubleshooting

If you experience problem with the script, try the following:

1. Try running the `mbus-serial-request-data-multi-reply` command on the command line
2. Delete the addresses.txt (it's only a cache to speed up the readings)
3. Check if the script has execution permissions
4. Change the shebang (first line of script) to `#!/bin/bash -x` to get addidtional output, what is executed and if it is the same as the working command from (1), if it is not executed at all, it could not find any meters on the bus or your addresses.txt is empty

If this still does not help, write me an Email.

Have fun!

## Tell Me What You Think About This Article

## Latest Reviews
