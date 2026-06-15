#!/usr/bin/env python3
"""adx_ema14_trend_filter -- ADX crosses above 25, then EMA13 (proxy for EMA14) entry. ForexTester.

Wait for ADX to cross above 25 (trend beginning). Then enter long if close > EMA13 on a
bullish body (body_mom > 0), short if close < EMA13 on a bearish body.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_ema14_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "adx, ema13 (proxy for ema14), body_mom",
    "long": "ADX > 25 and close > EMA13 and body_mom > 0",
    "short": "ADX > 25 and close < EMA13 and body_mom < 0",
    "desc": "ADX trend-start filter with EMA13/body direction entry (ForexTester variant)",
    "source": "web:https://forextester.com/blog/adx-14-ema-strategy/",
}


def signal(ind, pos, htf=None):
    """ADX > 25 onset + EMA13 + body direction."""
    adx_v = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    e13 = ind["ema13"][pos]
    bm = ind["body_mom"][pos]
    c = ind["close"][pos]
    if nan(adx_v, adx1, e13, bm, c):
        return None
    # ADX must be above 25 (not just crossing; accept any bar when ADX > 25)
    if adx_v < 25:
        return None
    if c > e13 and bm > 0:
        return "long"
    if c < e13 and bm < 0:
        return "short"
    return None
