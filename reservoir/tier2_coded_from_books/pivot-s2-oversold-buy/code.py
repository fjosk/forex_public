# Engine signal function for 'pivot_s2_oversold_buy' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def pivot_s2_oversold_buy(I, i, htf):
    s2, r2 = I['piv_s2'][i], I['piv_r2'][i]
    lo, hi, c = I['low'][i], I['high'][i], I['close'][i]
    rsi, k = I['rsi'][i], I['stoch_k'][i]
    if _nan(s2, r2, lo, hi, c, rsi, k):
        return None
    if lo <= s2 and c > s2 and rsi < 35 and k < 25:
        return 'long'
    if hi >= r2 and c < r2 and rsi > 65 and k > 75:
        return 'short'
    return None
