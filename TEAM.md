# Working on Dashboard Royale together

Two people, one submission. This file is the split: who owns which question, which files only one person edits, and the tables you hand each other so you can work at the same time.

The casino is fictional. Data release `0.9.0-draft` (January 1–June 30, 2025, gaming days 06:00–06:00 America/Los_Angeles). Read [GUIDE.md](GUIDE.md) once before you start. Column meanings live in [reference/DATA_DICTIONARY.md](reference/DATA_DICTIONARY.md). Money definitions live in [reference/DATASET.md](reference/DATASET.md). Do not edit anything under `data/` or `reference/`.

| | Floor | Guests |
| --- | --- | --- |
| Questions | 1, 2, 3, and the required model | 4, 5, 6 |
| Judging weight you carry | Analytical validity on the floor, modeling (20%) | Player and comp validity, recommendations (15%), write-up |
| Folder only you edit | `work/floor/` | `work/guests/` |
| Dashboard page only you edit | `dashboard/floor.html` | `dashboard/guests.html` and `dashboard/actions.html` |

Shared files have one editor. The other person reads them and comments in `work/shared/NOTES.md`.

| Shared file | Editor |
| --- | --- |
| `work/shared/CONTRACT.md` | Floor, until both of you sign the metric names below. After that, neither person changes a name without the other. |
| `work/shared/NOTES.md` | Whoever is writing the note. Append. Do not rewrite the other person's lines. |
| `dashboard/index.html` | Guests, and only after both pages exist. It links the two pages and the action page. It does not recompute metrics. |
| `submission/writeup.md` | Guests drafts. Floor adds the model paragraph. |
| `submission/claims.md` | Each person writes only their own claims. |
| `submission/ai.md` | Each person writes only their own disclosure. |

## How you stay out of each other's way

1. Copy this repository once. Each person works in their own clone, or on their own machine. This folder sits in OneDrive. Two people editing the same file there will produce conflicted copies. Git is the handoff. OneDrive is only the backup of the repo.
2. Floor works on branch `floor`. Guests works on branch `guests`. Merge into `main` only at the checkpoints below.
3. Pass results as the parquet files in **Handoff tables**, not as notebooks. A notebook is private. A parquet file is the interface.
4. Neither person loads the other's large tables. Floor does not open `sessions`, `loyalty_ledger`, or `fnb_transactions`. Guests does not open `machine_hour`.
5. `example-dashboard.html` is a layout sample with placeholder numbers. Leave it unchanged. Build the real dashboard under `dashboard/`.

```
work/
  shared/CONTRACT.md          metric names both of you use
  shared/NOTES.md             questions and decisions, append-only
  floor/                      notebooks, scripts, charts
  floor/out/                  parquet files Guests is allowed to read
  guests/                     notebooks, scripts, charts
  guests/out/                 parquet files Floor is allowed to read
dashboard/
  floor.html                  Floor
  guests.html                 Guests
  actions.html                Guests
  index.html                  Guests, last
submission/
  writeup.md                  400 words, main text
  claims.md                   Claims & Evidence appendix
  ai.md                       what each person used AI for
```

Create the folders when you start. Do not commit `.venv/`, extracted `.csv` files, or caches.

## Shared rules

Both analyses use these definitions. They are already checked by `scripts/verify_semantics.py`.

| Name | Formula | Where it applies |
| --- | --- | --- |
| Coin-in | Sum of wagers, including winnings bet again | Machine and player tables |
| House win | Coin-in − payout. Can be negative. | `prepared_daily_view`, `property_day`, `machine_day` |
| Player net | Payout − coin-in. Opposite sign of house win. | `player_period` (`tracked_net_usd`) |
| Theo | Sum of bet × (1 − configured RTP) | Exposure benchmark, not a guaranteed loss |
| Luck residual, machines | House win − theo | `prepared_daily_view.luck_residual_usd` |
| Luck residual, players | Tracked net + theo | `player_period.luck_residual_usd` |
| Hold | Sum of house win / sum of coin-in | Never the average of daily holds |
| Availability | Available hours / scheduled hours | Use `calendar_day.scheduled_seconds`. March 8, 2025 has 23 hours (82,800 seconds). |
| Contribution, machine | House win − lease − service − power − repair | Do not add rent, tax, or depreciation |
| Contribution, property | House win + POS cash − POS COGS − machine supplied costs − tech labor | `comp_cost_usd` is already inside POS COGS. Subtract it once. |
| Tracked contribution | −tracked net + linked POS cash − linked POS COGS | Carded guests only |

