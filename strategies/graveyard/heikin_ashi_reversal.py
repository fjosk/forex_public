#!/usr/bin/env python3
"""heikin_ashi_reversal -- Contrarian HA body expansion at extreme: bearish expansion -> long. je-suis-tm."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "heikin_ashi_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "ha_close, ha_open, high, low",
    "long": "bearish HA (open==high, no upper wick) with expanding body AND prev bearish -> contrarian long",
    "short": "bullish HA (open==low, no lower wick) with expanding body AND prev bullish -> contrarian short",
    "desc": "Heikin-Ashi momentum reversal: expanding extreme bar triggers contrarian entry",
    "source": "https://github.com/je-suis-tm/quant-trading",
}

_TOL = 1e-8  # floating-point equality tolerance for ha_open == ha_high / ha_low


def signal(ind, pos, htf=None):
    """HA body expansion contrarian reversal."""
    hc = ind["ha_close"][pos]
    ho = ind["ha_open"][pos]
    hc1 = ind["ha_close"][pos - 1]
    ho1 = ind["ha_open"][pos - 1]
    # ha_high and ha_low are not separate keys; approximate from ha_open/ha_close direction
    # No-upper-wick on bearish HA bar means ha_open == ha_high (open is the top)
    # We use the high/low arrays as the HA high/low approximation
    h = ind["high"][pos]
    l = ind["low"][pos]
    if nan(hc, ho, hc1, ho1, h, l):
        return None
    body = abs(hc - ho)
    body1 = abs(hc1 - ho1)
    bear_bar = ho > hc
    bull_bar = hc > ho
    no_upper_wick = abs(ho - h) < _TOL  # ha_open at top of candle range
    no_lower_wick = abs(ho - l) < _TOL  # ha_open at bottom (bullish ha open==low)
    prev_bear = ho1 > hc1
    prev_bull = hc1 > ho1
    # Contrarian long: bearish extreme bar (no upper wick, expanding body) after bearish bar
    if bear_bar and no_upper_wick and body > body1 and prev_bear:
        return "long"
    # Contrarian short: bullish extreme bar (no lower wick, expanding body) after bullish bar
    if bull_bar and no_lower_wick and body > body1 and prev_bull:
        return "short"
    return None
