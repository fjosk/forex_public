#!/usr/bin/env python3
"""triple_ma_macd_alignment -- Three-EMA stack with MACD crossover confirmation. Zeta-Zetra Python."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "triple_ma_macd_alignment",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ema9, ema21, ema50, macd, macd_sig",
    "long": "ema9 > ema21 > ema50 AND macd crosses above macd_sig",
    "short": "ema9 < ema21 < ema50 AND macd crosses below macd_sig",
    "desc": "Triple MA stack confirmed by MACD crossover in same direction",
    "source": "Zeta-Zetra 'Forex Strategies Tested in Python' -- triple_ma_macd (ChatGPT-generated, Python)",
}


def signal(ind, pos, htf=None):
    """Three-EMA stack required; MACD crossover triggers the entry."""
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    mc = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    mc1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(e9, e21, e50, mc, ms, mc1, ms1):
        return None
    bull_stack = e9 > e21 > e50
    bear_stack = e9 < e21 < e50
    if bull_stack and _xup(mc, mc1, ms, ms1):
        return "long"
    if bear_stack and _xdn(mc, mc1, ms, ms1):
        return "short"
    return None
