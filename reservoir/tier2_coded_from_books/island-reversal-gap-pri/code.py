# Engine signal function for 'island_reversal_gap_pri' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def island_reversal_gap_pri(I, i, htf):
    if i < 2:
        return None
    h0, l0 = I["high"][i], I["low"][i]
    h1, l1 = I["high"][i-1], I["low"][i-1]
    h2, l2 = I["high"][i-2], I["low"][i-2]
    if _nan(h0, l0, h1, l1, h2, l2):
        return None
    gap_up_in = l1 > h2
    gap_dn_out = h0 < l1
    gap_dn_in = h1 < l2
    gap_up_out = l0 > h1
    if gap_up_in and gap_dn_out:
        return "short"
    if gap_dn_in and gap_up_out:
        return "long"
    return None
