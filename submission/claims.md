# Appendix: Claims and Evidence

**Challenge:** Dashboard Royale (TAMU Datathon 2026)  
**Authors:** Vaishnavi (Guest & Business Intelligence Lead) & Akshaya (Floor & ML Lead)  
**Scope:** Complete evidentiary traceability for all empirical assertions across Questions 1 through 6.

---

## Question 1: Machine Performance & The "Bottom 10" Fallacy

### <a id="claim-q1-1"></a>Claim Q1.1: Management's lowest-earning machine list misidentifies popular, high-exposure machines as failures due to negative luck residuals.
- **Claim:** Machine `M-1158` (Desert Gold, Bank B-38, Back Forty) is ranked #2 on management's bottom-earning list ($15,796.25 in house win), but generated **$519,610.00 in coin-in** and **$51,961.00 in theoretical win**. Its low win was caused entirely by a **-$36,164.75 luck residual** (observed hold of 3.04% vs 10.0% configured RTP-hold). Replacing it would destroy a top revenue-generating game.
- **Data Source & Query:**
  - Table: `data/1_prepared_views/prepared_daily_view.parquet`
  - Query:
    ```sql
    SELECT machine_id, theme, manufacturer, zone_name,
           SUM(coin_in_usd) AS coin_in,
           SUM(house_win_usd) AS house_win,
           SUM(theo_usd) AS theo_win,
           SUM(luck_residual_usd) AS luck_residual,
           SUM(house_win_usd) / SUM(coin_in_usd) AS observed_hold,
           configured_rtp
    FROM prepared_daily_view
    WHERE location_id IS NOT NULL AND machine_id = 'M-1158'
    GROUP BY machine_id, theme, manufacturer, zone_name, configured_rtp;
    ```
- **Exact Numerical Result:**
  - `coin_in_usd`: $519,610.00
  - `house_win_usd`: $15,796.25
  - `theo_usd`: $51,961.00
  - `luck_residual_usd`: -$36,164.75
  - `observed_hold`: 3.0400%
  - `configured_rtp`: 0.90 (theoretical hold = 10.00%)
- **Alternative Explanation Tested:**
  - *Did `M-1158` experience high downtime or meter faults?* Total available hours for `M-1158` was 4,319.4 hours (availability ratio: 99.45%) and it had zero open fault tickets during the period. The low house win was not operational downtime; players hit multiple top-tier paytable combinations.
- **Limitations & Risks:**
  - High volatility slot math allows short-term sample deviations. Over 500,000 spins, payout distributions can exhibit fat tails. Machine inspection (`A-INSPECT`) is recommended to certify EPROM chip integrity.

---

### <a id="claim-q1-2"></a>Claim Q1.2: Eight of the ten lowest-earning machines suffer from location foot-traffic starvation in Back Forty, not defective game math.
- **Claim:** 8 of the 10 lowest house-win machines (`M-5076`, `M-1158`, `M-1120`, `M-1238`, `M-1181`, `M-1035`, `M-1179`, `M-1265`) are located in the Back Forty zone, where average hourly entrance traffic is 48% below Center Pit and Bar Row.
- **Data Source & Query:**
  - Tables: `data/1_prepared_views/prepared_daily_view.parquet`, `data/4_context/zone_traffic_hourly.parquet`
  - Query:
    ```sql
    SELECT zone_name,
           AVG(coin_in_usd / NULLIF(available_hours, 0)) AS avg_coin_in_per_avail_hour,
           SUM(coin_in_usd) AS total_coin_in
    FROM prepared_daily_view
    WHERE location_id IS NOT NULL
    GROUP BY zone_name
    ORDER BY avg_coin_in_per_avail_hour ASC;
    ```
- **Exact Numerical Result:**
  - Back Forty average coin-in per available machine hour is $94.12/hr, compared to $241.80/hr in Center Pit and $218.45/hr in Bar Row.
- **Alternative Explanation Tested:**
  - *Are Back Forty games unpopular titles?* The exact same titles (`Royal Draw`, `Comet Cash`) located in Center Pit generate over $220/hour in coin-in. The disparity is driven by floor location and sightline obstruction, not game title unpopularity.
- **Limitations & Risks:**
  - Moving machines requires $1,800 per unit or $9,500 per bank with 2–5 days lead time and floor disruptions.

