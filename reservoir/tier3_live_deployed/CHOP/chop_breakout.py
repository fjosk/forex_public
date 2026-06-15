from __future__ import annotations

"""CHOP -- Choppiness-regime-exit breakout (4h). When the Choppiness Index(14) drops THROUGH 38.2
(a ranging -> trending transition), enter in the direction of close vs EMA50. Signal timeframe is
4h (the "swing" cadence the gauntlet scored it at); reads the candles_4h builder arg, NOT the 1h
`candles`.

FORWARD-TEST CANDIDATE, override-added 2026-06-04 (the operator's call after the round-3 deep-research
sweep). It cleared the official deploy gate on SOL + NEAR, was 3/3-engine agreement, single-holdout
walk-forward ROBUST, and rolling-WFO ROBUST -- a stronger gauntlet profile than B10/CMO/RSI14 and
identical to the deployed QQE -- but it is FRAGILE under the execution-stress filter, so the
standard gated deploy (pipeline.py/deploy_to_trade.py) refuses it. Added to paper+testnet only to
accumulate live evidence; it is NOT a proven edge and is NOT on the live/mainnet roster. Scoped to
SOL/NEAR via cfg['strategy_universe']['CHOP'].

EXIT parity is EXACT (unlike CMO/COPP/ATRC): the backtest exit is the BREAK archetype with
exit_opposite=False, which the shared TRADE exit core implements directly -- ATR sl 2.0x / tp 4.0x /
36h, no opposite-exit. So the live forward-test tracks the backtested exit policy without divergence.

Signal logic is the monorepo single source shared.strategies.chop_breakout; the Choppiness/EMA50
math is shared.indicators.choppiness/ema, validated identical to the LAB backtest (<3e-14) and
signal-level 0-diff on the deploy coins.
"""

import numpy as np

from trade.strategy._common_4h import MIN_CANDLES_SHORT, _atr, _choppiness, _ema, _ohlc, _sig
from shared.strategies import chop_breakout as _chop_breakout


def build_chop_breakout_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_SHORT:         # EMA50 + Choppiness(14) warmup
        return None
    o, h, l, c = _ohlc(c4)
    chop = _choppiness(h, l, c, 14); e50 = _ema(c, 50); a = _atr(h, l, c, 14)
    side = _chop_breakout({"chop": chop, "ema50": e50, "close": c}, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None or np.isnan(a[-1]) or a[-1] <= 0:
        return None
    return _sig(coin, side, c[-1], a[-1], ctx, cfg, "CHOP",
                "chop_atr_sl_mult", "chop_atr_tp_mult", "chop_max_holding_hours")
