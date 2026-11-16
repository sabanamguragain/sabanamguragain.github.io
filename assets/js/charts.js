/* ============================================================
   Interactive charts (Chart.js v4). Renders lazily when each
   dashboard scrolls into view, so the page stays light.
   ============================================================ */

const C = {
  primary: '#0083FF',
  teal:    '#12B5A5',
  accent:  '#FFB020',
  alert:   '#FF5C7A',
  purple:  '#6A3CFF',
  ink:     '#51637a',
  grid:    'rgba(11,31,58,.08)',
};
const SECTOR_COLORS = ['#0083FF', '#6A3CFF', '#12B5A5', '#FFB020', '#FF5C7A', '#4AA8FF', '#9B7BFF', '#9db2c9'];

// Force crisp text on every display: render the canvas at >=2x device pixels.
Chart.defaults.devicePixelRatio = Math.max(window.devicePixelRatio || 1, 2);
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = C.ink;
Chart.defaults.plugins.legend.labels.boxWidth = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'rectRounded';
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.titleColor = '#fff';
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(18,38,60,.92)';
Chart.defaults.maintainAspectRatio = false;

const axis = (opts = {}) => ({
  grid: { color: C.grid, drawTicks: false },
  border: { display: false },
  ticks: { padding: 6, ...(opts.ticks || {}) },
  ...opts,
});

const pct = (v) => `${v}%`;
const base = (plugins = {}) => ({
  responsive: true,
  interaction: { mode: 'index', intersect: false },
  plugins: { legend: { display: false }, ...plugins },
});

