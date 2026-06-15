#!/usr/bin/env python3
"""
Cross-engine independent confirmation for the FX gauntlet -- the robustness floor.

Ported from sister-lab/LAB/backtest/tools/cross_engines.py. An edge that only OUR engine sees may be an
artifact of OUR engine; an edge that two INDEPENDENT general-purpose backtest libraries also see
(vectorbt + backtesting.py) is far likelier real. This module re-prices a strategy's OWN entry
signals on those two engines and reports each pooled profit factor, so build_registry can require
INDEPENDENT CONFIRMATION (both vbt + backtesting.py PF>1) as part of the gate (the 2026-06 sister-lab
audit rule: our engine is the candidate, not a third vote).

SCOPE / HONESTY: the two external engines are BAREBONES -- entry signal + a fixed ATR sl/tp, no
trailing / time-stop / opposite-exit, and only a crude flat fee+slippage (Ostium-ish 3 bps + 1.5
bps; NOT Ostium's per-pair spread / rollover / oracle / gap-through-stop). So they confirm the
SIGNAL edge is not an artifact of our engine -- they do NOT re-check Ostium cost realism (that is
owned by our engine + costs.py + gate/stress). Compare PF (robustness), never net$ (different
cash/sizing). They are FX-portable because they read only OHLC (no volume).

TRIM: the external engines MUST run on the SAME per-pair window the engine uses (no simulation
before instruments.backtest_start_year). HistData's sparse/garbage 2000-2003 bars produced an
impossible negative take-profit in backtesting.py until the trim was applied -- see cross_pnls.

Pure-ish: no file I/O. Imports engine (for prepare/_year_ms) + shared.instruments (for the trim).
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

import vectorbt as vbt
from backtesting import Backtest, Strategy

import engine
from shared import instruments as _instr

# Crude external-engine costs: Ostium-ish round-trip (open 3 bps) + slippage floor 1.5 bps. Kept
# deliberately simple -- these engines confirm the signal, the cost realism lives in our engine.
EXT_FEE = 0.0003       # per-side fraction (vbt fees / btpy commission)
EXT_SLIP = 0.00015     # vbt slippage fraction

# pandas freq per cadence entry timeframe (vbt annualization only; PF is freq-independent here).
_FREQ = {"1m": "1min", "5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h", "1d": "1d"}

# backtesting.py reads these module globals (its Strategy API has no clean per-run injection).
# Set immediately before each Backtest(...).run() in _btpy_pnls; safe because a worker runs
# strategies sequentially (one process, no concurrent Backtest in this module).
_LE = _SE = _ATR = None
_SLM = _TPM = 0.0


class _Gen(Strategy):
    """Generic engine: take the precomputed long/short signal, exit on a fixed ATR sl/tp.
    Guards tp/sl > 0 before placing (an out-of-range stop crashes backtesting.py mid-run, not at
    the buy() call, so the try/except around buy() cannot catch it -- the guard must be here)."""
    def init(self):
        self.le = self.I(lambda: _LE.astype(float), name="le", plot=False)
        self.se = self.I(lambda: _SE.astype(float), name="se", plot=False)
        self.atr = self.I(lambda: _ATR, name="atr", plot=False)

    def next(self):
        if self.position:
            return
        a = self.atr[-1]
        if a is None or np.isnan(a) or a <= 0:
            return
        p = self.data.Close[-1]
        if self.le[-1] > 0.5:
            sl, tp = p - _SLM * a, p + _TPM * a
            if sl > 0 and tp > 0:
                try:
                    self.buy(size=0.2, sl=sl, tp=tp)
                except Exception:
                    pass
        elif self.se[-1] > 0.5:
            sl, tp = p + _SLM * a, p - _TPM * a
            if sl > 0 and tp > 0:               # short tp can go negative on cheap pairs / bad bars
                try:
                    self.sell(size=0.2, sl=sl, tp=tp)
                except Exception:
                    pass


def _signals(fn, I, htf, n, start):
    """Boolean long/short entry arrays from a strategy's own signal fn, from `start` to n."""
    le = np.zeros(n, bool)
    se = np.zeros(n, bool)
    for i in range(start, n):
        s = fn(I, i, htf)
        if s == "long":
            le[i] = True
        elif s == "short":
            se[i] = True
    return le, se


