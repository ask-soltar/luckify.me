"""
Validation: System 1 Only (Color × Element)
Compares System 1-only screener picks to actual results
"""

import pandas as pd
import sys

# Load signal database
print("\nLoading signal database...")
df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')

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
color_a_col = find_col(df_matchups, 'color', '[a]')
color_b_col = find_col(df_matchups, 'color', '[b]')
element_a_col = find_col(df_matchups, 'element', '[a]')
element_b_col = find_col(df_matchups, 'element', '[b]')
winner_col = find_col(df_matchups, 'winner')

if not winner_col:
    print("ERROR: Could not find 'Winner' column")
    exit(1)

print(f"Found {len(df_matchups)} matchups with results")
print(f"(Moon, Horoscope columns ignored — System 1 only)\n")

# Score each matchup and compare to actual
results = []

for idx, row in df_matchups.iterrows():
    player_a = str(row[player_a_col]).strip()
    player_b = str(row[player_b_col]).strip()
    condition = str(row[condition_col]).strip()
    round_type = str(row[round_type_col]).strip()
    color_a = str(row[color_a_col]).strip()
    color_b = str(row[color_b_col]).strip()
    element_a = str(row[element_a_col]).strip()
    element_b = str(row[element_b_col]).strip()
    winner = str(row[winner_col]).strip()

    # System 1: Color × Element
    s1_a = df_s1[
        (df_s1['condition'] == condition) &
        (df_s1['round_type'] == round_type) &
        (df_s1['color'] == color_a) &
        (df_s1['element'] == element_a)
    ]
    s1_a_roi = s1_a['adjusted_roi'].values[0] if len(s1_a) > 0 else 0.0

    s1_b = df_s1[
        (df_s1['condition'] == condition) &
        (df_s1['round_type'] == round_type) &
        (df_s1['color'] == color_b) &
        (df_s1['element'] == element_b)
    ]
    s1_b_roi = s1_b['adjusted_roi'].values[0] if len(s1_b) > 0 else 0.0

    # Total scores (System 1 only)
    score_a = s1_a_roi
    score_b = s1_b_roi
    gap = score_a - score_b

    # Prediction (adjusted thresholds for single system)
    if gap > 6:
        prediction = player_a
    elif gap < -6:
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
print("VALIDATION: SYSTEM 1 ONLY (Color × Element)")
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
    print(f"\nExpected win rate (50-55%): TARGET")
    print(f"Actual win rate: {win_pct:.1f}%")
    if win_pct >= 55:
        print(f"Status: VALIDATING — on track to beat baseline")
    elif win_pct >= 50:
        print(f"Status: UNCERTAIN — at 50/50 threshold, need more data")
    else:
        print(f"Status: UNDERPERFORMING — track live performance before scaling")

# Breakdown by signal strength
print(f"\n\nBy Signal Strength:")
print("-"*60)

for threshold in [10, 6]:
    strong = df_graded[df_graded['gap'].abs() >= threshold]
    if len(strong) > 0:
        strong_wins = len(strong[strong['correct'] == True])
        strong_pct = strong_wins / len(strong) * 100
        print(f"  Gap >= {threshold}%: {strong_wins}/{len(strong)} ({strong_pct:.1f}%)")

# Pushes and skips
pushes = len(df_results[df_results['result'] == 'PUSH'])
skips = len(df_results[df_results['result'] == 'SKIP'])
print(f"\nPushes: {pushes}")
print(f"Skipped (gap < 6%): {skips}")

# Save detailed results
output_file = matchup_file.replace('.csv', '_validated_s1.csv')
df_results.to_csv(output_file, index=False)
print(f"\n[OK] Validation results saved to: {output_file}")

print("\n[OK] Validation complete!")
