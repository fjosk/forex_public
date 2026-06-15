# Engine signal function for 'three_bar_hl_revert' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def three_bar_hl_revert(I, i, htf):
    if i < 3:
        return None
    c = I['close'][i]; e50 = I['ema50'][i]
    lo = I['low'][i]; hi = I['high'][i]
    s3l = I['sma3_low'][i]; s3h = I['sma3_high'][i]
    if _nan(c, e50, lo, hi, s3l, s3h):
        return None
    trend_up = c > e50
    trend_dn = c < e50
    if trend_up and lo <= s3l:
        return 'long'
    if trend_dn and hi >= s3h:
        return 'short'
    return None
