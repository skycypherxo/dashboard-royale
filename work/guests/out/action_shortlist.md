# Operational Action Shortlist & Financial Allocation Plan

**Author:** Vaishnavi (Guest & Business Intelligence Lead)  
**Budget Horizon:** July 1 – July 30, 2025 (30-day operating horizon)  
**Available Operations Budget:** $100,000  
**Status:** Approved for Submission  

---

## Executive Summary

Management's initial plan was to replace the **10 lowest-earning slot machines** by total house win over the January–June 2025 window. Our analytical investigation across machine-level coin-in, theoretical win ($\text{theo}$), luck residual ($\text{house\_win} - \text{theo}$), downtime, foot traffic, and loyalty cardholder behaviors demonstrates that **replacing these 10 machines would be an expensive operational blunder**:

1. **The "Bottom 10" Are Not Broken**: Machines like `M-1158` (Desert Gold) earned only $15,796.25 in house win, but generated **$519,610.00 in coin-in** and **$51,961.00 in theoretical win**. Its observed hold was 3.04% against a configured 10.0% RTP-hold, representing an extreme negative luck residual of **-$36,164.75** (players hit an unusual winning streak). It is actually one of the most played machines on the floor. Replacing it with purchased machines ($22,000 each = $220,000, exceeding budget) or leases ($3,380 each) would discard a top revenue generator.
2. **Location Starvation, Not Machine Failure**: Eight of the ten lowest-earning machines sit in the **Back Forty** zone, which suffers from low foot traffic rather than defective games.
3. **Severe Loyalty Under-Comping**: Tracked cardholders generate **65.81% of property coin-in ($163.8M)** and **$15.58M in house win**, but the casino's complimentary reinvestment rate is an astonishingly low **1.23% of theoretical win** (industry benchmarks range from 8% to 15%). Furthermore, loyalty points have a tiny **4.38% redemption rate**, signaling severe program friction.
4. **Targeted Operational Fixes**: Machine breakdowns are heavily concentrated in a single manufacturer (**Ridgeline Gaming**, responsible for 56.3% of all faults: 680 tickets) and during **Swing Shift** (47.8% of faults: 577 tickets), which has only a single technician on duty.

We recommend deploying **three targeted action types** totaling **$28,600** (or **$38,600** including a $10,000 variable comp reserve), while **preserving $61,400 to $71,400 of the unspent budget** in accordance with challenge guidelines.

---

## Portfolio Budget Summary

| Action Type ID | Action Name | Target | Quantity | Unit Cost | Lead Days | Operating Days | Total Cost |
|---|---|---|---|---|---|---|---|
| `A-COMP-PILOT` | Comp Policy Pilot with Control Group | 1,000 Active Local/Gold Cardholders | 1 pilot | $4,000 | 5 | 25 | $4,000 (+$10,000 comp reserve = $14,000) |
| `A-PREVENTIVE` | Preventive Maintenance Sweep | Ridgeline Gaming (86 machines) | 1 sweep | $9,000 | 7 | 23 | $9,000 |
| `A-INSPECT` | Machine Inspection & Paytable Verification | Top 5 Luck-Deficit Machines (`M-1158`, `M-1288`, `M-1070`, `M-1290`, `M-1152`) | 5 machines | $1,200 | 1 | 29 | $6,000 |
| `A-HOLD` | Preserve Unspent Budget | Treasury / Reserve | — | $0 | 0 | 30 | $71,000 ($61,400 net of comp reserve) |
| **Total** | | | | | | | **$100,000** |

*Alternative Action Evaluated:* `A-TECH-SHIFT` (Add 1 technician to Swing Shift for 30 days: $11,520). See Section 4 for trade-off analysis.

---

## Detailed Action Profiles (9 Required Criteria)

### Recommendation 1: Comp Policy Pilot with Control Group (`A-COMP-PILOT`)

1. **Action Type**: `A-COMP-PILOT` (Comp policy pilot with control group).
2. **Quantity**: 1 pilot package.
3. **Target Guest Segments**: 1,000 active Local cardholders in the Gold tier and high-frequency Base tier who visited $\ge 3$ times in Q2 2025.
4. **Estimated Cost**:
   - Fixed package cost: **$4,000** (covers experimental design, system tracking, and staff training).
   - Lead time: 5 days (effective July 6–30, 25 operating days).
   - Variable comp allowance reserve: **$10,000** (budgeted from unspent funds).
   - Total Committed Cost: **$14,000**.
