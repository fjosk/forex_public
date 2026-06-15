# Engine signal function for 'rsi_revert_chop_gated' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def rsi_revert_chop_gated(I, i, htf):
    if i < 1:
        return None
    r, r1, adx = I["rsi"][i], I["rsi"][i-1], I["adx"][i]
    if _nan(r, r1, adx):
        return None
    if adx >= 25:                             # only fade in a non-trending regime
        return None
    if r1 <= 25 and r > 25:                    # RSI re-crosses up through 25
        return "long"
    if r1 >= 75 and r < 75:                    # RSI re-crosses down through 75
        return "short"
    return None
