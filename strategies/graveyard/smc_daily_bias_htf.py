#!/usr/bin/env python3
"""smc_daily_bias_htf -- SMC Daily Bias HTF-to-LTF top-down entry. ICT / SMC community.

Coarse HTF bias via ema200 + sma200_dir; 4h discount/premium zone via frac midpoint;
entry only when price is on the correct side with a fractal sweep reversal confirming.
Source: web:https://innercircletrader.net/tutorials/ict-daily-bias-explained/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "smc_daily_bias_htf",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, ema200, sma200_dir, atr, hour_utc",
    "long": "ema200 bull bias + sma200_dir>0; price in discount zone (below 50% of frac range); sweep+return of frac_dn_px in killzone",
    "short": "ema200 bear bias + sma200_dir<0; price in premium zone; sweep+return of frac_up_px in killzone",
    "desc": "SMC daily bias top-down: HTF bias + discount/premium zone + fractal sweep reversal",
    "source": "web:https://innercircletrader.net/tutorials/ict-daily-bias-explained/",
}


def signal(ind, pos, htf=None):
    """SMC HTF bias: ema200 direction + frac-zone filter + fractal sweep-return in killzone."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    h = ind["hour_utc"][pos]
    e200 = ind["ema200"][pos]
    s200d = ind["sma200_dir"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    if nan(c, lo, hi, h, e200, s200d, frac_lo, frac_hi):
        return None

    # Killzone: London (07-10 UTC) or NY AM (12-15 UTC)
    in_kz = (7 <= h < 10) or (12 <= h < 15)
    if not in_kz:
        return None

    rng = frac_hi - frac_lo
    if rng <= 0:
        return None

    equil = frac_lo + 0.50 * rng

    # Long: bull HTF bias; price in discount (below equil); fractal sweep-return of low
    if c > e200 and s200d > 0 and c < equil:
        if lo < frac_lo and c > frac_lo:
            return "long"

    # Short: bear HTF bias; price in premium (above equil); fractal sweep-return of high
    if c < e200 and s200d < 0 and c > equil:
        if hi > frac_hi and c < frac_hi:
            return "short"

    return None
