#!/usr/bin/env python3
"""trend_channel_trade_range_breakout -- Dual-mode Donchian strategy: range-fade mode (buy near
lower band, short near upper) when chop > 50; breakout mode (buy on close above dc_up, short on
close below dc_lo) when chop <= 50.

Source: j_person_a_complete_guide_to_technical_trading_tac, Ch.5 pp.79-80.
"""
from strategies._common import nan, BREAK, REVERT, ALL_CLASSES

META = {
    "id": "trend_channel_trade_range_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, dc_lo, dc_up, chop",
    "long": "Range (chop>50): close near dc_lo; Breakout (chop<=50): close > dc_up",
    "short": "Range (chop>50): close near dc_up; Breakout (chop<=50): close < dc_lo",
    "desc": "Trend channel dual-mode: range-fade at Donchian bands (chop>50) or breakout from channel (chop<=50)",
    "source": "j_person_a_complete_guide_to_technical_trading_tac Ch.5 pp.79-80",
}

_CHOP_THRESH = 50.0
_BAND_FRAC = 0.10


def signal(ind, pos, htf=None):
    """Donchian dual-mode: range-fade or breakout based on chop regime."""
    c = ind["close"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    ch = ind["chop"][pos]
    if nan(c, dlo, dup, ch) or dup <= dlo:
        return None
    bw = dup - dlo
    if ch > _CHOP_THRESH:
        # range-fade mode
        if c <= dlo + _BAND_FRAC * bw:
            return "long"
        if c >= dup - _BAND_FRAC * bw:
            return "short"
    else:
        # breakout mode
        if c > dup:
            return "long"
        if c < dlo:
            return "short"
    return None
