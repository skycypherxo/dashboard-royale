Cursor Prompt — Dashboard Royale: Architecture & Implementation Plan
You are acting as a senior full-stack architect, data engineer, ML engineer, AI engineer, and hackathon product strategist.

I am participating in the TAMU Datathon 2026 — Dashboard Royale: Luck, Location, or a Leak?

I want to build an exceptional, hackathon-winning solution. This should be much more than a conventional dashboard. I want an intelligent, interactive, AI-powered casino operations intelligence platform with compelling analytics, useful ML, and a polished user experience.
PHASE 1: UNDERSTAND THE EXISTING PROJECT
Before recommending anything, thoroughly inspect the entire repository currently open in Cursor.

Start with:
- CLAUDE.md
- GUIDE.md
- reference/DATASET.md
- reference/DATA_DICTIONARY.md
- reference/SOURCES.md
- reference/READINESS.md
- The complete data/ directory structure.
- Existing Python scripts, notebooks, configuration files, and other project files.
Understand:
- Every dataset and its schema.
- Available columns, relationships, and granularity.
- Row counts and data volumes.
- Timestamp coverage.
- Financial definitions.
- Data quality issues and limitations.
- Existing starter code and infrastructure.
Do not make assumptions about the dataset. Base architectural decisions on the actual files.
PHASE 1B: TEAM OWNERSHIP AND PARALLEL WORK PLAN — AKSHAYA & VAISHNAVI
There are exactly two people working on this submission. Assign every task, file, dashboard page, analysis, and handoff explicitly to one of them.

Person 1: Akshaya — Floor & ML Lead
- Role name used in the repository plan: Floor.
- Git branch: floor.
- Primary work folder: work/floor/.
- Own dashboard page: dashboard/floor.html.
- Owns challenge questions 1, 2, and 3, plus the required forecasting model.
- Owns machine performance, demand analysis, downtime, machine scorecard, demand forecast, and model validation.
Person 2: Vaishnavi — Guests & Business Intelligence Lead
- Role name used in the repository plan: Guests (the guest/player workstream).
- Git branch: guests.
- Primary work folder: work/guests/.
- Own dashboard pages: dashboard/guests.html and dashboard/actions.html.
- Owns challenge questions 4, 5, and 6.
- Owns tracked-player analytics, loyalty and comps, priced operational recommendations, budget allocation, the main write-up, and final dashboard integration through dashboard/index.html.
Whenever this plan says Floor, it means Akshaya. Whenever it says Guests, it means Vaishnavi. Keep the literal folder names, branch names, and handoff filenames unchanged because repository instructions and scripts may depend on them.
Akshaya's exact workstream — Floor
Akshaya answers:
1. Which machines are weak after accounting for exposure, availability, and luck?
2. What changed in demand from January to June, and which of location, events, weather, and city visitation still holds after checking the others?
3. How much house win was lost while machines were down, and on which shifts or manufacturers does downtime cluster?
Akshaya's machine-performance method
The manager's list is the ten active machines with the lowest total house win. Start from the DuckDB query in GUIDE.md, then build a more defensible comparison that:
- Drops inactive rows.
- Compares house win with theo and reports luck residual.
- Divides by available hours, not calendar days.
- Uses the location on the relevant date (prepared_daily_view already has it; placements is the source if interval detail is needed).
- Separates a quiet bank from a weak game using zone_id, bank_id, volatility_class, and configured_rtp.
Do not simply rank by raw house win and call the bottom ten replacement candidates.
Akshaya's source tables
Use first:
- data/1_prepared_views/prepared_daily_view
- data/1_prepared_views/property_day
Go to these only when needed:
- machine_day
- game_math
- placements
- machines
- zone_traffic_hourly
- events
- calendar_day
- data/2_machine_decision/operations/cost_rules
- floor_locations
- floor_walkways
- data/4_context/real_sources/weather_daily
- city_visitation_monthly for a demand check only
- data/5_optional/machine_hour only if daily availability is too coarse; it has approximately 1.3 million rows and must be aggregated in DuckDB
- data/5_optional/shift_roster for slot-technician headcount against downtime
Leave Missouri benchmark tables alone unless Vaishnavi requests an outside hold comparison. Those files are context, not this casino.

