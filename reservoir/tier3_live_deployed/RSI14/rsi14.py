from __future__ import annotations

"""RSI14 -- RSI(14) reversal taken with the EMA200 trend (added 2026-06-01: the only strategy
that survived walk-forward on a major, on ETH + DOGE). 4h signal. Long when close > EMA200 AND
RSI crosses up through 30; short when close < EMA200 AND RSI crosses down through 70. Exit:
REVERT (ATR sl 1.5x / tp 2.0x / 24h time stop), no opposite-exit.

Signal logic is the monorepo single source `shared.strategies.rsi14`; this builder assembles the
indicator window and carries the exit envelope. Validated 0-diff vs the prior copy + LAB."""

import numpy as np

from trade.strategy._common_4h import MIN_CANDLES_PSAR, _atr, _ema, _ohlc, _sig, _wilder_rsi
from shared.strategies import rsi14 as _rsi14


def build_rsi14_trend_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_PSAR:        # needs EMA200
        return None
    o, h, l, c = _ohlc(c4)
    r = _wilder_rsi(c, 14); e200 = _ema(c, 200); a = _atr(h, l, c, 14)
    side = _rsi14({"rsi": r, "close": c, "ema200": e200}, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None or np.isnan(a[-1]) or a[-1] <= 0:
        return None
    return _sig(coin, side, c[-1], a[-1], ctx, cfg, "RSI14", "rsi14_atr_sl_mult", "rsi14_atr_tp_mult", "rsi14_max_holding_hours")
