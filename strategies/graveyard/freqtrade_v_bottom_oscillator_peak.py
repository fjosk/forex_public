#!/usr/bin/env python3
"""freqtrade_v_bottom_oscillator_peak -- V-Bottom RSI+CCI entry (MFI dropped; volume=0 on FX)."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_v_bottom_oscillator_peak",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi, cci, bb_mid",
    "long": "5 declining avg-price bars then uptick AND low < bb_mid AND cci[-1] < -100 AND rsi[-1] < 30",
    "short": "not implemented",
    "desc": "V-bottom entry: 5-bar avg-price decline then uptick, confirmed by CCI+RSI oversold",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/SmoothOperator.py",
}


def signal(ind, pos, htf=None):
    """V-bottom detection: 5 declining avg-price bars + uptick + oscillator oversold."""
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    bbm = ind["bb_mid"][pos]
    cci1 = ind["cci"][pos - 1]
    r1 = ind["rsi"][pos - 1]
    # need 6 bars back
    avgs = []
    for i in range(pos - 5, pos + 1):
        if i < 0:
            return None
        oi, hi, li, ci = o[i], h[i], lo[i], c[i]
        if nan(oi, hi, li, ci):
            return None
        avgs.append((oi + hi + li + ci) / 4.0)
    if nan(bbm, cci1, r1):
        return None
    declining = all(avgs[k] > avgs[k + 1] for k in range(4))
    uptick = avgs[5] > avgs[4]
    if declining and uptick and lo[pos] < bbm and cci1 < -100 and r1 < 30:
        return "long"
    return None
