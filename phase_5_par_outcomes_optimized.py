"""
Phase 5 Refinement (Optimized): Par Outcomes with Optimized Shrinkage
Using shrinkage parameter 50
"""

import pandas as pd
import numpy as np

print("Loading data with optimized shrinkage...")
residuals = pd.read_csv('residual_table.csv')
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')

# Condition averages
condition_avgs = analysis.groupby('condition')['player_hist_par'].mean().to_dict()

# Merge and recalculate
merged = residuals.merge(
    analysis[['player_id', 'event_id', 'year', 'round_num', 'player_hist_par', 'player_his_cnt']],
    on=['player_id', 'event_id', 'year', 'round_num'],
    how='inner'
)

merged = merged.dropna(subset=['projected_vs_par', 'actual_vs_par', 'condition', 'player_hist_par', 'player_his_cnt'])

# Recalculate with optimized parameter
SHRINKAGE_PARAM = 50
merged['condition_avg'] = merged['condition'].map(condition_avgs)
merged['projected_vs_par_opt'] = (
    (merged['player_hist_par'] * merged['player_his_cnt'] +
     merged['condition_avg'] * SHRINKAGE_PARAM) /
    (merged['player_his_cnt'] + SHRINKAGE_PARAM)
)

# Build par outcomes
results = []

for (event_id, year, round_num), group in merged.groupby(['event_id', 'year', 'round_num']):
    field_avg = group['projected_vs_par_opt'].mean()

    for _, player in group.iterrows():
        ev = field_avg - player['projected_vs_par_opt']
        actual = player['actual_vs_par']

        results.append({
            'ev': ev,
            'projected_vs_par': player['projected_vs_par_opt'],
            'actual_vs_par': actual,
            'beats_par': 1 if actual < 0 else 0,
            'matches_par': 1 if actual == 0 else 0,
            'over_par': 1 if actual > 0 else 0
        })

results_df = pd.DataFrame(results)
results_df['ev_bucket'] = (results_df['ev'] / 0.25).round() * 0.25

# Aggregate
par_outcomes = results_df.groupby('ev_bucket').agg({
    'projected_vs_par': 'mean',
    'beats_par': ['sum', 'count'],
    'matches_par': 'sum',
    'over_par': 'sum'
}).reset_index()

par_outcomes.columns = ['ev_bucket', 'avg_projected_vs_par', 'beats_par_count', 'total_players',
                         'matches_par_count', 'over_par_count']

par_outcomes['p_beats_par'] = par_outcomes['beats_par_count'] / par_outcomes['total_players']
par_outcomes['p_matches_par'] = par_outcomes['matches_par_count'] / par_outcomes['total_players']
par_outcomes['p_over_par'] = par_outcomes['over_par_count'] / par_outcomes['total_players']

# Merge with odds
odds = pd.read_csv('matchup_fair_odds_optimized.csv')
par_outcomes = par_outcomes.merge(
    odds[['ev_bucket', 'p_a_win', 'fair_american']],
    on='ev_bucket',
    how='left'
)

par_outcomes = par_outcomes.sort_values('ev_bucket').reset_index(drop=True)

print(f"\n=== OPTIMIZED PAR OUTCOMES (PARAM 50) ===")
display = par_outcomes[['ev_bucket', 'avg_projected_vs_par', 'total_players',
                        'p_beats_par', 'p_matches_par', 'p_over_par', 'p_a_win']].copy()
print(display.iloc[::15].to_string())

# Validation
ev_0 = par_outcomes[par_outcomes['ev_bucket'] == 0.0]
if not ev_0.empty:
    print(f"\nAt EV 0 (neutral):")
    print(f"  P(beats par) = {ev_0['p_beats_par'].values[0]:.1%}")
    print(f"  P(over par) = {ev_0['p_over_par'].values[0]:.1%}")
    print(f"  Win prob = {ev_0['p_a_win'].values[0]:.1%}")

# Save
save_cols = ['ev_bucket', 'avg_projected_vs_par', 'total_players',
             'beats_par_count', 'matches_par_count', 'over_par_count',
             'p_beats_par', 'p_matches_par', 'p_over_par',
             'p_a_win', 'fair_american']
par_outcomes[save_cols].to_csv('par_outcomes_by_ev_optimized.csv', index=False)
print(f"\nSaved to par_outcomes_by_ev_optimized.csv")
