# Engine signal function for 'hilo_activator_flip' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def hilo_activator_flip(I, i, htf):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    shi, shi1 = I["sma_high21"][i], I["sma_high21"][i-1]
    slo, slo1 = I["sma_low21"][i], I["sma_low21"][i-1]
    if _nan(c, c1, shi, shi1, slo, slo1):
        return None
    if c > shi and c1 <= shi1:
        return "long"
    if c < slo and c1 >= slo1:
        return "short"
    return None
