# FOREX - On-Chain Forex and Commodities Backtesting Lab

> Status: Archived research project. Development concluded; the lab is complete and
> left intact as a reusable reference. The honest verdict that ended it is in
> [Why this project is closed](#why-this-project-is-closed-the-verdict).

A self-contained Python lab for researching, backtesting, and (optionally) deploying
systematic trading strategies on **forex pairs and commodities**, with live execution
targeted at **on-chain perpetual futures** (decentralized, wallet-based, no broker account).

It was built to answer one question with real rigor:

> Is there a durable, tradeable edge in technical forex and commodity strategies once you
> pay realistic trading costs?

The short answer the lab reached, after sweeping more than a thousand strategy
specifications, was **no - not in the styles and data tested**. That negative result is
the main finding, and it is documented honestly rather than buried.

---

## Table of contents

- [What is this, in plain terms?](#what-is-this-in-plain-terms)
- [Headline finding](#headline-finding)
- [Architecture](#architecture)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
- [Usage](#usage)
  - [1. Get market data](#1-get-market-data)
  - [2. Run the backtest gauntlet](#2-run-the-backtest-gauntlet)
  - [3. Explore results in the dashboard](#3-explore-results-in-the-dashboard)
  - [4. Write your own strategy](#4-write-your-own-strategy)
  - [5. The live trader scaffold (advanced)](#5-the-live-trader-scaffold-advanced)
- [The backtest gauntlet explained](#the-backtest-gauntlet-explained)
- [Data: sources, coverage, schema, caveats](#data-sources-coverage-schema-caveats)
- [Why this project is closed](#why-this-project-is-closed-the-verdict)
- [Disclaimers](#disclaimers)

---

## What is this, in plain terms?

A few terms first, for readers who are new to the space:

- **Forex (FX)** is the market for currency pairs, for example EUR/USD (euro against US dollar).
- **Commodities** here means gold, silver, crude oil, copper, and natural gas.
- **Perpetual futures ("perps")** are contracts that let you bet on a price going up or
  down with leverage, and that never expire.
- **On-chain / DeFi** means the trading happens through smart contracts on a blockchain
  (this project targets [Ostium](https://ostium.app), a perpetuals exchange on the Arbitrum
  network) instead of a traditional broker. You trade from a crypto wallet; there is no
  sign-up or account approval.
- **Backtest** means replaying a trading rule over years of historical price data to see
  whether it would have made money.
- **Edge** means a real, repeatable advantage that survives trading costs and is not just
  luck or curve-fitting to the past.

With that vocabulary, the project does four things:

1. **Collects** years of one-minute price history for 16 instruments (13 currency pairs and
   3 commodities) and stores them in a clean, uniform format.
2. **Backtests** trading strategies against that history through a deliberately harsh,
   multi-stage filter (the "gauntlet") that charges realistic costs and aggressively tests
   for curve-fitting.
3. **Organizes** strategies into a lifecycle (candidates -> forward-test -> live -> retired)
   so that only the ones that survive the gauntlet get promoted.
4. **Scaffolds** a live trading bot for the Ostium venue, with on-chain order placement
   switched OFF by default so nothing can spend real money by accident.

A small web dashboard ties it together: charts of the data, a sortable table of every
backtest result, and a profit-and-loss view for the (paper and live) trader.

---

## Headline finding

The lab applied its full gauntlet to a large library of strategies (directional/technical,
session/time-of-day, and statistical). The result, across every batch:

- **No strategy was robust on forex majors.** What edge survived clustered narrowly on a
  few **commodities** (oil, copper, natural gas), and even those were fragile under stress.
- Session and time-of-day strategies showed **no edge even at zero cost** - so it was not a
  cost problem, the raw signal simply was not there in the available data.

In other words: the realistic-cost gauntlet did its job. It is much easier to build a
backtester that flatters strategies than one that honestly rejects them, and this one was
built to reject. The negative result is the deliverable.

---

## Architecture

The codebase is split into three parts with a strict one-way dependency rule, so a bug in
one part cannot break the others:

```
            +------------------------------------------+
            |  shared/   pure math, data clients,       |
            |            the instrument registry        |
            |  (imported by everything; depends on none)|
            +------------------------------------------+
                 ^                              ^
                 |                              |
   +---------------------------+   +-----------------------------+
   |  LAB/   the offline lab   |   |  TRADE/  the live trader    |
   |  data pipeline + backtest |   |  scaffold (Ostium venue)    |
   |  gauntlet + web dashboard |   |                             |
   |  (imports shared/ only)   |   |  (imports shared/ only)     |
   +---------------------------+   +-----------------------------+
```

- **`shared/`** holds the single source of truth for indicators (EMA, RSI, MACD, ATR, ...),
  exit math (stops/targets/trailing), the live-price client, and the instrument registry.
  Adding or removing a tradeable instrument is a one-line edit here.
- **`LAB/`** is the research half: it downloads and cleans data, runs the backtest gauntlet,
  and serves the dashboard. It never imports `TRADE/`.
- **`TRADE/`** is the execution half: it runs the same strategy code live against the Ostium
  venue. It never imports `LAB/`.

The key design choice: **a strategy is written once** as a pure function and is used,
unchanged, by both the backtester and the live trader. There is no separate "live version"
of a strategy to drift out of sync.

---

## Repository layout

```
shared/            Pure math + data clients + the instrument registry (imported everywhere)
  indicators.py      EMA/RSI/MACD/ATR and friends
  exits.py           stop-loss / take-profit / trailing math
  instruments.py     THE registry: the 16-instrument universe, one row per instrument
  ostium_data.py     read-only client for the venue's public live price feed
  timeutils.py       epoch-ms / timezone helpers

LAB/               The offline research lab (imports shared/ only)
  download.py        download raw 1-minute forex history (HistData source)
  convert.py         convert raw archives into unified parquet
  dukascopy_*.py     secondary source for commodities the primary source lacks
  gap_check.py       data-continuity audit
  requirements.txt   Python dependencies
  backtest/          the gauntlet: engine, cost model, gate, walk-forward, stress, runner
  plainchart/        the web dashboard (charts, results table, PnL)
  labchart.py        shared charting core

TRADE/             The live trader scaffold (imports shared/ only)
  ostium_client.py   thin wrapper over the venue's Python SDK
  ostium_trader.py   the bot loop (signal -> size -> order); order placement gated OFF
  ostium_testnet_setup.py   testnet funding helper

strategies/        The managed strategy library, organized by lifecycle
  _template.py       copy this to author a new strategy
  loader.py          discovers strategy modules and builds the catalog
  promote.py         routes strategies between lifecycle folders by their verdict
  candidates/        authored, not yet screened
  forward/           passed enough to forward-test (paper)
  live/              cleared the full gauntlet
  graveyard/         tested and dropped (kept for the record)

reservoir/         A large pool of raw strategy research mined from trading literature,
                   used as a source to author new candidates from

webcore/           Shared static web assets (theme, fonts, images)
```

Large, regenerable artifacts (downloaded archives, the built parquet, logs, virtual
environments, and any local secrets) are intentionally **not** committed - see `.gitignore`.

---

## Getting started

### Requirements

- Python 3.10 or newer.
- About 3 GB of free disk for the full historical dataset once you build it.

### Install

```bash
# from the repository root
python3 -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -r LAB/requirements.txt
```

Key dependencies (all pinned in `LAB/requirements.txt`): `pandas` and `pyarrow` for data,
`numpy` for math, and two independent backtesting libraries (`vectorbt` and `backtesting`)
that the gauntlet uses to cross-check its own results.

The live trader depends on the venue's own SDK (`ostium-python-sdk`). That SDK has a heavy
dependency tree, so if you ever run the trader, install it in a **separate** virtual
environment to keep it isolated.

### A note on data

The repository ships **code only**. The actual price history is large and freely
re-downloadable, so it is not stored here - you build it locally with the pipeline below.

---

## Usage

A typical session goes: get data, run the gauntlet, look at the results in the dashboard.
Authoring strategies and running the live trader are optional, more advanced steps.

### 1. Get market data

```bash
cd LAB
python3 download.py        # download all forex pairs (resumable; re-run to fill gaps)
python3 convert.py         # convert raw archives into unified parquet
python3 gap_check.py       # audit the data for suspicious gaps
```

Useful flags:

```bash
python3 download.py --pairs eurusd          # just one pair
python3 download.py --start-year 2024       # shallow, fast probe
python3 convert.py --pairs eurusd --force   # rebuild one pair's parquet
```

To add the commodities the primary source does not carry (oil, copper, natural gas), use
the secondary Dukascopy ingester (best run in its own virtual environment):

```bash
python3 dukascopy_ingest.py --pull wti copper natgas
```

### 2. Run the backtest gauntlet

```bash
cd LAB/backtest

python3 build_registry.py --quick     # smoke test: 2 instruments, a few minutes
python3 build_registry.py             # the full sweep (can take hours on many strategies)
python3 build_registry.py --triage    # cheap gate-only pre-filter, writes triage.json
```

Common options:

| Flag             | Effect                                                            |
|------------------|------------------------------------------------------------------|
| `--quick`        | Smoke run on EUR/USD and gold only                               |
| `--strategy IDS` | Comma-separated strategy IDs to run                              |
| `--pairs CODES`  | Restrict to specific instruments, e.g. `EURUSD,XAUUSD`          |
| `--cadence C`    | Restrict to one trade cadence (`day` / `swing` / `scalp`)        |
| `--active-only`  | Skip the graveyard (faster iteration)                           |
| `--procs N`      | Number of worker processes                                       |
| `--promote`      | After the run, route survivors to their lifecycle folders        |

The run writes `strategy_registry.json` - a full record of every strategy, every
instrument, and every verdict. That file is what the dashboard's Results page reads.

### 3. Explore results in the dashboard

```bash
# from the repository root
LAB/plainchart/run.sh
# or, equivalently:
python3 LAB/plainchart/app.py --port 9500 --host 127.0.0.1
```

Then open `http://127.0.0.1:9500`. The dashboard has five views:

- **Backtest** - charts of your local historical data.
- **Results** - a sortable, filterable table of every strategy's gauntlet verdict.
- **Paper** - the trader's paper/testnet account (empty until the trader runs).
- **Live** - the trader's live account (empty until the trader runs).
- **PnL** - paper and live profit-and-loss side by side.

The host and port are configurable; by default the dashboard binds to localhost only.

### 4. Write your own strategy

Each strategy is a single Python file with two things: a `META` description and a pure
`signal` function.

```bash
cp strategies/_template.py strategies/candidates/MY_STRATEGY.py
# then edit the new file
```

The signal function has this exact shape:

```python
def signal(ind, pos, htf=None):
    """
    ind : dict of precomputed indicator arrays (e.g. ind["ema_fast"], ind["rsi"])
    pos : the current bar index (an integer)
    htf : optional higher-timeframe indicators (None for single timeframe)

    Return "long" to go long, "short" to go short, or None to do nothing.
    Must be pure: no file/network access, no global state.
    """
    ...
    return None
```

Because the function is pure and uses the shared indicator/exit libraries, the very same
code is run by the backtester and (if promoted) by the live trader. The `loader` discovers
your file automatically; `promote.py` later moves it between the lifecycle folders based on
how it does in the gauntlet.

Note: the forex data here has **no volume** (see caveats), so volume-based rules will not
work on it.

### 5. The live trader scaffold (advanced)

`TRADE/ostium_trader.py` can run the promoted strategies against the Ostium venue, in two
modes: **testnet** (a free practice network with fake funds) and **live** (real funds on
Arbitrum mainnet).

> Safety first: **on-chain order placement is OFF by default.** The trader computes signals
> and tracks a simulated profit-and-loss, but it will not place a real order unless it is
> explicitly *armed* - both a command-line `--arm` flag and an environment flag must be set
> together. With either one missing, it runs in a harmless dry mode. Treat the live mode as
> experimental and start on testnet.

To run it you provide a wallet private key and (optionally) RPC endpoints through
**environment variables** - they are never hardcoded in the repository. See
`TRADE/ostium_client.py` for the exact variable names. Keep secrets in an untracked `.env`
file or your shell environment; the `.gitignore` is configured to keep such files out of
version control.

---

## The backtest gauntlet explained

The gauntlet is the heart of the project. Its job is to be a tough, honest judge. A strategy
is reported as **ROBUST** only if it clears every stage below; it lands in **CONSIDERATION**
if it passes the basics but is fragile; otherwise it is **DROP**ped (and archived, not
deleted).

1. **Realistic-cost gate.** The strategy is run through an in-house engine that charges the
   real costs of trading on the target venue: opening fees, a bid/ask impact that scales by
   asset class, daily carry/rollover, a fixed per-close oracle fee, and - most importantly -
   **slippage that scales with volatility** (calm bars cost little, violent bars cost a lot,
   capped to model fat tails). To pass, a strategy must clear sensible thresholds (a healthy
   profit factor, a positive net result, a bounded drawdown, and enough trades to be
   meaningful).

2. **Independent cross-confirmation.** The same trade signals are re-run through two
   third-party backtesting libraries (`vectorbt` and `backtesting`). Both must also show a
   profit on a given instrument before that instrument counts. This guards against bugs or
   quirks in the in-house engine flattering a strategy. Confirmation is required
   per-instrument, because a real edge can legitimately exist on only one market (say, gold).

3. **Walk-forward test.** Each instrument's history is split into an in-sample part (used to
   decide whether the strategy looks good) and a later, unseen out-of-sample part (used to
   check whether it still works). A strategy that looks great in-sample but dies
   out-of-sample is curve-fitting, and is dropped.

4. **Rolling walk-forward.** A stricter version of the above: a window is slid across the
   whole history many times, with a gap to prevent leakage, and the out-of-sample results
   are stitched together. This checks that an edge persists across many different market
   regimes, not just one lucky split.

5. **Stress test.** The surviving trades are re-priced under deliberately worse conditions
   (higher fees, multiplied slippage, doubled holding costs). If the edge flips to a loss
   under stress, it is graded fragile.

A few key terms used above: **profit factor** is gross profit divided by gross loss (above
1.0 means profitable); **drawdown** is the worst peak-to-trough equity drop; **slippage** is
the gap between the price you expect and the price you actually get.

The cost model is single-venue and intentionally pessimistic. It is not a worst-of-every-
broker "Frankenstein" - it models one real venue coherently, which is both fairer and harder
to game.

---

## Data: sources, coverage, schema, caveats

**Universe (16 instruments):**

- Majors and developed-market pairs: EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD,
  NZD/USD
- A non-USD cross: EUR/JPY
- Metals: gold (XAU/USD), silver (XAG/USD)
- Energy: Brent crude (BCO/USD), plus WTI crude and natural gas (from the secondary source)
- Emerging-market exotics: USD/ZAR, USD/MXN
- An industrial metal: copper

**Timeframes:** one-minute base data, losslessly resampled to 5m, 15m, 1h, 4h, and 1d.

**Sources:** HistData.com (free, generic ASCII, one-minute bars) for the forex pairs, and
Dukascopy for the three commodities the primary source does not carry and for cross-checking.

**Storage:** a single uniform parquet schema (9 columns) shared by every instrument and
timeframe, so any consumer reads any instrument the same way. Timestamps are stored as UTC
epoch milliseconds.

**Honest caveats (these shape what the data can and cannot tell you):**

- The free forex data is **bid-only** (no ask), so there is no spread information in the raw
  bars; spreads/costs are applied by the backtest cost model instead.
- Forex **volume is always zero** (there is no central exchange for FX), so volume-based
  indicators do not apply.
- HistData timestamps are US Eastern *without* daylight saving; the converter shifts them to
  UTC with a fixed offset.
- The earliest years (2000-2003) are sparse at the source and cannot be repaired from any
  free feed, so the backtest trims each instrument to where its data becomes solid (majors
  from 2004; metals/energy/exotics from their later start years).

---

## Why this project is closed

The project was closed deliberately after the research question was answered. Three broad
families of strategy were swept to exhaustion:

1. **Directional / technical** (over a thousand specifications mined from books, code, and
   public sources): the few out-of-sample survivors netted a trivial amount - noise, not a
   business - and lost money applied across the full universe.
2. **Session / time-of-day** (opening-range, pivots, day-of-week, and similar): essentially
   none had an edge even at zero cost, which means the signal itself is absent in this data,
   not merely eaten by fees. (True session edges likely need order-flow data this lab does
   not have.)
3. **Statistical / pairs**: with no base edge anywhere to manage, this was not pursued.

The conclusion: with the strategy styles and freely available data tested, **on-chain forex
trading did not present a durable retail edge.** Revisiting it would require a genuinely new
source of edge (order-flow, funding/carry history, or news/event data) rather than another
pass over the same ideas. The lab is kept intact so that work could start from here rather
than from scratch.

This is a result worth publishing precisely because it is negative: the infrastructure is
sound, the test was fair, and the honest answer was "no."

---

## Disclaimers

- **Not financial advice.** This is a research and educational project. Nothing here is a
  recommendation to trade anything.
- **No warranty.** The code is provided as-is, as an archived reference.
- **Trading is risky.** Leveraged perpetual futures can lose money faster than they make it.
  On-chain/DeFi trading carries additional smart-contract, oracle, and self-custody risks.
- **The live trader is experimental** and ships with real-money order placement disabled by
  default. If you choose to enable it, you do so at your own risk; start on testnet.

Josoka.com
