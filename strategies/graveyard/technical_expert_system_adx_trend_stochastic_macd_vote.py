#!/usr/bin/env python3
"""technical_expert_system_adx_stoch_macd -- Fishman-Barr-Loick expert system: ADX trend + stochastic + MACD vote. trading_systems_and_methods_kaufman_perry_j_kaufma.

Trending market: ADX > 18 AND ADX >= ADX[2 bars ago].
Long: stochastic high-zone crossover (SK[1]>70 AND SD[1]>70 AND SK crosses above SD) OR MACD > signal.
Short: stochastic low-zone crossover (SK[1]<30 AND SD[1]<30 AND SK crosses below SD) OR MACD < signal.
Requires trending regime AND at least one of stochastic/MACD to fire.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "technical_expert_system_adx_trend_stochastic_macd_vote",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,stoch_k,stoch_d,macd,macd_sig",
    "long": "ADX trending (>18, rising) AND (stochastic high-zone cross or MACD above signal)",
    "short": "ADX trending AND (stochastic low-zone cross or MACD below signal)",
    "desc": "Technical expert system: ADX trend filter with stochastic + MACD voting rules",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch20 Rules 1-8",
}


def signal(ind, pos, htf=None):
    """ADX-gated expert system: stoch and MACD vote for direction."""
    if pos < 2:
        return None
    dx   = ind["adx"][pos]
    dx2  = ind["adx"][pos - 2]
    sk   = ind["stoch_k"][pos]
    sk1  = ind["stoch_k"][pos - 1]
    sd   = ind["stoch_d"][pos]
    sd1  = ind["stoch_d"][pos - 1]
    mc   = ind["macd"][pos]
    ms   = ind["macd_sig"][pos]
    if nan(dx, dx2, sk, sk1, sd, sd1, mc, ms):
        return None
    trending = dx > 18 and dx >= dx2
    if not trending:
        return None
    # Long vote: stoch high-zone crossover or MACD above signal
    stoch_long  = sk1 > 70 and sd1 > 70 and sk > sd and sk1 <= sd1
    macd_long   = mc > ms
    # Short vote: stoch low-zone crossover or MACD below signal
    stoch_short = sk1 < 30 and sd1 < 30 and sk < sd and sk1 >= sd1
    macd_short  = mc < ms
    if stoch_long or macd_long:
        if not (stoch_short or macd_short):
            return "long"
    if stoch_short or macd_short:
        if not (stoch_long or macd_long):
            return "short"
    return None
