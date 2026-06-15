#!/usr/bin/env python3
"""nr7_narrow_range_volatility_breakout -- NR7 narrow-range day breakout (Toby Crabel). StockCharts.

When today's bar range (high-low) is narrowest of the last 7 bars, volatility compression has
occurred. Trade the breakout above last bar's high (long) or below last bar's low (short).
Trend filter: close > SMA200 for longs; close < SMA200 for shorts.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "nr7_narrow_range_volatility_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "daily",
    "indicators": "high, low, close, sma200",
    "long": "NR7 condition met and close breaks above prior bar high with close > SMA200",
    "short": "NR7 condition met and close breaks below prior bar low with close < SMA200",
    "desc": "NR7 narrow-range volatility compression breakout (Toby Crabel)",
    "source": "web:https://chartschool.stockcharts.com NR7; Toby Crabel Day Trading (1990)",
}


def signal(ind, pos, htf=None):
    """NR7 breakout: narrowest range of last 7 bars, then break above/below prior bar."""
    if pos < 7:
        return None
    hi = ind["high"]
    lo = ind["low"]
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    # current bar range
    today_range = hi[pos] - lo[pos]
    if nan(today_range, c, s200):
        return None
    # NR7: today is narrowest of last 7 (compare to prior 6)
    for i in range(1, 7):
        r = hi[pos - i] - lo[pos - i]
        if nan(r):
            return None
        if today_range >= r:
            return None  # not narrowest
    # NR7 confirmed -- breakout of prior bar
    prev_hi = hi[pos - 1]
    prev_lo = lo[pos - 1]
    if nan(prev_hi, prev_lo):
        return None
    if c > prev_hi and c > s200:
        return "long"
    if c < prev_lo and c < s200:
        return "short"
    return None
