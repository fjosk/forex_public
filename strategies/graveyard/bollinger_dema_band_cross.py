#!/usr/bin/env python3
"""bollinger_dema_band_cross -- Bollinger Bands + DEMA Band-Cross Mean Reversion. AM2 MQL5."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_dema_band_cross",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "bb_lo, bb_up, dema20",
    "long": "DEMA rising AND bullish candle crosses back inside lower BB from below",
    "short": "DEMA falling AND bearish candle crosses back inside upper BB from above",
    "desc": "BB re-entry fade with DEMA direction confirmation (AM2 MQL5 EA)",
    "source": "mql5.com/en/code/166 Bollinger DEMA EA by AM2",
}


def signal(ind, pos, htf=None):
    """DEMA-direction-filtered BB re-entry cross."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    o = ind["open"][pos]
    bbl = ind["bb_lo"][pos]
    bbl1 = ind["bb_lo"][pos - 1]
    bbu = ind["bb_up"][pos]
    bbu1 = ind["bb_up"][pos - 1]
    d = ind["dema20"][pos]
    d1 = ind["dema20"][pos - 1]
    if nan(c, c1, o, bbl, bbl1, bbu, bbu1, d, d1):
        return None
    bull_candle = c > o
    bear_candle = c < o
    bull_cross_lower = c1 < bbl1 and c > bbl
    bear_cross_upper = c1 > bbu1 and c < bbu
    dema_rising = d > d1
    dema_falling = d < d1
    if dema_rising and bull_cross_lower and bull_candle:
        return "long"
    if dema_falling and bear_cross_upper and bear_candle:
        return "short"
    return None
