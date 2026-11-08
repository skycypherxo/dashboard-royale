# Data Contract & Shared Metric Definitions

**Team:** Akshaya (Floor & ML Lead) & Vaishnavi (Guest & Business Intelligence Lead)  
**Version:** 1.0.0  
**Status:** Approved by both leads  

---

## 1. Accounting & Mathematical Conventions

| Term | Mathematical Definition | Scope & Sign Convention | Notes |
|---|---|---|---|
| **Gaming Day** | 06:00 to 06:00 local time (`America/Los_Angeles`) | Calendar & all daily tables | March 8, 2025 has 23 scheduled hours (82,800 sec). Never assume 24 hours. |
| **Coin-In** | Total wagered, including replayed winnings | Floor & Tracked | Cents in source; Dollars in prepared views. |
| **Payout** | Total returned from game outcomes | Floor & Tracked | Jackpots and handpays counted once. |
| **House Win** | $\text{Coin-in} - \text{Payout}$ | Casino perspective | Positive = casino profit; Negative = casino loss. |
| **Player Net** | $\text{Payout} - \text{Coin-in} = -(\text{House Win})$ | Player perspective | Positive = player profit; Negative = player loss. Do not confuse with House Win! |
| **Observed Hold** | $\frac{\sum \text{House Win}}{\sum \text{Coin-in}}$ | Floor & Player | Must compute **ratio of sums**, never average of daily/player ratios. Undefined if coin-in = 0. |
| **Configured RTP** | Published payout percentage ($1 - \text{theo\_hold}$) | Machine setting | e.g. 90.0% RTP corresponds to 10.0% theoretical hold. |
| **Theoretical Win ($\text{theo}$)** | $\sum (\text{Coin-in} \times (1 - \text{Configured RTP}))$ | Floor & Player | Expected house win based on exposure and game math. Benchmark, not a guarantee. |
| **Luck Residual (Floor)** | $\text{House Win} - \text{Theo}$ | Machine tables | Positive = house was lucky; Negative = house ran behind expected win. |
| **Luck Residual (Player)** | $\text{Tracked Net} + \text{Theo} = -(\text{House Luck Residual})$ | Player tables | Positive = player ran ahead of expected return; Negative = player was unlucky. |
| **Comp Face Value** | Menu / retail price of comped items | Guest tables | Not revenue; retail valuation of items. |
| **Comp Economic Cost** | Actual food & beverage cost of goods | Guest tables | Equal to POS COGS for comped items. Averages ~27.93% of face value. |
| **Comp Reinvestment** | $\frac{\sum \text{Comp Economic Cost}}{\sum \text{Theo Win}}$ | Guest tables | Ratio of economic cost to theoretical win over a stated period. |
| **Tracked Contribution** | $\text{Tracked House Win} + \text{POS Cash} - \text{POS COGS}$ | Guest tables | Comp cost is already inside POS COGS. **Do not subtract comp cost twice!** |

---

## 2. Dataset Population Rules

1. **Carded vs. All Play:**
   - Source table `machine_day` covers all play on the floor.
   - Source tables `players`, `sessions`, `trips`, and `player_period` cover carded loyalty-card play only.
   - Tracked play represents approximately 65.81% of property coin-in. The remaining 34.19% is uncarded play. These two populations will never match, and that is expected.
2. **Off-Floor Machine Records:**
   - 1,018 rows in `prepared_daily_view` and `machine_day` represent days before a machine was installed or after it was retired (`location_id` is null).
   - These rows MUST be excluded before machine ranking or availability calculation.
3. **Fact Table Aggregation:**
   - Always aggregate child fact tables (`sessions`, `loyalty_ledger`, `fnb_transactions`) to player-month or machine-day before joining. Never join two granular fact tables row-by-row and sum.
4. **Traffic Sensors:**
   - Missing traffic counts in `zone_traffic_hourly` indicate an offline sensor (`counter_status`), not zero visitors.
5. **Action Catalog Pricing Formula:**
   - For any action from `action_catalog`:
     $$\text{Budget Cost} = \frac{\text{quantity} \times (\text{unit\_cost\_cents} + \text{recurring\_cost\_cents\_per\_day} \times \max(0, 30 - \text{lead\_days}))}{100}$$
   - Fixed package costs (e.g. technician packages) are charged in full.

---

## 3. Analytical Handoffs

1. **Floor to Guests (Akshaya to Vaishnavi):**
   - File: `work/floor/out/machine_scorecard.parquet`
   - File: `work/floor/out/demand_daily.parquet`
   - File: `work/floor/out/model_card.md`
   - Usage: Vaishnavi references machine-level downtime, exposure, and luck residuals to price and substantiate machine-related operational actions.
2. **Guests to Shared Integration (Vaishnavi to Team):**
   - File: `work/guests/out/player_month.parquet`
   - File: `work/guests/out/action_shortlist.md`
   - File: `dashboard/guests.html`
   - File: `dashboard/actions.html`
   - File: `dashboard/index.html`
   - File: `submission/writeup.md`
   - File: `submission/claims.md`
   - File: `submission/ai.md`

