---
title: "Par14a-Database – 754 Price Sheets, One SQLite File"
date: '2026-10-26'
description: 'What does my grid operator really charge a heat pump or wallbox under §14a EnWG? I dug through the price sheets of all 754 German distribution grid operators and turned them into one queryable database.'
image: /images/blog/2026/10/par14a-database-title.jpeg
categories:
  - Energy
  - Dev
  - Tools
tags:
  - par14a
  - enwg
  - grid-fees
  - heat-pump
  - wallbox
  - battery-storage
  - smart-meter
  - sqlite
  - web-scraping
  - open-data
---

<div style="display: flex; justify-content: flex-end; margin: 0 0 1rem;">
  <a href="https://github.com/the78mole/Par14a-Database" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none; color: inherit; font-size: 0.9rem; padding: 0.35rem 0.7rem; border: 1px solid #d0d7de; border-radius: 0.5rem;">
    <svg height="18" width="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
    <span>the78mole/Par14a-Database</span>
  </a>
</div>

A heat pump, a wallbox and a home battery walk into a burrow. The grid operator says: "You three may be dimmed when the grid gets tight – and in return you pay less." Fair deal. The obvious follow-up question is *how much* less, and that is where the fun ends. Germany doesn't have one grid operator. It has **754** distribution system operators (DSOs), and each of them publishes its own price sheet – as a PDF, somewhere on its website, in its own layout, sometimes as a scanned image, sometimes behind a bot wall.

In the [last post](/blog/2026/predictiondb-forecasting-german-power-prices-from-free-weather) I dug for next week's power price. But for a heat pump or a wallbox, the energy price is only half the bill – the grid fee is often the bigger lever. And for §14a devices there are three different ways to pay it, plus time windows that change by quarter. Comparing that across operators by clicking through PDFs is a job for a very patient mole. I am not that mole. So I built a database instead.

## §14a in One Paragraph

Since 1 January 2024, new *controllable consumption devices* (steuerbare Verbrauchseinrichtungen) – heat pumps, wallboxes, home batteries, larger air conditioners – fall under §14a of the German Energy Industry Act (EnWG). The grid operator may throttle them down to 4.2 kW when the local grid is congested. In exchange, the Federal Network Agency's determination BK8-22/010-A grants a reduced grid fee, in one of three flavours:

| Module | What you get | Catch |
|--------|-------------|-------|
| **Module 1** | Fixed annual reduction in €/a on the household connection | – |
| **Module 2** | 60 % off the energy part of the grid fee | Needs a separate meter for the device |
| **Module 3** | Time-variable grid fee: high (HT), standard (ST) and low (NT) tariff stages | Only together with Module 1, needs a smart meter |

Modules 1 and 2 are simple numbers. Module 3 is where it gets interesting: every DSO picks its own HT and NT windows, its own prices within a corridor, and the quarters in which the whole thing is active at all.

## What's in the Database

