#!/usr/bin/env python3
"""volatility_contraction_channel_touch -- NR2 contraction + 25-bar channel touch entry.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_contraction_channel_touch",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "high, low, close",
    "long": "range[-1] < range[-2] AND close equals 25-bar high of closes",
    "short": "range[-1] < range[-2] AND close equals 25-bar low of closes",
    "desc": "Volatility contraction + channel touch: NR2 bar followed by close at 25-bar price extreme",
    "source": "github.com/zeta-zetra/code filtered_entry.py",
}


def signal(ind, pos, htf=None):
    """Volatility contraction + 25-bar channel touch."""
    if pos < 26:
        return None
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    h2 = ind["high"][pos - 2]
    l2 = ind["low"][pos - 2]
    c0 = ind["close"][pos]
    if nan(h1, l1, h2, l2, c0):
        return None
    # Range contraction: prior bar narrower than two bars back
    range_t1 = h1 - l1
    range_t2 = h2 - l2
    if range_t1 >= range_t2:
        return None
    # 25-bar channel of closes
    closes = [ind["close"][pos - i] for i in range(25)]
    if any(nan(v) for v in closes):
        return None
    upper_25 = max(closes)
    lower_25 = min(closes)
    if c0 >= upper_25:
        return "long"
    if c0 <= lower_25:
        return "short"
    return None
