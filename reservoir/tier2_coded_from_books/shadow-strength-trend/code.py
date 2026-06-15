# Engine signal function for 'shadow_strength_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def shadow_strength_trend(I, i, htf):
    if i < 1:
        return None
    lo = I['lo_shadow_sma'][i]; lo1 = I['lo_shadow_sma'][i-1]
    up = I['up_shadow_sma'][i]; up1 = I['up_shadow_sma'][i-1]
    if _nan(lo, lo1, up, up1):
        return None
    lo_up = lo > lo1
    up_up = up > up1
    if lo_up and not up_up:
        return 'long'
    if up_up and not lo_up:
        return 'short'
    return None