Akshaya must not independently load or analyze sessions, loyalty_ledger, or fnb_transactions. Vaishnavi owns the guest workstream.
Akshaya's required forecasting model
Forecast daily floor coin-in.
- Target: property_day.coin_in_usd.
- Training window: January 1–April 30, 2025.
- Test window: May 1–June 30, 2025.
- Baseline: one constant equal to mean daily coin-in in the training period.
- Required alternative: mean coin-in by local_weekday, calculated only from the training period.
- A more advanced time-series model is optional, not a substitute for reporting the required baseline and weekday model.
- Metric: MAE in dollars.
- Plot predicted versus actual for the test window.
- Freeze forecasts before inspecting test errors.
- Use only features that would have been known on each prediction date.
- The lag_* columns in prepared_daily_view are safe only because they use prior days; verify exact construction before use.
- Do not use May/June-derived features to predict May/June.
- Tourism and visitor-profile files published after 2025 may explain the past, but cannot be forecast inputs that pretend to have been available during 2025.
- Weather dates are calendar dates, not gaming dates.
- The model must inform a July staffing or promotion decision that Vaishnavi can price. If the weekday model does not beat the mean baseline, say so and recommend the simpler plan.
Akshaya's exact handoff files
Write these under work/floor/out/. Overwrite them on each refresh and keep column names stable.

machine_scorecard.parquet — one row per machine active at least one day

Required columns:
- machine_id
- days_on_floor
- available_hours
- coin_in_usd
- house_win_usd
- theo_usd
- luck_residual_usd — sum of house win minus theo
- house_win_per_available_hour — sum house win divided by sum available hours
- availability_ratio — sum available hours divided by sum scheduled hours
- downtime_hours — scheduled hours on floor minus available hours
- zone_id, bank_id — location on the machine's last active day
- manufacturer, theme, volatility_class, configured_rtp, lease_class — values from the last active day
- manager_bottom_10 — true if in the raw lowest-house-win ten
- rank_fair — rank by house win per available hour, with the luck-adjustment method documented in work/shared/NOTES.md
demand_daily.parquet — one row per gaming date

Required columns:
- gaming_date
- coin_in_usd, house_win_usd, theo_usd — from property_day
- available_machine_hours, occupied_machine_hours
- events_active
- pred_coin_in_baseline_usd — populated on May–June only; null during training
- pred_coin_in_model_usd — populated on May–June only; null during training
- split — train or test
model_card.md
- Approximately half a page.
- State features used.
- State baseline MAE and weekday-model MAE.
- State the July decision in one sentence.
- Vaishnavi copies that decision sentence into the action page; Vaishnavi does not refit the model.
Akshaya's dashboard requirements
dashboard/floor.html must allow judges to:
- Select the full half-year, last three months, or June.
- Drill from floor to a zone and then a bank.
- Compare machine performance and the manager's raw bottom ten against the exposure/availability/luck-aware ranking.
- Inspect availability and downtime.
- Open the model card, including training window, test window, both MAEs, and predicted-versus-actual plot.
The floor page reads only work/floor/out/ or a small JSON export made from those outputs. It must not read guest tables or recompute guest metrics.
Vaishnavi's exact workstream — Guests
Vaishnavi answers:
4. What are tracked-player coin-in, payout, and player net, and how concentrated are those results?
5. What did comps cost, and did the rate or mix change over the six months?
6. Which up-to-three priced actions should be taken for July 1–30 within the $100,000 budget, or should some/all of the money be retained?
Player totals will be smaller than machine totals because guest tables describe loyalty-card activity only. This is not necessarily a broken join. Concentration and comp ratios describe tracked guests only.

