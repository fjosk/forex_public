#!/usr/bin/env python3
"""swing_value_vol_breakout_talon -- Talon-style swing-value volatility breakout: buy/sell at open +/- a multiple of the largest multi-day price swing (inter-bar high-low offsets). Williams/Deravin long_term_secrets Ch.4.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "swing_value_vol_breakout_talon",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "open, high, low, close",
    "long": "high >= open + 0.80 * max(high[3]-low[0], high[1]-low[3])",
    "short": "low <= open - 1.20 * max(high[3]-low[0], high[1]-low[3])",
    "desc": "Talon swing-value breakout: entry threshold derived from the largest 3-day inter-bar price swing",
    "source": "long_term_secrets_to_short_term_trading -- Ch.4 Separating Buyers from Sellers / Talon Figure 4.20 pp.71-72",
}


def signal(ind, pos, htf=None):
    """Talon: intrabar penetration of open +/- swing-value threshold."""
    if pos < 3:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    h1 = ind["high"][pos - 1]
    h3 = ind["high"][pos - 3]
    l3 = ind["low"][pos - 3]
    if nan(o, h, l, h1, h3, l3):
        return None
    # swingA = high 3 bars ago minus today's low; swingB = high 1 bar ago minus low 3 bars ago
    swing_a = h3 - l
    swing_b = h1 - l3
    swing = max(swing_a, swing_b)
    if swing <= 0:
        return None
    buy_stop = o + 0.80 * swing
    sell_stop = o - 1.20 * swing
    if h >= buy_stop:
        return "long"
    if l <= sell_stop:
        return "short"
    return None
