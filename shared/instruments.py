#!/usr/bin/env python3
"""
THE instrument registry -- the SINGLE SOURCE OF TRUTH for FOREX's traded/charted universe.

Before this module the universe was hand-maintained in FOUR places that had to be kept in sync by
hand (adding or dropping a pair meant editing all four, and they had already drifted):
  - LAB/labchart.py        COIN_ORDER         (the 16, display order, UPPERCASE)
  - LAB/download.py        DEFAULT_PAIRS      (the 13 HistData FX, lowercase)
  - shared/ostium_data.py  PAIR_MAP / NOT_ON_OSTIUM / OHLC_PAIR (the Ostium 14 + overrides)
  - LAB/dukascopy_fetch.py INSTRUMENTS        (the 15 Dukascopy ids, lowercase)
Now every one of those is DERIVED from the table below, so a pair is defined ONCE.

Each row carries everything a consumer needs:
  code            our canonical UPPERCASE code (also the parquet folder/file prefix)
  klass           asset class (grouping/readability only)
  histdata_start  earliest year HistData posts it; None if not on HistData (commodities)
  backtest_start  first year safe to backtest (early HistData years 2000-2003 are too sparse, so
                  majors+EURJPY are trimmed to 2004; everything else starts at its native year)
  ostium          Ostium Builder price-feed name, or None if Ostium does not list it
  ostium_ohlc     Ostium /v1/ohlc asset name WHEN it differs from the price name (else None)
  dukascopy       dukascopy_python INSTRUMENT_* constant, or None if not fetched from Dukascopy

Sources by instrument:
  - HistData (download.py): rows where histdata_start is not None  -> 13 FX/metals/energy pairs.
  - Dukascopy (dukascopy_fetch.py): rows where dukascopy is not None -> the 12 FX (for patching) +
    WTI/COPPER/NATGAS (HistData lacks these; Ostium trades them).
  - Ostium (ostium_data.py): rows where ostium is not None -> the 14 tradeable instruments.
Keep this module PURE (no I/O, no state) so it is safe to import anywhere, incl. shared/.
"""

# ostium_id = Ostium MAINNET subgraph trading pair_id (verified 2026-06-06 via sdk.subgraph.get_pairs);
# None = not listed on Ostium. The TRADER should still resolve name->id at runtime via get_pairs()
# (testnet ids may differ) -- these are reference/sanity values. NOTE: WTI trades under CL-USD (id 7)
# and COPPER under HG-USD (id 6) -- the same names as their ostium_ohlc override.
# code,        klass,        histdata_start, backtest_start, ostium,       ostium_ohlc, dukascopy,                              ostium_id
_T = [
    ("EURUSD", "fx_major",   2000, 2004, "EUR-USD",   None,     "INSTRUMENT_FX_MAJORS_EUR_USD",          2),
    ("USDJPY", "fx_major",   2000, 2004, "USD-JPY",   None,     "INSTRUMENT_FX_MAJORS_USD_JPY",          4),
    ("GBPUSD", "fx_major",   2000, 2004, "GBP-USD",   None,     "INSTRUMENT_FX_MAJORS_GBP_USD",          3),
    ("USDCHF", "fx_major",   2000, 2004, "USD-CHF",   None,     "INSTRUMENT_FX_MAJORS_USD_CHF",          25),
    ("AUDUSD", "fx_major",   2000, 2004, "AUD-USD",   None,     "INSTRUMENT_FX_MAJORS_AUD_USD",          26),
    ("USDCAD", "fx_major",   2000, 2004, "USD-CAD",   None,     "INSTRUMENT_FX_MAJORS_USD_CAD",          16),
    ("NZDUSD", "fx_major",   2005, 2005, "NZD-USD",   None,     "INSTRUMENT_FX_MAJORS_NZD_USD",          27),
    ("EURJPY", "fx_cross",   2002, 2004, None,        None,     "INSTRUMENT_FX_CROSSES_EUR_JPY",         None),
    ("XAUUSD", "metal",      2009, 2009, "XAU-USD",   None,     "INSTRUMENT_FX_METALS_XAU_USD",          5),
    ("XAGUSD", "metal",      2009, 2009, "XAG-USD",   None,     "INSTRUMENT_FX_METALS_XAG_USD",          8),
    ("BCOUSD", "energy",     2010, 2010, "BRENT-USD", None,     None,                                    55),  # Brent: HistData only (no Dukascopy id)
    ("WTI",    "energy",     None, 2011, "WTI-USD",   "CL-USD", "INSTRUMENT_CMD_ENERGY_E_LIGHT",         7),   # trades as CL-USD
    ("COPPER", "industrial", None, 2012, "XCU-USD",   "HG-USD", "INSTRUMENT_CMD_METALS_COPPER_CMD_USD",  6),   # trades as HG-USD
    ("NATGAS", "energy",     None, 2012, "UNG-USD",   None,     "INSTRUMENT_CMD_ENERGY_GAS_CMD_USD",     58),
    ("USDZAR", "exotic",     2010, 2010, None,        None,     "INSTRUMENT_FX_CROSSES_USD_ZAR",         None),
    ("USDMXN", "exotic",     2010, 2010, "USD-MXN",   None,     "INSTRUMENT_FX_CROSSES_USD_MXN",         17),
]

