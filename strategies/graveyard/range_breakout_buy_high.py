#!/usr/bin/env python3
"""range_breakout_buy_high -- Buy-high-sell-higher: enter breakout above range high without waiting for pullback.
calm_trader_steve_burns.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "range_breakout_buy_high",
    "cadences": ["swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, dc_lo, close",
    "long": "close > Donchian upper (range breakout; take the breakout immediately, no pullback)",
    "short": "close < Donchian lower (breakdown below range low)",
    "desc": "Buy-high-sell-higher range breakout: enter on close above prior range high without waiting for pullback",
    "source": "book: calm_trader_win_in_the_stock_market_steve_burns",
}


def signal(ind, pos, htf=None):
    """Enter on the breakout bar itself; do not wait for a pullback."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(c, dc_up, dc_lo):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
