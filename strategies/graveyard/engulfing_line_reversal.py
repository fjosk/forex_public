#!/usr/bin/env python3
"""engulfing_line_reversal -- FX engulfing reversal: second candle body fully engulfs first;
prior move filter via ema20; smaller first body = stronger signal.
Currency Trading for Dummies 2nd Ed., Ch.11 'Engulfing lines'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_line_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "open,close,ema20",
    "long": "bullish engulfing after downmove (close < ema20): dark bar1, white bar2 engulfs bar1 body",
    "short": "bearish engulfing after upmove (close > ema20): white bar1, dark bar2 engulfs bar1 body",
    "desc": "FX engulfing line reversal with ema20 trend direction gate",
    "source": "Currency Trading for Dummies 2nd Ed., Ch.11 'Engulfing lines'",
}


def signal(ind, pos, htf=None):
    """Engulfing reversal: bar2 body fully spans bar1 body, opposite color, trend filter."""
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
    # Bullish: bar1 dark (close < open), bar2 white (close > open), bar2 body engulfs bar1
    if c1 < o1 and c2 > o2 and o2 <= body1_lo and c2 >= body1_hi and c2 < ema:
        return "long"
    # Bearish: bar1 white (close > open), bar2 dark (close < open), bar2 body engulfs bar1
    if c1 > o1 and c2 < o2 and o2 >= body1_hi and c2 <= body1_lo and c2 > ema:
        return "short"
    return None
