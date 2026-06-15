# Engine signal function for 'stoch_extreme_touch_trend_gated' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def stoch_extreme_touch_trend_gated(I, i, htf):
    if i < 1:
        return None
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    k = I["stoch_k"][i]
    if _nan(e21, e21p, k):
        return None
    ema_up = e21 > e21p
    if ema_up and k <= 15:                    # buy oversold dips only when EMA21 is rising
        return "long"
    if (not ema_up) and k >= 85:               # sell overbought pops only when EMA21 is falling
        return "short"
    return None
