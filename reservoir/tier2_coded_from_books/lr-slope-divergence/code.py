# Engine signal function for 'lr_slope_divergence' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def lr_slope_divergence(I, i, htf):
    if i < 1:
        return None
    sp = I['lr_slope_price'][i]; sr = I['lr_slope_rsi'][i]
    if _nan(sp, sr):
        return None
    if sp < 0 and sr > 0:
        return 'long'
    if sp > 0 and sr < 0:
        return 'short'
    return None
