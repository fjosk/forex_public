# Engine signal function for 'strength_osc_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def strength_osc_trend(I, i, htf):
    if i < 1:
        return None
    thr = 0.30
    s, s1 = I["strength_osc"][i], I["strength_osc"][i-1]
    if _nan(s, s1):
        return None
    if s > thr and s1 <= thr:
        return "long"
    if s < -thr and s1 >= -thr:
        return "short"
    return None
