#!/usr/bin/env python3
"""fib_retrace_rebound -- Fibonacci retracement rebound: enter at the 38.2/50/61.8% pullback of the most recent fractal swing, in the EMA50 trend direction.. tier2 (book-extracted from sister-lab catalog_books).

book:pivot-sr. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "fib_retrace_rebound",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h-4h",
    "indicators": "Fractal swing high/low (frac_up_px/frac_dn_px), EMA(50), high/low",
    "long": "Close above EMA50 near a 38/50/62% fib retracement of the last fractal swing, swing low intact",
    "short": "Close below EMA50 near a 38/50/62% fib retracement of the last fractal swing, swing high intact",
    "desc": "Fibonacci retracement rebound: enter at the 38.2/50/61.8% pullback of the most recent fractal swing, in the EMA50 trend direction.",
    "source": "book:pivot-sr",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    H, L = I["frac_up_px"][i], I["frac_dn_px"][i]
    c, e50 = I["close"][i], I["ema50"][i]
    lo, hi = I["low"][i], I["high"][i]
    if _nan(H, L, c, e50, lo, hi) or H <= L:
        return None
    rng = H - L
    tol = 0.0025 * c

    def near(lvl):
        return abs(c - lvl) <= tol

    if c > e50 and (near(H - 0.382 * rng) or near(H - 0.5 * rng) or near(H - 0.618 * rng)) and lo >= L:
        return "long"     # uptrend pullback into a fib retracement, swing low held
    if c < e50 and (near(L + 0.382 * rng) or near(L + 0.5 * rng) or near(L + 0.618 * rng)) and hi <= H:
        return "short"    # downtrend rally into a fib retracement, swing high held
    return None
