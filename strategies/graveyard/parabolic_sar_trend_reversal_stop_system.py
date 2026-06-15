#!/usr/bin/env python3
"""parabolic_sar_trend_reversal_stop_system -- Parabolic SAR direction flip triggers trend reversal entry. elder_alexander_trading_for_a_living."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_trend_reversal_stop_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "psar_dir",
    "long": "Parabolic SAR flips from above price (short) to below price (long): psar_dir turns +1",
    "short": "Parabolic SAR flips from below price (long) to above price (short): psar_dir turns -1",
    "desc": "Parabolic SAR stop-and-reverse: enter on SAR flip direction change",
    "source": "book:elder_alexander_trading_for_a_living Sec 44 p.244-247",
}


def signal(ind, pos, htf=None):
    """Enter long when PSAR flips to bullish, short when flips to bearish."""
    if pos < 1:
        return None
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    if nan(d, d1):
        return None
    # psar_dir: +1 = SAR below price (bullish), -1 = SAR above price (bearish)
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
