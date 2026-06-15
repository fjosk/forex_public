#!/usr/bin/env python3
"""ssl_channel -- SSL Channel (Semaphore Signal Level) flip with EMA200 + MACD filter. web:ataquant.com.

ssl_hlv flip from -1 to +1 = long; +1 to -1 = short. Confirmed by ema200 side and
MACD histogram positive/negative. No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ssl_channel",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ssl_hlv, ema200, macd_hist",
    "long": "ssl_hlv flips -1 to +1 AND close > ema200 AND macd_hist > 0",
    "short": "ssl_hlv flips +1 to -1 AND close < ema200 AND macd_hist < 0",
    "desc": "SSL Channel flip with EMA200 trend filter and MACD histogram confirmation",
    "source": "web:https://ataquant.com/ssl-channel-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """SSL hlv flip with EMA200 and MACD histogram confirmation."""
    hlv = ind["ssl_hlv"][pos]
    hlvp = ind["ssl_hlv"][pos - 1]
    c = ind["close"][pos]
    ema = ind["ema200"][pos]
    mh = ind["macd_hist"][pos]
    if nan(hlv, hlvp, c, ema, mh):
        return None
    if hlv == 1 and hlvp == -1 and c > ema and mh > 0:
        return "long"
    if hlv == -1 and hlvp == 1 and c < ema and mh < 0:
        return "short"
    return None
