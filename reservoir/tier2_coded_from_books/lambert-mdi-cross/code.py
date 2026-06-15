# Engine signal function for 'lambert_mdi_cross' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def lambert_mdi_cross(I, i, htf):
    if i < 1:
        return None
    m, m1 = I["mdi"][i], I["mdi"][i-1]
    if _nan(m, m1):
        return None
    if m > 0 and m1 <= 0:
        return "long"
    if m < 0 and m1 >= 0:
        return "short"
    return None
