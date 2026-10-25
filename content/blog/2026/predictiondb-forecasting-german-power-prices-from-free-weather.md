---
title: "PredictionDB – Digging for Next Week's Power Price in Free Weather Data"
date: '2026-10-25'
description: 'Tomorrow''s prices are free at 13:00 anyway – a half-built stack that forecasts German load and power prices for the whole coming week, so a battery can plan further than tonight.'
image: /images/blog/2026/10/predictiondb-price-profile-summer.png
categories:
  - Dev
  - Energy
  - Tools
tags:
  - forecasting
  - machine-learning
  - lightgbm
  - noaa-gfs
  - grib2
  - timescaledb
  - day-ahead
  - price-forecast
  - photovoltaics
  - battery-storage
---

<div style="display: flex; justify-content: flex-end; margin: 0 0 1rem;">
  <a href="https://github.com/the78mole/PredictionDB" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none; color: inherit; font-size: 0.9rem; padding: 0.35rem 0.7rem; border: 1px solid #d0d7de; border-radius: 0.5rem;">
    <svg height="18" width="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
    <span>the78mole/PredictionDB</span>
  </a>
</div>

Moles are famously bad at weather. Down in the burrow it's always 9 °C and slightly damp, so when it comes to the sky I have to rely on instruments. And lately the sky has started to matter a lot: whether the next days are sunny or windy decides whether the power price at noon is 12 ct/kWh or −2 ct/kWh, and what my battery should be doing *right now*.

Tomorrow's prices are no secret. The day-ahead auction publishes them every day around 13:00, and SMARD or Energy-Charts show them to anyone for free. But by then half of today's decisions are already made. Should the battery fill up from the roof this morning – or stay half-empty, because tomorrow noon will probably go negative and pay me for charging? Should a big storage hold its energy through a dull Tuesday because Thursday evening looks expensive? A one-day window can't answer that. What you actually want is a rough idea of the **whole coming week**, and you want it in the morning, *before* the auction.

There are services that sell exactly that. They want a contract and a monthly fee. Meanwhile NOAA publishes a global weather model four times a day for free, the German grid operators publish load and generation, and the exchange prices end up on SMARD and Energy-Charts. All the raw material is lying around in the open. So I started digging a tunnel from those piles of free data to a week-ahead forecast of German grid load and power prices.

That tunnel is **PredictionDB**. It isn't finished – there's no public API yet, and the neural networks are still a line in the roadmap. But it already does something useful, and I'll get to that before the end of the post.

## The Goal

Forecast, for Germany (bidding zone DE-LU), using **only free data sources**:

- **Grid load** in Germany, 15 min resolution, up to 16 days ahead
- **Day-ahead price** DE-LU for the delivery days D+1 to D+7, as quantiles (P10/P50/P90) – issued every morning at 08 UTC, before the auction closes; scenarios up to D+14 later
- **Wind, PV and run-of-river generation** as helper targets
- Later: forecasts for your *own* PV, wind or small hydro plant via an API, and heat pump demand and scheduling

The price for D+1 is the least interesting of these, because a few hours later it's known exactly. The forecast earns its keep on the days *after* that, and in the morning hours before 13:00:

| Decision | Needs |
|----------|-------|
| Charge the battery from PV this morning, or keep room for tomorrow's negative noon? | Tomorrow's price shape – before it's published |
| Hold a large storage over a cheap, windy day for an expensive evening later in the week? | D+2 … D+5 |
| Charge the EV once this week – today, or is it worth waiting for the weekend? | Which days are cheap, not just which hours |
| Pre-heat with the heat pump today, or wait for a cheaper day? | D+1 … D+3 |
| How much capacity is worth keeping free at all? | The spread over the coming days |

The whole thing runs as a Docker Compose stack in a VM on my Proxmox box, and it's built so that moving it to the cloud is a configuration change, not a rewrite.

## The Stack

