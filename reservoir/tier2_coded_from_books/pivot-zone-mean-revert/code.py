# Engine signal function for 'pivot_zone_mean_revert' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def pivot_zone_mean_revert(I, i, htf):
    if i < 1:
        return None
    p, s1, r1 = I['piv_p'][i], I['piv_s1'][i], I['piv_r1'][i]
    c, c1 = I['close'][i], I['close'][i-1]
    lo, hi = I['low'][i], I['high'][i]
    if _nan(p, s1, r1, c, c1, lo, hi):
        return None
    if s1 < c < p and c > c1 and lo < c1:
        return 'long'
    if p < c < r1 and c < c1 and hi > c1:
        return 'short'
    return None
