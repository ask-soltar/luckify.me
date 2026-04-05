#!/usr/bin/env python3
"""
Score 2-ball matchups with 35/65 Exec/Upside weighting.
Then test different difference thresholds.
"""

import pandas as pd

# Load Golf Historics and matchups
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

# Score with 35/65 weighting
print("\n[SCORING] with 35% Exec / 65% Upside...\n")

exec_weight = 0.35
upside_weight = 0.65

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

    # 35/65 weighted average
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

df = pd.DataFrame(results)
graded = df[df['actual_winner'] != 'Push'].copy()

print(f"Scored: {len(df)} matchups")
print(f"Failed: {failed_count} matchups\n")

# Test different thresholds
print("="*70)
print("THRESHOLD TESTING (35% Exec / 65% Upside)")
print("="*70)

thresholds = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-" * 70)

results_by_threshold = []

for threshold in thresholds:
    filtered = graded[graded['difference'] >= threshold].copy()

    if len(filtered) > 0:
        wins = len(filtered[filtered['correct'] == True])
        win_rate = (wins / len(filtered)) * 100
        results_by_threshold.append({
            'threshold': threshold,
            'qualified': len(filtered),
            'wins': wins,
            'win_rate': win_rate
        })
        print(f"    >= {threshold:4.1f}   {len(filtered):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# Show by round type for top 3 thresholds
print(f"\n" + "="*70)
print("TOP 3 THRESHOLDS - BY ROUND TYPE")
print("="*70)

df_thresholds = pd.DataFrame(results_by_threshold).sort_values('win_rate', ascending=False)

for idx, (_, row) in enumerate(df_thresholds.head(3).iterrows(), 1):
    threshold = row['threshold']
    print(f"\n{idx}. Threshold >= {threshold} ({row['win_rate']:.1f}% win rate)")

    filtered = graded[graded['difference'] >= threshold].copy()

    for round_type in ['Open', 'Positioning', 'Closing']:
        subset = filtered[filtered['round_type'] == round_type]
        if len(subset) > 0:
            wins = len(subset[subset['correct'] == True])
            rate = (wins / len(subset)) * 100
            print(f"   {round_type:12} - Qualified: {len(subset):3.0f}, Wins: {wins:3.0f}, Win Rate: {rate:5.1f}%")

# Save scored data
df.to_csv('2ball_scored_35_65.csv', index=False)
print(f"\n[OK] Scored matchups saved to: 2ball_scored_35_65.csv")
