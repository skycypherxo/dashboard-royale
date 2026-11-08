# Appendix: Claims and Evidence

**Challenge:** Dashboard Royale (TAMU Datathon 2026)  
**Authors:** Vaishnavi (Guest & Business Intelligence Lead) & Akshaya (Floor & ML Lead)  
**Scope:** Complete evidentiary traceability for all empirical assertions across Questions 1 through 6.

---

## Question 1: Machine Performance & The "Bottom 10" Fallacy

### Claim 1.1
Management's lowest-earning machine list misidentifies popular, high-exposure machines as failures due to negative luck residuals.

- **Owner:** Akshaya
- **Table:** `data/1_prepared_views/prepared_daily_view.parquet`
- **Query or notebook:** `work/floor/generate_floor_models.py`
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
- **Result:** Machine `M-1158` (Desert Gold, Bank B-38, Back Forty) is ranked #2 on management's bottom-earning list ($15,796.25 in house win), but generated $519,610.00 in coin-in and $51,961.00 in theoretical win. Its low win was caused entirely by a -$36,164.75 luck residual (observed hold of 3.04% vs 10.0% configured RTP-hold). Total available hours was 4,319.4 hours (99.45% availability) with zero fault tickets.
- **Alternative explanation tested:** Tested whether `M-1158` suffered from high downtime or offline meters. Analysis showed 99.45% availability and normal occupancy; the deviation is pure paytable jackpot variance.
- **Limitation:** High-volatility slot mathematics allow wide sample variance over finite spins; paytable verification (`A-INSPECT`) is required to certify EPROM integrity.

---

### Claim 1.2
Eight of the ten lowest-earning machines suffer from location foot-traffic starvation in Back Forty, not defective game math.

- **Owner:** Akshaya
- **Table:** `data/1_prepared_views/prepared_daily_view.parquet`, `data/4_context/zone_traffic_hourly.parquet`
- **Query or notebook:** `work/floor/generate_floor_models.py`
  ```sql
  SELECT zone_name,
         AVG(coin_in_usd / NULLIF(available_hours, 0)) AS avg_coin_in_per_avail_hour,
         SUM(coin_in_usd) AS total_coin_in
  FROM prepared_daily_view
  WHERE location_id IS NOT NULL
  GROUP BY zone_name
  ORDER BY avg_coin_in_per_avail_hour ASC;
  ```
- **Result:** Back Forty average coin-in per available machine hour is $122.31/hr, compared to $229.20/hr in Main Entrance, $218.85/hr in Center Pit, and $189.83/hr in Bar Row. Eight of the ten bottom machines (`M-5076`, `M-1158`, `M-1120`, `M-1238`, `M-1181`, `M-1035`, `M-1179`, `M-1265`) sit in Back Forty.
- **Alternative explanation tested:** Tested whether Back Forty titles are intrinsically unpopular. The identical game titles (`Royal Draw`, `Comet Cash`) placed in Center Pit generate over $220/hour in coin-in, proving location starvation rather than game unpopularity.
- **Limitation:** Moving entire machine banks requires $9,500 per bank and causes 480 minutes of floor downtime.

---

## Question 2: Demand Analysis & Machine Learning

### Claim 2.1
Casino floor demand exhibits pronounced weekly periodicity with weekend peaks, while monthly aggregates remained stable between January and June.

- **Owner:** Akshaya
- **Table:** `data/1_prepared_views/property_day.parquet`
- **Query or notebook:** `work/floor/generate_floor_models.py`
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
- **Result:** Total daily coin-in averaged $1,375,166.96 across 181 days ($248,905,219.25 total coin-in, $23,638,155.10 house win, 9.50% hold). Saturdays peaked at $1,842,510.40 mean coin-in, while Tuesdays troughed at $1,012,314.15 mean coin-in (an 82.0% volume surge).
- **Alternative explanation tested:** Tested whether weather or city conventions explained day-to-day fluctuations. Regression confirmed that event weekends produced transient +14% lifts, but day-of-week seasonality explained > 70% of variance.
- **Limitation:** Zone traffic counters suffered intermittent offline gaps (`counter_status`), requiring reliance on machine meters.

---

### Claim 2.2
Day-of-week demand stratification reduces out-of-sample coin-in prediction error by 68.52% without data leakage.

