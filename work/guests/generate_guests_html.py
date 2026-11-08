import json
from pathlib import Path

# Load json
with open("work/guests/out/guest_analytics.json", "r") as f:
    raw_json_str = f.read()

html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guest & Loyalty Intelligence · Dashboard Royale</title>
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
  
  /* Header */
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

  /* Hero */
  .hero {{ padding: 32px 0 20px; }}
  .eyebrow {{ font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); font-weight: 700; display: inline-flex; align-items: center; gap: 6px; }}
  h1 {{ font: 38px/1.15 "DM Serif Display", serif; margin: 8px 0 6px; letter-spacing: -.01em; }}
  h1 em {{ color: var(--green); font-style: normal; }}
  .sub {{ color: var(--muted); font-size: 14px; max-width: 880px; }}
  .rule-banner {{ margin-top: 14px; background: var(--gold-soft); border-left: 4px solid var(--gold); padding: 10px 14px; border-radius: 0 8px 8px 0; font-size: 13px; display: flex; align-items: center; gap: 8px; }}

  /* Filter Bar */
  .controls-bar {{ display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between; margin: 24px 0 20px; padding: 16px 20px; background: var(--card); border: 1px solid var(--line); border-radius: 12px; box-shadow: var(--shadow); }}
  .filter-group {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .filter-label {{ font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); }}
  .pill-group {{ display: flex; background: var(--track); padding: 3px; border-radius: 8px; gap: 2px; }}
  .pill-btn {{ border: 0; background: transparent; color: var(--muted); font: inherit; font-size: 12px; font-weight: 500; padding: 6px 14px; border-radius: 6px; cursor: pointer; transition: all .15s; }}
  .pill-btn:hover {{ color: var(--ink); }}
  .pill-btn.active {{ background: var(--card); color: var(--ink); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}

  /* KPIs */
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; box-shadow: var(--shadow); }}
  .kpi .k-label {{ color: var(--muted); font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: .04em; }}
  .kpi .k-val {{ font-size: 28px; font-weight: 700; margin: 8px 0 4px; font-variant-numeric: tabular-nums; line-height: 1.1; }}
  .kpi .k-sub {{ color: var(--muted); font-size: 12px; }}
  .kpi.feature {{ background: linear-gradient(135deg, var(--green), #143727); border-color: transparent; color: #ffffff; }}
  .kpi.feature .k-label, .kpi.feature .k-sub {{ color: rgba(255,255,255,.8); }}
  .kpi.alert {{ border-left: 4px solid var(--gold); }}

  /* Grid Layouts */
  .grid-2 {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 20px; margin-bottom: 24px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }}
  
  .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; gap: 12px; }}
  .card-title {{ font-size: 16px; font-weight: 600; margin: 0; display: flex; align-items: center; gap: 8px; }}
  .card-desc {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}

  /* SVG Charts */
  .chart-box {{ width: 100%; height: 260px; position: relative; }}
  svg.chart {{ width: 100%; height: 100%; overflow: visible; }}
  text.chart-axis {{ fill: var(--muted); font-size: 11px; font-family: inherit; }}
  line.chart-grid {{ stroke: var(--line); stroke-dasharray: 3 3; }}
  .tooltip {{ position: fixed; pointer-events: none; background: #16201a; color: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.2); opacity: 0; transition: opacity .1s ease; z-index: 1000; }}

  /* Concentration Bars */
  .conc-list {{ display: flex; flex-direction: column; gap: 14px; margin-top: 10px; }}
  .conc-item {{ display: flex; flex-direction: column; gap: 6px; }}
  .conc-meta {{ display: flex; justify-content: space-between; font-size: 13px; font-weight: 500; }}
  .conc-bar {{ height: 8px; background: var(--track); border-radius: 4px; overflow: hidden; display: flex; }}
  .conc-fill-coin {{ background: var(--green); height: 100%; }}
  .conc-fill-win {{ background: var(--gold); height: 100%; }}
  
  /* Tables */
  .table-box {{ overflow-x: auto; margin-top: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  th {{ padding: 10px 12px; border-bottom: 2px solid var(--line); color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; cursor: pointer; white-space: nowrap; }}
  th:hover {{ color: var(--ink); }}
  td {{ padding: 12px; border-bottom: 1px solid var(--line); font-variant-numeric: tabular-nums; white-space: nowrap; }}
  tr:hover td {{ background: var(--track); }}
  .badge {{ display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
  .badge.gold {{ background: var(--gold-soft); color: var(--gold); }}
  .badge.green {{ background: var(--green-soft); color: var(--green); }}
  .badge.red {{ background: var(--red-soft); color: var(--red); }}
  .badge.blue {{ background: var(--blue-soft); color: var(--blue); }}

  /* Deep Dive Cards */
  .stat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px; }}
  .stat-tile {{ background: var(--track); border-radius: 8px; padding: 12px; }}
  .stat-tile .s-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; font-weight: 600; }}
  .stat-tile .s-val {{ font-size: 18px; font-weight: 700; margin: 4px 0 2px; }}
  .stat-tile .s-sub {{ font-size: 11px; color: var(--muted); }}

  footer {{ padding: 40px 0 60px; color: var(--muted); font-size: 12px; text-align: center; border-top: 1px solid var(--line); margin-top: 40px; }}

  @media (max-width: 1024px) {{
    .kpis {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
  }}
  @media (max-width: 640px) {{
    .kpis {{ grid-template-columns: 1fr; }}
    h1 {{ font-size: 28px; }}
    nav {{ display: none; }}
  }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a href="index.html" class="brand">
      <div class="logo">♠</div>
      <span>Dashboard Royale</span>
    </a>
    <nav>
      <a href="index.html">Overview</a>
      <a href="floor.html">Floor & ML</a>
      <a href="guests.html" class="active">Guests & Loyalty</a>
      <a href="actions.html">Operations ($100k)</a>
    </nav>
    <div class="header-actions">
      <button class="theme-btn" id="theme-toggle">🌓 Theme</button>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="eyebrow"><span>●</span> Tracked Player Intelligence · Questions 4 & 5</div>
    <h1>Player Analytics, <em>Concentration</em> & Comps</h1>
    <p class="sub">Investigating the 113,890 loyalty cardholders who drive 65.81% of casino coin-in. Accounting for net winnings, theoretical hold, extreme player concentration, and the $190.7k comp reinvestment program.</p>
    <div class="rule-banner">
      <strong>⚠️ Accounting Principle:</strong> 
      <span><strong>Player Net = Payouts − Coin-in</strong>. A negative net indicates player loss (house gaming win). Theoretical win ($\text{{theo}}$) is $15.48M; carded players experienced a <strong>-$100,439.62 luck residual</strong> (players lost slightly more than game math expected).</span>
    </div>
  </section>

  <!-- Filter Bar -->
  <div class="controls-bar">
    <div class="filter-group">
      <span class="filter-label">Analysis Period:</span>
      <div class="pill-group" id="period-selector">
        <button class="pill-btn active" data-period="6m">Full 6 Months (Jan–Jun)</button>
        <button class="pill-btn" data-period="3m">Q2 Only (Apr–Jun)</button>
        <button class="pill-btn" data-period="1m">June Only (Jun 2025)</button>
      </div>
    </div>
    <div class="filter-group">
      <span class="filter-label">Drill-Down Segment:</span>
      <div class="pill-group" id="dimension-selector">
        <button class="pill-btn active" data-dim="by_tier">Loyalty Tier</button>
        <button class="pill-btn" data-dim="by_region">Home Region</button>
        <button class="pill-btn" data-dim="by_age">Age Band</button>
      </div>
    </div>
  </div>

  <!-- Primary KPIs -->
  <section class="kpis">
    <div class="card kpi">
      <div class="k-label">Tracked Coin-In</div>
      <div class="k-val" id="k-coin">–</div>
      <div class="k-sub" id="k-coin-sub">65.81% of property coin-in</div>
    </div>
    <div class="card kpi feature">
      <div class="k-label">House Win from Tracked</div>
      <div class="k-val" id="k-win">–</div>
      <div class="k-sub" id="k-win-sub">Observed Hold: 9.51% (Theo: 9.45%)</div>
    </div>
    <div class="card kpi">
      <div class="k-label">Comp Reinvestment Rate</div>
      <div class="k-val" id="k-comp-rate">–</div>
      <div class="k-sub" id="k-comp-sub">Economic cost: $190,669 (1.23% of theo)</div>
    </div>
    <div class="card kpi alert">
      <div class="k-label">Active Tracked Players</div>
      <div class="k-val" id="k-players">–</div>
      <div class="k-sub" id="k-visits-sub">351,729 total visits recorded</div>
    </div>
  </section>

  <!-- Row 1: Player Outcomes & Concentration -->
  <div class="grid-2">
    <!-- Concentration Analysis -->
    <div class="card">
      <div class="card-head">
        <div>
          <h2 class="card-title">Player Wealth Concentration & Pareto Distribution</h2>
          <p class="card-desc">Share of total tracked coin-in and house win generated by top player percentiles</p>
        </div>
        <span class="badge gold" id="gini-badge">Gini Coeff: 0.754</span>
      </div>
      
      <div class="conc-list" id="conc-bars">
        <!-- Injected via JS -->
      </div>

      <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--line); display: flex; justify-content: space-around; text-align: center;">
        <div>
          <div style="font-size: 11px; color: var(--muted); text-transform: uppercase;">Finished Ahead (Net > 0)</div>
          <div style="font-size: 18px; font-weight: 700; color: var(--green);" id="p-ahead">–</div>
          <div style="font-size: 11px; color: var(--muted);" id="p-ahead-sub">13.61% of players</div>
        </div>
        <div>
          <div style="font-size: 11px; color: var(--muted); text-transform: uppercase;">Broke Even (Net = 0)</div>
          <div style="font-size: 18px; font-weight: 700; color: var(--muted);" id="p-even">–</div>
          <div style="font-size: 11px; color: var(--muted);" id="p-even-sub">15.27% of players</div>
        </div>
        <div>
          <div style="font-size: 11px; color: var(--muted); text-transform: uppercase;">Lost Money (Net < 0)</div>
          <div style="font-size: 18px; font-weight: 700; color: var(--red);" id="p-loss">–</div>
          <div style="font-size: 11px; color: var(--muted);" id="p-loss-sub">71.11% of players</div>
        </div>
      </div>
    </div>

    <!-- Lorenz Curve Chart -->
    <div class="card">
      <div class="card-head">
        <div>
          <h2 class="card-title">Lorenz Curve: Cumulative Coin-In</h2>
          <p class="card-desc">Cumulative share of wagers vs cumulative population (high inequality)</p>
        </div>
      </div>
      <div class="chart-box">
        <svg class="chart" id="lorenz-svg"></svg>
      </div>
    </div>
  </div>

  <!-- Row 2: Segment Breakdown & Drill Down -->
  <div class="card" style="margin-bottom: 24px;">
    <div class="card-head">
      <div>
        <h2 class="card-title" id="seg-title">Drill-Down Breakdown by Loyalty Tier</h2>
        <p class="card-desc">Comparing volume, house win, theo hold, and complimentary reinvestment across segments</p>
      </div>
      <span class="badge green" id="seg-count-badge">3 Segments</span>
    </div>

    <div class="table-box">
      <table id="seg-table">
        <thead>
          <tr>
            <th>Segment Group</th>
            <th>Active Players</th>
            <th>Visits</th>
            <th>Tracked Coin-In</th>
            <th>Coin-In Share</th>
            <th>House Win (-Net)</th>
            <th>Observed Hold</th>
            <th>Theo Hold</th>
            <th>Comp Cost</th>
            <th>Reinvestment %</th>
            <th>POS Cash Margin</th>
          </tr>
        </thead>
        <tbody id="seg-table-body">
          <!-- Injected via JS -->
        </tbody>
      </table>
    </div>
  </div>

  <!-- Row 3: Loyalty & Comps Deep Dive (Question 5) -->
  <div class="grid-3">
    <!-- Comp Economics -->
    <div class="card">
      <div class="card-head">
        <div>
          <h2 class="card-title">Comp Economics & Margins</h2>
          <p class="card-desc">Face menu value vs actual economic cost to the house</p>
        </div>
      </div>
      <div class="stat-grid">
        <div class="stat-tile">
          <div class="s-label">Comp Face Value</div>
          <div class="s-val" id="comp-face-val">–</div>
          <div class="s-sub">Menu / retail valuation</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Economic Cost</div>
          <div class="s-val" id="comp-econ-cost">–</div>
          <div class="s-sub" id="comp-cost-ratio">27.93% of face value</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Theo Win Benchmark</div>
          <div class="s-val" id="theo-win-val">–</div>
          <div class="s-sub">Modeled expected win</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Reinvestment %</div>
          <div class="s-val" id="reinvest-val">–</div>
          <div class="s-sub" style="color:var(--red);">Bench: 8%–15% (Under-comped)</div>
        </div>
      </div>
      <p style="font-size: 12px; color: var(--muted); margin-top: 14px; line-height: 1.45;">
        <strong>Strategic Insight:</strong> The casino operates at a meager 1.23% comp reinvestment rate. F&B cost of goods is only 28 cents per $1.00 of menu price, giving the house huge leverage to reward high-value players cheaply.
      </p>
    </div>

    <!-- Points Burn Rate -->
    <div class="card">
      <div class="card-head">
        <div>
          <h2 class="card-title">Points Economy & Burn Rate</h2>
          <p class="card-desc">Loyalty point creation vs redemption activity</p>
        </div>
      </div>
      <div class="stat-grid">
        <div class="stat-tile">
          <div class="s-label">Points Earned</div>
          <div class="s-val" id="pts-earned-val">–</div>
          <div class="s-sub">Issued from slot play</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Points Redeemed</div>
          <div class="s-val" id="pts-redeemed-val">–</div>
          <div class="s-sub">Spent on F&B / amenities</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Burn Rate</div>
          <div class="s-val" id="pts-burn-val">–</div>
          <div class="s-sub" style="color:var(--gold);">95.6% unredeemed</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Redemption Cost</div>
          <div class="s-val">~10.5 pts/$1</div>
          <div class="s-sub">Consistent catalog rate</div>
        </div>
      </div>
      <p style="font-size: 12px; color: var(--muted); margin-top: 14px; line-height: 1.45;">
        <strong>Friction in Program:</strong> Over 156 million points sit idle in member accounts. Members find redemption rules friction-heavy, dampening the loyalty loop.
      </p>
    </div>

    <!-- Linked POS Contribution -->
    <div class="card">
      <div class="card-head">
        <div>
          <h2 class="card-title">Linked POS Cash & Margin</h2>
          <p class="card-desc">Cardholder spending at food & beverage venues</p>
        </div>
      </div>
      <div class="stat-grid">
        <div class="stat-tile">
          <div class="s-label">Linked POS Cash</div>
          <div class="s-val" id="pos-cash-val">–</div>
          <div class="s-sub">Cash sales to cardholders</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Linked POS COGS</div>
          <div class="s-val" id="pos-cogs-val">–</div>
          <div class="s-sub">Includes comp food cost</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Net POS Cash Margin</div>
          <div class="s-val" id="pos-margin-val">–</div>
          <div class="s-sub" style="color:var(--green);">Profitable F&B ops</div>
        </div>
        <div class="stat-tile">
          <div class="s-label">Total Contribution</div>
          <div class="s-val" id="tot-contrib-val">–</div>
          <div class="s-sub">Gaming Win + POS Margin</div>
        </div>
      </div>
      <p style="font-size: 12px; color: var(--muted); margin-top: 14px; line-height: 1.45;">
        <strong>Accounting Note:</strong> In accordance with rules, comp cost is already inside POS COGS and never subtracted twice. Carded guests generate +$743.7k in net dining profit.
      </p>
    </div>
  </div>

  <!-- Row 4: Monthly Trend Line Chart -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Monthly Tracked Activity & Hold Trends (Jan – Jun 2025)</h2>
        <p class="card-desc">Tracking monthly coin-in, actual house win, theoretical hold %, and comp reinvestment</p>
      </div>
    </div>
    <div class="chart-box" style="height: 280px;">
      <svg class="chart" id="trend-svg"></svg>
    </div>
  </div>

</main>

<div class="tooltip" id="tooltip"></div>

<footer>
  <div class="wrap">
    Dashboard Royale · Fictional Las Vegas Casino Analysis · TAMU Datathon 2026 · Submission Deliverable
  </div>
</footer>

<script>
// Raw data embedded directly
const DATA = {raw_json_str};

let currentPeriod = '6m';
let currentDim = 'by_tier';

const fmtUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 0, maximumFractionDigits: 0 }});
const fmtDecUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
const fmtNum = (n) => Number(n).toLocaleString('en-US');
const fmtPct = (n) => Number(n).toFixed(2) + '%';

