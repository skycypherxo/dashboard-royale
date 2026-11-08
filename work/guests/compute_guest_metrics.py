import pandas as pd
import numpy as np
import json
from pathlib import Path

df = pd.read_parquet("work/guests/out/player_month.parquet")

periods = {
    "6m": ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06"],
    "3m": ["2025-04", "2025-05", "2025-06"],
    "1m": ["2025-06"]
}

def gini_coefficient(values):
    # Mean absolute difference
    v = np.sort(values)
    n = len(values)
    if n == 0 or np.sum(v) == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return float((2.0 * np.sum(index * v) - (n + 1) * np.sum(v)) / (n * np.sum(v)))

data_output = {}

for p_key, p_months in periods.items():
    sub = df[df['period_month'].isin(p_months)].copy()
    
    # Summary by period
    tot_coin = sub['tracked_coin_in_usd'].sum()
    tot_payout = sub['tracked_payout_usd'].sum()
    tot_net = sub['tracked_net_usd'].sum() # player perspective (payout - coin_in)
    tot_win = -tot_net # house perspective
    tot_theo = sub['theo_usd'].sum()
    tot_luck = sub['luck_residual_usd'].sum() # tracked_net + theo
    tot_comp_face = sub['comp_face_value_usd'].sum()
    tot_comp_cost = sub['comp_cost_usd'].sum()
    tot_pos_cash = sub['linked_pos_cash_usd'].sum()
    tot_pos_cogs = sub['linked_pos_cogs_usd'].sum()
    tot_pos_net = tot_pos_cash - tot_pos_cogs
    tot_contrib = sub['tracked_contribution_usd'].sum()
    tot_pts_earned = int(sub['points_earned'].sum())
    tot_pts_redeemed = int(sub['points_redeemed'].sum())
    
    unique_players = int(sub['player_id'].nunique())
    tot_visits = int(sub['observed_visits'].sum())
    tot_play_hours = float(sub['carded_play_hours'].sum())
    
    # Player level aggregation for concentration
    player_agg = sub.groupby('player_id').agg({
        'tracked_coin_in_usd': 'sum',
        'tracked_net_usd': 'sum',
        'theo_usd': 'sum',
        'comp_cost_usd': 'sum',
        'observed_visits': 'sum',
        'carded_play_hours': 'sum'
    }).reset_index()
    player_agg['house_win'] = -player_agg['tracked_net_usd']
    
    # Sort descending by coin-in
    player_agg = player_agg.sort_values('tracked_coin_in_usd', ascending=False).reset_index(drop=True)
    n_p = len(player_agg)
    
    # Percentiles
    conc = {}
    for pct in [1, 5, 10, 20, 50]:
        cutoff = max(1, int(n_p * (pct / 100.0)))
        top_slice = player_agg.iloc[:cutoff]
        conc[f"top_{pct}"] = {
            "player_count": cutoff,
            "coin_share_pct": round(float(top_slice['tracked_coin_in_usd'].sum() / tot_coin * 100.0), 2) if tot_coin > 0 else 0,
            "win_share_pct": round(float(top_slice['house_win'].sum() / tot_win * 100.0), 2) if tot_win > 0 else 0,
            "comp_share_pct": round(float(top_slice['comp_cost_usd'].sum() / tot_comp_cost * 100.0), 2) if tot_comp_cost > 0 else 0,
        }
    
    # Outcome distributions
    ahead_count = int((player_agg['tracked_net_usd'] > 0).sum())
    even_count = int((player_agg['tracked_net_usd'] == 0).sum())
    loss_count = int((player_agg['tracked_net_usd'] < 0).sum())
    
    gini_coin = gini_coefficient(player_agg['tracked_coin_in_usd'].values)
    
    # Lorenz curve (10 points: 10% increments)
    lorenz_points = []
    # Sort ascending for Lorenz
    p_asc = player_agg.sort_values('tracked_coin_in_usd', ascending=True).reset_index(drop=True)
    cum_coin = p_asc['tracked_coin_in_usd'].cumsum() / tot_coin * 100.0
    for decile in range(10, 110, 10):
        idx = min(n_p - 1, int(n_p * (decile / 100.0)) - 1)
        lorenz_points.append({
            "population_pct": decile,
            "coin_cum_pct": round(float(cum_coin.iloc[idx]), 2)
        })
    
    # Aggregation by dimensions
    def agg_dim(col_name):
        grouped = sub.groupby(col_name).agg({
            'player_id': 'nunique',
            'observed_visits': 'sum',
            'tracked_coin_in_usd': 'sum',
            'tracked_payout_usd': 'sum',
            'tracked_net_usd': 'sum',
            'theo_usd': 'sum',
            'luck_residual_usd': 'sum',
            'comp_face_value_usd': 'sum',
            'comp_cost_usd': 'sum',
            'linked_pos_cash_usd': 'sum',
            'linked_pos_cogs_usd': 'sum',
            'points_earned': 'sum',
            'points_redeemed': 'sum',
            'tracked_contribution_usd': 'sum'
        }).reset_index()
        
        records = []
        for _, r in grouped.iterrows():
            coin = float(r['tracked_coin_in_usd'])
            net = float(r['tracked_net_usd'])
            h_win = -net
            theo = float(r['theo_usd'])
            comp_cost = float(r['comp_cost_usd'])
            comp_face = float(r['comp_face_value_usd'])
            pts_e = int(r['points_earned'])
            pts_r = int(r['points_redeemed'])
            records.append({
                "group": str(r[col_name]),
                "unique_players": int(r['player_id']),
                "observed_visits": int(r['observed_visits']),
                "tracked_coin_in_usd": round(coin, 2),
                "coin_share_pct": round(coin / tot_coin * 100.0, 2) if tot_coin > 0 else 0,
                "tracked_payout_usd": round(float(r['tracked_payout_usd']), 2),
                "tracked_net_usd": round(net, 2),
                "house_win_usd": round(h_win, 2),
                "observed_hold_pct": round(h_win / coin * 100.0, 2) if coin > 0 else 0,
                "theo_usd": round(theo, 2),
                "theo_hold_pct": round(theo / coin * 100.0, 2) if coin > 0 else 0,
                "luck_residual_usd": round(float(r['luck_residual_usd']), 2),
                "comp_face_value_usd": round(comp_face, 2),
                "comp_cost_usd": round(comp_cost, 2),
                "cost_to_face_pct": round(comp_cost / comp_face * 100.0, 2) if comp_face > 0 else 0,
                "comp_reinvestment_pct": round(comp_cost / theo * 100.0, 2) if theo > 0 else 0,
                "linked_pos_cash_usd": round(float(r['linked_pos_cash_usd']), 2),
                "linked_pos_cogs_usd": round(float(r['linked_pos_cogs_usd']), 2),
                "pos_margin_usd": round(float(r['linked_pos_cash_usd']) - float(r['linked_pos_cogs_usd']), 2),
                "points_earned": pts_e,
                "points_redeemed": pts_r,
                "points_burn_rate_pct": round(pts_r / pts_e * 100.0, 2) if pts_e > 0 else 0,
                "tracked_contribution_usd": round(float(r['tracked_contribution_usd']), 2),
                "avg_coin_per_visit": round(coin / max(1, r['observed_visits']), 2),
                "avg_coin_per_player": round(coin / max(1, r['player_id']), 2),
            })
        return records

    by_tier = agg_dim('tier_end')
    by_age = agg_dim('age_band')
    by_region = agg_dim('home_region')
    
    # Monthly progression
    monthly_trend = []
    month_grouped = sub.groupby('period_month').agg({
        'player_id': 'nunique',
        'observed_visits': 'sum',
        'tracked_coin_in_usd': 'sum',
        'tracked_payout_usd': 'sum',
        'tracked_net_usd': 'sum',
        'theo_usd': 'sum',
        'luck_residual_usd': 'sum',
        'comp_face_value_usd': 'sum',
        'comp_cost_usd': 'sum',
        'linked_pos_cash_usd': 'sum',
        'linked_pos_cogs_usd': 'sum',
        'points_earned': 'sum',
        'points_redeemed': 'sum',
        'tracked_contribution_usd': 'sum'
    }).reset_index()
    
    for _, r in month_grouped.iterrows():
        c = float(r['tracked_coin_in_usd'])
        n = float(r['tracked_net_usd'])
        th = float(r['theo_usd'])
        cc = float(r['comp_cost_usd'])
        pe = int(r['points_earned'])
        pr = int(r['points_redeemed'])
        monthly_trend.append({
            "month": str(r['period_month']),
            "unique_players": int(r['player_id']),
            "observed_visits": int(r['observed_visits']),
            "tracked_coin_in_usd": round(c, 2),
            "tracked_payout_usd": round(float(r['tracked_payout_usd']), 2),
            "tracked_net_usd": round(n, 2),
            "house_win_usd": round(-n, 2),
            "observed_hold_pct": round(-n / c * 100.0, 2) if c > 0 else 0,
            "theo_usd": round(th, 2),
            "theo_hold_pct": round(th / c * 100.0, 2) if c > 0 else 0,
            "luck_residual_usd": round(float(r['luck_residual_usd']), 2),
            "comp_face_value_usd": round(float(r['comp_face_value_usd']), 2),
            "comp_cost_usd": round(cc, 2),
            "comp_reinvestment_pct": round(cc / th * 100.0, 2) if th > 0 else 0,
            "linked_pos_cash_usd": round(float(r['linked_pos_cash_usd']), 2),
            "linked_pos_cogs_usd": round(float(r['linked_pos_cogs_usd']), 2),
            "points_earned": pe,
            "points_redeemed": pr,
            "points_burn_rate_pct": round(pr / pe * 100.0, 2) if pe > 0 else 0,
            "tracked_contribution_usd": round(float(r['tracked_contribution_usd']), 2)
        })

    data_output[p_key] = {
        "kpis": {
            "unique_players": unique_players,
            "observed_visits": tot_visits,
            "carded_play_hours": round(tot_play_hours, 1),
            "tracked_coin_in_usd": round(tot_coin, 2),
            "tracked_payout_usd": round(tot_payout, 2),
            "tracked_net_usd": round(tot_net, 2),
            "house_win_usd": round(tot_win, 2),
            "observed_hold_pct": round(tot_win / tot_coin * 100.0, 2) if tot_coin > 0 else 0,
            "theo_usd": round(tot_theo, 2),
            "theo_hold_pct": round(tot_theo / tot_coin * 100.0, 2) if tot_coin > 0 else 0,
            "luck_residual_usd": round(tot_luck, 2),
            "comp_face_value_usd": round(tot_comp_face, 2),
            "comp_cost_usd": round(tot_comp_cost, 2),
            "comp_cost_to_face_pct": round(tot_comp_cost / tot_comp_face * 100.0, 2) if tot_comp_face > 0 else 0,
            "comp_reinvestment_pct": round(tot_comp_cost / tot_theo * 100.0, 2) if tot_theo > 0 else 0,
            "linked_pos_cash_usd": round(tot_pos_cash, 2),
            "linked_pos_cogs_usd": round(tot_pos_cogs, 2),
            "pos_net_margin_usd": round(tot_pos_net, 2),
            "points_earned": tot_pts_earned,
            "points_redeemed": tot_pts_redeemed,
            "points_burn_rate_pct": round(tot_pts_redeemed / tot_pts_earned * 100.0, 2) if tot_pts_earned > 0 else 0,
            "tracked_contribution_usd": round(tot_contrib, 2),
            "gini_coin": round(gini_coin, 3),
            "ahead_players": ahead_count,
            "ahead_pct": round(ahead_count / n_p * 100.0, 2) if n_p > 0 else 0,
            "even_players": even_count,
            "even_pct": round(even_count / n_p * 100.0, 2) if n_p > 0 else 0,
            "loss_players": loss_count,
            "loss_pct": round(loss_count / n_p * 100.0, 2) if n_p > 0 else 0,
        },
        "concentration": conc,
        "lorenz_curve": lorenz_points,
        "by_tier": by_tier,
        "by_age": by_age,
        "by_region": by_region,
        "monthly_trend": monthly_trend
    }

json_path = Path("work/guests/out/guest_analytics.json")
with open(json_path, "w") as f:
    json.dump(data_output, f, indent=2)

print(f"Exported detailed guest analytics to {json_path}")
print("6M KPIs:", data_output['6m']['kpis'])

