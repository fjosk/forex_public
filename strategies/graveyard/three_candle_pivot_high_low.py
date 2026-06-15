#!/usr/bin/env python3
"""three_candle_pivot_high_low -- 3-bar pivot high/low structure: higher pivot lows = bullish, lower pivot highs = bearish. binary_options_unmasked_pdfdrive.

Successive higher pivot lows (two recent frac_dn at ascending price levels) -> long.
Successive lower pivot highs (two recent frac_up at descending price levels) -> short.
Uses the precomputed frac_up/frac_dn flags and their price levels.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "three_candle_pivot_high_low",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "frac_dn,frac_dn_px,frac_up,frac_up_px,close",
    "long": "two recent fractal lows where second frac_dn_px > first frac_dn_px (higher pivot low structure)",
    "short": "two recent fractal highs where second frac_up_px < first frac_up_px (lower pivot high structure)",
    "desc": "3-bar pivot structure: higher pivot lows = bullish trend; lower pivot highs = bearish trend",
    "source": "binary_options_unmasked_pdfdrive, Ch10 Fig10.17-10.18",
}


def signal(ind, pos, htf=None):
    """Successive fractal pivots in same direction confirm structural trend."""
    if pos < 10:
        return None
    # Scan back for the last two fractal lows (frac_dn == 1) within last 10 bars
    frac_dn_prices = []
    frac_up_prices = []
    for k in range(1, 11):
        idx = pos - k
        fd = ind["frac_dn"][idx]
        fu = ind["frac_up"][idx]
        fdp = ind["frac_dn_px"][idx]
        fup = ind["frac_up_px"][idx]
        if not nan(fd) and fd == 1 and not nan(fdp):
            frac_dn_prices.append(fdp)
        if not nan(fu) and fu == 1 and not nan(fup):
            frac_up_prices.append(fup)
        if len(frac_dn_prices) >= 2 and len(frac_up_prices) >= 2:
            break
    c = ind["close"][pos]
    if nan(c):
        return None
    # Higher pivot lows: most recent frac low > prior frac low -> bullish
    if len(frac_dn_prices) >= 2 and frac_dn_prices[0] > frac_dn_prices[1]:
        return "long"
    # Lower pivot highs: most recent frac high < prior frac high -> bearish
    if len(frac_up_prices) >= 2 and frac_up_prices[0] < frac_up_prices[1]:
        return "short"
    return None
