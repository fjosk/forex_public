#!/usr/bin/env python3
"""failed_round_number_breakout_reversal -- Fake-move stop-and-reverse at round-number level. reminiscences_of_a_stock_operator_edwin_lefevre.

Bar breaks above a round-number level (round_step) then the NEXT bar closes back below it -> failed
breakout -> short (stop-and-reverse). Mirror for down: break below a round level then close back above.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "failed_round_number_breakout_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "round_step,close,high,low",
    "long": "prior bar breaks below a round-number level AND current bar closes back above it (failed breakdown -> long)",
    "short": "prior bar breaks above a round-number level AND current bar closes back below it (failed breakout -> short)",
    "desc": "Failed round-number breakout reversal: break-then-retrace-back signals stop-and-reverse",
    "source": "reminiscences_of_a_stock_operator_edwin_lefevre, ch.IX",
}


def signal(ind, pos, htf=None):
    """Failed round-number breakout: prior bar pierces level, current bar returns inside."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    rs = ind["round_step"][pos]
    if nan(c, c1, h1, l1, rs) or rs <= 0:
        return None
    import math
    # Nearest round level to prior bar
    level = round(c1 / rs) * rs
    tol = rs * 0.1  # 10% of round step as tolerance
    # Prior bar broke ABOVE the round level (high > level) but current close is back below
    if h1 > level + tol and c < level:
        return "short"
    # Prior bar broke BELOW the round level (low < level) but current close is back above
    if l1 < level - tol and c > level:
        return "long"
    return None