# Normalize the table into a list of dicts (one per instrument, in display/canonical order).
INSTRUMENTS = [
    {"code": c, "klass": k, "histdata_start": hs, "backtest_start": bs,
     "ostium": o, "ostium_ohlc": oo, "dukascopy": d, "ostium_id": oid}
    for (c, k, hs, bs, o, oo, d, oid) in _T
]
_BY_CODE = {r["code"]: r for r in INSTRUMENTS}


# --- accessors: every legacy hardcoded list is now one of these -------------------------------

def universe():
    """All 16 instrument codes (UPPERCASE), display order. Was labchart.COIN_ORDER."""
    return [r["code"] for r in INSTRUMENTS]


def histdata_pairs():
    """Lowercase codes carried by HistData (13). Was download.DEFAULT_PAIRS."""
    return [r["code"].lower() for r in INSTRUMENTS if r["histdata_start"] is not None]


def ostium_pair_map():
    """{CODE: ostium-name} for the 14 Ostium-listed instruments. Was ostium_data.PAIR_MAP."""
    return {r["code"]: r["ostium"] for r in INSTRUMENTS if r["ostium"]}


def ostium_not_listed():
    """Codes in the universe that Ostium does NOT list (2). Was ostium_data.NOT_ON_OSTIUM."""
    return {r["code"] for r in INSTRUMENTS if not r["ostium"]}


def ostium_ohlc_overrides():
    """{CODE: ohlc-asset-name} where the OHLC name differs from the price name. Was OHLC_PAIR."""
    return {r["code"]: r["ostium_ohlc"] for r in INSTRUMENTS if r["ostium_ohlc"]}


def dukascopy_map():
    """{lowercase-code: INSTRUMENT_* const} for the 15 Dukascopy instruments. Was dukascopy INSTRUMENTS."""
    return {r["code"].lower(): r["dukascopy"] for r in INSTRUMENTS if r["dukascopy"]}


def backtest_start_year(code):
    """First year safe to backtest for an instrument (early sparse HistData years trimmed)."""
    r = _BY_CODE.get(code.upper())
    return r["backtest_start"] if r else None


def ostium_id(code):
    """Ostium MAINNET trading pair_id (reference; the trader should confirm via get_pairs()). None
    if not on Ostium. WTI->7 (CL-USD), COPPER->6 (HG-USD)."""
    r = _BY_CODE.get(code.upper())
    return r["ostium_id"] if r else None


# Map the registry's fine-grained klass to the cost model's asset class (costs.py spread buckets).
_KLASS_TO_COST = {"fx_major": "major", "fx_cross": "cross", "metal": "commodity",
                  "energy": "commodity", "industrial": "commodity", "exotic": "exotic"}


def cost_class(code):
    """Cost-model asset class for a pair ('major'|'cross'|'commodity'|'exotic'), used to pick the
    Ostium spread bucket in costs.py. Defaults to 'major' for an unknown code."""
    r = _BY_CODE.get(code.upper())
    return _KLASS_TO_COST.get(r["klass"], "major") if r else "major"
