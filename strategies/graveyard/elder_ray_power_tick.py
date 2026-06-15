#!/usr/bin/env python3
"""elder_ray_power_tick -- Elder-Ray bull/bear power tick taken in the EMA21 trend direction as the counter-trend power fades.. tier2 (book-extracted from sister-lab catalog_books).

book:oscillator. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND, ALL_CLASSES

META = {
    "id": "elder_ray_power_tick",
    "cadences": ['day', 'swing'],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "Elder-Ray Bull/Bear Power, EMA(21)",
    "long": "EMA21 rising and Bear Power negative but ticking up",
    "short": "EMA21 falling and Bull Power positive but ticking down",
    "desc": "Elder-Ray bull/bear power tick taken in the EMA21 trend direction as the counter-trend power fades.",
    "source": "book:oscillator",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    bep, bep1 = I["bear_power"][i], I["bear_power"][i-1]
    bup, bup1 = I["bull_power"][i], I["bull_power"][i-1]
    if _nan(e21, e21p, bep, bep1, bup, bup1):
        return None
    ema_up = e21 > e21p
    if ema_up and bep < 0 and bep > bep1:     # uptrend: bear power negative but ticking up (dip ending)
        return "long"
    if (not ema_up) and bup > 0 and bup < bup1:  # downtrend: bull power positive but ticking down (rally ending)
        return "short"
    return None
