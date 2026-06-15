# Engine signal function for 'p3t_pivot_stoch_confluence' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def p3t_pivot_stoch_confluence(I, i, htf):
    if i < 1:
        return None
    s1, r1 = I['piv_s1'][i], I['piv_r1'][i]
    lo, hi, c = I['low'][i], I['high'][i], I['close'][i]
    k, k1 = I['stoch_k'][i], I['stoch_k'][i-1]
    d, d1 = I['stoch_d'][i], I['stoch_d'][i-1]
    if _nan(s1, r1, lo, hi, c, k, k1, d, d1):
        return None
    if lo <= s1 and c > s1 and k1 < 30 and k1 <= d1 and k > d:
        return 'long'
    if hi >= r1 and c < r1 and k1 > 70 and k1 >= d1 and k < d:
        return 'short'
    return None
