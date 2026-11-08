import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

host = os.environ.get('DATABRICKS_SERVER_HOSTNAME')
token = os.environ.get('DATABRICKS_TOKEN') or os.environ.get('DATABRICKS_ACCESS_TOKEN')
http_path = os.environ.get('DATABRICKS_HTTP_PATH')

from databricks import sql

print('Connecting to Databricks...')
with sql.connect(server_hostname=host, http_path=http_path, access_token=token) as conn:
    with conn.cursor() as cur:
        print('Creating and uploading gold_demand_daily...')
        df_dem = pd.read_parquet('work/floor/out/demand_daily.parquet')
        cur.execute('''
            CREATE OR REPLACE TABLE default.gold_demand_daily (
                gaming_date STRING,
                local_weekday STRING,
                events_active STRING,
                active_machines INT,
                coin_in_usd DOUBLE,
                payout_usd DOUBLE,
                house_win_usd DOUBLE,
                theo_usd DOUBLE,
                observed_hold DOUBLE,
                is_train BOOLEAN,
                pred_baseline_coin DOUBLE,
                pred_weekday_coin DOUBLE
            ) USING DELTA;
        ''')
        rows = []
        for _, r in df_dem.iterrows():
            evt = str(r.get('events_active', '')).replace("'", "''")
            g_date = str(r['gaming_date'])[:10]
            rows.append(f"('{g_date}', '{r['local_weekday']}', '{evt}', {int(r['active_machines'])}, {float(r['coin_in_usd'])}, {float(r['payout_usd'])}, {float(r['house_win_usd'])}, {float(r['theo_usd'])}, {float(r['observed_hold'])}, {str(bool(r['is_train'])).lower()}, {float(r['pred_baseline_coin'])}, {float(r['pred_weekday_coin'])})")
            if len(rows) == 50:
                cur.execute(f"INSERT INTO default.gold_demand_daily VALUES {', '.join(rows)};")
                rows = []
        if rows:
            cur.execute(f"INSERT INTO default.gold_demand_daily VALUES {', '.join(rows)};")
        print('Uploaded gold_demand_daily to Databricks successfully!')
        
        cur.execute('SHOW TABLES IN default;')
        print('Databricks tables:', cur.fetchall())
