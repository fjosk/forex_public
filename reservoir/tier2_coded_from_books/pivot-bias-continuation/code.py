# Engine signal function for 'pivot_bias_continuation' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def pivot_bias_continuation(I, i, htf):
    if i < 1:
        return None
    p, r1, s1 = I['piv_p'][i], I['piv_r1'][i], I['piv_s1'][i]
    c, c1, e20 = I['close'][i], I['close'][i-1], I['ema20'][i]
    if _nan(p, r1, s1, c, c1, e20):
        return None
    if c1 <= p and c > p and c > e20 and c < r1:
        return 'long'
    if c1 >= p and c < p and c < e20 and c > s1:
        return 'short'
    return None
