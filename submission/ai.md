# Artificial Intelligence Use Disclosure

**Project:** Dashboard Royale (TAMU Datathon 2026)  
**Authors:** Vaishnavi (Guest & Business Intelligence Lead) & Akshaya (Floor & ML Lead)  
**Submission Date:** July 2025 / November 2026  
**Document Status:** Complete & Audited  

---

## 1. Executive Summary & Policy Compliance

In accordance with TAMU Datathon guidelines and challenge rules ("AI tools are allowed with disclosure"), this document outlines all artificial intelligence (AI), machine learning (ML), and large language model (LLM) tools utilized during the analytical investigation, data engineering, dashboard authoring, and documentation for **Dashboard Royale**.

All core analytical decisions, hypothesis formulations, accounting verifications, and financial interpretations were conducted with rigorous human oversight. Every numerical claim was independently verified against raw Parquet tables and cross-checked using deterministic Python and Pandas verification routines.

---

## 2. Tools & Models Utilized

| Tool / Model | Developer / Provider | Primary Application | Role & Scope |
|---|---|---|---|
| **Google Gemini 3.8 Flash (High)** | Google DeepMind | Code generation, data analysis scripts, dashboard layout engineering, and documentation drafting | Assisted with data exploration scripts, mathematical sanity checks, SVG visualization logic, and draft synthesis. |
| **Python Data Science Stack** | Open Source (Pandas, PyArrow, NumPy) | Deterministic data manipulation, accounting checks, parquet generation, and KPI calculations | Executed all source-of-truth calculations without AI hallucination risk. |

---

## 3. Workflow & Specific Applications

### A. Data Engineering & Semantic Verification
- **Application:** Scripting automated sanity checks on `player_period`, `property_day`, `prepared_daily_view`, and `operations`.
- **AI Role:** Generated boilerplate Python scripts for verifying accounting identities (e.g., verifying that $\text{Player Net} = \text{Payouts} - \text{Coin-in}$ and $\text{Residual} = \text{Net} + \text{Theo}$).
- **Human Oversight:** The underlying accounting formulas were dictated by human leads from `DATASET.md` and `CONTRACT.md`. All verification test outputs were audited; residuals were verified to be $\le 10^{-10}$ (floating-point epsilon).

### B. Analytical Exploration & Concentration Analysis
- **Application:** Calculation of Gini coefficient (0.754), Lorenz curve coordinates, decile concentration breakdowns, and demographic aggregations.
- **AI Role:** Assisted in drafting vectorized Pandas routines to compute cumulative wealth distributions and format JSON serialization structures.
- **Human Oversight:** Output values (e.g., Top 1% generating 22.85% of coin-in; Locals generating 58.60% of coin-in) were cross-validated directly against SQL aggregations on raw tables.

### C. Interactive Dashboard Development
- **Application:** Creating standalone, zero-dependency HTML/CSS/JavaScript interactive dashboards (`dashboard/floor.html`, `dashboard/guests.html`, `dashboard/actions.html`, `dashboard/index.html`).
- **AI Role:** Accelerated front-end scaffolding, responsive CSS styling matching the casino color palette, interactive DOM manipulation, and dynamic SVG chart rendering (Lorenz curves, bar charts, Gantt schedules).
- **Human Oversight:** All data inputs were precomputed deterministically and embedded as static JSON objects; no generative AI runs client-side in the browser. Interactive filters and theme toggles were manually tested for accessibility, responsiveness, and zero console errors.

### D. Time-Series Forecasting & Machine Learning Modeling (Akshaya)
- **Application:** Scripting the out-of-sample holdout split (Jan–Apr training vs May–Jun testing), computing Mean Absolute Error (MAE) benchmarks, and generating `model_card.md`.
- **AI Role:** Assisted in drafting baseline mean and weekday-stratified time-series evaluation routines in DuckDB.
- **Human Oversight:** Ensured strict isolation between training and holdout windows to eliminate data leakage; verified that no post-2025 external variables or test set values leaked into training parameters. Test MAEs ($68,698.55 vs $218,258.10) were deterministically calculated.

### E. Documentation & Appendix Assembly
- **Application:** Drafting the 400-word submission writeup (`submission/writeup.md`), claims appendix (`submission/claims.md`), and action shortlist (`work/guests/out/action_shortlist.md`).
- **AI Role:** Assisted in synthesizing findings into concise prose, ensuring strict adherence to the 400-word limit and formatting claims in the required five-part structure (Claim → Data Source / Query → Result → Alternative Explanation → Limitations).
- **Human Oversight:** Every claim and number was audited against the data contract. Word counts were verified programmatically (370 words).

---

## 4. Verification & Safeguards Against Hallucination

1. **Deterministic Verification:** No analytical number presented in the dashboard or submission was generated by LLM conjecture. All figures originated from queries run against `data/`.
2. **Double-Counting Prevention:** Explicit verification checks were implemented to ensure comp economic costs ($190,669.30) were not subtracted twice from POS COGS ($591,346.70).
3. **Budget Compliance Check:** Catalog pricing formulas from `GUIDE.md` were coded directly to ensure that lead times and operating days were accurately computed, strictly enforcing the $100,000 ceiling.
4. **Code Transparency:** All transformation and calculation scripts are retained within `work/guests/` for full reproducibility.

