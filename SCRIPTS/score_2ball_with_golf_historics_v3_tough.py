#!/usr/bin/env python3
"""
Score 2-ball matchups using Golf Historics v3 (with Tough conditions).
Uses 35% Exec / 65% Upside weighting.
"""

import pandas as pd

# Load data
matchups = pd.read_csv('matchup.csv')
gh_v3 = pd.read_csv('Golf Historics v3 - Manual Anlysis.csv')

# Clean Golf Historics column names
gh_v3.columns = gh_v3.columns.str.strip()

# Keep only needed columns
gh_v3 = gh_v3[['Color', 'Exec/Upside', 'bucket', 'Course Condition', 'Round Type', 'Score']].copy()

# Rename for easier reference
gh_v3.columns = ['color', 'exec_upside', 'bucket', 'condition', 'round_type', 'score']

# Remove any NaN scores
gh_v3 = gh_v3[gh_v3['score'].notna()].copy()

print(f"Golf Historics v3 loaded: {len(gh_v3)} rows")
print(f"Conditions: {gh_v3['condition'].unique()}")

# Helper function to get bucket from value
def get_bucket(value):
    if value < 25:
        return '0-25'
    elif value < 50:
        return '25-50'
    elif value < 75:
        return '50-75'
    else:
        return '75-100'

# Function to lookup score
def lookup_score(color, exec_val, upside_val, condition, round_type, is_exec):
    """Lookup score in Golf Historics v3"""
    # Determine bucket
    if is_exec:
        bucket = get_bucket(exec_val)
        exec_upside_type = 'Exec'
    else:
        bucket = get_bucket(upside_val)
        exec_upside_type = 'Upside'

    # Query
    match = gh_v3[(gh_v3['color'] == color) &
                   (gh_v3['exec_upside'] == exec_upside_type) &
                   (gh_v3['bucket'] == bucket) &
                   (gh_v3['condition'] == condition) &
                   (gh_v3['round_type'] == round_type)]

    if len(match) > 0:
        return match.iloc[0]['score']
    else:
        return None

# Score each matchup
scored_rows = []

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

    # Skip if missing critical data
    if pd.isna(exec_a) or pd.isna(upside_a) or pd.isna(exec_b) or pd.isna(upside_b):
        continue
    if pd.isna(color_a) or pd.isna(color_b):
        continue

    # Lookup Exec scores
    exec_score_a = lookup_score(color_a, exec_a, upside_a, condition, round_type, True)
    exec_score_b = lookup_score(color_b, exec_b, upside_b, condition, round_type, True)

    # Lookup Upside scores
    upside_score_a = lookup_score(color_a, exec_a, upside_a, condition, round_type, False)
    upside_score_b = lookup_score(color_b, exec_b, upside_b, condition, round_type, False)

    # Skip if any score not found
    if exec_score_a is None or exec_score_b is None or upside_score_a is None or upside_score_b is None:
        continue

    # Weighted score: 35% Exec + 65% Upside
    score_a = (0.35 * exec_score_a) + (0.65 * upside_score_a)
    score_b = (0.35 * exec_score_b) + (0.65 * upside_score_b)

    # Determine winner and score difference
    if score_a > score_b:
        winner_score = score_a
        loser_score = score_b
        prediction = player_a
    else:
        winner_score = score_b
        loser_score = score_a
        prediction = player_b

    difference = winner_score - loser_score

    # Determine if correct
    if winner == 'Push':
        correct = None
    else:
        correct = (prediction == winner)

    scored_rows.append({
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

# Create dataframe
scored_df = pd.DataFrame(scored_rows)

print(f"\nScored matchups: {len(scored_df)}")
print(f"Wins: {len(scored_df[scored_df['correct']==True])}")
print(f"Losses: {len(scored_df[scored_df['correct']==False])}")

# Breakdown by condition
print(f"\nBy condition:")
for cond in ['Calm', 'Moderate', 'Tough']:
    cond_data = scored_df[scored_df['condition'] == cond]
    if len(cond_data) > 0:
        wins = len(cond_data[cond_data['correct']==True])
        losses = len(cond_data[cond_data['correct']==False])
        rate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0
        print(f"  {cond}: {wins}/{wins+losses} = {rate:.1f}%")

# Save
scored_df.to_csv('2ball_scored_35_65_with_tough.csv', index=False)
print(f"\nSaved to: 2ball_scored_35_65_with_tough.csv")

EOF
