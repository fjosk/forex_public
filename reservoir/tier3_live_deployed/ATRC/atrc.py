from __future__ import annotations

"""ATRC -- ATR-channel breakout (4h). Close breaks EMA20 +/- 2*ATR with EMA20 sloping the
same way. Walk-forward survivor, scoped to HYPE. ATR sl 2.0x / tp 4.0x, no opposite-exit.

Signal logic is the monorepo single source `shared.strategies.atrc`; this builder only assembles
the indicator window, applies allow_shorts, and carries the exit envelope. Validated 0-diff vs
the prior self-contained copy and vs the LAB backtest."""

from trade.strategy._common_4h import MIN_CANDLES_SHORT, _atr, _ema, _ohlc, _sig
from shared.strategies import atrc as _atrc


def build_atr_channel_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_SHORT:
        return None
    o, h, l, c = _ohlc(c4)
    ind = {"close": c, "ema20": _ema(c, 20), "atr": _atr(h, l, c, 14)}
    side = _atrc(ind, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None:
        return None
    return _sig(coin, side, c[-1], ind["atr"][-1], ctx, cfg, "ATRC", "atrc_atr_sl_mult", "atrc_atr_tp_mult", "atrc_max_holding_hours")
