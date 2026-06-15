#!/usr/bin/env python3
"""elder_triple_screen_elder_ray_variant -- Elder Triple-Screen with Elder-Ray: weekly EMA trend + daily bear/bull power + prior-day breakout. Kaufman.

tier1 multi-timeframe momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_triple_screen_elder_ray_variant",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "bull_power, bear_power, high, low",
    "long": "Bear Power < 0 AND Bear Power rising (bear_power > bear_power[1]); HTF trend up",
    "short": "Bull Power > 0 AND Bull Power falling (bull_power < bull_power[1]); HTF trend down",
    "desc": "Elder Triple-Screen Elder-Ray variant: HTF trend gating + daily bear/bull power direction",
    "source": "Kaufman, Trading Systems and Methods, Ch.19 Elder Triple-Screen Elder-Ray, p.12",
}


def signal(ind, pos, htf=None):
    """Elder-Ray bear/bull power with HTF trend gate."""
    if pos < 1:
        return None
    bp = ind["bear_power"][pos]
    bp1 = ind["bear_power"][pos - 1]
    bull = ind["bull_power"][pos]
    bull1 = ind["bull_power"][pos - 1]
    if nan(bp, bp1, bull, bull1):
        return None
    # HTF trend filter (weekly EMA slope)
    htf_up = True
    htf_dn = True
    if htf is not None:
        e_htf = htf.get("ema50")
        if e_htf is not None and len(e_htf) >= 2:
            htf_up = e_htf[-1] > e_htf[-2]
            htf_dn = e_htf[-1] < e_htf[-2]
    # Long: weekly trend up AND bear power negative but rising
    if htf_up and bp < 0 and bp > bp1:
        return "long"
    # Short: weekly trend down AND bull power positive but falling
    if htf_dn and bull > 0 and bull < bull1:
        return "short"
    return None
