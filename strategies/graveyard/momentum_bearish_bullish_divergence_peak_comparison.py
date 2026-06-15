#!/usr/bin/env python3
"""momentum_bearish_bullish_divergence_peak_comparison -- RSI divergence from price fractals:
bullish divergence (price lower low, RSI higher low) -> long; bearish (price higher high, RSI
lower high) -> short.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.6 pp.155-157.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "momentum_bearish_bullish_divergence_peak_comparison",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "rsi, frac_dn_px, frac_up_px, close",
    "long": "Bullish divergence: current fractal low (frac_dn_px) < prior fractal low AND current RSI > RSI at prior fractal low (RSI prior < 40)",
    "short": "Bearish divergence: current fractal high (frac_up_px) > prior fractal high AND current RSI < RSI at prior fractal high (RSI prior > 60)",
    "desc": "Classic RSI/price divergence at fractal swing points: fade new extreme unconfirmed by RSI",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.6 pp.155-157",
}


def signal(ind, pos, htf=None):
    """RSI divergence at fractal swing points (frac_up_px = swing high, frac_dn_px = swing low)."""
    if pos < 2:
        return None
    r = ind["rsi"][pos]
    frac_lo = ind["frac_dn_px"][pos]   # current fractal low price
    frac_hi = ind["frac_up_px"][pos]   # current fractal high price
    if nan(r, frac_lo, frac_hi):
        return None

    # Bearish divergence: current swing high > prior swing high but RSI lower
    for look in range(1, min(20, pos)):
        prev_hi = ind["frac_up_px"][pos - look]
        if nan(prev_hi) or prev_hi <= 0:
            continue
        r_prev = ind["rsi"][pos - look]
        if nan(r_prev):
            continue
        if frac_hi > prev_hi and r < r_prev and r_prev > 60:
            return "short"
        break

    # Bullish divergence: current swing low < prior swing low but RSI higher
    for look in range(1, min(20, pos)):
        prev_lo = ind["frac_dn_px"][pos - look]
        if nan(prev_lo) or prev_lo <= 0:
            continue
        r_prev = ind["rsi"][pos - look]
        if nan(r_prev):
            continue
        if frac_lo < prev_lo and r > r_prev and r_prev < 40:
            return "long"
        break

    return None
