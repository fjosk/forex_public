#!/usr/bin/env python3
"""awesome_oscillator_saucer -- AO saucer pattern + zero-line crossover. je-suis-tm/quant-trading GitHub."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "awesome_oscillator_saucer",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "ao, open, close",
    "long": "Bullish saucer: green bar, two prior red bars, AO rising but negative; OR AO zero cross up",
    "short": "Bearish saucer: red bar, two prior green bars, AO falling but positive; OR AO zero cross down",
    "desc": "Awesome Oscillator saucer pattern + zero-line crossover entry",
    "source": "je-suis-tm/quant-trading GitHub (Awesome Oscillator backtest.py)",
}


def signal(ind, pos, htf=None):
    """AO saucer or zero-cross momentum signal."""
    ao = ind["ao"][pos]
    ao1 = ind["ao"][pos - 1]
    ao2 = ind["ao"][pos - 2]
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    c2 = ind["close"][pos - 2]
    o2 = ind["open"][pos - 2]
    if nan(ao, ao1, ao2, c, o, c1, o1, c2, o2):
        return None
    # Saucer long: green bar, two prior reds, AO rising but stays negative
    if c > o and c1 < o1 and c2 < o2 and ao > ao1 and ao < 0:
        return "long"
    # Saucer short: red bar, two prior greens, AO falling but stays positive
    if c < o and c1 > o1 and c2 > o2 and ao < ao1 and ao > 0:
        return "short"
    # Zero-line cross
    if ao > 0 and ao1 <= 0:
        return "long"
    if ao < 0 and ao1 >= 0:
        return "short"
    return None
