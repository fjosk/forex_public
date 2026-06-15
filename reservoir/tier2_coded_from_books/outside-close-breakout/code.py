# Engine signal function for 'outside_close_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def outside_close_breakout(I, i, htf):
    if i < 1:
        return None
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    c = I["close"][i]
    if _nan(hi, hi1, lo, lo1, c):
        return None
    outside = hi > hi1 and lo < lo1
    if outside and c > hi1:
        return "long"
    if outside and c < lo1:
        return "short"
    return None