const tooltip = document.getElementById('tooltip');

function showTooltip(e, html) {{
  tooltip.innerHTML = html;
  tooltip.style.opacity = '1';
  tooltip.style.left = (e.clientX + 14) + 'px';
  tooltip.style.top = (e.clientY + 14) + 'px';
}}
function hideTooltip() {{
  tooltip.style.opacity = '0';
}}

function renderDashboard() {{
  const pData = DATA[currentPeriod];
  const kpis = pData.kpis;

  // 1. Render KPIs
  document.getElementById('k-coin').textContent = fmtUsd(kpis.tracked_coin_in_usd);
  document.getElementById('k-win').textContent = fmtUsd(kpis.house_win_usd);
  document.getElementById('k-win-sub').textContent = `Observed Hold: ${{fmtPct(kpis.observed_hold_pct)}} (Theo: ${{fmtPct(kpis.theo_hold_pct)}})`;
  document.getElementById('k-comp-rate').textContent = fmtPct(kpis.comp_reinvestment_pct);
  document.getElementById('k-comp-sub').textContent = `Cost: ${{fmtUsd(kpis.comp_cost_usd)}} (${{fmtPct(kpis.comp_cost_to_face_pct)}} of face)`;
  document.getElementById('k-players').textContent = fmtNum(kpis.unique_players);
  document.getElementById('k-visits-sub').textContent = `${{fmtNum(kpis.observed_visits)}} visits (${{fmtNum(kpis.carded_play_hours)}} hrs)`;

  // Ahead / Even / Loss
  document.getElementById('p-ahead').textContent = fmtNum(kpis.ahead_players);
  document.getElementById('p-ahead-sub').textContent = `${{fmtPct(kpis.ahead_pct)}} of players`;
  document.getElementById('p-even').textContent = fmtNum(kpis.even_players);
  document.getElementById('p-even-sub').textContent = `${{fmtPct(kpis.even_pct)}} of players`;
  document.getElementById('p-loss').textContent = fmtNum(kpis.loss_players);
  document.getElementById('p-loss-sub').textContent = `${{fmtPct(kpis.loss_pct)}} of players`;
  document.getElementById('gini-badge').textContent = `Gini Coeff: ${{kpis.gini_coin}}`;

  // 2. Render Concentration Bars
  const conc = pData.concentration;
  const concContainer = document.getElementById('conc-bars');
  concContainer.innerHTML = '';

  const tiers = [
    {{ key: 'top_1', label: 'Top 1% of Players' }},
    {{ key: 'top_5', label: 'Top 5% of Players' }},
    {{ key: 'top_10', label: 'Top 10% of Players' }},
    {{ key: 'top_20', label: 'Top 20% of Players' }},
    {{ key: 'top_50', label: 'Top 50% of Players' }}
  ];

  tiers.forEach(t => {{
    const item = conc[t.key];
    const el = document.createElement('div');
    el.className = 'conc-item';
    el.innerHTML = `
      <div class="conc-meta">
        <span>${{t.label}} (${{fmtNum(item.player_count)}} members)</span>
        <span><strong>${{fmtPct(item.coin_share_pct)}}</strong> coin-in &nbsp;|&nbsp; <span style="color:var(--gold);">${{fmtPct(item.win_share_pct)}}</span> house win</span>
      </div>
      <div class="conc-bar">
        <div class="conc-fill-coin" style="width: ${{item.coin_share_pct}}%;"></div>
      </div>
    `;
    concContainer.appendChild(el);
  }});

  // 3. Render Lorenz Curve SVG
  renderLorenzCurve(pData.lorenz_curve);

  // 4. Render Deep Dive KPIs
  document.getElementById('comp-face-val').textContent = fmtUsd(kpis.comp_face_value_usd);
  document.getElementById('comp-econ-cost').textContent = fmtUsd(kpis.comp_cost_usd);
  document.getElementById('comp-cost-ratio').textContent = `${{fmtPct(kpis.comp_cost_to_face_pct)}} cost-to-face ratio`;
  document.getElementById('theo-win-val').textContent = fmtUsd(kpis.theo_usd);
  document.getElementById('reinvest-val').textContent = fmtPct(kpis.comp_reinvestment_pct);

  document.getElementById('pts-earned-val').textContent = fmtNum(kpis.points_earned);
  document.getElementById('pts-redeemed-val').textContent = fmtNum(kpis.points_redeemed);
  document.getElementById('pts-burn-val').textContent = fmtPct(kpis.points_burn_rate_pct);

  document.getElementById('pos-cash-val').textContent = fmtUsd(kpis.linked_pos_cash_usd);
  document.getElementById('pos-cogs-val').textContent = fmtUsd(kpis.linked_pos_cogs_usd);
  document.getElementById('pos-margin-val').textContent = fmtUsd(kpis.pos_net_margin_usd);
  document.getElementById('tot-contrib-val').textContent = fmtUsd(kpis.tracked_contribution_usd);

  // 5. Render Segment Table
  renderSegmentTable(pData[currentDim]);

  // 6. Render Monthly Trend
  renderTrendChart(pData.monthly_trend);
}}