5. **Supporting Evidence**:
   - Tracked players generated $163,804,869.65 in coin-in (65.81% of property total) and $15,485,020.98 in theoretical win.
   - Economic comp reinvestment is currently **1.23%** ($190,669.30 comp cost / $15.48M theo). In Las Vegas, standard competitive reinvestment for slots is 10%–15%.
   - Over 95% of earned loyalty points remain unredeemed (4.38% burn rate), indicating low perceived value or high redemption hurdles.
   - F&B operations have a strong gross margin (linked POS cash was $1.335M vs $591k COGS, yielding $743.7k positive margin). Food & beverage economic cost is only 27.93% of face menu value ($1 of comp voucher costs the house only 28 cents).
6. **Expected Effect**:
   - The pilot tests raising effective comp reinvestment from 1.23% to 4.5% of theo via targeted dining vouchers for the treatment group ($25–$50 food vouchers at on-property restaurants).
   - Expected 6%–10% lift in visit frequency and coin-in among treated players based on standard gaming loyalty elasticities.
   - At a 7% visit lift, 1,000 target players generate an incremental ~$140,000 in coin-in and **~$13,200 in incremental theoretical win**, plus ~$3,500 in linked cash F&B sales. Net incremental contribution to the house: **+$6,700 to +$10,500** in July alone, establishing proof of concept for floor-wide optimization.
7. **Uncertainty and Risks**:
   - *Cannibalization Risk*: Players might consume comped dining without playing additional spins. (Mitigated by distributing vouchers conditional on active play sessions).
   - *Control Contamination*: Word-of-mouth between local patrons could cause dissatisfaction in the control group. (Mitigated by framing the promotion as a randomized "Player Appreciation Surprise").
8. **Conditions to Abandon**:
   - If after 14 operating days (July 20), the treatment group shows no statistically significant increase in visit frequency or coin-in compared to the control group ($p > 0.10$).
   - If voucher redemption causes restaurant kitchen capacity overloads during peak weekend dinner hours.
9. **30-Day Measurement Plan**:
   - Randomized Controlled Trial (RCT): 1,000 treatment players vs. 1,000 randomized synthetic-control cardholders matched on Q1-Q2 trip frequency and baseline coin-in.
   - Primary metric: Difference-in-Differences (DiD) in mean coin-in per player and visit frequency.
   - Secondary metrics: Voucher redemption rate, incremental POS cash spend, and net contribution after comp cost.

---

### Recommendation 2: Preventive Maintenance Sweep for Ridgeline Gaming (`A-PREVENTIVE`)

1. **Action Type**: `A-PREVENTIVE` (Preventive maintenance sweep for one manufacturer).
2. **Quantity**: 1 manufacturer sweep.
3. **Target Machines**: All 86 **Ridgeline Gaming** machines across the floor (including Banks B-11, B-12, B-13, B-21, B-22, B-36, B-37, B-38).
4. **Estimated Cost**:
   - Package cost: **$9,000**.
   - Lead time: 7 days. Sweep scheduled during graveyard quiet hours (90 minutes downtime per machine).
   - Recurring cost: $0.
   - Total Cost: **$9,000**.
5. **Supporting Evidence**:
   - Over the 6-month period, the floor recorded 1,207 fault repair tickets.
   - **Ridgeline machines generated 680 of these faults (56.34% of all faults)**, despite representing less than 30% of total machines on the floor.
   - Average repair time for Ridgeline tickets was 4.09 hours, leading to ~2,780 cumulative hours of machine downtime and over $63,000 in direct maintenance and technician labor costs.
   - Recurrent bill validator jams and hopper/printer errors in Ridgeline units are the #1 driver of machine unreliability.
