#!/usr/bin/env python3
"""weekly_monday_tuesday_breakout -- Mon-Tue weekly range breakout on Wed-Fri. web:forexfactory."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "weekly_monday_tuesday_breakout",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "dow, high, low, close",
    "long": "Wed-Fri, close breaks above Mon-Tue range high + 15% extension",
    "short": "Wed-Fri, close breaks below Mon-Tue range low - 15% extension",
    "desc": "Monday-Tuesday weekly range breakout: enter on Wed-Fri if price clears the extended Mon-Tue range",
    "source": "web:https://www.forexfactory.com/thread/976730-simple-monday-tuesday-system-attached-calculator",
}

_LOOKBACK = 10  # enough to find Mon and Tue in the same week


def signal(ind, pos, htf=None):
    """Mon-Tue range breakout on Wed-Fri."""
    c = ind["close"][pos]
    dow = ind["dow"][pos]
    if nan(c, dow):
        return None
    # Only fire on Wednesday(2), Thursday(3), Friday(4)
    # dow: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri (standard weekday numbering)
    if int(dow) not in (2, 3, 4):
        return None
    mon_hi = None
    mon_lo = None
    tue_hi = None
    tue_lo = None
    start = max(1, pos - _LOOKBACK)
    for i in range(start, pos):
        d_i = ind["dow"][i]
        if nan(d_i):
            continue
        bh = ind["high"][i]
        bl = ind["low"][i]
        if nan(bh, bl):
            continue
        if int(d_i) == 0:  # Monday
            if mon_hi is None or bh > mon_hi:
                mon_hi = bh
            if mon_lo is None or bl < mon_lo:
                mon_lo = bl
        elif int(d_i) == 1:  # Tuesday
            if tue_hi is None or bh > tue_hi:
                tue_hi = bh
            if tue_lo is None or bl < tue_lo:
                tue_lo = bl
    if mon_hi is None or mon_lo is None or tue_hi is None or tue_lo is None:
        return None
    range_hi = max(mon_hi, tue_hi)
    range_lo = min(mon_lo, tue_lo)
    rng = range_hi - range_lo
    if rng <= 0:
        return None
    buy_stop = range_hi + 0.15 * rng
    sell_stop = range_lo - 0.15 * rng
    if c > buy_stop:
        return "long"
    if c < sell_stop:
        return "short"
    return None