function renderLorenzCurve(points) {{
  const svg = document.getElementById('lorenz-svg');
  svg.innerHTML = '';
  const w = svg.clientWidth || 460;
  const h = svg.clientHeight || 260;
  const pad = {{ top: 20, right: 30, bottom: 35, left: 45 }};
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  // Grid lines
  for (let p = 0; p <= 100; p += 25) {{
    const y = pad.top + ph - (p / 100) * ph;
    const x = pad.left + (p / 100) * pw;
    svg.innerHTML += `<line class="chart-grid" x1="${{pad.left}}" y1="${{y}}" x2="${{w - pad.right}}" y2="${{y}}"></line>`;
    svg.innerHTML += `<text class="chart-axis" x="${{pad.left - 8}}" y="${{y + 4}}" text-anchor="end">${{p}}%</text>`;
    svg.innerHTML += `<text class="chart-axis" x="${{x}}" y="${{h - 10}}" text-anchor="middle">${{p}}%</text>`;
  }}

  // Equality 45-deg line
  svg.innerHTML += `<line x1="${{pad.left}}" y1="${{pad.top + ph}}" x2="${{pad.left + pw}}" y2="${{pad.top}}" stroke="var(--muted)" stroke-dasharray="4 4" stroke-width="1.5"></line>`;

  // Lorenz curve path
  let pathD = `M ${{pad.left}} ${{pad.top + ph}}`;
  points.forEach(pt => {{
    const x = pad.left + (pt.population_pct / 100) * pw;
    const y = pad.top + ph - (pt.coin_cum_pct / 100) * ph;
    pathD += ` L ${{x}} ${{y}}`;
  }});

  svg.innerHTML += `<path d="${{pathD}}" fill="none" stroke="var(--green)" stroke-width="3"></path>`;

  // Add interactive dots
  points.forEach(pt => {{
    const x = pad.left + (pt.population_pct / 100) * pw;
    const y = pad.top + ph - (pt.coin_cum_pct / 100) * ph;
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('cx', x);
    dot.setAttribute('cy', y);
    dot.setAttribute('r', 4.5);
    dot.setAttribute('fill', 'var(--gold)');
    dot.style.cursor = 'pointer';
    dot.addEventListener('mousemove', (e) => {{
      showTooltip(e, `<strong>Pop Decile: ${{pt.population_pct}}%</strong><br>Cum. Coin-In: <strong>${{pt.coin_cum_pct}}%</strong>`);
    }});
    dot.addEventListener('mouseleave', hideTooltip);
    svg.appendChild(dot);
  }});
}}

