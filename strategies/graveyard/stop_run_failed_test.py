#!/usr/bin/env python3
"""stop_run_failed_test -- Failed test of a prior swing: a wick beyond the last confirmed fractal that closes back inside is a stop-run reversal.. tier2 (book-extracted from sister-lab catalog_books).

book:price-action. Ingested by strategies/_ingest_tier2.py (signal body verbatim). Price/OHLC only.
"""
from strategies._common import _nan, REVERT, ALL_CLASSES

META = {
    "id": "stop_run_failed_test",
    "cadences": ['day', 'swing'],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "price-action",
    "tf": "1h-4h",
    "indicators": "OHLC, Fractal swing prices",
    "long": "Bar pokes below the last confirmed down-fractal then closes back above it -- failed stop-run, go long",
    "short": "Bar pokes above the last confirmed up-fractal then closes back below it -- failed stop-run, go short",
    "desc": "Failed test of a prior swing: a wick beyond the last confirmed fractal that closes back inside is a stop-run reversal.",
    "source": "book:price-action",
}


def signal(I, i, htf=None):
    if i < 1:
        return None
    h0, l0, c0 = I["high"][i], I["low"][i], I["close"][i]
    fup, fdn = I["frac_up_px"][i-1], I["frac_dn_px"][i-1]
    if _nan(h0, l0, c0, fup, fdn):
        return None
    poke_up = h0 > fup and c0 < fup
    poke_down = l0 < fdn and c0 > fdn
    if poke_up:
        return "short"
    if poke_down:
        return "long"
    return None
