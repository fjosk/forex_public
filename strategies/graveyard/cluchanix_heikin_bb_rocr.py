#!/usr/bin/env python3
"""cluchanix_heikin_bb_rocr -- ClucHAnix Heikin-Ashi BB ROCR. freqtrade ssssi/E0V1E."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "cluchanix_heikin_bb_rocr",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "ha_close, ha_open, bb_lo, bb_mid, ema50, roc",
    "long": "roc macro filter positive AND (BB delta dip OR HA below EMA50 deep dip)",
    "short": "not implemented",
    "desc": "ClucHAnix: HA-based BB delta dip or EMA deep dip with ROC macro filter",
    "source": "github.com/ssssi/freqtrade_strs ClucHAnix.py",
}


def signal(ind, pos, htf=None):
    """HA BB-delta or EMA deep-dip entry with ROC macro filter (long only)."""
    hac = ind["ha_close"][pos]
    hac1 = ind["ha_close"][pos - 1]
    hao = ind["ha_open"][pos]
    bbl = ind["bb_lo"][pos]
    bbl1 = ind["bb_lo"][pos - 1]
    bbm = ind["bb_mid"][pos]
    e50 = ind["ema50"][pos]
    roc_v = ind["roc"][pos]
    if nan(hac, hac1, hao, bbl, bbl1, bbm, e50, roc_v):
        return None
    # macro filter: ROC > 0 approximates ROCR > 1 (positive momentum on longer frame)
    if roc_v <= 0:
        return None
    bbdelta = abs(bbm - bbl)
    closedelta = abs(hac - hac1)
    tail = abs(hac - min(hac, hao))
    cond_a = (bbl1 > 0
              and bbdelta > hac * 0.01965
              and closedelta > hac * 0.00556
              and tail < bbdelta * 0.95089
              and hac < bbl1
              and hac <= hac1)
    cond_b = hac < e50 and bbm > 0 and hac < bbm * 0.008
    if cond_a or cond_b:
        return "long"
    return None
