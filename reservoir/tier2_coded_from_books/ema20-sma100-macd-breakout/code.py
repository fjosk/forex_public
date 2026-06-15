# Engine signal function for 'ema20_sma100_macd_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def ema20_sma100_macd_breakout(I, i, htf):
    if i < 6:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    e20, e201 = I["ema20"][i], I["ema20"][i-1]
    s100, s1001 = I["sma100"][i], I["sma100"][i-1]
    if _nan(c, c1, e20, e201, s100, s1001):
        return None
    crossed_up = c > e20 and c > s100 and (c1 <= e201 or c1 <= s1001)
    crossed_dn = c < e20 and c < s100 and (c1 >= e201 or c1 >= s1001)
    macd_up_recent = False
    macd_dn_recent = False
    for k in range(0, 5):
        h0, hm1 = I["macd_hist"][i-k], I["macd_hist"][i-k-1]
        if _nan(h0, hm1):
            continue
        if h0 > 0 and hm1 <= 0:
            macd_up_recent = True
        if h0 < 0 and hm1 >= 0:
            macd_dn_recent = True
    if crossed_up and macd_up_recent:
        return "long"
    if crossed_dn and macd_dn_recent:
        return "short"
    return None
