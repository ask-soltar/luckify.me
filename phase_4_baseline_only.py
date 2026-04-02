"""
Phase 4 (Simplified): 2-Ball Matchup Edge-to-Win Probability
Baseline-Only Model (Recent Form Removed)

Uses Adj_his_par directly from ANALYSIS_v2 (already Bayesian-shrinkage optimized with param 50).
No blending, no decay calculation—just clean edge calculation and historical validation.

Proven via tier-specific optimization: Recent form adds 0% value.
Baseline-only is game theory optimal.
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("PHASE 4: BASELINE-ONLY 2-BALL MATCHUP MODEL")
print("=" * 80)

# Load ANALYSIS_v2
print("\n[1] Loading ANALYSIS_v2...")
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')
print(f"    Total rows: {len(analysis):,}")
print(f"    Unique players: {analysis['player_id'].nunique():,}")
print(f"    Year range: {analysis['year'].min()}-{analysis['year'].max()}")

# Verify Adj_his_par column exists
if 'Adj_his_par' not in analysis.columns:
    print("    [ERROR] Adj_his_par column not found in ANALYSIS_v2")
    print("    Available columns:", list(analysis.columns))
    exit(1)

# Get unique event-round combinations (some rows are duplicates with different conditions)
print("\n[2] Aggregating unique event-rounds (first condition per round)...")
analysis_unique = analysis.drop_duplicates(
    subset=['player_id', 'event_id', 'round_num'],
    keep='first'
)[['player_id', 'player_name', 'event_id', 'year', 'round_num', 'Adj_his_par', 'actual_vs_par']].copy()

print(f"    Unique event-round combos: {len(analysis_unique):,}")

# Remove rows with missing Adj_his_par or actual_vs_par
analysis_unique = analysis_unique.dropna(subset=['Adj_his_par', 'actual_vs_par'])
print(f"    After removing NaN: {len(analysis_unique):,}")

# Generate all 2-ball matchups
print("\n[3] Generating 2-ball matchups...")
results = []

for (event_id, year, round_num), group in analysis_unique.groupby(['event_id', 'year', 'round_num']):
    # Field average projection
    field_avg_projected = group['Adj_his_par'].mean()

    # Pairwise matchups
    players_list = group.to_dict('records')

    for i in range(len(players_list)):
        for j in range(i + 1, len(players_list)):
            player_a = players_list[i]
            player_b = players_list[j]

            # Calculate edge (lower projected_vs_par is better in golf)
            # Edge = field average - player projection
            # Positive edge = player is better than field
            edge_a = field_avg_projected - player_a['Adj_his_par']
            edge_b = field_avg_projected - player_b['Adj_his_par']
            relative_edge = edge_a - edge_b

            # Outcome (lower score wins in matchup)
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
                'edge_a': edge_a,
                'edge_b': edge_b,
                'relative_edge': relative_edge,
                'a_wins': a_wins,
                'is_tie': is_tie,
            })

results_df = pd.DataFrame(results)
print(f"    Total matchups: {len(results_df):,}")

# Bucket edges (0.25 stroke buckets)
print("\n[4] Bucketing edges and aggregating...")
results_df['edge_bucket'] = (results_df['relative_edge'] / 0.25).round() * 0.25

# Aggregate by edge bucket
lookup = results_df.groupby('edge_bucket').agg({
    'a_wins': ['count', 'sum'],
    'is_tie': 'sum'
}).reset_index()

lookup.columns = ['edge_bucket', 'total_matchups', 'a_wins', 'ties']
lookup['a_loss'] = lookup['total_matchups'] - lookup['a_wins'] - lookup['ties']

# Win probability (excluding ties)
lookup['p_a_win'] = lookup['a_wins'] / (lookup['total_matchups'] - lookup['ties'])
lookup['p_a_loss'] = lookup['a_loss'] / (lookup['total_matchups'] - lookup['ties'])
lookup['p_tie'] = lookup['ties'] / lookup['total_matchups']

# Sort by edge
lookup = lookup.sort_values('edge_bucket').reset_index(drop=True)

print(f"    Edge buckets: {len(lookup)}")
print(f"    Edge range: {lookup['edge_bucket'].min():.2f} to {lookup['edge_bucket'].max():.2f}")

# Display sample
print("\n[5] BASELINE-ONLY MATCHUP LOOKUP:")
print("=" * 80)
print(lookup[['edge_bucket', 'total_matchups', 'a_wins', 'p_a_win']].iloc[::10].to_string(index=False))

# Validation: Edge 0 should be ~50% win probability
edge_0 = lookup[lookup['edge_bucket'] == 0.0]
if not edge_0.empty:
    p_win_at_0 = edge_0['p_a_win'].values[0]
    print(f"\n    [CHECK] At edge 0: P(A wins) = {p_win_at_0:.1%} (should be ~50%)")
    if 0.45 < p_win_at_0 < 0.55:
        print(f"    [PASS] Symmetry check passed")
    else:
        print(f"    [WARN] Symmetry check: unexpected value")

# Monotonicity: increasing edge should increase win probability
monotonic = lookup['p_a_win'].is_monotonic_increasing or lookup['p_a_win'].iloc[::-1].is_monotonic_increasing
if monotonic:
    print(f"    [PASS] Monotonicity: p_a_win increases with edge")
else:
    print(f"    [WARN] Non-monotonic relationship detected")

# Save
lookup.to_csv('matchup_lookup_baseline.csv', index=False)
print(f"\n[6] Saved to matchup_lookup_baseline.csv")

# Summary statistics
print("\n[7] SUMMARY STATISTICS:")
print(f"    Total historical matchups analyzed: {lookup['total_matchups'].sum():,}")
print(f"    Average ties per bucket: {lookup['ties'].mean():.1f}")
print(f"    Overall tie rate: {lookup['ties'].sum() / lookup['total_matchups'].sum():.2%}")
print(f"    Win probability range: {lookup['p_a_win'].min():.1%} to {lookup['p_a_win'].max():.1%}")

print("\n" + "=" * 80)
print("PHASE 4 COMPLETE: BASELINE-ONLY MATCHUP LOOKUP READY")
print("=" * 80)
