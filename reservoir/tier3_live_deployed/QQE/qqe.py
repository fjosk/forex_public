from __future__ import annotations

"""
QQE -- Quantitative Qualitative Estimation cross (the strongest edge from the round-2
sister-lab/backtest research sweep, 2026-05-31). Plugged 2026-05-31 to local paper +
testnet alongside B1 and ICHI.

SIGNAL TIMEFRAME IS 4h (validated "swing" cadence). Reads the candles_4h builder arg,
NOT the 1h candles (running it at 1h loses on the portfolio). Mirrors build_b1_signal's
contract exactly.

WHAT IT IS. QQE is a volatility trailing line built on a smoothed RSI:
  rsi = Wilder RSI(14); rsiMa = EMA(rsi, 5);
  atrRsi = |rsiMa - rsiMa[-1]|; MaAtrRsi = EMA(atrRsi, 27); dar = EMA(MaAtrRsi, 27)*4.236;
  qqe_line = ATR-style trailing stop of rsiMa using dar as the band.
Long when rsiMa crosses ABOVE qqe_line while rsiMa>50; short on the mirror below 50.

WHY THIS ONE. Across all 13 coins, full history, realistic Hyperliquid fees, with the
deployed exit (ATR sl 2.0x / tp 3.0x / 48h time stop, trailing, no opposite-exit):
profit factor 1.071, +$1728 total, 10/13 coins net positive. Scoped to the PF>=1.05
coins SOL/LINK/SUI/ZEC/ONDO/HYPE via cfg['strategy_universe']['QQE'].

This deployed exit was tuned to be TRADE-reproducible: the research catalog used an
exit-on-opposite-signal variant (PF 1.067) the shared core does not implement; the
tp 3.0x / no-opposite config above scores PF 1.071 with no core change.

CAVEAT: in-sample, full-history backtest, no walk-forward -- same status as B1 and ICHI.
Paper/testnet forward-test, NOT a proven live edge.

The QQE computation is self-contained here (clean-room copy of sister-lab/backtest
indicators.qqe, validated 0-mismatch against the backtest) so the plug depends only on
trade.strategy.indicators.atr and trade.models.Candle.
"""

from typing import Any

import numpy as np

from trade.models import Candle
from trade.numbers import to_float
from trade.strategy.indicators import atr

MIN_CANDLES = 120          # RSI(14) warm + EMA(27) double-smoothing settle + headroom


# QQE math + cross logic now live in the monorepo-wide single source of truth.
from shared.indicators import qqe_values as _qqe_values  # noqa: E402
from shared.strategies import qqe as _qqe_sig  # noqa: E402


def build_qqe_signal(coin: str, candles: list[Candle], candles_4h: list[Candle] | None,
                     ctx: dict[str, Any], allow_shorts: bool,
                     cfg: dict[str, Any] | None = None,
                     sr_cache: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """QQE smoothed-RSI / trailing-line cross on the 4h timeframe.

    Reads candles_4h (entry timeframe). Ignores the 1h `candles` and sr_cache.
    """
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES:
        return None
    closes = np.array([c.c for c in c4], dtype=float)
    rsi_ma, line = _qqe_values(closes)
    side = _qqe_sig({"qqe_rsima": rsi_ma, "qqe_line": line}, len(closes) - 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None:
        return None

    a = atr(c4, int(to_float(cfg.get("atr_period"), 14)))     # 4h ATR (entry timeframe)
    if a is None:
        return None

    r, l = rsi_ma[-1], line[-1]                               # for the round-robin score below

    funding = to_float(ctx.get("funding"), 0.0)
    score = round(abs(r - l), 4)                              # cross magnitude (round-robin only)

    return {
        "coin": coin, "side": side, "reason": "qqe_cross",
        "score": score, "close": c4[-1].c, "atr": a, "size_mult": 1.0,
        "funding": funding,
        "sr_blocking_price": 0.0, "sr_blocking_touches": 0,
        # --- exit params (deployed config: PF 1.071, no opposite-exit needed) ---
        "strategy": "QQE",
        "sl_mult": to_float(cfg.get("qqe_atr_sl_mult"), 2.0),
        "tp_mult": to_float(cfg.get("qqe_atr_tp_mult"), 3.0),
        "min_rr": to_float(cfg.get("qqe_min_rr"), 0.0),
        "use_sr_cap": False,
        "max_holding_hours": to_float(cfg.get("qqe_max_holding_hours"), 48),
    }
