# Databricks Notebook: 02_silver_transformations
# Data cleaning, gaming-day boundary handling, active floor filtering, and accounting validations

from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, IntegerType

print("Executing Silver Layer Transformations...")

bronze_base = "/mnt/delta/bronze"
silver_base = "/mnt/delta/silver"

# 1. SILVER ACTIVE MACHINES DAILY
# Filter off-floor machines (location_id IS NOT NULL) and enforce accounting conventions
prep_df = spark.read.format("delta").load(f"{bronze_base}/bronze_prepared_daily")

silver_machine_daily = prep_df \
    .filter(F.col("location_id").isNotNull()) \
    .withColumn("coin_in_usd", F.col("coin_in_usd").cast(DoubleType())) \
    .withColumn("payout_usd", F.col("payout_usd").cast(DoubleType())) \
    .withColumn("house_win_usd", F.col("house_win_usd").cast(DoubleType())) \
    .withColumn("theo_usd", F.col("theo_usd").cast(DoubleType())) \
    .withColumn("luck_residual_usd", F.col("house_win_usd") - F.col("theo_usd")) \
    .withColumn("observed_hold_pct", F.when(F.col("coin_in_usd") > 0, (F.col("house_win_usd") / F.col("coin_in_usd")) * 100.0).otherwise(0.0))

silver_machine_daily.write.format("delta").mode("overwrite").save(f"{silver_base}/silver_active_machine_day")
spark.sql(f"CREATE TABLE IF NOT EXISTS silver_active_machine_day USING DELTA LOCATION '{silver_base}/silver_active_machine_day'")

# 2. SILVER OPERATIONS & SHIFT BOTTLENECK
# Calculate repair durations and tag operational shifts
ops_df = spark.read.format("delta").load(f"{bronze_base}/bronze_operations")
mach_df = spark.read.format("delta").load(f"{bronze_base}/bronze_machines")

silver_ops = ops_df \
    .filter(F.col("event_type") == "fault_repair") \
    .withColumn("duration_seconds", F.unix_timestamp("available_at_utc") - F.unix_timestamp("opened_at_utc")) \
    .withColumn("duration_hours", F.col("duration_seconds") / 3600.0) \
    .withColumn("local_hour", F.hour(F.col("opened_at_local"))) \
    .withColumn("shift", 
        F.when((F.col("local_hour") >= 6) & (F.col("local_hour") < 14), "Day")
         .when((F.col("local_hour") >= 14) & (F.col("local_hour") < 22), "Swing")
         .otherwise("Graveyard")
    ) \
    .join(mach_df.select("machine_id", "manufacturer", "theme"), on="machine_id", how="left")

silver_ops.write.format("delta").mode("overwrite").save(f"{silver_base}/silver_clean_operations")
spark.sql(f"CREATE TABLE IF NOT EXISTS silver_clean_operations USING DELTA LOCATION '{silver_base}/silver_clean_operations'")

# 3. SILVER COMP & F&B TRANSACTIONS
# Separate comped food & beverage from direct cash sales, computing true COGS economic costs
fnb_df = spark.read.format("delta").load(f"{bronze_base}/bronze_fnb_transactions")

silver_comps = fnb_df \
    .filter(F.col("comp_id").isNotNull()) \
    .withColumn("face_value_usd", F.col("face_value_cents") / 100.0) \
    .withColumn("cogs_usd", F.col("cogs_cents") / 100.0) \
    .withColumn("cogs_ratio", F.col("cogs_usd") / F.col("face_value_usd"))

silver_comps.write.format("delta").mode("overwrite").save(f"{silver_base}/silver_fnb_comps")
spark.sql(f"CREATE TABLE IF NOT EXISTS silver_fnb_comps USING DELTA LOCATION '{silver_base}/silver_fnb_comps'")

print("Silver transformations completed successfully!")

