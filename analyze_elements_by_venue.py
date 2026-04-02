"""
Analyze Wu Xing element performance by venue.
Groups tournaments, shows which elements score high vs low at each venue.
"""

import pandas as pd
import numpy as np
from collections import defaultdict

# Load the ANALYSIS data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv')

print("=" * 100)
print("ELEMENT ANALYSIS BY VENUE")
print("=" * 100)
print(f"\nTotal rounds: {len(df)}")
print(f"Unique venues: {df['event_name'].nunique()}")
print(f"Unique players: {df['player_name'].nunique()}")
print(f"Element types: {df['wu_xing'].unique()}")

# Remove REMOVE rounds
df_clean = df[df['round_type'] != 'REMOVE'].copy()
print(f"Rounds after removing REMOVE: {len(df_clean)}")

# Group by venue and element type
venue_element_stats = []

for venue, venue_data in df_clean.groupby('event_name'):
    print(f"\n{'=' * 100}")
    print(f"VENUE: {venue}")
    print(f"Total rounds: {len(venue_data)}")

    # Stats per element
    element_stats = []

    for element, element_data in venue_data.groupby('wu_xing'):
        count = len(element_data)
        avg_exec = element_data['exec'].mean()
        avg_upside = element_data['upside'].mean()
        avg_score = element_data['score'].mean()
        avg_vs_avg = element_data['vs_avg'].mean()

        # Win rate (score better than course average)
        wins = (element_data['vs_avg'] > 0).sum()
        win_rate = wins / count if count > 0 else 0

        element_stats.append({
            'venue': venue,
            'element': element,
            'count': count,
            'avg_exec': avg_exec,
            'avg_upside': avg_upside,
            'avg_score': avg_score,
            'avg_vs_avg': avg_vs_avg,
            'win_rate': win_rate,
            'wins': wins
        })

    # Sort by exec (highest to lowest)
    element_stats.sort(key=lambda x: x['avg_exec'], reverse=True)

    print("\n  Element Performance (sorted by Exec):")
    print(f"  {'Element':<12} {'Count':<6} {'Avg Exec':<10} {'Avg Upside':<10} {'Avg Score':<10} {'vs Avg':<10} {'Win Rate':<10}")
    print("  " + "-" * 86)

    for stat in element_stats:
        print(f"  {stat['element']:<12} {stat['count']:<6} {stat['avg_exec']:<10.2f} {stat['avg_upside']:<10.2f} {stat['avg_score']:<10.2f} {stat['avg_vs_avg']:<10.2f} {stat['win_rate']:<10.1%}")

    # High vs Low scoring
    if len(element_stats) >= 2:
        high = element_stats[0]
        low = element_stats[-1]

        exec_diff = high['avg_exec'] - low['avg_exec']
        upside_diff = high['avg_upside'] - low['avg_upside']
        vs_avg_diff = high['avg_vs_avg'] - low['avg_vs_avg']
        win_diff = high['win_rate'] - low['win_rate']

        print(f"\n  HIGH vs LOW:")
        print(f"    High: {high['element']} (Exec={high['avg_exec']:.2f}, Upside={high['avg_upside']:.2f})")
        print(f"    Low:  {low['element']} (Exec={low['avg_exec']:.2f}, Upside={low['avg_upside']:.2f})")
        print(f"    Differences:")
        print(f"      Exec:    {exec_diff:+.2f} ({exec_diff/low['avg_exec']*100:+.1f}%)")
        print(f"      Upside:  {upside_diff:+.2f} ({upside_diff/low['avg_upside']*100:+.1f}%)")
        print(f"      vs Avg:  {vs_avg_diff:+.2f}")
        print(f"      Win Rate: {win_diff:+.1%}")

    venue_element_stats.extend(element_stats)

# Summary table: Best/worst elements overall
print(f"\n{'=' * 100}")
print("SUMMARY: ELEMENT PERFORMANCE ACROSS ALL VENUES")
print(f"{'=' * 100}")

summary = pd.DataFrame(venue_element_stats)
overall = summary.groupby('element').agg({
    'count': 'sum',
    'avg_exec': 'mean',
    'avg_upside': 'mean',
    'avg_score': 'mean',
    'avg_vs_avg': 'mean',
    'win_rate': 'mean',
    'wins': 'sum'
}).sort_values('avg_exec', ascending=False)

print("\n  Aggregate Element Performance:")
print(f"  {'Element':<12} {'Total Rounds':<15} {'Avg Exec':<10} {'Avg Upside':<10} {'Avg vs Avg':<12} {'Avg Win Rate':<12}")
print("  " + "-" * 79)

for element, row in overall.iterrows():
    print(f"  {element:<12} {row['count']:<15.0f} {row['avg_exec']:<10.2f} {row['avg_upside']:<10.2f} {row['avg_vs_avg']:<12.2f} {row['win_rate']:<12.1%}")

# Variance analysis: How much do elements differ by venue?
print(f"\n{'=' * 100}")
print("VARIANCE ANALYSIS: ELEMENT CONSISTENCY ACROSS VENUES")
print(f"{'=' * 100}")
print("\nHow much does each element's performance vary by venue?")
print(f"  {'Element':<12} {'Venues':<8} {'Exec Std Dev':<15} {'Exec Min-Max':<25}")
print("  " + "-" * 60)

for element in df_clean['wu_xing'].unique():
    element_venues = summary[summary['element'] == element]
    exec_std = element_venues['avg_exec'].std()
    exec_min = element_venues['avg_exec'].min()
    exec_max = element_venues['avg_exec'].max()

    print(f"  {element:<12} {len(element_venues):<8} {exec_std:<15.2f} {exec_min:.1f} - {exec_max:.1f}")

print("\n✓ Analysis complete. Save this for venue-specific element strategies.\n")