/* --- registry: id -> factory. Built only when its section appears. --- */
const CHART_BUILDERS = {

  /* ===== Economic ===== */
  'c-gdp-growth': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.years, datasets: [{ label: 'Real GDP growth', data: ECON.realGdpGrowth, backgroundColor: C.primary, borderRadius: 5, maxBarThickness: 48 }] },
    options: { ...base(), scales: { y: axis({ beginAtZero: true, ticks: { callback: pct } }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` ${i.parsed.y}% growth` } } } },
  }),

  'c-nominal-gdp': (ctx) => new Chart(ctx, {
    type: 'line',
    data: { labels: ECON.years, datasets: [{ label: 'Nominal GDP', data: ECON.nominalGdp, borderColor: C.teal, backgroundColor: 'rgba(27,107,107,.12)', fill: true, tension: .35, pointRadius: 4, pointBackgroundColor: C.teal, borderWidth: 2.5 }] },
    options: { ...base(), scales: { y: axis({ ticks: { callback: (v) => `Rs ${v.toLocaleString()}B` } }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` Rs ${i.parsed.y.toLocaleString()} billion` } } } },
  }),

  'c-inflation': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.years, datasets: [
      { label: 'Overall CPI', data: ECON.cpiOverall, backgroundColor: C.primary, borderRadius: 4 },
      { label: 'Food', data: ECON.cpiFood, backgroundColor: C.accent, borderRadius: 4 },
      { label: 'Non-food', data: ECON.cpiNonFood, backgroundColor: C.alert, borderRadius: 4 },
    ] },
    options: { ...base({ legend: { display: true, position: 'top' } }), scales: { y: axis({ ticks: { callback: pct } }), x: axis() } },
  }),

  'c-trade': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.years, datasets: [
      { label: 'Exports', data: ECON.exports, backgroundColor: C.teal, borderRadius: 4 },
      { label: 'Imports', data: ECON.imports, backgroundColor: C.alert, borderRadius: 4 },
    ] },
    options: { ...base({ legend: { display: true, position: 'top' } }), scales: { y: axis({ ticks: { callback: (v) => `Rs ${v.toLocaleString()}B` } }), x: axis() } },
  }),

  'c-remittances': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.years, datasets: [{ label: 'Remittances', data: ECON.remittances, backgroundColor: C.purple, borderRadius: 5, maxBarThickness: 48 }] },
    options: { ...base(), scales: { y: axis({ ticks: { callback: (v) => `Rs ${v.toLocaleString()}B` } }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` Rs ${i.parsed.y.toLocaleString()} billion` } } } },
  }),

  'c-forex': (ctx) => new Chart(ctx, {
    type: 'line',
    data: { labels: ECON.years, datasets: [{ label: 'Forex reserves', data: ECON.forex, borderColor: C.primary, backgroundColor: 'rgba(46,90,172,.12)', fill: true, tension: .35, pointRadius: 4, pointBackgroundColor: C.primary, borderWidth: 2.5 }] },
    options: { ...base(), scales: { y: axis({ ticks: { callback: (v) => `$${(v/1000).toFixed(0)}B` } }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` $${i.parsed.y.toLocaleString()} million` } } } },
  }),

  'c-rates': (ctx) => new Chart(ctx, {
    type: 'line',
    data: { labels: ECON.years, datasets: [
      { label: '91-day T-Bill', data: ECON.tbill91, borderColor: C.teal, tension: .3, pointRadius: 3, borderWidth: 2.5 },
      { label: 'Avg lending rate', data: ECON.lendingRate, borderColor: C.alert, tension: .3, pointRadius: 3, borderWidth: 2.5 },
    ] },
    options: { ...base({ legend: { display: true, position: 'top' } }), scales: { y: axis({ ticks: { callback: pct } }), x: axis() } },
  }),

  'c-nepse': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.years, datasets: [{ label: 'NEPSE index', data: ECON.nepse, backgroundColor: C.purple, borderRadius: 5, maxBarThickness: 48 }] },
    options: { ...base(), scales: { y: axis(), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` ${i.parsed.y.toLocaleString()} points` } } } },
  }),

  'c-sector': (ctx) => new Chart(ctx, {
    type: 'doughnut',
    data: { labels: ECON.sectorLabels, datasets: [{ data: ECON.sectorShare, backgroundColor: SECTOR_COLORS, borderColor: '#fff', borderWidth: 2 }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: '58%',
      plugins: { legend: { display: true, position: 'right', labels: { boxWidth: 10, padding: 8, font: { size: 11 } } },
        tooltip: { callbacks: { label: (i) => ` ${i.label}: ${i.parsed}%` } } } },
  }),

  'c-percapita': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: ECON.perCapitaLabels, datasets: [
      { label: '2023/24', data: ECON.perCapita2024, backgroundColor: 'rgba(46,90,172,.55)', borderRadius: 4 },
      { label: '2024/25', data: ECON.perCapita2025, backgroundColor: C.teal, borderRadius: 4 },
    ] },
    options: { ...base({ legend: { display: true, position: 'top' } }), scales: { y: axis({ ticks: { callback: (v) => `${(v/1000).toFixed(0)}k` } }), x: axis() },
      plugins: { legend: { display: true, position: 'top' }, tooltip: { callbacks: { label: (i) => ` ${i.dataset.label}: NRs ${i.parsed.y.toLocaleString()}` } } } },
  }),

  /* ===== Education & disability ===== */
  'c-literacy': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: EDU.literacyLabels, datasets: [{ label: 'Literacy', data: EDU.literacy,
      backgroundColor: EDU.literacyLabels.map(l => l === 'Female' ? C.alert : C.primary), borderRadius: 5, maxBarThickness: 54 }] },
    options: { ...base(), scales: { y: axis({ beginAtZero: true, max: 100, ticks: { callback: pct } }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` ${i.parsed.y}% literate (age 5+)` } } } },
  }),

  'c-cwd': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: EDU.cwdLevels, datasets: [{ label: 'Recorded share', data: EDU.cwdShare,
      backgroundColor: EDU.cwdLevels.map(l => l === 'Primary' ? C.alert : C.primary), borderRadius: 5, maxBarThickness: 56 }] },
    options: { ...base(), scales: { y: axis({ beginAtZero: true, suggestedMax: 5.2, ticks: { callback: pct } }), x: axis() },
      plugins: { ...base().plugins,
        tooltip: { callbacks: { label: (i) => ` ${i.parsed.y}% of enrolment`, afterLabel: () => 'Estimated prevalence: 5–10%' } },
        annotationLine: true } },
    plugins: [{
      id: 'annotationLine',
      afterDraw(chart) {
        const { ctx, chartArea: { left, right }, scales: { y } } = chart;
        const yy = y.getPixelForValue(EDU.cwdExpectedLow);
        ctx.save();
        ctx.setLineDash([6, 5]); ctx.strokeStyle = C.accent; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(left, yy); ctx.lineTo(right, yy); ctx.stroke();
        ctx.setLineDash([]); ctx.fillStyle = C.accent; ctx.font = '600 11px Inter';
        ctx.fillText('Expected prevalence ≥ 5%', left + 8, yy - 6);
        ctx.restore();
      }
    }],
  }),

  'c-barriers': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: EDU.barrierLabels, datasets: [{ label: '% citing', data: EDU.barriers, backgroundColor: C.accent, borderRadius: 4 }] },
    options: { ...base(), indexAxis: 'y', scales: { x: axis({ beginAtZero: true, max: 100, ticks: { callback: pct } }), y: axis({ ticks: { font: { size: 11 } } }) },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` ${i.parsed.x}% of respondents` } } } },
  }),

  'c-gpi': (ctx) => new Chart(ctx, {
    type: 'bar',
    data: { labels: EDU.gpiLevels, datasets: [{ label: 'Gender Parity Index', data: EDU.gpi,
      backgroundColor: EDU.gpi.map(v => v < 0.97 ? C.alert : C.teal), borderRadius: 5, maxBarThickness: 60 }] },
    options: { ...base(), scales: { y: axis({ beginAtZero: false, min: 0.8, max: 1.1 }), x: axis() },
      plugins: { ...base().plugins, tooltip: { callbacks: { label: (i) => ` GPI ${i.parsed.y} ${i.parsed.y < 1 ? '(girls disadvantaged)' : '(at/above parity)'}` } } } },
    plugins: [{
      id: 'parityLine',
      afterDraw(chart) {
        const { ctx, chartArea: { left, right }, scales: { y } } = chart;
        const yy = y.getPixelForValue(1.0);
        ctx.save();
        ctx.setLineDash([6, 5]); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(left, yy); ctx.lineTo(right, yy); ctx.stroke();
        ctx.setLineDash([]); ctx.fillStyle = C.ink; ctx.font = '600 11px Inter';
        ctx.fillText('Parity = 1.0', right - 78, yy - 6);
        ctx.restore();
      }
    }],
  }),
};

/* --- Lazy build each chart when its container scrolls in --- */
const built = new Set();
const buildChart = (canvas) => {
  const id = canvas.id;
  if (built.has(id) || !CHART_BUILDERS[id]) return;
  const chart = CHART_BUILDERS[id](canvas.getContext('2d'));
  built.add(id);
  // Re-rasterize once layout and web fonts have settled, so text stays crisp.
  requestAnimationFrame(() => chart.resize());
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => chart.resize());
  }
};

const chartIO = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { buildChart(e.target); chartIO.unobserve(e.target); }
  });
}, { threshold: 0.15 });

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('canvas[id^="c-"]').forEach(c => chartIO.observe(c));
});
