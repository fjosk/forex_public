#!/usr/bin/env python3
"""take_day_trade_overnight_close_near_extreme -- When the bar closes within 0.15*ATR of its
high, the next bar tends to exceed that high; mirror for close near the low.
come_into_my_trading_room_alexander_elder.

Long: close[pos] >= high[pos] - 0.15*atr[pos] (closed near the high).
Short: close[pos] <= low[pos] + 0.15*atr[pos] (closed near the low).
Signal fires on the current bar; engine enters on the next open.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "take_day_trade_overnight_close_near_extreme",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "high,low,close,atr",
    "long": "close within 0.15*ATR of the bar high - expect follow-through above the high next bar",
    "short": "close within 0.15*ATR of the bar low - expect follow-through below the low next bar",
    "desc": "Close-near-extreme continuation: bar closing on its extreme typically extends in that direction next bar",
    "source": "come_into_my_trading_room_alexander_elder Ch.6 Taking Day-Trades Overnight (pp.149-150)",
}


def signal(ind, pos, htf=None):
    """Signal when close is within a tight band of the bar's high or low."""
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    c  = ind["close"][pos]
    a  = ind["atr"][pos]
    if nan(hi, lo, c, a) or a <= 0:
        return None
    band = 0.15 * a
    if c >= hi - band:
        return "long"
    if c <= lo + band:
        return "short"
    return None
