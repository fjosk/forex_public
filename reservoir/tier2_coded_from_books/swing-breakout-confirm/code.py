# Engine signal function for 'swing_breakout_confirm' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def swing_breakout_confirm(I, i, htf):
    if i < 1:
        return None
    trig_hi = I["frac_dn_bar_high"][i]
    trig_lo = I["frac_up_bar_low"][i]
    c = I["close"][i]
    c1 = I["close"][i - 1]
    if _nan(c, c1):
        return None
    if not _nan(trig_hi) and c1 <= trig_hi and c > trig_hi:
        return "long"
    if not _nan(trig_lo) and c1 >= trig_lo and c < trig_lo:
        return "short"
    return None
