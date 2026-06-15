from __future__ import annotations

"""B10 -- BINOPT-10 strong-signal Ichimoku (1h). An Ichimoku Tenkan/Kijun cross taken in the
cloud's direction AND confirmed by MACD: long above the cloud on Tenkan-over-Kijun with
macd>signal; short on the mirror below the cloud with macd<signal. Signal timeframe is 1h (the
"day" cadence the gauntlet scored it at) -- reads the 1h `candles`, NOT candles_4h.

FORWARD-TEST CANDIDATE, override-added 2026-06-04 (the operator's call). It cleared the official deploy gate
on ONDO and was single-holdout walk-forward ROBUST, but it is rolling-WFO OVERFIT and FRAGILE under
execution stress, so the gated deploy refuses it. Added to paper+testnet only to accumulate live
evidence; NOT a proven edge, NOT on live/mainnet. Scoped to ONDO via cfg['strategy_universe']['B10'].

EXIT: ATR sl 2.0x / tp 4.0x / 48h, no S/R cap, no opposite-exit -- this MATCHES the backtest exit
(b10's backtest exit was already exit_opposite=False), unlike CMO/CHAND which diverge.

Reuses ichimoku_tk._ichimoku_values (the point form proven identical to the LAB displaced-array
form at the last bar) on the 1h candles + trade.strategy.indicators.macd. Signal logic is the
monorepo single source shared.strategies.b10, validated 0-diff vs the LAB backtest on ONDO.
"""

from typing import Any

from trade.models import Candle
from trade.numbers import to_float
from trade.strategy.indicators import atr, macd
from trade.strategy.ichimoku_tk import _ichimoku_values, MIN_CANDLES
from shared.strategies import b10 as _b10


def build_b10_signal(coin: str, candles: list[Candle], candles_4h: list[Candle] | None,
                     ctx: dict[str, Any], allow_shorts: bool,
                     cfg: dict[str, Any] | None = None,
                     sr_cache: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Ichimoku TK cross in the cloud direction + MACD confirmation, on the 1h timeframe.

    Reads the 1h `candles` (day-cadence entry tf). Ignores candles_4h and sr_cache.
    """
    cfg = cfg or {}
    cd = candles
    if not cd or len(cd) < MIN_CANDLES:
        return None
    iv = _ichimoku_values(cd)
    if iv is None:
        return None
    ten, ten_prev, kij, kij_prev, span_a, span_b = iv

    closes = [c.c for c in cd]
    m = macd(closes)
    a = atr(cd, int(to_float(cfg.get("atr_period"), 14)))     # 1h ATR (entry timeframe)
    if m is None or a is None:
        return None
    line, sig, _hist = m
    close = cd[-1].c

    # Single source: shared.strategies.b10. The point form feeds 2-element arrays evaluated at
    # pos=1 (pos-1=0 is the prior bar). b10 reads ten/kij at pos and pos-1, the spans + macd/signal
    # at pos -- mirrors build_ichimoku_tk_signal, with the MACD confirmation added.
    side = _b10({"close": [close, close],
                 "ich_ten": [ten_prev, ten], "ich_kij": [kij_prev, kij],
                 "ich_a": [span_a, span_a], "ich_b": [span_b, span_b],
                 "macd": [line[-1], line[-1]], "macd_sig": [sig[-1], sig[-1]]}, 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None:
        return None

    funding = to_float(ctx.get("funding"), 0.0)
    cloud_top, cloud_bot = max(span_a, span_b), min(span_a, span_b)
    edge = cloud_top if side == "long" else cloud_bot
    score = round(abs(ten - kij) / close * 100.0 + abs(close - edge) / close * 100.0, 4)

    return {
        "coin": coin, "side": side, "reason": "b10_ichimoku_macd",
        "score": score, "close": close, "atr": a, "size_mult": 1.0,
        "funding": funding,
        "sr_blocking_price": 0.0, "sr_blocking_touches": 0,
        # --- exit params (matches the backtest exit; no opposite-exit) ---
        "strategy": "B10",
        "sl_mult": to_float(cfg.get("b10_atr_sl_mult"), 2.0),
        "tp_mult": to_float(cfg.get("b10_atr_tp_mult"), 4.0),
        "min_rr": to_float(cfg.get("b10_min_rr"), 0.0),
        "use_sr_cap": False,
        "max_holding_hours": to_float(cfg.get("b10_max_holding_hours"), 48),
    }
