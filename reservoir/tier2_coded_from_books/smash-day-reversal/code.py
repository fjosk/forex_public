# Engine signal function for 'smash_day_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def smash_day_reversal(I, i, htf):
    if i < 2:
        return None
    c1 = I["close"][i-1]
    lo2, lo1, lo = I["low"][i-2], I["low"][i-1], I["low"][i]
    hi2, hi1, hi = I["high"][i-2], I["high"][i-1], I["high"][i]
    if _nan(c1, lo2, lo1, lo, hi2, hi1, hi):
        return None
    if c1 < lo2 and hi > hi1:                 # prior bar smashed below the bar before it, now breaking back up -> long
        return "long"
    if c1 > hi2 and lo < lo1:                 # prior bar smashed above the bar before it, now breaking back down -> short
        return "short"
    return None
