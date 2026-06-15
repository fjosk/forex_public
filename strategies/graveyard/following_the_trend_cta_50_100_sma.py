#!/usr/bin/env python3
"""following_the_trend_cta_50_100_sma -- Clenow CTA: SMA50/100 filter + 50-bar high breakout. web:https://www.followingthetrend.com/the-trading-system/trading-system-rules/"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "following_the_trend_cta_50_100_sma",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "sma50, sma100, close",
    "long": "sma50 > sma100 AND close is 50-bar high",
    "short": "sma50 < sma100 AND close is 50-bar low",
    "desc": "Clenow CTA replication: SMA50/100 trend filter with 50-day breakout entry",
    "source": "web:https://www.followingthetrend.com/the-trading-system/trading-system-rules/",
}


def signal(ind, pos, htf=None):
    """SMA50 > SMA100 regime + new 50-bar close high breakout."""
    if pos < 50:
        return None
    sma50 = ind["sma50"][pos]
    sma100 = ind["sma100"][pos]
    c = ind["close"][pos]
    if nan(sma50, sma100, c):
        return None
    closes = ind["close"][pos - 50:pos]
    if any(nan(v) for v in closes):
        return None
    trend_up = sma50 > sma100
    trend_dn = sma50 < sma100
    new_hi = c >= max(closes)
    new_lo = c <= min(closes)
    if trend_up and new_hi:
        return "long"
    if trend_dn and new_lo:
        return "short"
    return None
