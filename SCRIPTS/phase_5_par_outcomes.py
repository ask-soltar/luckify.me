"""
Phase 5 Refinement: Par Outcome Table with EV and Odds Differences

For each +EV/-EV bucket:
- Average projected_vs_par (par advantage)
- P(beats par) / P(matches par) / P(over par)
- Fair odds vs standard market (-110)
"""

import pandas as pd
import numpy as np

print("Loading residual table...")
residuals = pd.read_csv('residual_table.csv')
residuals = residuals.dropna(subset=['projected_vs_par', 'actual_vs_par'])

# Load 2-ball matchup lookup for +EV/-EV buckets
lookup = pd.read_csv('matchup_fair_odds.csv')

# Build results for each tournament-round
results = []

for (event_id, year, round_num), group in residuals.groupby(['event_id', 'year', 'round_num']):
    field_avg = group['projected_vs_par'].mean()

    for _, player in group.iterrows():
        projected = player['projected_vs_par']
        actual = player['actual_vs_par']

        # Calculate EV
        ev = field_avg - projected

        # Par outcomes
        beats_par = 1 if actual < 0 else 0
        matches_par = 1 if actual == 0 else 0
        over_par = 1 if actual > 0 else 0

        results.append({
            'ev': ev,
            'projected_vs_par': projected,
            'actual_vs_par': actual,
            'beats_par': beats_par,
            'matches_par': matches_par,
            'over_par': over_par
        })

results_df = pd.DataFrame(results)

# Bucket EV
results_df['ev_bucket'] = (results_df['ev'] / 0.25).round() * 0.25

# Group by EV bucket and calculate par probabilities
par_outcomes = results_df.groupby('ev_bucket').agg({
    'projected_vs_par': 'mean',
    'beats_par': ['sum', 'count'],
    'matches_par': 'sum',
    'over_par': 'sum'
}).reset_index()

par_outcomes.columns = ['ev_bucket', 'avg_projected_vs_par', 'beats_par_count', 'total_players',
                         'matches_par_count', 'over_par_count']

# Calculate probabilities
par_outcomes['p_beats_par'] = par_outcomes['beats_par_count'] / par_outcomes['total_players']
par_outcomes['p_matches_par'] = par_outcomes['matches_par_count'] / par_outcomes['total_players']
par_outcomes['p_over_par'] = par_outcomes['over_par_count'] / par_outcomes['total_players']

# Merge with win probabilities from matchup lookup
par_outcomes = par_outcomes.merge(
    lookup[['ev_bucket', 'p_a_win', 'fair_american']],
    on='ev_bucket',
    how='left'
)

# Calculate standard market odds at -110 (typical sportsbook vig)
# -110 = ~52.38% to break even
# For comparison: what would -110 odds be for the actual win probability
def american_to_prob(american):
    """Convert American odds to implied probability"""
    if pd.isna(american) or american == 0:
        return np.nan
    if american < 0:
        return -american / (-american + 100)
    else:
        return 100 / (american + 100)

def prob_to_american(prob):
    """Convert probability to American odds"""
    if prob == 0.5:
        return 100
    elif prob > 0.5:
        return -100 * prob / (1 - prob)
    else:
        return 100 * (1 - prob) / prob

# Standard -110 market
standard_market_prob = american_to_prob(-110)
par_outcomes['market_prob_at_minus_110'] = standard_market_prob

# If our fair prob differs from -110, show the vig difference
par_outcomes['vig_adjusted_american'] = par_outcomes['fair_american'].apply(
    lambda x: american_to_prob(x) if not pd.isna(x) else np.nan
)

# How much better/worse is our fair odds vs -110
par_outcomes['odds_advantage_vs_market'] = (
    par_outcomes['vig_adjusted_american'] - par_outcomes['market_prob_at_minus_110']
)

# Sort and round
par_outcomes = par_outcomes.sort_values('ev_bucket').reset_index(drop=True)

# Round for display
display_cols = ['ev_bucket', 'avg_projected_vs_par', 'total_players',
                'p_beats_par', 'p_matches_par', 'p_over_par',
                'p_a_win', 'fair_american', 'odds_advantage_vs_market']

par_outcomes_display = par_outcomes[display_cols].copy()
for col in ['avg_projected_vs_par', 'p_beats_par', 'p_matches_par', 'p_over_par',
            'p_a_win', 'odds_advantage_vs_market']:
    par_outcomes_display[col] = par_outcomes_display[col].round(4)

print("\n=== PAR OUTCOME TABLE BY +EV/-EV BUCKET ===")
print(par_outcomes_display.iloc[::15].to_string())

# Save full table
save_cols = ['ev_bucket', 'avg_projected_vs_par', 'total_players',
             'beats_par_count', 'matches_par_count', 'over_par_count',
             'p_beats_par', 'p_matches_par', 'p_over_par',
             'p_a_win', 'fair_american', 'odds_advantage_vs_market']
par_outcomes[save_cols].to_csv('par_outcomes_by_ev.csv', index=False)
print(f"\nSaved to par_outcomes_by_ev.csv")

# Key insights
print("\n=== KEY INSIGHTS ===")
ev_0 = par_outcomes[par_outcomes['ev_bucket'] == 0.0]
if not ev_0.empty:
    print(f"At EV 0 (neutral matchup):")
    print(f"  P(beats par) = {ev_0['p_beats_par'].values[0]:.1%}")
    print(f"  P(matches par) = {ev_0['p_matches_par'].values[0]:.1%}")
    print(f"  P(over par) = {ev_0['p_over_par'].values[0]:.1%}")
    print(f"  Win probability = {ev_0['p_a_win'].values[0]:.1%}")
    print(f"  Fair American = {ev_0['fair_american'].values[0]:.0f}")

# Show where beating par correlates with positive EV
print(f"\nPositive correlation check:")
print(f"  EV -3.0 beats par: {par_outcomes[par_outcomes['ev_bucket'] == -3.0]['p_beats_par'].values[0]:.1%}")
print(f"  EV 0.0  beats par: {par_outcomes[par_outcomes['ev_bucket'] == 0.0]['p_beats_par'].values[0]:.1%}")
print(f"  EV +3.0 beats par: {par_outcomes[par_outcomes['ev_bucket'] == 3.0]['p_beats_par'].values[0]:.1%}")
