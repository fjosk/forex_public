#!/usr/bin/env python3
"""stochastic_crossover -- Stochastic K/D cross in oversold/overbought zone with EMA200 trend filter. OANDA."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "stoch_k, stoch_d, ema200",
    "long": "%K crosses above %D AND both < 20 (oversold) AND close > ema200",
    "short": "%K crosses below %D AND both > 80 (overbought) AND close < ema200",
    "desc": "Stochastic K/D crossover in oversold/overbought zone with EMA200 trend alignment",
    "source": "web:https://www.oanda.com/us-en/trade-tap-blog/trading-knowledge/mastering-stochastic-oscillator-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Stoch K/D cross in extreme zone aligned with EMA200."""
    sk = ind["stoch_k"][pos]
    skp = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sdp = ind["stoch_d"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(sk, skp, sd, sdp, c, e200):
        return None
    cross_up = _xup(sk, skp, sd, sdp)
    cross_dn = _xdn(sk, skp, sd, sdp)
    oversold = sd < 20
    overbought = sd > 80
    if cross_up and oversold and c > e200:
        return "long"
    if cross_dn and overbought and c < e200:
        return "short"
    return None
