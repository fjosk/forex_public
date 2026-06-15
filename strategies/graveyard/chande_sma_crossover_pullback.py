#!/usr/bin/env python3
"""chande_sma_crossover_pullback -- SMA5 just crossed below SMA10, price below SMA5 = contrarian long. Zeta-zetra.

Long when close < SMA5 AND SMA5 just crossed below SMA10 (bearish cross but anticipating reversion).
Short when close > SMA5 AND SMA5 just crossed above SMA10 (bullish cross, fade the pop).
SMA5 computed inline (5-bar mean of close); sma10 available directly.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "chande_sma_crossover_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h",
    "indicators": "sma10, close",
    "long": "close < sma5 AND sma5 just crossed below sma10 (post-bearish-cross pullback)",
    "short": "close > sma5 AND sma5 just crossed above sma10 (post-bullish-cross fade)",
    "desc": "Chande entry: fade the SMA5/SMA10 cross immediately after it happens; contrarian pullback",
    "source": "web:https://github.com/zeta-zetra/code",
}

_N = 5


def signal(ind, pos, htf=None):
    """SMA5/SMA10 cross pullback: enter against the cross direction."""
    if pos < _N + 1:
        return None
    s10 = ind["sma10"][pos]
    s10_1 = ind["sma10"][pos - 1]
    c = ind["close"][pos]
    if nan(s10, s10_1, c):
        return None
    # Compute SMA5 and prior SMA5 inline
    closes = ind["close"]
    vals = [closes[pos - i] for i in range(_N)]
    vals1 = [closes[pos - 1 - i] for i in range(_N)]
    if any(nan(v) for v in vals + vals1):
        return None
    sma5 = sum(vals) / _N
    sma5_1 = sum(vals1) / _N
    # Long: SMA5 just crossed below SMA10 (bearish cross), price already below SMA5
    if sma5_1 > s10_1 and sma5 < s10 and c < sma5:
        return "long"
    # Short: SMA5 just crossed above SMA10 (bullish cross), price already above SMA5
    if sma5_1 < s10_1 and sma5 > s10 and c > sma5:
        return "short"
    return None
