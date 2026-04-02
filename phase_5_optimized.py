"""
Phase 5 (Optimized): Convert Fair Probability to Fair Odds
Using optimized 2-ball matchup lookup (shrinkage param 50)
"""

import pandas as pd
import numpy as np

print("Loading optimized matchup lookup...")
df = pd.read_csv('matchup_edge_lookup_optimized.csv')

# Convert to odds
df['fair_decimal'] = 1.0 / df['p_a_win']

def prob_to_american(prob):
    if pd.isna(prob) or prob <= 0 or prob >= 1:
        return np.nan
    if prob == 0.5:
        return 100
    elif prob > 0.5:
        return -100 * prob / (1 - prob)
    else:
        return 100 * (1 - prob) / prob

df['fair_american'] = df['p_a_win'].apply(prob_to_american)

df['fair_decimal'] = df['fair_decimal'].round(3)
df['fair_american'] = df['fair_american'].round(0)

# Format
def format_american(x):
    if pd.isna(x):
        return "N/A"
    return f"{int(x):+d}" if x < 0 else f"+{int(x)}"

df['american_formatted'] = df['fair_american'].apply(format_american)

print("\n=== OPTIMIZED FAIR ODDS (PARAM 50) ===")
display = df[['ev_bucket', 'total_matchups', 'p_a_win', 'fair_decimal', 'fair_american']].copy()
print(display.iloc[::25])

# Validation
ev_0 = df[df['ev_bucket'] == 0.0]
if not ev_0.empty:
    prob = ev_0['p_a_win'].values[0]
    decimal = ev_0['fair_decimal'].values[0]
    american = ev_0['fair_american'].values[0]
    print(f"\nAt EV 0 (even matchup):")
    print(f"  P(A wins) = {prob:.1%}")
    print(f"  Fair decimal = {decimal:.3f}")
    print(f"  Fair American = {american:.0f}")

# Save
output_cols = ['ev_bucket', 'total_matchups', 'p_a_win', 'p_tie', 'p_a_loss',
               'fair_decimal', 'fair_american']
df_output = df[output_cols]
df_output = df_output.replace({np.nan: '', np.inf: '', -np.inf: ''})
df_output.to_csv('matchup_fair_odds_optimized.csv', index=False)
print(f"\nSaved to matchup_fair_odds_optimized.csv")
