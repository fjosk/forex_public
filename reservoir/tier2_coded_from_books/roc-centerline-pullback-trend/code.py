# Engine signal function for 'roc_centerline_pullback_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def roc_centerline_pullback_trend(I, i, htf):
    if i < 1:
        return None
    e50, e200 = I["ema50"][i], I["ema200"][i]
    r, r1 = I["roc"][i], I["roc"][i-1]
    if _nan(e50, e200, r, r1):
        return None
    trend_up = e50 > e200
    if trend_up and r1 < 0 and r > r1:
        return "long"
    if (not trend_up) and r1 > 0 and r < r1:
        return "short"
    return None
