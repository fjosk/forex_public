#!/usr/bin/env python3
"""market_thermometer -- Elder Market Thermometer quiet-then-explode: a run of below-average volatility primes a trend-aligned breakout on the first expansion bar.. tier2 (book-extracted from sister-lab catalog_books).

book:volatility. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, BREAK, ALL_CLASSES

META = {
    "id": "market_thermometer",
    "cadences": ['day', 'swing'],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "volatility",
    "tf": "1h-4h",
    "indicators": "EMA(20), Elder Market Thermometer (thermo) + EMA(22) of it (thermo_ema)",
    "long": "Five quiet bars (thermo below its EMA) then close above EMA20 with a new high",
    "short": "Five quiet bars (thermo below its EMA) then close below EMA20 with a new low",
    "desc": "Elder Market Thermometer quiet-then-explode: a run of below-average volatility primes a trend-aligned breakout on the first expansion bar.",
    "source": "book:volatility",
}


def signal(I, i, htf=None):
    if i < 5:
        return None
    c, e20 = I["close"][i], I["ema20"][i]
    h, h1 = I["high"][i], I["high"][i-1]
    l, l1 = I["low"][i], I["low"][i-1]
    if _nan(c, e20, h, h1, l, l1):
        return None
    quiet_run = True
    for k in range(0, 5):
        t, te = I["thermo"][i-k], I["thermo_ema"][i-k]
        if _nan(t, te) or not (t < te):
            quiet_run = False
            break
    if not quiet_run:
        return None
    if c > e20 and h > h1:
        return "long"
    if c < e20 and l < l1:
        return "short"
    return None
