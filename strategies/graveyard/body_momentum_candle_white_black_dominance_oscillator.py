#!/usr/bin/env python3
"""body_momentum_candle_white_black_dominance_oscillator -- 14-bar body momentum oscillator: whites dominate (>70) = long bias, blacks dominate (<20) = short bias. trading_systems_and_methods_kaufman_perry_j_kaufma Ch9."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "body_momentum_candle_white_black_dominance_oscillator",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "body_mom",
    "long": "body_mom > 70 (white/bullish candles dominate over 14 bars)",
    "short": "body_mom < 20 (black/bearish candles dominate over 14 bars)",
    "desc": "14-bar candle body momentum oscillator: whites dominate (>70) long, blacks dominate (<20) short",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch9",
}

OB = 70.0
OS = 20.0


def signal(ind, pos, htf=None):
    """Long when body_mom crosses above 70; short when it crosses below 20."""
    if pos < 1:
        return None
    bm = ind["body_mom"][pos]
    bm1 = ind["body_mom"][pos - 1]
    if nan(bm, bm1):
        return None
    if bm > OB and bm1 <= OB:
        return "long"
    if bm < OS and bm1 >= OS:
        return "short"
    return None
