#!/usr/bin/env python3
"""pullback_shifted_close_structure -- Pullback in long-term structure: close vs shifted close at 10/20/200 bars.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pullback_shifted_close_structure",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "close, open",
    "long": "bull candle AND close < close[-200] AND close > close[-20] AND close < close[-10]",
    "short": "bear candle AND close > close[-200] AND close < close[-20] AND close > close[-10]",
    "desc": "Pullback shifted close structure: short-term pullback within long-term structure using shifted close levels",
    "source": "github.com/zeta-zetra/code pullback_crude.py",
}


def signal(ind, pos, htf=None):
    """Pullback within long-term structure using shifted close levels."""
    if pos < 200:
        return None
    c0 = ind["close"][pos]
    op = ind["open"][pos]
    c10 = ind["close"][pos - 10]
    c20 = ind["close"][pos - 20]
    c200 = ind["close"][pos - 200]
    if nan(c0, op, c10, c20, c200):
        return None
    # long: bullish candle, oversold vs 200-bar, above 20-bar, mild pullback vs 10-bar
    if c0 > op and c0 < c200 and c0 > c20 and c0 < c10:
        return "long"
    # short: bearish candle, overbought vs 200-bar, below 20-bar, mild pullback vs 10-bar
    if c0 < op and c0 > c200 and c0 < c20 and c0 > c10:
        return "short"
    return None