[Par14a-Database](https://github.com/the78mole/Par14a-Database) collects, per DSO and year:

- the standard grid fee (low voltage, no power metering) as reference
- Module 1 reduction, Module 2 base and energy price
- Module 3 HT/ST/NT prices, the active quarters, and every single time window
- a link to the price sheet PDF, the page that links to it, the PDF's SHA-256 and the page number where the §14a section lives
- the smart meter rollout quota of the metering operator, from the Federal Network Agency's list

The master data – all 754 DSOs with name, BDEW code, address and voltage levels – comes from [vnbdigital.de](https://www.vnbdigital.de) via my small [vnbdigital-client](https://github.com/the78mole/vnbdigital-client).

At the time of writing:

| Year | Covered | Status |
|------|---------|--------|
| 2026 | **729 of 754** (97 %) | 714 final, 15 preliminary |
| 2027 | **489 of 754** (65 %) | almost all preliminary – the final sheets arrive around December |

The data lives as plain CSV in the repo, so every change is a reviewable diff. On each push, GitHub Actions builds one SQLite file per year and attaches it to a release (`daten-2026`, `daten-2027`), and a second workflow publishes a small static query page.

## The Web Page

If you just want to know what *your* operator charges, there's no need to touch SQL. The [query page](https://the78mole.github.io/Par14a-Database/) lets you search by operator, postcode or town, switch the year, and toggle gross prices including 19 % VAT. The detail view shows all three modules, the Module 3 windows per quarter as a little timeline, and links straight to the source PDF.

![Detail view of the query page for enercity Netz GmbH 2026: standard grid fee, Module 1 reduction of 131.28 €/a, Module 2 at 3.42 ct/kWh, Module 3 with HT 13.35, ST 8.54 and NT 0.86 ct/kWh, plus HT and NT windows per quarter and the smart meter rollout quota](/images/blog/2026/10/par14a-web-detail.png)

Taking Hannover as an example: a heat pump using 4,000 kWh a year on Module 2 saves (8.54 − 3.42) ct × 4,000 kWh ≈ 205 € net per year on the grid fee – minus whatever the second meter costs. Module 1 would give a flat 131.28 €, and with Module 3 on top, every kWh the heat pump shifts into the night pays 0.86 instead of 8.54 ct. Which one wins depends on how much the device consumes and how flexible it is – but at least now you can do the maths without hunting for the PDF.

## How to Read 754 PDFs Without Going Blind

Price sheets are made for humans with a printer, not for machines. There is no common format. Some list §14a on page 3, some on page 31. Some write "Modul 3", others "zeitvariables Netzentgelt", "Hochlasttarif", "Tarifstufe" or "Niedertarif". Some are scanned images. The pipeline is therefore deliberately *semi*-automatic:

1. **Crawl.** `find_preisblatt.py` starts at the operator's stored grid-fee page (or its homepage), follows links containing words like *Netzentgelte*, *Preisblatt* or *Veröffentlichungen* breadth-first on the same host, downloads candidate PDFs and searches them for §14a content. Text, year, page numbers and hash land in a cache.
2. **OCR where needed.** Pages without a text layer go through `pdftoppm` and Tesseract.
3. **Propose.** `vorschlag.py` hunts for the numbers – with a trick (see below).
4. **Time windows.** `fenster.py` heuristically extracts HT/NT windows and active quarters, and only marks them as *safe* if HT and NT were both found, don't overlap and the quarters were stated explicitly.
5. **Look at it.** `ausschnitt.py` cuts the Module 3 section out of each proposed PDF and tiles several operators into one review image. A human (or a mole with glasses) checks it before `uebernehmen.py` writes the values into the CSV.

### The Trick: Module 1 Is a Formula

Finding "the right number" in a PDF full of tables is the hard part. Luckily, the regulator made Modules 1 and 2 depend on a single value: the standard energy price *AP* for low voltage without power metering.

```text
Module 1 = 80 € gross (= 67.23 € net) + 3,750 kWh × AP × 20 %
         = 67.23 € + 7.5 × AP[ct/kWh]

Module 2 = 40 % × AP
```

So `vorschlag.py` doesn't look for one number, it looks for a **triple** (AP, M1, M2) that satisfies both equations. A random table cell might look like a price; three numbers that fit the formula almost certainly *are* the price sheet. Module 3 prices are then searched inside the corridors the regulation allows: HT between AP and 2 × AP, NT between 10 % and 40 % of AP.

![Scatter plot of Module 1 reduction against standard energy price for 729 German grid operators in 2026: 707 points lie exactly on the line 67.23 € + 7.5 × AP, 22 lie off it](/images/blog/2026/10/par14a-module1-formula.png)

For 2026, 707 of 729 operators sit exactly on that line. The 22 that don't are exactly the sheets I look at twice.

### The Bot Wall

The Energy Industry Act obliges grid operators to publish their grid fees on the internet. For about two dozen of them, "published" means: visible in a full browser that passes a JavaScript check, and `HTTP 403` for everything else – including screen readers and download tools without JavaScript. Several of the big ones are on that list. I didn't try to work around it; those sheets were read manually in a browser, and the repo keeps a [list of these access barriers](https://github.com/the78mole/Par14a-Database/blob/main/ZUGANGSBARRIEREN.md) with the type of block and whether it also happens from a private DSL line. Machine-readable publication obligations would be a nice idea for the next amendment.

## A Few Things the Data Says

Now for the fun part – what comes out once 729 price sheets sit in one table. All prices net, 2026:

| | min | average | max |
|--|----:|----:|----:|
| Standard energy price AP (ct/kWh) | 2.22 | 7.35 | 17.39 |
| Module 1 reduction (€/a) | 83.88 | 122.35 | 206.05 |
| Module 3 NT (ct/kWh) | 0.32 | 2.22 | 6.96 |
| Module 3 HT (ct/kWh) | 2.71 | 10.67 | 25.19 |

On average HT costs almost six times as much as NT – a spread of about 8.5 ct/kWh that a heat pump with a buffer tank or a car standing in the driveway overnight can actually use.

The more interesting question is *when* those stages apply. Here's every Module 3 window of Q1 2026, stacked across 676 operators:

![Stacked chart of the share of German grid operators applying NT, ST or HT for each quarter-hour of the day in Q1 2026: NT dominates from midnight to 6:00, HT peaks between 17:00 and 19:00 at almost 90 %, a smaller HT bump around noon, and roughly 10 % of operators have NT around midday](/images/blog/2026/10/par14a-module3-q1-2026.png)

- **The night is cheap.** From midnight to 6:00, up to nine out of ten operators are in NT.
- **The evening is expensive.** Between 17:00 and 19:00 almost everyone is in HT – that's when Germany cooks dinner and plugs in the car.
- **Noon is contested.** Up to 40 % of operators put an HT window around midday, while about one in ten already uses NT there to soak up solar peaks. In Q2, 69 operators have NT across 12:00–13:00.
- **Quarters matter.** 410 operators only activate Module 3 in Q1 and Q4, 259 run it all year. If you plan your heat pump around summer NT windows, check the quarters first.

### Winter Is Coming – Module 3 Isn't (Everywhere)

For a heat pump, the winter quarters are the ones that count: Q1 (January to March) and Q4 (October to December) are when it actually runs. Most operators agree – but not all of them. In 2026:

| Module 3 in winter | Operators |
|--------------------|----------:|
| Active in both Q1 and Q4 | 673 |
| Only in one of the two winter quarters | 17 |
| **Summer only (Q2 and Q3), no winter at all** | **31** |
| Quarters not stated on the price sheet | 8 |

So 45 operators have no time-variable grid fee from January to March, 34 have none from October to December, and 31 skip winter entirely. These aren't just tiny village utilities either: Bayernwerk Netz, Westfalen Weser Netz, Netze ODR and naturenergie netze are among the summer-only crowd. Their logic is the grid's, not the heat pump's – they use Module 3 to pull consumption into the solar midday hours, which only works when there's sun to pull from. The preliminary 2027 sheets look much the same: 19 of 489 operators are summer-only so far.

Which brings me to some advice from someone who has dug a few burrows. Before you choose where to dig yours, check what the local grid operator does in winter. Moles are careful about soil, drainage and how close the nearest earthworm colony is – but I've never met one who checked the §14a price sheet first, and that's a mistake. You can tunnel through clay, install a shiny heat pump with a buffer tank big enough to heat the whole underground, write a scheduler that knows every NT window to the quarter-hour – and then find out in November that your operator's Module 3 has gone into hibernation until April. Your heat pump will be awake all winter. The cheap tariff won't. Moving a burrow is a lot of digging; looking up an operator in the [query page](https://the78mole.github.io/Par14a-Database/) takes ten seconds.

From 2026 to 2027 (preliminary, 486 operators in both years), the standard energy price rises by only 0.17 ct/kWh on average – and 180 operators actually get cheaper.

And the smart meter column: Module 3 requires one, so the rollout quota matters. As of 30 June 2026, 402 of 729 operators had reached the 20 % mandatory rollout target. If yours is not among them, Module 3 may stay theory for a while.

## Query It Yourself

Grab a release and ask your own questions:

```bash
curl -LO https://github.com/the78mole/Par14a-Database/releases/download/daten-2026/par14a_2026.sqlite
```

Which operators offer NT across lunchtime in Q2, cheapest first?

```sql
SELECT v.name, z.von, z.bis, p.m3_nt_ct_kwh
FROM m3_zeitfenster z
JOIN vnb v USING (vnb_id)
JOIN preisblatt p USING (vnb_id, jahr)
WHERE z.quartal = 2
  AND z.stufe = 'NT'
  AND z.von <= '12:00' AND z.bis >= '13:00'
ORDER BY p.m3_nt_ct_kwh
LIMIT 5;
```

```text
Stadtwerke Neumarkt i.d.OPf. Energie GmbH | 10:00 | 15:00 | 0.39
LEW Verteilnetz GmbH                      | 10:00 | 15:00 | 0.41
Markt Zellingen                           | 10:00 | 15:00 | 0.45
Bayernwerk Netz GmbH                      | 10:00 | 15:00 | 0.47
ÜZ Mainfranken eG                         | 12:00 | 14:00 | 0.54
```

The schema is in [`schema.sql`](https://github.com/the78mole/Par14a-Database/blob/main/schema.sql): tables `vnb`, `preisblatt`, `m3_zeitfenster` (one row per quarter, stage and window) and `rollout_quote`. Column names are German, the numbers are not.

## What's Next

- **2027 final sheets.** Most 2027 entries are preliminary; the final versions should show up towards December, and the stored grid-fee page plus the PDF hash make it easy to spot what changed.
- **The last 25 for 2026.** Mostly small operators without a findable §14a sheet – the repo lists them with reasons.
- **Feeding PredictionDB.** With the time windows in a table, the grid fee becomes just another price curve that a battery or heat pump scheduler can optimise against.

Found a missing or newer price sheet? There's an [issue form](https://github.com/the78mole/Par14a-Database/issues/new?template=preisblatt.yml) for that – the PDF, its download link and the page it's linked from are all I need.

Back into the tunnel. 754 operators, one table, and at least one fewer reason to open a PDF.
