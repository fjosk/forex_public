#!/usr/bin/env python3
"""range_bound_channel_mean_reversion_trade -- Classic Donchian channel range trade: buy near
lower band, sell near upper band, abort on channel breakout.

Source: the_naked_trader_how_anyone_can_still_make_money_t, Ch.4 Strategy 5.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "range_bound_channel_mean_reversion_trade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, dc_lo, dc_up, chop",
    "long": "Range confirmed (chop > 50); close <= dc_lo + 0.1*(dc_up-dc_lo): buy near lower Donchian band",
    "short": "Range confirmed (chop > 50); close >= dc_up - 0.1*(dc_up-dc_lo): short near upper Donchian band",
    "desc": "Range-bound Donchian channel mean reversion: buy lower band, short upper band in a confirmed range",
    "source": "the_naked_trader_how_anyone_can_still_make_money_t Ch.4",
}

_CHOP_THRESH = 50.0
_BAND_FRAC = 0.10  # within 10% of band edge


def signal(ind, pos, htf=None):
    """Buy near dc_lo, short near dc_up, only in a range (chop > threshold)."""
    c = ind["close"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    ch = ind["chop"][pos]
    if nan(c, dlo, dup, ch) or dup <= dlo:
        return None
    if ch <= _CHOP_THRESH:
        return None  # not range-bound
    band_width = dup - dlo
    if c <= dlo + _BAND_FRAC * band_width:
        return "long"
    if c >= dup - _BAND_FRAC * band_width:
        return "short"
    return None
