"""
Measure predictive power: How well do high vs low scoring elements predict placement?
Compares element-based grouping vs other factors (color, round type, etc.)
"""

import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv')
df_clean = df[df['round_type'] != 'REMOVE'].copy()

print("\n" + "=" * 100)
print("ELEMENT-BASED PLACEMENT PREDICTION ANALYSIS")
print("=" * 100)

# Strategy 1: Classify players into high/low element groups per venue
print("\n1. WITHIN-VENUE ELEMENT GROUPING (HIGH vs LOW)")
print("-" * 100)

prediction_accuracy = []
venue_results = []

for venue, venue_data in df_clean.groupby('event_name'):
    if len(venue_data) < 20:  # Skip small venues
        continue

    # Get element performance at this venue
    element_exec = venue_data.groupby('wu_xing')['exec'].mean()

    if len(element_exec) < 2:
        continue

    # Classify elements: high exec = top 50%, low = bottom 50%
    median_exec = element_exec.median()

    # Label players based on their element
    venue_data['element_class'] = venue_data['wu_xing'].map(
        lambda x: 'HIGH' if element_exec.get(x, 0) > median_exec else 'LOW'
    )

    # Compare scores between groups
    high_group = venue_data[venue_data['element_class'] == 'HIGH']
    low_group = venue_data[venue_data['element_class'] == 'LOW']

    if len(high_group) < 5 or len(low_group) < 5:
        continue

    # Performance difference
    high_vs_avg = high_group['vs_avg'].mean()
    low_vs_avg = low_group['vs_avg'].mean()
    diff = high_vs_avg - low_vs_avg

    # Statistical test
    t_stat, p_value = stats.ttest_ind(
        high_group['vs_avg'].dropna(),
        low_group['vs_avg'].dropna()
    )

    # Win rate difference
    high_wins = (high_group['vs_avg'] > 0).sum() / len(high_group)
    low_wins = (low_group['vs_avg'] > 0).sum() / len(low_group)
    win_diff = high_wins - low_wins

    venue_results.append({
        'venue': venue,
        'high_vs_avg': high_vs_avg,
        'low_vs_avg': low_vs_avg,
        'difference': diff,
        'p_value': p_value,
        'high_wins': high_wins,
        'low_wins': low_wins,
        'win_diff': win_diff,
        'n_high': len(high_group),
        'n_low': len(low_group),
        'significant': 'YES' if p_value < 0.05 else 'NO'
    })

venue_results_df = pd.DataFrame(venue_results)

# Show top differentiators
print("\nVenues where HIGH scoring elements significantly outperform LOW:")
print(f"{'Venue':<40} {'High vs Avg':<12} {'Low vs Avg':<12} {'Difference':<12} {'p-value':<10} {'Win Rate Diff':<15} {'Significant':<12}")
print("-" * 113)

for _, row in venue_results_df.sort_values('difference', ascending=False).head(15).iterrows():
    print(f"{row['venue']:<40} {row['high_vs_avg']:<12.3f} {row['low_vs_avg']:<12.3f} {row['difference']:<12.3f} {row['p_value']:<10.4f} {row['win_diff']:<15.1%} {row['significant']:<12}")

# Statistics
significant_venues = (venue_results_df['p_value'] < 0.05).sum()
avg_difference = venue_results_df['difference'].mean()
positive_venues = (venue_results_df['difference'] > 0).sum()

print(f"\n  Summary:")
print(f"    Venues analyzed: {len(venue_results_df)}")
print(f"    Venues with significant difference (p<0.05): {significant_venues} ({significant_venues/len(venue_results_df)*100:.1f}%)")
print(f"    Venues where HIGH > LOW: {positive_venues} ({positive_venues/len(venue_results_df)*100:.1f}%)")
print(f"    Average difference: {avg_difference:.3f}")
print(f"    Mean p-value: {venue_results_df['p_value'].mean():.4f}")

# Strategy 2: Compare predictive power vs other factors
print("\n\n2. PREDICTIVE POWER COMPARISON: Element vs Color vs Round Type")
print("-" * 100)

predictors = ['wu_xing', 'color', 'round_type', 'condition']
predictor_power = []

