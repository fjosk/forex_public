# Engine signal function for 'momentum_break_macdhist_chop' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def momentum_break_macdhist_chop(I, i, htf):
    if i < 1:
        return None
    chop, c, du, dl, mh = I["chop"][i], I["close"][i], I["dc_up"][i-1], I["dc_lo"][i-1], I["macd_hist"][i]
    if _nan(chop, c, du, dl, mh):
        return None
    flat = chop > 55
    if flat and c > du and mh > 0:
        return "long"
    if flat and c < dl and mh < 0:
        return "short"
    return None
