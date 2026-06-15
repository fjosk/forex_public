#!/usr/bin/env python3
"""harami_pivot_filter -- Harami reversal candlestick at S2/R2 pivot levels. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "harami_pivot_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "piv_r2, piv_s2, open, high, low, close",
    "long": "bullish harami (small body inside prior bearish body) AND close < S2",
    "short": "bearish harami AND close > R2",
    "desc": "Harami reversal at S2/R2 pivot: small inside candle signals exhaustion and reversal",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """Bullish harami below S2 = long; bearish harami above R2 = short."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    r2 = ind["piv_r2"][pos]
    s2 = ind["piv_s2"][pos]
    if nan(c, o, c1, o1, r2, s2):
        return None
    # Harami: current body is entirely inside the prior body AND direction changes
    body_lo = min(o, c)
    body_hi = max(o, c)
    prior_lo = min(o1, c1)
    prior_hi = max(o1, c1)
    inside = body_lo > prior_lo and body_hi < prior_hi
    if not inside:
        return None
    # Bullish harami: prior was bearish, current bullish
    bull_harami = c1 < o1 and c > o
    # Bearish harami: prior was bullish, current bearish
    bear_harami = c1 > o1 and c < o
    if bull_harami and c < s2:
        return "long"
    if bear_harami and c > r2:
        return "short"
    return None
