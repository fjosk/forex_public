#!/usr/bin/env python3
"""hurst_regime_filter -- Hurst exponent regime filter: trend EMA cross when H>0.55, RSI reversion when H<0.45.

QuantNeuralEdge / MacroSynergy. Uses Hurst to gate two signal types: trend-following in
persistent regimes (H>0.55) and mean-reversion in anti-persistent regimes (H<0.45).
Neutral zone [0.45, 0.55] = no entry.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "hurst_regime_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "hurst, ema50, sma200, rsi, bb_pctb",
    "long": "H>0.55: ema50 crosses above sma200; H<0.45: rsi < 30 with close above bb_lo",
    "short": "H>0.55: ema50 crosses below sma200; H<0.45: rsi > 70 with close below bb_up",
    "desc": "Hurst exponent regime filter gating trend or reversion entries",
    "source": "web:https://quantneuraledge.com/blog/hurst-exponent-trending-ranging-markets",
}


def signal(ind, pos, htf=None):
    """Hurst regime gates trend EMA cross (H>0.55) or RSI reversion (H<0.45)."""
    h = ind["hurst"][pos]
    if nan(h):
        return None
    e50 = ind["ema50"][pos]
    s200 = ind["sma200"][pos]
    e50_1 = ind["ema50"][pos - 1]
    s200_1 = ind["sma200"][pos - 1]
    rsi_v = ind["rsi"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    c = ind["close"][pos]
    if nan(e50, s200, e50_1, s200_1, rsi_v, bb_lo, bb_up, c):
        return None
    # trending regime: EMA crossover
    if h > 0.55:
        if e50 > s200 and e50_1 <= s200_1:
            return "long"
        if e50 < s200 and e50_1 >= s200_1:
            return "short"
    # mean-reverting regime: RSI extremes
    if h < 0.45:
        if rsi_v < 30 and c > bb_lo:
            return "long"
        if rsi_v > 70 and c < bb_up:
            return "short"
    return None
