#!/usr/bin/env python3
"""geraked_2macdsto_dual_macd_stochastic -- MACD + macd_hist sign as second MACD proxy + Stochastic. geraked."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "geraked_2macdsto_dual_macd_stochastic",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "macd, macd_sig, macd_hist, stoch_k, stoch_d",
    "long": "MACD>sig AND macd_hist positive (second MACD proxy) AND stoch_k>stoch_d from oversold (<30)",
    "short": "MACD<sig AND macd_hist negative AND stoch_k<stoch_d from overbought (>70)",
    "desc": "Dual MACD + Stochastic three-way confluence (macd_hist sign used as second MACD proxy)",
    "source": "geraked/metatrader5 GitHub 2MACDSTO strategy",
}


def signal(ind, pos, htf=None):
    """Three-way MACD/Stochastic convergence; macd_hist sign proxies a second MACD instance."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    mh = ind["macd_hist"][pos]
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    if nan(m, ms, mh, sk, sd):
        return None
    macd1_bull = m > ms
    macd1_bear = m < ms
    # macd_hist sign proxies agreement from a second MACD perspective
    macd2_bull = mh > 0
    macd2_bear = mh < 0
    stoch_bull = sk > sd and sk < 30
    stoch_bear = sk < sd and sk > 70
    if macd1_bull and macd2_bull and stoch_bull:
        return "long"
    if macd1_bear and macd2_bear and stoch_bear:
        return "short"
    return None
