/* FOREX Results page: render every backtest in the gauntlet (strategy_registry.json) as a
   sortable, filterable table. Data from /api/registry (summary, one row per strategy+cadence);
   per-pair detail lazy-loaded from /api/registry/pairs on row expand. Vanilla JS, no framework.
   Built to stay responsive at hundreds-to-thousands of rows. Ported from sister-lab's results.js. */
"use strict";

// --- formatters -----------------------------------------------------------
const f3 = v => (v == null ? "-" : Number(v).toFixed(3));
const pct1 = v => (v == null ? "-" : Number(v).toFixed(1) + "%");
const money = v => {
  if (v == null) return "-";
  const n = Number(v);
  const s = Math.abs(n) >= 1000 ? Math.round(n).toLocaleString() : n.toFixed(0);
  return (n >= 0 ? "+" : "-") + "$" + s.replace("-", "");
};

// Class for a profit factor cell. ~1.2 is a healthy gate floor; 1.0 is breakeven.
const pfClass = v => (v == null ? "dim" : v >= 1.2 ? "good" : v >= 1.0 ? "warn" : "bad");
const signClass = v => (v == null ? "dim" : v > 0 ? "pos" : v < 0 ? "neg" : "dim");
// Robustness verdict words (walk-forward / rolling / stress) normalize to good/bad/dim.
const GOOD_V = new Set(["robust", "survives", "survived", "pass", "passed"]);
const BAD_V = new Set(["overfit", "fragile", "failed", "dies", "fail", "drop"]);
const verdictClass = v => {
  const k = String(v || "").toLowerCase();
  if (GOOD_V.has(k)) return "good";
  if (BAD_V.has(k)) return "bad";
  return "dim";
};
// Promotion verdict (FOREX policy): ROBUST -> forward-test, CONSIDERATION -> pool, DROP.
const promoClass = v => {
  const k = String(v || "").toLowerCase();
  if (k === "robust") return "good";
  if (k === "consideration") return "warn";
  if (k === "drop") return "bad";
  return "dim";
};

// --- column spec ----------------------------------------------------------
// num=true => right-aligned + numeric sort; fmt formats the cell; cls colors it.
const COLS = [
  { key: "id", label: "Strategy", align: "l" },
  { key: "style", label: "Style", align: "l" },
  { key: "cadence", label: "Cad", align: "l" },
  { key: "tf", label: "TF", align: "l" },
  { key: "trades", label: "Trades", num: true },
  { key: "win_pct", label: "Win%", num: true, fmt: pct1 },
  { key: "pf", label: "PF", num: true, fmt: f3, cls: r => pfClass(r.pf) },
  { key: "net_usd", label: "Net$", num: true, fmt: money, cls: r => signClass(r.net_usd) },
  { key: "return_pct", label: "Ret%", num: true, fmt: pct1, cls: r => signClass(r.return_pct) },
  { key: "expectancy_R", label: "Exp R", num: true, fmt: f3, cls: r => signClass(r.expectancy_R) },
  { key: "agreement", label: "Eng", align: "c" },
  { key: "gate_n", label: "Gate", num: true, cls: r => (r.gate_n > 0 ? "good" : "dim"),
    fmt: v => (v > 0 ? v : "0") },
  { key: "wfo", label: "WFO", align: "c", cls: r => verdictClass(r.wfo) },
  { key: "rolling_wfo", label: "Roll", align: "c", cls: r => verdictClass(r.rolling_wfo) },
  { key: "stress", label: "Stress", align: "c", cls: r => verdictClass(r.stress) },
  { key: "verdict", label: "Verdict", align: "c", cls: r => promoClass(r.verdict),
    fmt: v => (v && v !== "-" ? v : "-") },
  { key: "forward", label: "Fwd", align: "c", cls: r => (r.forward ? "good" : "dim"),
    fmt: v => (v ? "✓" : "-") },
];

// --- state ----------------------------------------------------------------
let ROWS = [];                 // all rows from the API
let sortKey = "pf";            // default: best profit factor first
let sortDir = -1;              // -1 desc, 1 asc
let cadSel = "all";
let verSel = "all";            // promotion-verdict filter
const pairCache = {};          // `${id}|${cadence}` -> per-pair payload
const expanded = new Set();    // `${id}|${cadence}` rows currently open

