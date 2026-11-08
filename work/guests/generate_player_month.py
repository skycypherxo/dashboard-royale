import pandas as pd
import numpy as np
from pathlib import Path

out_dir = Path("work/guests/out")
out_dir.mkdir(parents=True, exist_ok=True)

print("Reading player_period...")
pp = pd.read_parquet("data/1_prepared_views/player_period.parquet")

for col in ['tracked_coin_in_usd', 'tracked_payout_usd', 'tracked_net_usd',
            'theo_usd', 'comp_cost_usd', 'comp_face_value_usd',
            'linked_pos_cash_usd', 'tracked_contribution_usd']:
    pp[col] = pp[col].astype(float)

records = []
for month, grp in pp.groupby('period_month'):
    n_players = int(grp['player_id'].nunique())
    tot_coin = float(grp['tracked_coin_in_usd'].sum())
    tot_payout = float(grp['tracked_payout_usd'].sum())
    tot_net = float(grp['tracked_net_usd'].sum())
    tot_theo = float(grp['theo_usd'].sum())
    tot_comp_cost = float(grp['comp_cost_usd'].sum())
    tot_comp_face = float(grp['comp_face_value_usd'].sum())
    tot_pos_cash = float(grp['linked_pos_cash_usd'].sum())
    tot_contrib = float(grp['tracked_contribution_usd'].sum())
    
    # Top 1% of players by coin-in in this month
    k = max(1, int(np.ceil(0.01 * n_players)))
    top_by_coin = grp.sort_values('tracked_coin_in_usd', ascending=False).head(k)
    coin_share_top1 = float(top_by_coin['tracked_coin_in_usd'].sum() / tot_coin) if tot_coin > 0 else 0.0
    
    # Sign convention for share_of_net_top_1pct_players:
    # Tracked net is (payout - coin_in), which is negative for net player losses.
    # We define share_of_net_top_1pct_players as the share of total monthly net losses
    # (-tracked_net_usd) accounted for by the top 1% largest wagering cardholders.
    # Mathematically, (top1_tracked_net_usd / tot_tracked_net_usd).
    net_share_top1 = float(top_by_coin['tracked_net_usd'].sum() / tot_net) if tot_net != 0 else 0.0
    
    records.append({
        'period_month': str(month),
        'players': n_players,
        'tracked_coin_in_usd': round(tot_coin, 2),
        'tracked_payout_usd': round(tot_payout, 2),
        'tracked_net_usd': round(tot_net, 2),
        'theo_usd': round(tot_theo, 2),
        'comp_cost_usd': round(tot_comp_cost, 2),
        'comp_face_value_usd': round(tot_comp_face, 2),
        'linked_pos_cash_usd': round(tot_pos_cash, 2),
        'tracked_contribution_usd': round(tot_contrib, 2),
        'share_of_coin_in_top_1pct_players': round(coin_share_top1, 4),
        'share_of_net_top_1pct_players': round(net_share_top1, 4)
    })

df_out = pd.DataFrame(records)
out_path = out_dir / "player_month.parquet"
df_out.to_parquet(out_path, index=False, engine='pyarrow')
print(f"PASS: Wrote {out_path} ({len(df_out)} rows x {len(df_out.columns)} cols).")
print(df_out.to_string())
