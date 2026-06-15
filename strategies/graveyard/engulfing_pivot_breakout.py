#!/usr/bin/env python3
"""engulfing_pivot_breakout -- Engulfing candle at S2/R2 pivot: breakout or mean-reversion. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_pivot_breakout",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "piv_r2, piv_s2, open, close",
    "long": "bullish engulfing at/below S2 (close > prior open, open < prior close)",
    "short": "bearish engulfing at/above R2",
    "desc": "Engulfing reversal pattern at S2/R2 pivot levels (mean-reversion variant)",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Bullish engulf below S2 = long; bearish engulf above R2 = short."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    r2 = ind["piv_r2"][pos]
    s2 = ind["piv_s2"][pos]
    if nan(c, o, c1, o1, r2, s2):
        return None
    # Bullish engulfing: prior bar bearish, current bullish and engulfs
    bull_engulf = c1 < o1 and c > o and o < c1 and c > o1
    # Bearish engulfing: prior bar bullish, current bearish and engulfs
    bear_engulf = c1 > o1 and c < o and o > c1 and c < o1
    if bull_engulf and c < s2:
        return "long"
    if bear_engulf and c > r2:
        return "short"
    return None
