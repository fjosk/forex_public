#!/usr/bin/env python3
"""daily_pivot_point_support_resistance_entry_stop_framework -- Daily pivot-point bias entry: long above PP, short below PP; target S1/R1. thirty_days_of_forex_trading_trades_tactics_and_te Day27."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "daily_pivot_point_support_resistance_entry_stop_framework",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "piv_p,piv_r1,piv_s1,close",
    "long": "Price above PP (bullish bias), pull back to or below S1 then close back above S1",
    "short": "Price below PP (bearish bias), bounce to or above R1 then close back below R1",
    "desc": "Daily pivot PP/S1/R1 bias entry: long on S1 support with PP as bias line; short on R1 resistance",
    "source": "book: thirty_days_of_forex_trading_trades_tactics_and_te, Day27",
}


def signal(ind, pos, htf=None):
    """Long on pullback to S1 while price is above PP; short on rally to R1 while below PP."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    pp = ind["piv_p"][pos]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    if nan(c, c1, pp, r1, s1):
        return None
    # Long: price is above PP (bullish bias) and touched S1 last bar but recovered above it
    if c > pp and c1 <= s1 and c > s1:
        return "long"
    # Short: price is below PP (bearish bias) and touched R1 last bar but fell back below it
    if c < pp and c1 >= r1 and c < r1:
        return "short"
    return None
