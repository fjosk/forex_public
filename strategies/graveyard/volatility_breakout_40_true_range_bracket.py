#!/usr/bin/env python3
"""volatility_breakout_40_true_range_bracket -- Intraday volatility breakout: enter when price
moves 40% of prior-bar true range away from the day open.
Trade Your Way to Financial Freedom, Ch.1."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_breakout_40_true_range_bracket",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "day_open,high,low,close",
    "long": "high > day_open + 0.40 * prior-bar true range",
    "short": "low < day_open - 0.40 * prior-bar true range",
    "desc": "40% true-range bracket around day open: breakout triggers directional entry",
    "source": "Trade Your Way to Financial Freedom, Ch.1 'The Legend of the Holy Grail'",
}

_ATR_K = 0.40


def signal(ind, pos, htf=None):
    """Intraday volatility breakout: high/low vs day_open +/- 40% of prior bar TR."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    do = ind["day_open"][pos]
    # Prior bar true range (using high/low of previous bar; no explicit prev_close needed
    # since we approximate TR as high-low of prior bar which is the dominant component on FX)
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(h, l, do, h1, l1, c1):
        return None
    # True range = max(high, prior_close) - min(low, prior_close)
    if pos >= 2:
        c2 = ind["close"][pos - 2]
        if not nan(c2):
            tr = max(h1, c2) - min(l1, c2)
        else:
            tr = h1 - l1
    else:
        tr = h1 - l1
    if tr <= 0:
        return None
    band = _ATR_K * tr
    if h > do + band:
        return "long"
    if l < do - band:
        return "short"
    return None
