#!/usr/bin/env python3
"""heiken_ashi_naive_reversal_ea -- Counter-trend HA exhaustion: two consecutive same-color + expanding body. EarnForex."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "heiken_ashi_naive_reversal_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "ha_close, ha_open, high, low",
    "long": "two consecutive bearish HA + expanding body + no upper wick (exhaustion) -> buy",
    "short": "two consecutive bullish HA + expanding body + no lower wick -> sell",
    "desc": "Counter-trend: two-bar HA exhaustion with no-wick confirmation; EarnForex Naive EA",
    "source": "web:https://www.earnforex.com/metatrader-expert-advisors/Heiken-Ashi-Naive/",
}

_WICK_TOL = 0.1   # wick must be < 10% of body to count as "no wick"


def signal(ind, pos, htf=None):
    """Two-bar HA exhaustion with expanding body and suppressed opposing wick."""
    ha_c = ind["ha_close"][pos]
    ha_o = ind["ha_open"][pos]
    ha_c1 = ind["ha_close"][pos - 1]
    ha_o1 = ind["ha_open"][pos - 1]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(ha_c, ha_o, ha_c1, ha_o1, hi, lo):
        return None
    body_now = abs(ha_c - ha_o)
    body_prev = abs(ha_c1 - ha_o1)
    if body_now <= 0 or body_prev <= 0:
        return None
    # HA-derived high/low
    ha_high = max(hi, ha_o, ha_c)
    ha_low = min(lo, ha_o, ha_c)
    ha_bear = ha_c < ha_o
    ha_bull = ha_c > ha_o
    ha_was_bear = ha_c1 < ha_o1
    ha_was_bull = ha_c1 > ha_o1
    # Long: two consecutive bearish HA, expanding body, no upper wick on bear bar
    if ha_bear and ha_was_bear and body_now > body_prev:
        upper_wick = ha_high - max(ha_o, ha_c)
        if upper_wick < _WICK_TOL * body_now:
            return "long"
    # Short: two consecutive bullish HA, expanding body, no lower wick on bull bar
    if ha_bull and ha_was_bull and body_now > body_prev:
        lower_wick = min(ha_o, ha_c) - ha_low
        if lower_wick < _WICK_TOL * body_now:
            return "short"
    return None
