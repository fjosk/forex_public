#!/usr/bin/env python3
"""qqe_line_crossover -- QQE fast/slow line cross in sub-50 or supra-50 zone. theforexgeek.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "qqe_line_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "qqe_line, qqe_rsima",
    "long": "qqe_line crosses above qqe_rsima while qqe_line < 50 (oversold cross)",
    "short": "qqe_line crosses below qqe_rsima while qqe_line > 50 (overbought cross)",
    "desc": "QQE line / RSI-MA crossover in oversold (<50) or overbought (>50) zone",
    "source": "web:https://theforexgeek.com/qqe-strategy/",
}


def signal(ind, pos, htf=None):
    """QQE line crosses qqe_rsima in the appropriate zone."""
    ql = ind["qqe_line"][pos]
    qlp = ind["qqe_line"][pos - 1]
    qr = ind["qqe_rsima"][pos]
    qrp = ind["qqe_rsima"][pos - 1]
    if nan(ql, qlp, qr, qrp):
        return None
    if _xup(ql, qlp, qr, qrp) and ql < 50:
        return "long"
    if _xdn(ql, qlp, qr, qrp) and ql > 50:
        return "short"
    return None
