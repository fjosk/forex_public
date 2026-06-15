#!/usr/bin/env python3
"""doji_star_pivot_filter -- Doji-star candlestick pattern with S2/R2 pivot filter. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "doji_star_pivot_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "piv_r2, piv_s2, open, high, low, close",
    "long": "bullish doji-star near/below S2 pivot (body near-zero after prior bar)",
    "short": "bearish doji-star near/above R2 pivot",
    "desc": "Doji-star reversal pattern filtered by S2/R2 pivot levels",
    "source": "web:https://github.com/zeta-zetra/code",
}

_DOJI_FRAC = 0.15   # body < 15% of bar range = doji


def signal(ind, pos, htf=None):
    """Doji-star reversal at S2 (long) or R2 (short) pivot filter."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    r2 = ind["piv_r2"][pos]
    s2 = ind["piv_s2"][pos]
    if nan(c, o, h, l, c1, o1, h1, l1, r2, s2):
        return None
    bar_range1 = h1 - l1
    if bar_range1 <= 0:
        return None
    body1 = abs(c1 - o1)
    # Current bar is a doji if body < threshold fraction of range
    bar_range = h - l
    if bar_range <= 0:
        return None
    body = abs(c - o)
    is_doji = body < _DOJI_FRAC * bar_range
    if not is_doji:
        return None
    # Doji-star: prior bar was large non-doji (gap or significant move)
    prior_non_doji = body1 >= _DOJI_FRAC * bar_range1
    if not prior_non_doji:
        return None
    # Mean-reversion variant: doji at S2 = long; at R2 = short
    if c <= s2 and o1 > c1:  # prior bearish bar pushed to S2 support
        return "long"
    if c >= r2 and o1 < c1:  # prior bullish bar pushed to R2 resistance
        return "short"
    return None
