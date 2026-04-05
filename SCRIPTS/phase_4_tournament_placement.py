"""
Phase 4: Convert Edge to Win Probability (Empirical Lookup)

Build historical win/tie/loss % by edge bucket.
Tournament placement lookup: edge_bucket -> P(Top 5/10/20/40)

CRITICAL FIX: Edge must be inverted
- In golf, lower vs_par is BETTER
- So edge = field_avg_projected - player_projected (not player - field_avg)
- Negative projected_vs_par (like -8) is good, so higher field_avg means positive edge
"""

import pandas as pd
import numpy as np

# Load residual table (foundation for accurate edges)
print("Loading residual table...")
residuals = pd.read_csv('residual_table.csv')

# Remove rows with missing critical columns
residuals = residuals.dropna(subset=['projected_vs_par', 'actual_vs_par'])
print(f"Rows after cleanup: {len(residuals)}")

# Group by tournament (event_id + year + round_num)
# to calculate field averages and derive finishing positions
results = []

for (event_id, year, round_num), group in residuals.groupby(['event_id', 'year', 'round_num']):
    # Calculate field average projected_vs_par
    field_avg_projected = group['projected_vs_par'].mean()

    # Rank by actual_vs_par (lower = better = higher finish)
    # finish_position 1 is best, last is worst
    group_ranked = group.copy()
    group_ranked['finish_position'] = group_ranked['actual_vs_par'].rank(method='min')

    # Calculate CORRECTED edge: field_average - player_projected
    # This ensures:
    # - Negative projected (like -8) with positive field_avg gives positive edge
    # - Positive edge = player better than field = higher finish probability
    group_ranked['edge'] = field_avg_projected - group_ranked['projected_vs_par']

    # Bucket edge into 0.25 increments
    group_ranked['edge_bucket'] = (group_ranked['edge'] / 0.25).round() * 0.25

    # Track tournament info
    group_ranked['event_id'] = event_id
    group_ranked['year'] = year
    group_ranked['round_num'] = round_num

    results.append(group_ranked)

results_df = pd.concat(results, ignore_index=True)
print(f"Total player-round observations: {len(results_df)}")

# Create finishing metrics
results_df['top_5'] = (results_df['finish_position'] <= 5).astype(int)
results_df['top_10'] = (results_df['finish_position'] <= 10).astype(int)
results_df['top_20'] = (results_df['finish_position'] <= 20).astype(int)
results_df['top_40'] = (results_df['finish_position'] <= 40).astype(int)

# Group by edge bucket and calculate probabilities
lookup = results_df.groupby('edge_bucket').agg({
    'player_id': 'count',  # sample size
    'top_5': 'sum',
    'top_10': 'sum',
    'top_20': 'sum',
    'top_40': 'sum',
}).reset_index()

lookup.columns = ['edge_bucket', 'sample_n', 'top_5_count', 'top_10_count', 'top_20_count', 'top_40_count']

# Calculate probabilities
lookup['p_top_5'] = lookup['top_5_count'] / lookup['sample_n']
lookup['p_top_10'] = lookup['top_10_count'] / lookup['sample_n']
lookup['p_top_20'] = lookup['top_20_count'] / lookup['sample_n']
lookup['p_top_40'] = lookup['top_40_count'] / lookup['sample_n']

# Sort by edge bucket
lookup = lookup.sort_values('edge_bucket').reset_index(drop=True)

print("\n=== CORRECTED TOURNAMENT PLACEMENT LOOKUP ===")
print(lookup[['edge_bucket', 'sample_n', 'p_top_5', 'p_top_10', 'p_top_20', 'p_top_40']].head(20))

# Save to CSV
lookup.to_csv('tournament_placement_lookup.csv', index=False)
print(f"\nSaved to tournament_placement_lookup.csv")

# Validate the fix: should be monotonically increasing with edge
print("\n=== VALIDATION ===")
print("P(Top 5) by edge (should increase with edge):")
print(lookup[['edge_bucket', 'sample_n', 'p_top_5']].iloc[::10])  # Every 10th row

# Flag any non-monotonic increases
top5_values = lookup['p_top_5'].values
violations = sum(1 for i in range(1, len(top5_values)) if top5_values[i] < top5_values[i-1])
print(f"\nMonotonicity violations (should be 0 or very few): {violations}")
