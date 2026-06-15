/* PnL page: two glanceable cards, Paper + Live, from /api/pnl. One combined view (only two modes)
   so you compare both at once. Vanilla JS. Empty state until the Ostium trader has run. */
"use strict";

var MODES = [
  { key: "paper", label: "Paper", sub: "Ostium testnet (Sepolia, real orders)" },
  { key: "live",  label: "Live",  sub: "Ostium mainnet (real funds)" },
];

function money(v) {
  if (v == null) return "--";
  var n = Number(v);
  var s = Math.abs(n) >= 1000 ? Math.round(n).toLocaleString() : n.toFixed(2);
  return (n >= 0 ? "+" : "-") + "$" + s.replace("-", "");
}
function bal(v) { return v == null ? "--" : "$" + Number(v).toLocaleString(undefined, { maximumFractionDigits: 2 }); }
function pct1(v) { return v == null ? "--" : Number(v).toFixed(1) + "%"; }
function f2(v) { return v == null ? "--" : Number(v).toFixed(2); }
function fee(v) { return v == null ? "--" : "-$" + Number(Math.abs(v)).toFixed(2); }  // fees are a cost
function signClass(v) { return v == null ? "dim" : v > 0 ? "pos" : v < 0 ? "neg" : "dim"; }

function stat(k, v, cls) {
  return '<div class="stat"><div class="k">' + k + '</div><div class="v ' + (cls || "") + '">' + v + "</div></div>";
}

function cardHtml(def, d) {
  var head = '<div class="pnlhead">' + def.label + '<span class="badge">' + def.sub + "</span></div>";
  if (!d || !d.started) {
    var msg = d && d.error ? d.error
            : def.key === "live" ? "Mainnet not started yet."
            : "No testnet trades yet.";
    return '<div class="pnlcard mode-' + def.key + '">' + head +
           '<div class="pdim pnlempty">' + msg + "</div></div>";
  }
  // The four headline figures the operator wants: Equity (big, below) + Realized / Unrealized / Fees, then the ratios.
  var stats =
    stat("Realized", money(d.realized), signClass(d.realized)) +
    stat("Unreal", money(d.unrealized), signClass(d.unrealized)) +
    stat("Fees", fee(d.fees), "neg") +
    stat("Win", pct1(d.win_pct)) +
    stat("PF", f2(d.profit_factor)) +
    stat("Trades", d.trades != null ? d.trades : "--") +
    stat("Open", d.open != null ? d.open : "--");
  return '<div class="pnlcard mode-' + def.key + '">' + head +
    '<div class="pnlbig">' + bal(d.equity) + "</div>" +
    '<div class="pnlsub"><span class="' + signClass(d.net_usd) + '">' + money(d.net_usd) + "</span>" +
      ' &middot; <span class="' + signClass(d.return_pct) + '">' + pct1(d.return_pct) + "</span></div>" +
    '<div class="statrow">' + stats + "</div></div>";
}

function render(data) {
  var modes = (data && data.modes) || {};
  document.getElementById("pnlgrid").innerHTML =
    MODES.map(function (m) { return cardHtml(m, modes[m.key]); }).join("");
}

function boot() {
  fetch("api/pnl").then(function (r) { return r.json(); }).then(render).catch(function () {
    render({ modes: {} });
  });
}

boot();
