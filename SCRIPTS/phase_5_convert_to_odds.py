"""
Phase 5: Convert Fair Probability to Fair Odds

Takes win probability and converts to:
- Decimal odds (direct: 1 / probability)
- American odds (moneyline format)
"""

import pandas as pd
import numpy as np

print("Loading matchup probability lookup...")
df = pd.read_csv('matchup_edge_lookup.csv')

# Convert probability to fair odds
df['fair_decimal'] = 1.0 / df['p_a_win']

# American odds formula
def prob_to_american(prob):
    """Convert probability to American odds (moneyline)"""
    if pd.isna(prob) or prob <= 0 or prob >= 1:
        return np.nan  # Invalid probability
    if prob == 0.5:
        return 100  # Even money
    elif prob > 0.5:
        # Favorite: negative odds
        return -100 * prob / (1 - prob)
    else:
        # Underdog: positive odds
        return 100 * (1 - prob) / prob

df['fair_american'] = df['p_a_win'].apply(prob_to_american)

# Round for readability
df['fair_decimal'] = df['fair_decimal'].round(3)
df['fair_american'] = df['fair_american'].round(0)

# For display: show American as formatted
def format_american(x):
    if pd.isna(x):
        return "N/A"
    return f"{int(x):+d}" if x < 0 else f"+{int(x)}"

df['american_formatted'] = df['fair_american'].apply(format_american)

print("\n=== FAIR ODDS BY +EV/-EV BUCKET ===")
display = df[['ev_bucket', 'total_matchups', 'p_a_win', 'fair_decimal', 'fair_american', 'american_formatted']].copy()
print(display.iloc[::15])  # Every 15th row

# Save full table
output_cols = ['ev_bucket', 'total_matchups', 'p_a_win', 'p_tie', 'p_a_loss',
               'fair_decimal', 'fair_american']
df_output = df[output_cols]
df_output.to_csv('matchup_fair_odds.csv', index=False)
print(f"\nSaved to matchup_fair_odds.csv")

# Validation
print("\n=== VALIDATION ===")

# At EV 0, should be close to -110 (standard even-money)
ev_0 = df[df['ev_bucket'] == 0.0]
if not ev_0.empty:
    prob = ev_0['p_a_win'].values[0]
    american = ev_0['fair_american'].values[0]
    decimal = ev_0['fair_decimal'].values[0]
    print(f"At EV 0 (even matchup):")
    print(f"  P(A wins) = {prob:.1%}")
    print(f"  Fair decimal = {decimal:.3f}")
    print(f"  Fair American = {american:.0f}")
    print(f"  (Standard -110 is typical market vig)")

# Check relationship: higher probability = lower odds number
print(f"\nMonotonicity check (decimal odds should decrease with EV):")
sample = df[['ev_bucket', 'p_a_win', 'fair_decimal']].iloc[[50, 100, 110, 120, 150]]
print(sample)

# Sanity: American odds should flip from positive to negative around 50%
prob_50_idx = (df['p_a_win'] - 0.5).abs().idxmin()
print(f"\nAround 50% probability:")
print(df[['ev_bucket', 'p_a_win', 'fair_american']].iloc[prob_50_idx-2:prob_50_idx+3])
