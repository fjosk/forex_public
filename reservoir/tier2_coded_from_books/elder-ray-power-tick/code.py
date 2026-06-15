# Engine signal function for 'elder_ray_power_tick' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def elder_ray_power_tick(I, i, htf):
    if i < 1:
        return None
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    bep, bep1 = I["bear_power"][i], I["bear_power"][i-1]
    bup, bup1 = I["bull_power"][i], I["bull_power"][i-1]
    if _nan(e21, e21p, bep, bep1, bup, bup1):
        return None
    ema_up = e21 > e21p
    if ema_up and bep < 0 and bep > bep1:     # uptrend: bear power negative but ticking up (dip ending)
        return "long"
    if (not ema_up) and bup > 0 and bup < bup1:  # downtrend: bull power positive but ticking down (rally ending)
        return "short"
    return None
