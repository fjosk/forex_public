# Engine signal function for 'stop_run_failed_test' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def stop_run_failed_test(I, i, htf):
    if i < 1:
        return None
    h0, l0, c0 = I["high"][i], I["low"][i], I["close"][i]
    fup, fdn = I["frac_up_px"][i-1], I["frac_dn_px"][i-1]
    if _nan(h0, l0, c0, fup, fdn):
        return None
    poke_up = h0 > fup and c0 < fup
    poke_down = l0 < fdn and c0 > fdn
    if poke_up:
        return "short"
    if poke_down:
        return "long"
    return None
