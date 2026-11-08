# The Gilded Ace · Casino Decision Intelligence Platform

> **CASINO DECISION INTELLIGENCE PLATFORM · JAN–JUN 2025**  
> Total House Win: **$23,638,155** | Machine Availability: **99.62%** | Theoretical House Win: **$23,545,364** | Budget: **$100K**

A production-grade, multi-page decision intelligence platform built for TAMU Datathon 2026. Rather than relying on intuition or replacing machines based on naive house win, **The Gilded Ace** implements a closed decision loop:  
**Observe ➔ Investigate ➔ Predict ➔ Decide ➔ Measure**

---

## 1. Quick Start & Environment Configuration

### Step A: Configure Environment Variables (`.env`)
The platform supports live credentials for **Google Gemini**, **xAI Grok**, **MongoDB Atlas**, and **Databricks SQL Warehouse**.

A ready-to-use template is provided in [`.env.example`](.env.example). Copy it to `.env`:

```powershell
cp .env.example .env
```

Edit `.env` with your API keys or database connections:

```ini
# Server Port & Host
PORT=8000
HOST=127.0.0.1

# AI Copilot APIs (Optional - falls back to pre-computed verified decision responses if not provided)
GEMINI_API_KEY=your_gemini_api_key_here
XAI_API_KEY=your_xai_api_key_here

# MongoDB Atlas (Optional - falls back to persistent local store in data/mongo_atlas_store.json)
# Purpose: Dynamic investigation records, auditor notes, and saved simulation portfolios
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=gilded_ace_intelligence

# Databricks SQL Warehouse (Optional - falls back to embedded SQL Delta store in data/the_gilded_ace.db)
# Purpose: Columnar OLAP engine for Gold feature tables, gaming day aggregations, and MLflow models
DATABRICKS_SERVER_HOSTNAME=your_databricks_host
DATABRICKS_HTTP_PATH=your_http_path
DATABRICKS_TOKEN=your_token
```

> **Zero-Config Guarantee:** If no API keys or cloud database connections are configured, the backend automatically uses its embedded, zero-dependency engines:
> - **Databricks SQL Engine:** Direct SQL execution on local Gold/Silver Delta store (`data/the_gilded_ace.db`) covering 56,110 gaming records, 30,401 sensor logs, and player telemetry.
> - **MongoDB Atlas Engine:** Audit case tracking, analyst notes, and scenario persistence stored locally in `data/mongo_atlas_store.json`.
> - **Gemini & Grok AI Engine:** Deterministic, contract-verified answers grounded in actual telemetry and analytical findings.

### Step B: Launch the Platform

Run the unified backend server:

```powershell
python run_platform.py
```

- **Interactive Decision Platform:** [http://localhost:8000/dashboard/index.html](http://localhost:8000/dashboard/index.html)
- **FastAPI Interactive Docs & Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)

*Note: All HTML files in `dashboard/` can also be opened directly in any browser for static offline review.*

---

## 2. Dynamic Backend Data Architecture vs Hardcoding

All 8 dashboard pages are dynamically wired to real REST and database endpoints:

1. **Global Period Filtering (`GET /api/metrics/summary?period=all|last_3m|june_only`):**
   - Switching the time-window selector in the header instantly re-computes Floor Win, Theoretical Win, Availability, and Hold % across 181 gaming days in real-time.
2. **Dynamic Machine Drill-Down & 6-Question Audit (`GET /api/machines/{machine_id}/audit`):**
   - Clicking any machine in `dashboard/machine_intelligence.html` triggers a dynamic backend calculation of coin-in rank, theoretical hold deficit, $Z$-score, $p$-value, availability, and alternative intervention savings.
3. **MongoDB Atlas Audit Logging (`POST /api/audit/case` & `GET /api/audit/cases`):**
   - Analysts can create, flag, and commit audit cases with custom notes and recommended actions directly into the MongoDB Atlas investigation collection.
4. **Interactive Databricks SQL Console (`GET /api/databricks/query?sql=...`):**
   - In `dashboard/evidence_explorer.html`, users can write and execute arbitrary SQL queries against the Gold and Silver tables, receiving live JSON datasets and row counts.
5. **Interactive $100K Intervention Simulator (`POST /api/optimizer/simulate`):**
   - Sending action combinations validates the 5 hard constraints ($100k cap, max 3 action types, stock limits, incompatible actions) and runs Monte Carlo sensitivity simulations (+35% optimistic, expected, -30% pessimistic).
6. **Interactive SQL & Telemetry via Databricks Delta Lake (`GET /api/databricks/query?sql=...`):**
   - Direct SQL querying over `gold_zone_traffic` (30,401 rows), `gold_players` (113,890 rows), and `gold_machine_scorecard` (310 machines).
7. **Dual-AI Copilot (`POST /api/ai/chat`):**
   - Switch between **Gemini 1.5 Flash** (decision intelligence copilot) and **xAI Grok** (adversarial fraud and red-teaming auditor).

---

## 2. Multi-Page Decision Platform Structure

