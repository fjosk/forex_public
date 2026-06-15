#!/usr/bin/env python3
"""trend_day_reversal_day_extreme_outside_reversal_day_patterns -- Kaufman's trend/reversal/extreme outside day patterns. trading_systems_and_methods_kaufman_perry_j_kaufma.

Three patterns based on yesterday's high/close vs prior close:
- Trend up: H[1]>H[2] AND C[1]>C[2] -> expect continuation (long).
- Reversal: H[1]>H[2] AND C[1]<C[2] -> expect reversal (short).
- Extreme (outside) reversal: H[1]>H[2] AND C[1]<L[2] -> stronger reversal (short).
Signal fires at current bar i (pos) based on prior two bars.
"""
from strategies._common import nan, TREND, REVERT, ALL_CLASSES

# NOTE: uses TREND exit for continuation, REVERT for reversal
_EXIT = REVERT   # reversal patterns; the trend-day long also uses REVERT (short-term continuation)

META = {
    "id": "trend_day_reversal_day_extreme_outside_reversal_day_patterns",
    "cadences": ["day", "swing"],
    "exit": _EXIT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,low,close",
    "long": "Trend day: H[i-1]>H[i-2] AND C[i-1]>C[i-2] -> expect continuation up; buy",
    "short": "Reversal day: H[i-1]>H[i-2] AND C[i-1]<C[i-2]; or Extreme: C[i-1]<L[i-2] -> short",
    "desc": "Kaufman trend/reversal/extreme outside reversal day patterns based on prior two bars HLC",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Trend/reversal/extreme day patterns from prior two bars."""
    if pos < 2:
        return None
    h  = ind["high"]
    lo = ind["low"]
    c  = ind["close"]
    if nan(h[pos-1], lo[pos-1], c[pos-1], h[pos-2], lo[pos-2], c[pos-2]):
        return None

    prev_h_new_high = h[pos-1] > h[pos-2]

    # Extreme outside reversal: yesterday high > prior high BUT close < prior LOW
    if prev_h_new_high and c[pos-1] < lo[pos-2]:
        return "short"

    # Standard reversal day: yesterday high > prior high BUT close < prior close
    if prev_h_new_high and c[pos-1] < c[pos-2]:
        return "short"

    # Trend day (continuation): yesterday high > prior high AND close > prior close
    if prev_h_new_high and c[pos-1] > c[pos-2]:
        return "long"

    return None