Rows to drop before any machine ranking: `prepared_daily_view` rows with an empty `location_id` (1,018 days before install or after retirement). They are not zero-earning machines.

Carded play and all play never match. Compare them with `carded_*` on `machine_day` or `prepared_daily_view`. Guest tables are loyalty-card only.

Join fact tables only after each one is aggregated. Joining `sessions` to `fnb_transactions` row by row double-counts money.

A missing traffic count is offline, not zero. Check `counter_status`. Counts are crossings, not unique visitors.

Model split, for both people: train on January–April 2025, test on May–June 2025. Split by time. The `lag_*` columns on `prepared_daily_view` are safe because they use prior days only. Tourism and visitor-profile files were published after 2025. They can explain the past. They cannot be inputs to a forecast that claims to have been made during 2025. Weather dates are calendar dates, not gaming dates.

Budget, July 1–30, 2025, at most three action types from `action_catalog`. Keeping unspent money is allowed and does not use a slot. Cost in dollars:

`quantity × (unit_cost_cents + recurring_cost_cents_per_day × max(0, 30 − lead_days)) / 100`

A lease ordered July 1 with 14 lead days has 16 operating days: $2,500 + 16 × $55 = $3,380. Fixed packages (the technician) are charged in full. Do not put a move and a replacement on the same machine. Do not combine the comp pilot with the floor-wide comp change.

## Floor

You answer whether the ten lowest-earning machines are actually the problem, what happened to demand, and how much play downtime removed. You also build the one model the submission requires.

### Questions

1. Which machines are weak after exposure, availability, and luck?
2. What changed in demand from January to June, and which of location, events, weather, and city visitation still holds after you check the others?
3. How much house win was lost while machines were down, and on which shifts or manufacturers that clusters?

The manager's list is the ten active machines with the lowest total house win. Start from the DuckDB query in [GUIDE.md](GUIDE.md). Then replace that ranking with one that:

- drops inactive rows
- compares house win with theo, and reports the luck residual
- divides by available hours, not by calendar days
- uses the location on that date (`prepared_daily_view` already has it; `placements` is the source if you need the interval)
- separates a quiet bank from a weak game (`zone_id`, `bank_id`, `volatility_class`, `configured_rtp`)

### Tables you own

| Use first | Go here when the first table is not enough |
| --- | --- |
| `data/1_prepared_views/prepared_daily_view` | `machine_day`, `game_math`, `placements`, `machines` |
| `data/1_prepared_views/property_day` | `zone_traffic_hourly`, `events`, `calendar_day` |
| `data/2_machine_decision/operations` | `cost_rules`, `floor_locations`, `floor_walkways` |
| `data/4_context/real_sources/weather_daily` | `city_visitation_monthly` for a demand check only |
| `data/5_optional/machine_hour` | Only if daily availability is too coarse. It is 1.3 million rows. Aggregate in DuckDB. |
| `data/5_optional/shift_roster` | Slot-tech headcount against downtime |

Leave Missouri benchmark tables alone unless Guests asks for an outside hold comparison. Those files are context, not this casino.

### Model

Forecast daily floor coin-in. The simple version is enough if you validate it honestly.

- Training target: `property_day.coin_in_usd`, January 1–April 30.
- Baseline: one number, the mean daily coin-in in training.
- Alternative: mean coin-in by `local_weekday` in training. A fuller time-series model is optional. It still has to beat, tie, or lose to this baseline in the open.
- Test: May 1–June 30. Freeze both forecasts before you look at test error.
- Score: mean absolute error in dollars, plus a plot of prediction against actual.
- Decision the model has to change: a staffing or promotion choice in July, written so Guests can price it. If the weekday model does not beat the mean, say so and recommend the simpler plan.

Use only columns that would have been known on the prediction date. Do not compute a feature from May or June and then predict May or June.

### What you hand Guests

