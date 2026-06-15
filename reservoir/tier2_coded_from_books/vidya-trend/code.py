# Engine signal function for 'vidya_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def vidya_trend(I, i, htf):
    if i < 1:
        return None
    v, v1, a = I["vidya"][i], I["vidya"][i-1], I["atr"][i]
    if _nan(v, v1, a):
        return None
    band = 0.10 * a
    if v - v1 > band:
        return "long"
    if v - v1 < -band:
        return "short"
    return None
