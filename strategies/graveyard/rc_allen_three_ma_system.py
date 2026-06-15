#!/usr/bin/env python3
"""rc_allen_three_ma_system -- R.C. Allen: both shorter MAs cross above/below the longest MA. trade_your_way_to_financial_freedom_mabroke_blogsp.

Uses SMA10/SMA20/SMA50 as the short/medium/long triple.
Long entry: SMA10 > SMA50 AND SMA20 > SMA50 (both above longest).
Short entry: SMA10 < SMA50 AND SMA20 < SMA50.
Exit (TREND, not TREND_FLIP): short MA crosses back through medium.
"""
from strategies._common import nan, TREND, ALL_CLASSES, _xdn, _xup

META = {
    "id": "rc_allen_three_ma_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma10,sma20,sma50",
    "long": "SMA10 and SMA20 both newly cross above SMA50 (short MA above medium above long)",
    "short": "SMA10 and SMA20 both newly cross below SMA50",
    "desc": "R.C. Allen three-MA: both short and medium cross above/below the longest for trend entry",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch9",
}


def signal(ind, pos, htf=None):
    """R.C. Allen system: entry when both shorter MAs cross same side of the longest."""
    if pos < 1:
        return None
    s10  = ind["sma10"][pos];  s101 = ind["sma10"][pos - 1]
    s20  = ind["sma20"][pos];  s201 = ind["sma20"][pos - 1]
    s50  = ind["sma50"][pos];  s501 = ind["sma50"][pos - 1]
    if nan(s10, s101, s20, s201, s50, s501):
        return None
    # Both short+medium above long, and at least one just crossed
    above_both = s10 > s50 and s20 > s50
    above_prev = s101 > s501 and s201 > s501
    below_both = s10 < s50 and s20 < s50
    below_prev = s101 < s501 and s201 < s501
    if above_both and not above_prev:
        return "long"
    if below_both and not below_prev:
        return "short"
    return None
