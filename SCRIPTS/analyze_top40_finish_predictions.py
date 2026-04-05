"""
Analyze Top 40 finish position predictions using scoring system.
For each venue, rank players by predicted score, measure if higher-ranked players finish top 40.
"""

import pandas as pd
import numpy as np

# Load rescored data
df = pd.read_csv('ANALYSIS_v3_RESCORED.csv', low_memory=False)

# Clean: remove REMOVE rounds, missing scorer data
df_clean = df[(df['round_type'] != 'REMOVE') & (df['predicted_score'].notna())].copy()

print("=" * 120)
print("TOP 40 FINISH POSITION ANALYSIS")
print("Predicting which players finish top 40 using scoring system")
print("=" * 120)

print(f"\nTotal rounds: {len(df_clean)}")
print(f"Venues: {df_clean['event_name'].nunique()}")

# For each venue, analyze field
venue_results = []

for venue in sorted(df_clean['event_name'].unique()):
    venue_data = df_clean[df_clean['event_name'] == venue].copy()

    # Get unique players at this venue
    players_at_venue = venue_data.groupby('player_name').agg({
        'predicted_score': 'mean',  # Average predicted score across rounds
        'actual_win': 'mean',        # Actual win rate
        'score_difference': 'mean',  # How much they beat/miss scorer
        'vs_avg': 'mean',            # Actual vs course average
        'exec': 'mean',
        'upside': 'mean',
        'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Most common color
        'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Most common element
        'condition': 'count'  # Count of rounds = proxy for field position
    }).reset_index()

    if len(players_at_venue) < 30:  # Skip small fields
        continue

    players_at_venue.columns = ['player_name', 'avg_predicted_score', 'actual_win_rate',
                                 'avg_score_diff', 'avg_vs_avg', 'avg_exec', 'avg_upside',
                                 'primary_color', 'primary_element', 'n_rounds']

    # Rank by predicted score (highest = best)
    players_at_venue['rank'] = players_at_venue['avg_predicted_score'].rank(ascending=False, method='average')

    # Approximate top 40: if field > 120 players, top 40 is top 33%. If < 120, adjust proportionally
    field_size = len(players_at_venue)
    top40_cutoff = max(10, int(field_size * 0.33))  # Top 33% or at least 10

    players_at_venue['predicted_top40'] = players_at_venue['rank'] <= top40_cutoff

    # Actual top 40: players with positive vs_avg (beat field average) = more likely to finish well
    # Better proxy: higher actual_win_rate = finishes better
    players_at_venue['actual_top_performer'] = players_at_venue['avg_vs_avg'] > 0

    # Accuracy: how many top-predicted players actually beat field average?
    top_predicted = players_at_venue[players_at_venue['predicted_top40']]

    if len(top_predicted) > 0:
        accuracy = (top_predicted['actual_top_performer'].sum() / len(top_predicted))

        venue_results.append({
            'venue': venue,
            'field_size': field_size,
            'top40_cutoff': top40_cutoff,
            'n_top_predicted': len(top_predicted),
            'n_actually_beat_avg': top_predicted['actual_top_performer'].sum(),
            'accuracy': accuracy,
            'avg_exec_top40': top_predicted['avg_exec'].mean(),
            'avg_exec_bottom': players_at_venue[~players_at_venue['predicted_top40']]['avg_exec'].mean(),
            'avg_upside_top40': top_predicted['avg_upside'].mean(),
            'avg_upside_bottom': players_at_venue[~players_at_venue['predicted_top40']]['avg_upside'].mean(),
            'color_distribution_top40': top_predicted['primary_color'].value_counts().to_dict(),
            'element_distribution_top40': top_predicted['primary_element'].value_counts().to_dict(),
        })

# Display results
results_df = pd.DataFrame(venue_results)

print(f"\n{'=' * 120}")
print(f"VENUE-BY-VENUE: Scorer Accuracy at Predicting Top 40")
print(f"{'=' * 120}\n")

print(f"{'Venue':<40} {'Field':<8} {'Top40':<7} {'Beat Avg':<10} {'Accuracy':<10} {'Exec Gap':<12}")
print("-" * 97)

