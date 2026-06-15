# Engine signal function for 'gap_climax_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def gap_climax_reversal(I, i, htf):
    if i < 5:
        return None
    ap, ap5 = I["atr_pct"][i], I["atr_pct"][i-5]
    do = I["day_open"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    c, hi, lo = I["close"][i], I["high"][i], I["low"][i]
    if _nan(ap, ap5, do, pdll, pdhh, c, hi, lo):
        return None
    vol_spike = ap > 1.8 * ap5
    rng = max(hi - lo, 1e-9)
    close_pos = (c - lo) / rng
    if vol_spike and do < pdll and close_pos >= 0.66:    # gap down on a vol climax, closing strong off the low -> long
        return "long"
    if vol_spike and do > pdhh and close_pos <= 0.34:    # gap up on a vol climax, closing weak off the high -> short
        return "short"
    return None
