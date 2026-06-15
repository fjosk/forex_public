#!/usr/bin/env python3
"""freqtrade_ewo_v8_dual_condition -- V8 EWO dual entry: pullback OR deep correction. ynstf/Good-Freqtrade.

Two long entry conditions sharing a price-below-EMA offset gate, based on EWO (Elliott Wave Osc).
EMA buy period not specified; ema50 used. HMA50 from spec -> hma21 (closest available).
RSI4 approximated by rsi2 (2-period is closest available). RSI20 approximated by rsi.
Long-only per spec.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_ewo_v8_dual_condition",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h",
    "indicators": "ewo, rsi2, rsi, ema50, hma21",
    "long": "C1: rsi2<35 AND close<ema50*0.978 AND ewo>3.147 AND rsi<57; C2: rsi2<35 AND close<ema50*0.978 AND ewo<-17.145",
    "short": "Not implemented (long-only)",
    "desc": "V8 EWO dual-condition long: trending pullback OR deep correction entry",
    "source": "https://github.com/ynstf/Good-Freqtrade-Strategies/blob/main/V8ichi.py",
}

_EWO_HIGH = 3.147
_EWO_LOW = -17.145
_OFFSET = 0.978


def signal(ind, pos, htf=None):
    """EWO dual-condition long entry."""
    ewo = ind["ewo"][pos]
    r2 = ind["rsi2"][pos]
    r = ind["rsi"][pos]
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(ewo, r2, r, c, e50):
        return None
    price_below = c < e50 * _OFFSET
    # Condition 1: trend pullback
    c1 = r2 < 35 and price_below and ewo > _EWO_HIGH and r < 57
    # Condition 2: deep correction
    c2 = r2 < 35 and price_below and ewo < _EWO_LOW
    if c1 or c2:
        return "long"
    return None
