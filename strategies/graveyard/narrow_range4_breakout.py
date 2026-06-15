#!/usr/bin/env python3
"""narrow_range4_breakout -- NR4 congestion breakout: 4-bar narrow range then directional break.
trade_your_way_to_financial_freedom.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "narrow_range4_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, dc_lo, bb_width, atr, high, low",
    "long": "4-bar range is narrow (< 0.75 * ATR) AND current high breaks above 4-bar Donchian high",
    "short": "4-bar range is narrow AND current low breaks below 4-bar Donchian low",
    "desc": "NR4 congestion breakout: tight 4-bar range followed by directional break",
    "source": "book: trade_your_way_to_financial_freedom_mabroke_blogsp",
}

_NARROW_MULT = 0.75   # 4-bar range must be < 0.75 * ATR to qualify as narrow


def signal(ind, pos, htf=None):
    """Enter breakout only after a narrow 4-bar range (NR4 setup)."""
    if pos < 4:
        return None
    h = ind["high"][pos]
    lo = ind["low"][pos]
    atr = ind["atr"][pos]
    # 4-bar range = high of last 4 bars minus low of last 4 bars (bars pos-4..pos-1)
    highs = [ind["high"][pos - k] for k in range(1, 5)]
    lows = [ind["low"][pos - k] for k in range(1, 5)]
    if any(nan(x) for x in highs + lows) or nan(h, lo, atr):
        return None
    box_high = max(highs)
    box_low = min(lows)
    box_range = box_high - box_low
    if box_range > _NARROW_MULT * atr:
        return None   # range not narrow enough
    if h > box_high:
        return "long"
    if lo < box_low:
        return "short"
    return None
