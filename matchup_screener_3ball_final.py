"""
3-Ball Matchup Screener — Color x Exec + Color x Upside Model (v2 Rebuild)
Uses: Player A/B/C, Condition, Round Type, Color [A/B/C], Exec [A/B/C], Upside [A/B/C]
Skips matchups with missing required data
Output: Rankings + scores + Winner column preserved
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
    print("\nUsage: python matchup_screener_3ball_final.py <matchup_file.csv>")
    print("\nNo file provided. Using default: 3balls.csv")
    matchup_file = '3balls.csv'
else:
    matchup_file = sys.argv[1]

try:
    df_matchups = pd.read_csv(matchup_file, sep='\t' if '\t' in open(matchup_file).readline() else ',')
    print(f"\nLoaded matchups: {matchup_file}")
    print(f"  {len(df_matchups)} 3-balls to analyze")
except FileNotFoundError:
    print(f"ERROR: {matchup_file} not found")
    exit(1)

# Normalize column names (strip whitespace)
df_matchups.columns = df_matchups.columns.str.strip()

# Required columns (exact match, case-insensitive)
def find_col_exact(df, name):
    name_lower = name.lower()
    for col in df.columns:
        if col.lower() == name_lower:
            return col
    return None

# Build column map
required_cols = {
    'player_a': find_col_exact(df_matchups, 'Player A'),
    'player_b': find_col_exact(df_matchups, 'Player B'),
    'player_c': find_col_exact(df_matchups, 'Player C'),
    'condition': find_col_exact(df_matchups, 'Condition'),
    'round_type': find_col_exact(df_matchups, 'Round Type'),
    'color_a': find_col_exact(df_matchups, 'Color [A]'),
    'color_b': find_col_exact(df_matchups, 'Color [B]'),
    'color_c': find_col_exact(df_matchups, 'Color [C]'),
    'exec_a': find_col_exact(df_matchups, 'Exec A'),
    'exec_b': find_col_exact(df_matchups, 'Exec [B]'),
    'exec_c': find_col_exact(df_matchups, 'Exec C'),
    'upside_a': find_col_exact(df_matchups, 'Upside [A]'),
    'upside_b': find_col_exact(df_matchups, 'Upside [B]'),
    'upside_c': find_col_exact(df_matchups, 'Upside [C]'),
    'winner': find_col_exact(df_matchups, 'Winner'),
}

print(f"\nColumn mapping:")
for key, col in required_cols.items():
    status = "OK" if col else "MISSING"
    print(f"  {key}: {col} ({status})")

# Check required columns
missing = [k for k, v in required_cols.items() if v is None and k != 'winner']
if missing:
    print(f"\nERROR: Missing required columns: {missing}")
    exit(1)

# Parse winner for 3-ball (handle pushes)
def parse_3ball_winner(winner_str, player_a, player_b, player_c):
    """
    Parse 3-ball winner string.
    Returns: (actual_winner, is_push, push_type)

    Examples:
      "Sami Valimaki" -> ("Sami Valimaki", False, None)
      "Push (Jhonattan Vegas / Taylor Pendrith)" -> (None, True, "2-way")
      "Push" -> (None, True, "3-way")
    """
    if not winner_str or str(winner_str).strip() == '':
        return (None, False, None)

    winner_str = str(winner_str).strip()

    # Check if it's a push
    if winner_str.lower().startswith('push'):
        # Parse push type
        if '(' in winner_str and ')' in winner_str:
            # 2-way push: "Push (Player B / Player C)"
            return (None, True, '2-way')
        else:
            # 3-way push or just "Push"
            return (None, True, '3-way')
    else:
        # Regular winner
        winner_name = winner_str.strip()
        return (winner_name, False, None)

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
print("\n" + "="*180)
print("SCORING 3-BALL MATCHUPS (Color x Exec + Color x Upside, averaged)")
print("="*180 + "\n")

results = []
skipped = 0

for idx, row in df_matchups.iterrows():
    # Check for missing required data
    required_values = [
        row[required_cols['player_a']], row[required_cols['player_b']], row[required_cols['player_c']],
        row[required_cols['condition']], row[required_cols['round_type']],
        row[required_cols['color_a']], row[required_cols['color_b']], row[required_cols['color_c']],
        row[required_cols['exec_a']], row[required_cols['exec_b']], row[required_cols['exec_c']],
        row[required_cols['upside_a']], row[required_cols['upside_b']], row[required_cols['upside_c']],
    ]

    # Skip if any required value is NaN or empty string
    if any(pd.isna(v) or str(v).strip() == '' for v in required_values):
        skipped += 1
        continue

    condition = str(row[required_cols['condition']]).strip()
    round_type = str(row[required_cols['round_type']]).strip()

    player_scores = {}

    # Score each player
    for p_letter, p_key_name, p_key_color, p_key_exec, p_key_upside in [
        ('a', 'player_a', 'color_a', 'exec_a', 'upside_a'),
        ('b', 'player_b', 'color_b', 'exec_b', 'upside_b'),
        ('c', 'player_c', 'color_c', 'exec_c', 'upside_c'),
    ]:
        player_name = str(row[required_cols[p_key_name]]).strip()
        color = str(row[required_cols[p_key_color]]).strip()
        exec_raw = row[required_cols[p_key_exec]]
        upside_raw = row[required_cols[p_key_upside]]

        # Bucket scores
        exec_bucket = bucket_score(exec_raw)
        upside_bucket = bucket_score(upside_raw)

        if exec_bucket is None or upside_bucket is None:
            skipped += 1
            break

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

    # Skip if bucketing failed
    if len(player_scores) < 3:
        skipped += 1
        continue

    # Rank players
    ranked = sorted(player_scores.items(), key=lambda x: x[1]['score'], reverse=True)

    # Calculate edges
    best_score = ranked[0][1]['score']
    second_score = ranked[1][1]['score']

    best_vs_second = best_score - second_score

    # Recommendation
    if best_vs_second > 8:
        recommendation = f"STRONG: Bet {ranked[0][0].upper()}"
    elif best_vs_second > 5:
        recommendation = f"MODERATE: Lean {ranked[0][0].upper()}"
    elif best_vs_second > 0:
        recommendation = f"SLIGHT: {ranked[0][0].upper()} favored"
    else:
        recommendation = "SKIP: No edge"

    # Get winner if available
    winner_raw = str(row[required_cols['winner']]).strip() if required_cols['winner'] else ""
    actual_winner, is_push, push_type = parse_3ball_winner(
        winner_raw,
        player_scores['a']['name'],
        player_scores['b']['name'],
        player_scores['c']['name']
    )

    results.append({
        'player_a': player_scores['a']['name'],
        'player_b': player_scores['b']['name'],
        'player_c': player_scores['c']['name'],
        'condition': condition,
        'round_type': round_type,
        'score_a': player_scores['a']['score'],
        'score_b': player_scores['b']['score'],
        'score_c': player_scores['c']['score'],
        'best_player': ranked[0][0].upper(),
        'best_score': best_score,
        'best_vs_second': best_vs_second,
        'recommendation': recommendation,
        'winner_raw': winner_raw,
        'actual_winner': actual_winner,
        'is_push': is_push,
        'push_type': push_type,
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

df_results = pd.DataFrame(results)

print(f"Processed: {len(df_matchups)} matchups")
print(f"Scored: {len(df_results)}")
print(f"Skipped (missing data): {skipped}\n")

# Sort by edge
df_results = df_results.sort_values('best_vs_second', ascending=False)

# Print results
print(f"{'Edge':>7} {'Best':>4} {'Rec':<20} {'Player A':<20} {'Player B':<20} {'Player C':<20} {'Result':<20}")
print("-"*180)

for _, row in df_results.iterrows():
    sign = "+" if row['best_vs_second'] > 0 else ""

    # Format result
    if row['is_push']:
        if row['push_type'] == '2-way':
            result_str = "PUSH (2-way)"
        else:
            result_str = "PUSH (3-way)"
    elif pd.notna(row['actual_winner']) and row['actual_winner']:
        result_str = f"WON: {row['actual_winner']}"
    else:
        result_str = "NO RESULT"

    print(f"{sign}{row['best_vs_second']:>6.1f}% {row['best_player']:<4} {row['recommendation']:<20} {row['player_a']:<20} {row['player_b']:<20} {row['player_c']:<20} {result_str:<20}")

# Detailed breakdown
if len(df_results) > 0:
    print("\n" + "="*180)
    print("DETAILED BREAKDOWN (Top 10)")
    print("="*180)

    for idx, (_, row) in enumerate(df_results.head(10).iterrows(), 1):
        sign = "+" if row['best_vs_second'] > 0 else ""

        # Format result for display
        if row['is_push']:
            if row['push_type'] == '2-way':
                result_str = "PUSH (2-way push)"
            else:
                result_str = "PUSH (3-way / all tied)"
        elif pd.notna(row['actual_winner']) and row['actual_winner']:
            result_str = f"WINNER: {row['actual_winner']}"
        else:
            result_str = "No result recorded"

        print(f"\n{idx}. {row['player_a']} vs {row['player_b']} vs {row['player_c']}")
        print(f"   Condition: {row['condition']} x {row['round_type']}")
        print(f"   EDGE: {sign}{row['best_vs_second']:.1f}% ({row['best_player']} best)")
        print(f"   Scores: A={row['score_a']:>6.1f}%, B={row['score_b']:>6.1f}%, C={row['score_c']:>6.1f}%")
        print(f"   {row['recommendation']}")
        print(f"   Result: {result_str}")

# Save results
output_file = matchup_file.replace('.csv', '').replace('.tsv', '') + '_scored_3ball.csv'
df_results.to_csv(output_file, index=False)
print(f"\n\n[OK] Scored 3-balls saved to: {output_file}")

# Summary
print("\n" + "="*180)
print("SUMMARY")
print("="*180)
strong = len(df_results[df_results['best_vs_second'] > 8])
moderate = len(df_results[(df_results['best_vs_second'] > 5) & (df_results['best_vs_second'] <= 8)])
slight = len(df_results[(df_results['best_vs_second'] > 0) & (df_results['best_vs_second'] <= 5)])
skip = len(df_results[df_results['best_vs_second'] <= 0])

print(f"\nTotal 3-balls scored: {len(df_results)}")
print(f"STRONG edge (> 8%): {strong}")
print(f"MODERATE edge (5-8%): {moderate}")
print(f"SLIGHT edge (0-5%): {slight}")
print(f"SKIP (no edge): {skip}")

if len(df_results) > 0:
    print(f"\nBest edge: {df_results['best_vs_second'].max():.1f}%")
    print(f"Mean edge: {df_results['best_vs_second'].mean():.1f}%")
    print(f"Median edge: {df_results['best_vs_second'].median():.1f}%")

print("\n[OK] Model: Color x Exec + Color x Upside (averaged)")
print("[OK] Built from ANALYSIS v3 data (Open + Positioning only)")

print("\n[OK] 3-Ball screener complete!")
