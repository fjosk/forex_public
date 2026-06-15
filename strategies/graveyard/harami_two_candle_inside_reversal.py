#!/usr/bin/env python3
"""harami_two_candle_inside_reversal -- Harami: candle2 body fully contained within candle1
body; top vs bottom context via ema20 trend filter.
J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'harami'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "harami_two_candle_inside_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,close,ema20",
    "long": "bullish harami at bottom: large down bar1, small inside bar2; close < ema20",
    "short": "bearish harami at top: large up bar1, small inside bar2; close > ema20",
    "desc": "Harami two-candle inside reversal: bar2 body contained within bar1 body, trend-filtered",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'harami'",
}

_INSIDE_RATIO = 0.50   # bar2 body <= 50% of bar1 body to be a valid inside candle


def signal(ind, pos, htf=None):
    """Harami reversal: bar2 body inside bar1 body with opposite trend context."""
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
    body1 = body1_hi - body1_lo
    body2 = body2_hi - body2_lo
    if body1 <= 0:
        return None
    # bar2 body must be inside bar1 body
    if not (body2_hi <= body1_hi and body2_lo >= body1_lo):
        return None
    # Prefer smaller bar2 (confirmation of momentum stall)
    if body2 > _INSIDE_RATIO * body1:
        return None
    # Bullish harami: bar1 down, at a bottom (below ema20)
    if c1 < o1 and c2 < ema:
        return "long"
    # Bearish harami: bar1 up, at a top (above ema20)
    if c1 > o1 and c2 > ema:
        return "short"
    return None
