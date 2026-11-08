# Team Architecture & Unified System Specifications

**Project:** THE GILDED ACE · Casino Decision Intelligence Platform  
**Architecture:** Multi-Database Polyglot Persistence + Dual AI Engine (Gemini & Grok)  
**Status:** Unified Production Architecture  

---

## 1. Unified Architecture & Database Division of Labor

Instead of a fragmented manual split, the platform integrates specialized database engines where each handles what it was built for, with zero hardcoding:

```
                                  ┌─────────────────────────────┐
                                  │      THE GILDED ACE         │
                                  │  Executive Decision UI (8p) │
                                  └──────────────┬──────────────┘
                                                 │
                                                 ▼
                                  ┌─────────────────────────────┐
                                  │   FastAPI Backend Engine    │
                                  │   (Real-time Dynamic Calc)  │
                                  └──────┬───────────────┬──────┘
                                         │               │
            ┌────────────────────────────┘               └──────────────────────────┐
            ▼                                                                       ▼
┌──────────────────────────────────────┐                   ┌────────────────────────────────────────┐
│     DATABRICKS DELTA LAKE            │                   │             MONGODB ATLAS              │
│  (Analytical Warehouse & Medallion)  │                   │         (Investigation Store)          │
├──────────────────────────────────────┤                   ├────────────────────────────────────────┤
│ • Spark medallion ETL (Bronze/Silver/│                   │ • Machine audit investigation records  │
│   Gold)                              │                   │ • Analyst flag overrides & memos       │
│ • Parquet/Delta columnar storage     │                   │ • Custom $100K optimizer portfolios    │
│ • MLflow demand model registry       │                   │ • Dynamic scenario persistence         │
│ • High-performance analytical SQL    │                   │ • AI red-team conversation states      │
│ • 30,401 sensor traffic logs         │                   │ • Flexible JSON document schema        │
└──────────────────────────────────────┘                   └────────────────────────────────────────┘
```

---

## 2. Multi-Database Architecture: Why Databricks & MongoDB?

We deliberately selected and paired two industry-leading databases to match their native strengths:

| Database System | Primary Purpose | Why This Database? | Datasets & Tables Managed |
|---|---|---|---|
| **Databricks Delta Lake** | **Analytical Foundation, Feature Store & MLflow** | Columnar OLAP engine optimized for high-throughput scans, complex group-bys, gaming-day aggregations (06:00 to 06:00), theoretical hold variance, and machine ranking across 56,110 daily records and 30,401 sensor logs. Provides ACID guarantees, schema enforcement, and integrated MLflow experiment tracking. | `gold_machine_scorecard` (310 machines), `gold_demand_daily` (181 days), `gold_zone_traffic` (30,401 records), `gold_players` (113,890 records), `gold_fnb_transactions` (227,833 records), `silver_clean_operations` (1,226 events), MLflow model artifacts. |
| **MongoDB Atlas** | **Auditor Investigation Store & Scenario State** | Document database designed for flexible, semi-structured operational data. Audit investigations require rapid schema agility: notes, analyst verdicts, ROM inspection tags, flag overrides, and custom user-built $100K intervention scenarios cannot fit into rigid relational tables without frequent schema migrations. | `audit_cases` (flag records, inspection authorizations, engineer notes), `simulation_scenarios` (custom portfolios saved by executives), `auditor_overrides`. |

---

## 3. Dynamic Data Pipeline (No Hardcoding)

Data flows dynamically from the database tier straight to the UI:
1. **Direct Database Loads:** The backend engine reads directly from the Databricks Delta Lake SQL database (`gold_prepared_daily_view`, `gold_daily_property`, `gold_players`, `gold_zone_traffic`).
2. **On-the-Fly Aggregations:** Period filtering (`all`, `last_3m`, `june_only`) calculates house win, theoretical hold, and uptime dynamically without pre-baked static numbers.
3. **Investigation Workflow:** When an auditor flags a machine or overrides a replacement recommendation, the state is persisted into MongoDB Atlas in real time.

---

## 3. Dual-AI Cognitive Engine: Gemini vs. Grok

The platform implements two complementary AI engines serving distinct operational roles:

### 1. Google Gemini (Executive Decision Copilot)
- **Role:** Chief Analytics Officer & Strategy Justifier.
- **Purpose:** 
  - Grounded telemetry explanations connecting data to decisions.
  - Explains why naively underperforming machines (e.g., M-1158) should be retained.
  - Generates executive ROI justifications and board-ready capital expenditure memos.
- **Integration:** Google Gemini 1.5/2.0 API with backend tool calling and database grounding.

### 2. xAI Grok (Adversarial Floor Auditor & Devil's Advocate)
- **Role:** Red-Team Risk Analyst & Casino Fraud Auditor.
- **Purpose:**
  - Pokes holes in executive assumptions (e.g., *"Is M-1158's Z = -20.21 really luck, or a syndicated PRNG exploit?"*).
  - Stress-tests comp reinvestment against guest cannibalization and restaurant kitchen capacity bottlenecks.
  - Questions vendor motives (e.g., Ridgeline's 56.34% fault rate and swing shift overtime billing).
- **Integration:** Grok API / Adversarial Red-Team Engine.

---

## 4. Multi-Page Decision Platform (8 Dedicated Pages)

All pages are dynamically served, support period filtering (`Jan–Jun`, `Apr–Jun`, `Jun-only`), and drill into individual units:

1. **Floor overview** (`dashboard/floor_overview.html`): Daily revenue velocity, observed hold vs theoretical hold, 7-zone matrix, foot traffic vs occupancy.
2. **Machine intelligence** (`dashboard/machine_intelligence.html`): 310-machine scorecard, risk-adjusted rankings, and interactive **6-Question Decision Audit** (Why flagged, statistical luck test, downtime factor, location problem, replacement justification, cheaper alternatives).
3. **Demand analytics** (`dashboard/demand_analytics.html`): Traffic, events, day-of-week seasonality (Saturday $1.82M vs Tuesday $1.11M), out-of-sample forward ML evaluation (**68.52% error cut**).
4. **Operations** (`dashboard/operations.html`): 1,207 fault events, Ridgeline 56.34% concentration, Swing shift 47.8% bottleneck, MTTR turnaround.
5. **Guest intelligence** (`dashboard/guest_intelligence.html`): Top 5% generates 55.33% coin-in (Gini 0.754), 1.23% comp reinvestment, 27.93% F&B COGS leverage, local VIPs.
6. **Budget optimizer** (`dashboard/budget_optimizer.html`): **Mode 1 Manual Simulator** (checks ≤$100k, max 3 action types, limits, lead times, downtime, incompatibilities) + **Mode 2 Recommendation Engine** (Top 3 ranked portfolios).
7. **Gemini & Grok copilot** (`dashboard/gemini_copilot.html`): Natural language decision investigation with instant toggle between Gemini (Executive Copilot) and Grok (Adversarial Auditor).
8. **Evidence explorer** (`dashboard/evidence_explorer.html`): Filterable claims ledger with source queries, empirical results, alternative explanations, and limitations.

---

## 5. Execution Command

To run the unified backend with all database clients and the multi-page platform:

```powershell
python run_platform.py
```
