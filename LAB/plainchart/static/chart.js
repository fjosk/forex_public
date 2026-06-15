// FOREX offline chart. Renders the unified per-instrument series (HistData FX + Dukascopy
// commodities) from /api/candles: candlestick + volume + EMA20/50 (lightweight-charts v4,
// bundled locally in static/vendor). NOTE: FX/commodity volume is always 0 in this dataset,
// so the volume histogram sits flat -- it is kept only for layout parity, not a real signal.

// The three PURPOSE views (mirrors sister-lab). Each maps to a data source: Backtest runs on our
// local parquet; Paper + Live both run on the Ostium live feed (same chart -- testnet/mainnet
// only differ in contracts, not price). [id, label, source, accent-class].
var VIEWS = [
  ['backtest', 'Backtest',    'local'],
  ['paper',    'Paper Trade', 'ostium'],
  ['live',     'Live Trade',  'ostium'],
];

var S = {
  meta: null, coin: 'EURUSD', iv: '1h',
  view: 'backtest', source: 'local',   // view drives source; backtest=local parquet, paper/live=ostium
  ostiumPairs: [],            // instrument codes Ostium lists -> the rest are hidden in paper/live
  candles: [], earliest: null, loading: false,
  chart: null, cs: null, vs: null, e20: null, e50: null,
};

// Only instruments Ostium actually lists are selectable -- in EVERY view, Backtest included.
// We only ever trade on Ostium, so backtesting a pair it doesn't carry (EUR/JPY, USD/ZAR) is
// pointless; the parquet still holds all 16, we just never surface the two off-venue ones.
// (Fallback: if the Ostium pair list failed to load, show everything rather than hide all.)
function coinAvailable(c) {
  return !S.ostiumPairs.length || S.ostiumPairs.indexOf(c) >= 0;
}
function firstAvailableCoin() {
  for (var i = 0; i < S.meta.coins.length; i++) {
    if (coinAvailable(S.meta.coins[i])) return S.meta.coins[i];
  }
  return S.meta.coins[0];
}

// Endpoint for the current source. Ostium candles come from /api/ostium_candles (proxied to the
// Ostium Builder API server-side); local candles from /api/candles (our parquet).
function candleEndpoint() {
  return S.source === 'ostium' ? 'api/ostium_candles' : 'api/candles';
}

function fmtDate(sec) {
  return new Date(sec * 1000).toISOString().slice(0, 16).replace('T', ' ');
}

function ema(candles, period) {
  var k = 2 / (period + 1), out = [], prev = null;
  for (var i = 0; i < candles.length; i++) {
    var c = candles[i].close;
    prev = prev === null ? c : c * k + prev * (1 - k);
    out.push({ time: candles[i].time, value: prev });
  }
  return out;
}

function buildChart() {
  var box = document.getElementById('chartbox');
  S.chart = LightweightCharts.createChart(box, {
    width: box.clientWidth, height: box.clientHeight,
    layout: { background: { color: '#0d1017' }, textColor: '#d1d4dc', attributionLogo: false },
    grid: { vertLines: { color: '#161c28' }, horzLines: { color: '#161c28' } },
    timeScale: { timeVisible: true, secondsVisible: false, borderColor: '#2a2e39' },
    rightPriceScale: { borderColor: '#2a2e39' },
    crosshair: { mode: 0 },
  });
  S.cs = S.chart.addCandlestickSeries({
    upColor: '#26a69a', downColor: '#ef5350', borderUpColor: '#26a69a',
    borderDownColor: '#ef5350', wickUpColor: '#26a69a', wickDownColor: '#ef5350',
    priceLineVisible: false, lastValueVisible: false,
  });
  S.vs = S.chart.addHistogramSeries({ priceScaleId: 'vol', priceLineVisible: false, lastValueVisible: false });
  S.chart.priceScale('vol').applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });
  S.e20 = S.chart.addLineSeries({ color: '#ffc107', lineWidth: 1, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });
  S.e50 = S.chart.addLineSeries({ color: '#ff9800', lineWidth: 1, priceLineVisible: false, lastValueVisible: false, crosshairMarkerVisible: false });

  S.chart.timeScale().subscribeVisibleLogicalRangeChange(function (r) {
    if (r && r.from < 8) loadOlder();
  });
  S.chart.subscribeCrosshairMove(function (p) {
    if (!p || !p.time || !p.seriesData) { return updateLegend(null); }
    updateLegend(p.seriesData.get(S.cs));
  });
  // Keep the chart matched to its container at all times. Covers the initial
  // sizing race (chart built before the coin row wraps and shrinks main) plus
  // any window resize -- no page scroll, no stale canvas height.
  new ResizeObserver(function () {
    S.chart.resize(box.clientWidth, box.clientHeight);
  }).observe(box);
}

