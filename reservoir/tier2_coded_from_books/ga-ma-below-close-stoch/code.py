# Engine signal function for 'ga_ma_below_close_stoch' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def ga_ma_below_close_stoch(I, i, htf):
    if i < 2:
        return None
    m, m1 = I["sma20"][i], I["sma20"][i-1]
    c1, c2 = I["close"][i-1], I["close"][i-2]
    k, k1 = I["stoch_k"][i], I["stoch_k"][i-1]
    if _nan(m, m1, c1, c2, k, k1):
        return None
    long_now = m < c1 and k > 50
    long_prev = m1 < c2 and k1 > 50
    short_now = m > c1 and k < 50
    short_prev = m1 > c2 and k1 < 50
    if long_now and not long_prev:
        return "long"
    if short_now and not short_prev:
        return "short"
    return None