- **Owner:** Akshaya
- **Table:** `work/floor/out/demand_daily.parquet`
- **Query or notebook:** `work/floor/generate_floor_models.py`
  ```sql
  SELECT AVG(ABS(coin_in_usd - pred_baseline_coin)) AS mae_baseline,
         AVG(ABS(coin_in_usd - pred_weekday_coin)) AS mae_weekday,
         (AVG(ABS(coin_in_usd - pred_baseline_coin)) - AVG(ABS(coin_in_usd - pred_weekday_coin)))
         / AVG(ABS(coin_in_usd - pred_baseline_coin)) * 100.0 AS error_reduction_pct
  FROM demand_daily
  WHERE NOT is_train;
  ```
- **Result:** The baseline constant mean model trained on Jan 1 – Apr 30 produced an out-of-sample test MAE of **$218,258.10** on May 1 – Jun 30. The weekday-stratified model achieved an out-of-sample test MAE of **$68,698.55**, reducing prediction error by **68.52%**.
- **Alternative explanation tested:** Evaluated whether test holdout data leaked into training. All conditional means were computed strictly on the 120 training days before May 1, 2025; no future data or post-2025 tourism reports were used.
- **Limitation:** Model assumes stationary intra-week seasonality and does not predict rare unannounced macro shocks.

---

## Question 3: Downtime & Operational Bottlenecks

### Claim 3.1
Equipment failures are heavily concentrated in Ridgeline Gaming machines and Swing Shift, generating $90.3k in lost theoretical win floor-wide.

- **Owner:** Akshaya
- **Table:** `data/2_machine_decision/operations.parquet`, `data/1_prepared_views/prepared_daily_view.parquet`
- **Query or notebook:** `work/floor/generate_floor_models.py`
  ```sql
  SELECT manufacturer,
         COUNT(*) AS faults_opened,
         ROUND(COUNT(*) * 100.0 / 1207, 2) AS fault_share_pct
  FROM prepared_daily_view
  WHERE location_id IS NOT NULL AND faults_opened > 0
  GROUP BY manufacturer;
  ```
- **Result:** Ridgeline Gaming units caused **680 out of 1,207 faults (56.34%)**, 2,755.0 downtime hours (54.87%), and $48,921.28 in lost theo win. Swing Shift recorded 577 faults (47.80%) with only one technician on duty. Floor-wide cumulative downtime reached 5,021.1 hours and $90,313.38 in lost theo win.
- **Alternative explanation tested:** Tested whether Ridgeline constitutes the majority of floor units. Ridgeline represents only 27.7% of machines; its failure rate (7.91 faults/unit) is more than triple Halcyon (2.13) or Northwind (3.24).
- **Limitation:** Open-to-available duration includes queue waiting time before technician arrival.

---

## Question 4: Player Analytics & Concentration

### Claim 4.1
<a id="claim-q4-1"></a>
Tracked loyalty cardholders drive 65.81% of property coin-in and exhibit extreme Pareto wealth concentration.

- **Owner:** Vaishnavi
- **Table:** `data/1_prepared_views/player_period.parquet`, `work/guests/out/player_month.parquet`
- **Query or notebook:** `work/guests/compute_guest_metrics.py`
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
- **Result:** 113,890 tracked cardholders generated **$163,804,869.65 in coin-in (65.81% of property total)**, received $148,219,409.05 in payouts, and had a net result of **-$15,585,460.60 (house win: $15,585,460.60, hold: 9.51% vs 9.45% theo)**. Top 1% of players generated 22.85% of coin-in; Top 5% generated 55.33%; Gini coefficient is **0.754**.
- **Alternative explanation tested:** Tested whether losses were uniform. 15,504 players (13.61%) finished ahead with net positive winnings; 17,394 (15.27%) broke even; 80,992 (71.11%) had net losses.
- **Limitation:** Data describes carded play only; uncarded anonymous gamblers contribute the remaining 34.19% ($85.10M) of coin-in.

---

### Claim 4.2
<a id="claim-q4-2"></a>
Local cardholders represent the economic backbone of the casino, generating 58.60% of tracked coin-in despite being only 7.0% of the player population.

- **Owner:** Vaishnavi
- **Table:** `data/1_prepared_views/player_period.parquet`
- **Query or notebook:** `work/guests/compute_guest_metrics.py`
  ```sql
  SELECT home_region,
         COUNT(DISTINCT player_id) AS player_count,
         SUM(tracked_coin_in_usd) AS coin_in,
         SUM(tracked_coin_in_usd) / 163804869.65 * 100.0 AS coin_share_pct,
         SUM(tracked_coin_in_usd) / COUNT(DISTINCT player_id) AS coin_per_player
  FROM player_period
  GROUP BY home_region
  ORDER BY coin_in DESC;
  ```
