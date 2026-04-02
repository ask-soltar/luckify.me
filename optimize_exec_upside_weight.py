#!/usr/bin/env python3
"""
Optimize Exec vs Upside weighting to maximize win rate with difference >= 4 filter.
"""

import pandas as pd
import numpy as np

# Load Golf Historics lookup table and matchups
print("[LOADING] Golf Historics v3 lookup table...")
gh = pd.read_csv('Golf Historics v3 - Manual Anlysis.csv')

print("[LOADING] matchup.csv...")
matchups = pd.read_csv('matchup.csv')

def get_bucket(score):
    if score < 25:
        return "0-25"
    elif score < 50:
        return "25-50"
    elif score < 75:
        return "50-75"
    else:
        return "75-100"

def lookup_score(color, exec_or_upside, bucket, condition, round_type, lookup_df):
    match = lookup_df[
        (lookup_df['Color'] == color) &
        (lookup_df['Exec/Upside'] == exec_or_upside) &
        (lookup_df['bucket'] == bucket) &
        (lookup_df['Course Condition'] == condition) &
        (lookup_df['Round Type'] == round_type)
    ]
    if len(match) > 0:
        return match.iloc[0]['Score']
    else:
        return None

# Score each matchup with variable weighting
def score_matchups(exec_weight):
    upside_weight = 1.0 - exec_weight

    results = []
    failed_count = 0

    for idx, row in matchups.iterrows():
        player_a = row['Player A']
        player_b = row['Player B']
        color_a = row['Color [A]']
        color_b = row['Color [B]']
        exec_a = row['Exec A']
        exec_b = row['Exec B']
        upside_a = row['Upside [A]']
        upside_b = row['Upside [B]']
        condition = row['Condition']
        round_type = row['Round Type']
        winner = row['Winner']

        if pd.isna(round_type) or round_type == '#REF!' or round_type == '':
            failed_count += 1
            continue

        exec_a_bucket = get_bucket(exec_a)
        upside_a_bucket = get_bucket(upside_a)
        exec_b_bucket = get_bucket(exec_b)
        upside_b_bucket = get_bucket(upside_b)

        exec_score_a = lookup_score(color_a, 'Exec', exec_a_bucket, condition, round_type, gh)
        upside_score_a = lookup_score(color_a, 'Upside', upside_a_bucket, condition, round_type, gh)
        exec_score_b = lookup_score(color_b, 'Exec', exec_b_bucket, condition, round_type, gh)
        upside_score_b = lookup_score(color_b, 'Upside', upside_b_bucket, condition, round_type, gh)

        if exec_score_a is None or upside_score_a is None or exec_score_b is None or upside_score_b is None:
            failed_count += 1
            continue

        # Weighted average
        score_a = (exec_weight * exec_score_a) + (upside_weight * upside_score_a)
        score_b = (exec_weight * exec_score_b) + (upside_weight * upside_score_b)

        winner_score = max(score_a, score_b)
        loser_score = min(score_a, score_b)
        difference = winner_score - loser_score

        if score_a > score_b:
            prediction = player_a
        elif score_b > score_a:
            prediction = player_b
        else:
            prediction = "TIE"

        if winner == "Push":
            correct = None
        elif prediction == "TIE":
            correct = None
        elif prediction == winner:
            correct = True
        else:
            correct = False

        results.append({
            'player_a': player_a,
            'player_b': player_b,
            'condition': condition,
            'round_type': round_type,
            'score_a': score_a,
            'score_b': score_b,
            'winner_score': winner_score,
            'loser_score': loser_score,
            'difference': difference,
            'prediction': prediction,
            'actual_winner': winner,
            'correct': correct
        })

    return pd.DataFrame(results)

# Test different weights
print("\n[TESTING] Exec/Upside weight combinations...\n")

results_summary = []

for exec_pct in range(0, 101, 5):
    exec_weight = exec_pct / 100.0
    upside_weight = 1.0 - exec_weight

    df = score_matchups(exec_weight)
    graded = df[df['actual_winner'] != 'Push'].copy()
    filtered = graded[graded['difference'] >= 4].copy()

    if len(filtered) > 0:
        wins = len(filtered[filtered['correct'] == True])
        win_rate = (wins / len(filtered)) * 100

        results_summary.append({
            'exec_pct': exec_pct,
            'upside_pct': 100 - exec_pct,
            'qualified': len(filtered),
            'wins': wins,
            'win_rate': win_rate
        })

df_results = pd.DataFrame(results_summary)

# Sort by win rate descending
df_results = df_results.sort_values('win_rate', ascending=False)

print("="*70)
print("OPTIMIZATION RESULTS (Difference >= 4 Filter)")
print("="*70)
print(f"\n{'Exec':>5} {'Upside':>7} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-" * 70)

for _, row in df_results.iterrows():
    print(f"{row['exec_pct']:5.0f}% {row['upside_pct']:7.0f}% {row['qualified']:10.0f} {row['wins']:6.0f} {row['win_rate']:9.1f}%")

# Show top 5
print(f"\n" + "="*70)
print("TOP 5 WEIGHTS")
print("="*70)

for i, (_, row) in enumerate(df_results.head(5).iterrows(), 1):
    print(f"\n{i}. Exec {row['exec_pct']:.0f}% / Upside {row['upside_pct']:.0f}%")
    print(f"   Qualified: {row['qualified']:.0f} | Wins: {row['wins']:.0f} | Win Rate: {row['win_rate']:.1f}%")

# Now run detailed analysis for the best weight
best_weight = df_results.iloc[0]
optimal_exec_pct = best_weight['exec_pct']
optimal_exec_weight = optimal_exec_pct / 100.0

print(f"\n" + "="*70)
print(f"DETAILED ANALYSIS: Exec {optimal_exec_pct:.0f}% / Upside {100-optimal_exec_pct:.0f}%")
print(f"="*70)

df_optimal = score_matchups(optimal_exec_weight)
graded_optimal = df_optimal[df_optimal['actual_winner'] != 'Push'].copy()
filtered_optimal = graded_optimal[graded_optimal['difference'] >= 4].copy()

print(f"\nBaseline (no filter): {len(graded_optimal)} matchups, {len(graded_optimal[graded_optimal['correct'] == True])} wins, {(len(graded_optimal[graded_optimal['correct'] == True])/len(graded_optimal)*100):.1f}%")
print(f"With difference >= 4: {len(filtered_optimal)} matchups, {len(filtered_optimal[filtered_optimal['correct'] == True])} wins, {(len(filtered_optimal[filtered_optimal['correct'] == True])/len(filtered_optimal)*100):.1f}%\n")

for round_type in ['Open', 'Positioning', 'Closing']:
    subset = filtered_optimal[filtered_optimal['round_type'] == round_type]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        rate = (wins / len(subset)) * 100
        print(f"{round_type:12} - Qualified: {len(subset):3.0f}, Wins: {wins:3.0f}, Win Rate: {rate:5.1f}%")
