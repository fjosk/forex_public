#!/usr/bin/env python3
"""freqtrade_enhanced_ewo_rsi_ema -- EWO+RSI+EMA-offset long entry; two independent conditions. ynstf GitHub."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "freqtrade_enhanced_ewo_rsi_ema",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "ewo, rsi, rsi2, ema20, hma21",
    "long": "rsi2<35 AND close<ema20*0.978 AND (EWO>3.147 AND rsi<57 OR EWO<-17.145)",
    "short": "Not used (long-only per source; symmetric short suppressed)",
    "desc": "Enhanced EWO RSI EMA offset: two independent oversold entry conditions via EWO regime",
    "source": "ynstf/Good-Freqtrade-Strategies EnhancedIndicatorStrategy.py",
}

_LOW_OFFSET = 0.978
_EWO_HIGH = 3.147
_EWO_DEEP = -17.145
_RSI2_ENTRY = 35
_RSI14_GATE = 57


def signal(ind, pos, htf=None):
    """Long when price dipped below EMA offset with EWO confirming strong trend or deep correction."""
    ewo = ind["ewo"][pos]
    r = ind["rsi"][pos]
    r2 = ind["rsi2"][pos]
    e20 = ind["ema20"][pos]
    c = ind["close"][pos]
    if nan(ewo, r, r2, e20, c):
        return None
    below_offset = c < e20 * _LOW_OFFSET
    rsi2_os = r2 < _RSI2_ENTRY
    # Condition 1: high EWO (strong underlying trend) + RSI14 not overbought
    cond1 = rsi2_os and below_offset and ewo > _EWO_HIGH and r < _RSI14_GATE
    # Condition 2: deeply negative EWO (hard correction)
    cond2 = rsi2_os and below_offset and ewo < _EWO_DEEP
    if cond1 or cond2:
        return "long"
    return None
