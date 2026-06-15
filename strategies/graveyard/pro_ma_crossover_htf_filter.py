#!/usr/bin/env python3
"""pro_ma_crossover_htf_filter -- EMA5/50 crossover with optional HTF MA direction filter. MQL5 CodeBase."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "pro_ma_crossover_htf_filter",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema5, ema50, close",
    "long": "ema5 crosses above ema50 AND close > ema5; HTF ema50 rising if available",
    "short": "ema5 crosses below ema50 AND close < ema5; HTF ema50 falling if available",
    "desc": "EMA5/50 crossover confirmed by price position; HTF slope filter when available",
    "source": "Pro MA Crossover EA (Vivekpanu, MQL5 CodeBase 70916, 2026)",
}


def signal(ind, pos, htf=None):
    """Crossover of EMA5 over EMA50 with price above/below fast MA confirmation."""
    f = ind["ema5"][pos]
    s = ind["ema50"][pos]
    f1 = ind["ema5"][pos - 1]
    s1 = ind["ema50"][pos - 1]
    c = ind["close"][pos]
    if nan(f, s, f1, s1, c):
        return None
    # HTF slope gate: if HTF provided, require ema50 trending in the same direction
    htf_ok_long = True
    htf_ok_short = True
    if htf is not None:
        htf_e50 = htf.get("ema50")
        htf_e50_1 = htf.get("ema50_1")
        if htf_e50 is not None and htf_e50_1 is not None and not nan(htf_e50, htf_e50_1):
            htf_ok_long = htf_e50 > htf_e50_1
            htf_ok_short = htf_e50 < htf_e50_1
    if _xup(f, f1, s, s1) and c > f and htf_ok_long:
        return "long"
    if _xdn(f, f1, s, s1) and c < f and htf_ok_short:
        return "short"
    return None
