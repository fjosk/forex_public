#!/usr/bin/env python3
"""vwap_pullback_scalp -- VWAP pullback reversal scalp. ICFM India trading guide.

Long: price above VWAP, retraces to near VWAP, bullish reversal candle at the touch.
Short: price below VWAP, rallies to near VWAP, bearish reversal candle at the touch.
Near-VWAP threshold: 0.1% of price (ATR-neutral proxy for ~5 pips on EURUSD).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "vwap_pullback_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m-15m",
    "indicators": "vwap, open, high, low, close",
    "long": "close > vwap, price near vwap (within 0.1%), bullish reversal candle (body > 50% range, close > open)",
    "short": "close < vwap, price near vwap, bearish reversal candle",
    "desc": "VWAP pullback reversal scalp: near-VWAP touch with confirming candle",
    "source": "web:https://www.icfmindia.com/blog/scalping-strategy-with-vwap-and-supportresistance-a-traders-quick-guide",
}

_VWAP_PROXIMITY = 0.001  # 0.1% price proximity threshold


def signal(ind, pos, htf=None):
    """VWAP pullback reversal scalp."""
    vwap = ind["vwap"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    if nan(vwap, o, h, l, c) or vwap == 0:
        return None

    rng = h - l
    if rng == 0:
        return None

    near_vwap = abs(c - vwap) / vwap < _VWAP_PROXIMITY
    bull_reversal = (c - o) > 0.5 * rng and c > o
    bear_reversal = (o - c) > 0.5 * rng and c < o

    if c > vwap and near_vwap and bull_reversal:
        return "long"
    if c < vwap and near_vwap and bear_reversal:
        return "short"
    return None
