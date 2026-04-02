"""
Validation: Exec + Upside + Color Model
Compares screener picks to actual results
"""

import pandas as pd
import sys

# Load ROI tables
print("\nLoading ROI tables...")
df_exec = pd.read_csv('color_exec_bucket_roi.csv')
df_upside = pd.read_csv('color_upside_bucket_roi.csv')

# Load matchup CSV with results
if len(sys.argv) < 2:
    matchup_file = 'matchups.csv'
else:
    matchup_file = sys.argv[1]

try:
    df_matchups = pd.read_csv(matchup_file)
    print(f"Loaded: {matchup_file}")
except FileNotFoundError:
    print(f"ERROR: {matchup_file} not found")
    exit(1)

# Normalize column names
df_matchups.columns = df_matchups.columns.str.strip()

# Find columns
def find_col(df, *keywords):
    for col in df.columns:
        col_lower = col.lower()
        if all(kw.lower() in col_lower for kw in keywords):
            return col
    return None

player_a_col = find_col(df_matchups, 'player', 'a')
player_b_col = find_col(df_matchups, 'player', 'b')
condition_col = find_col(df_matchups, 'condition')
round_type_col = find_col(df_matchups, 'round', 'type')
color_a_col = find_col(df_matchups, 'color', 'a')
color_b_col = find_col(df_matchups, 'color', 'b')
exec_a_col = find_col(df_matchups, 'exec', 'a')
exec_b_col = find_col(df_matchups, 'exec', 'b')
upside_a_col = find_col(df_matchups, 'upside', 'a')
upside_b_col = find_col(df_matchups, 'upside', 'b')
winner_col = find_col(df_matchups, 'winner')

if not winner_col:
    print("ERROR: Could not find 'Winner' column")
    exit(1)

print(f"Found {len(df_matchups)} matchups with results\n")

# Bucket function
def bucket_score(score):
    try:
        score = float(score)
        if score < 25:
            return "0-25"
        elif score < 50:
            return "25-50"
        elif score < 75:
            return "50-75"
        else:
            return "75-100"
    except:
        return None

# Lookup ROI
def get_exec_roi(condition, round_type, color, exec_bucket):
    match = df_exec[
        (df_exec['condition'] == condition) &
        (df_exec['round_type'] == round_type) &
        (df_exec['color'] == color) &
        (df_exec['exec_bucket'] == exec_bucket)
    ]
    return match['roi'].values[0] if len(match) > 0 else 0.0

def get_upside_roi(condition, round_type, color, upside_bucket):
    match = df_upside[
        (df_upside['condition'] == condition) &
        (df_upside['round_type'] == round_type) &
        (df_upside['color'] == color) &
        (df_upside['upside_bucket'] == upside_bucket)
    ]
    return match['roi'].values[0] if len(match) > 0 else 0.0

# Score each matchup and compare to actual
results = []

for idx, row in df_matchups.iterrows():
    player_a = str(row[player_a_col]).strip()
    player_b = str(row[player_b_col]).strip()
    condition = str(row[condition_col]).strip()
    round_type = str(row[round_type_col]).strip()
    color_a = str(row[color_a_col]).strip()
    color_b = str(row[color_b_col]).strip()

    exec_a_bucket = bucket_score(row[exec_a_col])
    exec_b_bucket = bucket_score(row[exec_b_col])
    upside_a_bucket = bucket_score(row[upside_a_col])
    upside_b_bucket = bucket_score(row[upside_b_col])

    winner = str(row[winner_col]).strip()

    # Get ROIs
    exec_a_roi = get_exec_roi(condition, round_type, color_a, exec_a_bucket)
    exec_b_roi = get_exec_roi(condition, round_type, color_b, exec_b_bucket)
    upside_a_roi = get_upside_roi(condition, round_type, color_a, upside_a_bucket)
    upside_b_roi = get_upside_roi(condition, round_type, color_b, upside_b_bucket)

    # Average
    score_a = (exec_a_roi + upside_a_roi) / 2.0
    score_b = (exec_b_roi + upside_b_roi) / 2.0
    gap = score_a - score_b

    # Prediction
    if gap > 8:
        prediction = player_a
    elif gap < -8:
        prediction = player_b
    else:
        prediction = "SKIP"

    # Result
    if winner.lower() == "push":
        result = "PUSH"
        correct = None
    elif prediction == "SKIP":
        result = "SKIP"
        correct = None
    elif winner == prediction:
        result = "WIN"
        correct = True
    else:
        result = "LOSS"
        correct = False

    results.append({
        'player_a': player_a,
        'player_b': player_b,
        'condition': condition,
        'round_type': round_type,
        'prediction': prediction,
        'actual_winner': winner,
        'gap': gap,
        'score_a': score_a,
        'score_b': score_b,
        'result': result,
        'correct': correct
    })

df_results = pd.DataFrame(results)

# Analysis
print("="*140)
print("VALIDATION: EXEC + UPSIDE + COLOR MODEL")
print("="*140 + "\n")

# Print all predictions vs results
print(f"{'Prediction':<20} {'Winner':<20} {'Gap':>7} {'Result':<10} {'Matchup':<50}")
print("-"*140)

for _, row in df_results.iterrows():
    matchup = f"{row['player_a']} vs {row['player_b']}"
    sign = "+" if row['gap'] > 0 else ""
    print(f"{row['prediction']:<20} {row['actual_winner']:<20} {sign}{row['gap']:>6.1f}% {row['result']:<10} {matchup:<50}")

# Summary stats
print("\n" + "="*140)
print("SUMMARY STATISTICS")
print("="*140 + "\n")

# Filter out pushes and skips for accuracy calculation
df_graded = df_results[df_results['result'] != 'PUSH']
df_graded = df_graded[df_graded['result'] != 'SKIP']

if len(df_graded) > 0:
    wins = len(df_graded[df_graded['correct'] == True])
    losses = len(df_graded[df_graded['correct'] == False])
    win_pct = wins / len(df_graded) * 100 if len(df_graded) > 0 else 0

    print(f"Graded matchups: {len(df_graded)}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win rate: {win_pct:.1f}%")
    print(f"\nExpected win rate (55%+): TARGET")
    print(f"Actual win rate: {win_pct:.1f}%")
    if win_pct >= 55:
        print(f"Status: ✓ VALIDATING — on track!")
    elif win_pct >= 50:
        print(f"Status: ⚠ UNCERTAIN — at 50% threshold, need more data")
    else:
        print(f"Status: ✗ UNDERPERFORMING — below 50%")

# Breakdown by signal strength
print(f"\n\nBy Signal Strength:")
print("-"*60)

for threshold in [15, 8]:
    strong = df_graded[df_graded['gap'].abs() >= threshold]
    if len(strong) > 0:
        strong_wins = len(strong[strong['correct'] == True])
        strong_pct = strong_wins / len(strong) * 100
        print(f"  Gap >= {threshold}%: {strong_wins}/{len(strong)} ({strong_pct:.1f}%)")

# Pushes and skips
pushes = len(df_results[df_results['result'] == 'PUSH'])
skips = len(df_results[df_results['result'] == 'SKIP'])
print(f"\nPushes: {pushes}")
print(f"Skipped (gap < 8%): {skips}")

# Save detailed results
output_file = matchup_file.replace('.csv', '_validated_exec_upside.csv')
df_results.to_csv(output_file, index=False)
print(f"\n[OK] Validation results saved to: {output_file}")

print("\n[OK] Validation complete!")
