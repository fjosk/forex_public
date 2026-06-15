#!/usr/bin/env python3
"""consequent_encroachment_ce -- ICT CE precision entry at FVG 50% midpoint.

Detects the most recent valid bullish or bearish FVG within the lookback window.
Entry fires when current price touches the CE (50% midpoint of the gap) and
the close remains inside the zone on the touch bar.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "consequent_encroachment_ce",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m, 15m",
    "indicators": "high, low, close, atr",
    "long": "bullish FVG detected; price retraces to CE (50% of gap); close >= gap_lo",
    "short": "bearish FVG detected; price retraces to CE (50% of gap); close <= gap_hi",
    "desc": "ICT Consequent Encroachment: FVG midpoint precision entry",
    "source": "web:https://innercircletrader.net/tutorials/ict-consequent-encroachment/",
}

_LOOKBACK = 30


def signal(ind, pos, htf=None):
    """CE precision FVG midpoint entry."""
    c = ind["close"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(c, hi, lo):
        return None

    high = ind["high"]
    low = ind["low"]
    close = ind["close"]

    # Find most recent unmitigated bullish FVG
    for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
        if i + 1 >= pos:
            continue
        g_lo = high[i - 1]
        g_hi = low[i + 1]
        if nan(g_lo, g_hi) or g_hi <= g_lo:
            continue
        ce = (g_lo + g_hi) / 2.0
        # Check mitigation: any bar between gap and now closed below g_lo
        mitigated = any(close[j] < g_lo for j in range(i + 1, pos) if not nan(close[j]))
        if mitigated:
            continue
        # CE touch: bar's low reached CE level and close held above gap_lo
        if lo <= ce and c >= g_lo:
            return "long"
        break

    # Find most recent unmitigated bearish FVG
    for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
        if i + 1 >= pos:
            continue
        g_hi = low[i - 1]
        g_lo = high[i + 1]
        if nan(g_lo, g_hi) or g_hi <= g_lo:
            continue
        ce = (g_lo + g_hi) / 2.0
        # Check mitigation
        mitigated = any(close[j] > g_hi for j in range(i + 1, pos) if not nan(close[j]))
        if mitigated:
            continue
        # CE touch: bar's high reached CE and close held below gap_hi
        if hi >= ce and c <= g_hi:
            return "short"
        break

    return None
