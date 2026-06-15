# Shared signal function 'cmo_zero' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def cmo_zero(ind, pos, htf=None):
    """Chande Momentum zero-cross taken with the EMA200 trend: long when CMO crosses up through 0
    while close>EMA200, short when it crosses down through 0 while close<EMA200. ind carries
    cmo/ema200/close. Forward-test candidate (cleared the official gate on HYPE/NEAR but FRAGILE
    under the execution-stress filter; added to paper/testnet to accumulate live evidence)."""
    c, c1, e200, px = ind["cmo"][pos], ind["cmo"][pos - 1], ind["ema200"][pos], ind["close"][pos]
    if _nan(c, c1, e200, px):
        return None
    if c > 0 and c1 <= 0 and px > e200:
        return "long"
    if c < 0 and c1 >= 0 and px < e200:
        return "short"
    return None
