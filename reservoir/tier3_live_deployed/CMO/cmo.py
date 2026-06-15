from __future__ import annotations

"""CMO -- Chande Momentum Oscillator zero-cross, EMA200-trend-filtered (4h). Long when CMO(20)
crosses up through 0 with close>EMA200, short on the mirror. Signal timeframe is 4h (the "swing"
cadence the gauntlet scored it at); reads the candles_4h builder arg, NOT the 1h `candles`.

FORWARD-TEST CANDIDATE, override-added 2026-06-04 (the operator's call). It cleared the official deploy
gate on HYPE + NEAR and was single-holdout walk-forward ROBUST, but it is FRAGILE under the
execution-stress filter, so the standard gated deploy (pipeline.py/deploy_to_trade.py) refuses it.
Added to paper+testnet only to accumulate live evidence; it is NOT a proven edge and is NOT on the
live/mainnet roster. Scoped to HYPE/NEAR via cfg['strategy_universe']['CMO'].

EXIT divergence (accepted, same as COPP/ATRC): the backtest exit used exit_opposite=True, which the
shared TRADE exit core does not implement. Deployed here with ATR sl 2.0x / tp 4.0x / 48h, no
opposite-exit -- so the live forward-test will not track the backtested PnL exactly.

Signal logic is the monorepo single source shared.strategies.cmo_zero; the CMO/EMA200 math is the
shared shared.indicators.cmo/ema, validated 0-diff vs the LAB backtest on the deploy coins.
"""

import numpy as np

from trade.strategy._common_4h import MIN_CANDLES_PSAR, _atr, _cmo, _ema, _ohlc, _sig
from shared.strategies import cmo_zero as _cmo_zero


def build_cmo_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_PSAR:          # EMA200 warmup (shared with PSAR/RSI14 gate)
        return None
    o, h, l, c = _ohlc(c4)
    cmo_arr = _cmo(c, 20); e200 = _ema(c, 200); a = _atr(h, l, c, 14)
    side = _cmo_zero({"cmo": cmo_arr, "ema200": e200, "close": c}, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None or np.isnan(a[-1]) or a[-1] <= 0:
        return None
    return _sig(coin, side, c[-1], a[-1], ctx, cfg, "CMO",
                "cmo_atr_sl_mult", "cmo_atr_tp_mult", "cmo_max_holding_hours")
