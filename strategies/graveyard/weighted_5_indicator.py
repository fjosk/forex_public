#!/usr/bin/env python3
"""weighted_5_indicator -- 5-indicator consensus vote (>= 2 of 5 agree). AlbertoCuadra/algo_trading.

MACD, StochRSI, RSI, SuperTrend, EMA cross each score 1; enter if >= 2 sub-signals agree.
Low confidence due to author's own curve-fitting warning.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "weighted_5_indicator",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd, macd_sig, srsi_k, srsi_d, rsi, st_dir, ema20, ema50",
    "long": "At least 2 of 5 sub-signals bullish: MACD cross up, srsi_k cross from OS, RSI rising, ST bull, EMA20>50",
    "short": "At least 2 of 5 sub-signals bearish: MACD cross dn, srsi_k cross from OB, RSI falling, ST bear, EMA20<50",
    "desc": "Weighted 5-indicator consensus vote (>= 2 of 5 must agree)",
    "source": "https://github.com/AlbertoCuadra/algo_trading_weighted_strategy weighted_strategy.pine",
}

_WEIGHT = 2


def signal(ind, pos, htf=None):
    """5-indicator vote: >= 2 bull or >= 2 bear sub-signals."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    sk = ind["srsi_k"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    sd = ind["srsi_d"][pos]
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    st = ind["st_dir"][pos]
    e20 = ind["ema20"][pos]
    e50 = ind["ema50"][pos]
    if nan(m, ms, m1, ms1, sk, sk1, sd, r, r1, st, e20, e50):
        return None
    bull = 0
    bear = 0
    # MACD cross
    if m > ms and m1 <= ms1:
        bull += 1
    elif m < ms and m1 >= ms1:
        bear += 1
    # StochRSI: k crosses d from oversold
    if sk > sd and sk1 <= sd and sk < 20:
        bull += 1
    elif sk < sd and sk1 >= sd and sk > 80:
        bear += 1
    # RSI direction
    if r > r1:
        bull += 1
    else:
        bear += 1
    # SuperTrend
    if st == 1:
        bull += 1
    elif st == -1:
        bear += 1
    # EMA cross
    if e20 > e50:
        bull += 1
    elif e20 < e50:
        bear += 1
    if bull >= _WEIGHT and bull > bear:
        return "long"
    if bear >= _WEIGHT and bear > bull:
        return "short"
    return None
