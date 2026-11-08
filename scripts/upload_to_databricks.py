import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

host = os.environ.get('DATABRICKS_SERVER_HOSTNAME')
token = os.environ.get('DATABRICKS_TOKEN') or os.environ.get('DATABRICKS_ACCESS_TOKEN')
http_path = os.environ.get('DATABRICKS_HTTP_PATH')

df = pd.read_parquet('work/floor/out/machine_scorecard.parquet')
print('Read parquet scorecard:', len(df), 'rows')

from databricks import sql
with sql.connect(server_hostname=host, http_path=http_path, access_token=token) as conn:
    with conn.cursor() as cur:
        cur.execute('''
            CREATE OR REPLACE TABLE default.gold_machine_scorecard (
                machine_id STRING,
                theme STRING,
                manufacturer STRING,
                volatility_class STRING,
                configured_rtp DOUBLE,
                lease_class STRING,
                zone_name STRING,
                bank_id STRING,
                location_id STRING,
                coin_in_usd DOUBLE,
                house_win_usd DOUBLE,
                theo_usd DOUBLE,
                luck_residual_usd DOUBLE,
                observed_hold_pct DOUBLE,
                theo_hold_pct DOUBLE,
                available_hours DOUBLE,
                action_recommendation STRING
            ) USING DELTA;
        ''')
        rows = []
        for _, r in df.iterrows():
            theme = str(r['theme']).replace("'", "''")
            mfg = str(r['manufacturer']).replace("'", "''")
            loc = str(r.get('location_id', '')).replace("'", "''")
            zone = str(r.get('zone_name', '')).replace("'", "''")
            bank = str(r.get('bank_id', '')).replace("'", "''")
            act = str(r.get('action_recommendation', 'A-INSPECT')).replace("'", "''")
            
            row_str = (
                f"('{r['machine_id']}', '{theme}', '{mfg}', '{r['volatility_class']}', "
                f"{r['configured_rtp']}, '{r['lease_class']}', '{zone}', '{bank}', '{loc}', "
                f"{r['coin_in_usd']}, {r['house_win_usd']}, {r['theo_usd']}, "
                f"{r['luck_residual_usd']}, {r['observed_hold_pct']}, {r['theo_hold_pct']}, "
                f"{r['available_hours']}, '{act}')"
            )
            rows.append(row_str)
            if len(rows) == 50:
                cur.execute(f"INSERT INTO default.gold_machine_scorecard VALUES {', '.join(rows)};")
                rows = []
        if rows:
            cur.execute(f"INSERT INTO default.gold_machine_scorecard VALUES {', '.join(rows)};")
            
        cur.execute('SELECT count(*) as cnt, sum(house_win_usd) as total_win FROM default.gold_machine_scorecard;')
        res = cur.fetchall()
        print('Databricks cloud table default.gold_machine_scorecard populated successfully! Result:', res)