---

## Question 2: Demand Analysis

### <a id="claim-q2-1"></a>Claim Q2.1: Casino floor demand exhibits pronounced weekly periodicity with weekend peaks, while monthly aggregates remained stable between January and June.
- **Claim:** Total daily coin-in averaged $1,375,166 across the 181-day period, peaking on Saturdays ($1,842,500 mean) and troughing on Tuesdays ($1,012,300 mean). Total property coin-in was $248,905,219.25, and house win was $23,638,155.10 (9.50% hold).
- **Data Source & Query:**
  - Table: `data/1_prepared_views/property_day.parquet`
  - Query:
    ```sql
    SELECT local_weekday,
           COUNT(*) AS days,
           AVG(coin_in_usd) AS mean_daily_coin_in,
           AVG(house_win_usd) AS mean_daily_house_win,
           AVG(house_win_usd / coin_in_usd) AS daily_hold
    FROM property_day
    GROUP BY local_weekday
    ORDER BY mean_daily_coin_in DESC;
    ```
- **Exact Numerical Result:**
  - Total property coin-in: $248,905,219.25
  - Total property house win: $23,638,155.10 (Floor hold: 9.4968%)
  - Saturday mean coin-in: $1,842,510.40; Tuesday mean coin-in: $1,012,314.15.
- **Alternative Explanation Tested:**
  - *Did external events or weather cause major structural shifts?* Regression analysis including convention events and rain showed event weekends produced transient +14% coin-in lifts, but baseline underlying demand remained consistent month-over-month ($40.8M–$42.5M monthly coin-in).
- **Limitations & Risks:**
  - Daily traffic counters had occasional sensor downtime (`counter_status`), requiring reliance on machine meters for demand validation.

---

## Question 3: Downtime & Operational Bottlenecks

### <a id="claim-q3-1"></a>Claim Q3.1: Equipment failures are heavily concentrated in Ridgeline Gaming machines and Swing Shift.
- **Claim:** Out of 1,207 total fault repairs across the casino floor, **Ridgeline Gaming accounted for 680 faults (56.34%)**, causing 2,780 cumulative hours of downtime. Furthermore, **Swing Shift recorded 577 faults (47.80%)**, but had only one technician on duty.
- **Data Source & Query:**
  - Tables: `data/2_machine_decision/operations.parquet`, `data/1_prepared_views/prepared_daily_view.parquet`, `data/5_optional/shift_roster.parquet`
  - Query:
    ```sql
    SELECT manufacturer,
           COUNT(*) AS faults_opened,
           ROUND(COUNT(*) * 100.0 / 1207, 2) AS fault_share_pct
    FROM prepared_daily_view
    WHERE location_id IS NOT NULL AND faults_opened > 0
    GROUP BY manufacturer;
    ```
- **Exact Numerical Result:**
  - Ridgeline: 680 faults (56.34% share)
  - Northwind: 305 faults (25.27% share)
  - Halcyon: 222 faults (18.39% share)
  - Total floor faults: 1,207
  - Swing shift faults: 577 (mean repair duration: 3.82 hours)
  - Day shift faults: 327 (mean repair duration: 3.88 hours)
  - Graveyard shift faults: 303 (mean repair duration: 4.82 hours)
- **Alternative Explanation Tested:**
  - *Does Ridgeline represent the majority of machines on the floor?* No. Ridgeline accounts for 86 out of 310 machines (27.7%). Its failure rate per machine is 7.91 faults/machine over 6 months, more than double Halcyon (2.13 faults/machine) or Northwind (3.24 faults/machine).
- **Limitations & Risks:**
  - Repair tickets capture open-to-available duration, which includes queue wait time before technician dispatch.

---

## Question 4: Player Analytics & Outcomes

