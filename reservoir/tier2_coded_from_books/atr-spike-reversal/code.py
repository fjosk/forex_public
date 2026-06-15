# Engine signal function for 'atr_spike_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def atr_spike_reversal(I, i, htf):
    if i < 1:
        return None
    K = 1.0
    h, h1 = I["high"][i], I["high"][i-1]
    l, l1 = I["low"][i], I["low"][i-1]
    hh1, ll1, a1 = I["hh_n"][i-1], I["ll_n"][i-1], I["atr"][i-1]
    if _nan(h, h1, l, l1, hh1, ll1, a1):
        return None
    if (h1 - hh1) > K * a1 and h < h1:
        return "short"
    if (ll1 - l1) > K * a1 and l > l1:
        return "long"
    return None