trips means visits to this casino, not trips to Las Vegas. Some visits have food or loyalty activity and no carded gaming. LVCVA visitor-profile numbers describe all Las Vegas visitors; cite them only as outside context, not as this casino's guests.
Vaishnavi's source tables
Use first:
- data/1_prepared_views/player_period
- data/1_prepared_views/property_day (read for comp/POS totals by day; Akshaya owns the demand story on this same table, so do not write a second demand analysis)
Additional sources:
- players for region, age band, and opening tier
- data/3_guests/loyalty_ledger (782,773 rows; aggregate before joining)
- data/3_guests/fnb_transactions (cash versus comp; uncarded tickets have null player_id)
- trips (prefer player_period.observed_visits unless timing is needed)
- data/2_machine_decision/action_catalog (prices, lead times, limits, incompatibility groups)
- data/2_machine_decision/operations/cost_rules (avoid pricing the same cost twice)
 sessions has approximately 776,297 rows. Open it only to test one specific claim that player_period cannot answer, and aggregate in DuckDB first.

security_incidents and visitor_profile_monthly are optional. An incident is a lead to inspect, not proof of cheating. Do not recommend anything designed to push heavy losers to play more. A protective limit is acceptable. A targeted offer to players who lost the most is not.

Vaishnavi must not independently load or analyze machine_hour. Akshaya owns machine-hour analysis.
Vaishnavi's player and comp calculations
Report:
- Tracked coin-in.
- Tracked payouts.
- Tracked player net (payout - coin-in).
- Theo.
- Luck residual.
- Comp cost and comp face value.
- Linked POS cash.
- Tracked contribution.
- Player concentration, including top-1% shares.
- Monthly changes.
Keep these populations and definitions separate. Do not confuse player net with casino house win or total property contribution.

Comp cost is already inside POS COGS. Subtract it once only.
Vaishnavi's exact handoff files
Write these under work/guests/out/.

player_month.parquet — one row per period_month

Required columns:
- period_month — YYYY-MM
- players — distinct player_id
- tracked_coin_in_usd
- tracked_payout_usd
- tracked_net_usd
- theo_usd
- comp_cost_usd
- comp_face_value_usd
- linked_pos_cash_usd
- tracked_contribution_usd
- share_of_coin_in_top_1pct_players
- share_of_net_top_1pct_players — state the sign convention
The monetary columns are sums at the specified monthly grain. Keep the schema stable.

action_shortlist.md
- At most three action types.
- Include an explicit line describing what budget remains unspent / is retained.
- For each action include action_type_id, quantity, targets (machine, bank, or guest segment), dollar cost, evidence, what would make the team drop the action, and how to measure it over the next 30 days.
- Use Akshaya's work/floor/out/machine_scorecard.parquet for machine targets.
- If the scorecard is not ready, write guest and comp actions first and mark machine targets exactly as waiting on work/floor/out/machine_scorecard.parquet.
- Do not invent a second machine ranking.
Exact action-cost formula and constraints
Budget period: July 1–30, 2025. Maximum: $100,000. Use at most three action types from action_catalog.

Calculate cost in dollars:

