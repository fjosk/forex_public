#!/usr/bin/env python3
"""psar_200ema_5m -- EMA200 macro + PSAR direction + close above EMA9. web:forextradingstrategies4u.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "psar_200ema_5m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema200, psar_dir, ema9 (proxy ema10)",
    "long": "close > ema200 AND psar_dir > 0 AND close > ema9",
    "short": "close < ema200 AND psar_dir < 0 AND close < ema9",
    "desc": "Three-condition 5m scalp: EMA200 macro trend + PSAR dots + EMA9 momentum",
    "source": "web:https://forextradingstrategies4u.com/5-minute-forex-scalping-strategy-using-parabolic-sar-and-200-ema/",
}


def signal(ind, pos, htf=None):
    """All three conditions must align: EMA200 trend, PSAR direction, EMA9 close."""
    e200 = ind["ema200"][pos]
    pdir = ind["psar_dir"][pos]
    e9 = ind["ema9"][pos]
    c = ind["close"][pos]
    if nan(e200, pdir, e9, c):
        return None
    if c > e200 and pdir > 0 and c > e9:
        return "long"
    if c < e200 and pdir < 0 and c < e9:
        return "short"
    return None
