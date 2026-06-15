# Engine signal function for 'sroc_centerline_turn' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def sroc_centerline_turn(I, i, htf):
    if i < 1:
        return None
    s, s1 = I["sroc"][i], I["sroc"][i-1]
    if _nan(s, s1):
        return None
    if s1 < 0 and s > s1:
        return "long"
    if s1 > 0 and s < s1:
        return "short"
    return None
