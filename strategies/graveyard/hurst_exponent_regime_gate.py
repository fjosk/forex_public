#!/usr/bin/env python3
"""hurst_exponent_regime_gate -- Hurst regime gate: trend follow when H>0.55, mean-revert when H<0.45.

Self-contained directional rule: trending regime -> EMA slope; MR regime -> RSI extreme.
No volume -> FX-applicable.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "hurst_exponent_regime_gate",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "hurst, ema20, ema50, rsi",
    "long": "H>0.55 AND ema20>ema50; OR H<0.45 AND rsi<30",
    "short": "H>0.55 AND ema20<ema50; OR H<0.45 AND rsi>70",
    "desc": "Hurst regime gate: trend-follow when trending (H>0.55), mean-revert when H<0.45",
    "source": "pyquantlab.medium.com/enhancing-trading-strategies-with-a-hurst-based-regime-filter",
}

_TREND_H = 0.55
_MR_H = 0.45


def signal(ind, pos, htf=None):
    """Hurst regime classifier: trend or mean-reversion entry depending on H."""
    h = ind["hurst"][pos]
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    rs = ind["rsi"][pos]
    if nan(h, e20, e50, rs):
        return None
    # Trending regime: follow EMA slope
    if h > _TREND_H:
        if e20 > e50:
            return "long"
        if e20 < e50:
            return "short"
    # Mean-reverting regime: fade RSI extreme
    elif h < _MR_H:
        if rs < 30:
            return "long"
        if rs > 70:
            return "short"
    return None
