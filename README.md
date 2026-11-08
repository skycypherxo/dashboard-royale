# The Gilded Ace · Casino Decision Intelligence Platform

> **CASINO DECISION INTELLIGENCE PLATFORM · JAN–JUN 2025**  
> Total House Win: **$23,638,155** | Machine Availability: **99.62%** | Theoretical House Win: **$23,545,364** | Budget: **$100K**

A production-grade, multi-page decision intelligence platform built for TAMU Datathon 2026. Rather than relying on intuition or replacing machines based on naive house win, **The Gilded Ace** implements a closed decision loop:  
**Observe ➔ Investigate ➔ Predict ➔ Decide ➔ Measure**

---

## 1. Quick Start: Launch the Platform

Run the unified backend and launch the platform in your browser with a single command:

```powershell
python run_platform.py
```

- **Interactive Decision Platform:** [http://localhost:8000/dashboard/index.html](http://localhost:8000/dashboard/index.html)
- **FastAPI Interactive Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

*Note: You can also open any of the HTML files in `dashboard/` directly in any web browser without running a server.*

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
