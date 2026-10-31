---
title: "PredictionDB – A Shop Window, a Filing Cabinet and 96 GB of Index Cards"
date: '2026-10-31'
description: 'The mole puts its week-ahead power price forecast on the surface for everyone, writes 110 software requirements without being forced to, and finds out that the index of its storage is bigger than the raw data.'
image: /images/blog/2026/10/predictiondb-shop-window-and-paperwork.jpeg
categories:
  - Dev
  - Energy
  - Tools
tags:
  - forecasting
  - grafana
  - requirements-engineering
  - strictdoc
  - gefs
  - timescaledb
  - garage
  - price-forecast
---

<div style="display: flex; justify-content: flex-end; margin: 0 0 1rem;">
  <a href="https://github.com/the78mole/PredictionDB" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 0.4rem; text-decoration: none; color: inherit; font-size: 0.9rem; padding: 0.35rem 0.7rem; border: 1px solid #d0d7de; border-radius: 0.5rem;">
    <svg height="18" width="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
    <span>the78mole/PredictionDB</span>
  </a>
</div>

There comes a point in every mole's life when it stops digging long enough to look at what it has built – and realises it has no idea how big the burrow actually is, nobody outside can see any of it, and the only documentation is a pile of muddy notes on the tunnel walls.

That point was this week.

**Previously, underground:** [PredictionDB](/blog/2026/predictiondb-forecasting-german-power-prices-from-free-weather) forecasts German grid load and day-ahead power prices for the coming week, from free data only. [Two days later](/blog/2026/predictiondb-two-days-fifty-prs-later) it pulled three years of weather history through GitHub Actions and tripped over the clock change. [Two days after that](/blog/2026/predictiondb-sixty-seven-prs-and-one-expensive-thursday), a Thursday at 560 €/MWh taught all five model versions humility, and the burrow gained a 31-member weather ensemble.

