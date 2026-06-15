# Engine signal function for 'macd_hist_seasons' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def macd_hist_seasons(I, i, htf):
    if i < 1:
        return None
    hh, h1 = I["macd_hist"][i], I["macd_hist"][i-1]
    if _nan(hh, h1):
        return None
    rising = hh > h1
    if hh < 0 and rising:
        return "long"
    if hh > 0 and not rising:
        return "short"
    return None