Write these three files under `work/floor/out/`. Overwrite them on each refresh. Keep the column names stable.

**`machine_scorecard.parquet`** — one row per machine that was active at least one day.

| Column | Meaning |
| --- | --- |
| `machine_id` | |
| `days_on_floor` | Active days |
| `available_hours` | Sum |
| `coin_in_usd` | Sum |
| `house_win_usd` | Sum |
| `theo_usd` | Sum |
| `luck_residual_usd` | Sum of house win − theo |
| `house_win_per_available_hour` | Sum house win / sum available hours |
| `availability_ratio` | Sum available hours / sum scheduled hours |
| `downtime_hours` | Scheduled hours on floor minus available hours |
| `zone_id`, `bank_id` | Location on the machine's last active day |
| `manufacturer`, `theme`, `volatility_class`, `configured_rtp`, `lease_class` | From the last active day |
| `manager_bottom_10` | True if this machine is in the raw lowest-house-win ten |
| `rank_fair` | Rank by house win per available hour after you state the luck adjustment in `work/shared/NOTES.md` |

**`demand_daily.parquet`** — one row per gaming date.

| Column | Meaning |
| --- | --- |
| `gaming_date` | |
| `coin_in_usd`, `house_win_usd`, `theo_usd` | From `property_day` |
| `available_machine_hours`, `occupied_machine_hours` | |
| `events_active` | |
| `pred_coin_in_baseline_usd` | Filled on May–June only; null in training |
| `pred_coin_in_model_usd` | Same |
| `split` | `train` or `test` |

**`model_card.md`** — half a page: features used, MAE of baseline, MAE of model, and the July decision in one sentence. Guests copies that sentence into the action page. They do not refit the model.

### Dashboard page

`dashboard/floor.html` needs the controls judges use:

- change the period (full half-year, last three months, June)
- drill from the floor to one zone and then one bank
- open the model card: training window, test window, both MAEs, predicted against actual

The page reads `work/floor/out/` or a small JSON you export from those parquets. It does not read guest tables.

## Guests

You answer what tracked players wagered and won, what the comp program cost, and which actions to buy with $100,000. You assemble the submission text.

### Questions

4. Tracked coin-in, payout, and player net, and how concentrated those results are.
5. What comps cost, and whether the rate or the mix changed over the six months.
6. Up to three priced actions for July 1–30, or a recommendation to keep the money, each with effect, uncertainty, and a measurement plan.

Player totals will be smaller than machine totals. That is the carded subset, not a broken join. Concentration and comp ratios describe tracked guests only.

`trips` are visits to this casino, not Las Vegas trips. Some visits have food or loyalty activity and no carded gaming. LVCVA visitor-profile numbers describe all Las Vegas visitors. Cite them as outside context. Do not treat them as this floor's guests.

### Tables you own

| Use first | Go here when the first table is not enough |
| --- | --- |
| `data/1_prepared_views/player_period` | `players` for region, age band, opening tier |
| `data/1_prepared_views/property_day` | Comp and POS totals by day. Read it. Floor owns the demand story on the same file. Do not write a second demand analysis. |
| `data/3_guests/loyalty_ledger` | Points, tier changes, economic cost. 782,773 rows. Aggregate before any join. |
| `data/3_guests/fnb_transactions` | Cash versus comp. Uncarded tickets have a null `player_id`. |
| `data/3_guests/trips` | Visit counts. Prefer `player_period.observed_visits` unless you need timing. |
| `data/2_machine_decision/action_catalog` | Prices, lead times, limits, incompatibility groups |
| `data/2_machine_decision/cost_rules` | So a recommended action is not priced twice |

`sessions` is 776,297 rows. Open it only to test one claim that `player_period` cannot answer, and aggregate it in DuckDB first.

`security_incidents` and `visitor_profile_monthly` are optional. An incident is a lead to inspect, not a finding of cheating. Do not recommend anything designed to push heavy losers to play more. A protective limit is in bounds. A targeted offer to players who lost the most is not.

### What you hand Floor

**`work/guests/out/player_month.parquet`** — one row per `period_month`.

