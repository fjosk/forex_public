#!/usr/bin/env python3
"""buy_on_open_exit_on_close_pattern_consecutive_down_closes -- Three consecutive down closes -> buy. long_term_secrets_to_short_term_trading.

After three consecutive down closes (close[i]<close[i-1]<close[i-2]<close[i-3]), buy at next
bar open (approximated as signal on current close for engine = enters next open). Mean-reversion
pullback buy in any market.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "buy_on_open_exit_on_close_pattern_consecutive_down_closes",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "close",
    "long": "Three consecutive down closes (close[i]<close[i-1]<close[i-2]<close[i-3]) -> buy on next open",
    "short": "none (spec defines long-only pullback buy)",
    "desc": "Three-down-close pullback buy: mean-reversion long after three consecutive down closes",
    "source": "book:long_term_secrets_to_short_term_trading",
}


def signal(ind, pos, htf=None):
    """Three consecutive down closes -> mean-reversion long."""
    if pos < 3:
        return None
    c = ind["close"]
    if nan(c[pos], c[pos-1], c[pos-2], c[pos-3]):
        return None

    if c[pos] < c[pos-1] < c[pos-2] < c[pos-3]:
        return "long"

    return None
