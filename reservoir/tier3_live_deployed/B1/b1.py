from __future__ import annotations

from typing import Any

from trade.models import Candle
from trade.numbers import to_float
from trade.strategy.indicators import atr, macd
from shared.strategies import b1 as _b1


def build_b1_signal(coin: str, candles: list[Candle], candles_4h: list[Candle] | None, ctx: dict[str, Any], allow_shorts: bool, cfg: dict[str, Any] | None = None, sr_cache: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """B1 -- MACD Weak-Rally SELL (short only).

    Adapted from BINOPT/01_MACD_WEAK_RALLY_SELL to 1h crypto futures and validated in
    /home/user/sister-lab/LAB/backtest (full-history backtest, realistic Hyperliquid fees). Fades a
    weak rally: price has drifted UP over the last few bars while MACD momentum is still
    bearish and the histogram is rolling over -- i.e. the rally is not confirmed.

    Short-only by design; never returns a long. Ignores `candles_4h` / `sr_cache`
    (no higher-TF or S/R dependency). Exit params ride on the signal so the shared
    calc_open_order / execute_open stay strategy-agnostic: ATR stop 1.5x, ATR target
    2.0x, NO S/R cap, no min-R:R gate; the core adds Chandelier trailing (after +1R)
    and the time stop. These are the exact exit settings the backtest used.

    NOTE: selected for the coins it won on in-sample (DOGE/ZEC/ONDO/WLD/HYPE) -- this is a
    forward-test on paper/testnet, not a proven edge. Do not promote to live until the
    paper/testnet forward-test confirms it holds.
    """
    cfg = cfg or {}
    if not allow_shorts:
        return None
    if len(candles) < 90:                       # MACD(26,9) warm + close[-4]; matches MR1 history gate
        return None

    closes = [c.c for c in candles]
    atr_period = int(to_float(cfg.get("atr_period"), 14))
    a = atr(candles, atr_period)
    m = macd(closes)
    if a is None or m is None:
        return None
    line, _sig, hist = m

    # Single source: shared.strategies.b1 decides the short (reads close/macd/macd_hist arrays).
    side = _b1({"close": closes, "macd": line, "macd_hist": hist}, len(closes) - 1)
    if side is None:
        return None

    close = closes[-1]
    close_3 = closes[-4]
    macd_line = line[-1]
    macd_hist = hist[-1]

    funding = to_float(ctx.get("funding"), 0.0)
    # Score is only used for round-robin ordering; B1 runs alone so any magnitude works.
    score = round((close / close_3 - 1.0) * 100.0 + (-macd_hist) * 100.0, 4)

    return {
        "coin": coin, "side": "short", "reason": "macd_weak_rally_sell",
        "score": score, "close": close, "atr": a, "size_mult": 1.0,
        "macd_line": macd_line, "macd_hist": macd_hist, "funding": funding,
        "sr_blocking_price": 0.0, "sr_blocking_touches": 0,
        # --- exit params (backtest-matched) ---
        "strategy": "B1",
        "sl_mult": to_float(cfg.get("b1_atr_sl_mult"), 1.5),
        "tp_mult": to_float(cfg.get("b1_atr_tp_mult"), 2.0),
        "min_rr": to_float(cfg.get("b1_min_rr"), 0.0),
        "use_sr_cap": False,
        "max_holding_hours": to_float(cfg.get("b1_max_holding_hours"), 24),
    }