- **Result:** Local cardholders (7,967 players) generated **$95,992,384.30 in coin-in (58.60% of all tracked coin-in)**, averaging $12,048.75 in coin-in per player over 6 months, compared to $656.00 for Regional and $626.60 for Domestic patrons.
- **Alternative explanation tested:** Tested whether tourists spent more per visit. Tourists had higher coin-in per trip, but locals visited far more often (14.8 visits vs 1.4 visits), driving massive cumulative customer lifetime value.
- **Limitation:** Home regions are coarse geographic categories captured at loyalty enrollment.

---

## Question 5: Loyalty, Comps & Reinvestment

### Claim 5.1
<a id="claim-q5-1"></a>
The casino severely under-comps its tracked players, reinvesting only 1.23% of theoretical win into complimentary rewards.

- **Owner:** Vaishnavi
- **Table:** `data/1_prepared_views/player_period.parquet`, `work/guests/out/player_month.parquet`
- **Query or notebook:** `work/guests/compute_guest_metrics.py`
  ```sql
  SELECT tier_end,
         SUM(comp_cost_usd) AS comp_cost,
         SUM(theo_usd) AS theo_win,
         SUM(comp_cost_usd) / SUM(theo_usd) * 100.0 AS reinvestment_pct
  FROM player_period
  GROUP BY tier_end;
  ```
- **Result:** Total comp economic cost was **$190,669.30 against $15,485,020.98 in theoretical win**, representing an aggregate reinvestment rate of **1.23%**. Base tier was 0.91%, Gold was 1.53%, and Platinum was 1.42%—all far below the standard Las Vegas benchmark of 8% to 15%.
- **Alternative explanation tested:** Tested whether comp face value ($682,749.50) represented higher benefit. Economic cost to the casino is only $190,669.30 (27.93% cost-to-face ratio); food & beverage COGS is only ~28¢ per $1.00 menu item.
- **Limitation:** Soft uncarded floor beverages are excluded from electronic tracking.

---

### Claim 5.2
<a id="claim-q5-2"></a>
The loyalty points program suffers from acute friction, resulting in a 4.38% redemption burn rate.

- **Owner:** Vaishnavi
- **Table:** `data/1_prepared_views/player_period.parquet`, `data/3_guests/loyalty_ledger.parquet`
- **Query or notebook:** `work/guests/compute_guest_metrics.py`
  ```sql
  SELECT SUM(points_earned) AS earned,
         SUM(points_redeemed) AS redeemed,
         ROUND(SUM(points_redeemed) * 100.0 / SUM(points_earned), 2) AS burn_rate_pct
  FROM player_period;
  ```
- **Result:** Cardholders earned **163,617,200 loyalty points** but redeemed only **7,172,979 points**, yielding a tiny burn rate of **4.38%**. Over 156 million points remain unredeemed in member balances.
- **Alternative explanation tested:** Tested whether points expired prematurely. Points persist across periods; low redemption is driven by high threshold barriers and limited digital redemption integration at POS.
- **Limitation:** Outstanding points represent an unredeemed balance liability, though actual economic cost per 10 points is only ~$0.026.

---

### Claim 5.3
<a id="claim-q5-3"></a>
Carded food & beverage activity is highly profitable, generating +$743,736.30 in net POS cash margin.

- **Owner:** Vaishnavi
- **Table:** `data/1_prepared_views/player_period.parquet`
- **Query or notebook:** `work/guests/compute_guest_metrics.py`
  ```sql
  SELECT SUM(linked_pos_cash_usd) AS pos_cash,
         SUM(linked_pos_cogs_usd) AS pos_cogs,
         SUM(linked_pos_cash_usd) - SUM(linked_pos_cogs_usd) AS net_pos_margin
  FROM player_period;
  ```
- **Result:** Linked POS cash receipts totaled **$1,335,083.00**, while linked POS COGS (which already includes all $190.7k in comp costs) totaled **$591,346.70**, producing a net POS cash margin of **+$743,736.30** (55.71% gross margin) and total tracked contribution of **$16,329,196.90**.
- **Alternative explanation tested:** Verified that comp cost was not subtracted twice. Per data dictionary rules, comp cost is already inside POS COGS; formula $\text{Tracked House Win} + \text{POS Cash} - \text{POS COGS}$ is verified with zero accounting residual.
- **Limitation:** Excludes venue rent and fixed operational labor overhead.

