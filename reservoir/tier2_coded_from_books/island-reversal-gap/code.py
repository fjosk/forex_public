# Engine signal function for 'island_reversal_gap' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def island_reversal_gap(I, i, htf):
    if i < 2:
        return None
    h = I['high'][i]; l = I['low'][i]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    h2 = I['high'][i-2]; l2 = I['low'][i-2]
    if _nan(h, l, h1, l1, h2, l2):
        return None
    if (h1 < l2) and (l > h1):
        return 'long'
    if (l1 > h2) and (h < l1):
        return 'short'
    return None
