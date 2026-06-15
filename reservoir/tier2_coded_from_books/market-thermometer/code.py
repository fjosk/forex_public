# Engine signal function for 'market_thermometer' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def market_thermometer(I, i, htf):
    if i < 5:
        return None
    c, e20 = I["close"][i], I["ema20"][i]
    h, h1 = I["high"][i], I["high"][i-1]
    l, l1 = I["low"][i], I["low"][i-1]
    if _nan(c, e20, h, h1, l, l1):
        return None
    quiet_run = True
    for k in range(0, 5):
        t, te = I["thermo"][i-k], I["thermo_ema"][i-k]
        if _nan(t, te) or not (t < te):
            quiet_run = False
            break
    if not quiet_run:
        return None
    if c > e20 and h > h1:
        return "long"
    if c < e20 and l < l1:
        return "short"
    return None
