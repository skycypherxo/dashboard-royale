# Machine Learning Model Card: Daily Floor Coin-In Forecasting

## Model Overview
- **Objective:** Forecast daily property-wide slot coin-in to optimize staffing schedules and promotion timing.
- **Training Period:** January 1 – April 30, 2025 (120 gaming days).
- **Testing Period (Out-of-Sample Holdout):** May 1 – June 30, 2025 (61 gaming days).
- **Target Variable:** `coin_in_usd` (total daily paid wagers on property).

## Model Comparison & Honest Validation
1. **Baseline Model (Constant Training Mean):**
   - Method: Predicts the overall historical daily mean from the training window ($1,368,421.15/day).
   - Test MAE (Mean Absolute Error): **$218,258.10**
2. **Alternative Model (Local Weekday-Stratified Mean):**
   - Method: Predicts mean daily coin-in conditioned on day-of-week (Monday through Sunday) estimated strictly on training data.
   - Test MAE (Mean Absolute Error): **$68,698.55**
   - Improvement: **68.52% reduction in prediction error**.

## Decision Impact (July Staffing & Promotions)
The weekday model captures the substantial demand swing from Tuesday troughs ($1.01M) to Saturday peaks ($1.84M). A flat baseline would under-forecast Saturday volume by over $470,000, risking severe understaffing of slot technicians and floor attendants during peak coin-in hours. Conversely, the weekday forecast prevents overstaffing on quiet mid-week shifts, directly informing July shift roster scheduling.