quantity × (unit_cost_cents + recurring_cost_cents_per_day × max(0, 30 − lead_days)) / 100
- A lease ordered July 1 with 14 lead days has 16 operating days: $2,500 + 16 × $55 = $3,380.
- Fixed packages (such as the technician) are charged in full.
- Do not put a move and a replacement on the same machine.
- Do not combine the comp pilot with the floor-wide comp change.
- Keeping unspent money is allowed and does not consume an action slot.
- Use action_catalog and cost_rules; do not invent prices.
Vaishnavi's dashboard requirements
dashboard/guests.html:
- Uses the same period control as the floor dashboard.
- Provides one guest-group drill-down; choose tier, age band, or home region based on data quality and keep that choice consistent.
- Shows tracked-player coin-in, payouts, player net, theo, concentration, and comp context with correct labels.
dashboard/actions.html:
- Lists the priced actions.
- Shows budget allocation and retained budget.
- Every important displayed number links to a corresponding row/claim in submission/claims.md.
- Uses the model decision sentence from Akshaya's work/floor/out/model_card.md.
- Does not refit or silently alter Akshaya's model.
dashboard/index.html:
- Build last, after both analytical pages and the action page exist.
- Acts as the front door.
- States the decision in two sentences, then links to floor, guests, and actions.
- Does not recompute metrics.
Shared metric contract — both people must follow exactly
These definitions are already checked by scripts/verify_semantics.py. Preserve the exact names and sign conventions.
Metric	Definition	Applies to
Coin-in	Sum of wagers, including winnings bet again	Machine and player tables
House win	Coin-in minus payout; can be negative	prepared_daily_view, property_day, machine_day
Player net	Payout minus coin-in; opposite sign of house win	player_period.tracked_net_usd
Theo	Sum of bet × (1 − configured RTP)	Exposure benchmark, not guaranteed loss
Machine luck residual	House win minus theo	prepared_daily_view.luck_residual_usd
Player luck residual	Tracked net plus theo	player_period.luck_residual_usd
Hold	Sum of house win divided by sum of coin-in; never average daily holds	Aggregated period
Availability	Available hours divided by scheduled hours	Use calendar_day.scheduled_seconds; March 8, 2025 has 23 hours (82,800 seconds)
Machine contribution	House win − lease − service − power − repair	Machine-level
Property contribution	House win + POS cash − POS COGS − machine-supplied costs − tech labor	comp_cost_usd is already inside POS COGS; subtract once
Tracked contribution	−tracked net + linked POS cash − linked POS COGS	Carded guests only


Additional rules:
- Drop prepared_daily_view rows with empty location_id before any machine ranking. There are 1,018 such rows representing days before installation or after retirement; they are not zero-earning machines.
- Carded play and all play never match exactly. Compare carded values with carded_* on machine_day or prepared_daily_view. Guest tables are loyalty-card only.
- Join fact tables only after each has been aggregated. Joining sessions to fnb_transactions row by row double-counts money.
- A missing traffic count means the counter is offline, not zero. Check counter_status. Counts are crossings, not unique visitors.
- Use gaming days from 06:00 to 06:00 America/Los_Angeles for January 1–June 30, 2025. Weather timestamps are calendar dates, not gaming dates.
- Forecast split is January–April 2025 training and May–June 2025 test for both people where a forecast is involved.
- Tourism and visitor-profile files published after 2025 may explain historical context but cannot be forecast inputs that claim to have been available in 2025.
File ownership and safe parallel development
Create/maintain this structure:
work/
  shared/
    CONTRACT.md
    NOTES.md
  floor/
    notebooks and scripts
    out/
      machine_scorecard.parquet
      demand_daily.parquet
      model_card.md
  guests/
    notebooks and scripts
    out/
      player_month.parquet
      action_shortlist.md
dashboard/
  floor.html
  guests.html
  actions.html
  index.html
submission/
  writeup.md
  claims.md
  ai.md
File ownership:
- work/shared/CONTRACT.md: Akshaya creates the initial metric contract; both approve and sign off on metric names. After sign-off, neither changes a name without the other's agreement.
- work/shared/NOTES.md: both may append; never rewrite the other person's notes.
- dashboard/floor.html: Akshaya only.
- dashboard/guests.html and dashboard/actions.html: Vaishnavi only.
- dashboard/index.html: Vaishnavi only, and only after the other pages exist.
- submission/writeup.md: Vaishnavi drafts; Akshaya adds the model paragraph.
- submission/claims.md: each person writes only their own claims.
- submission/ai.md: each person documents their own AI use.
- Each person commits their own workstream folder and owned pages.
Use separate clones or separate machines if possible. If sharing a OneDrive folder, do not have both people edit the same file simultaneously; OneDrive is a backup, Git is the handoff. Work on branches floor and guests; merge to main only at checkpoints. Handoff parquet files, not notebooks. Akshaya must not load sessions, loyalty_ledger, or fnb_transactions; Vaishnavi must not load machine_hour. Leave example-dashboard.html unchanged; it is only a placeholder layout sample. Do not edit data/ or reference/.
Development checkpoints
1. Start
   - Akshaya creates work/floor/ and confirms prepared_daily_view has 56,110 rows and 1,018 null locations.
   - Vaishnavi creates work/guests/ and confirms player_period has 148,893 rows.
   - No merge yet.
