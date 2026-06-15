#!/usr/bin/env python3
"""rectangle_range_trade_buy_support_short_resistance -- Buy at Donchian lower boundary when
Stochastic turns up from oversold; short at upper boundary when Stochastic turns down from
overbought.

Source: elder_alexander_trading_for_a_living, Sec.23 p.109.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rectangle_range_trade_buy_support_short_resistance",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "dc_lo, dc_up, stoch_k, stoch_d, close",
    "long": "Close near dc_lo (lower band) AND stoch_k < 25 turning up (stoch_k > stoch_k[1])",
    "short": "Close near dc_up (upper band) AND stoch_k > 75 turning down (stoch_k < stoch_k[1])",
    "desc": "Rectangle range trade: buy Donchian lower band with stochastic turning up from oversold; mirror short",
    "source": "elder_alexander_trading_for_a_living Sec.23 p.109",
}

_BAND_FRAC = 0.15
_OS = 25.0
_OB = 75.0


def signal(ind, pos, htf=None):
    """Rectangle range: Donchian band touch + stochastic reversal confirmation."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    dlo = ind["dc_lo"][pos]
    dup = ind["dc_up"][pos]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(c, dlo, dup, sk, sk1) or dup <= dlo:
        return None
    band_width = dup - dlo
    near_lo = c <= dlo + _BAND_FRAC * band_width
    near_hi = c >= dup - _BAND_FRAC * band_width
    if near_lo and sk < _OS and sk > sk1:
        return "long"
    if near_hi and sk > _OB and sk < sk1:
        return "short"
    return None