| Page | File | What the Judge Sees |
|---|---|---|
| **1. Floor overview** | [`dashboard/floor_overview.html`](dashboard/floor_overview.html) | Revenue velocity, daily hold trends, 7-zone comparisons, foot traffic vs occupancy. |
| **2. Machine intelligence** | [`dashboard/machine_intelligence.html`](dashboard/machine_intelligence.html) | 310-machine scorecard, risk-adjusted rankings, and interactive **6-Question Decision Audit**. |
| **3. Demand analytics** | [`dashboard/demand_analytics.html`](dashboard/demand_analytics.html) | Wagering traffic, events, day-of-week seasonality, and **out-of-sample ML forecasting** (68.52% error cut). |
| **4. Operations** | [`dashboard/operations.html`](dashboard/operations.html) | Downtime by manufacturer (**56.34% Ridgeline**), **Swing Shift technician bottleneck (47.8% faults)**, MTTR. |
| **5. Guest intelligence** | [`dashboard/guest_intelligence.html`](dashboard/guest_intelligence.html) | Player concentration (top 5% = 55.33% coin-in, **Gini 0.754**), comp reinvestment rate (**1.23%**), **27.93% F&B COGS ratio**. |
| **6. Budget optimizer** | [`dashboard/budget_optimizer.html`](dashboard/budget_optimizer.html) | **Mode 1 Manual Simulator** + **Mode 2 Recommendation Engine** enforcing $100k cap, max 3 action types, limits, and lead times. |
| **7. Gemini copilot** | [`dashboard/gemini_copilot.html`](dashboard/gemini_copilot.html) | Natural-language decision investigation grounded in analytical tables with tool calling and live Gemini API key integration. |
| **8. Evidence explorer** | [`dashboard/evidence_explorer.html`](dashboard/evidence_explorer.html) | Searchable claims matrix with exact SQL queries, empirical metrics, alternative explanations, and limitations. |

---

## 3. Machine Intelligence & The 6-Question Decision Audit

When the judge clicks on any machine (such as **M-1158**), the platform opens the **6-Question Decision Audit**:

1. **Why was it flagged?**  
   *M-1158 flagged at Rank #2 lowest raw win ($15,796) out of 310 machines.*
2. **Whether its losses are statistically unusual?**  
   *YES: It is an established player favorite with **$519,610 in coin-in** (top 15% floor volume). The -$36,165 shortfall yields **$Z = -20.21$ ($p < 0.0001$)**, confirming statistical luck variance, NOT poor appeal.*
3. **Whether downtime explains its performance?**  
   *NO: Achieved **99.93% availability** (only 3.0h offline).*
4. **Whether it has a location problem?**  
   *Located in Back Forty but commands high coin-in despite lower zone traffic.*
5. **Whether replacement is economically justified?**  
   *NO: Purchasing a replacement costs **$22,000** and has negative payback.*
6. **Which alternative intervention is cheaper?**  
   *Deploy **`A-INSPECT` ($1,200)** to audit ROM chips and meters, **saving $20,800** compared to replacement.*

---

## 4. The $100K Budget Optimizer

Strictly enforces all 5 formal constraints:
- Total expenditure $\le \$100,000$.
- Maximum of 3 distinct action types.
- Catalog quantity limits.
- Lead times and downtime hours.
- Incompatibility rules (`same_machine` and `comp_policy`).

### Two Operating Modes:
- **Mode 1: Manual Planning Simulator:** Sliders and counters for all 13 catalogue actions with real-time constraint validation, downtime tracking, and Monte Carlo sensitivity testing (-30% pessimistic, expected, +35% optimistic).
- **Mode 2: Recommendation Engine:** Pre-evaluated, evidence-grounded portfolios:
  1. **Recommended Strategic Portfolio:** `A-COMP-PILOT` ($14,000) + `A-PREVENTIVE` ($9,000) + `A-INSPECT` ($6,000) + `A-HOLD` ($71,000 cash). **Net annual gain: +$153,400 | Payback: 1.9 months**.
  2. **Operations Reliability Package:** `A-TECH-SHIFT` ($11,520) + `A-PREVENTIVE` ($9,000) + `A-INSPECT` ($6,000) + `A-HOLD` ($73,480).
  3. **Zone Revitalization Package:** `A-MOVE-BANK` ($9,500) + `A-WAYFINDING` ($7,500) + `A-COMP-PILOT` ($14,000) + `A-HOLD` ($69,000).

---

## 5. Databricks & Delta Lake Medallion Pipeline

Scripts located in [`work/databricks/`](work/databricks/):
- **`01_bronze_ingestion.py`**: Raw parquet ingestion into append-only Delta Lake tables with audit metadata.
- **`02_silver_transformations.py`**: Off-floor filtering (`location_id IS NOT NULL`), gaming-day alignment (06:00 to 06:00), and shift tagging.
- **`03_gold_feature_store.py`**: Aggregates `gold_machine_scorecard`, `gold_operations_mfg`, and `gold_operations_shift`.
- **`04_mlflow_demand_forecasting.py`**: MLflow experiment tracking comparing Baseline Constant Mean (MAE **$218,258.10**) vs Weekday Stratified ML Model (MAE **$68,698.55**), logging parameters, metrics, and registered models.

---

## 6. Deployment on Vultr / Cloud

To deploy on a Vultr Cloud Compute instance (Ubuntu 22.04 LTS):

```bash
# 1. Clone repository
git clone https://github.com/potiv/dashboard-royale.git
cd dashboard-royale

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Run FastAPI backend with Uvicorn
uvicorn backend.main:app --host 0.0.0.0 --port 80
```

Configure your GoDaddy / custom domain DNS to point an `A` record to your Vultr server public IP.
