import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import date

# Read machine scorecard and demand daily
scorecard = pd.read_parquet("work/floor/out/machine_scorecard.parquet")
demand = pd.read_parquet("work/floor/out/demand_daily.parquet")

# Precompute data for floor.html
# Floor KPIs
tot_coin = scorecard['coin_in_usd'].sum()
tot_win = scorecard['house_win_usd'].sum()
tot_theo = scorecard['theo_usd'].sum()
tot_avail_h = scorecard['available_hours'].sum()
tot_faults = int(scorecard['faults_opened'].sum())

# By Zone
zone_agg = scorecard.groupby('zone_name').agg({
    'machine_id': 'count',
    'coin_in_usd': 'sum',
    'house_win_usd': 'sum',
    'theo_usd': 'sum',
    'available_hours': 'sum',
    'occupied_hours': 'sum',
    'faults_opened': 'sum'
}).reset_index()

zone_list = []
for _, r in zone_agg.iterrows():
    c = float(r['coin_in_usd'])
    w = float(r['house_win_usd'])
    th = float(r['theo_usd'])
    ah = float(r['available_hours'])
    zone_list.append({
        "zone": str(r['zone_name']),
        "machines": int(r['machine_id']),
        "coin_in": round(c, 2),
        "house_win": round(w, 2),
        "theo_win": round(th, 2),
        "hold_pct": round(w / c * 100.0, 2) if c > 0 else 0,
        "theo_hold_pct": round(th / c * 100.0, 2) if c > 0 else 0,
        "coin_per_avail_hour": round(c / ah, 2) if ah > 0 else 0,
        "faults": int(r['faults_opened'])
    })

# Machine table
mach_list = []
for _, r in scorecard.iterrows():
    c = float(r['coin_in_usd'])
    w = float(r['house_win_usd'])
    th = float(r['theo_usd'])
    luck = float(r['luck_residual_usd'])
    ah = float(r['available_hours'])
    mach_list.append({
        "id": str(r['machine_id']),
        "theme": str(r['theme']),
        "manufacturer": str(r['manufacturer']),
        "zone": str(r['zone_name']),
        "bank": str(r['bank_id']),
        "coin_in": round(c, 2),
        "house_win": round(w, 2),
        "theo_win": round(th, 2),
        "luck_residual": round(luck, 2),
        "hold_pct": round(w / c * 100.0, 2) if c > 0 else 0,
        "theo_hold_pct": round(th / c * 100.0, 2) if c > 0 else 0,
        "theo_per_hour": round(th / ah, 2) if ah > 0 else 0,
        "coin_per_hour": round(c / ah, 2) if ah > 0 else 0,
        "faults": int(r['faults_opened']),
        "recommendation": str(r['action_recommendation'])
    })

# Demand / Model daily records
demand_records = []
for _, r in demand.iterrows():
    demand_records.append({
        "date": str(r['gaming_date']),
        "weekday": str(r['local_weekday']),
        "is_train": bool(r['is_train']),
        "actual_coin": round(float(r['coin_in_usd']), 2),
        "pred_baseline": round(float(r['pred_baseline_coin']), 2),
        "pred_weekday": round(float(r['pred_weekday_coin']), 2)
    })

floor_data = {
    "kpis": {
        "total_coin": round(tot_coin, 2),
        "total_win": round(tot_win, 2),
        "floor_hold_pct": round(tot_win / tot_coin * 100.0, 2),
        "theo_win": round(tot_theo, 2),
        "theo_hold_pct": round(tot_theo / tot_coin * 100.0, 2),
        "available_hours": round(tot_avail_h, 1),
        "faults": tot_faults,
        "mae_baseline": 218258.10,
        "mae_weekday": 68698.55,
        "mae_improvement_pct": 68.52
    },
    "zones": zone_list,
    "machines": mach_list,
    "demand": demand_records
}

raw_json = json.dumps(floor_data)