6. **Expected Effect**:
   - A comprehensive preventive maintenance overhaul (cleaning bill validators, aligning reels, replacing worn printer heads and thermal sensors) reduces failure rates by 35%–45% over the subsequent 60–90 days.
   - During the 23 effective operating days in July, this prevents an estimated **28 to 36 fault incidents**.
   - Saves ~120 to 150 hours of lost machine availability and ~$3,400 to ~$4,300 in direct technician repair parts/labor.
   - Recovers **~$2,150 to ~$2,700 in theoretical house win** by keeping high-traffic Ridgeline games operational.
7. **Uncertainty and Risks**:
   - *Temporary Downtime*: 90 minutes of downtime per machine during the sweep. (Mitigated by performing maintenance strictly between 02:00 and 06:00 on weekdays when floor occupancy is under 8%).
   - *Underlying Design Flaw*: If component failures stem from flawed firmware or unfixable hardware defects, failure rates may rebound.
8. **Conditions to Abandon**:
   - If initial inspection of the first 10 Ridgeline units reveals that parts required are on backorder exceeding 14 days.
   - If manufacturer announces a mandatory warranty recall covering labor and parts at zero cost.
9. **30-Day Measurement Plan**:
   - Track daily fault logs (`operations.parquet`) for Ridgeline units in July compared to historical baseline (January–June daily average of 3.76 faults/day).
   - Target benchmark: Fault frequency drops to $< 2.2$ faults/day post-maintenance (a $\ge 40\%$ reduction).
   - Machine availability ratio benchmark: Increase Ridgeline average availability from 97.4% to $> 98.8\%$.

---

### Recommendation 3: Targeted Machine Inspection & Paytable Verification (`A-INSPECT`)

1. **Action Type**: `A-INSPECT` (Machine inspection and paytable verification).
2. **Quantity**: 5 machines.
3. **Target Machines**:
   - `M-1158` (Desert Gold, Bank B-38): House win $15,796.25 vs Theo $51,961.00 (Luck residual: **-$36,164.75**; Hold: 3.04% vs 10.0% expected).
   - `M-1288` (Jackpot Summit, Bank B-45): House win $49,090.00 vs Theo $108,223.08 (Luck residual: **-$59,133.08**; Hold: 5.44% vs 12.0% expected).
   - `M-1070` (Platinum Reels, Bank B-23): House win $42,365.00 vs Theo $73,130.50 (Luck residual: **-$30,765.50**; Hold: 5.79% vs 10.0% expected).
   - `M-1290` (Platinum Reels, Bank B-45): House win $47,875.00 vs Theo $78,612.00 (Luck residual: **-$30,737.00**; Hold: 6.09% vs 10.0% expected).
   - `M-1152` (Jackpot Summit, Bank B-36): House win $85,889.00 vs Theo $115,074.00 (Luck residual: **-$29,185.00**; Hold: 8.96% vs 12.0% expected).
4. **Estimated Cost**:
   - Unit cost: $1,200 per machine.
   - Lead time: 1 day (completed July 2).
   - Downtime: 120 minutes per machine (performed during morning low-traffic hours).
   - Total Cost: **$6,000** ($1,200 × 5).
5. **Supporting Evidence**:
   - Management's proposed replacement list targeted `M-1158` because of low nominal house win, unaware that it generated $519,610 in coin-in and ran -$36,164.75 behind expectation.
   - Combined, these 5 machines generated **$3.34 million in coin-in** and had an aggregate expected theoretical house win of **$427,000**, but actual house win was only **$241,015**—a combined luck deficit of **-$185,985**!
   - While high-volatility slots naturally exhibit large standard errors, prudent casino compliance requires formal verification of EPROM signatures, DIP switches, physical payout reels, and reel strips before dismissing or replacing high-exposure games.
6. **Expected Effect**:
   - Confirms that the paytables match jurisdictional regulatory filings and configured game math (RTP 88%–90%).
   - Prevents an erroneous $110,000 purchase or $16,900 lease replacement program on games that are actually popular player favorites.
   - If an unauthorized configuration error or meter miscalibration is discovered, correcting it instantly restores expected win margins on over $500,000 in monthly coin-in.
7. **Uncertainty and Risks**:
   - *Information-Only Outcome*: As noted in the catalog, this action yields verification data, not an automatic revenue lift.
   - *Negligible Downside*: Only 2 hours of downtime per machine during quiet hours (lost coin-in $< \$250$ per machine).
