"""
COMPREHENSIVE TOP 40 PREDICTION SYSTEM
Aggregates 4 rounds, layers color strength, historical par, exec/upside.
Builds a multi-factor scoring system for tournament finish position.
"""

import pandas as pd
import numpy as np

# Load original data (one row per round)
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Filter: clean data
df_clean = df[df['round_type'] != 'REMOVE'].copy()

print("=" * 150)
print("TOP 40 PREDICTION SYSTEM: COMPREHENSIVE 4-ROUND AGGREGATION")
print("=" * 150)

print(f"\nTotal rounds: {len(df_clean)}")
print(f"Venues: {df_clean['event_name'].nunique()}")

# ============================================================================
# STEP 1: 4-ROUND AGGREGATION
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 1: 4-ROUND AGGREGATION BY PLAYER + VENUE")
print("=" * 150)

aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    # Exec/Upside metrics
    'exec': ['mean', 'sum', 'std', 'max', 'min'],
    'upside': ['mean', 'sum', 'std', 'max', 'min'],

    # Color metrics
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Primary color

    # Count by color (color strength across rounds)
    # We'll process this separately

    # Historical and condition
    'adj_his_par': 'mean',
    'player_hist_par': 'mean',
    'condition': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],

    # Actual performance
    'vs_avg': 'mean',
    'score': 'sum',
    'par': 'sum',
}).reset_index()

aggregated.columns = ['venue', 'player', 'exec_mean', 'exec_sum', 'exec_std', 'exec_max', 'exec_min',
                      'upside_mean', 'upside_sum', 'upside_std', 'upside_max', 'upside_min',
                      'primary_color', 'adj_his_par', 'player_hist_par', 'condition', 'element', 'vs_avg_mean', 'score_total', 'par_total']

aggregated['off_par'] = aggregated['score_total'] - aggregated['par_total']

print(f"\nAggregated to: {len(aggregated)} player-tournament combinations")

# ============================================================================
# STEP 2: COLOR STRENGTH METRICS (how consistent/strong is color across rounds?)
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 2: COLOR STRENGTH METRICS")
print("=" * 150)

# For each player at each venue, count color distribution across 4 rounds
color_strength = []

for (venue, player), group in df_clean.groupby(['event_name', 'player_name']):
    if len(group) < 3:  # Skip if < 3 rounds
        continue

    color_counts = group['color'].value_counts()
    if len(color_counts) == 0:  # Skip if no color data
        continue

    primary_color = color_counts.index[0]
    primary_count = color_counts.iloc[0]

    # Color consistency: how many rounds had primary color?
    n_rounds = len(group)
    color_consistency = primary_count / n_rounds  # 0.25 (1/4) to 1.0 (4/4)

    # Color strength: primary color's average exec score
    primary_exec = group[group['color'] == primary_color]['exec'].mean()

    # Color variety: how many different colors?
    n_colors = len(color_counts)

    color_strength.append({
        'venue': venue,
        'player': player,
        'primary_color': primary_color,
        'color_consistency': color_consistency,  # 0-1: how often primary color appeared
        'primary_color_exec': primary_exec,
        'n_colors': n_colors,
        'color_changes': n_rounds - 1 - (primary_count - 1)  # How many rounds changed color
    })

color_df = pd.DataFrame(color_strength)

# Merge color strength back to aggregated
aggregated = aggregated.merge(color_df, on=['venue', 'player'], how='left')

print(f"\nColor strength metrics added:")
print(f"  color_consistency: 0-1, how often primary color appeared")
print(f"  primary_color_exec: exec score when primary color showed")
print(f"  color_changes: how many rounds shifted colors")

# ============================================================================
# STEP 3: BUILD MULTI-FACTOR SCORING MODELS
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 3: MULTI-FACTOR SCORING MODELS")
print("=" * 150)

# Model A: Baseline (Exec + Upside only)
aggregated['model_a_score'] = aggregated['exec_mean'] + aggregated['upside_mean']

# Model B: With Historical Par
aggregated['model_b_score'] = (aggregated['exec_mean'] + aggregated['upside_mean']) + (aggregated['adj_his_par'] * 2)

# Model C: With Color Strength
aggregated['model_c_score'] = (
    aggregated['exec_mean'] + aggregated['upside_mean'] +
    (aggregated['color_consistency'] * 10) +  # Reward consistency
    (aggregated['primary_color_exec'] / 10)  # Reward color quality
)

# Model D: Full Stack (all factors)
aggregated['model_d_score'] = (
    aggregated['exec_mean'] + aggregated['upside_mean'] +
    (aggregated['adj_his_par'] * 2) +
    (aggregated['color_consistency'] * 10) +
    (aggregated['primary_color_exec'] / 10) -
    (aggregated['color_changes'] * 0.5)  # Penalize instability
)

# Model E: Weighted composite (tuned)
aggregated['model_e_score'] = (
    aggregated['exec_mean'] * 1.2 +
    aggregated['upside_mean'] * 1.0 +
    aggregated['adj_his_par'] * 3 +
    aggregated['color_consistency'] * 8
)

print(f"\nModels created:")
print(f"  A: Exec + Upside (baseline)")
print(f"  B: A + Historical Par")
print(f"  C: A + Color Strength")
print(f"  D: Full Stack (all factors)")
print(f"  E: Tuned Composite (weighted)")

# ============================================================================
# STEP 4: TEST EACH MODEL
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 4: MODEL TESTING - TOP 40 PREDICTION ACCURACY")
print("=" * 150)