| Layer | Technology |
|-------|-----------|
| Language / tooling | Python 3.12, uv workspace (monorepo), Ruff, mypy, pytest |
| Database | PostgreSQL 17 + TimescaleDB (hypertables with compression) |
| Object storage | Garage (S3 API, single node) |
| Weather | NOAA GFS 0.25°, 384 h, four runs per day, GRIB2 partial downloads |
| Energy data | SMARD, ENTSO-E Transparency, Energy-Charts, ECB, World Bank, Netztransparenz |
| Plant inventory | Marktstammdatenregister (MaStR) full export, quarterly |
| Forecasting | LightGBM, two-stage, quantile loss |
| Monitoring | Grafana, Prometheus, cAdvisor, node-exporter |
| Deployment | GHCR image per green CI run, systemd timer on the VM rolls it out |

## Weather Without Drowning in It

GFS is big. Download every variable of every run at full resolution and you're suddenly running a weather archive instead of a forecasting tool. Storing the grid values as database rows would be even worse – billions of rows for a handful of years.

So the weather pipeline is strictly layered, bronze → silver → gold:

| Tier | Where | What |
|------|-------|------|
| Bronze | S3 bucket `wx-bronze` | Original GRIB2 per forecast step, cropped to 44–58° N / 0–20° E, CCSDS-packed, with a manifest (endpoint, SHA-256, messages, missing variables) |
| Silver | S3 bucket `wx-silver` | One Zarr v3 store per run, Int16 with scale/offset, Blosc/Zstd – about 13 MB per run |
| Gold | TimescaleDB `feat.nwp_value` | Weather features per *plant cluster*, run and valid time |

`wx-ingest` never downloads a whole GRIB file. It reads the `.idx` index, merges the byte ranges of the 22 fields it actually needs (temperature, dew point, wind at 10 m and 100 m, gusts, radiation, clouds, precipitation, snow, soil temperature and moisture, …) and fetches only those via HTTP range requests. If NOMADS hiccups, it falls back to the AWS mirror, then Google. I wrote a small library for this, `gribkit`, instead of using Herbie – I wanted the cropping and re-packing in the same step.

The trick that turns "weather" into "energy" is the gold tier. `mastr-ingest` imports the German plant register every quarter, geolocates every wind turbine and PV array, and clusters them per technology. `wx-process` then computes, for every GFS run, capacity-weighted features per cluster: wind speed extrapolated to hub height, a generic power curve, PV capacity factor with temperature correction, snow on the panels. The model never sees "wind at grid point 52.25° N / 8.5° E" – it sees "expected output of onshore wind cluster c07, weighted by the capacity installed there".

And because the register goes back years, the stack reconstructs the **installed capacity per cluster per day** from commissioning and decommissioning dates. Training on 2019 data with 2026 capacity would be a quietly lying model.

## Two Stages and a Strict "What Did We Know?"

The first model, `de_lu_v1`, is deliberately boring: gradient boosting with LightGBM, trained in two to three minutes on a laptop CPU.

- **Stage 1** forecasts load, onshore wind, offshore wind and PV. Wind and PV are learned as capacity factors and multiplied back by the capacity on the delivery day.
- **Stage 2** forecasts the price, using everything from stage 1 plus its P50 forecasts and the **residual load** derived from them (load minus wind minus PV). The less the renewables cover, the more expensive the power plant that sets the price.

Every target gets three boosters (P10, P50, P90) with pinball loss. Stage 2 is trained on *out-of-fold* stage 1 predictions – otherwise it would learn to trust perfect inputs it will never get in production.

<details>
<summary><strong>Boosters and pinball loss, in two paragraphs</strong> (click to expand)</summary>

