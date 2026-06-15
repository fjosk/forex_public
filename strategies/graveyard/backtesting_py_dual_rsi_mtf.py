#!/usr/bin/env python3
"""backtesting_py_dual_rsi_mtf -- HTF bias + perfect MA stack entry. backtesting.py MTF example.

Higher-timeframe trend bias (EMA20>EMA50) combined with a perfect bullish MA stack on the
entry timeframe. HTF RSI > daily RSI > 70 from spec approximated by htf.bias > 0 + RSI > 60
(engine RSI is period=14; period=30 not available; threshold adjusted accordingly).
Long-only per original spec.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "backtesting_py_dual_rsi_mtf",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "rsi, sma10, sma20, sma50, sma100",
    "long": "HTF bias bullish AND RSI14 > 60 AND perfect MA stack close>SMA10>SMA20>SMA50>SMA100",
    "short": "Not implemented (long-only per original spec)",
    "desc": "HTF bias + RSI momentum + perfect MA stack entry (backtesting.py MTF example)",
    "source": "https://kernc.github.io/backtesting.py/doc/examples/Multiple%20Time%20Frames.html",
}


def signal(ind, pos, htf=None):
    """HTF bullish bias + RSI elevated + perfect MA stack."""
    c = ind["close"][pos]
    s10 = ind["sma10"][pos]
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    s100 = ind["sma100"][pos]
    r = ind["rsi"][pos]
    if nan(c, s10, s20, s50, s100, r):
        return None
    htf_bull = (htf is not None and htf["bias"][pos] > 0) if htf is not None else True
    stack_ok = c > s10 and s10 > s20 and s20 > s50 and s50 > s100
    if htf_bull and r > 60 and stack_ok:
        return "long"
    return None
