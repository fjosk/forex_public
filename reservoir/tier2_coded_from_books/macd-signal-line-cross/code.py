# Engine signal function for 'macd_signal_line_cross' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def macd_signal_line_cross(I, i, htf):
    if i < 1:
        return None
    m, s, m1, s1 = I["macd"][i], I["macd_sig"][i], I["macd"][i-1], I["macd_sig"][i-1]
    if _nan(m, s, m1, s1):
        return None
    if _xup(m, m1, s, s1):
        return "long"
    if _xdn(m, m1, s, s1):
        return "short"
    return None