for _, row in results_df.sort_values('accuracy', ascending=False).iterrows():
    exec_gap = row['avg_exec_top40'] - row['avg_exec_bottom']
    print(f"{row['venue']:<40} {row['field_size']:<8} {row['n_top_predicted']:<7} {row['n_actually_beat_avg']:<10} {row['accuracy']:<10.1%} {exec_gap:<12.1f}")

# Summary statistics
print(f"\n{'=' * 120}")
print(f"SUMMARY: Scoring System Predictiveness for Top 40")
print(f"{'=' * 120}\n")

print(f"Venues analyzed: {len(results_df)}")
print(f"Average field size: {results_df['field_size'].mean():.0f}")
print(f"Average top 40 cutoff: {results_df['top40_cutoff'].mean():.0f} players")
print(f"\nAverage Prediction Accuracy: {results_df['accuracy'].mean():.1%}")
print(f"  Median: {results_df['accuracy'].median():.1%}")
print(f"  Std Dev: {results_df['accuracy'].std():.1%}")
print(f"  Best: {results_df['accuracy'].max():.1%}")
print(f"  Worst: {results_df['accuracy'].min():.1%}")

print(f"\nExec Score Gap (Top 40 vs Bottom):")
print(f"  Average gap: {(results_df['avg_exec_top40'] - results_df['avg_exec_bottom']).mean():.1f} points")
print(f"  This suggests top 40 finishers average {(results_df['avg_exec_top40'] - results_df['avg_exec_bottom']).mean():.1f} higher exec")

print(f"\nUpside Score Gap (Top 40 vs Bottom):")
print(f"  Average gap: {(results_df['avg_upside_top40'] - results_df['avg_upside_bottom']).mean():.1f} points")

# Color analysis
print(f"\n{'=' * 120}")
print(f"COLOR PATTERNS IN TOP 40")
print(f"{'=' * 120}\n")

# Aggregate color distribution
all_top40_colors = {}
all_bottom_colors = {}

for _, row in results_df.iterrows():
    for color, count in row['color_distribution_top40'].items():
        all_top40_colors[color] = all_top40_colors.get(color, 0) + count

print(f"{'Color':<12} {'Top 40 Appearances':<20} {'%':<10}")
print("-" * 42)

total_top40 = sum(all_top40_colors.values())
for color in sorted(all_top40_colors.keys(), key=lambda c: all_top40_colors[c], reverse=True):
    pct = all_top40_colors[color] / total_top40 * 100
    print(f"{color:<12} {all_top40_colors[color]:<20} {pct:<10.1f}%")

# Element analysis
print(f"\n{'=' * 120}")
print(f"ELEMENT PATTERNS IN TOP 40")
print(f"{'=' * 120}\n")

all_top40_elements = {}
for _, row in results_df.iterrows():
    for element, count in row['element_distribution_top40'].items():
        all_top40_elements[element] = all_top40_elements.get(element, 0) + count

print(f"{'Element':<12} {'Top 40 Appearances':<20} {'%':<10}")
print("-" * 42)

total_elements = sum(all_top40_elements.values())
for element in sorted(all_top40_elements.keys(), key=lambda e: all_top40_elements[e], reverse=True):
    pct = all_top40_elements[element] / total_elements * 100
    print(f"{element:<12} {all_top40_elements[element]:<20} {pct:<10.1f}%")

# Most accurate venues (best predictors)
print(f"\n{'=' * 120}")
print(f"BEST & WORST PREDICTION VENUES")
print(f"{'=' * 120}\n")

print("TOP 10 VENUES (Highest prediction accuracy):")
print(f"{'Venue':<45} {'Accuracy':<10} {'Exec Gap':<10}")
print("-" * 65)

for _, row in results_df.nlargest(10, 'accuracy').iterrows():
    exec_gap = row['avg_exec_top40'] - row['avg_exec_bottom']
    print(f"{row['venue']:<45} {row['accuracy']:<10.1%} {exec_gap:<10.1f}")

print("\nBOTTOM 10 VENUES (Lowest prediction accuracy):")
print(f"{'Venue':<45} {'Accuracy':<10} {'Exec Gap':<10}")
print("-" * 65)

for _, row in results_df.nsmallest(10, 'accuracy').iterrows():
    exec_gap = row['avg_exec_top40'] - row['avg_exec_bottom']
    print(f"{row['venue']:<45} {row['accuracy']:<10.1%} {exec_gap:<10.1f}")

print("\n")
