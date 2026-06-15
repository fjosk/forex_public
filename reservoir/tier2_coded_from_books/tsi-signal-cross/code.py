# Engine signal function for 'tsi_signal_cross' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def tsi_signal_cross(I, i, htf):
    if i < 1:
        return None
    t, s, t1, s1 = I["tsi"][i], I["tsi_sig"][i], I["tsi"][i-1], I["tsi_sig"][i-1]
    if _nan(t, s, t1, s1):
        return None
    if _xup(t, t1, s, s1):
        return "long"
    if _xdn(t, t1, s, s1):
        return "short"
    return None
