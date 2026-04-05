"""
Phase 4 (Optimized): 2-Ball Matchup Edge-to-Win Probability
Using optimal shrinkage parameter: 50 (not 12)

Recalculates projected_vs_par with param 50, then builds matchup lookup.
"""

import pandas as pd
import numpy as np

print("Loading data...")
residuals = pd.read_csv('residual_table.csv')
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')

# Get condition averages
condition_avgs = analysis.groupby('condition')['player_hist_par'].mean().to_dict()
print(f"Condition averages: {condition_avgs}")

# Merge to get sample sizes
merged = residuals.merge(
    analysis[['player_id', 'event_id', 'year', 'round_num', 'player_hist_par', 'player_his_cnt']],
    on=['player_id', 'event_id', 'year', 'round_num'],
    how='inner'
)

merged = merged.dropna(subset=['projected_vs_par', 'actual_vs_par', 'condition', 'player_hist_par', 'player_his_cnt'])

print(f"Total player-rounds: {len(merged)}")

# RECALCULATE projected_vs_par with OPTIMAL shrinkage parameter (50, not 12)
SHRINKAGE_PARAM = 50
merged['condition_avg'] = merged['condition'].map(condition_avgs)
merged['projected_vs_par_optimized'] = (
    (merged['player_hist_par'] * merged['player_his_cnt'] +
     merged['condition_avg'] * SHRINKAGE_PARAM) /
    (merged['player_his_cnt'] + SHRINKAGE_PARAM)
)

print(f"Recalculated projected_vs_par with shrinkage parameter = {SHRINKAGE_PARAM}")

# Generate all 2-ball matchups
results = []

for (event_id, year, round_num), group in merged.groupby(['event_id', 'year', 'round_num']):
    field_avg_projected = group['projected_vs_par_optimized'].mean()

    # Pairwise matchups
    players_list = group.to_dict('records')

    for i in range(len(players_list)):
        for j in range(i + 1, len(players_list)):
            player_a = players_list[i]
            player_b = players_list[j]

            # Calculate +EV (positive = advantage)
            ev_a = field_avg_projected - player_a['projected_vs_par_optimized']
            ev_b = field_avg_projected - player_b['projected_vs_par_optimized']
            relative_ev = ev_a - ev_b

            # Outcome
            actual_a = player_a['actual_vs_par']
            actual_b = player_b['actual_vs_par']
            a_wins = 1 if actual_a < actual_b else 0
            is_tie = 1 if actual_a == actual_b else 0

            results.append({
                'event_id': event_id,
                'year': year,
                'round_num': round_num,
                'player_a': player_a['player_name'],
                'player_b': player_b['player_name'],
                'ev_a': ev_a,
                'ev_b': ev_b,
                'relative_ev': relative_ev,
                'a_wins': a_wins,
                'is_tie': is_tie,
            })

results_df = pd.DataFrame(results)
print(f"Generated {len(results_df):,} matchups")

# Bucket EV
results_df['ev_bucket'] = (results_df['relative_ev'] / 0.25).round() * 0.25

# Aggregate
lookup = results_df.groupby('ev_bucket').agg({
    'a_wins': ['count', 'sum'],
    'is_tie': 'sum'
}).reset_index()

lookup.columns = ['ev_bucket', 'total_matchups', 'a_wins', 'ties']
lookup['a_loss'] = lookup['total_matchups'] - lookup['a_wins'] - lookup['ties']

# Probabilities
lookup['p_a_win'] = lookup['a_wins'] / (lookup['total_matchups'] - lookup['ties'])
lookup['p_tie'] = lookup['ties'] / lookup['total_matchups']
lookup['p_a_loss'] = lookup['a_loss'] / (lookup['total_matchups'] - lookup['ties'])

# Sort
lookup = lookup.sort_values('ev_bucket').reset_index(drop=True)

print("\n=== OPTIMIZED 2-BALL LOOKUP (PARAM 50) ===")
print(lookup[['ev_bucket', 'total_matchups', 'p_a_win', 'p_tie']].iloc[::20])

# Validation
ev_0 = lookup[lookup['ev_bucket'] == 0.0]
if not ev_0.empty:
    print(f"\nAt EV 0: P(A wins) = {ev_0['p_a_win'].values[0]:.1%}")

# Save
lookup.to_csv('matchup_edge_lookup_optimized.csv', index=False)
print(f"\nSaved to matchup_edge_lookup_optimized.csv")
