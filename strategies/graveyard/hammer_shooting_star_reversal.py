#!/usr/bin/env python3
"""hammer_shooting_star_reversal -- FX pin-bar reversal: hammer (long tail below) after a
decline; shooting star (long tail above) after an advance. ema20 trend filter.
Currency Trading for Dummies 2nd Ed., Ch.11 'Hammers and shooting stars'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hammer_shooting_star_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "open,high,low,close,ema20",
    "long": "hammer after decline (close < ema20): lower tail >= 2x body, small body near top",
    "short": "shooting star after advance (close > ema20): upper tail >= 2x body, small body near bottom",
    "desc": "Hammer/shooting star FX pin-bar reversal with ema20 trend direction filter",
    "source": "Currency Trading for Dummies 2nd Ed., Ch.11 'Hammers and shooting stars'",
}


def signal(ind, pos, htf=None):
    """Hammer (long) or shooting star (short) pin-bar reversal."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    ema = ind["ema20"][pos]
    if nan(o, h, l, c, ema):
        return None
    body = abs(c - o)
    if body <= 0:
        return None
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)
    # Hammer: long lower tail >= 2x body; after decline (below ema20)
    if lower_shadow >= 2.0 * body and c < ema:
        return "long"
    # Shooting star: long upper tail >= 2x body; after advance (above ema20)
    if upper_shadow >= 2.0 * body and c > ema:
        return "short"
    return None
