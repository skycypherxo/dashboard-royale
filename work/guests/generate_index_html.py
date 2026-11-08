from pathlib import Path

html_content = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard Royale · Executive Intelligence Suite</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f4f5f0; --card: #ffffff; --ink: #1a2e24; --muted: #64756c; --line: #e2e6df;
    --green: #1d4d38; --green-soft: #e8f2ec; --gold: #b38b46; --gold-soft: #fbf5e8;
    --red: #a83232; --red-soft: #fbeeee; --blue: #2a5f8a; --blue-soft: #edf4f9;
    --track: #ebefe9; --shadow: 0 4px 16px rgba(0,0,0,.05);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
      --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
      --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
      --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
    }
  }
  :root[data-theme="dark"] {
    --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
    --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
    --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
    --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--ink); font: 14px/1.55 Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 1240px; margin: 0 auto; padding: 0 20px; }
  
  /* Header */
  header { background: var(--card); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 3px rgba(0,0,0,.03); }
  header .wrap { display: flex; align-items: center; justify-content: space-between; height: 68px; gap: 16px; }
  .brand { display: flex; align-items: center; gap: 12px; font: 22px "DM Serif Display", serif; text-decoration: none; color: inherit; }
  .logo { width: 36px; height: 36px; border-radius: 8px; background: var(--green); color: var(--gold); display: grid; place-items: center; font-size: 20px; font-weight: bold; }
  nav { display: flex; gap: 6px; align-items: center; }
  nav a { text-decoration: none; color: var(--muted); padding: 8px 14px; border-radius: 8px; font-weight: 500; font-size: 13px; transition: all .15s; }
  nav a:hover { color: var(--ink); background: var(--track); }
  nav a.active { color: var(--green); background: var(--green-soft); font-weight: 600; }
  .header-actions { display: flex; align-items: center; gap: 10px; }
  .theme-btn { background: transparent; border: 1px solid var(--line); border-radius: 8px; padding: 6px 10px; cursor: pointer; color: var(--muted); font-size: 13px; }

  /* Hero */
  .hero { padding: 44px 0 28px; text-align: center; }
  .eyebrow { font-size: 11px; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); font-weight: 700; margin-bottom: 10px; display: inline-flex; align-items: center; gap: 6px; }
  h1 { font: 46px/1.12 "DM Serif Display", serif; margin: 0 0 12px; letter-spacing: -.02em; }
  h1 em { color: var(--green); font-style: normal; }
  .sub { color: var(--muted); font-size: 15px; max-width: 820px; margin: 0 auto 20px; line-height: 1.6; }
  
  /* Primary Banner */
  .verdict-banner { background: var(--card); border: 2px solid var(--gold); border-radius: 12px; padding: 20px 24px; max-width: 980px; margin: 0 auto 36px; text-align: left; box-shadow: var(--shadow); display: flex; gap: 18px; align-items: flex-start; }
  .verdict-icon { font-size: 32px; line-height: 1; }
  .verdict-title { font-size: 16px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }
  .verdict-desc { font-size: 13px; color: var(--muted); line-height: 1.5; }

  /* KPIs */
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 36px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; box-shadow: var(--shadow); }
  .kpi .k-label { color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
  .kpi .k-val { font-size: 30px; font-weight: 700; margin: 8px 0 4px; font-variant-numeric: tabular-nums; line-height: 1.1; }
  .kpi .k-sub { color: var(--muted); font-size: 12px; }
  .kpi.feature { background: linear-gradient(135deg, var(--green), #143727); border-color: transparent; color: #ffffff; }
  .kpi.feature .k-label, .kpi.feature .k-sub { color: rgba(255,255,255,.8); }

  /* Portal Gateway Cards */
  .gateway-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }
  .portal-card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 26px; box-shadow: var(--shadow); display: flex; flex-direction: column; transition: transform .2s, box-shadow .2s; text-decoration: none; color: inherit; position: relative; overflow: hidden; }
  .portal-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.08); border-color: var(--green); }
  .portal-card::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
  .portal-card.card-floor::before { background: var(--gold); }
  .portal-card.card-guests::before { background: var(--green); }
  .portal-card.card-actions::before { background: var(--blue); }

  .portal-tag { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 10px; display: inline-flex; align-items: center; gap: 6px; }
  .card-floor .portal-tag { color: var(--gold); }
  .card-guests .portal-tag { color: var(--green); }
  .card-actions .portal-tag { color: var(--blue); }

  .portal-title { font: 24px "DM Serif Display", serif; margin-bottom: 10px; line-height: 1.2; }
  .portal-desc { font-size: 13px; color: var(--muted); line-height: 1.5; margin-bottom: 20px; flex: 1; }
  .portal-bullets { list-style: none; margin-bottom: 24px; display: flex; flex-direction: column; gap: 8px; font-size: 12px; color: var(--ink); }
  .portal-bullets li { display: flex; align-items: center; gap: 8px; }
  .portal-bullets li::before { content: "✓"; color: var(--green); font-weight: bold; }
  .portal-btn { background: var(--track); color: var(--ink); border-radius: 8px; padding: 10px 16px; font-size: 13px; font-weight: 600; text-align: center; display: flex; align-items: center; justify-content: center; gap: 6px; transition: background .15s; }
  .portal-card:hover .portal-btn { background: var(--green); color: #fff; }

  /* AI Analyst Section */
  .ai-section { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 26px; box-shadow: var(--shadow); margin-bottom: 40px; }
  .ai-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }
  .ai-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }
  .ai-chip { background: var(--track); border: 1px solid var(--line); border-radius: 20px; padding: 6px 14px; font-size: 12px; cursor: pointer; color: var(--ink); transition: all .15s; }
  .ai-chip:hover, .ai-chip.active { background: var(--green); color: #fff; border-color: var(--green); }
  .ai-chatbox { background: var(--bg); border: 1px solid var(--line); border-radius: 10px; padding: 18px; min-height: 120px; font-size: 13.5px; line-height: 1.6; margin-bottom: 16px; }
  .ai-input-row { display: flex; gap: 10px; }
  .ai-input { flex: 1; border: 1px solid var(--line); border-radius: 8px; background: var(--card); padding: 10px 14px; font: inherit; font-size: 13px; color: var(--ink); }
  .ai-send-btn { background: var(--green); color: #fff; border: 0; border-radius: 8px; padding: 0 20px; font-weight: 600; cursor: pointer; font-size: 13px; }
  .ai-send-btn:hover { background: #143727; }
  .ai-api-toggle { font-size: 11px; color: var(--muted); margin-top: 8px; display: flex; align-items: center; gap: 8px; }

  /* Key Takeaways Grid */
  .takeaways-section { margin-bottom: 40px; }
  .section-head { margin-bottom: 20px; text-align: center; }
  .section-head h2 { font: 28px "DM Serif Display", serif; margin-bottom: 6px; }
  .section-head p { font-size: 13px; color: var(--muted); }
  
  .takeaways-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .takeaway-card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; }
  .takeaway-num { font-size: 12px; font-weight: 700; color: var(--gold); text-transform: uppercase; margin-bottom: 6px; }
  .takeaway-title { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
  .takeaway-text { font-size: 13px; color: var(--muted); line-height: 1.5; }

  footer { padding: 40px 0 60px; color: var(--muted); font-size: 12px; text-align: center; border-top: 1px solid var(--line); margin-top: 40px; }

  @media (max-width: 900px) {
    .gateway-grid, .takeaways-grid { grid-template-columns: 1fr; }
    .kpis { grid-template-columns: repeat(2, 1fr); }
    h1 { font-size: 34px; }
  }
  @media (max-width: 600px) {
    .kpis { grid-template-columns: 1fr; }
  }
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
      <a href="index.html" class="active">Overview</a>
      <a href="floor.html">Floor & ML</a>
      <a href="guests.html">Guests & Loyalty</a>
      <a href="actions.html">Operations ($100k)</a>
    </nav>
    <div class="header-actions">
      <button class="theme-btn" id="theme-toggle">🌓 Theme</button>
    </div>
  </div>
</header>

<main class="wrap">
  <section class="hero">
    <div class="eyebrow"><span>●</span> Executive Intelligence Portal · The Gilded Ace</div>
    <h1>Luck, Location, <em>or a Leak?</em></h1>
    <p class="sub">Six months of gaming, player, downtime, and operational telemetry synthesized into a decision-grade command center. Uncovering the mathematical truth behind floor earnings and deploying $100,000 with disciplined precision.</p>
  </section>

  <!-- Executive Verdict -->
  <div class="verdict-banner">
    <div class="verdict-icon">⚖️</div>
    <div>
      <div class="verdict-title">Executive Determination: Stop Management's Machine Replacement Plan</div>
      <div class="verdict-desc">
        Management’s proposal to replace the 10 lowest-earning machines by nominal house win is an expensive mistake. Machines like <code>M-1158</code> generated <strong>$519.6k in coin-in</strong> and <strong>$52.0k in theoretical win</strong>, but ran -$36.2k behind expectation due to pure negative player luck (3.04% hold vs 10% expected). Eight of the ten bottom machines suffer from foot-traffic starvation in Back Forty, not bad math. Instead of wasting capital on replacements, we deploy <strong>$29,000</strong> on root-cause maintenance, machine inspections, and a loyalty comp pilot, while <strong>preserving $71,000 in treasury cash</strong>.
      </div>
    </div>
  </div>

  <!-- Primary Casino KPIs -->
  <section class="kpis">
    <div class="card kpi">
      <div class="k-label">Property Coin-In (6 Months)</div>
      <div class="k-val">$248.91M</div>
      <div class="k-sub">181 gaming days · 300–308 machines</div>
    </div>
    <div class="card kpi feature">
      <div class="k-label">Total House Gaming Win</div>
      <div class="k-val">$23.64M</div>
      <div class="k-sub">Floor Observed Hold: 9.50%</div>
    </div>
    <div class="card kpi">
      <div class="k-label">Tracked Player Share</div>
      <div class="k-val">65.81%</div>
      <div class="k-sub">$163.80M coin-in · 113,890 members</div>
    </div>
    <div class="card kpi">
      <div class="k-label">Available Budget Preserved</div>
      <div class="k-val">$71,000</div>
      <div class="k-sub">Committed: $29,000 of $100,000</div>
    </div>
  </section>

  <!-- Navigation Gateways -->
  <div class="gateway-grid">

    <!-- Card 1: Floor -->
    <a href="floor.html" class="portal-card card-floor">
      <div class="portal-tag">Floor Analytics & Forecasting</div>
      <h3 class="portal-title">Floor Performance & Machine Scorecard</h3>
      <p class="portal-desc">Investigate all 300 machines across exposure, availability, manufacturer downtime, and the daily coin-in forecasting ML model.</p>
      <ul class="portal-bullets">
        <li>Machine scorecard per available hour</li>
        <li>Ridgeline downtime concentration (56.3%)</li>
        <li>Daily coin-in time-series ML forecast (-68.5% MAE)</li>
      </ul>
      <div class="portal-btn">Launch Floor Dashboard →</div>
    </a>

    <!-- Card 2: Guests -->
    <a href="guests.html" class="portal-card card-guests">
      <div class="portal-tag">Player Analytics & Loyalty</div>
      <h3 class="portal-title">Guest Intelligence & Comp Economics</h3>
      <p class="portal-desc">Explore carded player outcomes, extreme player wealth concentration (Gini: 0.754), and the 1.23% complimentary reinvestment program.</p>
      <ul class="portal-bullets">
        <li>Top 1% generates 22.85% of coin-in</li>
        <li>Locals drive 58.6% of tracked volume</li>
        <li>Comp economic cost is only 27.9% of face value</li>
      </ul>
      <div class="portal-btn">Launch Guest Dashboard →</div>
    </a>

    <!-- Card 3: Actions -->
    <a href="actions.html" class="portal-card card-actions">
      <div class="portal-tag">Operational Budget ($100k)</div>
      <h3 class="portal-title">Priced Recommendations & Allocation</h3>
      <p class="portal-desc">Priced 30-day action portfolio for July 1–30. All 9 required criteria, uncertainty, abandonment triggers, and $71,000 preserved budget.</p>
      <ul class="portal-bullets">
        <li>Comp Policy Pilot with Control Group ($14k)</li>
        <li>Ridgeline Preventive Maintenance ($9k)</li>
        <li>Targeted Paytable Inspections ($6k)</li>
      </ul>
      <div class="portal-btn">Launch Actions Dashboard →</div>
    </a>

  </div>

  <!-- Interactive AI Casino Analyst Section (TEAM.md Phase 3E) -->
  <section class="ai-section">
    <div class="ai-head">
      <div>
        <div class="eyebrow"><span>●</span> Natural Language Intelligence · Phase 3E</div>
        <h2 style="font: 26px 'DM Serif Display', serif; margin-top: 4px;">AI Casino Operations Analyst</h2>
        <p style="font-size: 13px; color: var(--muted);">Ask questions about machine performance, downtime root causes, player wealth concentration, or the $100k budget.</p>
      </div>
      <div style="font-size: 12px; color: var(--muted); background: var(--track); padding: 6px 12px; border-radius: 8px;">
        Grounded in 6-Month Casino Telemetry
      </div>
    </div>

    <!-- Pre-built Quick Prompt Chips -->
    <div class="ai-chips">
      <button class="ai-chip active" data-q="bottom10">Why are the bottom 10 machines earning so little?</button>
      <button class="ai-chip" data-q="m1158">Why shouldn't we replace machine M-1158?</button>
      <button class="ai-chip" data-q="downtime">Is machine downtime responsible for poor contribution?</button>
      <button class="ai-chip" data-q="concentration">How concentrated is player wealth?</button>
      <button class="ai-chip" data-q="comps">Why is the comp reinvestment rate so low?</button>
      <button class="ai-chip" data-q="budget">How was the $100,000 budget allocated?</button>
    </div>

    <!-- AI Response Box -->
    <div class="ai-chatbox" id="ai-response">
      <strong>AI Analyst:</strong> Evaluating management's naive bottom 10 machines reveals a critical flaw in traditional nominal house-win evaluation. Machine <code>M-1158</code> generated <strong>$519,610.00 in coin-in</strong> and <strong>$51,961.00 in theoretical win</strong>, but ran <strong>-$36,164.75 behind expectation</strong> due to temporary player luck. Furthermore, 8 of the 10 lowest-earning machines sit in <strong>Back Forty</strong>, where entrance foot traffic is 48% below Center Pit. Replacing these games would discard high-volume player favorites while failing to fix traffic starvation.
    </div>

    <!-- Custom Question Input -->
    <div class="ai-input-row">
      <input type="text" class="ai-input" id="ai-custom-input" placeholder="Ask a custom operations question (e.g., 'What is our swing shift downtime exposure?')...">
      <button class="ai-send-btn" id="ai-send-btn">Ask AI Analyst</button>
    </div>

    <div class="ai-api-toggle">
      <span>💡 Pro tip: Grounded in deterministic query tables. Optional Google Gemini API key:</span>
      <input type="password" id="gemini-key" placeholder="Optional Google Gemini API Key" style="border:1px solid var(--line); border-radius:4px; padding:3px 8px; font-size:11px; width:220px; background:var(--card); color:var(--ink);">
    </div>
  </section>

  <!-- Key Analytical Takeaways -->
  <section class="takeaways-section">
    <div class="section-head">
      <h2>Four Foundational Insights from the Telemetry</h2>
      <p>Why conventional casino wisdom fails without multi-layered data verification</p>
    </div>

    <div class="takeaways-grid">
      <div class="takeaway-card">
        <div class="takeaway-num">Finding 01</div>
        <div class="takeaway-title">The Fallacy of House Win Ranking</div>
        <div class="takeaway-text">
          Evaluating slot machines by nominal win ignores statistical variance. High-volatility titles with substantial coin-in can experience temporary unlucky runs. Ranking by theoretical win per available hour reveals true game health.
        </div>
      </div>
      <div class="takeaway-card">
        <div class="takeaway-num">Finding 02</div>
        <div class="takeaway-title">Severe Loyalty Under-Comping</div>
        <div class="takeaway-text">
          At 1.23% reinvestment and a 4.38% point burn rate, the casino is under-rewarding its core local patrons. Food & beverage items cost only 28 cents per $1 menu price, offering enormous margin room to drive repeat visitation.
        </div>
      </div>
      <div class="takeaway-card">
        <div class="takeaway-num">Finding 03</div>
        <div class="takeaway-title">Single-Manufacturer Fault Cluster</div>
        <div class="takeaway-text">
          Ridgeline Gaming units generate 56.3% of all floor breakdowns and 2,780 hours of downtime. A single preventive maintenance sweep ($9,000) eliminates the primary operational failure point without buying new machines.
        </div>
      </div>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    Dashboard Royale · TAMU Datathon 2026 Submission · Built by Vaishnavi (Guest & BI Lead) & Akshaya (Floor & ML Lead)
  </div>
</footer>

<script>
// Knowledge Base for Grounded AI Analyst Responses
const KB = {
  bottom10: "<strong>AI Analyst:</strong> Evaluating management's naive bottom 10 machines reveals a critical flaw in traditional nominal house-win evaluation. Machine <code>M-1158</code> generated <strong>$519,610.00 in coin-in</strong> and <strong>$51,961.00 in theoretical win</strong>, but ran <strong>-$36,164.75 behind expectation</strong> due to temporary player luck. Furthermore, 8 of the 10 lowest-earning machines sit in <strong>Back Forty</strong>, where entrance foot traffic is 48% below Center Pit. Replacing these games would discard high-volume player favorites while failing to fix traffic starvation.",
  m1158: "<strong>AI Analyst on M-1158:</strong> Replacing <code>M-1158</code> (Desert Gold, Bank B-38) would be an operational disaster. Despite recording only $15,796.25 in house win, it had <strong>$519,610.00 in coin-in</strong> (averaging $120.30/hr) and <strong>$51,961.00 in theoretical win</strong> across 4,319.4 available hours (99.45% availability). Its low hold of 3.04% vs 10.0% expected reflects high-volatility jackpot variance. Replacing it with a leased title ($3,380) or purchase ($22,000) throws away an active player favorite.",
  downtime: "<strong>AI Analyst on Downtime:</strong> Yes, downtime is heavily concentrated. Out of 1,207 fault tickets, <strong>Ridgeline Gaming accounted for 680 faults (56.34%)</strong> and 2,780 hours of downtime ($63k+ in repair costs). Moreover, <strong>Swing Shift suffered 577 faults (47.8%)</strong> but had only 1 technician on duty. Our recommended preventive maintenance sweep (<code>A-PREVENTIVE</code>: $9,000) directly targets all 86 Ridgeline units during graveyard hours.",
  concentration: "<strong>AI Analyst on Player Wealth:</strong> Player wagering exhibits extreme Pareto concentration. The <strong>top 1% of cardholders (1,138 players) generates 22.85% of coin-in</strong>, while the <strong>top 5% generates 55.33%</strong> (Gini coefficient: <strong>0.754</strong>). Local players (only 7.0% of cardholders) drive <strong>58.60% of all tracked coin-in ($95.99M)</strong>, averaging over $12,048 in coin-in per player over 6 months.",
  comps: "<strong>AI Analyst on Comps & Loyalty:</strong> The casino operates at an anemic <strong>1.23% comp reinvestment rate</strong> ($190,669 comp cost / $15.48M theoretical win), compared to the 8%–15% Las Vegas benchmark. Over 95% of loyalty points go unredeemed (4.38% burn rate). However, F&B cost of goods is only <strong>27.93% of menu face value</strong> (costing the house 28¢ per $1 menu item). Our <code>A-COMP-PILOT</code> ($14,000) tests raising reinvestment to 4.5% of theo via dining comps.",
  budget: "<strong>AI Analyst on $100k Budget Allocation:</strong> We deployed exactly <strong>$29,000.00</strong> across three targeted actions: 1) <code>A-COMP-PILOT</code> ($14,000 incl. $10k comp reserve), 2) <code>A-PREVENTIVE</code> ($9,000 for Ridgeline sweep), and 3) <code>A-INSPECT</code> ($6,000 to verify 5 top luck-deficit machines). We preserved <strong>$71,000.00 in treasury cash</strong> (<code>A-HOLD</code>), avoiding speculative machine purchases."
};

document.querySelectorAll('.ai-chip').forEach(chip => {
  chip.addEventListener('click', (e) => {
    document.querySelectorAll('.ai-chip').forEach(c => c.classList.remove('active'));
    e.target.classList.add('active');
    const qKey = e.target.getAttribute('data-q');
    document.getElementById('ai-response').innerHTML = KB[qKey] || "Analyzing telemetry...";
  });
});

document.getElementById('ai-send-btn').addEventListener('click', async () => {
  const query = document.getElementById('ai-custom-input').value.trim();
  const key = document.getElementById('gemini-key').value.trim();
  const responseBox = document.getElementById('ai-response');

  if (!query) return;

  responseBox.innerHTML = "<em>Analyzing casino telemetry with AI operations model...</em>";

  if (key) {
    try {
      const prompt = `You are the executive AI Casino Operations Analyst for 'The Gilded Ace' (Dashboard Royale). Ground all answers in this factual telemetry:
- Property Coin-In: $248.91M, House Win: $23.64M (9.50% hold).
- Tracked Players: 113,890 members driving 65.81% of coin-in ($163.80M).
- Player Concentration: Top 1% drives 22.85%, Top 5% drives 55.33% (Gini: 0.754).
- Local Cardholders: 7.0% of players driving 58.60% of tracked coin-in ($95.99M).
- Comp Reinvestment: Only 1.23% of theoretical win (Las Vegas benchmark: 8%-15%). F&B cost is 27.93% of face value. Point burn rate is 4.38%.
- Machine Faults: 1,207 total; Ridgeline accounts for 680 faults (56.34%). Swing shift has 577 faults (47.8%).
- Machine M-1158: House win $15,796, but Coin-in was $519,610 and Theo Win was $51,961 with -$36,165 luck residual. DO NOT REPLACE.
- $100k Budget: $14k on A-COMP-PILOT, $9k on A-PREVENTIVE (Ridgeline), $6k on A-INSPECT (5 units), and $71,000 PRESERVED via A-HOLD.
Question: ${query}`;

      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${key}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
      });
      const data = await res.json();
      const text = data.candidates[0].content.parts[0].text;
      responseBox.innerHTML = `<strong>Gemini 1.5 Flash:</strong> ${text.replace(/\\n/g, '<br>')}`;
    } catch (err) {
      responseBox.innerHTML = `<strong>AI Fallback Analyst:</strong> ${matchQuery(query)}`;
    }
  } else {
    setTimeout(() => {
      responseBox.innerHTML = `<strong>AI Operations Analyst:</strong> ${matchQuery(query)}`;
    }, 400);
  }
});

function matchQuery(q) {
  const l = q.toLowerCase();
  if (l.includes('1158') || l.includes('replace') || l.includes('bottom 10')) return KB.m1158;
  if (l.includes('downtime') || l.includes('fault') || l.includes('ridgeline') || l.includes('repair')) return KB.downtime;
  if (l.includes('comp') || l.includes('points') || l.includes('loyalty') || l.includes('reinvest')) return KB.comps;
  if (l.includes('budget') || l.includes('100') || l.includes('action') || l.includes('spend')) return KB.budget;
  if (l.includes('player') || l.includes('local') || l.includes('concentration') || l.includes('gini')) return KB.concentration;
  return "Based on 181 gaming days of telemetry, the floor is fundamentally sound (9.50% hold, $248.9M coin-in). High-priority operational risks cluster in Ridgeline mechanical downtime (56.3% of faults) and loyalty under-comping (1.23% reinvestment). We recommend deploying $29,000 on targeted fixes while preserving $71,000 in capital agility.";
}

// Theme Toggle
document.getElementById('theme-toggle').addEventListener('click', () => {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
});
</script>
</body>
</html>
"""

out_file = Path("dashboard/index.html")
out_file.write_text(html_content, encoding="utf-8")
print(f"Generated {out_file} with AI Casino Analyst! Size: {len(html_content):,} bytes")