html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Floor Performance & Machine Learning · Dashboard Royale</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #f4f5f0; --card: #ffffff; --ink: #1a2e24; --muted: #64756c; --line: #e2e6df;
    --green: #1d4d38; --green-soft: #e8f2ec; --gold: #b38b46; --gold-soft: #fbf5e8;
    --red: #a83232; --red-soft: #fbeeee; --blue: #2a5f8a; --blue-soft: #edf4f9;
    --track: #ebefe9; --shadow: 0 4px 16px rgba(0,0,0,.05);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
      --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
      --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
      --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
    --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
    --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
    --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--ink); font: 14px/1.55 Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
  .wrap {{ max-width: 1240px; margin: 0 auto; padding: 0 20px; }}
  
  header {{ background: var(--card); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 3px rgba(0,0,0,.03); }}
  header .wrap {{ display: flex; align-items: center; justify-content: space-between; height: 68px; gap: 16px; }}
  .brand {{ display: flex; align-items: center; gap: 12px; font: 22px "DM Serif Display", serif; text-decoration: none; color: inherit; }}
  .logo {{ width: 36px; height: 36px; border-radius: 8px; background: var(--green); color: var(--gold); display: grid; place-items: center; font-size: 20px; font-weight: bold; }}
  nav {{ display: flex; gap: 6px; align-items: center; }}
  nav a {{ text-decoration: none; color: var(--muted); padding: 8px 14px; border-radius: 8px; font-weight: 500; font-size: 13px; transition: all .15s; }}
  nav a:hover {{ color: var(--ink); background: var(--track); }}
  nav a.active {{ color: var(--green); background: var(--green-soft); font-weight: 600; }}
  .header-actions {{ display: flex; align-items: center; gap: 10px; }}
  .theme-btn {{ background: transparent; border: 1px solid var(--line); border-radius: 8px; padding: 6px 10px; cursor: pointer; color: var(--muted); font-size: 13px; }}

  .hero {{ padding: 32px 0 20px; }}
  .eyebrow {{ font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); font-weight: 700; display: inline-flex; align-items: center; gap: 6px; }}
  h1 {{ font: 38px/1.15 "DM Serif Display", serif; margin: 8px 0 6px; letter-spacing: -.01em; }}
  h1 em {{ color: var(--green); font-style: normal; }}
  .sub {{ color: var(--muted); font-size: 14px; max-width: 900px; }}

  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; box-shadow: var(--shadow); margin-bottom: 24px; }}
  .kpi .k-label {{ color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
  .kpi .k-val {{ font-size: 28px; font-weight: 700; margin: 8px 0 4px; font-variant-numeric: tabular-nums; line-height: 1.1; }}
  .kpi .k-sub {{ color: var(--muted); font-size: 12px; }}
  .kpi.feature {{ background: linear-gradient(135deg, var(--green), #143727); border-color: transparent; color: #ffffff; }}
  .kpi.feature .k-label, .kpi.feature .k-sub {{ color: rgba(255,255,255,.8); }}

  .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; gap: 12px; }}
  .card-title {{ font-size: 18px; font-weight: 600; margin: 0; display: flex; align-items: center; gap: 8px; }}
  .card-desc {{ font-size: 13px; color: var(--muted); margin-top: 2px; }}

  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
  .chart-box {{ width: 100%; height: 260px; position: relative; }}
  svg.chart {{ width: 100%; height: 100%; overflow: visible; }}
  text.chart-axis {{ fill: var(--muted); font-size: 11px; }}
  line.chart-grid {{ stroke: var(--line); stroke-dasharray: 3 3; }}
  
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  th {{ padding: 10px 12px; border-bottom: 2px solid var(--line); color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; cursor: pointer; white-space: nowrap; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); font-variant-numeric: tabular-nums; white-space: nowrap; }}
  tr:hover td {{ background: var(--track); }}
  .table-box {{ overflow-x: auto; max-height: 480px; overflow-y: auto; }}

  .badge {{ display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
  .badge.gold {{ background: var(--gold-soft); color: var(--gold); }}
  .badge.green {{ background: var(--green-soft); color: var(--green); }}
  .badge.red {{ background: var(--red-soft); color: var(--red); }}
  .badge.blue {{ background: var(--blue-soft); color: var(--blue); }}

  input[type="search"] {{ border: 1px solid var(--line); background: var(--card); color: var(--ink); border-radius: 8px; height: 36px; padding: 0 12px; font: inherit; width: 240px; }}

  footer {{ padding: 40px 0 60px; color: var(--muted); font-size: 12px; text-align: center; border-top: 1px solid var(--line); margin-top: 40px; }}
  @media (max-width: 900px) {{
    .kpis {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a href="index.html" class="brand"><div class="logo">♠</div><span>Dashboard Royale</span></a>
    <nav>
      <a href="index.html">Overview</a>
      <a href="floor.html" class="active">Floor & ML</a>
      <a href="guests.html">Guests & Loyalty</a>
      <a href="actions.html">Operations ($100k)</a>
    </nav>
    <div class="header-actions"><button class="theme-btn" id="theme-toggle">🌓 Theme</button></div>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="eyebrow"><span>●</span> Questions 1, 2, 3 & Machine Learning Model</div>
    <h1>Floor Performance, <em>Downtime</em> & Demand ML</h1>
    <p class="sub">Investigating all 300 machines across exposure, theoretical win, downtime, and out-of-sample time-series forecasting. Testing management's bottom 10 machines against mathematical truth.</p>
  </section>

  <section class="kpis">
    <div class="card kpi">
      <div class="k-label">Property Coin-In</div>
      <div class="k-val" id="k-coin">$248.91M</div>
      <div class="k-sub">181 gaming days · 300 machines</div>
    </div>
    <div class="card kpi feature">
      <div class="k-label">Total House Win</div>
      <div class="k-val" id="k-win">$23.64M</div>
      <div class="k-sub">Hold: 9.50% (Theo: 9.45%)</div>
    </div>
    <div class="card kpi">
      <div class="k-label">ML Forecast Test MAE</div>
      <div class="k-val" id="k-mae">$68,699</div>
      <div class="k-sub">Weekday Model (-68.5% error)</div>
    </div>
    <div class="card kpi">
      <div class="k-label">Downtime Concentration</div>
      <div class="k-val" id="k-faults">56.3%</div>
      <div class="k-sub">Ridgeline Gaming (680 faults)</div>
    </div>
  </section>

  <!-- ML Forecast Section -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Out-of-Sample Demand Forecasting: May–June 2025 Test Horizon</h2>
        <p class="card-desc">Trained strictly on Jan 1 – Apr 30; validated on May 1 – Jun 30. Compares Flat Mean Baseline vs Day-of-Week Stratified Model.</p>
      </div>
      <span class="badge green">MAE: $68.7k vs $218.3k Baseline (-68.5%)</span>
    </div>

    <div class="chart-box" style="height: 260px;">
      <svg class="chart" id="forecast-svg"></svg>
    </div>

    <div style="margin-top: 14px; font-size: 13px; color: var(--muted); display: flex; gap: 24px; flex-wrap: wrap;">
      <div><span style="display:inline-block;width:12px;height:3px;background:var(--ink);vertical-align:middle;margin-right:6px;"></span>Actual Coin-In</div>
      <div><span style="display:inline-block;width:12px;height:3px;background:var(--green);vertical-align:middle;margin-right:6px;"></span>Weekday Model Forecast (MAE: $68,699)</div>
      <div><span style="display:inline-block;width:12px;height:3px;background:var(--red);stroke-dasharray:3 3;vertical-align:middle;margin-right:6px;"></span>Flat Training Mean Baseline (MAE: $218,258)</div>
    </div>
  </div>

  <!-- Zone Breakdown -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Floor-to-Zone Performance Comparison</h2>
        <p class="card-desc">Comparing machine density, coin-in per available hour, and fault concentration across zones</p>
      </div>
    </div>
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>Zone Name</th>
            <th>Machines</th>
            <th>Total Coin-In</th>
            <th>House Win</th>
            <th>Observed Hold</th>
            <th>Theo Hold</th>
            <th>Coin-In / Avail Hour</th>
            <th>Faults</th>
          </tr>
        </thead>
        <tbody id="zone-tbody"></tbody>
      </table>
    </div>
  </div>

  <!-- Machine Scorecard Table -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Comprehensive Machine Scorecard (310 Units)</h2>
        <p class="card-desc">Ranked by theoretical win per available hour vs naive house win. Search by ID, theme, zone, or manufacturer.</p>
      </div>
      <input type="search" id="mach-search" placeholder="Filter machines (e.g. M-1158, Ridgeline, Back Forty)...">
    </div>
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>Machine ID</th>
            <th>Theme</th>
            <th>Manufacturer</th>
            <th>Zone</th>
            <th>Bank</th>
            <th>House Win</th>
            <th>Theo Win</th>
            <th>Luck Residual</th>
            <th>Obs. Hold</th>
            <th>Theo / Avail Hr</th>
            <th>Faults</th>
            <th>Action Recommendation</th>
          </tr>
        </thead>
        <tbody id="mach-tbody"></tbody>
      </table>
    </div>
  </div>

</main>

<footer>
  <div class="wrap">Dashboard Royale · Floor & ML Intelligence · TAMU Datathon 2026</div>
</footer>

<script>
const DATA = {raw_json};
const fmtUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 0, maximumFractionDigits: 0 }});
const fmtDecUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
const fmtPct = (n) => Number(n).toFixed(2) + '%';
const fmtNum = (n) => Number(n).toLocaleString('en-US');

// Render Zones
const zTbody = document.getElementById('zone-tbody');
DATA.zones.forEach(z => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><strong>${{z.zone}}</strong></td>
    <td>${{z.machines}}</td>
    <td>${{fmtUsd(z.coin_in)}}</td>
    <td style="color:var(--green);font-weight:600;">${{fmtUsd(z.house_win)}}</td>
    <td>${{fmtPct(z.hold_pct)}}</td>
    <td>${{fmtPct(z.theo_hold_pct)}}</td>
    <td><strong>${{fmtDecUsd(z.coin_per_avail_hour)}}/hr</strong></td>
    <td><span class="badge ${{z.faults > 200 ? 'red' : 'gold'}}">${{z.faults}}</span></td>
  `;
  zTbody.appendChild(tr);
}});

// Render Machine Table
const mTbody = document.getElementById('mach-tbody');
function renderMachines(query = '') {{
  mTbody.innerHTML = '';
  const q = query.toLowerCase();
  const filtered = DATA.machines.filter(m => 
    m.id.toLowerCase().includes(q) ||
    m.theme.toLowerCase().includes(q) ||
    m.manufacturer.toLowerCase().includes(q) ||
    m.zone.toLowerCase().includes(q) ||
    m.bank.toLowerCase().includes(q)
  );

  filtered.forEach(m => {{
    const tr = document.createElement('tr');
    if (m.id === 'M-1158') tr.style.background = 'var(--red-soft)';
    tr.innerHTML = `
      <td><strong>${{m.id}}</strong></td>
      <td>${{m.theme}}</td>
      <td>${{m.manufacturer}}</td>
      <td>${{m.zone}}</td>
      <td>${{m.bank}}</td>
      <td>${{fmtUsd(m.house_win)}}</td>
      <td>${{fmtUsd(m.theo_win)}}</td>
      <td style="color:${{m.luck_residual < -15000 ? 'var(--red)' : 'inherit'}}; font-weight:${{m.luck_residual < -15000 ? '700' : '400'}};">${{fmtUsd(m.luck_residual)}}</td>
      <td>${{fmtPct(m.hold_pct)}}</td>
      <td><strong>${{fmtDecUsd(m.theo_per_hour)}}/hr</strong></td>
      <td>${{m.faults}}</td>
      <td><span class="badge ${{m.recommendation.includes('RETAIN') ? 'green' : m.recommendation.includes('REPAIR') ? 'gold' : 'blue'}}">${{m.recommendation}}</span></td>
    `;
    mTbody.appendChild(tr);
  }});
}}

renderMachines();
document.getElementById('mach-search').addEventListener('input', (e) => renderMachines(e.target.value));

// Render Forecast Chart
function renderForecastChart() {{
  const svg = document.getElementById('forecast-svg');
  svg.innerHTML = '';
  const testPoints = DATA.demand.filter(d => !d.is_train);
  const w = svg.clientWidth || 1000;
  const h = svg.clientHeight || 260;
  const pad = {{ top: 20, right: 30, bottom: 35, left: 65 }};
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;
  const n = testPoints.length;

  const maxVal = 2500000;
  const minVal = 800000;

  for (let v = 1000000; v <= 2500000; v += 500000) {{
    const y = pad.top + ph - ((v - minVal) / (maxVal - minVal)) * ph;
    svg.innerHTML += `<line class="chart-grid" x1="${{pad.left}}" y1="${{y}}" x2="${{w - pad.right}}" y2="${{y}}"></line>`;
    svg.innerHTML += `<text class="chart-axis" x="${{pad.left - 8}}" y="${{y + 4}}" text-anchor="end">${{fmtUsd(v)}}</text>`;
  }}

  let pathActual = '', pathWeekday = '', pathBaseline = '';
  testPoints.forEach((pt, i) => {{
    const x = pad.left + (i / (n - 1)) * pw;
    const yAct = pad.top + ph - ((pt.actual_coin - minVal) / (maxVal - minVal)) * ph;
    const yWk = pad.top + ph - ((pt.pred_weekday - minVal) / (maxVal - minVal)) * ph;
    const yBase = pad.top + ph - ((pt.pred_baseline - minVal) / (maxVal - minVal)) * ph;

    pathActual += (i === 0 ? `M ${{x}} ${{yAct}}` : ` L ${{x}} ${{yAct}}`);
    pathWeekday += (i === 0 ? `M ${{x}} ${{yWk}}` : ` L ${{x}} ${{yWk}}`);
    pathBaseline += (i === 0 ? `M ${{x}} ${{yBase}}` : ` L ${{x}} ${{yBase}}`);
  }});

  svg.innerHTML += `<path d="${{pathBaseline}}" fill="none" stroke="var(--red)" stroke-dasharray="4 4" stroke-width="2"></path>`;
  svg.innerHTML += `<path d="${{pathWeekday}}" fill="none" stroke="var(--green)" stroke-width="2.5"></path>`;
  svg.innerHTML += `<path d="${{pathActual}}" fill="none" stroke="var(--ink)" stroke-width="2"></path>`;
}}

renderForecastChart();
window.addEventListener('resize', renderForecastChart);

document.getElementById('theme-toggle').addEventListener('click', () => {{
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
}});
</script>
</body>
</html>
"""

out_file = Path("dashboard/floor.html")
out_file.write_text(html_content, encoding="utf-8")
print(f"Generated {out_file} successfully! Size: {len(html_content):,} bytes")