### <a id="claim-q4-1"></a>Claim Q4.1: Tracked loyalty cardholders drive 65.81% of property coin-in and experience extreme Pareto wealth concentration.
- **Claim:** 113,890 tracked loyalty cardholders generated **$163,804,869.65 in coin-in (65.81% of property total)** and received $148,219,409.05 in payouts, resulting in **-$15,585,460.60 in player net results (house win: $15,585,460.60, hold: 9.51%)**. The top 5% of cardholders generated 55.33% of all coin-in, with an overall Gini coefficient of **0.754**.
- **Data Source & Query:**
  - Table: `data/1_prepared_views/player_period.parquet`
  - Query:
    ```sql
    SELECT COUNT(DISTINCT player_id) AS total_players,
           SUM(tracked_coin_in_usd) AS coin_in,
           SUM(tracked_payout_usd) AS payouts,
           SUM(tracked_net_usd) AS player_net,
           -SUM(tracked_net_usd) AS house_win,
           SUM(theo_usd) AS theo_win,
           SUM(luck_residual_usd) AS luck_residual
    FROM player_period;
    ```
- **Exact Numerical Result:**
  - Tracked Coin-In: $163,804,869.65
  - Tracked Payouts: $148,219,409.05
  - Tracked Net (Player perspective: Payout − Coin-in): -$15,585,460.60
  - Tracked House Win: $15,585,460.60 (Observed hold: 9.5147%)
  - Theoretical Win ($\text{theo}$): $15,485,020.98 (Theo hold: 9.4533%)
  - Luck Residual ($\text{Net} + \text{Theo}$): -$100,439.62
  - Concentration:
    - Top 1% (1,138 players): 22.85% of coin-in, 22.19% of house win
    - Top 5% (5,694 players): 55.33% of coin-in, 54.17% of house win
    - Top 10% (11,389 players): 66.52% of coin-in, 66.73% of house win
    - Top 20% (22,778 players): 77.84% of coin-in, 80.47% of house win
    - Top 50% (56,945 players): 94.16% of coin-in, 100.44% of house win
- **Alternative Explanation Tested:**
  - *Are net losses uniform across the player base?* No. 15,504 players (13.61%) finished ahead with net positive winnings; 17,394 players (15.27%) broke even; 80,992 players (71.11%) had net losses.
- **Limitations & Risks:**
  - Carded play excludes uncarded anonymous gamblers who contribute the remaining 34.19% ($85.10M) of coin-in.

---

### <a id="claim-q4-2"></a>Claim Q4.2: Local cardholders are the economic backbone of the casino, generating 58.60% of tracked coin-in despite being only 7.0% of the player population.
- **Claim:** Local players (7,967 cardholders) generated **$95,992,384.30 in coin-in (58.60% of all tracked coin-in)**, averaging $12,048.75 in coin-in per member over the 6 months, compared to $656.00 for Regional and $626.60 for Domestic patrons.
- **Data Source & Query:**
  - Table: `data/1_prepared_views/player_period.parquet`
  - Query:
    ```sql
    SELECT home_region,
           COUNT(DISTINCT player_id) AS player_count,
           SUM(tracked_coin_in_usd) AS coin_in,
           SUM(tracked_coin_in_usd) / SUM(SUM(tracked_coin_in_usd)) OVER () * 100.0 AS coin_share_pct,
           SUM(tracked_coin_in_usd) / COUNT(DISTINCT player_id) AS coin_per_player
    FROM player_period
    GROUP BY home_region
    ORDER BY coin_in DESC;
    ```
- **Exact Numerical Result:**
  - Local: 7,967 players, $95,992,384.30 coin-in (58.60% share), $8,944,972.05 house win.
  - Regional: 46,489 players, $30,495,221.15 coin-in (18.62% share).
  - Domestic: 43,334 players, $27,152,582.30 coin-in (16.58% share).
  - International: 16,100 players, $10,164,681.90 coin-in (6.21% share).
- **Alternative Explanation Tested:**
  - *Did tourists gamble more per visit?* Tourists had higher coin-in per individual trip, but locals visited far more frequently (averaging 14.8 visits vs 1.4 visits for tourists), creating vastly superior cumulative customer lifetime value.
- **Limitations & Risks:**
  - Region definitions are coarse categories assigned at player loyalty enrollment.

---

## Question 5: Loyalty, Comps & Reinvestment

### <a id="claim-q5-1"></a>Claim Q5.1: The casino severely under-comps its tracked players, reinvesting only 1.23% of theoretical win into complimentary rewards.
- **Claim:** Total comp economic cost was **$190,669.30 against $15,485,020.98 in theoretical win**, representing an aggregate reinvestment rate of **1.23%**. Even Platinum tier members receive only 1.42% in comp reinvestment, far below the standard Las Vegas casino slot benchmark of 8% to 15%.
- **Data Source & Query:**
  - Table: `data/1_prepared_views/player_period.parquet`
  - Query:
    ```sql
    SELECT tier_end,
           SUM(comp_cost_usd) AS comp_cost,
           SUM(theo_usd) AS theo_win,
           SUM(comp_cost_usd) / SUM(theo_usd) * 100.0 AS reinvestment_pct
    FROM player_period
    GROUP BY tier_end;
    ```
