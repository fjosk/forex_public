# Engine signal function for 'linreg_slope_flip' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def linreg_slope_flip(I, i, htf):
    if i < 1:
        return None
    s, s1 = I["lrs20"][i], I["lrs20"][i-1]
    if _nan(s, s1):
        return None
    if s > 0 and s1 <= 0:
        return "long"
    if s < 0 and s1 >= 0:
        return "short"
    return None
