# Engine signal function for 'sr_role_reversal_retest' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def sr_role_reversal_retest(I, i, htf):
    if i < 2:
        return None
    c, c2 = I['close'][i], I['close'][i-2]
    lo, hi = I['low'][i], I['high'][i]
    res, sup = I['frac_up_px'][i-2], I['frac_dn_px'][i-2]
    if _nan(c, c2, lo, hi, res, sup):
        return None
    if c2 > res and lo <= res * 1.001 and c > res:
        return 'long'
    if c2 < sup and hi >= sup * 0.999 and c < sup:
        return 'short'
    return None
