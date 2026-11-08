# Dashboard Royale Collaborative Project Notes (Append-Only)

---

## 2026-11-08 — Project Kickoff & Verification
- **Attendees:** Akshaya (Floor & ML Lead), Vaishnavi (Guest & BI Lead)
- **Actions:**
  - Reviewed `GUIDE.md`, `DATASET.md`, and `DATA_DICTIONARY.md`.
  - Executed data semantic verification script in pandas; all basic accounting identities on `player_period`, `property_day`, and `prepared_daily_view` verified with zero discrepancy (residuals $\le 10^{-10}$).
  - Agreed on shared definitions in `work/shared/CONTRACT.md`:
    - Player Net = Payout − Coin-in.
    - House Win = Coin-in − Payout.
    - Ratio of sums for all hold and reinvestment calculations.
    - Exclude 1,018 null-location rows from machine availability and performance rankings.
    - Comp cost is included in POS COGS; do not subtract twice.

---

## 2026-11-08 — Guest Analytics & Loyalty Investigation (Vaishnavi)
- **Findings on Questions 4 & 5:**
  - **Overall Play Breakdown:** Total Property Coin-in = $248,905,219.25; House Win = $23,638,155.10 (9.50% hold). Tracked coin-in = $163,804,869.65 (65.81% of property). Tracked house win = $15,585,460.60 (9.51% observed hold vs 9.45% theo hold).
  - **Player Luck Residual:** -$100,439.62. Tracked cardholders lost slightly more than expected by game math; the house ran slightly lucky on carded play.
  - **Player Wealth Concentration:** Extreme Pareto concentration. Top 1% (1,138 players) accounts for 22.85% of coin-in; Top 5% (5,694 players) accounts for 55.33% of coin-in; Top 10% accounts for 66.52% of coin-in. Gini coefficient is 0.754.
  - **Player Outcomes:** Out of 113,890 tracked members, 15,504 (13.61%) finished the 6-month period ahead with net positive winnings; 17,394 (15.27%) broke even; 80,992 (71.11%) experienced net losses.
  - **Demographic Driver:** Local players represent only 7,967 cardholders (7.0%), but drive **58.60% of all tracked coin-in ($95.99M)** and $8.94M in house win, averaging over $12,000 in coin-in per player.
  - **Loyalty Program Economics:**
    - Economic comp cost = $190,669.30 vs Comp Face Value = $682,749.50 (27.93% cost-to-face ratio: food & beverage COGS is only ~28 cents per $1.00 menu price).
    - Comp Reinvestment Rate = 1.23% ($190.7k cost / $15.48M theo win). Industry standard is 8% to 15%. This casino is drastically under-comping its players, especially high-tier cardholders.
    - Points Burn Rate = 4.38% (163,617,200 points awarded vs only 7,172,979 redeemed). Over 95% of earned loyalty points remain unredeemed due to friction or lack of awareness.
    - Linked POS Cash = $1,335,083.00 vs Linked POS COGS = $591,346.70. Food & beverage cash spend from carded players yields +$743,736.30 in net POS cash margin!

---

## 2026-11-08 — Floor Analysis & The "Bottom 10" Fallacy (Cross-Review)
- **Findings on Questions 1, 2, 3:**
  - Evaluated management's naive "Bottom 10" machine list based on house win.
  - Machine `M-1158` (Desert Gold) is #2 on management's hit list with only $15,796.25 in house win. But `M-1158` saw **$519,610.00 in coin-in** and **$51,961.00 in theoretical win**! Its observed hold was 3.04% vs 10.0% configured RTP-hold, generating an extreme negative luck residual of **-$36,164.75**. It is a high-volume player favorite that simply suffered bad luck. Replacing it would be an expensive blunder!
  - Machine `M-5076` (Royal Draw) was installed recently and only logged 1,170 available hours.
  - 8 of the 10 lowest-earning machines sit in **Back Forty**, which suffers from foot traffic starvation, not defective games.
  - Machine faults are heavily concentrated in **Ridgeline Gaming** (680 of 1,207 faults = 56.34% of all breakdowns).
  - Swing shift experiences 577 faults (47.8% of total) but has only a single technician on duty.

---

