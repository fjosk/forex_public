#!/usr/bin/env python3
"""nofri_congestion_phase_system_3rd_day_reversal -- In a congestion/range environment (high CHOP
index), fade 2 consecutive same-direction closes by trading the expected 3rd-day reversal.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.12 p.292-293.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "nofri_congestion_phase_system_3rd_day_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, chop",
    "long": "CHOP > 50 (range-bound) AND close[1] < close[2] AND close[0] < close[1] (2 consecutive down-closes) -> fade up",
    "short": "CHOP > 50 (range-bound) AND close[1] > close[2] AND close[0] > close[1] (2 consecutive up-closes) -> fade down",
    "desc": "Nofri congestion-phase 3rd-day reversal: fade 2-bar same-direction run inside a confirmed range",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.12 pp.292-293",
}

_CHOP_RANGE = 50.0  # above this = range-bound market


def signal(ind, pos, htf=None):
    """Range-bound 2-bar run fade (Nofri system)."""
    if pos < 2:
        return None
    ch = ind["chop"][pos]
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    if nan(ch, c0, c1, c2):
        return None
    if ch <= _CHOP_RANGE:
        return None  # not in a congestion/range regime
    # 2 consecutive down closes -> expect reversal up
    if c1 < c2 and c0 < c1:
        return "long"
    # 2 consecutive up closes -> expect reversal down
    if c1 > c2 and c0 > c1:
        return "short"
    return None
