from __future__ import annotations

"""COPP -- Coppock curve zero-cross (4h). Long when Coppock crosses up through 0, short on
the mirror. Walk-forward survivor, scoped to HYPE. ATR sl 2.0x / tp 4.0x, no opposite-exit.

Signal logic is the monorepo single source `shared.strategies.copp`; this builder assembles the
indicator window and carries the exit envelope. Validated 0-diff vs the prior copy + LAB."""

import numpy as np

from trade.strategy._common_4h import MIN_CANDLES_SHORT, _atr, _coppock, _ohlc, _sig
from shared.strategies import copp as _copp


def build_coppock_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_SHORT:
        return None
    o, h, l, c = _ohlc(c4)
    cp = _coppock(c); a = _atr(h, l, c, 14)
    side = _copp({"coppock": cp}, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None or np.isnan(a[-1]) or a[-1] <= 0:
        return None
    return _sig(coin, side, c[-1], a[-1], ctx, cfg, "COPP", "copp_atr_sl_mult", "copp_atr_tp_mult", "copp_max_holding_hours")