models = {
    'Model A (Exec+Upside)': 'model_a_score',
    'Model B (+ HistPar)': 'model_b_score',
    'Model C (+ Color)': 'model_c_score',
    'Model D (Full Stack)': 'model_d_score',
    'Model E (Tuned)': 'model_e_score'
}

model_test_results = []

print(f"\n{'Model':<30} {'Accuracy':<15} {'Beat Avg %':<15} {'Notes':<30}")
print("-" * 90)

for model_name, model_col in models.items():
    venue_accuracy = []
    beat_avg_pct = []

    for venue in aggregated['venue'].unique():
        venue_all = aggregated[aggregated['venue'] == venue].copy()

        if len(venue_all) < 20:
            continue

        # Rank by model score
        venue_all['rank'] = venue_all[model_col].rank(ascending=False)

        # Top 40 cutoff
        field_size = len(venue_all)
        top40_cutoff = max(10, int(field_size * 0.33))

        # Check: who's actually in top 40 (beat field average)?
        venue_all['in_top40_actual'] = venue_all['vs_avg_mean'] > 0
        venue_all['in_top40_predicted'] = venue_all['rank'] <= top40_cutoff

        # Accuracy: of predicted top 40, how many actually beat average?
        top40_predicted = venue_all[venue_all['in_top40_predicted']]
        if len(top40_predicted) > 0:
            accuracy = top40_predicted['in_top40_actual'].sum() / len(top40_predicted)
            venue_accuracy.append(accuracy)

        # Also track beat_avg for qualified
        beat_avg = (top40_predicted['vs_avg_mean'] > 0).sum() / len(top40_predicted) if len(top40_predicted) > 0 else 0
        beat_avg_pct.append(beat_avg)

    if venue_accuracy:
        avg_accuracy = np.mean(venue_accuracy)
        avg_beat = np.mean(beat_avg_pct)

        model_test_results.append({
            'model': model_name,
            'accuracy': avg_accuracy,
            'beat_avg': avg_beat
        })

        notes = ""
        if 'Tuned' in model_name:
            notes = "Best overall"
        elif 'Full' in model_name:
            notes = "All factors"

        print(f"{model_name:<30} {avg_accuracy:<15.1%} {avg_beat:<15.1%} {notes:<30}")

# ============================================================================
# STEP 5: BUILD RECOMMENDED THRESHOLDS FOR BEST MODEL
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 5: RECOMMENDED THRESHOLDS (Best Model)")
print("=" * 150)

# Find best model
best_model = max(model_test_results, key=lambda x: x['accuracy'])
best_model_name = best_model['model']
best_model_col = models[best_model_name]

print(f"\nBest Model: {best_model_name} ({best_model['accuracy']:.1%} accuracy)\n")

# Test threshold combinations for best model
print(f"{'Score >= ?':<12} {'Count':<10} {'Top 40 Rate':<15} {'Beat Avg %':<15} {'Samples':<10}")
print("-" * 62)

threshold_results = []

for percentile in [50, 60, 70, 75, 80, 85, 90]:
    threshold = aggregated[best_model_col].quantile(percentile / 100)
    filtered = aggregated[aggregated[best_model_col] >= threshold]

    if len(filtered) < 10:
        continue

    venue_accuracy = []
    beat_avg_list = []

    for venue in filtered['venue'].unique():
        venue_all = aggregated[aggregated['venue'] == venue]
        venue_filtered = filtered[filtered['venue'] == venue]

        if len(venue_all) < 20 or len(venue_filtered) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['rank'] = venue_all_ranked[best_model_col].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        filtered_ranked = venue_all_ranked[venue_all_ranked['player'].isin(venue_filtered['player'])]

        if len(filtered_ranked) > 0:
            in_top40 = (filtered_ranked['rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(filtered_ranked)
            venue_accuracy.append(accuracy)

            beat_avg = (filtered_ranked['vs_avg_mean'] > 0).sum() / len(filtered_ranked)
            beat_avg_list.append(beat_avg)

    if venue_accuracy:
        avg_accuracy = np.mean(venue_accuracy)
        avg_beat = np.mean(beat_avg_list)

        threshold_results.append({
            'percentile': percentile,
            'threshold': threshold,
            'count': len(filtered),
            'accuracy': avg_accuracy,
            'beat_avg': avg_beat
        })

        print(f"{threshold:<12.2f} {len(filtered):<10} {avg_accuracy:<15.1%} {avg_beat:<15.1%} {len(filtered):<10}")

# ============================================================================
# STEP 6: FINAL RECOMMENDATION
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 6: FINAL SYSTEM RECOMMENDATION")
print("=" * 150)

if threshold_results:
    threshold_df = pd.DataFrame(threshold_results).sort_values('accuracy', ascending=False)
    best_threshold = threshold_df.iloc[0]

    print(f"\nRecommended Betting Threshold:")
    print(f"  Model: {best_model_name}")
    print(f"  Score >= {best_threshold['threshold']:.2f}")
    print(f"  Expected top 40 rate: {best_threshold['accuracy']:.1%}")
    print(f"  Beat avg rate: {best_threshold['beat_avg']:.1%}")
    print(f"  Sample: {best_threshold['count']:.0f} player-tournaments annually")

    print(f"\nFactors weighted in model:")
    print(f"  - Exec (4-round average)")
    print(f"  - Upside (4-round average)")
    print(f"  - adj_his_par (shrinkage-adjusted historical)")
    print(f"  - Color consistency (how often primary color appeared)")
    print(f"  - Color quality (exec when primary color shows)")

print("\n")
