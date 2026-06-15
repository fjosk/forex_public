#!/usr/bin/env python3
"""ssl_wavetrend -- SSL Channel + WaveTrend cross inside Keltner Channel. kevinmck100 TradingView.

SSL direction flip combined with WaveTrend oversold cross inside Keltner Channel.
Candle-height threshold dropped (subjective); TP-clearance EMA check dropped (exit handled by engine).
"""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "ssl_wavetrend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ssl_hlv, wt1, wt2, kc_lo, kc_up",
    "long": "SSL flips to positive AND wt1 crosses above wt2 from oversold (<-60) AND price inside KC",
    "short": "SSL flips to negative AND wt1 crosses below wt2 from overbought (>60) AND price inside KC",
    "desc": "SSL Channel + WaveTrend cross inside Keltner Channel (NNFX)",
    "source": "https://www.tradingview.com/script/J0urw1QI-SSL-Wave-Trend-Strategy/ kevinmck100",
}


def signal(ind, pos, htf=None):
    """SSL flip + WaveTrend cross from OB/OS inside Keltner Channel."""
    ssl = ind["ssl_hlv"][pos]
    ssl1 = ind["ssl_hlv"][pos - 1]
    w1 = ind["wt1"][pos]
    w11 = ind["wt1"][pos - 1]
    w2 = ind["wt2"][pos]
    w21 = ind["wt2"][pos - 1]
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    c = ind["close"][pos]
    if nan(ssl, ssl1, w1, w11, w2, w21, kc_lo, kc_up, c):
        return None
    inside_kc = kc_lo < c < kc_up
    ssl_long = ssl > 0 and ssl1 <= 0
    ssl_short = ssl < 0 and ssl1 >= 0
    wt_up = _xup(w1, w11, w2, w21) and w2 < -60
    wt_dn = _xdn(w1, w11, w2, w21) and w2 > 60
    if ssl_long and wt_up and inside_kc:
        return "long"
    if ssl_short and wt_dn and inside_kc:
        return "short"
    return None
