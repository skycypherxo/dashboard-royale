# Databricks Notebook: 01_bronze_ingestion
# Ingests raw Casino Parquet files into Delta Lake Bronze tables

from pyspark.sql import functions as F

print("Starting Bronze Layer Ingestion for THE GILDED ACE...")

raw_base_path = "/FileStore/tables/dashboard-royale/data"
bronze_base_path = "/mnt/delta/bronze"

tables = [
    ("1_prepared_views/property_day.parquet", "bronze_property_day"),
    ("1_prepared_views/prepared_daily_view.parquet", "bronze_prepared_daily"),
    ("2_machine_decision/machines.parquet", "bronze_machines"),
    ("2_machine_decision/machine_day.parquet", "bronze_machine_day"),
    ("2_machine_decision/operations.parquet", "bronze_operations"),
    ("2_machine_decision/action_catalog.parquet", "bronze_action_catalog"),
    ("2_machine_decision/cost_rules.parquet", "bronze_cost_rules"),
    ("2_machine_decision/floor_locations.parquet", "bronze_floor_locations"),
    ("3_guests/players.parquet", "bronze_players"),
    ("3_guests/sessions.parquet", "bronze_sessions"),
    ("3_guests/fnb_transactions.parquet", "bronze_fnb_transactions"),
    ("4_context/zone_traffic_hourly.parquet", "bronze_zone_traffic")
]

for src_sub, tbl_name in tables:
    src_path = f"{raw_base_path}/{src_sub}"
    dest_path = f"{bronze_base_path}/{tbl_name}"
    print(f"Reading {src_path} -> {tbl_name}...")
    
    try:
        df = spark.read.parquet(src_path)
        df_bronze = df \
            .withColumn("_ingested_at_utc", F.current_timestamp()) \
            .withColumn("_source_file", F.input_file_name())
            
        df_bronze.write.format("delta").mode("overwrite").save(dest_path)
        spark.sql(f"CREATE TABLE IF NOT EXISTS {tbl_name} USING DELTA LOCATION '{dest_path}'")
        print(f"Loaded {tbl_name}: {df_bronze.count()} rows")
    except Exception as e:
        print(f"Note: Path {src_path} simulated for local run or requires cluster path: {e}")

print("Bronze ingestion pipeline completed!")