## 2026-11-08 — Operational Decisions & Deliverable Completion (Vaishnavi)
- **Decisions on Question 6 ($100,000 Budget):**
  - Reject machine replacements (purchasing 10 units = $220k, exceeding budget; leasing 10 units = $33.8k, discarding popular games).
  - Selected 3 high-ROI, targeted action types:
    1. `A-COMP-PILOT`: $4,000 package + $10,000 comp reserve = $14,000. 1,000-player RCT testing 4.5% comp reinvestment on active Local/Gold cardholders.
    2. `A-PREVENTIVE`: $9,000 sweep on all 86 Ridgeline units during graveyard quiet hours to eliminate 56% of machine breakdowns.
    3. `A-INSPECT`: $6,000 paytable inspection across top 5 luck-deficit machines (`M-1158`, `M-1288`, `M-1070`, `M-1290`, `M-1152`) to audit EPROM integrity.
    4. `A-HOLD`: Preserved $61,400 to $71,400 of unspent budget in treasury cash.
- **Deliverables Published:**
  - Generated `work/guests/out/player_month.parquet` (148,893 enriched player-month records).
  - Published `work/guests/out/action_shortlist.md` (comprehensive 9-criteria action profiles).
  - Generated `work/guests/out/guest_analytics.json` (structured precomputed multi-period data).
  - Built `dashboard/guests.html` (interactive player analytics, Lorenz curve, drill-downs).
  - Built `dashboard/actions.html` (interactive budget simulator, 9-point action profiles, evidence links).
  - Built `dashboard/index.html` (master executive portal integrating floor, guests, and actions).

---

## 2026-11-08 — Floor & ML Model Deliverables Finalized (Akshaya)
- **Completion of Questions 1, 2, 3 & ML Model:**
  - **Question 1 (Machine Performance):**
    - Complete evaluation of all 310 active units across exposure, coin-in, theo win, and luck residual.
    - Debunked management's naive "Bottom 10" house-win list:
      - Unit `M-1158` earned only $15,796.25 in house win but generated **$519,610.00 in coin-in** and **$51,961.00 in theoretical win**, crippled solely by an extreme negative luck residual of **-$36,164.75** (observed hold 3.04% vs 10.0% theo hold).
      - Unit `M-5076` was only active for 49 days (1,170 hours) after mid-May installation.
      - Unit `M-1118` was active for only 55 days (1,313.5 hours) before removal on Feb 24.
      - 8 of the 10 lowest-earning machines reside in **Back Forty**, where average coin-in per available hour is only **$122.31/hr** (vs $229.20/hr in Main Entrance and $218.85/hr in Center Pit), demonstrating location traffic starvation rather than bad game math.
  - **Question 2 (Demand Analysis):**
    - Proved that property-wide monthly coin-in remained highly stable between January and June ($39.6M to $43.6M/month).
    - Demonstrated massive weekly demand surges: Saturdays average **$1,842,510** in coin-in vs Tuesdays at **$1,012,314** (an $830,000 / +82.0% swing).
    - Regression analysis shows active events provide a transient +$138.4k/day lift ($p < 0.01$), whereas weather and monthly city visitation have negligible explanatory power once day-of-week and events are controlled for.
  - **Question 3 (Downtime Analysis):**
    - Floor-wide cumulative machine downtime reached **5,021.1 hours**, causing **$90,313.38 in lost theoretical win** and **$969,708.16 in lost coin-in**, plus **$212,945.21 in direct repair costs**.
    - Downtime is overwhelmingly concentrated in **Ridgeline Gaming**: 680 of 1,207 faults (56.34% of faults), 2,755.0 downtime hours (54.87%), and $48,921.28 in lost theo win (54.17%), with 7.2 faults/machine (double the rate of competitors).
    - Swing shift suffers 577 faults (47.8% of total) with 2,204.6 hours of downtime, severely bottlenecked by having only one technician on duty.
  - **Required ML Model:**
    - Trained strictly on Jan 1 – Apr 30, 2025 (120 days) and tested out-of-sample on May 1 – Jun 30, 2025 (61 days). Zero data leakage.
    - Constant Training Mean Baseline ($1,368,421.15/day) Test MAE: **$218,258.10**.
    - Day-of-Week Stratified Model Test MAE: **$68,698.55**.
    - Achieved an exact **68.52% reduction in prediction error**.
    - Model provides direct operational value for July: aligns technician and floor attendant rosters with the +$830k Saturday surge to prevent downtime bottlenecks.
- **Deliverables Published:**
  - Published `work/floor/out/machine_scorecard.parquet` (310 machine records with exposure, rates per available hour, ranks, and recommendations).
  - Published `work/floor/out/demand_daily.parquet` (181 daily property records with train/test splits, predictions, and errors).
  - Published `work/floor/out/model_card.md` (complete ML specification, leakage controls, residual diagnostics, and staffing impact).
  - Built `dashboard/floor.html` (fully responsive, standalone interactive dashboard with 3-period filtering, zone-to-bank drill-down, SVG forecast charts, downtime diagnostics, and searchable/sortable scorecard).


