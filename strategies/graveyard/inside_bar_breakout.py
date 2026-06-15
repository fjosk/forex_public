#!/usr/bin/env python3
"""inside_bar_breakout -- Inside bar (high <= prior high, low >= prior low) breakout on next bar. j_person_complete_guide."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "inside_bar_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "high, low",
    "long": "prior bar is an inside bar; current high exceeds inside bar high",
    "short": "prior bar is an inside bar; current low falls below inside bar low",
    "desc": "Inside bar breakout: volatility compression candle followed by directional break",
    "source": "j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Inside-bar pattern at pos-1; breakout at pos."""
    if pos < 2:
        return None
    h = ind["high"]
    l = ind["low"]
    # Check if pos-1 is an inside bar relative to pos-2
    if nan(h[pos], l[pos], h[pos - 1], l[pos - 1], h[pos - 2], l[pos - 2]):
        return None
    inside = h[pos - 1] <= h[pos - 2] and l[pos - 1] >= l[pos - 2]
    if not inside:
        return None
    if h[pos] > h[pos - 1]:
        return "long"
    if l[pos] < l[pos - 1]:
        return "short"
    return None
