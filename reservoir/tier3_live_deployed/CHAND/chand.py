from __future__ import annotations

"""CHAND -- Chandelier Exit direction flip (4h). Long when the ratcheting Chandelier direction
flips -1 -> +1, short on the mirror +1 -> -1. Signal timeframe is 4h (the "swing" cadence the
gauntlet scored it at); reads the candles_4h builder arg, NOT the 1h `candles`.

FORWARD-TEST CANDIDATE, override-added 2026-06-04 (the operator's call). It was the strongest new gate
clearer: it passed the official gate AND both walk-forwards (single-holdout ROBUST + rolling
robust) on SUI, failing ONLY the execution-stress filter (FRAGILE), so the gated deploy refuses
it. Added to paper+testnet only to accumulate live evidence; NOT a proven edge, NOT on
live/mainnet. Scoped to SUI via cfg['strategy_universe']['CHAND'].

EXIT divergence (accepted, same as COPP/ATRC/CMO): the backtest exit used exit_opposite=True, which
the shared TRADE exit core does not implement. Deployed with ATR sl 2.0x / tp 4.0x / 48h, no
opposite-exit -- the live forward-test will not track the backtested PnL exactly.

The Chandelier direction is STATEFUL (the stop ratchets across the whole series); the live builder
gets the full ~1000-bar 4h window the runner fetches, well past the convergence point validated by
the signal 0-diff harness. Signal logic is shared.strategies.chandelier; the indicator is
shared.indicators.chandelier_dir(22,3), validated 0-diff vs the LAB backtest on SUI.
"""

import numpy as np

from trade.strategy._common_4h import MIN_CANDLES_SHORT, _atr, _chandelier_dir, _ohlc, _sig
from shared.strategies import chandelier as _chandelier


def build_chandelier_signal(coin, candles, candles_4h, ctx, allow_shorts, cfg=None, sr_cache=None):
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES_SHORT:
        return None
    o, h, l, c = _ohlc(c4)
    cdir = _chandelier_dir(h, l, c, 22, 3.0); a = _atr(h, l, c, 14)
    side = _chandelier({"chand_dir": cdir}, len(c) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None or np.isnan(a[-1]) or a[-1] <= 0:
        return None
    return _sig(coin, side, c[-1], a[-1], ctx, cfg, "CHAND",
                "chand_atr_sl_mult", "chand_atr_tp_mult", "chand_max_holding_hours")
