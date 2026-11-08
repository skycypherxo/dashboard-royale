# Working on Dashboard Royale Together — Akshaya & Vaishnavi

## Team Ownership: Who Does What

Two people, one submission. This document defines individual responsibilities, file ownership, deliverables, and how we coordinate without interfering with each other's work.

| Person | Role | Primary Ownership |
|---|---|---|
| **Akshaya** | Floor & ML Lead | Questions 1, 2, 3 and required ML model. Machine performance, demand analysis, downtime, forecasting, machine scorecard, and floor dashboard. |
| **Vaishnavi** | Guest & Business Intelligence Lead | Questions 4, 5, 6. Player analytics, loyalty and comps, financial recommendations, budget allocation, write-up, and guest/actions dashboards. |

The original repository folder names (`work/floor/` and `work/guests/`) remain unchanged for compatibility.

---

## 1. Akshaya — Floor & ML Lead

**Branch:** `floor`

**Primary folder:** `work/floor/`

**Dashboard page:** `dashboard/floor.html`

### Responsibilities

You own the analytical investigation of the casino floor.

#### Question 1: Machine Performance

Determine whether the ten lowest-earning machines are actually underperforming.

- Analyze all 300 machines.
- Investigate house win, coin-in, theoretical win, and luck residual.
- Account for machine availability and downtime.
- Compare performance per available hour.
- Investigate differences between zones, banks, manufacturers, volatility classes, and configured RTP.
- Determine whether machines should be replaced, repaired, or retained.

#### Question 2: Demand Analysis

Investigate what changed in casino demand between January and June.

- Analyze daily coin-in trends.
- Investigate location and zone-level demand.
- Evaluate the effects of events, weather, and city visitation.
- Determine which factors remain relevant after accounting for others.
- Identify meaningful changes and patterns.

#### Question 3: Downtime Analysis

Investigate how much potential house win was lost because machines were unavailable.

- Analyze machine availability.
- Identify downtime patterns.
- Investigate differences across shifts and manufacturers.
- Determine which operational problems deserve attention.

#### Required ML Model

Build and validate a daily floor coin-in forecasting model.

- Training: January–April 2025.
- Testing: May–June 2025.
- Baseline: Mean daily coin-in during training.
- Alternative: Mean coin-in grouped by local weekday.
- Metric: Mean Absolute Error (MAE).
- Compare both models honestly.
- Avoid data leakage.
- Explain whether the model changes a July staffing or promotion decision.

### Data You Own

Start with:

- `data/1_prepared_views/prepared_daily_view`
- `data/1_prepared_views/property_day`

Additional sources:

- `machine_day`
- `game_math`
- `placements`
- `machines`
- `zone_traffic_hourly`
- `events`
- `calendar_day`
- `cost_rules`
- `floor_locations`
- `floor_walkways`
- `weather_daily`
- `city_visitation_monthly`
- `machine_hour` (only if daily availability is insufficient)
- `shift_roster`

Do not independently analyze the guest datasets.

### Deliverables

Save the following files under `work/floor/out/`:

1. `machine_scorecard.parquet`
2. `demand_daily.parquet`
3. `model_card.md`

Build:

`dashboard/floor.html`

The dashboard must support:

- Full six-month period.
- Last three months.
- June-only view.
- Floor-to-zone-to-bank drill-down.
- Machine performance comparisons.
- Availability and downtime.
- Model training/test information.
- Predicted versus actual coin-in.
- Both model MAEs.

### What You Hand Vaishnavi

- `machine_scorecard.parquet`
- `demand_daily.parquet`
- `model_card.md`

Vaishnavi will use your machine scorecard to select and price machine-related operational actions.

---

## 2. Vaishnavi — Guest & Business Intelligence Lead

**Branch:** `guests`

**Primary folder:** `work/guests/`

**Dashboard pages:**
- `dashboard/guests.html`
- `dashboard/actions.html`
- `dashboard/index.html` (final integration)

### Responsibilities

You own the tracked-player investigation, loyalty and comp analysis, financial recommendations, and submission write-up.

#### Question 4: Player Analytics

Investigate what tracked players wagered, received back, and actually won or lost.

Calculate:

- Total tracked coin-in.
- Total tracked payouts.
- Player net results.
- Theoretical win.
- Luck residual.
- Player-level concentration.
- Monthly changes in tracked-player activity.

Remember:

`Player Net = Payouts - Coin-in`

Positive values indicate player winnings. Negative values indicate player losses.

Do not confuse player net with casino house win.

#### Question 5: Loyalty and Comps

Investigate the casino's loyalty and complimentary rewards program.

- Analyze loyalty points and tier changes.
- Calculate comp costs.
- Compare comp face value against actual economic cost.
- Investigate monthly changes in comp rate and mix.
- Analyze linked POS cash and COGS.
- Identify meaningful patterns in tracked-player activity.

