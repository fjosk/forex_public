# Engine signal function for 'ewo_wave' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def ewo_wave(I, i, htf):
    if i < 1:
        return None
    e, e1 = I["ewo"][i], I["ewo"][i-1]
    if _nan(e, e1):
        return None
    if e > 0 and e1 <= 0:
        return "long"
    if e < 0 and e1 >= 0:
        return "short"
    return None
