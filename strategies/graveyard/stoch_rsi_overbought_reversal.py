#!/usr/bin/env python3
"""stoch_rsi_overbought_reversal -- StochRSI K/D cross in oversold/overbought zone. OANDA trading education."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "stoch_rsi_overbought_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "srsi_k, srsi_d",
    "long": "srsi_k crosses above srsi_d AND both < 20 (oversold zone)",
    "short": "srsi_k crosses below srsi_d AND both > 80 (overbought zone)",
    "desc": "Stochastic RSI K/D crossover in oversold (<20) or overbought (>80) zone",
    "source": "web:https://www.oanda.com/us-en/trade-tap-blog/trading-knowledge/mastering-stochastic-oscillator-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """srsi_k/srsi_d crossover in extreme zones."""
    sk = ind["srsi_k"][pos]
    skp = ind["srsi_k"][pos - 1]
    sd = ind["srsi_d"][pos]
    sdp = ind["srsi_d"][pos - 1]
    if nan(sk, skp, sd, sdp):
        return None
    cross_up = _xup(sk, skp, sd, sdp)
    cross_dn = _xdn(sk, skp, sd, sdp)
    oversold = sk < 20 and sd < 20
    overbought = sk > 80 and sd > 80
    if cross_up and oversold:
        return "long"
    if cross_dn and overbought:
        return "short"
    return None
