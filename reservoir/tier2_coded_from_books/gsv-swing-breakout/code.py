# Engine signal function for 'gsv_swing_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def gsv_swing_breakout(I, i, htf):
    if i < 7:
        return None
    F = 1.8
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]
    c1 = I['close'][i-1]; c6 = I['close'][i-6]; c7 = I['close'][i-7]
    bs = I['buy_swing'][i]; ss = I['sell_swing'][i]
    if _nan(o, h, l, c1, c6, c7, bs, ss):
        return None
    long_setup = c1 < c6
    short_setup = c1 > c7
    if long_setup and h >= o + F * bs:
        return 'long'
    if short_setup and l <= o - F * ss:
        return 'short'
    return None