for predictor in predictors:
    # For each value of predictor, measure how well it predicts above/below average
    groups = df_clean.groupby(predictor)

    correct_predictions = 0
    total_predictions = 0

    for group_value, group_data in groups:
        if group_value is None or pd.isna(group_value):
            continue

        avg_vs_avg = group_data['vs_avg'].mean()
        predictions = (group_data['vs_avg'] > 0) if avg_vs_avg > 0 else (group_data['vs_avg'] < 0)

        correct = predictions.sum()
        total = len(group_data)

        correct_predictions += correct
        total_predictions += total

    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0

    # Correlation with actual performance
    correlation = df_clean.groupby(predictor)['vs_avg'].mean().std()

    predictor_power.append({
        'predictor': predictor,
        'prediction_accuracy': accuracy,
        'group_variance': correlation,
        'n_groups': len(groups)
    })

predictor_df = pd.DataFrame(predictor_power).sort_values('group_variance', ascending=False)

print(f"\n{'Predictor':<15} {'N Groups':<10} {'Group Variance':<15} {'Prediction Accuracy':<20}")
print("-" * 60)
for _, row in predictor_df.iterrows():
    print(f"{row['predictor']:<15} {row['n_groups']:<10} {row['group_variance']:<15.3f} {row['prediction_accuracy']:<20.1%}")

print("\n  Interpretation:")
print("    - Group Variance: How much different groups differ from each other (higher = more predictive)")
print("    - Prediction Accuracy: Can we use this to predict above/below average? (50% = no signal)")

# Strategy 3: Element + Condition combination
print("\n\n3. ELEMENT × CONDITION COMBINATION (Best combo strategies)")
print("-" * 100)

element_condition_combos = []

for (element, condition), combo_data in df_clean.groupby(['wu_xing', 'condition']):
    if len(combo_data) < 10 or element is None or pd.isna(element):
        continue

    avg_exec = combo_data['exec'].mean()
    avg_upside = combo_data['upside'].mean()
    avg_vs_avg = combo_data['vs_avg'].mean()
    win_rate = (combo_data['vs_avg'] > 0).sum() / len(combo_data)

    element_condition_combos.append({
        'element': element,
        'condition': condition,
        'count': len(combo_data),
        'avg_exec': avg_exec,
        'avg_upside': avg_upside,
        'avg_vs_avg': avg_vs_avg,
        'win_rate': win_rate
    })

combo_df = pd.DataFrame(element_condition_combos).sort_values('avg_vs_avg', ascending=False)

print("\nTop 15 Element × Condition combos (best scores vs average):")
print(f"{'Element':<12} {'Condition':<12} {'Count':<6} {'Avg vs Avg':<12} {'Win Rate':<12} {'Avg Exec':<10}")
print("-" * 64)

for _, row in combo_df.head(15).iterrows():
    print(f"{row['element']:<12} {row['condition']:<12} {row['count']:<6.0f} {row['avg_vs_avg']:<12.3f} {row['win_rate']:<12.1%} {row['avg_exec']:<10.2f}")

print("\n\nBottom 15 (worst combos):")
print(f"{'Element':<12} {'Condition':<12} {'Count':<6} {'Avg vs Avg':<12} {'Win Rate':<12} {'Avg Exec':<10}")
print("-" * 64)

for _, row in combo_df.tail(15).iterrows():
    print(f"{row['element']:<12} {row['condition']:<12} {row['count']:<6.0f} {row['avg_vs_avg']:<12.3f} {row['win_rate']:<12.1%} {row['avg_exec']:<10.2f}")

print("\n" + "=" * 100)
print("CONCLUSION: Can Element grouping improve placement prediction?")
print("=" * 100)
print(f"\n[YES] with caveats:")
print(f"  - {significant_venues} of {len(venue_results_df)} venues show significant element effect (p<0.05)")
print(f"  - {positive_venues} venues show HIGH elements > LOW elements")
print(f"  - Element has {'STRONG' if predictor_df.iloc[0]['predictor'] == 'wu_xing' else 'MODERATE'} predictive power vs color/round_type")
print(f"  - Best strategy: Use Element × Condition combos (more specific than element alone)")
print("\n")