def _vbt_pnls(close_s, ent_s, sl_s, tp_s, direction, freq):
    """Trade PnLs from vectorbt for one direction; empty array if no trades."""
    pf = vbt.Portfolio.from_signals(
        close=close_s, entries=ent_s, sl_stop=sl_s, tp_stop=tp_s, direction=direction,
        fees=EXT_FEE, slippage=EXT_SLIP, init_cash=100000, size=0.2, size_type="percent",
        accumulate=False, freq=freq)
    rec = pf.trades.records_readable
    col = [c for c in rec.columns if c == "PnL" or "PnL" in c]
    return rec[col[0]].to_numpy() if len(rec) and col else np.array([])


def _btpy_pnls(data, le, se, atr, slm, tpm):
    """Trade PnLs from backtesting.py; empty array on failure or no trades."""
    global _LE, _SE, _ATR, _SLM, _TPM
    _LE, _SE, _ATR, _SLM, _TPM = le, se, atr, slm, tpm
    try:
        st = Backtest(data, _Gen, cash=100000, commission=EXT_FEE,
                      trade_on_close=True, finalize_trades=True).run()
        tr = st._trades
        return tr["PnL"].to_numpy() if len(tr) else np.array([])
    except Exception:
        return np.array([])


def cross_pnls(fn, ex, ctx, cadence, coin):
    """{'vbt': pnl_array, 'btpy': pnl_array} for one (strategy, pair) on its trimmed window.
    `coin` is the pair code (ctx from engine.prepare does NOT carry it). The arrays are POOLED
    across pairs by the caller, then turned into a PF per engine."""
    I, htf, n = ctx["I"], ctx["htf"], ctx["n"]
    # Per-pair backtest-start trim (same window the engine simulates -- no sparse 2000-2003 data).
    ot = I["open_time"]
    bt_year = _instr.backtest_start_year(coin) if coin else None
    eff = max(205, int(np.searchsorted(ot, engine._year_ms(bt_year), side="left"))) if bt_year else 205
    if eff >= n - 10:
        return {"vbt": np.array([]), "btpy": np.array([])}

    close = I["close"]; atr = I["atr"]
    le, se = _signals(fn, I, htf, n, eff)
    # Slice everything to the trimmed window so the external engines never see pre-trim bars.
    sl_idx = slice(eff, n)
    idx = pd.to_datetime(ot[sl_idx], unit="ms")
    close_t = close[sl_idx]; atr_t = atr[sl_idx]; le_t = le[sl_idx]; se_t = se[sl_idx]
    with np.errstate(divide="ignore", invalid="ignore"):
        base = np.where(close_t > 0, atr_t / close_t, np.nan)   # ATR-as-fraction; * mult = sl/tp frac
    slm = float(ex.get("sl_atr", 2.0)); tpm = float(ex.get("tp_atr", 4.0))
    freq = _FREQ.get(engine.CADENCES[cadence][0], "4h")

    close_s = pd.Series(close_t, index=idx)
    sl_s = pd.Series(base * slm, index=idx); tp_s = pd.Series(base * tpm, index=idx)
    vbt_pn = np.array([])
    try:
        lep = _vbt_pnls(close_s, pd.Series(le_t, index=idx), sl_s, tp_s, "longonly", freq)
        sep = _vbt_pnls(close_s, pd.Series(se_t, index=idx), sl_s, tp_s, "shortonly", freq)
        vbt_pn = np.concatenate([lep, sep])
    except Exception:
        pass

    data = pd.DataFrame({"Open": I["open"][sl_idx], "High": I["high"][sl_idx],
                         "Low": I["low"][sl_idx], "Close": close_t, "Volume": I["volume"][sl_idx]},
                        index=idx)
    btpy_pn = _btpy_pnls(data, le_t, se_t, atr_t, slm, tpm)
    return {"vbt": vbt_pn, "btpy": btpy_pn}


def pf_of(pnls):
    """Pooled profit factor over a flat PnL array; None when there are no losers (no denominator)."""
    a = np.asarray(pnls, dtype=float)
    if not len(a):
        return None
    losses = -a[a < 0].sum()
    if losses <= 0:
        return None
    return round(float(a[a > 0].sum() / losses), 3)
