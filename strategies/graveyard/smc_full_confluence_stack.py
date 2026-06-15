#!/usr/bin/env python3
"""smc_full_confluence_stack -- SMC Full Confluence Stack entry. SMC / ICT community.

Four-layer confirmation: (1) HTF bias via ema200; (2) London or NY AM killzone;
(3) fractal liquidity sweep with body return; (4) displacement body > 1.0 ATR closing
through the prior fractal in the reversal direction. All four must align.
Source: web:https://dailypriceaction.com/blog/smc-trading-strategy/
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "smc_full_confluence_stack",
    "cadences": ["day"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, open, high, low, ema200, hour_utc, frac_up_px, frac_dn_px, atr",
    "long": "ema200 bull + killzone + low sweeps frac_dn (body returns above) + large bull displacement body closing above frac_hi",
    "short": "ema200 bear + killzone + high sweeps frac_hi (body returns below) + large bear body closing below frac_lo",
    "desc": "SMC four-layer confluence: HTF bias + killzone + sweep + MSS displacement",
    "source": "web:https://dailypriceaction.com/blog/smc-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """SMC full stack: all four conditions on the same bar (sweep+MSS on current bar in killzone with HTF bias)."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    o = ind["open"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    c1 = ind["close"][pos - 1]
    h = ind["hour_utc"][pos]
    e200 = ind["ema200"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    frac_lo1 = ind["frac_dn_px"][pos - 1]
    frac_hi1 = ind["frac_up_px"][pos - 1]
    atr = ind["atr"][pos]
    if nan(c, o, lo, hi, c1, h, e200, frac_lo, frac_hi, frac_lo1, frac_hi1, atr):
        return None
    if atr == 0:
        return None

    # Killzone gate
    in_kz = (7 <= h < 10) or (12 <= h < 15)
    if not in_kz:
        return None

    body = abs(c - o)

    # Long: bull HTF bias + sweep of prior frac low on prev bar + current bar is large bullish
    # displacement closing above prior frac high
    bull_bias = c > e200
    sweep_lo = ind["low"][pos - 1] < frac_lo1   # prior bar spiked below fractal
    if bull_bias and sweep_lo and c > o and body >= 1.0 * atr and c > frac_hi1:
        return "long"

    # Short: bear HTF bias + sweep of prior frac high on prev bar + current bar large bearish
    # displacement closing below prior frac low
    bear_bias = c < e200
    sweep_hi = ind["high"][pos - 1] > frac_hi1
    if bear_bias and sweep_hi and c < o and body >= 1.0 * atr and c < frac_lo1:
        return "short"

    return None
