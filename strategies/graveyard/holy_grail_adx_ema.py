#!/usr/bin/env python3
"""holy_grail_adx_ema -- Linda Raschke Holy Grail: ADX>30 rising + SMA20 touch. web:https://www.tradingsetupsreview.com/the-holy-grail-trading-setup/"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "holy_grail_adx_ema",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "adx, sma20, close, high, low",
    "long": "ADX > 30 and rising, price dips to sma20 and closes above it",
    "short": "ADX > 30 and rising, price bounces to sma20 and closes below it",
    "desc": "Holy Grail: ADX above 30 and rising, pullback to SMA20 entry (Raschke/Connors)",
    "source": "web:https://www.tradingsetupsreview.com/the-holy-grail-trading-setup/",
}


def signal(ind, pos, htf=None):
    """ADX > 30 and rising, price touches SMA20 and resumes direction."""
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    sma20 = ind["sma20"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    c = ind["close"][pos]
    if nan(adx, adx1, sma20, lo, hi, c):
        return None
    strong_trend = adx > 30 and adx > adx1
    touched_low = lo <= sma20 and c > sma20
    touched_high = hi >= sma20 and c < sma20
    if strong_trend and touched_low:
        return "long"
    if strong_trend and touched_high:
        return "short"
    return None
