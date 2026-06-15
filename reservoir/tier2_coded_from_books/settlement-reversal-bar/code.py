# Engine signal function for 'settlement_reversal_bar' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def settlement_reversal_bar(I, i, htf):
    if i < 1:
        return None
    hi, hi1 = I["high"][i], I["high"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    c, c1 = I["close"][i], I["close"][i-1]
    e1 = I["ema20"][i-1]
    if _nan(hi, hi1, lo, lo1, c, c1, e1):
        return None
    if hi > hi1 and lo > lo1 and c < c1 and c1 > e1:
        return "short"
    if lo < lo1 and hi < hi1 and c > c1 and c1 < e1:
        return "long"
    return None
