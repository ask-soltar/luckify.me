"""
Validation: 3-Ball Model (Color x Exec + Color x Upside)
Compares screener picks to actual results
Handles regular wins and pushes
"""

import pandas as pd
import sys

# Load scored matchups
if len(sys.argv) < 2:
    scored_file = 'matchup3b_scored_3ball.csv'
else:
    scored_file = sys.argv[1]

try:
    df_scored = pd.read_csv(scored_file)
    print(f"Loaded: {scored_file}")
    print(f"  {len(df_scored)} 3-balls with scores and results\n")
except FileNotFoundError:
    print(f"ERROR: {scored_file} not found")
    exit(1)

# Validate results
print("="*140)
print("VALIDATION: 3-BALL MODEL (Color x Exec + Color x Upside)")
print("="*140 + "\n")

results_list = []

for _, row in df_scored.iterrows():
    # Get prediction and result
    recommendation = str(row['recommendation']).strip()
    is_push = row['is_push']
    actual_winner = row['actual_winner'] if pd.notna(row['actual_winner']) else None
    best_player_letter = row['best_player']  # 'A', 'B', or 'C'
    edge = row['best_vs_second']

    # Map letter to player name
    player_map = {
        'A': row['player_a'],
        'B': row['player_b'],
        'C': row['player_c']
    }
    best_player_name = player_map.get(best_player_letter, None)

    # Determine prediction (use player name, not letter)
    if 'SKIP' in recommendation:
        prediction = "SKIP"
    elif 'STRONG' in recommendation or 'MODERATE' in recommendation or 'SLIGHT' in recommendation:
        prediction = best_player_name
    else:
        prediction = "SKIP"

    # Determine result
    if is_push:
        result = "PUSH"
        correct = None
    elif prediction == "SKIP":
        result = "SKIP"
        correct = None
    elif prediction == actual_winner:
        result = "WIN"
        correct = True
    else:
        result = "LOSS"
        correct = False

    results_list.append({
        'player_a': row['player_a'],
        'player_b': row['player_b'],
        'player_c': row['player_c'],
        'recommendation': recommendation,
        'prediction': prediction,
        'actual_winner': actual_winner,
        'is_push': is_push,
        'edge': edge,
        'result': result,
        'correct': correct
    })

df_results = pd.DataFrame(results_list)

# Graded only (exclude SKIP and PUSH)
graded = df_results[(df_results['result'] != 'SKIP') & (df_results['result'] != 'PUSH')]

if len(graded) > 0:
    wins = len(graded[graded['correct'] == True])
    losses = len(graded[graded['correct'] == False])
    win_pct = wins / len(graded) * 100

    print(f"Graded matchups: {len(graded)}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win rate: {win_pct:.1f}%")
    print(f"\nTarget: 55%+")

    if win_pct >= 55:
        print(f"Status: ON TRACK - {win_pct:.1f}% > 55% target")
    elif win_pct >= 50:
        print(f"Status: MARGINAL - {win_pct:.1f}% near 50%")
    else:
        print(f"Status: UNDERPERFORMING - {win_pct:.1f}% < 50%")
else:
    print("No graded matchups")

# By signal strength
print(f"\n" + "="*140)
print("BY SIGNAL STRENGTH (graded only)")
print("="*140)

for signal in ['STRONG', 'MODERATE', 'SLIGHT']:
    subset = graded[graded['recommendation'].str.contains(signal, na=False)]
    if len(subset) > 0:
        wins_sig = len(subset[subset['correct'] == True])
        rate_sig = wins_sig / len(subset) * 100
        mean_edge = subset['edge'].mean()
        print(f"\n{signal}:")
        print(f"  Matchups: {len(subset)}")
        print(f"  Wins: {wins_sig}")
        print(f"  Win rate: {rate_sig:.1f}%")
        print(f"  Mean edge: {mean_edge:.1f}%")

# Pushes and skips
pushes = len(df_results[df_results['result'] == 'PUSH'])
skips = len(df_results[df_results['result'] == 'SKIP'])

print(f"\n" + "="*140)
print("OTHER OUTCOMES")
print("="*140)
print(f"\nPushes: {pushes}")
print(f"Skipped (no edge): {skips}")
print(f"Total: {len(df_results)}")

# Save detailed results
output_file = scored_file.replace('.csv', '_validated.csv')
df_results.to_csv(output_file, index=False)
print(f"\n[OK] Validation results saved to: {output_file}")

print("\n[OK] Validation complete!")
