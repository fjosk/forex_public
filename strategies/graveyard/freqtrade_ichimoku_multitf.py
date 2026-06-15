#!/usr/bin/env python3
"""freqtrade_ichimoku_multitf -- ichiV1: price above Ichimoku cloud with bullish candle + HTF bias. ynstf.

Price above both Ichimoku Span A and Span B, combined with a bullish entry candle and
HTF bullish bias. Multi-timeframe fan-magnitude check from spec omitted (custom ratio not
in indicator set); cloud filter + entry candle + HTF bias are the codeable subset.
Long-only per spec.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "freqtrade_ichimoku_multitf",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ich_a, ich_b, open, close",
    "long": "close > ich_a AND close > ich_b (above cloud) AND bullish entry candle AND HTF bias bullish",
    "short": "Not implemented (long-only per spec)",
    "desc": "Ichimoku cloud filter + bullish candle + HTF trend bias (ichiV1 multi-TF core)",
    "source": "https://github.com/ynstf/Good-Freqtrade-Strategies/blob/main/ichiV1.py",
}


def signal(ind, pos, htf=None):
    """Above Ichimoku cloud with bullish candle and HTF bias."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    if nan(c, o, ia, ib):
        return None
    above_cloud = c > ia and c > ib
    bullish_candle = c > o
    htf_bull = (htf["bias"][pos] > 0) if (htf is not None) else True
    if above_cloud and bullish_candle and htf_bull:
        return "long"
    return None
