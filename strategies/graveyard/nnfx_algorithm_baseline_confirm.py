#!/usr/bin/env python3
"""nnfx_algorithm_baseline_confirm -- NNFX: Kijun baseline cross + MACD C1 + QQE C2 + ATR proximity. NoNonsenseTrader/VP."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "nnfx_algorithm_baseline_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ich_kij, atr, macd_hist, qqe_line, qqe_rsima, bb_width",
    "long": "price crosses above Kijun within 1 ATR; macd_hist > 0 (C1); qqe_line > qqe_rsima in last 7 bars (C2); bb_width > atr (non-ranging V1 proxy)",
    "short": "price crosses below Kijun within 1 ATR; macd_hist < 0; qqe_line < qqe_rsima recently; bb_width > atr",
    "desc": "NNFX 6-component algorithm: Kijun baseline + MACD C1 + QQE C2 + volatility gate",
    "source": "web:https://nononsensetrader.com/part-2-no-nonsense-forex-newcomer-starter-guide/",
}

_C2_BARS = 7


def signal(ind, pos, htf=None):
    """Kijun cross within ATR + MACD C1 + QQE C2 recent + bb_width volatility gate."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    kij = ind["ich_kij"][pos]
    kijp = ind["ich_kij"][pos - 1]
    atr = ind["atr"][pos]
    mh = ind["macd_hist"][pos]
    bbw = ind["bb_width"][pos]
    if nan(c, cp, kij, kijp, atr, mh, bbw) or atr <= 0:
        return None

    cross_above = c > kij and cp <= kijp
    cross_below = c < kij and cp >= kijp
    near = abs(c - kij) <= atr

    # C1: MACD histogram direction
    c1_long = mh > 0
    c1_short = mh < 0

    # C2: QQE within last _C2_BARS bars
    c2_long = False
    c2_short = False
    start = max(1, pos - _C2_BARS + 1)
    for i in range(start, pos + 1):
        ql = ind["qqe_line"][i]
        qr = ind["qqe_rsima"][i]
        if not nan(ql, qr):
            if ql > qr:
                c2_long = True
            if ql < qr:
                c2_short = True

    # V1 proxy: bb_width above atr (non-ranging)
    v1_ok = bbw > atr

    if cross_above and near and c1_long and c2_long and v1_ok:
        return "long"
    if cross_below and near and c1_short and c2_short and v1_ok:
        return "short"
    return None
