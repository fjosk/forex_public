#!/usr/bin/env python3
"""heikin_ashi_supertrend_hybrid -- Supertrend direction on HA candles; execute at standard close.

Uses precomputed st_dir (standard Supertrend). The HA-specific Supertrend is approximated via
the standard st_dir filtered by HA candle direction (ha_close vs ha_open) for context alignment.
No volume -> FX-applicable.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "heikin_ashi_supertrend_hybrid",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "st_dir, ha_close, ha_open",
    "long": "st_dir flips to +1 (bullish) AND ha_close > ha_open (HA confirms bull)",
    "short": "st_dir flips to -1 (bearish) AND ha_close < ha_open (HA confirms bear)",
    "desc": "Supertrend flip gated by Heikin-Ashi candle direction agreement; execute at standard close",
    "source": "tradingview.com/script/9z16eauD-Heikin-Ashi-Supertrend/ jordanfray",
}


def signal(ind, pos, htf=None):
    """Supertrend flip confirmed by HA candle direction."""
    if pos < 1:
        return None
    st0 = ind["st_dir"][pos]
    st1 = ind["st_dir"][pos - 1]
    hao = ind["ha_open"][pos]
    hac = ind["ha_close"][pos]
    if nan(st0, st1, hao, hac):
        return None
    # st_dir: +1 = bullish, -1 = bearish (flip = direction change)
    if st0 > 0 and st1 <= 0 and hac > hao:
        return "long"
    if st0 < 0 and st1 >= 0 and hac < hao:
        return "short"
    return None
