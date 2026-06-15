#!/usr/bin/env python3
"""liquidity_sweep_stop_hunt -- Liquidity sweep / stop hunt reversal. SMC community.

Price spikes beyond a fractal swing level (stop cluster), then snaps back inside
the range on the same or next bar. The snap-back is the trade direction.
Spike must be meaningful (0.3-2.0 ATR) to filter noise and genuine breakouts.
Source: web:https://fxopen.com/blog/en/what-is-a-liquidity-sweep-and-how-can-you-use-it-in-trading/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "liquidity_sweep_stop_hunt",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr, hour_utc",
    "long": "low spikes below frac_dn_px by 0.3-2.0 ATR and close snaps back above it; London or NY killzone",
    "short": "high spikes above frac_up_px by 0.3-2.0 ATR and close snaps back below it; killzone active",
    "desc": "Liquidity sweep stop-hunt reversal with ATR size gate and killzone filter",
    "source": "web:https://fxopen.com/blog/en/what-is-a-liquidity-sweep-and-how-can-you-use-it-in-trading/",
}


def signal(ind, pos, htf=None):
    """Liquidity sweep: spike beyond fractal level then body return within same bar; killzone + ATR gate."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    atr = ind["atr"][pos]
    h = ind["hour_utc"][pos]
    if nan(c, lo, hi, frac_lo, frac_hi, atr, h) or atr == 0:
        return None

    # Killzone: London (07-10 UTC) or NY AM (12-15 UTC)
    in_kz = (7 <= h < 10) or (12 <= h < 15)
    if not in_kz:
        return None

    # Long: sell-side sweep -- low pierces below fractal low; body closes back above
    if lo < frac_lo and c > frac_lo:
        spike = frac_lo - lo
        if 0.3 * atr <= spike <= 2.0 * atr:
            return "long"

    # Short: buy-side sweep -- high pierces above fractal high; body closes back below
    if hi > frac_hi and c < frac_hi:
        spike = hi - frac_hi
        if 0.3 * atr <= spike <= 2.0 * atr:
            return "short"

    return None
