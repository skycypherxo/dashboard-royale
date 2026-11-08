import pandas as pd
import numpy as np

# Prepared daily view
prep = pd.read_parquet('data/1_prepared_views/prepared_daily_view.parquet')
prep_active = prep[prep['location_id'].notna()].copy()
print("\n=== PREPARED DAILY VIEW ===")
print("Active prepared rows:", len(prep_active))
print("Available hours sum:", prep_active['available_hours'].sum())
print("Occupied hours sum:", prep_active['occupied_hours'].sum())
print("Faults opened sum:", prep_active['faults_opened'].sum())
print("Faults by manufacturer:")
print(prep_active.groupby('manufacturer')['faults_opened'].sum())
print("\nFaults by zone:")
print(prep_active.groupby('zone_name')['faults_opened'].sum())

# Machine performance: coin-in, win, theo, hold, downtime per machine
for c in ['coin_in_usd', 'house_win_usd', 'theo_usd', 'luck_residual_usd', 'repair_cost_usd']:
    prep_active[c] = prep_active[c].astype(float)

m_perf = prep_active.groupby('machine_id').agg({
    'coin_in_usd': 'sum',
    'house_win_usd': 'sum',
    'theo_usd': 'sum',
    'luck_residual_usd': 'sum',
    'available_hours': 'sum',
    'occupied_hours': 'sum',
    'faults_opened': 'sum',
    'repair_cost_usd': 'sum',
    'manufacturer': 'first',
    'theme': 'first',
    'zone_name': 'first',
    'bank_id': 'first',
    'configured_rtp': 'first',
    'volatility_class': 'first'
}).reset_index()

m_perf['observed_hold_%'] = (m_perf['house_win_usd'] / m_perf['coin_in_usd']) * 100
m_perf['theo_hold_%'] = (m_perf['theo_usd'] / m_perf['coin_in_usd']) * 100
m_perf['win_per_avail_hour'] = m_perf['house_win_usd'] / m_perf['available_hours']
m_perf['theo_per_avail_hour'] = m_perf['theo_usd'] / m_perf['available_hours']
m_perf['coin_per_avail_hour'] = m_perf['coin_in_usd'] / m_perf['available_hours']

# Look at bottom 10 machines by house win (management's naive bottom 10)
bottom_10_win = m_perf.sort_values('house_win_usd').head(10)
print("\n=== MANAGEMENT BOTTOM 10 BY HOUSE WIN ===")
print(bottom_10_win[['machine_id', 'manufacturer', 'theme', 'zone_name', 'house_win_usd', 'theo_usd', 'luck_residual_usd', 'coin_in_usd', 'observed_hold_%', 'theo_hold_%']].to_string())

# Look at machines with lowest luck residual (worst luck for house = players won a lot)
print("\n=== 10 WORST LUCK RESIDUAL MACHINES (House underperformed theo most) ===")
worst_luck = m_perf.sort_values('luck_residual_usd').head(10)
print(worst_luck[['machine_id', 'manufacturer', 'theme', 'house_win_usd', 'theo_usd', 'luck_residual_usd', 'observed_hold_%', 'theo_hold_%']].to_string())

# Truly weak machines: lowest theo per available hour
print("\n=== 10 WEAKEST MACHINES BY THEO PER AVAILABLE HOUR (True underperformers) ===")
weakest_theo = m_perf.sort_values('theo_per_avail_hour').head(10)
print(weakest_theo[['machine_id', 'manufacturer', 'theme', 'zone_name', 'bank_id', 'theo_per_avail_hour', 'coin_per_avail_hour', 'house_win_usd', 'theo_usd']].to_string())