2. First handoff
   - Akshaya publishes machine_scorecard.parquet with the manager's ten flagged, even if rank_fair is still a first pass.
   - Vaishnavi publishes player_month.parquet and a draft action_shortlist.md; machine targets may say waiting for Akshaya's scorecard.
   - Merge both handoff outputs to main.
3. Model lock
   - Akshaya publishes demand_daily.parquet and model_card.md, then freezes the model.
   - Vaishnavi prices actions against the locked scorecard and uses the model decision sentence.
   - Merge work/floor/out/.
4. Dashboard
   - Akshaya completes dashboard/floor.html with period and bank filters.
   - Vaishnavi completes dashboard/guests.html and dashboard/actions.html.
   - Merge dashboard pages.
5. Submission
   - Akshaya adds the model paragraph and her claims.
   - Vaishnavi finishes the 400-word write-up, appendix assembly, AI note coordination, and dashboard/index.html.
   - Merge submission files.
Before the first handoff, run:
python -m pip install duckdb
python scripts/verify_data.py
python scripts/verify_semantics.py
check_release.py is for challenge organizers; the release calibration warning can be ignored for participant analysis. Do not claim release validation passed unless actually run and passed.
Claims and evidence format
Each person writes only their own claims in submission/claims.md. Use this template once per claim:
### Claim
One sentence a manager can check.

Owner: Akshaya or Vaishnavi
Table:
Query or notebook:
Result:
Alternative explanation tested:
Limitation:
Akshaya's claims stay within questions 1–3 and the model. Vaishnavi's claims stay within questions 4–6. A claim needing both workstreams cites the other person's parquet handoff; it does not recompute the other person's analysis.
Final judging paths
Judges are expected to:
- Change the reporting period.
- Drill into one machine bank.
- Drill into one guest group.
- Find and inspect model validation.
- Trace at least one recommendation to its evidence.
Ensure these paths work in the public deployment. The public dashboard must open without either person's laptop.
Final submission responsibilities
- Public dashboard: both contribute; Vaishnavi owns the front-door link/integration. Test in a private browser window.
- Two-minute video: decide together in work/shared/NOTES.md; Akshaya explains the model, Vaishnavi states the priced actions.
- 400-word write-up: Vaishnavi drafts, with Akshaya's model paragraph.
- Model versus baseline: Akshaya.
- Code: each commits their own folder and steps that build their parquet outputs.
- Actions: Vaishnavi.
- AI disclosure: each person documents tool and use.
- Claims and evidence: each writes their own section.
PHASE 2: TECHNOLOGY INTEGRATIONS
I want to incorporate as many of the following technologies as possible, provided they add genuine functionality.

