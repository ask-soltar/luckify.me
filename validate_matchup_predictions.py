"""
Matchup Prediction Validator
Compares screener picks to actual results
"""

import pandas as pd
import sys

# Load signal databases
print("\nLoading signal databases...")
df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')
df_s2 = pd.read_csv('system_western_moon_horoscope_ALL_combos.csv')

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
horoscope_a_col = find_col(df_matchups, 'horoscope', '[a]')
horoscope_b_col = find_col(df_matchups, 'horoscope', '[b]')
moon_col = find_col(df_matchups, 'moon')
winner_col = find_col(df_matchups, 'winner')

if not winner_col:
    print("ERROR: Could not find 'Winner' column")
    exit(1)

print(f"Found {len(df_matchups)} matchups with results\n")

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
    horoscope_a = str(row[horoscope_a_col]).strip()
    horoscope_b = str(row[horoscope_b_col]).strip()
    moon = str(row[moon_col]).strip()
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

    # System 2: Moon × Horoscope
    s2_a = df_s2[
        (df_s2['condition'] == condition) &
        (df_s2['round_type'] == round_type) &
        (df_s2['moonwest'] == moon) &
        (df_s2['horoscope'] == horoscope_a)
    ]
    s2_a_roi = s2_a['roi'].values[0] if len(s2_a) > 0 else 0.0

    s2_b = df_s2[
        (df_s2['condition'] == condition) &
        (df_s2['round_type'] == round_type) &
        (df_s2['moonwest'] == moon) &
        (df_s2['horoscope'] == horoscope_b)
    ]
    s2_b_roi = s2_b['roi'].values[0] if len(s2_b) > 0 else 0.0

    # Total scores
    score_a = s1_a_roi + s2_a_roi
    score_b = s1_b_roi + s2_b_roi
    gap = score_a - score_b

    # Prediction
    if gap > 5:
        prediction = player_a
    elif gap < -5:
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
print("PREDICTION VALIDATION RESULTS")
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
    print(f"\nExpected win rate (57-58%): REFERENCE")
    print(f"Actual win rate: {win_pct:.1f}%")
    if win_pct >= 55:
        print(f"Status: ON TRACK or BEATING EXPECTATION")
    elif win_pct >= 50:
        print(f"Status: SLIGHTLY BELOW but within variance")
    else:
        print(f"Status: UNDERPERFORMING - investigate system")

# Breakdown by signal strength
print(f"\n\nBy Signal Strength:")
print("-"*60)

for threshold in [10, 5]:
    strong = df_graded[df_graded['gap'].abs() >= threshold]
    if len(strong) > 0:
        strong_wins = len(strong[strong['correct'] == True])
        strong_pct = strong_wins / len(strong) * 100
        print(f"  Gap >= {threshold}%: {strong_wins}/{len(strong)} ({strong_pct:.1f}%)")

# Pushes and skips
pushes = len(df_results[df_results['result'] == 'PUSH'])
skips = len(df_results[df_results['result'] == 'SKIP'])
print(f"\nPushes: {pushes}")
print(f"Skipped (gap < 5%): {skips}")

# Save detailed results
output_file = matchup_file.replace('.csv', '_validated.csv')
df_results.to_csv(output_file, index=False)
print(f"\n[OK] Validation results saved to: {output_file}")

print("\n[OK] Validation complete!")
