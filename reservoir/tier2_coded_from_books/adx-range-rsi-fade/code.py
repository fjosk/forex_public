# Engine signal function for 'adx_range_rsi_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def adx_range_rsi_fade(I, i, htf):
    if i < 0:
        return None
    adx, r, k = I["adx"][i], I["rsi"][i], I["stoch_k"][i]
    c, bl, bu = I["close"][i], I["bb_lo"][i], I["bb_up"][i]
    if _nan(adx, r, k, c, bl, bu):
        return None
    ranging = adx < 25
    if ranging and (r < 30 or k < 20) and c <= bl:
        return "long"
    if ranging and (r > 70 or k > 80) and c >= bu:
        return "short"
    return None
