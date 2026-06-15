# Engine signal function for 'gravestone_dragonfly_doji' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def gravestone_dragonfly_doji(I, i, htf):
    if i < 0:
        return None
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]; c = I['close'][i]
    e = I['ema20'][i]
    if _nan(o, h, l, c, e):
        return None
    rng = h - l
    if rng <= 0:
        return None
    body = abs(c - o)
    is_doji = body <= 0.05 * rng
    if not is_doji:
        return None
    upper = h - max(o, c)
    lower = min(o, c) - l
    if lower <= 0.1 * rng and upper >= 0.6 * rng and c > e:
        return 'short'
    if upper <= 0.1 * rng and lower >= 0.6 * rng and c < e:
        return 'long'
    return None
