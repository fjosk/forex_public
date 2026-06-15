# Engine signal function for 'oops_gap_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def oops_gap_fade(I, i, htf):
    if i < 1:
        return None
    o = I['open'][i]; hi = I['high'][i]; lo = I['low'][i]
    hi1 = I['high'][i-1]; lo1 = I['low'][i-1]
    if _nan(o, hi, lo, hi1, lo1):
        return None
    if o < lo1 and hi >= lo1:
        return 'long'
    if o > hi1 and lo <= hi1:
        return 'short'
    return None
