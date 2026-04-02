# Golf Pricing Model Workflow

## Overview
Structured workflow for building a fair-value pricing model for 2-ball, 3-ball, and tournament golf matchups.

## Phase Architecture

### Phase 1: Build the Projection Spine
**Goal:** Calculate expected score edge between players

- **Input:** `player_hist_par` (filtered by condition bucket)
- **Source:** ANALYSIS_v2 sheet, Column R (`Adj_his_par`)
- **Calculation:** Bayesian shrinkage formula
  ```
  (player_hist_par * N + condition_avg * 12) / (N + 12)
  ```
- **Output:** `projected_vs_par` for each player

### Phase 2: Measure Uncertainty
**Goal:** Quantify the error distribution around projections

1. **Build Residuals**
   - Formula: `residual = actual_vs_par - projected_vs_par`
   - Source: `residual_table.csv` (67,860 player-rounds)
   - Filters: Exclude REMOVE round type, null scores, Tough condition

2. **Player Volatility**
   - Metric: `resid_sd` (residual standard deviation)
   - Source: `player_volatility_table.csv` (1,232 players)
   - Shrinkage: Blend player SD with field SD when N < 50
   - Reliability buckets:
     - STRONG: N ≥ 50
     - MEDIUM: 20 ≤ N < 50
     - WEAK: N < 20

3. **Key Statistics**
   - Field SD: 3.667 strokes
   - Early rounds (Open/Survival) noisier than late rounds (Positioning/Closing)
   - Calm condition slightly higher residual bias than Moderate

### Phase 3: Handle Golf-Specific Market Structure
**TODO:**
- Tie rate analysis (golf pushes often)
- Settlement rules by market type
- Dead heat handling

### Phase 4: Convert Edge to Win Probability
**Current approach:** Empirical bucket lookup (best for v1)

**Next steps:**
1. Bucket `proj_edge_strokes` into 0.25-stroke increments
2. Build historical win/tie/loss % by bucket
3. Create lookup table: edge_bucket → fair_win_prob

### Phase 5: Convert Probability to Odds
Once fair probability established:
- Fair decimal: `1 / fair_prob`
- Fair American: Standard conversion formula

### Phase 6: Backtest and Calibrate
Test model against actual outcomes by:
- Projected edge bucket
- Sample quality (STRONG/MEDIUM/WEAK)
- Round type (Open/Survival/Positioning/Closing)
- Condition bucket (Calm/Moderate)

---

## Technical Setup

### Google Sheets Authentication
**Method:** Service account credentials file

**File:** `luckifyme-f6c83489cd24.json` (in D:\Projects\luckify-me)

**Library:** gspread + google-auth-oauthlib

**Sheet ID:** `1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok`

**Python pattern:**
```python
import gspread
from google.oauth2.service_account import Credentials

CREDS_FILE = "luckifyme-f6c83489cd24.json"
SHEET_ID = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
ss = client.open_by_key(SHEET_ID)
ws = ss.worksheet("SHEET_NAME")
ws.update('A1', data, value_input_option="USER_ENTERED")
```

### Data Tables Structure

#### RESIDUAL_TABLE (residual_table.csv)
- **Rows:** 67,860 player-rounds
- **Columns:**
  - player_name, player_id, event_name, event_id, year, round_num
  - condition, round_type
  - score, par, actual_vs_par, projected_vs_par, residual
- **Use:** Foundation for volatility analysis

#### PLAYER_VOLATILITY (player_volatility_table.csv)
- **Rows:** 1,232 players
- **Columns:**
  - player_id, player_name
  - resid_n (sample size)
  - resid_mean, resid_sd (raw volatility)
  - adj_sd (shrinkage-adjusted SD)
  - reliability (STRONG/MEDIUM/WEAK)
- **Use:** Player uncertainty for pricing engine

---

## Current Status

✅ **Phase 1 Complete:** Projection spine (player_hist_par) established
✅ **Phase 2 Complete:** Residuals calculated, volatility measured
⏳ **Phase 3 Pending:** Golf market structure analysis (tie rates, rules)
⏳ **Phase 4 Pending:** Edge-to-probability empirical lookup
⏳ **Phase 5 Pending:** Probability-to-odds conversion
⏳ **Phase 6 Pending:** Backtest framework

---

## Key Insights

### From Residual Analysis
- **Positive bias:** Model is ~1.1 strokes optimistic on average
  - Calm: +1.708 ± 3.805 (more bias)
  - Moderate: +0.210 ± 3.231 (better calibrated)
- **Round progression:** Early rounds noisier, late rounds more predictable
  - Open: +1.298 ± 3.702
  - Survival: +1.273 ± 3.754
  - Positioning: +0.851 ± 3.400
  - Closing: +0.816 ± 3.615

### From Volatility Analysis
- **65% weak-sample players:** Shrinkage critical for small-N players
- **Field SD:** 3.667 strokes (baseline uncertainty)
- **Player range:** 2.7-6.6 strokes after shrinkage

### From Market Analysis (Reverse Engineering)
- Market pricing is ~93% baseline + 7.5% model influence
- Historical par scores don't directly predict 3-ball market odds
- **Lesson:** Market has independent pricing factors beyond historical par

---

## Next Steps (Priority Order)

1. **Build empirical edge bucket lookup**
   - Bucket residuals by edge_strokes increments
   - Calculate win% / tie% / loss% per bucket

2. **Test edge-to-probability conversion**
   - Simple mapping vs. logistic model
   - Validate against actual outcomes

3. **Backtest framework**
   - Split results by edge bucket, sample quality, round, condition
   - ROI analysis at market odds

4. **Golf market structure**
   - Tie rate analysis
   - Settlement rule validation
   - Dead heat handling
