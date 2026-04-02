"""
2-Ball Matchup Screener — System 1 Only (Color × Element)
Scores players based on Color + Element combinations only
Input: CSV with Player A, Player B, Condition, Round Type, Color [A], Color [B], Element [A], Element [B]
Output: Matchups sorted by gap (biggest advantages first)
"""

import pandas as pd
import numpy as np
import sys

# Load signal database
print("\nLoading signal database...")
try:
    df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')
    print("  System 1 (Color×Element): loaded")
except FileNotFoundError as e:
    print(f"  ERROR: {e}")
    print("  Make sure combo_scoring_rce_all_combos.csv exists")
    exit(1)

# Load matchup CSV
if len(sys.argv) < 2:
    print("\nUsage: python matchup_screener_system1_only.py <matchup_file.csv>")
    print("\nNo file provided. Using default: matchups.csv")
    matchup_file = 'matchups.csv'
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
print(f"\nColumns found: {list(df_matchups.columns)}")

# Identify columns (case-insensitive)
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

print(f"\nColumn mapping:")
print(f"  Player A: {player_a_col}")
print(f"  Player B: {player_b_col}")
print(f"  Condition: {condition_col}")
print(f"  Round Type: {round_type_col}")
print(f"  Color [A]: {color_a_col}")
print(f"  Color [B]: {color_b_col}")
print(f"  Element [A]: {element_a_col}")
print(f"  Element [B]: {element_b_col}")
print(f"  (Moon, Horoscope columns ignored — System 1 only)")

required = [player_a_col, player_b_col, condition_col, round_type_col, color_a_col, color_b_col,
            element_a_col, element_b_col]
if not all(required):
    print("\nERROR: Could not identify all required columns")
    print("CSV must include: Player A, Player B, Condition, Round Type, Color [A], Color [B], Element [A], Element [B]")
    exit(1)

# Score each matchup
print("\n" + "="*140)
print("SCORING MATCHUPS (System 1: Color × Element)")
print("="*140 + "\n")

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

    # Recommendation (adjusted thresholds for single system)
    if gap > 6:
        recommendation = "BET A"
    elif gap < -6:
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
        'element_a': element_a,
        'element_b': element_b
    })

# Sort by gap (biggest edges first)
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
    print(f"   Condition: {row['condition']} × {row['round_type']}")
    print(f"   EDGE: {gap_sign}{row['gap']:.1f}% → {row['recommendation']}")
    print(f"   ")
    print(f"   {row['player_a']:<25} {row['player_b']:<25}")
    print(f"   System 1 (Color×Element):")
    print(f"     {row['color_a']} × {row['element_a']:<15} = {row['score_a']:>6.1f}%  |  {row['color_b']} × {row['element_b']:<15} = {row['score_b']:>6.1f}%")
    print(f"   TOTAL: {row['score_a']:>6.1f}% vs {row['score_b']:>6.1f}%")

# Save results
output_file = matchup_file.replace('.csv', '_scored_s1.csv')
df_results.to_csv(output_file, index=False)
print(f"\n\n[OK] Scored matchups saved to: {output_file}")

# Summary
print("\n" + "="*140)
print("SUMMARY")
print("="*140)
bet_a = len(df_results[df_results['recommendation'].str.contains('BET A')])
bet_b = len(df_results[df_results['recommendation'] == 'BET B'])
skip = len(df_results[df_results['recommendation'] == 'SKIP'])

print(f"\nTotal matchups: {len(df_results)}")
print(f"BET A (gap > 6%): {bet_a}")
print(f"BET B (gap < -6%): {bet_b}")
print(f"SKIP (gap -6% to 6%): {skip}")

print(f"\nBest edge: {df_results['gap'].abs().max():.1f}%")
print(f"Mean edge: {df_results['gap'].abs().mean():.1f}%")

print("\n⚠️  NOTE: System 1 only (Color×Element). No Moon/Horoscope boost.")
print("Expected validation: ~50-55% win rate (conservative until validated live)")

print("\n[OK] Screener complete!")
