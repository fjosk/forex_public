#!/usr/bin/env python3
"""hull_suite -- HMA21 direction signal (current vs 2-bar-ago). web:https://www.tradingview.com/script/hg92pFwS-Hull-Suite/"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "hull_suite",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "hma21, sma200, close",
    "long": "hma21 > hma21[2] (turning up 2 bars ago), close > sma200",
    "short": "hma21 < hma21[2] (turning down 2 bars ago), close < sma200",
    "desc": "Hull Suite: HMA21 turns up relative to 2 bars ago, SMA200 macro filter",
    "source": "web:https://www.tradingview.com/script/hg92pFwS-Hull-Suite/",
}


def signal(ind, pos, htf=None):
    """HMA21 direction vs its value 2 bars ago with SMA200 regime filter."""
    if pos < 2:
        return None
    hma = ind["hma21"][pos]
    hma2 = ind["hma21"][pos - 2]
    hma1 = ind["hma21"][pos - 1]
    hma3 = ind["hma21"][pos - 3] if pos >= 3 else None
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    if nan(hma, hma2, hma1, c, s200):
        return None
    # turn detected: hma[pos-1] > hma[pos-3] and hma[pos-2] <= hma[pos-3]
    if pos >= 3 and not nan(hma3):
        bull_turn = hma1 > hma3 and hma2 <= hma3
        bear_turn = hma1 < hma3 and hma2 >= hma3
    else:
        bull_turn = hma > hma2
        bear_turn = hma < hma2
    if bull_turn and c > s200:
        return "long"
    if bear_turn and c < s200:
        return "short"
    return None
