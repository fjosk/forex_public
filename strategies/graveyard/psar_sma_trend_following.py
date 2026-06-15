#!/usr/bin/env python3
"""psar_sma_trend_following -- Parabolic SAR flip filtered by SMA200 trend. web:forextester.com.

SMA200 as long-term bias; PSAR flip provides entry timing. Only longs above SMA200,
only shorts below. PSAR line trails the trade. No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "psar_sma_trend_following",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "psar_dir, sma200",
    "long": "close > sma200 AND psar_dir flips from -1 to +1",
    "short": "close < sma200 AND psar_dir flips from +1 to -1",
    "desc": "Parabolic SAR flip as entry, SMA200 as trend filter",
    "source": "web:https://forextester.com/blog/parabolic-sar-moving-average-strategy/",
}


def signal(ind, pos, htf=None):
    """PSAR flip entry with SMA200 trend filter."""
    c = ind["close"][pos]
    sma = ind["sma200"][pos]
    pdir = ind["psar_dir"][pos]
    pdirp = ind["psar_dir"][pos - 1]
    if nan(c, sma, pdir, pdirp):
        return None
    if c > sma and pdir == 1 and pdirp == -1:
        return "long"
    if c < sma and pdir == -1 and pdirp == 1:
        return "short"
    return None
