#!/usr/bin/env python3
"""ssl_hybrid_qqe_waddah -- QQE bull + SSL Hybrid bull + WAE momentum gate. kevinmck100 / tradingview.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ssl_hybrid_qqe_waddah",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "qqe_line, qqe_rsima, ssl_hlv, macd, bb_width, atr",
    "long": "qqe_line > qqe_rsima AND ssl_hlv == 1 AND macd increasing AND bb_width > atr",
    "short": "qqe_line < qqe_rsima AND ssl_hlv == -1 AND macd decreasing AND bb_width > atr",
    "desc": "Triple-filter: QQE momentum + SSL Hybrid trend + WAE volatility gate (WAE approx via MACD+bb_width)",
    "source": "web:https://www.tradingview.com/script/YCob5r03-QQE-MOD-SSL-Hybrid-Waddah-Attar-Explosion/",
}


def signal(ind, pos, htf=None):
    """QQE bull + SSL bull + WAE (MACD increasing + bb_width > atr) all align."""
    ql = ind["qqe_line"][pos]
    qr = ind["qqe_rsima"][pos]
    ssl = ind["ssl_hlv"][pos]
    mc = ind["macd"][pos]
    mcp = ind["macd"][pos - 1]
    bbw = ind["bb_width"][pos]
    atr = ind["atr"][pos]
    if nan(ql, qr, ssl, mc, mcp, bbw, atr) or atr <= 0:
        return None
    qqe_bull = ql > qr
    qqe_bear = ql < qr
    ssl_bull = ssl == 1
    ssl_bear = ssl == -1
    wae_up = mc > mcp and bbw > atr
    wae_dn = mc < mcp and bbw > atr
    if qqe_bull and ssl_bull and wae_up:
        return "long"
    if qqe_bear and ssl_bear and wae_dn:
        return "short"
    return None