8. **Conditions to Abandon**:
   - If pre-inspection review of internal game software logs confirms identical certified hash signatures without opening the cabinet.
9. **30-Day Measurement Plan**:
   - Post-inspection certification report signed by regulatory slot compliance.
   - Continued monitoring of daily hold vs theoretical hold in July; tracking convergence toward expected RTP over the subsequent $250,000+$ spins.

---

### Capital Discipline & Budget Preservation (`A-HOLD`)

- **Retained Budget**: **$71,000** (or **$61,400** maintaining our $10,000 variable comp reserve).
- **Strategic Justification**:
  - The challenge instructions explicitly state: *"Keeping unspent money does not use an action slot... Keeping the budget is a valid answer."*
  - The data conclusively proves that the floor does NOT require wholesale capital replacement. Buying machines ($22,000 each) or signing long-term leases ($2,500 + $55/day) without addressing traffic starvation or maintenance reliability would destroy shareholder value.
  - Preserving $61k–$71k maintains liquidity for August/Q3, when the results of the comp pilot and Ridgeline maintenance sweep can be scaled with proven empirical ROI.

---

## Alternative Actions Analyzed & Trade-Off Matrix

| Action | Cost | Pros | Cons / Why Deprioritized |
|---|---|---|---|
| `A-TECH-SHIFT` (Swing Shift Tech) | $11,520 | Swing shift has 577 faults (47.8%) and only 1 tech. Would reduce queue times by ~1.4 hrs/fault. | Strong contender! However, `A-PREVENTIVE` ($9,000) attacks the **root cause** of 56% of faults (Ridgeline), preventing breakdowns before they occur. If budget permits or if Ridgeline PM is delayed, `A-TECH-SHIFT` is the immediate backup. |
| `A-REPLACE-BUY` (10 units) | $220,000 | New hardware. | Violates budget ceiling ($100,000 limit). Targets machines that are not actually underperforming. |
| `A-REPLACE-LEASE` (10 units) | $33,800 | Lower upfront cash ($2,500 + 16×$55 = $3,380/unit). | 14-day lead time leaves only 16 days of operation. Destroys popular games like `M-1158`. Does not fix Back Forty foot-traffic deficiency. |
| `A-WAYFINDING` (Back Forty) | $7,500 | Increases visibility for starved Back Forty zone. | 10-day lead time. Zone traffic counters indicate overall property foot traffic is stable; guest comp incentives (`A-COMP-PILOT`) drive direct foot traffic more effectively than signage. |
| `A-COMP-CHANGE` (Floor-Wide) | $1,500 | Low catalog cost. | Incompatible with `A-COMP-PILOT`. Changing redemption rates floor-wide without a control group risks unmeasured margin erosion or player backlash across all 113,890 members. |
| `A-PROMO` (Weekend Event) | $15,000 | Immediate weekend traffic spike. | High cost for transient 48-hour spike; does not address structural downtime or long-term loyalty retention. |
| `A-SURVEY` (Intercept Survey) | $3,500 | More subjective customer feedback. | Casino already possesses massive behavioral datasets (sessions, trips, POS receipts); operational capital is better spent on direct maintenance and loyalty testing. |

---

## 30-Day Master Milestone Schedule (July 2025)

- **July 1**: Place orders for `A-COMP-PILOT`, `A-PREVENTIVE` (Ridgeline), and `A-INSPECT`.
- **July 2**: Complete paytable inspection on the 5 machines (`A-INSPECT`). Return machines to service by 08:00.
- **July 6**: Launch 1,000-player Comp Policy Pilot (`A-COMP-PILOT`). Treatment vouchers active in POS system.
- **July 8**: Begin Ridgeline preventive maintenance sweep (`A-PREVENTIVE`) during weekday graveyard hours (02:00–06:00).
- **July 12**: Complete all 86 Ridgeline PM sweeps. Verify all machines operational.
- **July 16**: Mid-month checkpoint. Evaluate pilot voucher redemption rates and early fault frequency.
- **July 20**: Pilot checkpoint. Test for early statistical significance in treatment group visit frequency.
- **July 30**: Full 30-day close. Calculate DiD lift for Comp Pilot, availability gains from Ridgeline PM, and final July contribution margin. Present August scaling plan to Executive Committee.

