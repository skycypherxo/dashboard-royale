import pandas as pd
import numpy as np

# Load tables
player = pd.read_parquet('data/1_prepared_views/player_period.parquet')
prop = pd.read_parquet('data/1_prepared_views/property_day.parquet')
players = pd.read_parquet('data/3_guests/players.parquet')
fnb = pd.read_parquet('data/3_guests/fnb_transactions.parquet')
loyalty = pd.read_parquet('data/3_guests/loyalty_ledger.parquet')
actions = pd.read_parquet('data/2_machine_decision/action_catalog.parquet')

# Convert Decimals to float
for df in [player, prop]:
    for col in df.select_dtypes(include='object').columns:
        try:
            sample = df[col].dropna().iloc[0]
            if hasattr(sample, 'as_tuple'):
                df[col] = df[col].astype(float)
        except Exception:
            pass

print("=== TOTALS ACROSS 6 MONTHS ===")
tot_prop_coin = prop['coin_in_usd'].sum()
tot_prop_win = prop['house_win_usd'].sum()
tot_tracked_coin = player['tracked_coin_in_usd'].sum()
tot_tracked_payout = player['tracked_payout_usd'].sum()
tot_tracked_net = player['tracked_net_usd'].sum()
tot_theo = player['theo_usd'].sum()
tot_luck = player['luck_residual_usd'].sum()
tot_comp_face = player['comp_face_value_usd'].sum()
tot_comp_cost = player['comp_cost_usd'].sum()
tot_pos_cash = player['linked_pos_cash_usd'].sum()
tot_pos_cogs = player['linked_pos_cogs_usd'].sum()
tot_contrib = player['tracked_contribution_usd'].sum()
tot_pts_earned = player['points_earned'].sum()
tot_pts_redeemed = player['points_redeemed'].sum()

print(f"Property Coin-in: ${tot_prop_coin:,.2f}")
print(f"Property House Win: ${tot_prop_win:,.2f} (Hold: {tot_prop_win/tot_prop_coin*100:.2f}%)")
print(f"Tracked Coin-in: ${tot_tracked_coin:,.2f} ({tot_tracked_coin/tot_prop_coin*100:.2f}% of property)")
print(f"Tracked Payout: ${tot_tracked_payout:,.2f}")
print(f"Tracked Net (Payout - Coin-in): ${tot_tracked_net:,.2f}")
print(f"Tracked House Win (-Net): ${-tot_tracked_net:,.2f} (Observed Hold: {-tot_tracked_net/tot_tracked_coin*100:.2f}%)")
print(f"Tracked Theo Win: ${tot_theo:,.2f} (Theo Hold: {tot_theo/tot_tracked_coin*100:.2f}%)")
print(f"Tracked Luck Residual: ${tot_luck:,.2f}")
print(f"Comp Face Value: ${tot_comp_face:,.2f}")
print(f"Comp Economic Cost: ${tot_comp_cost:,.2f} (Cost/Face ratio: {tot_comp_cost/tot_comp_face*100:.2f}%)")
print(f"Reinvestment (Cost / Theo): {tot_comp_cost/tot_theo*100:.2f}%")
print(f"Linked POS Cash: ${tot_pos_cash:,.2f}")
print(f"Linked POS COGS (incl comp): ${tot_pos_cogs:,.2f}")
print(f"Tracked Net Contribution: ${tot_contrib:,.2f}")
print(f"Points Earned: {tot_pts_earned:,}, Points Redeemed: {tot_pts_redeemed:,} ({tot_pts_redeemed/tot_pts_earned*100:.2f}% burn rate)")

