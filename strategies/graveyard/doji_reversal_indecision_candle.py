#!/usr/bin/env python3
"""doji_reversal_indecision_candle -- Doji at a top (after advance, above ema50) as a short
signal; at bottoms needs confirmation (only short bias is given a deterministic entry here).
J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'doji'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "doji_reversal_indecision_candle",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,ema50",
    "long": "none (book states bottom-doji is only a caution, not a buy signal)",
    "short": "doji (body <= 5% of range) at a top (close above ema50 after advance)",
    "desc": "Doji top reversal: sell signal at top after advance; ambiguous at bottoms",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'doji'; p.46-47",
}

_BODY_RATIO = 0.05   # strict doji: body <= 5% of range


def signal(ind, pos, htf=None):
    """Short-only doji reversal at tops (above ema50 after prior advance)."""
    if pos < 2:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    ema = ind["ema50"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    if nan(o, h, l, c, ema, c1, c2):
        return None
    rng = h - l
    if rng <= 0:
        return None
    # Must be a doji
    if abs(c - o) > _BODY_RATIO * rng:
        return None
    # At a top: close above ema50 and prior two closes were advancing
    if c > ema and c1 > c2:
        return "short"
    return None
