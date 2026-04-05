"""
Phase 4: 2-Ball Matchup Edge-to-Win Probability

For each 2-ball matchup in tournament history:
- Calculate relative edge (edge_A - edge_B)
- Track who won (lower actual_vs_par)
- Build empirical lookup: relative_edge_bucket -> P(A wins)
"""

import pandas as pd
import itertools

print("Loading residual table...")
residuals = pd.read_csv('residual_table.csv')
residuals = residuals.dropna(subset=['projected_vs_par', 'actual_vs_par'])

# For each tournament-round, generate all pairwise matchups
results = []

for (event_id, year, round_num), group in residuals.groupby(['event_id', 'year', 'round_num']):
    field_avg_projected = group['projected_vs_par'].mean()

    # Calculate edge for each player in this tournament
    group_copy = group.copy()
    group_copy['edge'] = field_avg_projected - group_copy['projected_vs_par']

    # Get all pairwise combinations (A vs B, A > B only to avoid duplicates)
    players_list = group_copy.to_dict('records')

    for i in range(len(players_list)):
        for j in range(i + 1, len(players_list)):
            player_a = players_list[i]
            player_b = players_list[j]

            # Player A vs Player B
            edge_a = player_a['edge']
            edge_b = player_b['edge']

            relative_edge = edge_a - edge_b  # Positive = A better than B

            # Who won? (Lower actual_vs_par wins)
            actual_a = player_a['actual_vs_par']
            actual_b = player_b['actual_vs_par']

            a_wins = 1 if actual_a < actual_b else 0

            # Tie handling
            is_tie = 1 if actual_a == actual_b else 0

            results.append({
                'event_id': event_id,
                'year': year,
                'round_num': round_num,
                'player_a': player_a['player_name'],
                'player_b': player_b['player_name'],
                'edge_a': edge_a,
                'edge_b': edge_b,
                'relative_edge': relative_edge,
                'a_wins': a_wins,
                'is_tie': is_tie,
                'actual_a': actual_a,
                'actual_b': actual_b,
            })

results_df = pd.DataFrame(results)
print(f"Total 2-ball matchups generated: {len(results_df)}")

# Bucket relative edge
results_df['edge_bucket'] = (results_df['relative_edge'] / 0.25).round() * 0.25

# Group by edge bucket and calculate win probability
lookup = results_df.groupby('edge_bucket').agg({
    'a_wins': ['count', 'sum'],
    'is_tie': 'sum'
}).reset_index()

lookup.columns = ['edge_bucket', 'total_matchups', 'a_wins', 'ties']
lookup['a_loss'] = lookup['total_matchups'] - lookup['a_wins'] - lookup['ties']

# Calculate probabilities (excluding ties from denominator)
lookup['p_a_win'] = lookup['a_wins'] / (lookup['total_matchups'] - lookup['ties'])
lookup['p_tie'] = lookup['ties'] / lookup['total_matchups']
lookup['p_a_loss'] = lookup['a_loss'] / (lookup['total_matchups'] - lookup['ties'])

# Sort
lookup = lookup.sort_values('edge_bucket').reset_index(drop=True)

print("\n=== 2-BALL MATCHUP WIN PROBABILITY LOOKUP ===")
print(lookup[['edge_bucket', 'total_matchups', 'p_a_win', 'p_tie', 'p_a_loss']].head(25))

# Save
lookup.to_csv('matchup_edge_lookup.csv', index=False)
print(f"\nSaved to matchup_edge_lookup.csv")

# Validate: should be monotonically increasing
print("\n=== VALIDATION ===")
print("P(A wins) by relative edge (should increase with edge):")
print(lookup[['edge_bucket', 'total_matchups', 'p_a_win']].iloc[::10])

# Sanity check: at edge 0, should be ~50%
edge_0 = lookup[lookup['edge_bucket'] == 0.0]
if not edge_0.empty:
    print(f"\nAt edge 0 (even matchup): P(A wins) = {edge_0['p_a_win'].values[0]:.1%}")

# Check monotonicity
p_win_values = lookup['p_a_win'].dropna().values
violations = sum(1 for i in range(1, len(p_win_values)) if p_win_values[i] < p_win_values[i-1])
print(f"Monotonicity violations: {violations}")