function updateLegend(bar) {
  var el = document.getElementById('legend');
  var head = '<b>' + S.coin.replace('USDT', '') + '</b> &middot; ' + S.iv;
  if (!bar) {
    var n = S.candles.length;
    el.innerHTML = head + (n ? ' &middot; ' + n + ' bars loaded' : '');
    return;
  }
  var cls = bar.close >= bar.open ? 'up' : 'down';
  el.innerHTML = head + '  <span class="' + cls + '">O ' + bar.open + '  H ' + bar.high +
    '  L ' + bar.low + '  C ' + bar.close + '</span>';
}

function redraw() {
  S.cs.setData(S.candles);
  S.vs.setData(S.candles.map(function (c) {
    return { time: c.time, value: c.volume, color: c.close >= c.open ? 'rgba(38,166,154,.35)' : 'rgba(239,83,80,.35)' };
  }));
  S.e20.setData(ema(S.candles, 20));
  S.e50.setData(ema(S.candles, 50));
  updateLegend(null);
}

function load() {
  S.loading = true;
  var u = candleEndpoint() + '?coin=' + S.coin + '&interval=' + S.iv + '&limit=3000';
  fetch(u).then(function (r) { return r.json(); }).then(function (d) {
    S.candles = d.candles || [];
    S.earliest = d.earliest;
    redraw();
    S.chart.timeScale().fitContent();
    if (S.source === 'ostium' && !S.candles.length) {
      document.getElementById('legend').innerHTML = '<b>' + S.coin + '</b> &middot; no Ostium feed for this instrument';
    }
    S.loading = false;
  }).catch(function () { S.loading = false; });
}

function loadOlder() {
  if (S.loading || !S.candles.length) return;
  var oldest = S.candles[0].time;
  if (S.earliest != null && oldest <= S.earliest) return;  // nothing older
  S.loading = true;
  var u = candleEndpoint() + '?coin=' + S.coin + '&interval=' + S.iv + '&limit=3000&end=' + (oldest - 1);
  fetch(u).then(function (r) { return r.json(); }).then(function (d) {
    var older = (d.candles || []).filter(function (c) { return c.time < oldest; });
    if (older.length) {
      S.candles = older.concat(S.candles);
      S.earliest = d.earliest;
      redraw();
    }
    S.loading = false;
  }).catch(function () { S.loading = false; });
}

function jumpNow() { S.chart.timeScale().scrollToRealTime(); }

function buildCoins() {
  var box = document.getElementById('coins');
  box.innerHTML = '';
  S.meta.coins.forEach(function (c) {
    if (!coinAvailable(c)) return;   // hidden: Ostium doesn't list this pair in the Paper/Live views
    var b = document.createElement('button');
    b.textContent = c.replace('USDT', '');
    b.className = (c === S.coin ? 'on' : '');
    b.onclick = function () { S.coin = c; buildCoins(); ensureInterval(); load(); };
    box.appendChild(b);
  });
}

function buildIvs() {
  var box = document.getElementById('ivs');
  box.innerHTML = '';
  S.meta.intervals.forEach(function (iv) {
    var b = document.createElement('button');
    b.textContent = iv;
    b.className = (iv === S.iv ? 'on' : '');
    b.onclick = function () { S.iv = iv; buildIvs(); load(); };
    box.appendChild(b);
  });
}

function ensureInterval() {
  var ivs = (S.meta.info[S.coin] || {}).intervals || S.meta.intervals;
  if (ivs.indexOf(S.iv) < 0) S.iv = ivs[ivs.length - 1];
  buildIvs();
}

// The navbar is static HTML (identical on every page so it never collapses). Here we just mark the
// active view and intercept the three chart-view links so switching is instant (no reload) while
// staying deep-linkable via ?view= and shareable from the Results page. The active view recolors
// the whole page via --accent (green=backtest, amber=paper, red=live).
function go(view) {
  setView(view);
  history.pushState(null, '', '/?view=' + view);
}
function wireNav() {
  document.querySelectorAll('.navbar .views a[data-view]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); go(a.dataset.view); });
  });
}
function updateNavActive() {
  document.querySelectorAll('.navbar .views a[data-view]').forEach(function (a) {
    a.classList.toggle('active', a.dataset.view === S.view);
  });
}

