#!/usr/bin/env python3
"""day_of_week_seasonality_weekly_bar_timing -- In a bull regime (close > SMA200) buy
Monday/Tuesday weakness; in a bear regime short Monday/Tuesday strength.
elder_alexander_trading_for_a_living.

Bull = close > sma200; bear = close < sma200.
Long signal: Monday or Tuesday AND bull regime AND close below prior close (weakness to buy).
Short signal: Monday or Tuesday AND bear regime AND close above prior close (strength to short).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "day_of_week_seasonality_weekly_bar_timing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "dow,close,sma200",
    "long": "Monday or Tuesday pullback (close < prior close) in a bull market (close > SMA200)",
    "short": "Monday or Tuesday rally (close > prior close) in a bear market (close < SMA200)",
    "desc": "Day-of-week seasonality: Mon/Tue weakness in bull = buy; Mon/Tue strength in bear = short",
    "source": "elder_alexander_trading_for_a_living Sec 18 Charting",
}

# Python weekday: 0=Monday, 1=Tuesday
_BUY_DAYS  = {0, 1}
_SELL_DAYS = {0, 1}


def signal(ind, pos, htf=None):
    """Day-of-week seasonal bias with trend filter."""
    if pos < 1:
        return None
    dw   = ind["dow"][pos]
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    s200 = ind["sma200"][pos]
    if nan(dw, c, c1, s200):
        return None
    wd = int(dw)
    bull = c > s200
    bear = c < s200
    if wd in _BUY_DAYS and bull and c < c1:
        return "long"
    if wd in _SELL_DAYS and bear and c > c1:
        return "short"
    return None
