#!/usr/bin/env python3
"""rsi_shooting_star_wick -- Wick-to-body ratio hammer/shooting-star with RSI zone filter. zeta-zetra."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_shooting_star_wick",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "rsi, open, high, low, close",
    "long": "hammer: lower wick / body > 1.5 AND upper wick small AND RSI 30-55",
    "short": "shooting star: upper wick / body > 1.5 AND lower wick small AND RSI 50-70",
    "desc": "RSI-filtered shooting star / hammer via wick-body ratio; zeta-zetra Python backtest",
    "source": "web:https://github.com/zeta-zetra/code",
}

_RATIO_MIN = 1.5
_SMALL_FRAC = 0.30
_BODY_MIN = 0.0001   # minimum body in price units (avoids doji)


def signal(ind, pos, htf=None):
    """Hammer / shooting star via wick ratios with RSI zone confirmation."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    rsi = ind["rsi"][pos]
    if nan(c, o, h, l, rsi):
        return None
    body = abs(c - o)
    if body < _BODY_MIN:
        return None
    upper_wick = h - max(c, o)
    lower_wick = min(c, o) - l
    if upper_wick < 0:
        upper_wick = 0.0
    if lower_wick < 0:
        lower_wick = 0.0
    # Hammer: long lower wick, small upper wick, RSI oversold zone
    if (lower_wick / body > _RATIO_MIN
            and upper_wick < _SMALL_FRAC * lower_wick
            and 30 < rsi < 55):
        return "long"
    # Shooting star: long upper wick, small lower wick, RSI overbought zone
    if (upper_wick / body > _RATIO_MIN
            and lower_wick < _SMALL_FRAC * upper_wick
            and 50 < rsi < 70):
        return "short"
    return None
