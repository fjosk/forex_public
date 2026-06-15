#!/usr/bin/env python3
"""first_crossing_round_number_breakout -- First-time close above a major round price level (round_step). reminiscences_of_a_stock_operator."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "first_crossing_round_number_breakout_100_200_300_level",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "round_step, close",
    "long": "close crosses above a round-number level (round_step) for the first time in lookback",
    "short": "close crosses below a round-number level for the first time in lookback",
    "desc": "First-crossing round-number breakout: century/key level first-time cross per Livermore",
    "source": "reminiscences_of_a_stock_operator_edwin_lefevre",
}


def signal(ind, pos, htf=None):
    """Detect first-time cross of the nearest round number level."""
    if pos < 10:
        return None
    c = ind["close"]
    rs = ind["round_step"][pos]
    cv = c[pos]
    cv1 = c[pos - 1]
    if nan(cv, cv1, rs) or rs <= 0:
        return None

    # Nearest round level above and below
    import math
    level_up = math.ceil(cv / rs) * rs
    level_dn = math.floor(cv / rs) * rs

    # Long: close just crossed above level_dn (i.e. prior close was below level_dn, now above)
    # Use the level that was just crossed
    # Determine which round level was just crossed
    crossed_up = None
    crossed_dn = None
    for k in range(1, 2):
        prev_c = c[pos - k]
        if nan(prev_c):
            continue
        # Find if we crossed a round level between prev_c and cv
        if cv > prev_c:
            lvl = math.ceil(prev_c / rs) * rs
            if prev_c < lvl <= cv:
                crossed_up = lvl
        elif cv < prev_c:
            lvl = math.floor(prev_c / rs) * rs
            if cv <= lvl < prev_c:
                crossed_dn = lvl

    if crossed_up is None and crossed_dn is None:
        return None

    # Check "first time" in lookback (last 50 bars none were above/below the level)
    lookback = min(50, pos)
    if crossed_up is not None:
        for k in range(2, lookback + 1):
            if pos - k < 0:
                break
            prev = c[pos - k]
            if nan(prev):
                continue
            if prev >= crossed_up:
                return None  # level was crossed before; not first time
        return "long"

    if crossed_dn is not None:
        for k in range(2, lookback + 1):
            if pos - k < 0:
                break
            prev = c[pos - k]
            if nan(prev):
                continue
            if prev <= crossed_dn:
                return None
        return "short"

    return None