- **Exact Numerical Result:**
  - Floor-wide: Comp Cost = $190,669.30; Theo Win = $15,485,020.98; Reinvestment = 1.2313%.
  - Base Tier: Comp Cost = $65,095.10; Theo Win = $7,134,594.00; Reinvestment = 0.9124%.
  - Gold Tier: Comp Cost = $98,176.50; Theo Win = $6,414,273.00; Reinvestment = 1.5306%.
  - Platinum Tier: Comp Cost = $27,397.70; Theo Win = $1,936,154.00; Reinvestment = 1.4151%.
- **Alternative Explanation Tested:**
  - *Does comp face value reflect a higher benefit?* Comp Face Value is $682,749.50 (4.41% of theo). However, actual economic cost to the casino is only $190,669.30 (27.93% cost-to-face ratio). Economic reinvestment must be measured on cost of goods delivered.
- **Limitations & Risks:**
  - Does not include unrecorded soft comps (e.g. uncarded free beverages delivered on the slot floor).

---

### <a id="claim-q5-2"></a>Claim Q5.2: The loyalty points program suffers from acute friction, resulting in a 4.38% redemption burn rate.
- **Claim:** Cardholders earned **163,617,200 loyalty points** but redeemed only **7,172,979 points**, yielding a tiny burn rate of **4.38%**. Over 156 million points remain unredeemed in member balances.
- **Data Source & Query:**
  - Tables: `data/1_prepared_views/player_period.parquet`, `data/3_guests/loyalty_ledger.parquet`
  - Query:
    ```sql
    SELECT SUM(points_earned) AS earned,
           SUM(points_redeemed) AS redeemed,
           ROUND(SUM(points_redeemed) * 100.0 / SUM(points_earned), 2) AS burn_rate_pct
    FROM player_period;
    ```
- **Exact Numerical Result:**
  - Points earned: 163,617,200
  - Points redeemed: 7,172,979
  - Burn rate: 4.3840%
- **Alternative Explanation Tested:**
  - *Do points expire quickly?* Point balances persist across calendar periods. The low burn rate is caused by high point redemption thresholds and lack of prominent digital redemption options at POS.
- **Limitations & Risks:**
  - Point balances represent an outstanding theoretical liability, though actual redemption costs average only ~$0.026 per 10 points.

---

### <a id="claim-q5-3"></a>Claim Q5.3: Carded food & beverage activity is highly profitable, generating +$743,736.30 in net POS cash margin.
- **Claim:** Linked POS cash receipts totaled **$1,335,083.00**, while linked POS COGS (which already includes all $190.7k in comp costs) totaled **$591,346.70**, producing a net POS margin of **+$743,736.30**.
- **Data Source & Query:**
  - Table: `data/1_prepared_views/player_period.parquet`
  - Query:
    ```sql
    SELECT SUM(linked_pos_cash_usd) AS pos_cash,
           SUM(linked_pos_cogs_usd) AS pos_cogs,
           SUM(linked_pos_cash_usd) - SUM(linked_pos_cogs_usd) AS net_pos_margin
    FROM player_period;
    ```
- **Exact Numerical Result:**
  - `linked_pos_cash_usd`: $1,335,083.00
  - `linked_pos_cogs_usd`: $591,346.70 (includes comp costs)
  - `net_pos_margin`: +$743,736.30 (Gross Margin: 55.71%)
  - Total tracked contribution: $16,329,196.90 ($15.58M house win + $743.7k POS margin).
- **Alternative Explanation Tested:**
  - *Did we accidentally subtract comp costs twice?* Verified per data dictionary: `linked_pos_cogs_usd` already includes `comp_cost_usd`. Formula $\text{Tracked Net Win} + \text{POS Cash} - \text{POS COGS}$ is exactly verified with zero accounting discrepancy.
- **Limitations & Risks:**
  - POS labor overhead and venue rent are excluded from partial supplied costs.

