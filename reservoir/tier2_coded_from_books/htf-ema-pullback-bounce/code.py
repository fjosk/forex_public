# Engine signal function for 'htf_ema_pullback_bounce' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def htf_ema_pullback_bounce(I, i, htf):
    if i < 1:
        return None
    bias = htf["bias"][i]
    e21, e21_1 = I["ema21"][i], I["ema21"][i-1]
    l, h = I["low"][i], I["high"][i]
    c, c1 = I["close"][i], I["close"][i-1]
    if _nan(bias, e21, e21_1, l, h, c, c1):
        return None
    rising = e21 > e21_1
    falling = e21 < e21_1
    if bias > 0 and rising and l <= e21 and c > e21 and c >= c1:
        return "long"   # HTF up, EMA21 rising, pullback touches it, close reclaims + up bar
    if bias < 0 and falling and h >= e21 and c < e21 and c <= c1:
        return "short"  # HTF down, EMA21 falling, rally touches it, close rejects + down bar
    return None
