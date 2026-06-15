#!/usr/bin/env python3
"""hma_dual_period -- HMA21 direction change confirmed by EMA200 trend. hasnocool."""
from strategies._common import nan, TREND, ALL_CLASSES

# Source uses HMA50 (short) and HMA200 (long); we proxy with hma21 (short) and ema200 (long trend).

META = {
    "id": "hma_dual_period",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "hma21, ema200",
    "long": "hma21 changes from decreasing to increasing AND ema200 is increasing",
    "short": "hma21 changes from increasing to decreasing AND ema200 is decreasing",
    "desc": "Dual-period HMA: short HMA direction flip confirmed by long EMA200 trend",
    "source": "https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Hull%20Moving%20Average%20based%20strategy.pine",
}


def signal(ind, pos, htf=None):
    """HMA21 slope reversal with EMA200 direction filter."""
    h = ind["hma21"][pos]
    h1 = ind["hma21"][pos - 1]
    h2 = ind["hma21"][pos - 2] if pos >= 2 else float("nan")
    e200 = ind["ema200"][pos]
    e200_1 = ind["ema200"][pos - 1]
    if nan(h, h1, h2, e200, e200_1):
        return None
    # HMA was falling (h1 < h2) and now rising (h > h1) = direction flip up
    hma_flip_up = h > h1 and h1 < h2
    # HMA was rising and now falling = direction flip down
    hma_flip_dn = h < h1 and h1 > h2
    e200_rising = e200 > e200_1
    e200_falling = e200 < e200_1
    if hma_flip_up and e200_rising:
        return "long"
    if hma_flip_dn and e200_falling:
        return "short"
    return None
