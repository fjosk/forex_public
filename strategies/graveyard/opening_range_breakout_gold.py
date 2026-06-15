#!/usr/bin/env python3
"""opening_range_breakout_gold -- XAU initial balance breakout at London open. web:tradethatswing."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "opening_range_breakout_gold",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m",
    "indicators": "hour_utc, high, low, close, atr",
    "long": "close above IB high (London open 07:00-08:00 UTC) after IB closes",
    "short": "close below IB low after the initial balance window",
    "desc": "Gold/XAU initial balance breakout: London open first-hour range as the IB",
    "source": "web:https://tradethatswing.com/initial-balance-breakout-gold-strategy-411-in-last-year-fully-automatable/",
}

_IB_HOUR = 7   # initial balance hour (07:00-08:00 UTC = London open)
_ENTRY_START = 8
_ENTRY_END = 14
_LOOKBACK = 30


def signal(ind, pos, htf=None):
    """Gold initial balance breakout."""
    c = ind["close"][pos]
    hu = ind["hour_utc"][pos]
    atr = ind["atr"][pos]
    if nan(c, hu, atr):
        return None
    hu_int = int(hu)
    if not (_ENTRY_START <= hu_int <= _ENTRY_END):
        return None
    ib_high = None
    ib_low = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        h_i = ind["hour_utc"][i]
        if nan(h_i):
            continue
        if int(h_i) == _IB_HOUR:
            bh = ind["high"][i]
            bl = ind["low"][i]
            if nan(bh, bl):
                continue
            if ib_high is None or bh > ib_high:
                ib_high = bh
            if ib_low is None or bl < ib_low:
                ib_low = bl
    if ib_high is None or ib_low is None:
        return None
    ib_range = ib_high - ib_low
    if ib_range <= 0:
        return None
    # Abnormal volatility filter: skip if IB range > 2x ATR
    if ib_range > 2.0 * atr:
        return None
    if c > ib_high:
        return "long"
    if c < ib_low:
        return "short"
    return None
