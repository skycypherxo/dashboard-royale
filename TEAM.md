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
                                  └──────┬────────┬───────┬─────┘
                                         │        │       │
            ┌────────────────────────────┘        │       └──────────────────────────┐
            ▼                                     ▼                                  ▼
┌──────────────────────────┐         ┌─────────────────────────┐        ┌───────────────────────────┐
│     DATABRICKS LAKEHOUSE │         │      MONGODB ATLAS      │        │    TIGERDATA / TIMESCALE  │
│  (Bronze / Silver / Gold)│         │   (Investigation Store) │        │     (Time-Series Engine)  │
├──────────────────────────┤         ├─────────────────────────┤        ├───────────────────────────┤
│ • Spark medallion ETL    │         │ • Machine audit logs    │        │ • High-freq sensor counts │
│ • Parquet/Delta storage  │         │ • Analyst flag overrides│        │ • 1.32M hourly spin rows  │
│ • MLflow model registry  │         │ • Custom $100K scenarios│        │ • Downtime interval spans │
│ • True theo aggregations │         │ • AI conversation states│        │ • Hypertable time_bucket  │
└──────────────────────────┘         └─────────────────────────┘        └───────────────────────────┘
```

---

## 2. Multi-Database Storage Matrix

| Database System | Primary Purpose | Datasets & Tables Managed | Query Mechanism |
|---|---|---|---|
| **Databricks Delta Lake** | **Analytical Foundation & Medallion Storage** | `bronze_prepared_daily`, `silver_active_machine_day`, `gold_machine_scorecard` (310 machines), `gold_operations_mfg`, MLflow experiments. | Spark SQL, Delta Lake parquet engine, MLflow Client. |
| **MongoDB Atlas** | **Audit Trail & Investigation Store** | `audit_cases` (flags, ROM check records), `simulation_scenarios` (custom portfolios), analyst review notes. | MongoDB Atlas BSON/JSON document store. |
| **TigerData / Timescale (TigerDB)** | **High-Frequency Time-Series & Telemetry** | `zone_traffic_hourly` (30,401 rows), `machine_hour` (1,321,908 rows), downtime timestamps. | Hypertable window queries (`time_bucket`), ZSTD compression. |

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