---

## Question 6: Operational Recommendations & Pricing

### Claim 6.1
<a id="claim-q6-1"></a>
Comp Policy Pilot (`A-COMP-PILOT`) provides a controlled, high-ROI mechanism to test increased loyalty reinvestment.

- **Owner:** Vaishnavi
- **Table:** `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-COMP-PILOT'`)
- **Query or notebook:** `work/guests/out/action_shortlist.md`
- **Result:** Deploying `A-COMP-PILOT` costs **$14,000.00** ($4,000 fixed package + $10,000 comp allowance reserve) with 5 lead days and 25 active operating days. Raising reinvestment to 4.5% of theo on 1,000 active Gold/Local members is projected to generate **+$13,200 in incremental monthly theoretical win**, yielding a net positive return.
- **Alternative explanation tested:** Evaluated implementing floor-wide rate change (`A-COMP-CHANGE`, $1,500). Floor-wide rollout without an A/B control group creates unmeasured margin dilution risk across all 113,890 members; randomized trial establishes causal lift first.
- **Limitation:** Risk of dining cash spend cannibalization; mitigated by conditional play-session vouchers.

---

### Claim 6.2
<a id="claim-q6-2"></a>
Preventive maintenance on Ridgeline Gaming (`A-PREVENTIVE`) eliminates the primary floor downtime driver for $9,000.

- **Owner:** Vaishnavi (citing Akshaya's `work/floor/out/machine_scorecard.parquet`)
- **Table:** `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-PREVENTIVE'`)
- **Query or notebook:** `work/guests/out/action_shortlist.md`
- **Result:** One manufacturer sweep on Ridgeline Gaming costs **$9,000.00** (7 lead days, 23 operating days, 90 min graveyard downtime/unit). Reducing failure rates by 35%–45% prevents 28–36 breakdowns, saving ~$3,650 in repair costs and recovering **~$2,400 in lost theo win**.
- **Alternative explanation tested:** Evaluated adding a technician to Swing Shift (`A-TECH-SHIFT`, $11,520). `A-TECH-SHIFT` treats symptoms (queue times), whereas `A-PREVENTIVE` ($9,000) treats the root physical cause of 56% of machine breakdowns.
- **Limitation:** Does not prevent non-mechanical software/communication glitches.

---

### Claim 6.3
<a id="claim-q6-3"></a>
Machine inspection on 5 extreme luck-deficit units (`A-INSPECT`) audits EPROM integrity and prevents mistaken replacements for $6,000.

- **Owner:** Vaishnavi (citing Akshaya's `work/floor/out/machine_scorecard.parquet`)
- **Table:** `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-INSPECT'`)
- **Query or notebook:** `work/guests/out/action_shortlist.md`
- **Result:** Inspecting 5 units (`M-1158`, `M-1288`, `M-1070`, `M-1290`, `M-1152`) costs **$6,000.00** ($1,200 × 5; 1 lead day, 120 min quiet-hour downtime). These units suffered a combined -$185,985 luck residual. Inspection certifies compliance and prevents up to $110,000 in mistaken purchase replacements.
- **Alternative explanation tested:** Tested whether machines could be defective or tampered with. High-volatility slot titles exhibit natural variance; inspection provides definitive proof before capital commitment.
- **Limitation:** Produces diagnostic verification rather than direct mechanical revenue uplift.

---

### Claim 6.4
<a id="claim-q6-4"></a>
Preserving $71,000 of unspent budget (`A-HOLD`) maintains capital agility and stops waste.

- **Owner:** Vaishnavi
- **Table:** `data/2_machine_decision/action_catalog.parquet` (`action_type_id = 'A-HOLD'`)
- **Query or notebook:** `work/guests/out/action_shortlist.md`
- **Result:** Allocating $29,000 across the three targeted actions leaves **$71,000.00 in treasury reserve** ($81,000 net of comp reserve), avoiding speculative machine purchases.
- **Alternative explanation tested:** Evaluated spending remaining funds on zone signage (`A-WAYFINDING`, $7.5k) or promotions (`A-PROMO`, $15k). Preserving cash allows scaling the comp pilot in August once empirical ROI is proven.
- **Limitation:** Preserved budget earns $0 direct yield in July, but prevents capital destruction.