A **booster** is what LightGBM calls a trained gradient-boosting model. It's not one big clever tree but a long chain of small, dumb decision trees. The first tree makes a rough guess, the second one is trained only on what the first got wrong, the third on what the first two still got wrong, and so on. Each tree adds a small correction (scaled down by the learning rate, here 0.05), so no single tree can wreck the result. Here each booster is 400 trees with at most 63 leaves each. Sum them up and you get the forecast for one target and one quantile – which is why there are 15 boosters per model version: 5 targets × 3 quantiles.

The **pinball loss** is what tells a booster whether it is supposed to forecast the middle or an edge of the distribution. For a quantile τ, a forecast that ends up too low costs τ × the miss, and a forecast that ends up too high costs (1 − τ) × the miss. For P90 (τ = 0.9), undershooting is expensive and overshooting is cheap. Say the forecast is 120 €/MWh: if the actual price is 150, the loss is 0.9 × 30 = 27; if it's 100, only 0.1 × 20 = 2. The cheapest place for the model to sit is where only 10 % of the actual values land above it – exactly the definition of P90. P10 works the other way round, and for P50 both sides cost the same, which makes it the median (and the loss just half the absolute error). Three boosters with three different τ give you a band instead of a single number – and for a battery, "probably 40, but could be 120" is a very different instruction from a plain 40.

</details>

The part I spent the most time on is leakage. A forecast is issued daily at 08 UTC, before the day-ahead auction closes at noon. Every feature row is built with exactly what was public at that moment:

| Data | Known from |
|------|------------|
| Measured load and generation | end of interval + 2 h |
| Day-ahead price for a delivery day | 13:00 local time on the day before |
| GFS run | `run_time` + 6 h (fully processed) |
| Installed capacity | MaStR snapshot, reconstructed per day |

Every energy value in the database carries a `published` timestamp for exactly this reason. A backtest that peeks into the future looks fantastic and is worth nothing.

## How Good Is It – and How Far Out?

The backtest runs as an expanding window over 2025 to October 2026, against the dumb-but-honest baselines (yesterday's price, last week's load) and the grid operators' own day-ahead forecasts. `de_lu_v2` adds only free data on top of v1 – day-ahead prices of the 14 neighbouring zones, fuel prices with the EUR/USD rate, and self-computed market values.

First the one day where there's something to compare against:

| D+1, same hours 2025 – 10/2026 | Price MAE | Load MAE |
|---|---|---|
| `de_lu_v2/frei` | **26.4 €/MWh** | 1,757 MW |
| `de_lu_v2/frei_niveau` | 27.1 €/MWh | **1,719 MW** |
| `kalender` (v1, no weather) | 28.3 €/MWh | 1,833 MW |
| Yesterday's price | 28.7 €/MWh | – |
| Grid operators' day-ahead load forecast | – | 1,981 MW |

The load forecast beats the TSOs' official one by about 11 %, and the price model beats "tomorrow will be like today" for the first time. That's a useful sanity check, but nobody needs my D+1 price at 14:00. The interesting part is how the forecast holds up further out:

| Price, `de_lu_v2/frei` | D+1 | D+2 | D+3 | D+4 | D+5 | D+6 | D+7 |
|---|---|---|---|---|---|---|---|
| MAE (€/MWh) | 26.4 | 29.4 | 29.7 | 30.1 | 30.1 | 29.9 | 30.2 |
| Rank correlation of the hours within a day | 0.868 | 0.867 | 0.867 | 0.866 | 0.868 | 0.871 | 0.868 |

The error grows by only about 15 % from tomorrow to a week ahead. And the second row is the one a battery cares about: the rank correlation says how well the model gets the *order* of the hours right – which hours of a day are the cheap ones and which the expensive ones. It stays at 0.87 across the whole week. For charging and discharging, the order of the hours matters far more than the exact euro value. The same goes for the EV that only gets plugged in once a week: the question isn't "what will Saturday cost to the cent" but "is Saturday noon clearly cheaper than tonight, or am I waiting for nothing?"

