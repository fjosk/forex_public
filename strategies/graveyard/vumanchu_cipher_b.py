#!/usr/bin/env python3
"""vumanchu_cipher_b -- VuManChu Cipher B: WaveTrend cross in oversold/overbought + RSI momentum. web:tradingview.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "vumanchu_cipher_b",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h",
    "indicators": "wt1, wt2, rsi",
    "long": "wt1 crosses above wt2 with wt2 < -60 and rsi > 50 (money-flow proxy positive)",
    "short": "wt1 crosses below wt2 with wt2 > 60 and rsi < 50",
    "desc": "VuManChu Cipher B core signal: WaveTrend cross in extreme zones gated by RSI momentum",
    "source": "web:https://www.tradingview.com/script/Msm4SjwI-VuManChu-Cipher-B-Divergences/",
}


def signal(ind, pos, htf=None):
    """WaveTrend cross in oversold/overbought zone with RSI momentum gate."""
    w1 = ind["wt1"][pos]
    w2 = ind["wt2"][pos]
    w1p = ind["wt1"][pos - 1]
    w2p = ind["wt2"][pos - 1]
    rs = ind["rsi"][pos]
    if nan(w1, w2, w1p, w2p, rs):
        return None
    # green circle: wt1 crosses above wt2 in oversold, RSI-momentum positive
    if _xup(w1, w1p, w2, w2p) and w2 < -60 and rs > 50:
        return "long"
    # red circle: wt1 crosses below wt2 in overbought, RSI-momentum negative
    if _xdn(w1, w1p, w2, w2p) and w2 > 60 and rs < 50:
        return "short"
    return None
