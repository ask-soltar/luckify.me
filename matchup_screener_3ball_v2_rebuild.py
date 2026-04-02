"""
3-Ball Matchup Screener — Color × Exec + Color × Upside Model (v2 Rebuild)
Scores all 3 players and ranks by likelihood to win
Input: CSV with Player A/B/C, Condition, Round Type, Color [A/B/C], Exec [A/B/C], Upside [A/B/C]
Output: 3-balls ranked by edge (best player vs field)
"""

import pandas as pd
import numpy as np
import sys

# Load ROI tables (v2 rebuild)
print("\nLoading ROI tables (v2 rebuild)...")
try:
    df_exec = pd.read_csv('color_exec_bucket_roi_v2.csv')
    df_upside = pd.read_csv('color_upside_bucket_roi_v2.csv')
    print("  Color x Exec Bucket: loaded")
    print("  Color x Upside Bucket: loaded")
except FileNotFoundError as e:
    print(f"  ERROR: {e}")
    print("  Run: python3.13 build_color_exec_upside_roi_v2.py first")
    exit(1)

# Load matchup CSV
if len(sys.argv) < 2:
    print("\nUsage: python matchup_screener_3ball_v2_rebuild.py <matchup_file.csv>")
    print("\nNo file provided. Using default: matchups_3ball_sample.csv")
    matchup_file = 'matchups_3ball_sample.csv'
else:
    matchup_file = sys.argv[1]

try:
    # Try tab-separated first, then comma-separated
    if '\t' in open(matchup_file).readline():
        df_matchups = pd.read_csv(matchup_file, sep='\t')
    else:
        df_matchups = pd.read_csv(matchup_file)
    print(f"\nLoaded matchups: {matchup_file}")
    print(f"  {len(df_matchups)} 3-balls to analyze")
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

condition_col = find_col(df_matchups, 'condition')
round_type_col = find_col(df_matchups, 'round', 'type')

# Players A, B, C - more flexible matching
players = {}
for player_letter in ['a', 'b', 'c']:
    players[player_letter] = {
        'name': find_col(df_matchups, 'player', player_letter) or find_col(df_matchups, f'player {player_letter.upper()}'),
        'color': find_col(df_matchups, 'color', f'[{player_letter}]') or find_col(df_matchups, f'color {player_letter.upper()}'),
        'exec': find_col(df_matchups, 'exec', player_letter) or find_col(df_matchups, f'exec {player_letter.upper()}'),
        'upside': find_col(df_matchups, 'upside', f'[{player_letter}]') or find_col(df_matchups, f'upside {player_letter.upper()}'),
    }

print(f"\nColumn mapping:")
print(f"  Condition: {condition_col}")
print(f"  Round Type: {round_type_col}")
for p_letter in ['a', 'b', 'c']:
    p_info = players[p_letter]
    print(f"  Player {p_letter.upper()}: {p_info['name']}, Color: {p_info['color']}, Exec: {p_info['exec']}, Upside: {p_info['upside']}")

required = [condition_col, round_type_col] + [players[x][k] for x in ['a','b','c'] for k in ['name','color','exec','upside']]
if not all(required):
    print("\nERROR: Could not identify all required columns")
    exit(1)

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

# Score each 3-ball
print("\n" + "="*160)
print("SCORING 3-BALL MATCHUPS (Color x Exec + Color x Upside, averaged)")
print("="*160 + "\n")

results = []

