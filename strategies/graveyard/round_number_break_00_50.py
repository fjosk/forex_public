#!/usr/bin/env python3
"""round_number_break_00_50 -- Psychological round-number (00/50) breakout.
thirty_days_of_forex_trading.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "round_number_break_00_50",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "round_step, close",
    "long": "close crosses above the nearest round-number grid level (00/50)",
    "short": "close crosses below the nearest round-number grid level",
    "desc": "Psychological round-number break: close crosses 00/50 pip level with directional follow-through",
    "source": "book: thirty_days_of_forex_trading_trades_tactics_and_te",
}


def signal(ind, pos, htf=None):
    """Close crosses a round-step grid boundary (precomputed round_step)."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    rs = ind["round_step"][pos]
    if nan(c, c1, rs) or rs <= 0:
        return None
    import math
    # level below current close
    level_c = math.floor(c / rs) * rs
    level_c1 = math.floor(c1 / rs) * rs
    if level_c > level_c1:
        return "long"
    if level_c < level_c1:
        return "short"
    return None