| Column | Meaning |
| --- | --- |
| `period_month` | `YYYY-MM` |
| `players` | Distinct `player_id` |
| `tracked_coin_in_usd`, `tracked_payout_usd`, `tracked_net_usd`, `theo_usd` | Sums |
| `comp_cost_usd`, `comp_face_value_usd`, `linked_pos_cash_usd` | Sums. Comp cost stays inside the COGS story. |
| `tracked_contribution_usd` | Sum |
| `share_of_coin_in_top_1pct_players` | Concentration |
| `share_of_net_top_1pct_players` | Concentration of player net. State the sign. |

**`work/guests/out/action_shortlist.md`** — at most three action types, plus an explicit keep-the-rest line. For each: `action_type_id`, quantity, targets (machine, bank, or guest segment), dollar cost using the formula above, what evidence you used, what would make you drop it, and how you would measure it in the next 30 days.

Use Floor's `machine_scorecard.parquet` for any machine target. If that file is not ready, write the guest and comp actions first and leave machine targets as `WAITING ON floor/out/machine_scorecard.parquet`. Do not invent a second machine ranking.

### Dashboard pages

`dashboard/guests.html` needs a guest-group drill (tier, age band, or home region — pick one and keep it) and the same period control as the floor page.

`dashboard/actions.html` lists the priced actions. Every number on it links to a row in `submission/claims.md`. The model sentence comes from `work/floor/out/model_card.md`.

`dashboard/index.html` is a front door: the decision in two sentences, then links to floor, guests, and actions. Build it last.

## Checkpoints

Work between checkpoints is independent. At a checkpoint, merge the branch that owns the files in that row.

| When | Floor | Guests | Merge |
| --- | --- | --- | --- |
| Start | Create `work/floor/` and confirm `prepared_daily_view` has 56,110 rows and 1,018 null locations | Create `work/guests/` and confirm `player_period` has 148,893 rows | Nothing |
| First handoff | Publish `machine_scorecard.parquet` with the manager's ten flagged, even if `rank_fair` is still a first pass | Publish `player_month.parquet` and a draft action list that may still say `WAITING ON` | Both parquets onto `main` |
| Model lock | Publish `demand_daily.parquet` and `model_card.md`. Stop changing the model after this. | Price actions against the locked scorecard and the model sentence | `work/floor/out/` |
| Dashboard | `dashboard/floor.html` works with period and bank filters | `dashboard/guests.html` and `dashboard/actions.html` | `dashboard/` |
| Submission | Add the model paragraph and your claims | Finish the 400-word write-up, the appendix, and `index.html` | `submission/` |

Run this from `dashboard-royale` before the first handoff, so you know the files match:

```sh
python -m pip install duckdb
python scripts/verify_data.py
python scripts/verify_semantics.py
```

`check_release.py` is for the challenge organizers. You can ignore its calibration warning.

## Submission, split by person

Devpost: https://tamu-datathon-26-casino-royale.devpost.com/

| Piece | Owner | Constraint |
| --- | --- | --- |
| Public dashboard | Both pages, Guests owns the link | Judges can open it without your laptop. Test the link in a private window. |
| Video, 2 minutes | Decide together in `NOTES.md` who records | Floor explains the model. Guests states the priced actions. |
| Write-up | Guests, with Floor's model paragraph | 400 words. Appendix and AI note are separate. |
| Model versus baseline | Floor | Time holdout, MAE in dollars, no leakage |
| Code | Each person commits their own folder | Include the steps that build the parquet outputs |
| Actions | Guests | At most three types, cost, effect, uncertainty, measurement |
| AI disclosure | Each person, in `submission/ai.md` | Tool and what it was used for |
| Claims & Evidence | Each person, own section of `submission/claims.md` | Claim, table or query, result, alternative explanation, limitation |

Judges will change the period, drill into one bank or one guest group, find the model validation, and trace one recommendation to its evidence. Those four paths have to work on the day you submit.

## Claims template

Copy this block once per claim in `submission/claims.md`.

```
### Claim
One sentence a manager can check.

Owner: Floor or Guests
Table:
Query or notebook:
Result:
Alternative explanation tested:
Limitation:
```

Floor's claims stay inside questions 1–3 and the model. Guests' claims stay inside questions 4–6. A claim that needs both folders cites the other person's parquet file and does not recompute it.
