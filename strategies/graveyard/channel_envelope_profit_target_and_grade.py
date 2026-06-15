#!/usr/bin/env python3
"""channel_envelope_profit_target_and_grade -- Bollinger-band extremes as entry, EMA/opposite-band as target. come_into_my_trading_room_alexander_elder.

Elder: buy near lower Bollinger band (oversold), target upper band or EMA; short near upper band,
target lower band or EMA. The channel contains ~95% of price (= ~2 std dev). Uses bb_lo/bb_up/bb_mid.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "channel_envelope_profit_target_and_grade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "close,bb_lo,bb_up,bb_mid,bb_pctb",
    "long": "Close at or below lower Bollinger band (bb_pctb<=0) -> long; target bb_mid or bb_up",
    "short": "Close at or above upper Bollinger band (bb_pctb>=1) -> short; target bb_mid or bb_lo",
    "desc": "Channel/envelope profit target: buy at lower band, short at upper band; mean-reversion to EMA or opposite band",
    "source": "book:come_into_my_trading_room_alexander_elder",
}


def signal(ind, pos, htf=None):
    """Bollinger-band extremes: trade from outer bands back toward center."""
    if pos < 1:
        return None
    c      = ind["close"][pos]
    bb_lo  = ind["bb_lo"][pos]
    bb_up  = ind["bb_up"][pos]
    pctb   = ind["bb_pctb"][pos]
    if nan(c, bb_lo, bb_up, pctb):
        return None

    if c <= bb_lo or pctb <= 0.0:
        return "long"

    if c >= bb_up or pctb >= 1.0:
        return "short"

    return None
