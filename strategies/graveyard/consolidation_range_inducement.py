#!/usr/bin/env python3
"""consolidation_range_inducement -- Consolidation range sweep + FVG entry.

Detects a consolidation range (chop > 60 or rolling range < 1.5 * ATR over N bars),
then triggers on a sweep of the range edge with a body-return close back inside,
entering in the direction expected to target the opposite range boundary.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "consolidation_range_inducement",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h, 4h",
    "indicators": "close, high, low, atr, chop, bb_width",
    "long": "consolidation confirmed, sweep below range low, body closes back inside range",
    "short": "consolidation confirmed, sweep above range high, body closes back inside range",
    "desc": "Consolidation range inducement sweep: range sweep + return entry",
    "source": "web:https://acy.com/en/market-news/education/smc-playbook-series-part-2-spot-liquidity-pools-trading-j-o-103837/",
}

_RANGE_N = 20          # bars for rolling range detection
_CHOP_THRESHOLD = 60   # CHOP index above this = ranging
_RANGE_ATR_MULT = 1.5  # rolling range < mult * ATR = consolidating


def signal(ind, pos, htf=None):
    """Consolidation range sweep + return entry."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    atr = ind["atr"][pos]
    chop = ind["chop"][pos]
    if nan(c, h, l, atr, chop) or atr == 0:
        return None

    # Verify consolidation via chop index or rolling range
    in_chop = chop > _CHOP_THRESHOLD
    if not in_chop:
        start = max(0, pos - _RANGE_N)
        hi_vals = [ind["high"][i] for i in range(start, pos) if not nan(ind["high"][i])]
        lo_vals = [ind["low"][i] for i in range(start, pos) if not nan(ind["low"][i])]
        if len(hi_vals) < _RANGE_N // 2 or len(lo_vals) < _RANGE_N // 2:
            return None
        rolling_range = max(hi_vals) - min(lo_vals)
        in_chop = rolling_range < _RANGE_ATR_MULT * atr

    if not in_chop:
        return None

    # Compute range boundaries from lookback window
    start = max(0, pos - _RANGE_N)
    hi_vals = [ind["high"][i] for i in range(start, pos) if not nan(ind["high"][i])]
    lo_vals = [ind["low"][i] for i in range(start, pos) if not nan(ind["low"][i])]
    if not hi_vals or not lo_vals:
        return None
    range_hi = max(hi_vals)
    range_lo = min(lo_vals)

    # Sweep below range low, body closes back inside (long)
    if l < range_lo and c > range_lo:
        return "long"
    # Sweep above range high, body closes back inside (short)
    if h > range_hi and c < range_hi:
        return "short"
    return None
