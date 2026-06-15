# Engine signal function for 'pivot_ma_confluence_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def pivot_ma_confluence_reversal(I, i, htf):
    s1, r1 = I['piv_s1'][i], I['piv_r1'][i]
    e20, e50 = I['ema20'][i], I['ema50'][i]
    c, lo, hi = I['close'][i], I['low'][i], I['high'][i]
    if _nan(s1, r1, e20, e50, c, lo, hi):
        return None
    tol = 0.004 * c
    if (abs(s1 - e20) <= tol or abs(s1 - e50) <= tol) and lo <= s1 and c > s1:
        return 'long'
    if (abs(r1 - e20) <= tol or abs(r1 - e50) <= tol) and hi >= r1 and c < r1:
        return 'short'
    return None
