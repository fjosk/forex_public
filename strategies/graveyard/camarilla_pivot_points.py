#!/usr/bin/env python3
"""camarilla_pivot_points -- Camarilla S3/R3 breakout computed from prev-day OHLC. hasnocool Pine script.

Camarilla levels computed inline from prev_dhh, prev_dll, prev_dhc (previous daily H/L/C).
Long when close > Camarilla R3 (breakout above third resistance).
Short when close < Camarilla S3 (breakout below third support).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "camarilla_pivot_points",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "break",
    "tf": "4h",
    "indicators": "prev_dhh, prev_dll, prev_dhc, close",
    "long": "close > Camarilla R3 (prev_close + range * 1.1/4)",
    "short": "close < Camarilla S3 (prev_close - range * 1.1/4)",
    "desc": "Camarilla pivot R3/S3 breakout computed from previous daily OHLC",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Camarilla%20Pivot%20Points%20Backtest.pine",
}


def signal(ind, pos, htf=None):
    """Camarilla R3/S3 breakout from previous daily OHLC."""
    ph = ind["prev_dhh"][pos]
    pl = ind["prev_dll"][pos]
    pc = ind["prev_dhc"][pos]
    c = ind["close"][pos]
    if nan(ph, pl, pc, c):
        return None
    rng = ph - pl
    r3 = pc + rng * (1.1 / 4.0)
    s3 = pc - rng * (1.1 / 4.0)
    if c > r3:
        return "long"
    if c < s3:
        return "short"
    return None
