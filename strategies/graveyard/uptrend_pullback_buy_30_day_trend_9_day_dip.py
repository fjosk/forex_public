#!/usr/bin/env python3
"""uptrend_pullback_buy_30_day_trend_9_day_dip -- Buy when close > close[30] (uptrend) AND
close < close[9] (short pullback); mirror short.

Source: long_term_secrets_to_short_term_trading, Ch.7 pp.94-95.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "uptrend_pullback_buy_30_day_trend_9_day_dip",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "close > close[30] (uptrend) AND close < close[9] (9-bar pullback in progress)",
    "short": "close < close[30] (downtrend) AND close > close[9] (9-bar bounce in downtrend)",
    "desc": "30-bar trend + 9-bar dip pullback buy (or short into bounce); Williams-style trend-pullback",
    "source": "long_term_secrets_to_short_term_trading Ch.7 pp.94-95",
}


def signal(ind, pos, htf=None):
    """30-bar trend direction + 9-bar retracement condition."""
    if pos < 30:
        return None
    c0 = ind["close"][pos]
    c9 = ind["close"][pos - 9]
    c30 = ind["close"][pos - 30]
    if nan(c0, c9, c30):
        return None
    if c0 > c30 and c0 < c9:
        return "long"
    if c0 < c30 and c0 > c9:
        return "short"
    return None
