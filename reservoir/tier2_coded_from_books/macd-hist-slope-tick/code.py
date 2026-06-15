# Engine signal function for 'macd_hist_slope_tick' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def macd_hist_slope_tick(I, i, htf):
    if i < 2:
        return None
    hh, h1, h2 = I["macd_hist"][i], I["macd_hist"][i-1], I["macd_hist"][i-2]
    if _nan(hh, h1, h2):
        return None
    if hh > h1 and h1 <= h2:
        return "long"
    if hh < h1 and h1 >= h2:
        return "short"
    return None
