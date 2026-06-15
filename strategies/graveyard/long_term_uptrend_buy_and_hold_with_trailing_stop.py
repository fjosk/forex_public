#!/usr/bin/env python3
"""long_term_uptrend_buy_and_hold_with_trailing_stop -- Price above rising SMA200 as long-term uptrend entry; short when price below falling SMA200. the_naked_trader."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "long_term_uptrend_buy_and_hold_with_trailing_stop",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, sma200, sma200_dir",
    "long": "Price above SMA200 AND SMA200 is rising (smooth long-term uptrend)",
    "short": "Price below SMA200 AND SMA200 is falling",
    "desc": "Long-term uptrend: price above rising SMA200; ride with trailing stop",
    "source": "book:the_naked_trader_how_anyone_can_still_make_money_t Ch 4",
}


def signal(ind, pos, htf=None):
    """Long when price above rising SMA200; short when price below falling SMA200."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    sma_dir = ind["sma200_dir"][pos]
    if nan(c, sma, sma_dir):
        return None
    # sma200_dir > 0 = rising, < 0 = falling
    if c > sma and sma_dir > 0:
        return "long"
    if c < sma and sma_dir < 0:
        return "short"
    return None
