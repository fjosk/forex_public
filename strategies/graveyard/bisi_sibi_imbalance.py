#!/usr/bin/env python3
"""bisi_sibi_imbalance -- ICT BISI/SIBI directional FVG retrace entry.

BISI (bullish FVG): gap_lo = high[pos-2], gap_hi = low[pos]; retrace detected when
current close is within the gap zone and price touched or went below CE midpoint.
SIBI (bearish FVG): gap_hi = low[pos-2], gap_lo = high[pos]; retrace detected when
current close is within the gap zone and price touched or went above CE.
Uses a 2-bar lookback to find the most recent valid gap, then checks if current
price is retracing into that zone.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bisi_sibi_imbalance",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m, 15m",
    "indicators": "high, low, close, atr",
    "long": "BISI: bullish FVG gap, price retraces into zone touching CE midpoint",
    "short": "SIBI: bearish FVG gap, price retraces into zone touching CE midpoint",
    "desc": "ICT BISI/SIBI directional FVG retrace entry (bullish/bearish imbalance)",
    "source": "web:https://innercircletrader.net/tutorials/sibi-and-bisi-the-ict-concepts/",
}

_LOOKBACK = 30   # bars to search for unmitigated FVG


def signal(ind, pos, htf=None):
    """BISI/SIBI FVG retrace entry."""
    c = ind["close"][pos]
    if nan(c):
        return None

    high = ind["high"]
    low = ind["low"]
    close = ind["close"]

    # Scan for the most recent valid bullish FVG (BISI) not yet mitigated
    for i in range(pos - 1, max(1, pos - _LOOKBACK), -1):
        g_lo = high[i - 1]   # high of candle before displacement
        g_hi = low[i + 1] if (i + 1) <= pos else low[pos]  # low of candle after
        if nan(g_lo, g_hi):
            continue
        if g_hi <= g_lo:     # no valid gap
            continue
        ce = (g_lo + g_hi) / 2.0
        # Check if a subsequent bar already closed below g_lo (mitigated)
        mitigated = False
        for j in range(i + 1, pos):
            if close[j] < g_lo:
                mitigated = True
                break
        if mitigated:
            continue
        # Entry: current bar retraces into the BISI zone (low touched CE or below)
        if low[pos] <= ce and c >= g_lo:
            return "long"
        break  # only consider the most recent qualifying gap

    # Scan for the most recent valid bearish FVG (SIBI)
    for i in range(pos - 1, max(1, pos - _LOOKBACK), -1):
        g_hi = low[i - 1]   # low of candle before displacement
        g_lo = high[i + 1] if (i + 1) <= pos else high[pos]  # high of candle after
        if nan(g_lo, g_hi):
            continue
        if g_hi <= g_lo:     # no valid gap (lo must be above lo of next candle)
            continue
        ce = (g_lo + g_hi) / 2.0
        # Check if mitigated (subsequent bar closed above g_hi)
        mitigated = False
        for j in range(i + 1, pos):
            if close[j] > g_hi:
                mitigated = True
                break
        if mitigated:
            continue
        # Entry: current bar retraces up into SIBI zone (high touched CE or above)
        if high[pos] >= ce and c <= g_hi:
            return "short"
        break

    return None
