# Engine signal function for 'perfect_order_5ma' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def perfect_order_5ma(I, i, htf):
    if i < 1:
        return None
    s10, s20, s50, s100, s200 = I["sma10"][i], I["sma20"][i], I["sma50"][i], I["sma100"][i], I["sma200"][i]
    adx, adx1 = I["adx"][i], I["adx"][i-1]
    if _nan(s10, s20, s50, s100, s200, adx, adx1):
        return None
    bull = s10 > s20 > s50 > s100 > s200
    bear = s10 < s20 < s50 < s100 < s200
    if bull and adx > 20 and adx > adx1:
        return "long"
    if bear and adx > 20 and adx > adx1:
        return "short"
    return None
