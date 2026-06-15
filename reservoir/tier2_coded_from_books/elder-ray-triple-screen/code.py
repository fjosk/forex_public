# Engine signal function for 'elder_ray_triple_screen' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def elder_ray_triple_screen(I, i, htf):
    if i < 1:
        return None
    bias = htf['bias'][i]
    bep, bep1 = I['bear_power'][i], I['bear_power'][i-1]
    bup, bup1 = I['bull_power'][i], I['bull_power'][i-1]
    c, ph, pl = I['close'][i], I['high'][i-1], I['low'][i-1]
    if _nan(bias, bep, bep1, bup, bup1, c, ph, pl):
        return None
    if bias > 0 and bep < 0 and bep > bep1 and c > ph:
        return 'long'
    if bias < 0 and bup > 0 and bup < bup1 and c < pl:
        return 'short'
    return None
