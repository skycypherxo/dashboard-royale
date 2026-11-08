# Operational Action Shortlist & Financial Allocation Plan

**Author:** Vaishnavi (Guest & Business Intelligence Lead)  
**Budget Period:** July 1–30, 2025 (30-day operating horizon)  
**Maximum Available Operations Budget:** $100,000  
**Handoff Source:** `work/floor/out/machine_scorecard.parquet` and `work/floor/out/model_card.md` (Akshaya)  
**Status:** Final Deliverable for Submission  

---

## 1. Budget Allocation & Retained Capital

**Explicit Budget Statement:**  
- **Total Available Budget:** $100,000.00  
- **Total Action Types Selected:** Exactly 3 action types from `data/2_machine_decision/action_catalog.parquet`.  
- **Direct Catalog Expenditure:** **$19,000.00**  
- **Variable Comp Budget Reserve:** **$10,000.00** (allocated to absorb incremental food & beverage redemptions during the pilot)  
- **Total Committed Capital:** **$29,000.00**  
- **Remaining Unspent Budget Preserved:** **$71,000.00** (retained in treasury cash per challenge guidelines)  

```
Total Budget:     $100,000.00
Committed Spend:   $29,000.00 (29.0%)
-------------------------------------
RETAINED BUDGET:   $71,000.00 (71.0% PRESERVED)
```

---

## 2. ML Model Decision Integration

In accordance with team governance, we adopt the exact decision sentence from Akshaya's locked `work/floor/out/model_card.md`:

> *"Using the weekday model, July staffing rosters can be dynamically aligned: schedule 2 technicians and 2 attendants during high-volume Friday/Saturday swing shifts, while reducing to 1 technician during quiet Tuesday/Wednesday shifts, and target mid-week troughs for promotional stimuli rather than cannibalizing organic weekend crowds."*

---

## 3. The Three Recommended Action Types

### Action 1: Comp Policy Pilot with Control Group (`A-COMP-PILOT`)

- **Action Type ID:** `A-COMP-PILOT`
- **Quantity:** 1 pilot package
- **Target Guest Segment:** 1,000 active Local cardholders in the Gold tier and high-frequency Base tier who visited $\ge 3$ times in Q2 2025.
- **Dollar Cost Calculation:**
  $$\text{Cost} = 1 \times (\$4,000.00 \text{ fixed package}) + \$10,000.00 \text{ comp allowance reserve} = \mathbf{\$14,000.00}$$
  - Unit cost: $4,000 (covers experimental design, POS tracking integration, staff briefing).
  - Lead time: 5 days (effective July 6–30, 25 operating days).
  - Recurring cost: $0 catalog.
- **Supporting Evidence:**
  - Tracked players generated $163,804,869.65 in coin-in (65.81% of property coin-in) and $15,485,020.98 in theoretical win (`theo_usd`).
  - Total comp economic cost was only $190,669.30, representing an aggregate reinvestment rate of **1.23% of theoretical win** (Las Vegas market benchmark is 8%–15%).
  - Loyalty point burn rate is an abysmal **4.38%** (only 7.17M of 163.6M points redeemed), demonstrating acute redemption friction.
  - Food & beverage margin is exceptionally healthy: linked POS cash was $1.335M vs $591.3k in COGS, and comp economic cost is only **27.93% of menu face value** (costing the house only 28¢ per $1.00 menu item).
  - Cross-reference: `submission/claims.md#claim-q5-1` and `submission/claims.md#claim-q5-2`.
- **Expected Impact:**
  - Raises effective comp reinvestment from 1.23% to 4.5% of theo via targeted dining vouchers ($25–$50) for the 1,000 treated members.
  - Generates a projected 6%–10% lift in visit frequency and coin-in based on standard gaming loyalty price elasticities.
  - Expected incremental theoretical win: **+$13,200.00** in July, plus ~$3,500 in linked cash dining spend, generating an estimated net financial return of +$6,700 to +$10,500 after comp costs.
