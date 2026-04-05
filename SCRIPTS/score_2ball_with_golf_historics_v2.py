#!/usr/bin/env python3
"""
Score 2-ball matchups using Golf Historics v3 - using Win Ratio column.
"""

import pandas as pd

# Load Golf Historics lookup table
print("[LOADING] Golf Historics v3 lookup table...")
gh = pd.read_csv('Golf Historics v3 - Manual Anlysis.csv')
print(f"  {len(gh)} rows loaded\n")

# Load matchups
print("[LOADING] matchup.csv...")
matchups = pd.read_csv('matchup.csv')
print(f"  {len(matchups)} matchups loaded\n")

# Function to bin a score into bucket
def get_bucket(score):
    if score < 25:
        return "0-25"
    elif score < 50:
        return "25-50"
    elif score < 75:
        return "50-75"
    else:
        return "75-100"

# Function to look up Win Ratio from Golf Historics
def lookup_win_ratio(color, exec_or_upside, bucket, condition, round_type, lookup_df):
    """
    Look up Win Ratio from Golf Historics table.
    Returns the Win Ratio column value (as decimal, e.g., 0.6 for 60%).
    """
    match = lookup_df[
        (lookup_df['Color'] == color) &
        (lookup_df['Exec/Upside'] == exec_or_upside) &
        (lookup_df['bucket'] == bucket) &
        (lookup_df['Course Condition'] == condition) &
        (lookup_df['Round Type'] == round_type)
    ]

    if len(match) > 0:
        ratio = match.iloc[0]['Win Ratio']
        # Convert "63.64%" string to decimal if needed
        if isinstance(ratio, str) and '%' in ratio:
            try:
                return float(ratio.strip('%')) / 100
            except:
                return None
        else:
            try:
                return float(ratio)
            except:
                return None
    else:
        return None

# Score each matchup
print("[PROCESSING] Scoring matchups...\n")

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

    # Skip if round type is #REF! or other errors
    if pd.isna(round_type) or round_type == '#REF!' or round_type == '':
        failed_count += 1
        continue

    # Bin scores
    exec_a_bucket = get_bucket(exec_a)
    upside_a_bucket = get_bucket(upside_a)
    exec_b_bucket = get_bucket(exec_b)
    upside_b_bucket = get_bucket(upside_b)

    # Look up Win Ratios
    exec_ratio_a = lookup_win_ratio(color_a, 'Exec', exec_a_bucket, condition, round_type, gh)
    upside_ratio_a = lookup_win_ratio(color_a, 'Upside', upside_a_bucket, condition, round_type, gh)

    exec_ratio_b = lookup_win_ratio(color_b, 'Exec', exec_b_bucket, condition, round_type, gh)
    upside_ratio_b = lookup_win_ratio(color_b, 'Upside', upside_b_bucket, condition, round_type, gh)

    # Skip if any lookup failed
    if exec_ratio_a is None or upside_ratio_a is None or exec_ratio_b is None or upside_ratio_b is None:
        failed_count += 1
        continue

    # Average Exec + Upside Win Ratios
    score_a = (exec_ratio_a + upside_ratio_a) / 2
    score_b = (exec_ratio_b + upside_ratio_b) / 2

    # Determine winner and loser
    winner_score = max(score_a, score_b)
    loser_score = min(score_a, score_b)

    # Determine prediction
    if score_a > score_b:
        prediction = player_a
    elif score_b > score_a:
        prediction = player_b
    else:
        prediction = "TIE"

    # Determine if prediction was correct
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
        'color_a': color_a,
        'color_b': color_b,
        'condition': condition,
        'round_type': round_type,
        'exec_ratio_a': exec_ratio_a,
        'upside_ratio_a': upside_ratio_a,
        'score_a': score_a,
        'exec_ratio_b': exec_ratio_b,
        'upside_ratio_b': upside_ratio_b,
        'score_b': score_b,
        'winner_score': winner_score,
        'loser_score': loser_score,
        'prediction': prediction,
        'actual_winner': winner,
        'correct': correct
    })

df_results = pd.DataFrame(results)

print(f"Scored: {len(df_results)} matchups")
print(f"Failed: {failed_count} matchups\n")

# Baseline (all matchups, exclude pushes)
graded_all = df_results[df_results['actual_winner'] != 'Push'].copy()
if len(graded_all) > 0:
    wins_all = len(graded_all[graded_all['correct'] == True])
    rate_all = (wins_all / len(graded_all)) * 100
    print(f"="*70)
    print(f"BASELINE (No Filters)")
    print(f"="*70)
    print(f"Matchups: {len(graded_all)}")
    print(f"Wins: {wins_all}")
    print(f"Win Rate: {rate_all:.1f}%\n")

# Apply filter: Loser < 0.5 AND Winner > 0.5
print(f"="*70)
print(f"FILTER: Loser < 0.5 AND Winner > 0.5")
print(f"="*70)

filtered = df_results[(df_results['loser_score'] < 0.5) & (df_results['winner_score'] > 0.5)].copy()
graded = filtered[filtered['actual_winner'] != 'Push'].copy()

if len(graded) > 0:
    wins = len(graded[graded['correct'] == True])
    losses = len(graded[graded['correct'] == False])
    win_rate = (wins / len(graded)) * 100

    print(f"\nQualified matchups: {len(filtered)}")
    print(f"Graded matchups: {len(graded)}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.1f}%")
else:
    print("No graded matchups with this filter")

# Save results
df_results.to_csv('2ball_scored_golf_historics_v2.csv', index=False)
print(f"\n[OK] Detailed results saved to: 2ball_scored_golf_historics_v2.csv")