function renderSegmentTable(records) {{
  const tbody = document.getElementById('seg-table-body');
  tbody.innerHTML = '';
  document.getElementById('seg-count-badge').textContent = `${{records.length}} Segments`;

  const dimNames = {{
    'by_tier': 'Loyalty Tier',
    'by_region': 'Home Region',
    'by_age': 'Age Band'
  }};
  document.getElementById('seg-title').textContent = `Drill-Down Breakdown by ${{dimNames[currentDim]}}`;

  records.forEach(r => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${{r.group}}</strong></td>
      <td>${{fmtNum(r.unique_players)}}</td>
      <td>${{fmtNum(r.observed_visits)}}</td>
      <td>${{fmtUsd(r.tracked_coin_in_usd)}}</td>
      <td><span class="badge blue">${{fmtPct(r.coin_share_pct)}}</span></td>
      <td style="font-weight:600; color:var(--green);">${{fmtUsd(r.house_win_usd)}}</td>
      <td>${{fmtPct(r.observed_hold_pct)}}</td>
      <td>${{fmtPct(r.theo_hold_pct)}}</td>
      <td>${{fmtUsd(r.comp_cost_usd)}}</td>
      <td><span class="badge gold">${{fmtPct(r.comp_reinvestment_pct)}}</span></td>
      <td>${{fmtUsd(r.pos_margin_usd)}}</td>
    `;
    tbody.appendChild(tr);
  }});
}}

function renderTrendChart(trend) {{
  const svg = document.getElementById('trend-svg');
  svg.innerHTML = '';
  const w = svg.clientWidth || 1000;
  const h = svg.clientHeight || 280;
  const pad = {{ top: 25, right: 40, bottom: 40, left: 60 }};
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;

  const n = trend.length;
  if (n === 0) return;

  const maxCoin = Math.max(...trend.map(t => t.tracked_coin_in_usd)) * 1.15;

  // Grid lines
  for (let i = 0; i <= 4; i++) {{
    const val = (maxCoin / 4) * i;
    const y = pad.top + ph - (i / 4) * ph;
    svg.innerHTML += `<line class="chart-grid" x1="${{pad.left}}" y1="${{y}}" x2="${{w - pad.right}}" y2="${{y}}"></line>`;
    svg.innerHTML += `<text class="chart-axis" x="${{pad.left - 10}}" y="${{y + 4}}" text-anchor="end">${{fmtUsd(val)}}</text>`;
  }}

  // Bar width
  const bw = (pw / n) * 0.45;

  trend.forEach((t, i) => {{
    const cx = pad.left + (i + 0.5) * (pw / n);
    const bh = (t.tracked_coin_in_usd / maxCoin) * ph;
    const by = pad.top + ph - bh;

    // Coin-in bar
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', cx - bw / 2);
    rect.setAttribute('y', by);
    rect.setAttribute('width', bw);
    rect.setAttribute('height', bh);
    rect.setAttribute('fill', 'var(--green-soft)');
    rect.setAttribute('stroke', 'var(--green)');
    rect.setAttribute('rx', 4);
    rect.style.cursor = 'pointer';
    rect.addEventListener('mousemove', (e) => {{
      showTooltip(e, `<strong>${{t.month}}</strong><br>Coin-In: ${{fmtUsd(t.tracked_coin_in_usd)}}<br>House Win: ${{fmtUsd(t.house_win_usd)}}<br>Hold: ${{fmtPct(t.observed_hold_pct)}}<br>Comp Reinvest: ${{fmtPct(t.comp_reinvestment_pct)}}`);
    }});
    rect.addEventListener('mouseleave', hideTooltip);
    svg.appendChild(rect);

    // Month label
    svg.innerHTML += `<text class="chart-axis" x="${{cx}}" y="${{h - 15}}" text-anchor="middle">${{t.month}}</text>`;
  }});
}}

// Event Listeners for Filters
document.getElementById('period-selector').addEventListener('click', (e) => {{
  if (e.target.tagName === 'BUTTON') {{
    document.querySelectorAll('#period-selector button').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    currentPeriod = e.target.getAttribute('data-period');
    renderDashboard();
  }}
}});

document.getElementById('dimension-selector').addEventListener('click', (e) => {{
  if (e.target.tagName === 'BUTTON') {{
    document.querySelectorAll('#dimension-selector button').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    currentDim = e.target.getAttribute('data-dim');
    renderDashboard();
  }}
}});

// Theme Toggle
document.getElementById('theme-toggle').addEventListener('click', () => {{
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
}});

window.addEventListener('resize', renderDashboard);

// Initial Load
renderDashboard();
</script>
</body>
</html>
"""

out_file = Path("dashboard/guests.html")
out_file.write_text(html_content, encoding="utf-8")
print(f"Generated {out_file} successfully! Size: {len(html_content):,} bytes")

