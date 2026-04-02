"""
For each venue/tournament, measure how well each element type performs
relative to scorer predictions. Shows which elements have highest predictive value.
"""

import pandas as pd
import numpy as np

# Load rescored data
df = pd.read_csv('ANALYSIS_v3_RESCORED.csv', low_memory=False)

# Remove REMOVE rounds and rows without scorer data
df_clean = df[(df['round_type'] != 'REMOVE') & (df['predicted_score'].notna())].copy()

print("=" * 120)
print("ELEMENT CONSISTENCY ANALYSIS BY VENUE")
print("Measuring how well each element performs relative to scorer predictions")
print("=" * 120)

print(f"\nTotal rounds analyzed: {len(df_clean)}")
print(f"Venues: {df_clean['event_name'].nunique()}")
print(f"Elements: {df_clean['wu_xing'].dropna().unique()}")

# Store results for summary
venue_element_results = []

# Analyze each venue
for venue in sorted(df_clean['event_name'].unique()):
    venue_data = df_clean[df_clean['event_name'] == venue].copy()

    if len(venue_data) < 50:  # Skip small venues
        continue

    print(f"\n{'=' * 120}")
    print(f"VENUE: {venue}")
    print(f"Total rounds: {len(venue_data)}")

    # For each element type
    element_scores = []

    for element in venue_data['wu_xing'].dropna().unique():
        element_data = venue_data[venue_data['wu_xing'] == element].copy()

        if len(element_data) < 5:
            continue

        # Key metric: how well does scorer predict this element?
        # Lower error = more predictable = higher predictive value

        prediction_error = (element_data['score_difference'].abs()).mean()
        rmse = np.sqrt((element_data['score_difference'] ** 2).mean())

        # How much does this element beat/miss expectations?
        mean_error = element_data['score_difference'].mean()  # Signed error

        # Consistency: std dev of prediction errors (lower = more consistent)
        consistency = element_data['score_difference'].std()

        # Actual win rate vs predicted win rate
        actual_win_rate = element_data['actual_win'].mean()

        # Group by exec bucket to see consistency across score levels
        bucket_stats = []
        for bucket in sorted(element_data['exec_bucket'].dropna().unique()):
            bucket_data = element_data[element_data['exec_bucket'] == bucket]
            if len(bucket_data) >= 2:
                bucket_stats.append({
                    'bucket': bucket,
                    'count': len(bucket_data),
                    'mae': (bucket_data['score_difference'].abs()).mean(),
                    'mean_error': bucket_data['score_difference'].mean(),
                    'actual_win_rate': bucket_data['actual_win'].mean()
                })

        element_scores.append({
            'venue': venue,
            'element': element,
            'count': len(element_data),
            'mae': prediction_error,
            'rmse': rmse,
            'mean_error': mean_error,
            'consistency_std': consistency,
            'actual_win_rate': actual_win_rate,
            'bucket_stats': bucket_stats
        })

        venue_element_results.append({
            'venue': venue,
            'element': element,
            'count': len(element_data),
            'mae': prediction_error,
            'rmse': rmse,
            'mean_error': mean_error,
            'consistency': consistency,
            'win_rate': actual_win_rate
        })

    # Sort by MAE (lower = more predictable)
    element_scores.sort(key=lambda x: x['mae'])

    print(f"\n  Element Performance (sorted by MAE - lower is more predictable):")
    print(f"  {'Element':<12} {'Count':<6} {'MAE':<8} {'RMSE':<8} {'Mean Error':<12} {'Consistency':<12} {'Win Rate':<10}")
    print("  " + "-" * 98)

    for stat in element_scores:
        print(f"  {stat['element']:<12} {stat['count']:<6} {stat['mae']:<8.3f} {stat['rmse']:<8.3f} {stat['mean_error']:<12.3f} {stat['consistency_std']:<12.3f} {stat['actual_win_rate']:<10.1%}")

    # Detailed breakdown for best and worst elements
    if len(element_scores) >= 2:
        best = element_scores[0]
        worst = element_scores[-1]

        print(f"\n  BEST ELEMENT (Most Predictable): {best['element']}")
        print(f"    MAE: {best['mae']:.3f} (predictions within {best['mae']:.2f} strokes on average)")
        print(f"    Consistency: {best['consistency_std']:.3f} (std dev of errors)")
        print(f"    Bucket breakdown:")
        for bucket_stat in best['bucket_stats']:
            print(f"      {bucket_stat['bucket']}: n={bucket_stat['count']}, MAE={bucket_stat['mae']:.3f}, Win Rate={bucket_stat['actual_win_rate']:.1%}")

        print(f"\n  WORST ELEMENT (Least Predictable): {worst['element']}")
        print(f"    MAE: {worst['mae']:.3f}")
        print(f"    Consistency: {worst['consistency_std']:.3f}")
        print(f"    Bucket breakdown:")
        for bucket_stat in worst['bucket_stats']:
            print(f"      {bucket_stat['bucket']}: n={bucket_stat['count']}, MAE={bucket_stat['mae']:.3f}, Win Rate={bucket_stat['actual_win_rate']:.1%}")

        print(f"\n  Predictability Gap (Best vs Worst):")
        print(f"    MAE Difference: {worst['mae'] - best['mae']:.3f} ({(worst['mae']/best['mae'] - 1)*100:.1f}% worse)")
        print(f"    Consistency Difference: {worst['consistency_std'] - best['consistency_std']:.3f}")

# Summary: Which elements are most predictable across ALL venues?
print(f"\n\n{'=' * 120}")
print("SUMMARY: ELEMENT PREDICTABILITY ACROSS ALL VENUES")
print("=" * 120)

summary_df = pd.DataFrame(venue_element_results)
overall = summary_df.groupby('element').agg({
    'count': 'sum',
    'mae': 'mean',
    'rmse': 'mean',
    'mean_error': 'mean',
    'consistency': 'mean',
    'win_rate': 'mean'
}).sort_values('mae')

print(f"\n  {'Element':<12} {'Total Rounds':<15} {'Avg MAE':<10} {'Avg RMSE':<10} {'Mean Error':<12} {'Avg Consistency':<15} {'Avg Win Rate':<12}")
print("  " + "-" * 96)

for element, row in overall.iterrows():
    print(f"  {element:<12} {row['count']:<15.0f} {row['mae']:<10.3f} {row['rmse']:<10.3f} {row['mean_error']:<12.3f} {row['consistency']:<15.3f} {row['win_rate']:<12.1%}")

print(f"\n  Interpretation:")
print(f"    MAE = Mean Absolute Error (how far off predictions are)")
print(f"    Lower MAE = Scorer predictions more accurate for this element")
print(f"    Higher MAE = Element performance unpredictable by your scorer (element has hidden signal)")

# Variance across venues
print(f"\n  Venue-to-Venue Variance (how stable is each element across tournaments?):")
print(f"  {'Element':<12} {'MAE Std Dev':<15} {'Venues':<10} {'Consistency Ranking':<20}")
print("  " + "-" * 57)

for element in overall.index:
    element_venues = summary_df[summary_df['element'] == element]
    mae_stddev = element_venues['mae'].std()
    n_venues = len(element_venues)

    print(f"  {element:<12} {mae_stddev:<15.3f} {n_venues:<10} {'Low variance = stable' if mae_stddev < 1.0 else 'High variance = venue-dependent':<20}")

print("\n")
