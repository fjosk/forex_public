#!/usr/bin/env python3
"""force_index_ema_filter -- Force Index zero-cross with EMA50 trend gate. MQL5 articles/11269 (Elder)."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "force_index_ema_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "force13, ema50, close",
    "long": "close > ema50 AND Force Index crosses zero upward (force13 from negative to positive)",
    "short": "close < ema50 AND Force Index crosses zero downward (force13 from positive to negative)",
    "desc": "Force Index zero-cross with EMA50 trend direction gate",
    "source": "MQL5 articles/11269 Elder Force Index System 4 (buy/sell signals)",
}


def signal(ind, pos, htf=None):
    """Force Index zero-cross while price confirms trend side via EMA50."""
    fi = ind["force13"][pos]
    fi1 = ind["force13"][pos - 1]
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(fi, fi1, c, e50):
        return None
    if c > e50 and fi1 < 0 and fi > 0:
        return "long"
    if c < e50 and fi1 > 0 and fi < 0:
        return "short"
    return None