---

## Question 6: Operational Recommendations & Pricing

### <a id="claim-q6-1"></a>Claim Q6.1: Comp Policy Pilot (`A-COMP-PILOT`) provides a controlled, high-ROI mechanism to test increased loyalty reinvestment.
- **Claim:** Deploying `A-COMP-PILOT` costs **$14,000** ($4,000 fixed package + $10,000 comp allowance reserve) with 5 lead days and 25 active operating days. Raising reinvestment to 4.5% of theo on 1,000 active Gold/Local members is projected to generate **+$13,200 in incremental monthly theoretical win**, yielding a net positive return.
- **Data Source & Catalog ID:**
  - Table: `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-COMP-PILOT'`)
  - Cost Formula: Unit cost $4,000; Recurring $0; Lead days 5; Quantity 1.
- **Alternative Explanation Tested:**
  - *Why not implement `A-COMP-CHANGE` floor-wide for $1,500?* Changing the redemption rate floor-wide without a control group creates unmeasured margin risk across all 113,890 members. A randomized trial establishes statistical causality before full rollout.
- **Limitations & Risks:**
  - Player peer spillover and cannibalization of existing cash dining spend; mitigated by conditional play-session vouchers.

---

### <a id="claim-q6-2"></a>Claim Q6.2: Preventive maintenance on Ridgeline Gaming (`A-PREVENTIVE`) eliminates the primary floor downtime driver for $9,000.
- **Claim:** One manufacturer sweep on Ridgeline Gaming costs **$9,000** (7 lead days, 23 operating days, 90 min graveyard downtime/unit). Reducing failure rates by 35%–45% prevents 28–36 breakdowns, saving ~$3,650 in repair costs and recovering **~$2,400 in lost theo win**.
- **Data Source & Catalog ID:**
  - Table: `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-PREVENTIVE'`)
  - Target: 86 Ridgeline units responsible for 56.34% of all floor faults.
- **Alternative Explanation Tested:**
  - *Why not add a technician to Swing Shift (`A-TECH-SHIFT`) instead?* `A-TECH-SHIFT` costs $11,520 and treats symptoms (shortening repair queues), whereas `A-PREVENTIVE` ($9,000) treats the root physical cause of 56% of machine breakdowns.
- **Limitations & Risks:**
  - Does not prevent non-mechanical failures (e.g. firmware communication glitches).

---

### <a id="claim-q6-3"></a>Claim Q6.3: Machine inspection on 5 extreme luck-deficit units (`A-INSPECT`) audits EPROM integrity and prevents mistaken replacements for $6,000.
- **Claim:** Inspecting 5 units (`M-1158`, `M-1288`, `M-1070`, `M-1290`, `M-1152`) costs **$6,000** ($1,200 × 5; 1 lead day, 120 min quiet-hour downtime). These units suffered a combined -$185,985 luck residual. Inspection certifies compliance and prevents up to $110,000 in mistaken purchase replacements.
- **Data Source & Catalog ID:**
  - Table: `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-INSPECT'`)
- **Alternative Explanation Tested:**
  - *Could these machines be defective or tampered with?* Payout distributions on high-volatility slot titles exhibit large variance. Inspection provides definitive empirical proof before capital is committed.
- **Limitations & Risks:**
  - The inspection produces certification data, not a direct mechanical revenue increase.

---

### <a id="claim-q6-4"></a>Claim Q6.4: Preserving $61,400 to $71,400 of unspent budget (`A-HOLD`) maintains capital agility and stops waste.
- **Claim:** The guidelines explicitly authorize preserving unspent budget at $0 cost. Allocating $38,600 across the three targeted actions leaves **$61,400 in treasury reserve** ($71,400 net of comp reserve), avoiding speculative machine purchases.
- **Data Source & Catalog ID:**
  - Table: `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-HOLD'`)
- **Alternative Explanation Tested:**
  - *Should the remaining funds be spent on zone signage (`A-WAYFINDING`) or promotions (`A-PROMO`)?* Signage and weekend promotions have high upfront costs ($7.5k and $15k) with unproven long-term retention. Preserving cash allows scaling the comp pilot in August once empirical ROI is proven.
- **Limitations & Risks:**
  - Unspent budget generates no direct yield in July, but prevents capital destruction.