print("\n=== MONTHLY BREAKDOWN ===")
monthly = player.groupby('period_month').agg({
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
monthly['observed_hold_%'] = (-monthly['tracked_net_usd'] / monthly['tracked_coin_in_usd']) * 100
monthly['theo_hold_%'] = (monthly['theo_usd'] / monthly['tracked_coin_in_usd']) * 100
monthly['comp_reinvest_%'] = (monthly['comp_cost_usd'] / monthly['theo_usd']) * 100
monthly['avg_coin_per_player'] = monthly['tracked_coin_in_usd'] / monthly['player_id']
print(monthly[['period_month', 'player_id', 'tracked_coin_in_usd', 'tracked_net_usd', 'observed_hold_%', 'theo_hold_%', 'comp_reinvest_%']].to_string())

print("\n=== PLAYER-LEVEL CONCENTRATION ===")
# Group by player over the entire 6 months
p_tot = player.groupby('player_id').agg({
    'tracked_coin_in_usd': 'sum',
    'tracked_net_usd': 'sum',
    'theo_usd': 'sum',
    'observed_visits': 'sum',
    'comp_cost_usd': 'sum'
}).reset_index()

p_tot['house_win'] = -p_tot['tracked_net_usd']
p_tot = p_tot.sort_values('tracked_coin_in_usd', ascending=False).reset_index(drop=True)
n_players = len(p_tot)
tot_coin = p_tot['tracked_coin_in_usd'].sum()
tot_loss = p_tot['house_win'].sum()

print(f"Total Unique Tracked Players: {n_players:,}")
for p in [0.01, 0.05, 0.10, 0.20, 0.50]:
    k = int(n_players * p)
    sub = p_tot.iloc[:k]
    coin_share = sub['tracked_coin_in_usd'].sum() / tot_coin * 100
    loss_share = sub['house_win'].sum() / tot_loss * 100
    print(f"Top {int(p*100)}% ({k:,} players): Coin-in share = {coin_share:.2f}%, House Win share = {loss_share:.2f}%")

# Percentage of players that finished ahead (tracked_net_usd > 0)
ahead_players = (p_tot['tracked_net_usd'] > 0).sum()
print(f"Players who finished ahead (positive winnings): {ahead_players:,} ({ahead_players/n_players*100:.2f}%)")
print(f"Players who broke even: {(p_tot['tracked_net_usd'] == 0).sum():,}")
print(f"Players who lost money: {(p_tot['tracked_net_usd'] < 0).sum():,} ({(p_tot['tracked_net_usd'] < 0).sum()/n_players*100:.2f}%)")

print("\n=== BREAKDOWN BY TIER ===")
tier_agg = player.groupby('tier_end').agg({
    'player_id': 'nunique',
    'tracked_coin_in_usd': 'sum',
    'tracked_net_usd': 'sum',
    'theo_usd': 'sum',
    'comp_cost_usd': 'sum',
    'comp_face_value_usd': 'sum',
    'tracked_contribution_usd': 'sum'
}).reset_index()
tier_agg['comp_reinvest_%'] = (tier_agg['comp_cost_usd'] / tier_agg['theo_usd']) * 100
tier_agg['observed_hold_%'] = (-tier_agg['tracked_net_usd'] / tier_agg['tracked_coin_in_usd']) * 100
print(tier_agg.to_string())

print("\n=== BREAKDOWN BY HOME REGION ===")
region_agg = player.groupby('home_region').agg({
    'player_id': 'nunique',
    'tracked_coin_in_usd': 'sum',
    'tracked_net_usd': 'sum',
    'theo_usd': 'sum',
    'comp_cost_usd': 'sum',
    'tracked_contribution_usd': 'sum'
}).reset_index()
region_agg['coin_share_%'] = (region_agg['tracked_coin_in_usd'] / tot_tracked_coin) * 100
print(region_agg.to_string())

print("\n=== BREAKDOWN BY AGE BAND ===")
age_agg = player.groupby('age_band').agg({
    'player_id': 'nunique',
    'tracked_coin_in_usd': 'sum',
    'tracked_net_usd': 'sum',
    'theo_usd': 'sum',
    'comp_cost_usd': 'sum',
    'tracked_contribution_usd': 'sum'
}).reset_index()
age_agg['coin_share_%'] = (age_agg['tracked_coin_in_usd'] / tot_tracked_coin) * 100
print(age_agg.to_string())

