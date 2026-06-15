# Engine signal function for 'roc_band_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def roc_band_fade(I, i, htf):
    if i < 1:
        return None
    r = I['roc'][i]; r1 = I['roc'][i-1]; sd = I['roc_sd'][i]
    if _nan(r, r1, sd):
        return None
    upper = 2.0 * sd
    lower = -2.0 * sd
    if r1 < lower and r > r1:
        return 'long'
    if r1 > upper and r < r1:
        return 'short'
    return None
