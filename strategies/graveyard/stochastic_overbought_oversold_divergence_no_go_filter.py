#!/usr/bin/env python3
"""stochastic_overbought_oversold_divergence_no_go_filter -- Elder stochastic OB/OS with no-go filter and EMA trend gate. come_into_my_trading_room_alexander_elder Ch5."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_overbought_oversold_divergence_no_go_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k,stoch_d,ema20",
    "long": "Stoch <= 15 (OS), EMA rising; no-go: do NOT buy when stoch > 85",
    "short": "Stoch >= 85 (OB), EMA falling; no-go: do NOT short when stoch < 15",
    "desc": "Elder stochastic OS/OB entry gated by EMA22 trend with no-go filter at opposite extreme",
    "source": "book: come_into_my_trading_room_alexander_elder, Ch5",
}

OB = 85.0
OS = 15.0


def signal(ind, pos, htf=None):
    """Long near OS zone in uptrend; short near OB zone in downtrend; no-go filter applied."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    if nan(sk, sk1, ema, ema1):
        return None
    trend_up = ema > ema1
    trend_dn = ema < ema1
    # Long: EMA rising, stoch in or touching OS zone, no-go filter (stoch must not be OB)
    if trend_up and sk <= OS and sk > OB - 100:  # no-go already excluded by sk<=OS
        return "long"
    # Short: EMA falling, stoch in or touching OB zone
    if trend_dn and sk >= OB:
        return "short"
    return None
