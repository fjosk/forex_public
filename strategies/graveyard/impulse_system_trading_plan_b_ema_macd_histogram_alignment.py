#!/usr/bin/env python3
"""impulse_system_trading_plan_b_ema_macd_histogram_alignment -- Elder Impulse System: EMA slope AND MACD-Histogram slope both up/down simultaneously. come_into_my_trading_room_alexander_elder."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "impulse_system_trading_plan_b_ema_macd_histogram_alignment",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema20, macd_hist",
    "long": "EMA20 rising AND MACD-Histogram rising (both slopes positive simultaneously)",
    "short": "EMA20 falling AND MACD-Histogram falling (both slopes negative simultaneously)",
    "desc": "Elder Impulse System: EMA and MACD-Histogram alignment signals powerful trend impulse",
    "source": "book:come_into_my_trading_room_alexander_elder pp.260-263",
}


def signal(ind, pos, htf=None):
    """Impulse green = EMA rising + MACD-Hist rising; red = both falling."""
    if pos < 1:
        return None
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    mh = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    if nan(ema, ema1, mh, mh1):
        return None
    ema_up = ema > ema1
    ema_dn = ema < ema1
    hist_up = mh > mh1
    hist_dn = mh < mh1
    if ema_up and hist_up:
        return "long"
    if ema_dn and hist_dn:
        return "short"
    return None