for idx, row in df_matchups.iterrows():
    condition = str(row[condition_col]).strip()
    round_type = str(row[round_type_col]).strip()

    player_scores = {}

    # Score each player
    for p_letter in ['a', 'b', 'c']:
        p_info = players[p_letter]
        player_name = str(row[p_info['name']]).strip()
        color = str(row[p_info['color']]).strip()
        exec_raw = row[p_info['exec']]
        upside_raw = row[p_info['upside']]

        # Bucket scores
        exec_bucket = bucket_score(exec_raw)
        upside_bucket = bucket_score(upside_raw)

        # Get ROIs
        exec_roi = get_exec_roi(condition, round_type, color, exec_bucket)
        upside_roi = get_upside_roi(condition, round_type, color, upside_bucket)

        # Score
        score = (exec_roi + upside_roi) / 2.0

        player_scores[p_letter] = {
            'name': player_name,
            'color': color,
            'exec': exec_raw,
            'upside': upside_raw,
            'exec_bucket': exec_bucket,
            'upside_bucket': upside_bucket,
            'exec_roi': exec_roi,
            'upside_roi': upside_roi,
            'score': score
        }

    # Rank players
    ranked = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)

    # Calculate edges
    best_score = ranked[0][1]['score']
    second_score = ranked[1][1]['score']
    worst_score = ranked[2][1]['score']

    best_vs_second = best_score - second_score
    best_vs_worst = best_score - worst_score

    # Recommendation
    if best_vs_second > 8:
        recommendation = f"STRONG: Bet {ranked[0][0].upper()}"
    elif best_vs_second > 5:
        recommendation = f"MODERATE: Lean {ranked[0][0].upper()}"
    elif best_vs_second > 0:
        recommendation = f"SLIGHT: {ranked[0][0].upper()} favored"
    else:
        recommendation = "SKIP: No clear edge"

    results.append({
        'condition': condition,
        'round_type': round_type,
        'player_a': player_scores['a']['name'],
        'player_b': player_scores['b']['name'],
        'player_c': player_scores['c']['name'],
        'score_a': player_scores['a']['score'],
        'score_b': player_scores['b']['score'],
        'score_c': player_scores['c']['score'],
        'best_player': ranked[0][0].upper(),
        'best_score': best_score,
        'best_vs_second': best_vs_second,
        'best_vs_worst': best_vs_worst,
        'recommendation': recommendation,
        'color_a': player_scores['a']['color'],
        'color_b': player_scores['b']['color'],
        'color_c': player_scores['c']['color'],
        'exec_a': player_scores['a']['exec'],
        'exec_b': player_scores['b']['exec'],
        'exec_c': player_scores['c']['exec'],
        'upside_a': player_scores['a']['upside'],
        'upside_b': player_scores['b']['upside'],
        'upside_c': player_scores['c']['upside'],
    })

# Sort by edge
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('best_vs_second', ascending=False)

# Print results
print(f"{'Edge':>7} {'Best':>4} {'Rec':<20} {'Player A':<20} {'Player B':<20} {'Player C':<20}")
print("-"*160)

for _, row in df_results.iterrows():
    sign = "+" if row['best_vs_second'] > 0 else ""
    print(f"{sign}{row['best_vs_second']:>6.1f}% {row['best_player']:<4} {row['recommendation']:<20} {row['player_a']:<20} {row['player_b']:<20} {row['player_c']:<20}")

# Detailed breakdown
print("\n" + "="*160)
print("DETAILED BREAKDOWN (Top 10)")
print("="*160)

for idx, (_, row) in enumerate(df_results.head(10).iterrows(), 1):
    sign = "+" if row['best_vs_second'] > 0 else ""
    print(f"\n{idx}. {row['player_a']} vs {row['player_b']} vs {row['player_c']}")
    print(f"   Condition: {row['condition']} x {row['round_type']}")
    print(f"   EDGE: {sign}{row['best_vs_second']:.1f}% ({row['best_player']} best)")
    print(f"   Scores: A={row['score_a']:>6.1f}%, B={row['score_b']:>6.1f}%, C={row['score_c']:>6.1f}%")
    print(f"   {row['recommendation']}")

# Save results
output_file = matchup_file.replace('.csv', '_scored_3ball_v2.csv')
df_results.to_csv(output_file, index=False)
print(f"\n\n[OK] Scored 3-balls saved to: {output_file}")

# Summary
print("\n" + "="*160)
print("SUMMARY")
print("="*160)
strong = len(df_results[df_results['best_vs_second'] > 8])
moderate = len(df_results[(df_results['best_vs_second'] > 5) & (df_results['best_vs_second'] <= 8)])
slight = len(df_results[(df_results['best_vs_second'] > 0) & (df_results['best_vs_second'] <= 5)])
skip = len(df_results[df_results['best_vs_second'] <= 0])

print(f"\nTotal 3-balls: {len(df_results)}")
print(f"STRONG edge (> 8%): {strong}")
print(f"MODERATE edge (5-8%): {moderate}")
print(f"SLIGHT edge (0-5%): {slight}")
print(f"SKIP (no edge): {skip}")

print(f"\nBest edge: {df_results['best_vs_second'].max():.1f}%")
print(f"Mean edge: {df_results['best_vs_second'].mean():.1f}%")
print(f"Median edge: {df_results['best_vs_second'].median():.1f}%")

print("\n[OK] Model: Color x Exec + Color x Upside (averaged)")
print("[OK] Built from fresh ANALYSIS v3 data")
print("[OK] Open + Positioning rounds only")

print("\n[OK] 3-Ball screener complete!")