![MAE gain of the v2 feature groups over v1 per lead day, for grid load (left) and day-ahead price (right)](/images/blog/2026/10/predictiondb-v2-mae-gain.png)

Two honest caveats, because a mole that oversells its tunnel ends up in a collapsed one:

- **This is still without weather in the price model.** The forecast above knows calendar, holidays, installed capacity, recent prices, neighbours and fuels – but not whether next Thursday is sunny. The GFS features are only available as gold-tier data from January 2026, too short to train on. Wind and PV for D+3 onwards are exactly what decides whether a day is cheap, so this is the biggest lever left. A short test with half a year of weather already looked promising for D+1 wind (2.4 GW MAE versus 8.3 GW for persistence), but six months of training is not enough to judge it.
- **The quantile bands are too narrow.** P10–P90 contains 66–75 % of the actual values instead of 80 %. Calibrating that is on the list.

One more finding was about *why* v2 got better. Neighbour prices, fuels and market values each improved the price by 4–5 %, but all of them together barely more than each alone. Suspicious. The cross-check: just giving the model a 28-day average of its *own* price – no new source at all – already gets 3.6 %. Most of the gain is a longer price memory, not new information.

## The Part That Is Already Useful

Here's where I stopped digging forward for a moment and dug sideways. Before forecasting prices for a battery, it's worth knowing what a battery can earn from prices at all. Once you have nine years of hourly German day-ahead prices in a clean TimescaleDB, with a training snapshot as three Parquet files, you can answer questions that have nothing to do with forecasting – and that a lot of people are currently guessing about.

**The question:** a 10 kWp PV system (45°, facing south) sells its power at the exchange price. How much more does it earn if a battery shifts the noon output into the expensive evening hours?

The setup is deliberately realistic: the battery doesn't get to know the future. Every day at 13:00, when tomorrow's prices are published, it solves a linear program over the next 35 hours and executes it until 13:00 the following day. PV yield comes from PVGIS (2005–2023) and, for 2024/25, from the German PV feed-in scaled to the same plant. Round-trip efficiency 90 %, no charging from the grid.

First, the reason this question has become interesting at all:

![Average day-ahead price profile April–September for 2019–2025, showing the noon dip deepening to about 1 ct/kWh while evenings stay at 13–14 ct/kWh](/images/blog/2026/10/predictiondb-price-profile-summer.png)

Until 2021 the price was nearly flat across the day. Since 2023, the PV boom pushes summer noon prices down to 1–2 ct/kWh while the evening stays at 13–14 ct. Hours with negative prices went from 143 (2021) to 482 (2025). In 2025, PV power was worth only about half the average price. And that gap is exactly what a battery eats for breakfast:

| Year | Direct feed-in | + 10 kWh / 10 kW | + 20 kWh / 15 kW | + 30 kWh / 15 kW |
|------|---------------|------------------|------------------|------------------|
| 2019 | 382 € | 46 € | 78 € | 100 € |
| 2021 | 758 € | 127 € | 210 € | 261 € |
| 2023 | 769 € | 212 € | 370 € | 478 € |
| 2025 | 546 € | **342 €** | **615 €** | **798 €** |

![Extra revenue of the three battery sizes per year, 2019 to 2025](/images/blog/2026/10/predictiondb-storage-extra-revenue.png)

In 2025 the battery adds 63–146 % on top of what the bare PV system earns at the exchange. Including PV forecast errors and a worse efficiency (85 %), about 290 / 510 / 640 € per year remain. A few things surprised me:

