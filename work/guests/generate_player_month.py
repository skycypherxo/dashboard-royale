import pandas as pd
import numpy as np
from pathlib import Path

out_dir = Path("work/guests/out")
out_dir.mkdir(parents=True, exist_ok=True)

print("Reading player_period...")
df = pd.read_parquet("data/1_prepared_views/player_period.parquet")

# Cast decimal objects to float for analytical computations
decimal_cols = [
    'tracked_coin_in_usd', 'tracked_payout_usd', 'tracked_net_usd',
    'theo_usd', 'luck_residual_usd', 'linked_pos_cash_usd',
    'linked_pos_cogs_usd', 'comp_face_value_usd', 'comp_cost_usd',
    'tracked_contribution_usd'
]

for col in decimal_cols:
    if col in df.columns:
        df[col] = df[col].astype(float)

# Add derived analytical metrics
df['observed_hold_pct'] = np.where(df['tracked_coin_in_usd'] > 0, (-df['tracked_net_usd'] / df['tracked_coin_in_usd']) * 100.0, 0.0)
df['theo_hold_pct'] = np.where(df['tracked_coin_in_usd'] > 0, (df['theo_usd'] / df['tracked_coin_in_usd']) * 100.0, 0.0)
df['comp_reinvestment_pct'] = np.where(df['theo_usd'] > 0, (df['comp_cost_usd'] / df['theo_usd']) * 100.0, 0.0)
df['comp_cost_to_face_pct'] = np.where(df['comp_face_value_usd'] > 0, (df['comp_cost_usd'] / df['comp_face_value_usd']) * 100.0, 0.0)

# Visits & rate metrics
safe_visits = np.where(df['observed_visits'] > 0, df['observed_visits'], 1)
df['coin_in_per_visit'] = np.where(df['observed_visits'] > 0, df['tracked_coin_in_usd'] / safe_visits, 0.0)
df['hours_per_visit'] = np.where(df['observed_visits'] > 0, df['carded_play_hours'] / safe_visits, 0.0)
df['net_per_visit'] = np.where(df['observed_visits'] > 0, df['tracked_net_usd'] / safe_visits, 0.0)

# POS Net Margin
df['linked_pos_net_margin_usd'] = df['linked_pos_cash_usd'] - df['linked_pos_cogs_usd']

# Player status
df['is_ahead'] = df['tracked_net_usd'] > 0.0
df['is_loss'] = df['tracked_net_usd'] < 0.0
df['is_even'] = df['tracked_net_usd'] == 0.0

# Loyalty points burn rate
df['point_burn_rate_pct'] = np.where(df['points_earned'] > 0, (df['points_redeemed'] / df['points_earned']) * 100.0, 0.0)

# Monthly spend tier
conditions = [
    df['tracked_coin_in_usd'] >= 10000,
    df['tracked_coin_in_usd'] >= 2500,
    df['tracked_coin_in_usd'] >= 500,
    df['tracked_coin_in_usd'] > 0
]
choices = ['VIP ($10k+)', 'High Value ($2.5k-$10k)', 'Core ($500-$2.5k)', 'Casual (<$500)']
df['monthly_spend_segment'] = np.select(conditions, choices, default='Non-Gaming')

out_path = out_dir / "player_month.parquet"
df.to_parquet(out_path, index=False, engine='pyarrow')
print(f"Successfully wrote {len(df):,} rows to {out_path}")
print(df[['period_month', 'monthly_spend_segment', 'tracked_coin_in_usd', 'observed_hold_pct', 'comp_reinvestment_pct']].head())

