# Databricks Architecture & Delta Lake Pipeline

This directory contains the production Databricks & Delta Lake engineering pipeline for **THE GILDED ACE** decision intelligence platform.

---

## 1. Medallion Architecture Overview

```
Raw Parquet Data
      │
      ▼
[ Bronze Layer ]   (01_bronze_ingestion.py)
  • Raw append-only Delta Lake tables with audit metadata (_ingested_at, _source_file).
  • Tables: bronze_machine_day, bronze_property_day, bronze_operations, bronze_players, etc.
      │
      ▼
[ Silver Layer ]   (02_silver_transformations.py)
  • Data cleaning, schema enforcement, gaming-day alignment (06:00 to 06:00 local time).
  • Excludes off-floor records (location_id IS NOT NULL).
  • Standardizes accounting metrics (house_win, theo_win, luck_residual, comp_cogs).
  • Tables: silver_active_machine_day, silver_clean_operations, silver_fnb_comps.
      │
      ▼
[ Gold Layer ]     (03_gold_feature_store.py)
  • Business-level analytical aggregations and feature store.
  • Tables: gold_machine_scorecard (310 machines), gold_operations_mfg, gold_operations_shift.
      │
      ▼
[ MLflow Experiments ] (04_mlflow_demand_forecasting.py)
  • Tracks out-of-sample forward evaluation (Jan–Apr Train vs May–Jun Test).
  • Baseline Constant Mean MAE: $218,258.10.
  • Stratified Day-of-Week Conditional Model MAE: $68,698.55 (68.52% error reduction).
  • Registers winner: `Production_July_Demand_Forecaster`.
```

---

## 2. Notebook Execution Order

1. **`01_bronze_ingestion.py`**:
   - Ingests raw data files into Delta tables.
   - Enforces schema and appends tracking metadata.
2. **`02_silver_transformations.py`**:
   - Cleans timestamps and applies business filters.
   - Tags shifts (`Day`, `Swing`, `Graveyard`) and resolves manufacturer codes.
3. **`03_gold_feature_store.py`**:
   - Calculates risk-adjusted rankings, true theo hold per available hour, and downtime aggregations.
4. **`04_mlflow_demand_forecasting.py`**:
   - Runs model training and logs metrics, parameters, and tags directly to MLflow.

---

## 3. How to Run in Databricks

1. Log into your Databricks Workspace (Community Edition or Enterprise).
2. Go to **Workspace** -> **Import** -> Select the `work/databricks/` folder.
3. Attach to a cluster with **Databricks Runtime 14.3+ LTS ML** (includes PySpark, Delta Lake, and MLflow).
4. Run the notebooks sequentially (`01` -> `02` -> `03` -> `04`).

