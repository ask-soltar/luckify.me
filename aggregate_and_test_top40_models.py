"""
Test multiple 4-day aggregation methods for Top 40 prediction.
Find the method that best predicts tournament finish position.
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load original ANALYSIS data (one row per round)
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Clean: remove REMOVE rounds
df_clean = df[df['round_type'] != 'REMOVE'].copy()

print("=" * 130)
print("TESTING 4-DAY AGGREGATION METHODS FOR TOP 40 PREDICTION")
print("=" * 130)

print(f"\nTotal rounds: {len(df_clean)}")
print(f"Venues: {df_clean['event_name'].nunique()}")

# Aggregate by player + event
# Each player at each venue gets aggregated scores
print(f"\nAggregating by player + venue...")

aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': ['mean', 'sum', 'max', 'min', 'std'],
    'upside': ['mean', 'sum', 'max', 'min', 'std'],
    'vs_avg': ['mean', 'sum'],
    'score': ['sum'],
    'par': ['sum'],
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'condition': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'round_type': 'count'
}).reset_index()

aggregated.columns = ['venue', 'player', 'exec_mean', 'exec_sum', 'exec_max', 'exec_min', 'exec_std',
                      'upside_mean', 'upside_sum', 'upside_max', 'upside_min', 'upside_std',
                      'vs_avg_mean', 'vs_avg_sum', 'score_total', 'par_total', 'element', 'color', 'condition', 'n_rounds']

aggregated['off_par'] = aggregated['score_total'] - aggregated['par_total']

print(f"Aggregated to: {len(aggregated)} player-tournament combinations")

# Test different aggregation models
models = {}

# Model 1: Simple average exec/upside
aggregated['model_1_score'] = (aggregated['exec_mean'] + aggregated['upside_mean']) / 2
models['Model 1: Avg Exec + Avg Upside'] = 'model_1_score'

# Model 2: Sum exec/upside
aggregated['model_2_score'] = aggregated['exec_sum'] + aggregated['upside_sum']
models['Model 2: Sum Exec + Sum Upside'] = 'model_2_score'

# Model 3: Weighted sum (closing rounds weight 1.5x)
# Approximation: use sum + 0.5*(sum) = 1.5x
aggregated['model_3_score'] = aggregated['exec_sum'] + aggregated['upside_sum'] + 0.5 * (aggregated['exec_sum'] + aggregated['upside_sum'])
models['Model 3: Weighted Sum (1.5x)'] = 'model_3_score'

# Model 4: Best round (peak performance)
aggregated['model_4_score'] = aggregated['exec_max'] + aggregated['upside_max']
models['Model 4: Max Exec + Max Upside'] = 'model_4_score'

# Model 5: vs_avg (actual performance)
aggregated['model_5_score'] = aggregated['vs_avg_sum']
models['Model 5: Sum vs_avg (Actual)'] = 'model_5_score'

# Model 6: Off par (ultimate truth)
aggregated['model_6_score'] = -aggregated['off_par']  # Negative so lower par = higher score
models['Model 6: Off Par (Actual Finish)'] = 'model_6_score'

# Model 7: Consistency (penalize variance)
aggregated['model_7_score'] = aggregated['exec_sum'] + aggregated['upside_sum'] - (aggregated['exec_std'] + aggregated['upside_std']) * 2
models['Model 7: Sum - Variance Penalty'] = 'model_7_score'

# Model 8: Compound (sum * consistency bonus)
aggregated['consistency_bonus'] = 1 - (aggregated['exec_std'] + aggregated['upside_std']) / 100
aggregated['consistency_bonus'] = aggregated['consistency_bonus'].clip(0.5, 1.5)
aggregated['model_8_score'] = (aggregated['exec_sum'] + aggregated['upside_sum']) * aggregated['consistency_bonus']
models['Model 8: Sum × Consistency'] = 'model_8_score'

print(f"\n{'=' * 130}")
print("TESTING ACCURACY OF EACH MODEL")
print("=" * 130)

model_results = []

for model_name, model_col in models.items():
    accuracy_by_venue = []

    for venue in aggregated['venue'].unique():
        venue_data = aggregated[aggregated['venue'] == venue].copy()

        if len(venue_data) < 20:
            continue

        # Rank by model score
        venue_data['rank'] = venue_data[model_col].rank(ascending=False)

        # Top 40 cutoff
        field_size = len(venue_data)
        top40_cutoff = max(10, int(field_size * 0.33))

        # Actual top 40: beat field average (vs_avg_mean > 0)
        venue_data['actual_top_performer'] = venue_data['vs_avg_mean'] > 0

        # Predicted top 40
        venue_data['predicted_top40'] = venue_data['rank'] <= top40_cutoff

        # Accuracy
        if len(venue_data[venue_data['predicted_top40']]) > 0:
            accuracy = (venue_data[venue_data['predicted_top40']]['actual_top_performer'].sum() /
                       len(venue_data[venue_data['predicted_top40']]))
            accuracy_by_venue.append(accuracy)

    if accuracy_by_venue:
        avg_accuracy = np.mean(accuracy_by_venue)
        model_results.append({
            'model': model_name,
            'avg_accuracy': avg_accuracy,
            'std_accuracy': np.std(accuracy_by_venue),
            'n_venues': len(accuracy_by_venue)
        })

results_df = pd.DataFrame(model_results).sort_values('avg_accuracy', ascending=False)

print(f"\n{'Model':<50} {'Accuracy':<12} {'Std Dev':<12} {'Venues':<8}")
print("-" * 82)

for _, row in results_df.iterrows():
    print(f"{row['model']:<50} {row['avg_accuracy']:<12.1%} {row['std_accuracy']:<12.1%} {row['n_venues']:<8.0f}")

# Use best model for detailed analysis
best_model_name = results_df.iloc[0]['model']
best_model_col = models[best_model_name]

print(f"\n{'=' * 130}")
print(f"BEST MODEL: {best_model_name}")
print(f"Average Accuracy: {results_df.iloc[0]['avg_accuracy']:.1%}")
print("=" * 130)

# Now analyze Fire elements with best model
print(f"\nAnalyzing high-scoring Fire elements with {best_model_name}...\n")

fire_players = aggregated[aggregated['element'] == 'Fire'].copy()

if len(fire_players) > 0:
    print(f"Fire player tournaments: {len(fire_players)}")
    print(f"Exec sum range: {fire_players['exec_sum'].min():.1f} - {fire_players['exec_sum'].max():.1f}")
    print(f"Upside sum range: {fire_players['upside_sum'].min():.1f} - {fire_players['upside_sum'].max():.1f}")

    # Find optimal threshold using best model
    percentiles = [50, 60, 70, 75, 80, 85, 90]
    threshold_results = []

    for percentile in percentiles:
        exec_threshold = fire_players['exec_sum'].quantile(percentile / 100)
        upside_threshold = fire_players['upside_sum'].quantile(percentile / 100)

        high_fire = fire_players[
            (fire_players['exec_sum'] >= exec_threshold) &
            (fire_players['upside_sum'] >= upside_threshold)
        ]

        if len(high_fire) >= 10:
            # Check top 40 accuracy for this threshold
            venue_accuracy = []

            for venue in high_fire['venue'].unique():
                venue_all = aggregated[aggregated['venue'] == venue]
                venue_high_fire = high_fire[high_fire['venue'] == venue]

                if len(venue_all) < 20 or len(venue_high_fire) == 0:
                    continue

                venue_all_ranked = venue_all.copy()
                venue_all_ranked['rank'] = venue_all_ranked[best_model_col].rank(ascending=False)

                field_size = len(venue_all_ranked)
                top40_cutoff = max(10, int(field_size * 0.33))

                high_fire_ranked = venue_all_ranked[venue_all_ranked['player'].isin(venue_high_fire['player'])]

                if len(high_fire_ranked) > 0:
                    in_top40 = (high_fire_ranked['rank'] <= top40_cutoff).sum()
                    accuracy = in_top40 / len(high_fire_ranked)
                    venue_accuracy.append(accuracy)

            if venue_accuracy:
                avg_accuracy = np.mean(venue_accuracy)
                threshold_results.append({
                    'percentile': percentile,
                    'exec_threshold': exec_threshold,
                    'upside_threshold': upside_threshold,
                    'count': len(high_fire),
                    'accuracy': avg_accuracy
                })

    threshold_df = pd.DataFrame(threshold_results).sort_values('accuracy', ascending=False)

    print(f"\n{'Percentile':<12} {'Exec >= ?':<12} {'Upside >= ?':<14} {'Count':<8} {'Top 40 Accuracy':<18}")
    print("-" * 64)

    for _, row in threshold_df.head(10).iterrows():
        print(f"{row['percentile']:<12.0f} {row['exec_threshold']:<12.1f} {row['upside_threshold']:<14.1f} {row['count']:<8.0f} {row['accuracy']:<18.1%}")

    if len(threshold_df) > 0:
        best_threshold = threshold_df.iloc[0]
        print(f"\nRECOMMENDED FIRE THRESHOLD (using {best_model_name}):")
        print(f"  Exec Sum >= {best_threshold['exec_threshold']:.1f}")
        print(f"  Upside Sum >= {best_threshold['upside_threshold']:.1f}")
        print(f"  Prediction: {best_threshold['accuracy']:.1%} finish top 40")
        print(f"  Sample size: {best_threshold['count']:.0f} player-tournaments")

print("\n")
