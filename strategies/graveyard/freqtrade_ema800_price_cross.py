#!/usr/bin/env python3
"""freqtrade_ema800_price_cross -- Price above EMA200 long; below EMA200*0.99 exit. paulcpk freqtrade."""
from strategies._common import nan, TREND, ALL_CLASSES

# EMA800 is not available; EMA200 is the longest available key and is used as the proxy.
# The buffer (0.99) is preserved to capture the original intent of avoiding whipsaws.

META = {
    "id": "freqtrade_ema800_price_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema200, close",
    "long": "close > ema200 (proxy for ema800)",
    "short": "not used (long-only); exit when close < ema200 * 0.99",
    "desc": "Long-only price cross above EMA200 (EMA800 proxy) with 1% buffer for exits",
    "source": "https://github.com/paulcpk/freqtrade-strategies-that-work/blob/master/EMAPriceCrossoverWithThreshold.py",
}


def signal(ind, pos, htf=None):
    """Price cross above EMA200 long; 1% buffer below triggers short/exit."""
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e200_1 = ind["ema200"][pos - 1]
    if nan(e200, c, c1, e200_1):
        return None
    # Entry: price crosses above ema200
    if c > e200 and c1 <= e200_1:
        return "long"
    # Reversal: price drops 1% below ema200
    if c < e200 * 0.99:
        return "short"
    return None
