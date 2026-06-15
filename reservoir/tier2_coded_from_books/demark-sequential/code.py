# Engine signal function for 'demark_sequential' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def demark_sequential(I, i, htf):
    # Long side only: dm_buy_countdown (TD buy countdown completing at 13) is the
    # sole precomputed DeMark sequence. There is no dm_sell_countdown / sell_countdown
    # array in the engine, so the mirrored short trigger cannot be evaluated and is
    # dropped (kept causal/long-only rather than fabricated). See unknown_keys.
    if i < 1:
        return None
    cd = I['dm_buy_countdown'][i]; cd1 = I['dm_buy_countdown'][i-1]
    if _nan(cd, cd1):
        return None
    if cd >= 13 and cd1 < 13:
        return 'long'
    return None
