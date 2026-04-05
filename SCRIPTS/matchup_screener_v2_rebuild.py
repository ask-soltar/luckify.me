"""
Matchup Screener — Color × Exec + Color × Upside Model (v2 Rebuild)
Scores: (Exec ROI + Upside ROI) / 2 per player
Uses rebuilt ROI tables from full ANALYSIS v3 data
"""

import pandas as pd
import numpy as np
import sys

# Load ROI tables (v2 rebuild)
print("\nLoading ROI tables (v2 rebuild)...")
try:
    df_exec = pd.read_csv('color_exec_bucket_roi_v2.csv')
    df_upside = pd.read_csv('color_upside_bucket_roi_v2.csv')
    print("  Color × Exec Bucket: loaded")
    print("  Color × Upside Bucket: loaded")
except FileNotFoundError as e:
    print(f"  ERROR: {e}")
    print("  Run: python3.13 build_color_exec_upside_roi_v2.py first")
    exit(1)

# Load matchup CSV
if len(sys.argv) < 2:
    print("\nUsage: python matchup_screener_v2_rebuild.py <matchup_file.csv>")
    print("\nNo file provided. Using default: matchup.csv")
    matchup_file = 'matchup.csv'
else:
    matchup_file = sys.argv[1]

try:
    df_matchups = pd.read_csv(matchup_file)
    print(f"\nLoaded matchups: {matchup_file}")
    print(f"  {len(df_matchups)} matchups to analyze")
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

print(f"\nColumn mapping:")
print(f"  Player A: {player_a_col}")
print(f"  Player B: {player_b_col}")
print(f"  Condition: {condition_col}")
print(f"  Round Type: {round_type_col}")
print(f"  Color [A]: {color_a_col}")
print(f"  Color [B]: {color_b_col}")
print(f"  Exec [A]: {exec_a_col}")
print(f"  Exec [B]: {exec_b_col}")
print(f"  Upside [A]: {upside_a_col}")
print(f"  Upside [B]: {upside_b_col}")

required = [player_a_col, player_b_col, condition_col, round_type_col,
            color_a_col, color_b_col, exec_a_col, exec_b_col, upside_a_col, upside_b_col]
if not all(required):
    print("\nERROR: Could not identify all required columns")
    print("CSV must include: Player A, Player B, Condition, Round Type, Color [A], Color [B], Exec [A], Exec [B], Upside [A], Upside [B]")
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

# Score each matchup
print("\n" + "="*140)
print("SCORING MATCHUPS (Color × Exec + Color × Upside, averaged)")
print("="*140 + "\n")

results = []

for idx, row in df_matchups.iterrows():
    player_a = str(row[player_a_col]).strip()
    player_b = str(row[player_b_col]).strip()
    condition = str(row[condition_col]).strip()
    round_type = str(row[round_type_col]).strip()
    color_a = str(row[color_a_col]).strip()
    color_b = str(row[color_b_col]).strip()

    exec_a_raw = row[exec_a_col]
    exec_b_raw = row[exec_b_col]
    upside_a_raw = row[upside_a_col]
    upside_b_raw = row[upside_b_col]

    # Bucket scores
    exec_a_bucket = bucket_score(exec_a_raw)
    exec_b_bucket = bucket_score(exec_b_raw)
    upside_a_bucket = bucket_score(upside_a_raw)
    upside_b_bucket = bucket_score(upside_b_raw)

    # Get ROIs
    exec_a_roi = get_exec_roi(condition, round_type, color_a, exec_a_bucket)
    exec_b_roi = get_exec_roi(condition, round_type, color_b, exec_b_bucket)
    upside_a_roi = get_upside_roi(condition, round_type, color_a, upside_a_bucket)
    upside_b_roi = get_upside_roi(condition, round_type, color_b, upside_b_bucket)

    # Average
    score_a = (exec_a_roi + upside_a_roi) / 2.0
    score_b = (exec_b_roi + upside_b_roi) / 2.0
    gap = score_a - score_b

    # Recommendation
    if gap > 8:
        recommendation = "BET A"
    elif gap < -8:
        recommendation = "BET B"
    else:
        recommendation = "SKIP"

    results.append({
        'player_a': player_a,
        'player_b': player_b,
        'condition': condition,
        'round_type': round_type,
        'score_a': score_a,
        'score_b': score_b,
        'gap': gap,
        'recommendation': recommendation,
        'color_a': color_a,
        'color_b': color_b,
        'exec_a': exec_a_raw,
        'exec_b': exec_b_raw,
        'upside_a': upside_a_raw,
        'upside_b': upside_b_raw,
        'exec_a_bucket': exec_a_bucket,
        'exec_b_bucket': exec_b_bucket,
        'upside_a_bucket': upside_a_bucket,
        'upside_b_bucket': upside_b_bucket,
        'exec_a_roi': exec_a_roi,
        'exec_b_roi': exec_b_roi,
        'upside_a_roi': upside_a_roi,
        'upside_b_roi': upside_b_roi
    })

