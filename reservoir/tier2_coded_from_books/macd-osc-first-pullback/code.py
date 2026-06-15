# Engine signal function for 'macd_osc_first_pullback' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def macd_osc_first_pullback(I, i, htf):
    if i < 1:
        return None
    o, s, o1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    if _nan(o, s, o1, s1, lo, lo1, hi, hi1):
        return None
    if o1 > s1 and o <= s and lo > lo1:
        return "long"
    if o1 < s1 and o >= s and hi < hi1:
        return "short"
    return None
