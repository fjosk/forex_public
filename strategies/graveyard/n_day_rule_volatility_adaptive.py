#!/usr/bin/env python3
"""n_day_rule_volatility_adaptive -- N-day Donchian breakout; volatility gate via ATR ratio.
trading_systems_and_methods_kaufman. When short-term ATR is high vs longer-term (ATR
compressed), breakout is wider and less frequent (adaptive-N spirit).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "n_day_rule_volatility_adaptive",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h-1d",
    "indicators": "dc_up, dc_lo, high, low, atr",
    "long": "high > Donchian upper AND ATR is compressed (vol low -> wider effective channel)",
    "short": "low < Donchian lower AND ATR is compressed",
    "desc": "N-day rule breakout with volatility-adaptive gate: only enter when ATR is below its 20-bar SMA proxy",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma",
}

# ATR compression threshold: only trade breakout when current ATR < atr_pct_threshold of price
# (i.e. low volatility => short-run vol < long-run vol => N_adaptive > N_base => harder to trigger,
# but here we gate: ONLY breakout when ATR is relatively calm)
_ATR_GATE = 0.015   # 1.5% of price; breakout only allowed in normal/low vol environments


def signal(ind, pos, htf=None):
    """Donchian breakout gated by ATR compression (proxy for adaptive N)."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    lo = ind["low"][pos]
    atr = ind["atr"][pos]
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos - 1]
    dc_lo = ind["dc_lo"][pos - 1]
    if nan(h, lo, atr, c, dc_up, dc_lo) or c <= 0:
        return None
    # Proxy adaptive N: skip if ATR/close is elevated (treat as N shrunk to zero -> no trade)
    if atr / c > _ATR_GATE:
        return None
    if h > dc_up:
        return "long"
    if lo < dc_lo:
        return "short"
    return None