// Switch view = switch data source + accent. If the current instrument isn't carried by the new
// view's source (e.g. EUR/JPY on Ostium), fall back to the first one that is.
function setView(view) {
  var def = VIEWS.filter(function (v) { return v[0] === view; })[0] || VIEWS[0];
  S.view = def[0];
  S.source = def[2];
  document.body.classList.remove('view-backtest', 'view-paper', 'view-live');
  document.body.classList.add('view-' + S.view);
  if (!coinAvailable(S.coin)) S.coin = firstAvailableCoin();
  updateNavActive();
  buildCoins();
  ensureInterval();
  renderPanel();
  load();
}

// Right panel content per view. Placeholders for now -- the section shells (ids) are stable so the
// Ostium trader can drop real data in later: Backtest -> results/trades; Paper/Live -> account +
// open/closed positions.
function renderPanel() {
  var el = document.getElementById('panel');
  if (!el) return;
  if (S.view === 'backtest') {
    el.innerHTML =
      '<div class="psec"><h3>Backtest Results</h3>' +
      '<div class="body pdim" id="results">No backtest run yet.</div></div>' +
      '<div class="psec"><h3>Trades</h3>' +
      '<div class="body pdim" id="bt-trades">Run a strategy to list trades here.</div></div>';
  } else {
    var label = S.view === 'live' ? 'Live &middot; Ostium mainnet (REAL funds)'
                                  : 'Paper &middot; Ostium testnet (simulated)';
    el.innerHTML =
      '<div class="acct"><div class="pdim">' + label + '</div>' +
      '<div class="big" id="equity">--</div>' +
      '<div class="pdim" id="pnl">PnL --</div></div>' +
      '<div class="psec"><h3>Open Positions</h3>' +
      '<div class="body pdim" id="openlist">No open positions.</div></div>' +
      '<div class="psec"><h3>Closed Trades</h3>' +
      '<div class="body pdim" id="closedlist">No closed trades.</div></div>';
  }
}

// Drag-resize the right panel from its left edge (mirrors sister-lab's trader sidebar). Width persists
// in localStorage so it survives reloads. The chart re-fits live as the panel narrows/widens.
(function () {
  var resizer = document.getElementById('resizer');
  var sidebar = document.getElementById('sidebar');
  if (!resizer || !sidebar) return;
  var MIN = 220, MAX = 640, startX, startW;
  var saved = parseInt(localStorage.getItem('fx_side_w'), 10);
  if (saved >= MIN && saved <= MAX) sidebar.style.width = saved + 'px';
  function refit() {
    var b = document.getElementById('chartbox');
    if (S.chart && b) S.chart.resize(b.clientWidth, b.clientHeight);
  }
  resizer.addEventListener('mousedown', function (e) {
    startX = e.clientX; startW = sidebar.offsetWidth;
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
    e.preventDefault();
  });
  function onDrag(e) {
    var w = startW - (e.clientX - startX);
    if (w >= MIN && w <= MAX) { sidebar.style.width = w + 'px'; refit(); }
  }
  function stopDrag() {
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);
    localStorage.setItem('fx_side_w', sidebar.offsetWidth);
  }
})();

// Initial view from ?view= (so /results -> Backtest etc. deep-links land right); default backtest
// (safe, has data) when absent/invalid.
function viewFromUrl() {
  var v = new URLSearchParams(location.search).get('view');
  return VIEWS.some(function (x) { return x[0] === v; }) ? v : 'backtest';
}

function init() {
  wireNav();
  S.view = viewFromUrl();
  Promise.all([
    fetch('api/meta').then(function (r) { return r.json(); }),
    fetch('api/ostium_pairs').then(function (r) { return r.json(); }).catch(function () { return { pairs: [] }; }),
  ]).then(function (res) {
    S.meta = res[0];
    S.ostiumPairs = (res[1] && res[1].pairs) || [];
    if (S.meta.coins.indexOf(S.coin) < 0) S.coin = S.meta.coins[0];
    buildChart();
    setView(S.view);   // sets source + accent, marks nav, builds coins/ivs, loads candles
  });
}

// Back/forward buttons re-apply the ?view= state.
window.addEventListener('popstate', function () {
  var v = viewFromUrl();
  if (v !== S.view) setView(v);
});

init();
