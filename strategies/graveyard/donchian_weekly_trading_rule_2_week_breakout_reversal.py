#!/usr/bin/env python3
"""donchian_weekly_trading_rule_2week -- 2-week (10-bar) Donchian stop-and-reverse. the_complete_turtletrader."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "donchian_weekly_trading_rule_2_week_breakout_reversal",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, high, low",
    "long": "price moves above the highest high of prior 2 calendar weeks (~10 bars); cover short",
    "short": "price falls below the lowest low of prior 2 calendar weeks; liquidate long",
    "desc": "Donchian Weekly Trading Rule: 2-week channel breakout, always-in stop-and-reverse (Donchian original)",
    "source": "the_complete_turtletrader_nodrm",
}


def signal(ind, pos, htf=None):
    """2-week Donchian stop-and-reverse breakout."""
    if pos < 2:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, l, dc_up, dc_lo):
        return None
    if h > dc_up:
        return "long"
    if l < dc_lo:
        return "short"
    return None
