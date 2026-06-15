#!/usr/bin/env python3
"""nested_swing_structure -- Nested multi-timeframe swing structure: higher-low/lower-high continuation gated by EMA50 trend, using forward-filled confirmed-fractal prices as the 2-deep swing history.. tier2 (book-extracted from sister-lab catalog_books).

book:multi-timeframe. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "nested_swing_structure",
    "cadences": ['day', 'swing'],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "Bill Williams fractals (frac_up/dn + px), EMA(50)",
    "long": "New higher-low fractal above prior swing low with close>EMA50",
    "short": "New lower-high fractal below prior swing high with close<EMA50",
    "desc": "Nested multi-timeframe swing structure: higher-low/lower-high continuation gated by EMA50 trend, using forward-filled confirmed-fractal prices as the 2-deep swing history.",
    "source": "book:multi-timeframe",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    fd, fu = I["frac_dn"][i], I["frac_up"][i]
    fd_px, fu_px = I["frac_dn_px"][i], I["frac_up_px"][i]
    c, e50 = I["close"][i], I["ema50"][i]
    if _nan(c, e50):
        return None
    # frac_*_px is forward-filled, so the value at i-1 is the PRIOR confirmed
    # swing price (the one in effect right before a new fractal confirms at i).
    prev_swing_low = I["frac_dn_px"][i-1]
    prev_swing_high = I["frac_up_px"][i-1]
    if fd and not _nan(fd_px, prev_swing_low) and fd_px > prev_swing_low and c > e50:
        return "long"   # higher-low above prior swing low, price above EMA50
    if fu and not _nan(fu_px, prev_swing_high) and fu_px < prev_swing_high and c < e50:
        return "short"  # lower-high below prior swing high, price below EMA50
    return None
