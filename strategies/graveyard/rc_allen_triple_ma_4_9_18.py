#!/usr/bin/env python3
"""rc_allen_triple_ma_4_9_18 -- R.C. Allen 4-9-18 triple MA system with neutral zone. trade_your_way_to_financial_freedom_mabroke_blogsp.

Original: SMA(4), SMA(9), SMA(18). Closest available: EMA(5), EMA(9), EMA(20).
Long entry: EMA5 > EMA20 AND EMA9 > EMA20 (both above 18-equiv).
Short entry: EMA5 < EMA20 AND EMA9 < EMA20.
Exit when EMA5 crosses back through EMA9 (shortest re-crosses medium = neutral; TREND archetype stops on ATR).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rc_allen_triple_ma_4_9_18",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema5,ema9,ema20",
    "long": "EMA5 and EMA9 both cross above EMA20 (4-9-18 equiv long entry)",
    "short": "EMA5 and EMA9 both cross below EMA20 (4-9-18 equiv short entry)",
    "desc": "R.C. Allen 4-9-18 triple MA with neutral zone: EMA5/9/20 as 4/9/18 proxies",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch8",
}


def signal(ind, pos, htf=None):
    """R.C. Allen 4-9-18: both short and medium cross above/below the long MA."""
    if pos < 1:
        return None
    e5  = ind["ema5"][pos];  e51 = ind["ema5"][pos - 1]
    e9  = ind["ema9"][pos];  e91 = ind["ema9"][pos - 1]
    e20 = ind["ema20"][pos]; e201 = ind["ema20"][pos - 1]
    if nan(e5, e51, e9, e91, e20, e201):
        return None
    above_both = e5 > e20 and e9 > e20
    above_prev = e51 > e201 and e91 > e201
    below_both = e5 < e20 and e9 < e20
    below_prev = e51 < e201 and e91 < e201
    if above_both and not above_prev:
        return "long"
    if below_both and not below_prev:
        return "short"
    return None