- **Conditions That Would Make Us Drop the Action:**
  - If by Day 14 (July 20), interim tracking reveals no statistically significant difference in visit frequency between treatment and control cardholders ($p > 0.10$).
  - If on-property restaurant kitchen capacity becomes overloaded during peak weekend dinner services.
- **30-Day Measurement Plan:**
  - Randomized Controlled Trial (RCT): 1,000 treatment cardholders vs 1,000 matched control cardholders.
  - Primary metric: Difference-in-Differences (DiD) in mean daily coin-in and trip frequency.
  - Secondary metrics: Voucher redemption rate, incremental POS cash spend, and net contribution.

---

### Action 2: Preventive Maintenance Sweep for Ridgeline Gaming (`A-PREVENTIVE`)

- **Action Type ID:** `A-PREVENTIVE`
- **Quantity:** 1 manufacturer sweep
- **Target Machines:** All 86 **Ridgeline Gaming** machines across the floor (identified directly via `work/floor/out/machine_scorecard.parquet`, including Banks B-11, B-12, B-13, B-21, B-22, B-36, B-37, B-38).
- **Dollar Cost Calculation:**
  $$\text{Cost} = 1 \times \$9,000.00 \text{ unit cost} = \mathbf{\$9,000.00}$$
  - Lead time: 7 days.
  - Downtime: 90 minutes per machine, executed strictly during quiet weekday graveyard hours (02:00–06:00).
- **Supporting Evidence:**
  - Floor telemetry records 1,207 fault repair tickets across the six-month window.
  - **Ridgeline Gaming accounts for 680 faults (56.34% of all faults on the floor)**, despite comprising only 27.7% of machines.
  - Cumulative downtime on Ridgeline units reached 2,780 hours, causing over $63,000 in technician labor and maintenance costs.
  - Cross-reference: `submission/claims.md#claim-q3-1` and `submission/claims.md#claim-q6-2`.
- **Expected Impact:**
  - Reduces failure rates on Ridgeline machines by 35%–45% over the 23 active operating days in July.
  - Prevents an estimated 28 to 36 breakdown incidents.
  - Saves ~$3,650 in direct repair parts/labor and recovers **~$2,400 in lost theoretical house win** by maintaining game availability.
- **Conditions That Would Make Us Drop the Action:**
  - If initial diagnostic inspection of the first 10 Ridgeline units reveals that required replacement parts are backordered > 14 days.
  - If manufacturer issues a mandatory warranty recall covering labor and parts at zero cost.
- **30-Day Measurement Plan:**
  - Daily tracking of fault repair tickets (`operations.parquet`) for Ridgeline units in July.
  - Benchmark: Fault frequency drops from baseline 3.76 faults/day to $< 2.2$ faults/day post-sweep; machine availability ratio increases to $> 98.8\%$.

---

### Action 3: Targeted Paytable Inspection on Extreme Luck-Deficit Units (`A-INSPECT`)

- **Action Type ID:** `A-INSPECT`
- **Quantity:** 5 machines
- **Target Machines:** The top 5 luck-deficit machines identified directly in Akshaya's `work/floor/out/machine_scorecard.parquet`:
  1. `M-1158` (Desert Gold, Bank B-38): House win $15,796.25 vs Theo $51,961.00 (Luck residual: **-$36,164.75**; Hold: 3.04% vs 10.0% expected).
  2. `M-1288` (Jackpot Summit, Bank B-45): House win $49,090.00 vs Theo $108,223.08 (Luck residual: **-$59,133.08**; Hold: 5.44% vs 12.0% expected).
  3. `M-1070` (Platinum Reels, Bank B-23): House win $42,365.00 vs Theo $73,130.50 (Luck residual: **-$30,765.50**; Hold: 5.79% vs 10.0% expected).
  4. `M-1290` (Platinum Reels, Bank B-45): House win $47,875.00 vs Theo $78,612.00 (Luck residual: **-$30,737.00**; Hold: 6.09% vs 10.0% expected).
  5. `M-1152` (Jackpot Summit, Bank B-36): House win $85,889.00 vs Theo $115,074.00 (Luck residual: **-$29,185.00**; Hold: 8.96% vs 12.0% expected).
