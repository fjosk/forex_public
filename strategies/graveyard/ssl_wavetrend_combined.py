#!/usr/bin/env python3
"""ssl_wavetrend_combined -- SSL Hybrid + WaveTrend WT1/WT2 cross inside Keltner Channel. web:tradingview.com.

kevinmck100 dual-filter system: SSL for trend, WaveTrend cross for momentum, Keltner
Channel for candle-chasing guard. No volume dependency.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ssl_wavetrend_combined",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ssl_hlv, wt1, wt2, kc_up, kc_lo, atr, close, open",
    "long": "ssl_hlv == 1 AND WT1 crosses above WT2 AND close inside KC AND candle not too large",
    "short": "ssl_hlv == -1 AND WT1 crosses below WT2 AND close inside KC AND candle not too large",
    "desc": "SSL Hybrid + WaveTrend cross inside Keltner Channel (kevinmck100)",
    "source": "web:https://www.tradingview.com/script/J0urw1QI-SSL-Wave-Trend-Strategy/",
}


def signal(ind, pos, htf=None):
    """SSL direction + WaveTrend cross inside KC, candle-size guard."""
    hlv = ind["ssl_hlv"][pos]
    wt1, wt1p = ind["wt1"][pos], ind["wt1"][pos - 1]
    wt2, wt2p = ind["wt2"][pos], ind["wt2"][pos - 1]
    kc_hi = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    atr = ind["atr"][pos]
    if nan(hlv, wt1, wt1p, wt2, wt2p, kc_hi, kc_lo, c, o, atr):
        return None
    candle_body = abs(c - o)
    # candle-chasing guard: body must be less than 0.6x ATR
    if candle_body >= 0.6 * atr:
        return None
    inside_kc = kc_lo < c < kc_hi
    if not inside_kc:
        return None
    if hlv == 1 and _xup(wt1, wt1p, wt2, wt2p):
        return "long"
    if hlv == -1 and _xdn(wt1, wt1p, wt2, wt2p):
        return "short"
    return None