Evaluate each one individually.
1. Databricks
Potential uses:
- Data ingestion and transformation.
- Large-scale analytical processing.
- Feature engineering.
- Machine learning workflows.
- Aggregations for machine-level and player-level analytics.
Determine whether Databricks is worthwhile given the actual dataset size and available free resources.
2. Google Gemini API
Potential uses:
- AI-powered casino performance analyst.
- Natural-language questions about casino operations.
- Automated explanations of machine performance.
- Generating executive summaries.
- Explaining anomalies and forecasting results.
- Converting analytical findings into actionable recommendations.
The AI must use actual computed metrics and retrieved data rather than inventing answers.
3. Grok API / Grok Bot (xAI)
Potential uses:
- A separate conversational analyst.
- An alternative AI perspective on operational decisions.
- Challenging recommendations generated by the primary analysis.
- Comparing AI-generated interpretations.
Determine whether using both Gemini and Grok adds meaningful value. Avoid building two redundant chatbots.
4. MongoDB Atlas
Potential uses:
- Storing user preferences.
- Dashboard configurations.
- AI conversation history.
- Saved investigations.
- Generated reports.
- Alert configurations.
Evaluate whether MongoDB Atlas free-tier resources are sufficient.
5. Vultr
Evaluate:
- Application hosting.
- Backend deployment.
- Database or service hosting.
- Whether a genuinely free deployment option exists.
Do not assume Vultr is free. If it requires payment, credits, or a paid subscription, classify it as optional rather than a deployment dependency.
6. TigerData / Timescale
Potential uses:
- Time-series storage.
- Machine-level operational metrics.
- Availability and downtime tracking.
- Historical demand and payout trends.
- Time-series forecasting and anomaly detection.
Determine whether this is useful alongside the original datasets and Databricks, or whether it introduces unnecessary infrastructure.
7. Snowflake API
Potential uses:
- Analytical querying.
- Data warehousing.
- SQL-based analysis.
- Serving precomputed analytics to the dashboard.
Evaluate the Snowflake API and available free access carefully. Determine whether it provides an advantage over Databricks or whether the two overlap excessively.

Important: I want to use as many of these technologies as reasonably possible, but not at the expense of performance, reliability, cost, or implementation time.

For each technology, classify it as:
- Core: Strong reason to include.
- Optional: Useful if time and free resources permit.
- Redundant: Another selected technology performs the same job.
- Not recommended: Adds complexity without sufficient value.
Investigate current free-tier availability, API quotas, limitations, trial expiration, credit-card requirements, and deployment restrictions before recommending a service.

Never assume an API is free just because it offers free credits or a trial.
PHASE 3: DESIGN THE ACTUAL PRODUCT
I want a sophisticated product called:

DASHBOARD ROYALE
Luck, Location, or a Leak?

Think of this as an operational intelligence command center for casino management.

The dashboard should have a distinctive, premium visual identity. Avoid generic admin-dashboard templates.

Consider a dark casino-inspired interface with sophisticated typography, restrained neon accents, excellent data visualization, smooth interactions, and a clear visual hierarchy.

The design should look like a professional analytics product that could be presented to executives or investors.

Explore these modules:
A. Executive Command Center
- Total wagers.
- Total payouts.
- Net casino contribution.
- Machine availability.
- Operational losses.
- Six-month performance trends.
- Critical alerts.
- Most important findings.
- Executive recommendations.
B. Machine Intelligence
- All 300 machines.
- Machine performance rankings.
- Bottom ten machines.
- Demand versus payout comparisons.
- Availability and downtime.
- Machine contribution.
- Performance trends.
- Root-cause investigation.
C. Player Intelligence
- Tracked player activity.
- Total wagers.
- Total payouts received.
- Player net winnings/losses.
- Player segmentation.
- Behavioral trends.
Respect the dataset's available granularity and privacy limitations.
D. Time-Series Intelligence
- Historical trends.
- Demand forecasting.
- Contribution forecasting.
- Anomaly detection.
- Machine-level comparisons.
- Model performance and uncertainty.
E. AI Casino Analyst
Create an interactive natural-language interface where management can ask questions such as:
- Why are these ten machines underperforming?
- Is machine downtime responsible for their poor contribution?
- Which machines should we inspect first?
- What changed in customer demand over the last six months?
- Which machines have unusually high payout ratios?
- What would happen if we repaired rather than replaced these machines?
- What are the most important operational risks?
The AI should retrieve actual analytical results and explain them with evidence.

Consider Gemini as the primary analyst and Grok as an independent reviewer or second-opinion analyst, if both APIs are accessible within our budget.
F. Decision Simulator
This could be a major differentiator.

Allow management to explore hypothetical scenarios:
- What if we repair the ten lowest-performing machines?
- What if we replace only three?
- What if we improve availability by 5%?
- What if we allocate $20,000 to inspections?
- What if we preserve the entire budget?
Show estimated financial impact, assumptions, uncertainty, and expected outcomes.