- **For a small home battery, the 13:00 horizon is almost enough.** A 10–30 kWh battery charged only from its own PV earns just 0–2 % more with perfect knowledge of the entire year. It fills up every day and empties in the evening or next morning, so it rarely has to look further. That changes as soon as the storage gets bigger relative to the PV, may charge from the grid (which raises the extra revenue by another 55–85 % in the same analysis), or has to decide *before* 13:00 – and those are exactly the cases the week-ahead forecast is built for.
- **The first 10 kWh are worth the most.** About 34 €/kWh/year, the next 10 kWh 27 €, the third 18 €. Beyond 20 kWh there are too many days without enough cheap noon power to fill it.
- **Location barely matters.** North vs. south Germany changes the yield by −3 to +10 %, the battery's extra revenue hardly at all – it fills up almost every day either way.
- **Break-even:** with realistic numbers averaged over 2023–2025 and 15 years without interest, the battery may cost roughly 350 / 300 / 250 € per kWh installed to pay for itself through shifting alone. With 2025 prices, 430 / 380 / 320 €/kWh.

Here's what one week in June 2025 looks like with the 20 kWh battery – charging in the cheapest noon hours, often during negative prices, and dumping it into the evening peak:

![Example week from 9 June 2025: PV yield, feed-in with battery and state of charge on top, day-ahead price below](/images/blog/2026/10/predictiondb-storage-example-week.png)

A note before anyone forwards this to their installer: this applies to systems that sell at the exchange price – direct marketing, systems out of EEG funding, or new systems under the 2025 *Solarspitzengesetz* that get nothing during negative prices. With a fixed feed-in tariff, shifting earns exactly zero. And self-consumption isn't included; replacing 30+ ct grid power is usually worth more than any arbitrage.

There are two follow-up analyses in the repo: one comparing south vs. east-west vs. east-west plus a south facade for a 19.9 kWp / 50 kWh setup (south wins, even though east-west power has the slightly better market value), and a 2027 scenario where household power at the exchange gets 5 ct more expensive but noon stays at zero. In that scenario the battery's extra revenue nearly doubles – because a battery earns from the *spread*, not the price level. Every analysis is a script plus a README with tables and charts, and each release attaches them as rendered PDFs.

## Small Side Tunnels

A few other things fell out of the data along the way:

- **Is the 6-hours-newer GFS run worth waiting for?** Barely – 2–8 % lower MSE for temperature, wind and radiation, 15–20 % for pressure. But for day-ahead PV it's the difference that matters, because the 06Z run only completes after the auction closes. Using a *partial* run makes it usable in time.
- **Has GFS v16 gotten worse since 2021?** No. Absolute errors went up slightly, but the weather got harder to predict in the same measure (the persistence baseline degraded twice as fast). Only global radiation genuinely improved.
- **Can I compute the official market values myself from free data?** Base and solar: almost exactly. Wind: systematically 3–5 % too high, and the error grows with the number of negative-price hours – most likely because curtailment is handled differently in the TSOs' extrapolation.

## What's Next

Most of the plumbing is in place: GFS ingest with fallbacks and backfill, energy data with source cross-checks, the MaStR clustering, the weather features, training, a model registry with champion/challenger promotion, a prediction service and a Grafana status dashboard. Still on the roadmap:

- The GFS history since 2021 as gold-tier features, so the price model finally sees next week's wind and sun
- Re-running the battery analysis with *forecast* instead of known prices – the real test of what a week-ahead view is worth
- Calibrated quantile bands, a 28-day load level, and `de_lu_v2` running as challenger against the v1 champion
- Partial GFS runs for day-ahead PV
- More weather models (ECMWF open data, ICON, GEFS ensembles) – ensemble spread would make a nice uncertainty feature
- Sequence models (TFT, TiDE) that have to beat LightGBM first
- The FastAPI layer for forecasting your own PV, wind or hydro plant
- Heat, cooling and heat pump scheduling – the weather variables for that are already being collected

The code is on GitHub under the Business Source License 1.1, which allows internal use; check the [license](https://github.com/the78mole/PredictionDB/blob/main/LICENSE) before you build a business on it. The docs are in German, the numbers are in any language.

Back underground now. Somewhere between the GRIB files and next week's price curve there's a forecast that tells my battery on Monday morning what Thursday evening will pay – and I intend to dig until I hit it.
