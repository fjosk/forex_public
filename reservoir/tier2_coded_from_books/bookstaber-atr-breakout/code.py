# Engine signal function for 'bookstaber_atr_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def bookstaber_atr_breakout(I, i, htf):
    if i < 1:
        return None
    c, c1, a = I["close"][i], I["close"][i-1], I["atr"][i]
    if _nan(c, c1, a):
        return None
    K = 3.0
    if (c - c1) > K * a:
        return "long"
    if (c1 - c) > K * a:
        return "short"
    return None
