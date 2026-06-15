# Engine signal function for 'oops_gap_fade_pri' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def oops_gap_fade_pri(I, i, htf):
    if i < 1:
        return None
    o = I["open"][i]
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    if _nan(o, hi, hi1, lo, lo1):
        return None
    if o < lo1 and hi >= lo1:                 # gapped below prior low then traded back up into it -> long
        return "long"
    if o > hi1 and lo <= hi1:                 # gapped above prior high then traded back down into it -> short
        return "short"
    return None
