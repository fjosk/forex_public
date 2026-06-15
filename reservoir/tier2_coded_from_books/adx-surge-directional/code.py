# Engine signal function for 'adx_surge_directional' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def adx_surge_directional(I, i, htf):
    if i < 2:
        return None
    adx = I['adx'][i]; adx2 = I['adx'][i-2]
    dip = I['di_plus'][i]; dim = I['di_minus'][i]
    if _nan(adx, adx2, dip, dim):
        return None
    if adx - adx2 > 4 and dip > dim:
        return 'long'
    if adx - adx2 > 4 and dim > dip:
        return 'short'
    return None