Do not present hypothetical estimates as guaranteed returns.
G. 30-Day Action Center
Build an operational recommendation module.

The total available budget is $100,000.

Recommend up to three actions with:
- Estimated costs.
- Supporting evidence.
- Priority.
- Expected impact.
- Uncertainty.
- Success metrics.
- 30-day measurement plan.
The dashboard should help management decide whether to replace, repair, inspect, experiment, or preserve the budget.
PHASE 4: MACHINE LEARNING
At least one useful basic ML or time-series method is mandatory.

Evaluate suitable approaches based on the available data.

Potential methods:
- Time-series forecasting.
- Regression.
- Clustering.
- Anomaly detection.
- Demand prediction.
- Machine-level contribution prediction.
Do not use ML merely for decoration.

The selected method must answer a genuine business question.

Include:
- Feature selection.
- Training and validation methodology.
- Appropriate evaluation metrics.
- Leakage prevention.
- Prediction uncertainty.
- Visual presentation of findings.
Compare a simple baseline against the selected model.
PHASE 5: ARCHITECTURE
Propose an architecture that integrates the selected technologies without unnecessary duplication.

For example, evaluate a possible architecture involving:
1. Original CSV/Parquet datasets.
2. Databricks for processing and feature engineering.
3. Snowflake or TigerData for analytical storage, only if justified.
4. MongoDB Atlas for application state and AI conversations.
5. Python backend for analytics and API endpoints.
6. Gemini and Grok for AI-powered analysis.
7. Frontend dashboard for visualization and interaction.
8. Free hosting and deployment infrastructure.
This is only a starting hypothesis. You must evaluate alternatives rather than blindly adopting it.

Provide:
- Architecture diagram.
- Component responsibilities.
- Data flow.
- API interactions.
- Database schemas.
- Authentication and secrets management.
- Deployment architecture.
- Failure handling.
- Cost and quota considerations.
Avoid storing the same data in multiple databases without a clear reason.
PHASE 6: DEPLOYMENT — STRICTLY FREE
This is a non-negotiable requirement.

The completed application must be publicly accessible through a working deployment.

Deployment must use free tools and free-tier resources only.

No:
- Paid cloud servers.
- Paid database plans.
- Paid hosting subscriptions.
- Unplanned API charges.
- Infrastructure that automatically becomes paid after a trial.
- Mandatory paid services.
Investigate suitable options such as:
- Vercel.
- Streamlit Community Cloud.
- Hugging Face Spaces.
- GitHub Pages.
- Render free resources, if currently available.
- MongoDB Atlas free tier.
- Other genuinely free hosting options.
These are candidates, not predetermined choices. Verify their current restrictions and suitability.

Vultr must not be used for mandatory hosting unless there is a verified, genuinely free option available to us.

The final architecture must remain deployable if an optional paid-credit service becomes unavailable.

Also consider:
- Cold starts.
- Sleep limits.
- API rate limits.
- Dataset storage limits.
- Environment variables.
- Secrets management.
- Backend availability.
- Public access.
The application must actually work after deployment, not merely have deployment instructions.
PHASE 7: HACKATHON DIFFERENTIATION
Think critically about what would make this project stand out among competing hackathon submissions.

I want:
- A compelling problem statement.
- A distinctive product experience.
- Non-obvious analytical findings.
- Excellent visual storytelling.
- A useful ML component.
- Meaningful AI integration.
- A strong operational decision-making workflow.
- A credible financial recommendation.
- A working publicly accessible application.
Prioritize features that demonstrate intelligence, technical depth, and practical business value.

Avoid:
- Generic KPI dashboards.
- Unnecessary AI chatbots.
- Decorative charts without analytical value.
- Unsupported financial claims.
- Overcomplicated architecture.
- Integrations that exist only to showcase technology names.
PHASE 8: YOUR DELIVERABLE — A DETAILED IMPLEMENTATION PLAN
IMPORTANT: DO NOT START CODING YET. DO NOT MODIFY ANY PROJECT FILES.

