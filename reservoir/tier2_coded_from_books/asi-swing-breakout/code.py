# Engine signal function for 'asi_swing_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def asi_swing_breakout(I, i, htf):
    if i < 1:
        return None
    a, a1 = I["asi"][i], I["asi"][i-1]
    hsp1, lsp1 = I["asi_hsp"][i-1], I["asi_lsp"][i-1]
    if _nan(a, a1, hsp1, lsp1):
        return None
    if a > hsp1 and a1 <= hsp1:
        return "long"
    if a < lsp1 and a1 >= lsp1:
        return "short"
    return None
