# Engine signal function for 'gap_range_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def gap_range_fade(I, i, htf):
    if i < 1:
        return None
    do = I["day_open"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    if _nan(do, pdll, pdhh, lo, lo1, hi, hi1):
        return None
    if do < pdll and lo >= lo1:               # gapped below prior-day range, holding (not making new low) -> long
        return "long"
    if do > pdhh and hi <= hi1:               # gapped above prior-day range, capped (not making new high) -> short
        return "short"
    return None
