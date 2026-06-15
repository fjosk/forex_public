# Engine signal function for 'willr_protrend_pullback' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def willr_protrend_pullback(I, i, htf):
    if i < 1:
        return None
    w, w1 = I["willr"][i], I["willr"][i-1]
    e50, e200 = I["ema50"][i], I["ema200"][i]
    if _nan(w, w1, e50, e200):
        return None
    trend_up = e50 > e200
    if trend_up and w1 <= -95 and w > w1:     # deep oversold pullback turning up in an uptrend
        return "long"
    if (not trend_up) and w1 >= -10 and w < w1:  # deep overbought pullback turning down in a downtrend
        return "short"
    return None