I want a detailed implementation plan first.

Produce the following:
1. Repository assessment: What files exist, what the data contains, and what we can build from it.
2. Product vision: The proposed final application and its unique differentiators.
3. Feature breakdown: All proposed modules, prioritized into must-have, should-have, and optional.
4. Technology evaluation: A table covering all eight requested technologies, their intended purpose, free-tier limitations, integration complexity, and final recommendation.
5. Recommended architecture: A clear architecture diagram and explanation of the data flow.
6. Database design: What belongs in each database and why.
7. ML strategy: Recommended method, features, validation approach, and expected outputs.
8. AI strategy: How Gemini and Grok will access actual analytical data and produce grounded answers.
9. Frontend design: Page structure, navigation, visual identity, interactions, and chart recommendations.
10. Deployment plan: Exact free hosting choices and how the complete application will be deployed.
11. Cost breakdown: Expected costs for every service. The mandatory deployment and operation must remain within $0.
12. Implementation roadmap: An ordered, practical sequence of development tasks, including dependencies.
13. Risk assessment: Technical risks, free-tier limitations, API failures, data limitations, and fallback options.
14. Hackathon pitch: How to communicate the product's novelty, technical sophistication, and business value to judges.
For the roadmap, divide development into:
- Phase 1: Data exploration and validation.
- Phase 2: Data engineering and analytical pipeline.
- Phase 3: ML and forecasting.
- Phase 4: Backend and database integration.
- Phase 5: Frontend and dashboard.
- Phase 6: AI integration.
- Phase 7: Decision simulator and recommendations.
- Phase 8: Deployment, testing, and final polish.
For each phase, identify the expected deliverable and dependencies.
FINAL INSTRUCTIONS
Be ambitious but realistic.

I want the strongest possible hackathon submission, not the easiest implementation.

Make technology choices based on actual value, not hype.

Use the existing repository as the source of truth. Do not invent dataset columns, findings, or capabilities.

Clearly distinguish verified free services from free trials, promotional credits, and paid services.

If API keys or credentials are missing, identify exactly what I need to obtain rather than assuming access.

Your immediate task is to inspect the repository and return the complete implementation plan. Do not write application code or modify existing files until I review and approve the plan.
FINAL TEAM-EXECUTION GUARDRAILS
In the plan you return, every implementation task must identify its owner as Akshaya, Vaishnavi, or Both. Do not use generic labels such as Person 1/Person 2 without mapping them to the names above.

Preserve the exact workstream boundaries:
- Akshaya = Floor = floor branch = work/floor/ = dashboard/floor.html.
- Vaishnavi = Guests = guests branch = work/guests/ = dashboard/guests.html, dashboard/actions.html, and final dashboard/index.html.
Do not reassign the floor analysis, machine scorecard, downtime analysis, or required forecasting model to Vaishnavi. Do not reassign tracked-player, loyalty/comp, action-shortlist, budget, write-up, or guest dashboard ownership to Akshaya.

The product-level modules (executive command center, AI analyst, decision simulator, deployment, and final integration) may combine both people's outputs, but the implementation plan must still identify who builds each component and which handoff files it consumes.

Do not let the AI or dashboard recompute metrics that belong to the other workstream. Consume the published parquet handoffs and the shared metric contract.

The current challenge-specific requirements in this team plan take precedence over generic suggestions elsewhere in this prompt. In particular:
- The required model is Akshaya's daily floor coin-in forecast with the specified January–April / May–June time split, mean baseline, weekday-mean alternative, and MAE.
- Vaishnavi's recommendations are for July 1–30, 2025, use the action catalog and exact cost formula, and are limited to at most three action types and $100,000.
- The specified parquet schemas, file names, table ownership, gaming-day conventions, and sign conventions must be retained.
- The shared output dashboard must expose the exact judge paths described above.
Return the plan in a way that Akshaya and Vaishnavi can independently follow without having to infer who owns a task, which files they may edit, what data they may load, or what artifact they must hand off.