const $ = id => document.getElementById(id);

// --- filtering + sorting --------------------------------------------------
function visibleRows() {
  const q = $("q").value.trim().toLowerCase();
  const gateOnly = $("gateOnly").checked;
  const fwdOnly = $("fwdOnly").checked;
  let rows = ROWS.filter(r => {
    if (cadSel !== "all" && r.cadence !== cadSel) return false;
    if (verSel !== "all" && String(r.verdict).toUpperCase() !== verSel) return false;
    if (gateOnly && !(r.gate_n > 0)) return false;
    if (fwdOnly && !r.forward) return false;
    if (q) {
      const hay = (r.id + " " + r.style + " " + r.indicators + " " + r.desc).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
  const col = COLS.find(c => c.key === sortKey);
  rows.sort((a, b) => {
    let x = a[sortKey], y = b[sortKey];
    if (col && col.num) {
      x = x == null ? -Infinity : x; y = y == null ? -Infinity : y;   // nulls to the bottom
      return (x - y) * sortDir;
    }
    return String(x).localeCompare(String(y)) * sortDir;
  });
  return rows;
}

// --- render ---------------------------------------------------------------
function renderHead() {
  const tr = document.createElement("tr");
  COLS.forEach(c => {
    const th = document.createElement("th");
    th.textContent = c.label;
    th.className = (c.num ? "r" : c.align === "c" ? "c" : "l");
    if (c.key === sortKey) th.classList.add(sortDir < 0 ? "sort-d" : "sort-a");
    th.onclick = () => {
      if (sortKey === c.key) sortDir = -sortDir;
      else { sortKey = c.key; sortDir = c.num ? -1 : 1; }
      render();
    };
    tr.appendChild(th);
  });
  $("thead").replaceChildren(tr);
}

function cellText(c, r) {
  const raw = r[c.key];
  return c.fmt ? c.fmt(raw, r) : (raw == null ? "-" : raw);
}

function renderBody() {
  const rows = visibleRows();
  const frag = document.createDocumentFragment();
  rows.forEach(r => {
    const ekey = r.id + "|" + r.cadence;
    const tr = document.createElement("tr");
    tr.className = "row" + (r.forward ? " fwd" : "");
    if (expanded.has(ekey)) tr.classList.add("open");
    COLS.forEach(c => {
      const td = document.createElement("td");
      td.className = (c.num ? "r" : c.align === "c" ? "c" : "l");
      if (c.cls) td.classList.add(c.cls(r));
      td.textContent = cellText(c, r);
      tr.appendChild(td);
    });
    tr.onclick = () => toggleRow(ekey, r);
    frag.appendChild(tr);
    if (expanded.has(ekey)) frag.appendChild(detailRow(r, ekey));
  });
  const tb = $("tbody");
  tb.replaceChildren(frag);
  if (!rows.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = COLS.length;
    td.className = "empty pdim";
    td.textContent = ROWS.length ? "No rows match the filters."
                                 : "No backtests yet — run the gauntlet to populate this page.";
    tr.appendChild(td);
    tb.appendChild(tr);
  }
  $("count").textContent = rows.length + " / " + ROWS.length + " rows";
}

function render() { renderHead(); renderBody(); }

// --- row detail (rules + lazy per-pair) -----------------------------------
function detailRow(r, ekey) {
  const tr = document.createElement("tr");
  tr.className = "detail";
  const td = document.createElement("td");
  td.colSpan = COLS.length;

  const rules = document.createElement("div");
  rules.className = "rules";
  const src = r.source
    ? ` &middot; <a href="${r.source}" target="_blank" rel="noopener">source</a>`
    : "";
  rules.innerHTML =
    `<div><b>${r.id}</b> &mdash; ${r.desc || ""}${src}</div>` +
    `<div class="pdim">indicators: ${r.indicators || "-"}</div>` +
    `<div><span class="pos">long:</span> ${r.long || "-"}</div>` +
    `<div><span class="neg">short:</span> ${r.short || "-"}</div>` +
    (r.gate_pairs && r.gate_pairs.length
      ? `<div class="pdim">gate-passing pairs: ${r.gate_pairs.join(", ")}</div>` : "");
  td.appendChild(rules);

  const box = document.createElement("div");
  box.className = "coinsbox";
  box.textContent = "loading per-pair...";
  td.appendChild(box);
  loadPairs(r, ekey, box);

  tr.appendChild(td);
  return tr;
}

async function loadPairs(r, ekey, box) {
  let data = pairCache[ekey];
  if (!data) {
    try {
      const res = await fetch(`api/registry/pairs?id=${encodeURIComponent(r.id)}&cadence=${encodeURIComponent(r.cadence)}`);
      data = await res.json();
      pairCache[ekey] = data;
    } catch (e) {
      box.textContent = "per-pair unavailable";
      return;
    }
  }
  const list = (data && data.pairs) || [];
  if (!list.length) { box.textContent = "no per-pair data"; return; }
  const head = "<tr><th class='l'>Pair</th><th class='r'>Trades</th><th class='r'>Win%</th>" +
    "<th class='r'>PF</th><th class='r'>Net$</th><th class='r'>MaxDD%</th>" +
    "<th class='r'>Exp R</th><th class='c'>Gate</th></tr>";
  const body = list.map(c =>
    `<tr><td class='l'>${c.pair}</td><td class='r'>${c.trades}</td>` +
    `<td class='r'>${pct1(c.win_pct)}</td>` +
    `<td class='r ${pfClass(c.pf)}'>${f3(c.pf)}</td>` +
    `<td class='r ${signClass(c.net_usd)}'>${money(c.net_usd)}</td>` +
    `<td class='r'>${pct1(c.max_dd_pct)}</td>` +
    `<td class='r ${signClass(c.expectancy_R)}'>${f3(c.expectancy_R)}</td>` +
    `<td class='c ${c.gate_pass ? "good" : "dim"}'>${c.gate_pass ? "pass" : "-"}</td></tr>`
  ).join("");
  box.innerHTML = `<table class="coins-tbl"><thead>${head}</thead><tbody>${body}</tbody></table>`;
}

function toggleRow(ekey, r) {
  if (expanded.has(ekey)) expanded.delete(ekey);
  else expanded.add(ekey);
  renderBody();
}

// --- filters / boot -------------------------------------------------------
function buildChipFilter(boxId, values, selected, onpick) {
  const box = $(boxId);
  box.replaceChildren();
  values.forEach(v => {
    const b = document.createElement("button");
    b.textContent = v;
    if (v === selected()) b.classList.add("on");
    b.onclick = () => { onpick(v); renderBody(); };
    box.appendChild(b);
  });
}

function buildFilters() {
  const cads = ["all", ...Array.from(new Set(ROWS.map(r => r.cadence)))];
  buildChipFilter("cadFilter", cads, () => cadSel, v => { cadSel = v; buildFilters(); });
  const vers = ["all", "ROBUST", "CONSIDERATION", "DROP"];
  buildChipFilter("verFilter", vers, () => verSel, v => { verSel = v; buildFilters(); });
}

async function boot() {
  let data;
  try {
    data = await fetch("api/registry").then(r => r.json());
  } catch (e) {
    $("meta").textContent = "registry unavailable";
  }
  ROWS = (data && data.rows) || [];
  const m = (data && data.meta) || {};
  if (data) {
    const gen = m.generated
      ? new Date(m.generated).toISOString().slice(0, 16).replace("T", " ") + "Z" : "?";
    $("meta").textContent = `${m.n_strategies || 0} strategies, ${m.n_rows || 0} rows | generated ${gen}`;
    if (m.official_gate) $("meta").title = "gate: " + m.official_gate;
  } else {
    $("meta").textContent = "no registry yet";
  }
  buildFilters();
  ["q", "gateOnly", "fwdOnly"].forEach(id => {
    const el = $(id);
    el.addEventListener(id === "q" ? "input" : "change", renderBody);
  });
  render();
}

boot();
