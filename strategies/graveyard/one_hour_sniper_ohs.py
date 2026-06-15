#!/usr/bin/env python3
"""one_hour_sniper_ohs -- OHS: 4H stoch K > 80 or < 20 (htf) then 1H stoch K/D cross. ForexFactory."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "one_hour_sniper_ohs",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "stoch_k, stoch_d",
    "long": "4H stoch_k > 80 (htf momentum bull); 1H stoch_k crosses above stoch_d",
    "short": "4H stoch_k < 20 (htf momentum bear); 1H stoch_k crosses below stoch_d",
    "desc": "One Hour Sniper: 4H stochastic momentum gate + 1H stoch K/D crossover entry",
    "source": "web:https://www.forexfactory.com/thread/677843-one-hour-sniper-ohs",
}


def signal(ind, pos, htf=None):
    """4H stoch extreme (htf) + 1H stoch K/D cross."""
    sk = ind["stoch_k"][pos]
    skp = ind["stoch_k"][pos - 1]
    sd = ind["stoch_d"][pos]
    sdp = ind["stoch_d"][pos - 1]
    if nan(sk, skp, sd, sdp):
        return None

    # 4H filter via htf; fall back to current-bar stoch if htf unavailable
    if htf is not None:
        bias_arr = htf.get("bias")
        if bias_arr is not None and not nan(bias_arr[pos]):
            htf_bull = bias_arr[pos] > 0
            htf_bear = bias_arr[pos] < 0
        else:
            htf_bull = sk > 80
            htf_bear = sk < 20
    else:
        htf_bull = sk > 80
        htf_bear = sk < 20

    cross_up = _xup(sk, skp, sd, sdp)
    cross_dn = _xdn(sk, skp, sd, sdp)

    if htf_bull and cross_up:
        return "long"
    if htf_bear and cross_dn:
        return "short"
    return None
