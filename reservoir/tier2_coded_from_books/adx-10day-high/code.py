# Engine signal function for 'adx_10day_high' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def adx_10day_high(I, i, htf):
    if i < 9:
        return None
    adx = I['adx'][i]; dip = I['di_plus'][i]; dim = I['di_minus'][i]
    if _nan(adx, dip, dim):
        return None
    window = I['adx'][i-9:i+1]
    if any(_nan(v) for v in window):
        return None
    hi = max(window)
    if adx >= hi and dip > dim:
        return 'long'
    if adx >= hi and dim > dip:
        return 'short'
    return None
