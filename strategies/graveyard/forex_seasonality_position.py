#!/usr/bin/env python3
"""forex_seasonality_position -- Forex seasonality bias + EMA50 technical filter.

Uses calendar month as a directional bias layer, confirmed by price vs EMA50.
Seasonal windows encoded from historical research (Fusion Markets / Admiral Markets):
  EUR/USD bull months: April, July, December; bear: January, February, September, October.
  Gold (XAU) bull months: January, August, September, October.
Operates as a confluence filter: only fires if technical trend aligns with season.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "forex_seasonality_position",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "position",
    "tf": "daily",
    "indicators": "open_time, ema50, rsi, close",
    "long": "seasonal bull window for pair AND close > ema50 (technical trend aligned)",
    "short": "seasonal bear window AND close < ema50",
    "desc": "Forex seasonality position: calendar month bias confirmed by EMA50 trend",
    "source": "web:https://fusionmarkets.com/posts/Understanding-Forex-Seasonality",
}

# Month sets: defined for EUR/USD as the representative major pair
# Long months: April(4), July(7), December(12)
# Short months: January(1), February(2), September(9), October(10)
_BULL_MONTHS = {4, 7, 12}
_BEAR_MONTHS = {1, 2, 9, 10}


def signal(ind, pos, htf=None):
    """Forex seasonality position with EMA50 technical filter."""
    ts = ind["open_time"][pos]
    c = ind["close"][pos]
    ema50 = ind["ema50"][pos]
    rsi = ind["rsi"][pos]
    if nan(ts, c, ema50, rsi):
        return None
    # Only fire on the first bar of a new month (month transition)
    ts1 = ind["open_time"][pos - 1]
    if nan(ts1):
        return None
    dt0 = datetime.datetime.utcfromtimestamp(ts / 1000)
    dt1 = datetime.datetime.utcfromtimestamp(ts1 / 1000)
    m0 = dt0.month
    if m0 == dt1.month:
        return None   # not month transition
    if m0 in _BULL_MONTHS and c > ema50:
        return "long"
    if m0 in _BEAR_MONTHS and c < ema50:
        return "short"
    return None
