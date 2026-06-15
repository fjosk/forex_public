# Engine signal function for 'hidden_smash_day' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def hidden_smash_day(I, i, htf):
    if i < 2:
        return None
    h1, l1, c1, o1, c2 = I["high"][i-1], I["low"][i-1], I["close"][i-1], I["open"][i-1], I["close"][i-2]
    hi, lo = I["high"][i], I["low"][i]
    if _nan(h1, l1, c1, o1, c2, hi, lo):
        return None
    rng = h1 - l1
    if rng <= 0:
        return None
    buy_setup = c1 > c2 and c1 <= l1 + 0.25 * rng and c1 < o1
    sell_setup = c1 < c2 and c1 >= h1 - 0.25 * rng and c1 > o1
    if buy_setup and hi > h1:
        return "long"
    if sell_setup and lo < l1:
        return "short"
    return None