Since then: 34 more merged PRs ([#177](https://github.com/the78mole/PredictionDB/pull/177) to [#210](https://github.com/the78mole/PredictionDB/pull/210)). Fewer than last time, because some of them were the kind of work moles don't usually admit to doing. Paperwork, for instance.

| Tunnel | What happened | PRs |
|---|---|---|
| Shop window | Public week-ahead forecast with a fixed short link, daily | [#195](https://github.com/the78mole/PredictionDB/pull/195)–[#198](https://github.com/the78mole/PredictionDB/pull/198), [#200](https://github.com/the78mole/PredictionDB/pull/200), [#201](https://github.com/the78mole/PredictionDB/pull/201) |
| Filing cabinet | Requirements from stakeholder down to the function, traceable in code | [#193](https://github.com/the78mole/PredictionDB/pull/193), [#194](https://github.com/the78mole/PredictionDB/pull/194), [#203](https://github.com/the78mole/PredictionDB/pull/203)–[#205](https://github.com/the78mole/PredictionDB/pull/205) |
| Measuring the burrow | Storage per weather group, bronze clean-up, a tired disk | [#192](https://github.com/the78mole/PredictionDB/pull/192), [#202](https://github.com/the78mole/PredictionDB/pull/202), [#206](https://github.com/the78mole/PredictionDB/pull/206)–[#210](https://github.com/the78mole/PredictionDB/pull/210) |
| Weather for all of Europe | GFS Europe gold per bidding zone, GEFS catching up | [#180](https://github.com/the78mole/PredictionDB/pull/180), [#185](https://github.com/the78mole/PredictionDB/pull/185)–[#191](https://github.com/the78mole/PredictionDB/pull/191) |
| Thinking about GPUs | What training in the cloud would cost, and how the backtest works | [#181](https://github.com/the78mole/PredictionDB/pull/181), [#182](https://github.com/the78mole/PredictionDB/pull/182), [#184](https://github.com/the78mole/PredictionDB/pull/184) |

## The Shop Window: A Forecast You Can Actually Look At

Three posts in, a fair question from surface-dwellers was: "Nice charts. Can I see the forecast?" Until now the honest answer was "only if you're in my basement". The Grafana runs inside the home lab, behind a login, and I'm not putting a database with my whole infrastructure on the internet just to show a line chart.

The solution ([#197](https://github.com/the78mole/PredictionDB/pull/197)) is a small service that does the moley thing: it comes up for air once a day, takes a picture, and goes back down. Every day at 14:30 local time – after the day-ahead auction has published tomorrow's prices – it uploads the week panels as an interactive **Grafana snapshot** to snapshots.raintank.io and points a fixed short link at the newest one:

**[go.the78mole.de/predb](https://go.the78mole.de/predb)**

![Public snapshot of the week-ahead price forecast from 31 October 2026: day-ahead price for today and tomorrow, P50 forecast to D+7, grey P10–P90 band, orange daily means weighted with the household profile H0 and red error bars](/images/blog/2026/10/predictiondb-public-week-price.png)

*Screenshot of the public snapshot from 31 October 2026, 14:00 run. Prices: Bundesnetzagentur | SMARD.de, CC BY 4.0; forecasts from PredictionDB. The snapshot has its own panel with all sources and licenses.*

What you see there:

- **Load and price up to D+7** for the champion model, with the P50 as a line and the P10–P90 band in grey ([#195](https://github.com/the78mole/PredictionDB/pull/195)). For each hour, the newest run that covers it wins.
- **A daily mean per delivery day** with a red error bar from P10 to P90 ([#196](https://github.com/the78mole/PredictionDB/pull/196)). It's not the plain average: it's weighted with the BDEW household load profile H0, because a household doesn't use power evenly across the day. That's the number that matters if you're on a dynamic tariff – or if you're a mole deciding whether to charge the car this week or next.
- **Today and tomorrow are real prices**, not forecasts, as soon as the auction result is in.
- **A list of older snapshots** at the bottom, so you can check last week's forecast against what actually happened. Snapshots live for 30 days.

You can see in the screenshot what the model thinks of the next week: around 230 €/MWh, slowly easing towards 196 at the end. And you can see the band, which goes from "fairly sure" for tomorrow to "I'm a mole, not a prophet" by D+5. That band is honest. After last Thursday I'd rather show a wide band than a confident line.

<details>
<summary><strong>Why a snapshot and not a public dashboard</strong> (click to expand)</summary>

A Grafana snapshot is a frozen copy of the panels *with their data* – no database connection, no live queries, nothing that can reach back into the burrow. That's exactly what I want for something public: the home-lab Grafana stays behind its login, and the internet gets a picture that happens to be interactive (zoom, tooltips, legend toggles).

The catch: raintank's snapshot server only knows Grafana's standard panels. Internally, the price panels now use ECharts for the bold daily-mean labels and the error bars ([#198](https://github.com/the78mole/PredictionDB/pull/198)), so there's a separate "public" dashboard template built only from standard panels. The internal dashboard "Prognose aktuell" also moved into its own dashboard, because Grafana silently ignores relative panel time overrides as soon as you zoom once – and then your "next seven days" panel happily shows last Tuesday.

</details>

One bug surfaced right after the shop opened. Between 13:00 and the moment the auction result actually lands in the database, the model believed tomorrow's price was already known (that's the rule), found nothing there, and produced a price forecast of NaN – an empty shop window. [#199](https://github.com/the78mole/PredictionDB/pull/199) caps "known until" at the last value that's actually present, and the predictor refuses to write NaN at all. Customers prefer goods.

## The Filing Cabinet: 110 Requirements, Voluntarily

Here's a confession that will make some readers question everything they thought they knew about moles: I wrote requirements. Not because a customer demanded them. Because after 200 PRs, the specification and the architecture document had started telling slightly different stories, and "the code is the documentation" stops being funny once the Compose file lists 25 services.

So [#193](https://github.com/the78mole/PredictionDB/pull/193) turned the project into a [StrictDoc](https://strictdoc.readthedocs.io/) project under `reqs/`, structured along ISO/IEC/IEEE 29148, 15288 and 12207. Yes, for a hobby project. I know.

| Level | Prefix | Count |
|---|---|---|
| Stakeholder requirements (mission and guiding principles) | `STK-` | 25 |
| System requirements (incl. VM, Garage, Postgres, Grafana, Actions, GHCR) | `SYSR-` | 42 |
| System architecture | `SYSA-` | 28 |
| Software requirements for wx-ingest, wx-process, wx-exchange, energy-ingest, mastr-ingest | `SWR-<service>-` | 18 + 21 + 23 + 31 + 17 = **110** |
| Software architecture for the same five services | `SWA-<service>-` | 76 |

The fun part is the bottom of the pyramid. Every module points to its architecture component in the docstring, every function and test to the requirement it fulfils:

```python
def assemble(model, resolution, run, decoded, attrs=None) -> Dataset:
    """Setzt dekodierte Schritte zu einem Datensatz zusammen (Intervallwerte siehe decode).

    @relation(SWR-WXP-012, scope=function)
    """
```

(Shortened from `wx_process/silver.py`. The docstrings are German, like the rest of the project – the mole only blogs in English.)

A pre-commit hook (`reqs-abdeckung`) then complains about every requirement that's marked as implemented but has no reference from the code – or, if its verification method is "Test", no reference from a test. StrictDoc itself refuses to build if anything points at an ID that doesn't exist. The rendered HTML hangs off every CI run as an artifact. Only docstrings changed in the code; the mole remains a mole.

Five services are done: wx-ingest as the template, then wx-process, wx-exchange, energy-ingest and mastr-ingest ([#194](https://github.com/the78mole/PredictionDB/pull/194), [#203](https://github.com/the78mole/PredictionDB/pull/203)–[#205](https://github.com/the78mole/PredictionDB/pull/205)). The ML side is still waiting for its turn at the filing cabinet. The requirements were collected afterwards from the specification, the architecture, the code and the decisions in the PRs – which is the honest way of saying the paperwork came after the tunnel. As it always does.

## Measuring the Burrow

Next surprise: I didn't actually know how big everything was. So now a service measures it every hour and Grafana shows the storage per weather group – GFS Germany, GFS Europe, GEFS and "other" – split into bronze, silver, gold and metadata ([#207](https://github.com/the78mole/PredictionDB/pull/207)).

The first measurement on the VM:

| What | Size |
|---|---|
| Silver (Zarr stores in Garage) | 228 GB in 1.58 million objects |
| Bronze (raw GRIB in Garage) | 40 GB |
| Gold (`feat.nwp_value` in TimescaleDB) | 23 GB |
| **Garage metadata (LMDB plus two snapshots)** | **96 GB** |

Read the last line twice. The object store's own index is more than twice as big as all the raw weather data. 1.58 million small objects are 1.58 million index cards, and Garage keeps them very carefully. A mole with a 96 GB card index for a 268 GB cellar – that's the kind of thing you only find out when you measure. The listing itself was slow enough that the measurement service went through three iterations in two days: list silver first and in parallel, extrapolate the rest, and finally take the months from the database instead of listing prefixes at all ([#208](https://github.com/the78mole/PredictionDB/pull/208)–[#210](https://github.com/the78mole/PredictionDB/pull/210)).

Two clean-ups followed. Old GFS bronze is now deleted after 92 days – but only for runs whose silver exists ([#192](https://github.com/the78mole/PredictionDB/pull/192), [#206](https://github.com/the78mole/PredictionDB/pull/206)). Silver stays; I decided not to delete that.

And the disk got a break ([#202](https://github.com/the78mole/PredictionDB/pull/202)). The VM's Docker disk was 100 % busy at about 980 write IOPS, but only 27 MB/s and 48 ms per IO, while the CPU was idling at 1 %. The gold writers were mostly waiting for the write-ahead log. 581 of 3,072 checkpoints were forced because `max_wal_size` was 1 GB. Now Postgres gets 8 GB of WAL, 15-minute checkpoints, zstd WAL compression and 64 MB WAL buffers, and only the bulk weather writers run with `synchronous_commit=off`. If the VM crashes, they lose the last few seconds and simply redo those runs. Everything else still commits synchronously.

<details>
<summary><strong>What synchronous_commit=off actually risks</strong> (click to expand)</summary>

With the default, Postgres only reports a COMMIT as done once the WAL record is flushed to disk. With `synchronous_commit=off` it reports success right away and flushes a moment later (at most three times the WAL writer delay). The database never becomes inconsistent – a crash just loses the transactions from the last fraction of a second, as if they had never happened. For a weather job that writes features for a run and marks the run as done in the same transaction, that's harmless: after a crash, the run is simply due again. For anything a human typed in, I'd never do it.

</details>

## Weather for All of Europe

The European GFS at 0.5° from the last post was collecting silver but no gold, because gold needs regions and there was no plant clustering on that grid. [#190](https://github.com/the78mole/PredictionDB/pull/190) gives it the same regions as the GEFS ensemble: 50 bidding zones as areas plus Germany's wind and PV weighted by the plant register, all under the same codes. Now GFS and GEFS can be compared zone by zone – the deterministic run against the ensemble mean and spread.

The rest of the weather work was the unglamorous kind that keeps a burrow standing: GEFS gold percentiles vectorised, backlogs worked off without pauses, blocking work moved into its own thread pool, and an import from GHCR that survives Garage timeouts ([#180](https://github.com/the78mole/PredictionDB/pull/180), [#185](https://github.com/the78mole/PredictionDB/pull/185)–[#189](https://github.com/the78mole/PredictionDB/pull/189), [#191](https://github.com/the78mole/PredictionDB/pull/191)). The weather dashboard now also says which service does what, because "wx-process-backfill-eu" isn't self-explanatory even to the mole that named it ([#177](https://github.com/the78mole/PredictionDB/pull/177)).

## Side Tunnel: What Would a GPU Cost?

LightGBM is the baseline, and the roadmap has neural networks (TFT, TiDE, N-HiTS) that have to beat it. [`cloud-gpu-training`](https://github.com/the78mole/PredictionDB/tree/main/docs/analysen/cloud-gpu-training) ([#181](https://github.com/the78mole/PredictionDB/pull/181), [#184](https://github.com/the78mole/PredictionDB/pull/184)) estimated what renting the hardware would cost:

| Model | Backtest on the VM | On a rented RTX 4090 | Per month, weekly retraining |
|---|---|---|---|
| LightGBM | 3.8 h | 30–45 min (mostly more CPU cores), ~0.15 $ | ~0.60 $ |
| N-HiTS, TiDE | hours to half a day | ~1 h, under 0.30 $ | ~1 $ each |
| TFT | several days | 6–12 h, 1–2 $ | 5–8 $ |

The data isn't the problem: a training snapshot is 140 MB today, maybe 0.5–0.7 GB with the European weather and the ensemble, and it would travel through GHCR like everything else. The slowest step is exporting the snapshot on the VM (1.2–1.5 h), and that doesn't move to the cloud. The verdict for a mole on a budget: a TFT experiment costs less than a coffee, so cost isn't the excuse anymore. Time is.

To make sure the mole understands its own scoring system before it starts paying for GPUs, there's now a detailed [`docs/BACKTEST.md`](https://github.com/the78mole/PredictionDB/blob/main/docs/BACKTEST.md) ([#182](https://github.com/the78mole/PredictionDB/pull/182)) with seven Mermaid diagrams: expanding-window folds, out-of-fold stages, calibration per fold, metrics and the champion/challenger rule.

## What's Next

- **Results of the ablations** from the last post (marginal-cost index, calibrated bands) – the mole promised not to claim anything before the backtest speaks.
- **Requirements for `ml-train`**, the last big service without a place in the filing cabinet.
- **Watching the public forecast against reality.** The snapshot archive makes every miss public. That's the point.
- **A first neural network on a rented GPU**, now that it costs less than the snacks for the evening.

The code is still on GitHub under the Business Source License 1.1, which allows internal use; check the [license](https://github.com/the78mole/PredictionDB/blob/main/LICENSE) before you build a business on it. The data artifacts on GHCR are CC BY 4.0, with the source attributions passed on.

Back underground – but with a window now. If you walk past [go.the78mole.de/predb](https://go.the78mole.de/predb) in the afternoon, wave. The mole will be the one squinting at the error bars.
