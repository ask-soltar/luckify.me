"""
Validation: Color x Exec + Color x Upside Model (v2 Rebuild)
Compares screener picks to actual results
"""

import pandas as pd
import sys

# Load scored matchups
if len(sys.argv) < 2:
    scored_file = 'matchup_scored_v2_rebuild.csv'
else:
    scored_file = sys.argv[1]

try:
    df_scored = pd.read_csv(scored_file)
    print(f"Loaded: {scored_file}")
except FileNotFoundError:
    print(f"ERROR: {scored_file} not found")
    exit(1)

# Load original matchup data for Winner column
matchup_file = 'matchup.csv'
try:
    df_matchups = pd.read_csv(matchup_file)
    print(f"Loaded: {matchup_file}")
except FileNotFoundError:
    print(f"ERROR: {matchup_file} not found")
    exit(1)

# Merge to get Winner column
def find_col(df, *keywords):
    for col in df.columns:
        col_lower = col.lower()
        if all(kw.lower() in col_lower for kw in keywords):
            return col
    return None

winner_col = find_col(df_matchups, 'winner')
if not winner_col:
    print("ERROR: Could not find 'Winner' column")
    exit(1)

df_matchups_mini = df_matchups[[find_col(df_matchups, 'player', 'a'),
                                 find_col(df_matchups, 'player', 'b'),
                                 winner_col]].copy()
df_matchups_mini.columns = ['player_a_orig', 'player_b_orig', 'winner']

# Merge with scored data
df_results = df_scored.copy()
df_results = df_results.merge(df_matchups_mini, left_on=['player_a', 'player_b'],
                               right_on=['player_a_orig', 'player_b_orig'], how='left')

if 'winner' not in df_results.columns or df_results['winner'].isna().all():
    print("ERROR: Could not match matchups with winners")
    exit(1)

print(f"Merged {len(df_results)} matchups with results\n")

# Score predictions
results_list = []
for _, row in df_results.iterrows():
    prediction = row['recommendation']
    winner = str(row['winner']).strip() if pd.notna(row['winner']) else ""

    # Prediction
    if prediction == 'BET A':
        pred_player = row['player_a']
    elif prediction == 'BET B':
        pred_player = row['player_b']
    else:
        pred_player = "SKIP"

    # Result
    if winner.lower() == "push":
        result = "PUSH"
        correct = None
    elif prediction == "SKIP":
        result = "SKIP"
        correct = None
    elif winner == pred_player:
        result = "WIN"
        correct = True
    else:
        result = "LOSS"
        correct = False

    results_list.append({
        'player_a': row['player_a'],
        'player_b': row['player_b'],
        'condition': row['condition'],
        'round_type': row['round_type'],
        'gap': row['gap'],
        'prediction': pred_player,
        'actual_winner': winner,
        'result': result,
        'correct': correct
    })

df_final = pd.DataFrame(results_list)

# Print summary
print("="*130)
print("VALIDATION: COLOR x EXEC + COLOR x UPSIDE (v2 Rebuild)")
print("="*130 + "\n")

# Graded only
graded = df_final[(df_final['result'] != 'SKIP') & (df_final['result'] != 'PUSH')]

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

# By round type
print(f"\n" + "="*130)
print("BY ROUND TYPE (graded only)")
print("="*130)

by_round = graded.groupby('round_type').agg({
    'result': 'count',
    'correct': lambda x: (x == True).sum(),
    'gap': ['mean', 'min', 'max']
})
by_round.columns = ['Total', 'Wins', 'Gap_Avg', 'Gap_Min', 'Gap_Max']
by_round['Win_Rate_%'] = by_round['Wins'] / by_round['Total'] * 100

print(by_round[['Total', 'Wins', 'Win_Rate_%', 'Gap_Avg']].to_string())

# Save
output_file = scored_file.replace('.csv', '_validated.csv')
df_final.to_csv(output_file, index=False)
print(f"\n[OK] Validation saved to: {output_file}")
