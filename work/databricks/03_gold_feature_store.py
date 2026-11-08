# Databricks Notebook: 03_gold_feature_store
# Aggregates decision-support Gold tables for Floor, Machines, Demand, and Guest Intelligence

from pyspark.sql import functions as F
from pyspark.sql.window import Window

print("Building Gold Feature Tables for THE GILDED ACE...")

silver_base = "/mnt/delta/silver"
gold_base = "/mnt/delta/gold"

# 1. GOLD MACHINE SCORECARD (310 UNITS)
# Ranks machines by naive house win and true theoretical hold per available hour
silver_m = spark.read.format("delta").load(f"{silver_base}/silver_active_machine_day")

gold_scorecard = silver_m.groupBy("machine_id", "theme", "manufacturer", "zone_name").agg(
    F.sum("coin_in_usd").alias("coin_in_usd"),
    F.sum("payout_usd").alias("payout_usd"),
    F.sum("house_win_usd").alias("house_win_usd"),
    F.sum("theo_usd").alias("theo_usd"),
    F.sum("available_hours").alias("available_hours"),
    F.sum("occupied_hours").alias("occupied_hours"),
    F.sum("paid_spins").alias("paid_spins"),
    F.sum("faults_opened").alias("faults_opened")
) \
.withColumn("luck_residual_usd", F.col("house_win_usd") - F.col("theo_usd")) \
.withColumn("observed_hold_pct", (F.col("house_win_usd") / F.col("coin_in_usd")) * 100.0) \
.withColumn("theo_hold_pct", (F.col("theo_usd") / F.col("coin_in_usd")) * 100.0) \
.withColumn("theo_per_avail_hour", F.col("theo_usd") / F.col("available_hours")) \
.withColumn("occupancy_ratio", F.col("occupied_hours") / F.col("available_hours")) \
.withColumn("rank_naive_house_win", F.rank().over(Window.orderBy(F.asc("house_win_usd")))) \
.withColumn("rank_true_theo_hour", F.rank().over(Window.orderBy(F.asc("theo_per_avail_hour"))))

gold_scorecard.write.format("delta").mode("overwrite").save(f"{gold_base}/gold_machine_scorecard")
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_machine_scorecard USING DELTA LOCATION '{gold_base}/gold_machine_scorecard'")

# 2. GOLD OPERATIONS & DOWNTIME SUMMARY
silver_ops = spark.read.format("delta").load(f"{silver_base}/silver_clean_operations")

gold_ops_mfg = silver_ops.groupBy("manufacturer").agg(
    F.count("operation_id").alias("fault_count"),
    F.sum("duration_hours").alias("total_downtime_hours"),
    F.avg("duration_hours").alias("mean_turnaround_hours")
)
gold_ops_mfg.write.format("delta").mode("overwrite").save(f"{gold_base}/gold_operations_mfg")

gold_ops_shift = silver_ops.groupBy("shift").agg(
    F.count("operation_id").alias("fault_count"),
    F.sum("duration_hours").alias("total_downtime_hours"),
    F.avg("duration_hours").alias("mean_turnaround_hours")
)
gold_ops_shift.write.format("delta").mode("overwrite").save(f"{gold_base}/gold_operations_shift")

print("Gold feature tables built and persisted to Delta Lake!")

