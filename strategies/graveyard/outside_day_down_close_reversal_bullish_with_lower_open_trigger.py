#!/usr/bin/env python3
"""outside_day_down_close_reversal_bullish_with_lower_open_trigger -- Outside day down-close + gap-down open bullish reversal. long_term_secrets_to_short_term_trading.

Setup: bar i-1 is an outside day with a down close (high[i-1]>high[i-2], low[i-1]<low[i-2],
close[i-1]<low[i-2]). Trigger: bar i opens LOWER than bar i-1's close -> buy on that open.
Signal emitted at bar i (we read bar i's open to confirm the trigger).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "outside_day_down_close_reversal_bullish_with_lower_open_trigger",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "Bar i-1: outside day AND down close (close<low[i-2]). Bar i: open<close[i-1] -> long trigger confirmed",
    "short": "none (spec defines bullish setup only)",
    "desc": "Outside day with down close followed by gap-down open triggers a bullish reversal buy",
    "source": "book:long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Outside down-close reversal: setup on i-1, trigger on gap-down open at i."""
    if pos < 2:
        return None
    o  = ind["open"]
    h  = ind["high"]
    lo = ind["low"]
    c  = ind["close"]
    if nan(o[pos], h[pos], lo[pos], c[pos],
           h[pos-1], lo[pos-1], c[pos-1],
           h[pos-2], lo[pos-2]):
        return None

    # Setup: bar i-1 is an outside day with down close
    outside_prev = h[pos-1] > h[pos-2] and lo[pos-1] < lo[pos-2]
    down_close   = c[pos-1] < lo[pos-2]         # closed below prior bar's low = strong down
    if not (outside_prev and down_close):
        return None

    # Trigger: current bar opens below prior bar's close
    if o[pos] < c[pos-1]:
        return "long"

    return None
