#!/usr/bin/env python3
"""elder_ray_bull_power_bear_power_entry -- Elder-ray entry: uptrend + bear power negative and ticking up = long; downtrend + bull power positive and ticking down = short. come_into_my_trading_room_alexander_elder Ch5."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_ray_bull_power_bear_power_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "bull_power,bear_power,ema20",
    "long": "EMA rising AND bear_power < 0 AND bear_power ticks up (bears losing grip in uptrend)",
    "short": "EMA falling AND bull_power > 0 AND bull_power ticks down (bulls slipping in downtrend)",
    "desc": "Elder-ray: buy dips in uptrend when bear power is negative and turns up; sell rallies in downtrend when bull power positive and turns down",
    "source": "book: come_into_my_trading_room_alexander_elder, Ch5",
}


def signal(ind, pos, htf=None):
    """Elder-ray entry using ema20 slope as trend filter."""
    if pos < 1:
        return None
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    bp = ind["bull_power"][pos]
    bp1 = ind["bull_power"][pos - 1]
    br = ind["bear_power"][pos]
    br1 = ind["bear_power"][pos - 1]
    if nan(ema, ema1, bp, bp1, br, br1):
        return None
    if ema > ema1 and br < 0 and br > br1:
        return "long"
    if ema < ema1 and bp > 0 and bp < bp1:
        return "short"
    return None
