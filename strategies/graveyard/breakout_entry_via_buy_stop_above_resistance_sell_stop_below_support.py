#!/usr/bin/env python3
"""breakout_entry_via_buy_stop_resistance -- Buy stop above Donchian upper / sell stop below Donchian lower. j_person_complete_guide."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "breakout_entry_via_buy_stop_above_resistance_sell_stop_below_support",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "high trades at or above the channel resistance (Donchian upper); price proves it may go higher",
    "short": "low trades at or below the channel support (Donchian lower); price proves it may go lower",
    "desc": "Breakout entry via buy-stop above resistance / sell-stop below support using Donchian channel extremes",
    "source": "j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """High/low penetration of Donchian channel triggers entry."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h >= dc_up:
        return "long"
    if l <= dc_lo:
        return "short"
    return None