Remember that comp cost is already included in POS COGS. Do not subtract it twice.

#### Question 6: Operational Recommendations

Recommend up to three action types for July 1–30.

**Total available budget: $100,000.**

Investigate options such as:

- Machine repairs.
- Machine replacements.
- Inspections.
- Operational improvements.
- Comp-related actions.
- Preserving unspent budget.

For each recommendation, provide:

1. Action type.
2. Quantity.
3. Target machines, banks, or guest segments.
4. Estimated cost.
5. Supporting evidence.
6. Expected effect.
7. Uncertainty and risks.
8. Conditions that would make us abandon the action.
9. How success will be measured over 30 days.

Use Akshaya's `machine_scorecard.parquet` for machine-related decisions.

Do not create a separate machine ranking.

### Data You Own

Start with:

- `data/1_prepared_views/player_period`
- `data/1_prepared_views/property_day`

Additional sources:

- `players`
- `loyalty_ledger`
- `fnb_transactions`
- `trips`
- `action_catalog`
- `cost_rules`

Optional:
- `sessions`
- `security_incidents`
- `visitor_profile_monthly`

Aggregate large datasets before joining them.

Do not independently analyze the machine-hour dataset.

### Deliverables

Save:

`work/guests/out/player_month.parquet`

`work/guests/out/action_shortlist.md`

Build:

- `dashboard/guests.html`
- `dashboard/actions.html`
- `dashboard/index.html` (after both dashboard pages are ready)

The guest dashboard must support a period filter consistent with Akshaya's floor dashboard and a drill-down by one selected guest grouping, such as tier, age band, or home region.

The actions dashboard must show the priced recommendations and link every important figure to supporting evidence in `submission/claims.md`.

### Submission Ownership

You own:

- Drafting the 400-word submission write-up.
- Assembling the final claims and evidence appendix.
- Preparing the final AI disclosure file.
- Integrating the dashboard pages through `dashboard/index.html`.
- Ensuring the final public dashboard is accessible.

Akshaya will provide the ML paragraph and her analytical claims.

---

## 3. Shared Responsibilities

Both people must:

- Read `GUIDE.md`.
- Understand `reference/DATA_DICTIONARY.md`.
- Understand the financial definitions in `reference/DATASET.md`.
- Agree on shared metric definitions.
- Review each other's findings.
- Keep analytical claims evidence-backed.
- Test the final dashboard.
- Participate in final presentation preparation.

### Shared Files

| File | Ownership |
|---|---|
| `work/shared/CONTRACT.md` | Akshaya initially; both approve metric definitions |
| `work/shared/NOTES.md` | Both; append-only |
| `submission/writeup.md` | Vaishnavi drafts; Akshaya contributes ML paragraph |
| `submission/claims.md` | Each person writes their own claims |
| `submission/ai.md` | Each person documents their AI usage |
| `dashboard/index.html` | Vaishnavi, after both dashboard pages exist |

---

## 4. How We Work Independently

Use separate Git branches.

| Person | Branch |
|---|---|
| Akshaya | `floor` |
| Vaishnavi | `guests` |

Rules:

1. Each person works on their own branch.
2. Do not modify the other person's workstream files.
3. Use parquet files for analytical handoffs, not notebooks.
4. Keep shared metric definitions consistent.
5. Append decisions and questions to `work/shared/NOTES.md`.
6. Merge into `main` at agreed checkpoints.
7. Do not modify anything under `data/` or `reference/`.
8. Do not commit `.venv/`, extracted CSV files, or caches.

### Important Dataset Rules

- Drop `prepared_daily_view` rows with empty `location_id` before machine ranking.
- Carded play and all play are different populations.
- Guest tables represent loyalty-card activity only.
- Aggregate fact tables before joining them.
- Missing traffic counts indicate offline counters, not zero visitors.
- March 8, 2025 has 23 scheduled hours.
- Forecasting must use January–April for training and May–June for testing.
- Do not use future information as a forecasting feature.
- Tourism and visitor-profile files published after 2025 cannot be used as historical forecast inputs.

---

## 5. Development Checkpoints

| Checkpoint | Akshaya | Vaishnavi |
|---|---|---|
| Start | Create `work/floor/`; validate machine data | Create `work/guests/`; validate player data |
| First handoff | Publish machine scorecard | Publish player monthly summary and draft actions |
| Model lock | Publish demand forecasts and model card | Price recommendations using locked machine scorecard |
| Dashboard | Complete `floor.html` | Complete `guests.html` and `actions.html` |
| Final integration | Review floor findings and model | Complete index, write-up, and final integration |

Before the first handoff, run:

```bash
python -m pip install duckdb
python scripts/verify_data.py
python scripts/verify_semantics.py