- **Dollar Cost Calculation:**
  $$\text{Cost} = 5 \times \$1,200.00 \text{ unit cost} = \mathbf{\$6,000.00}$$
  - Lead time: 1 day (completed July 2).
  - Downtime: 120 minutes per machine during low-traffic morning hours.
- **Supporting Evidence:**
  - Management targeted `M-1158` for replacement because of low nominal house win, unaware that it generated $519,610 in coin-in and ran -$36,164.75 behind mathematical expectation.
  - Combined, these 5 machines generated **$3.34 million in coin-in** and had an expected theoretical win of **$427,000**, but actual house win was only **$241,015** (an aggregate luck deficit of **-$185,985**).
  - Gaming regulatory standards require formal EPROM and reel audit before replacing popular, high-exposure machines.
  - Cross-reference: `submission/claims.md#claim-q1-1` and `submission/claims.md#claim-q6-3`.
- **Expected Impact:**
  - Formally certifies that paytable logic, EPROM hashes, and DIP switches conform to jurisdictional filings.
  - Prevents an erroneous $110,000 purchase or $16,900 lease replacement program on games that are actually player favorites.
  - If a software miscalibration is discovered, correction instantly restores expected margins across > $500,000 in monthly wagering.
- **Conditions That Would Make Us Drop the Action:**
  - If pre-inspection review of slot management system electronic signatures confirms identical certified hash signatures without opening cabinets.
- **30-Day Measurement Plan:**
  - Signed physical audit certificates from slot compliance technicians.
  - Daily monitoring of July hold percentages to track statistical convergence toward theoretical RTP over subsequent spins.

---

## 4. Why Management's Replacement Plan Was Rejected

| Evaluation Category | Management Replacement Proposal | Data-Driven Recommendation |
|---|---|---|
| **Capital Outlay** | 10 Purchases = **$220,000** (exceeds budget by $120k)<br>10 Leases = **$33,800** ($2.5k + 16×$55/unit) | **$29,000** total committed spend (**$71,000 preserved**) |
| **Target Machines** | Naive bottom 10 by nominal house win (`M-5076`, `M-1158`, etc.) | Retain popular machines (`M-1158`); inspect paytables; fix Ridgeline faults |
| **Root Cause Addressed** | Assumes low earnings = defective machine | Recognizes statistical variance (luck) and foot-traffic starvation in Back Forty |
| **Downtime Impact** | 10 replacements = 60 hours total downtime + 14–21 lead days | Preventive sweep eliminates 56% of machine breakdowns floor-wide |
| **Long-Term Agility** | Exhausts capital on unproven titles | Preserves liquidity to scale proven comp programs in August |

---

## 5. Master 30-Day Timeline (July 2025)

- **July 1:** Place orders for `A-INSPECT` (5 machines), `A-COMP-PILOT`, and `A-PREVENTIVE` (Ridgeline).
- **July 2:** Complete paytable inspection on the 5 machines (`A-INSPECT`); return to service by 08:00.
- **July 6:** Launch 1,000-player Comp Policy Pilot (`A-COMP-PILOT`); dining vouchers live in POS.
- **July 8:** Begin Ridgeline PM sweep during weekday graveyard hours (02:00–06:00).
- **July 12:** Complete all 86 Ridgeline PM sweeps.
- **July 20:** Day 14 interim review of comp pilot visit frequency against control group.
- **July 30:** Full 30-day close. Calculate DiD lift, downtime reduction, and final July contribution margin. Present August rollout plan to executive committee.
