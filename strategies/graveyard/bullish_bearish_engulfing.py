#!/usr/bin/env python3
"""bullish_bearish_engulfing -- Engulfing reversal: white candle fully covers prior black body
(bullish) or black candle fully covers prior white body (bearish); filtered by ema50 trend.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.48-54."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bullish_bearish_engulfing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,close,ema50",
    "long": "bullish engulfing in a downtrend (close below ema50): open2 < close1, close2 > open1",
    "short": "bearish engulfing in an uptrend (close above ema50): open2 > close1, close2 < open1",
    "desc": "Engulfing pillar-of-strength / tower-of-weakness: full body engulfment with trend context",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.48-56",
}


def signal(ind, pos, htf=None):
    """Engulfing reversal filtered by ema50 trend direction."""
    if pos < 1:
        return None
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    o2 = ind["open"][pos]
    c2 = ind["close"][pos]
    ema = ind["ema50"][pos]
    if nan(o1, c1, o2, c2, ema):
        return None
    # Bullish engulfing: prior bar down, current bar up, body2 covers body1
    # In a downtrend: c2 below ema50
    if c1 < o1 and c2 > o2 and o2 < min(o1, c1) and c2 > max(o1, c1) and c2 < ema:
        return "long"
    # Bearish engulfing: prior bar up, current bar down, body2 covers body1
    # In an uptrend: c2 above ema50
    if c1 > o1 and c2 < o2 and o2 > max(o1, c1) and c2 < min(o1, c1) and c2 > ema:
        return "short"
    return None
