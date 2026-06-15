#!/usr/bin/env python3
"""ichimoku_kumo_breakout_ao -- Ichimoku cloud breakout confirmed by Awesome Oscillator flip. web:forextester."""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "ichimoku_kumo_breakout_ao",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1h",
    "indicators": "ich_a, ich_b, ao",
    "long": "close above kumo top (max of ich_a/b) and AO flips from negative to positive",
    "short": "close below kumo bottom (min of ich_a/b) and AO flips from positive to negative",
    "desc": "Ichimoku cloud breakout with Awesome Oscillator histogram direction confirmation",
    "source": "web:https://forextester.com/blog/kumo-strategy/",
}


def signal(ind, pos, htf=None):
    """Ichimoku kumo breakout confirmed by AO flip."""
    c = ind["close"][pos]
    a = ind["ich_a"][pos]
    b = ind["ich_b"][pos]
    ao = ind["ao"][pos]
    ao1 = ind["ao"][pos - 1]
    if nan(c, a, b, ao, ao1):
        return None
    kumo_top = max(a, b)
    kumo_bot = min(a, b)
    ao_flip_up = _xup(ao, ao1, 0.0, 0.0)
    ao_flip_dn = _xdn(ao, ao1, 0.0, 0.0)
    if c > kumo_top and ao_flip_up:
        return "long"
    if c < kumo_bot and ao_flip_dn:
        return "short"
    return None
