#!/usr/bin/env python3
"""engulfing_bar_reversal -- Bullish/bearish engulfing bar at pivot S/R or RSI extreme. web:forexfactory.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_bar_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "open, high, low, close, rsi, piv_s1, piv_r1",
    "long": "bullish engulfing (close > prior high, open < prior low, green) at support or RSI < 40",
    "short": "bearish engulfing (close < prior low, open > prior high, red) at resistance or RSI > 60",
    "desc": "Engulfing bar reversal at pivot S/R level or RSI extreme zone",
    "source": "web:https://www.forexfactory.com/thread/915933-engulfing",
}


def signal(ind, pos, htf=None):
    """Engulfing candle reversal at support/resistance."""
    c, o = ind["close"][pos], ind["open"][pos]
    c1, o1 = ind["close"][pos - 1], ind["open"][pos - 1]
    hi1, lo1 = ind["high"][pos - 1], ind["low"][pos - 1]
    rs = ind["rsi"][pos]
    s1, r1 = ind["piv_s1"][pos], ind["piv_r1"][pos]
    if nan(c, o, c1, o1, hi1, lo1, rs, s1, r1):
        return None
    # Bullish engulfing: close > prior high, open < prior low, green candle
    bull_engulf = c > hi1 and o < lo1 and c > o
    at_support = lo1 <= s1 or rs < 40
    if bull_engulf and at_support:
        return "long"
    # Bearish engulfing: close < prior low, open > prior high, red candle
    bear_engulf = c < lo1 and o > hi1 and c < o
    at_resist = hi1 >= r1 or rs > 60
    if bear_engulf and at_resist:
        return "short"
    return None
