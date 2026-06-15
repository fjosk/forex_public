#!/usr/bin/env python3
"""person_pivot_point_levels_floor_trader_pivot -- Person floor-trader pivot: first test of S1 or R1 triggers entry in bias direction. j_person_a_complete_guide_to_technical_trading_tac Ch6-7."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "person_pivot_point_levels_floor_trader_pivot",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "piv_p,piv_r1,piv_s1,close,low,high",
    "long": "Price touches S1 support and reverses up (long bias: open or close above PP)",
    "short": "Price touches R1 resistance and reverses down (short bias: open or close below PP)",
    "desc": "Person floor-trader pivot: buy S1 bounce in bullish bias (above PP); sell R1 rejection in bearish bias (below PP)",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac, Ch6-7",
}


def signal(ind, pos, htf=None):
    """S1/R1 reaction entry gated by PP bias."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    pp = ind["piv_p"][pos]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    if nan(c, lo, hi, pp, r1, s1):
        return None
    # Long bias: price above PP; buy on S1 test that recovers
    if c > pp and lo <= s1 and c > s1:
        return "long"
    # Short bias: price below PP; sell on R1 test that retreats
    if c < pp and hi >= r1 and c < r1:
        return "short"
    return None
