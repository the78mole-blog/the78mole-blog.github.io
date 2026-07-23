---
title: Hoermoles BlueObscure – Digging a Second Tunnel Into My Own Garage
date: '2026-07-23'
description: How I reverse-engineered the Hörmann BlueSecur BLE protocol out of a .NET MAUI app and ended up opening my garage door from a laptop terminal.
image: /images/blog/2026/07/Hoermann_SupraMatic_E4.jpg
categories:
- Embedded
- Smart Home
- DIY
tags:
- bluetooth
- BLE
- reverse-engineering
- hoermann
- bluesecur
- garage-door
- python
- home-assistant
- bleak
---

Every mole needs a proper entrance to the burrow, and mine got an upgrade: a Hörmann Supramatic Serie 4 mole hole cover drive with Bluetooth. Lovely bit of hardware. It came with an app called **BlueSecur**, a QR-code sticker, and a business model.

The first key – the admin key that pairs your phone with the drive – is free. Every additional "virtual access key" after that costs 9,99 €. And the whole architecture assumes there will always be a phone with an app installed somewhere in the tunnel. My burrow does not work that way. My burrow runs Home Assistant, and eventually it should run a fingerprint reader next to the door, because typing a PIN with muddy paws is a design flaw.

So I did what moles do. I started digging. One evening later, the door was moving on my command.

## The Stack I Had to Get Through

| Layer | What I found |
|---|---|
| APK | `.xapk` split bundle, version 26.1.3 |
| Runtime | .NET MAUI / Xamarin – so the code is **not** in the Smali |
| Payload | 428 .NET assemblies in one undocumented blob |
| Transport | BLE GATT, three sub-protocols on one characteristic |
| Crypto | RSA-2048 for pairing, HMAC-SHA256 for everyday commands |

The first surprise came early. I ran `apktool` over the APK, got a nice pile of Smali, and found… almost nothing. No protocol, no crypto, barely a hint of Bluetooth. That is because the app is .NET, and .NET-for-Android stuffs every assembly into a single file called `libassemblies.arm64-v8a.blob.so`.

That file is an "Assembly Store v2" container. It is internal, undocumented, and starts with the magic bytes `XABA`. I found the actual layout in Microsoft's own `dotnet/android` repository – `AssemblyStoreGenerator.cs` describes header, index and descriptor arrays precisely enough to write a parser. Descriptor table said one thing, the header's `index_size` said another, so I brute-forced the offset backwards from a name table I could already validate. Out came 428 LZ4-compressed assemblies. `ilspycmd` turned the interesting ones back into readable C#.

`2_SAL.dll` was the treasure chamber: the entire `SAL.BlueConnect.*` namespace. The complete Bluetooth protocol, in C#, with the original class and method names intact.

## The Protocol, Briefly

One GATT service, one write characteristic, one notify characteristic. Three different protocols share that single write channel, distinguished by a routing byte at the front of every raw message:

```txt
0x01  Signed        everyday commands, HMAC-signed
0x02  Encrypted     one-time registration, RSA
0x03  BlueControl   a different device profile, unused here
```

Everything is wrapped in `[routing byte][length, LE16][payload]` and chunked into fixed 20-byte pieces – hardcoded, regardless of the negotiated MTU. An everyday command like "move the door" is just:

```txt
[RootId (2)] [Command-ID (2)] [Length (2)] [payload] [HMAC-SHA256 (32)]
```

where the signature covers the frame plus an 8-byte challenge the drive hands out with every notification. Channel 1 is the classic impulse toggle, channel 2 the light, 3 partial opening, 4 and 5 direct open/close, 6 ventilation position. The mapping lives in a per-product table in the app and is identical across the whole Supramatic/Rollmatic/SilentDrive family.

The QR code on the sticker turned out **not** to be an X.509 certificate, despite what everyone (me included) assumed at first glance. It is a bare RSA-2048 public key in SPKI-DER format, Base64-encoded, with a 31-character numeric prefix in front carrying version, product class, serial number and customer ID. Pairing then works like this: I generate 32 random bytes, encrypt them with that public key (PKCS#1 v1.5, *not* OAEP), and send them over. The drive answers with 32 bytes of its own, and the real root key is the **XOR of both**. A neat little one-time-pad handshake where my random bytes only ever served as transport protection for the device's.

## Where I Wasted the Most Time

Two places, and neither was the protocol.

**Timing.** My first registration attempts died mid-transfer, so I did the obvious thing and slowed the transmission down. With a 150 ms pause between chunks the connection dropped after the *first* chunk. With 20 ms it survived about four. With no pause at all, all 16 chunks arrived cleanly. It is not a rate limit – it is a fixed time window of maybe 100–150 ms in which the entire message has to land. Sending politely was the problem.

**The actual wall.** For most of the evening the drive accepted all 13 packets of my pairing message and then said absolutely nothing. No ack, no error code, just a quiet disconnect. I reviewed the entire decompiled call chain from ViewModel down to the byte writes and found *zero* discrepancies with my implementation. The protocol had been correct the whole time.

The answer was hiding in `DevicesService.TeachNewDeviceAsync`. Before every pairing attempt, the real app checks an `AdminTeached` bit that the drive broadcasts in its BLE advertisement, and refuses to even try if it is set. My tool had no such guard – it was cheerfully sending pairing requests to a drive that already had an admin. Namely my own phone, with the official app, still working perfectly. The drive had been ignoring me correctly and silently the entire time.

Cue menu 19, parameter 02 – which clears all Bluetooth pairings and nothing else. The drive keeps its limit positions, its forces, its whole personality; it just forgets every key it ever handed out, including my phone's, and goes back to "first one to pair becomes admin". Which failed twice, because the PRG button has to be **held for five seconds** to confirm. Press it briefly and the menu hops back to 19 looking exactly like success, having cleared precisely nothing. Third time, held until the fast blinking started, and it actually took.

**The next pairing attempt worked on the first try.** A real root key, issued by real hardware, stored in a real (and thoroughly gitignored) JSON file.

Then I typed:

```bash
hoermoles-ble exec --address XX:XX:XX:XX:XX:XX impulse
```

…and from the other side of the wall, my garage door started moving.

## What Exists Now

The result is [`hoermoles-ble`](https://github.com/the78mole/hoermoles-ble), MIT-licensed: a Python library plus a CLI wrapper.

```bash
hoermoles-ble scan
hoermoles-ble save-qr "<qr code content>"
hoermoles-ble register --address <mac>
hoermoles-ble exec --address <mac> open|close|impulse|light|partial|ventilation
```

The core module `protocol.py` is deliberately dependency-free – pure byte logic, no crypto library, no BLE stack. It is meant as a template for ports to C, C++ and TypeScript, because the fingerprint reader at the burrow entrance is not going to run Python.

One deliberate boundary: this project is about interoperability with hardware I own, not about getting around anyone's price list. The key-sharing paywall is enforced entirely client-side against in-app purchases, and the cloud key exchange needs no account at all – both of which I found and then walked away from. A second admin key can be derived locally over BLE without ever touching Hörmann's servers, and if I ever need one, that is the route I will take.

## What's Next

The obvious gap is the interface. A CLI is fine for a mole with a terminal, but not for the Molewife standing in the rain. So the next dig is **Hoermoles BlueObscure** – a single-page web app, honestly named after the thing it clones, doing over Web Bluetooth what the original does over a store listing. After that: the Home Assistant integration, and eventually those ports of `protocol.py` down to bare metal.

The tunnel is dug. Now it needs a door handle.
