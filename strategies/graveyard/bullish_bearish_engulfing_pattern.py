#!/usr/bin/env python3
"""bullish_bearish_engulfing_pattern -- Two-candle body engulfment: second bar's body fully
contains the prior bar's body with opposite color. Reversal at extremes.
J. Person, A Complete Guide to Technical Trading Tactics, p.48-49."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bullish_bearish_engulfing_pattern",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,close,ema20",
    "long": "bullish engulfing at bottom: bar2 up body fully engulfs bar1 down body, below ema20",
    "short": "bearish engulfing at top: bar2 down body fully engulfs bar1 up body, above ema20",
    "desc": "Engulfing two-candle reversal: second body spans first body with opposite direction",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, p.48-49",
}


def signal(ind, pos, htf=None):
    """Bullish/bearish engulfing: body2 fully covers body1, opposite color, trend filter."""
    if pos < 1:
        return None
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    o2 = ind["open"][pos]
    c2 = ind["close"][pos]
    ema = ind["ema20"][pos]
    if nan(o1, c1, o2, c2, ema):
        return None
    body1_hi = max(o1, c1)
    body1_lo = min(o1, c1)
    body2_hi = max(o2, c2)
    body2_lo = min(o2, c2)
    # Bullish: prior bar down, current bar up, body2 fully engulfs body1
    if c1 < o1 and c2 > o2 and o2 <= body1_lo and c2 >= body1_hi and c2 < ema:
        return "long"
    # Bearish: prior bar up, current bar down, body2 fully engulfs body1
    if c1 > o1 and c2 < o2 and o2 >= body1_hi and c2 <= body1_lo and c2 > ema:
        return "short"
    return None
