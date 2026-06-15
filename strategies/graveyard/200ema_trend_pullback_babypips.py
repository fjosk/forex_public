#!/usr/bin/env python3
"""200ema_trend_pullback_babypips -- 200 EMA trend pullback confirmation candle during London-NY overlap. web:babypips.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "200ema_trend_pullback_babypips",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema200, close, body_mom, hour_utc",
    "long": "close above ema200, prior bar dipped then resumed up, bullish body, London-NY overlap",
    "short": "close below ema200, prior bar bounced then resumed down, bearish body, London-NY overlap",
    "desc": "200 EMA daily trend pullback confirmation candle during London-NY session",
    "source": "web:https://forums.babypips.com/t/insanely-stupid-and-easy-forex-trading-strategy/476480",
}


def signal(ind, pos, htf=None):
    """200 EMA trend pullback: dip/bounce then resumption candle in session window."""
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    bm = ind["body_mom"][pos]
    hr = ind["hour_utc"][pos]
    if nan(e200, c, c1, c2, bm, hr):
        return None
    # London-NY overlap: 13-17 UTC
    in_session = 13 <= hr <= 17
    if not in_session:
        return None
    # Long: above EMA, prior bar dipped (c1 < c2), current bar resumes (c > c1), bullish body
    if c > e200 and c1 < c2 and c > c1 and bm > 0:
        return "long"
    # Short: below EMA, prior bar bounced (c1 > c2), current bar resumes (c < c1), bearish body
    if c < e200 and c1 > c2 and c < c1 and bm < 0:
        return "short"
    return None
