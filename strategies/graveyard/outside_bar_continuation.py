#!/usr/bin/env python3
"""outside_bar_continuation -- Outside bar in trend direction signals continuation. j_person_a_complete_guide_to_technical_trading_tac.

Outside bar: today's range engulfs prior bar (high[i]>high[i-1] AND low[i]<low[i-1]).
Continuation: if close is in the upper portion of the bar and trend is up -> long;
if close is in the lower portion and trend is down -> short. Trend filter via EMA50.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "outside_bar_continuation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "continuation",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "Outside bar (engulfs prior range) AND close in upper 50% of bar range AND close>ema50",
    "short": "Outside bar AND close in lower 50% of bar range AND close<ema50",
    "desc": "Outside bar with trend-direction close signals continuation in the trend direction",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Outside bar continuation: range engulfs prior bar; close in trend direction."""
    if pos < 1:
        return None
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    ema = ind["ema50"][pos]
    if nan(h[pos], lo[pos], c[pos], h[pos-1], lo[pos-1], ema):
        return None

    # Outside bar condition
    is_outside = h[pos] > h[pos-1] and lo[pos] < lo[pos-1]
    if not is_outside:
        return None

    bar_range = h[pos] - lo[pos]
    if bar_range == 0:
        return None

    bar_mid = lo[pos] + 0.5 * bar_range

    # Continuation long: close in upper half + uptrend
    if c[pos] > bar_mid and c[pos] > ema:
        return "long"

    # Continuation short: close in lower half + downtrend
    if c[pos] < bar_mid and c[pos] < ema:
        return "short"

    return None
