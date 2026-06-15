#!/usr/bin/env python3
"""alexander_filter_swing -- Alexander Percent-Filter swing reversal: flip long/short when price clears the running extreme by a volatility-scaled percent filter. Stateless causal reimplementation of the mutable run_ext/state pse. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "alexander_filter_swing",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "Running extreme (run_ext), dynamic percent filter (filt_pct = max(5%, 3x ATR%))",
    "long": "Close rises filt_pct%% above the prior running extreme (upward percent-filter reversal)",
    "short": "Close falls filt_pct%% below the prior running extreme (downward percent-filter reversal)",
    "desc": "Alexander Percent-Filter swing reversal: flip long/short when price clears the running extreme by a volatility-scaled percent filter. Stateless causal reimplementation of the mutable run_ext/state pse",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    c = I["close"][i]
    ext1 = I["run_ext"][i-1]
    fp = I["filt_pct"][i]
    if _nan(c, ext1, fp):
        return None
    # NOTE: catalog fns are stateless across calls, so the pseudocode's mutable
    # run_ext / state flip cannot be carried in-function. run_ext is a precomputed
    # running extreme (the swing anchor); a percent-filter flip is detected causally
    # by close clearing last bar's extreme by the dynamic filt_pct band. Long flip =
    # close rises filt_pct% above the prior extreme; short flip = falls filt_pct% below.
    up = ext1 * (1.0 + fp / 100.0)
    dn = ext1 * (1.0 - fp / 100.0)
    if c >= up:
        return "long"
    if c <= dn:
        return "short"
    return None