# Sort by gap
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('gap', key=abs, ascending=False)

# Print results
print(f"{'Gap':>7} {'Rec':<10} {'Player A':<25} {'Player B':<25} {'Condition':<10} {'Round':<12}")
print("-"*140)

for _, row in df_results.iterrows():
    sign = "+" if row['gap'] > 0 else ""
    print(f"{sign}{row['gap']:>6.1f}% {row['recommendation']:<10} {row['player_a']:<25} {row['player_b']:<25} {row['condition']:<10} {row['round_type']:<12}")

# Detailed breakdown
print("\n" + "="*140)
print("DETAILED BREAKDOWN (Top 10 Edges)")
print("="*140)

for idx, (_, row) in enumerate(df_results.head(10).iterrows(), 1):
    gap_sign = "+" if row['gap'] > 0 else ""
    print(f"\n{idx}. {row['player_a']} vs {row['player_b']}")
    print(f"   Condition: {row['condition']} x {row['round_type']}")
    print(f"   EDGE: {gap_sign}{row['gap']:.1f}% -> {row['recommendation']}")
    print(f"   ")
    print(f"   {row['player_a']:<30} {row['player_b']:<30}")
    print(f"   Exec: {row['exec_a']:>6} ({row['exec_a_bucket']:<8}) ROI: {row['exec_a_roi']:>7.1f}%  |  {row['exec_b']:>6} ({row['exec_b_bucket']:<8}) ROI: {row['exec_b_roi']:>7.1f}%")
    print(f"   Upside: {row['upside_a']:>3} ({row['upside_a_bucket']:<8}) ROI: {row['upside_a_roi']:>7.1f}%  |  {row['upside_b']:>3} ({row['upside_b_bucket']:<8}) ROI: {row['upside_b_roi']:>7.1f}%")
    print(f"   SCORE: {row['score_a']:>6.1f}% vs {row['score_b']:>6.1f}%")

# Save results
output_file = matchup_file.replace('.csv', '_scored_v2_rebuild.csv')
df_results.to_csv(output_file, index=False)
print(f"\n\n[OK] Scored matchups saved to: {output_file}")

# Summary
print("\n" + "="*140)
print("SUMMARY")
print("="*140)
bet_a = len(df_results[df_results['recommendation'] == 'BET A'])
bet_b = len(df_results[df_results['recommendation'] == 'BET B'])
skip = len(df_results[df_results['recommendation'] == 'SKIP'])

print(f"\nTotal matchups: {len(df_results)}")
print(f"BET A (gap > 8%): {bet_a}")
print(f"BET B (gap < -8%): {bet_b}")
print(f"SKIP (gap -8% to 8%): {skip}")

print(f"\nBest edge: {df_results['gap'].abs().max():.1f}%")
print(f"Mean edge: {df_results['gap'].abs().mean():.1f}%")

print("\n[OK] Model: Color x Exec + Color x Upside (averaged)")
print("[OK] Built from fresh ANALYSIS v3 data")
print("[OK] Thresholds: ±8% for BET, <±8% SKIP")

print("\n[OK] Screener complete!")
