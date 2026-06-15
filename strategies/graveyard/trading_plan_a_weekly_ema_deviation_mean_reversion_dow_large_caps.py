#!/usr/bin/env python3
"""trading_plan_a_weekly_ema_deviation_mean_reversion_dow_large_caps -- Elder Trading Plan A:
price deviates far from a long-period EMA (proxy: ema200 as weekly trend), daily EMA (ema20)
turns -> snap-back mean-reversion entry.

Source: come_into_my_trading_room_alexander_elder, Ch. Trading Plan A pp.258-260.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "trading_plan_a_weekly_ema_deviation_mean_reversion_dow_large_caps",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "ema200, ema20, bb_width, close",
    "long": "Close below ema200 by >1.5*bb_width (extreme deviation) AND ema20 turns up (ema20 > ema20[1])",
    "short": "Close above ema200 by >1.5*bb_width (extreme deviation) AND ema20 turns down (ema20 < ema20[1])",
    "desc": "Elder Plan A: extreme EMA200 deviation + EMA20 turn -> snap-back mean reversion",
    "source": "come_into_my_trading_room_alexander_elder Ch. pp.258-260",
}


def signal(ind, pos, htf=None):
    """Extreme deviation from EMA200 + EMA20 first turn -> mean-reversion entry."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    bbw = ind["bb_width"][pos]
    if nan(c, e200, e20, e20_1, bbw) or bbw <= 0:
        return None
    dev = c - e200
    threshold = 1.5 * bbw
    ema20_up = e20 > e20_1
    ema20_dn = e20 < e20_1
    if dev < -threshold and ema20_up:
        return "long"
    if dev > threshold and ema20_dn:
        return "short"
    return None
