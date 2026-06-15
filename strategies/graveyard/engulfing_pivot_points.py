#!/usr/bin/env python3
"""engulfing_pivot_points -- Engulfing candle at pivot support/resistance. zeta-zetra.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "engulfing_pivot_points",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "piv_s1, piv_r1, open, close",
    "long": "bullish engulfing AND close > piv_s1",
    "short": "bearish engulfing AND close < piv_r1",
    "desc": "Bullish/bearish engulfing candle at pivot support or resistance level",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/candlestick/engulfing.html",
}


def signal(ind, pos, htf=None):
    """Engulfing candle at pivot point."""
    if pos < 1:
        return None
    o0 = ind["open"][pos]
    c0 = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    if nan(o0, c0, o1, c1, s1, r1):
        return None
    # bull engulf: prior candle bearish, current bullish, current body engulfs prior body
    bull_engulf = (c1 < o1) and (c0 > o0) and (o0 < c1) and (c0 > o1)
    # bear engulf: prior candle bullish, current bearish, current body engulfs prior body
    bear_engulf = (c1 > o1) and (c0 < o0) and (o0 > c1) and (c0 < o1)
    if bull_engulf and c0 > s1:
        return "long"
    if bear_engulf and c0 < r1:
        return "short"
    return None
