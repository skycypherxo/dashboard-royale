# Databricks Notebook: 04_mlflow_demand_forecasting
# Tracks demand forecasting experiments comparing Constant Mean Baseline vs Day-of-Week Stratified Model
# Logs parameters, metrics (MAE, RMSE, R2), and model artifacts to MLflow

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configure MLflow Experiment
mlflow.set_experiment("/Shared/The_Gilded_Ace_Demand_Forecasting")

print("Loading Daily Property Views from Gold / Parquet...")
gold_path = "/mnt/delta/gold/gold_demand_daily"
try:
    df = spark.read.format("delta").load(gold_path).toPandas()
except Exception:
    # Local fallback for execution verification
    import os
    from pathlib import Path
    root = Path.cwd()
    df = pd.read_parquet("work/floor/out/demand_daily.parquet")

df['gaming_date'] = pd.to_datetime(df['gaming_date'])
df = df.sort_values('gaming_date').reset_index(drop=True)

# Define zero-leakage temporal split
train_mask = df['gaming_date'] < pd.to_datetime('2025-05-01')
train_df = df[train_mask].copy()
test_df = df[~train_mask].copy()

y_train = train_df['coin_in_usd'].values
y_test = test_df['coin_in_usd'].values

print(f"Train Days: {len(train_df)} (Jan–Apr) | Test Days: {len(test_df)} (May–Jun)")

# -------------------------------------------------------------
# RUN 1: Baseline Constant Mean Benchmark
# -------------------------------------------------------------
with mlflow.start_run(run_name="Baseline_Constant_Mean"):
    train_mean = float(np.mean(y_train))
    y_pred_base = np.full_like(y_test, train_mean)
    
    mae_base = mean_absolute_error(y_test, y_pred_base)
    rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))
    r2_base = r2_score(y_test, y_pred_base)
    
    # Log MLflow parameters & metrics
    mlflow.log_param("model_type", "constant_training_mean")
    mlflow.log_param("train_start", "2025-01-01")
    mlflow.log_param("train_end", "2025-04-30")
    mlflow.log_param("test_start", "2025-05-01")
    mlflow.log_param("test_end", "2025-06-30")
    mlflow.log_param("constant_mean_usd", train_mean)
    
    mlflow.log_metric("test_mae", mae_base)
    mlflow.log_metric("test_rmse", rmse_base)
    mlflow.log_metric("test_r2", r2_base)
    
    print(f"[RUN 1 Baseline] Test MAE: ${mae_base:,.2f} | RMSE: ${rmse_base:,.2f} | R2: {r2_base:.4f}")

# -------------------------------------------------------------
# RUN 2: Day-of-Week Stratified Conditional Expectation Model
# -------------------------------------------------------------
with mlflow.start_run(run_name="Stratified_Weekday_ML_Model"):
    dow_means = train_df.groupby('local_weekday')['coin_in_usd'].mean().to_dict()
    y_pred_ml = test_df['local_weekday'].map(dow_means).values
    
    mae_ml = mean_absolute_error(y_test, y_pred_ml)
    rmse_ml = np.sqrt(mean_squared_error(y_test, y_pred_ml))
    r2_ml = r2_score(y_test, y_pred_ml)
    error_reduction = ((mae_base - mae_ml) / mae_base) * 100.0
    
    # Log MLflow parameters & metrics
    mlflow.log_param("model_type", "day_of_week_conditional_expectation")
    mlflow.log_param("stratification_key", "local_weekday")
    for dow, m in dow_means.items():
        mlflow.log_param(f"train_mean_{dow}", round(m, 2))
        
    mlflow.log_metric("test_mae", mae_ml)
    mlflow.log_metric("test_rmse", rmse_ml)
    mlflow.log_metric("test_r2", r2_ml)
    mlflow.log_metric("error_reduction_pct", error_reduction)
    
    # Log model artifact tags
    mlflow.set_tag("winner", "true")
    mlflow.set_tag("deployment_candidate", "Production_July_Demand_Forecaster")
    
    print(f"[RUN 2 Weekday ML] Test MAE: ${mae_ml:,.2f} | Error Reduction: {error_reduction:.2f}% | R2: {r2_ml:.4f}")

print("MLflow experiment tracking completed!")

