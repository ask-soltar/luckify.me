#!/usr/bin/env python3
"""
PLAYER SCREENER: Input player data, get V2 scores

Accepts: CSV file with player data
Output: Scored players with breakdown and explanations
"""

import pandas as pd
import sys
from player_scoring_system_v2 import PlayerScorerV2

print("="*100)
print("PLAYER SCREENER - V2 SCORING ENGINE")
print("="*100)
print()

# Initialize scorer
scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)
print()

# ============================================================================
# REQUIRED INPUT FORMAT
# ============================================================================

print("="*100)
print("REQUIRED INPUT FORMAT")
print("="*100)
print()

required_fields = """
CSV file with these columns (in any order):

REQUIRED (must be present):
  - name                  Player name (string) - e.g., "Rory McIlroy"
  - condition             Tournament condition - Calm / Moderate / Tough
  - round_type            Round type - Open / Survival / Positioning / Closing
  - color                 Feng shui color - Red / Blue / Green / Yellow / Purple / Orange
  - element               Wu Xing element - Fire / Earth / Wood / Metal / Water
  - exec_bucket           Execution percentile - 0 / 25 / 50 / 75
  - upside_bucket         Upside percentile - 0 / 25 / 50 / 75
  - chinese_zodiac        Zodiac sign - Rat / Ox / Tiger / Rabbit / Dragon / Snake / Horse / Goat / Monkey / Rooster / Dog / Pig

EXAMPLE CSV (save as "players.csv"):
---
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
Rory McIlroy,Calm,Positioning,Green,Metal,75,75,Snake
Jon Rahm,Calm,Closing,Blue,Fire,50,50,Dog
Scottie Scheffler,Calm,Closing,Purple,Water,75,50,Tiger
Max Homa,Calm,Closing,Yellow,Metal,50,50,Snake
---

OPTIONAL: You can add extra columns that won't be used (they'll be ignored)
"""

print(required_fields)
print()

# ============================================================================
# LOAD AND SCORE
# ============================================================================

if len(sys.argv) > 1:
    csv_file = sys.argv[1]
else:
    # Default location
    csv_file = 'D:\\Projects\\luckify-me\\players_to_score.csv'

print("="*100)
print(f"LOADING: {csv_file}")
print("="*100)
print()

try:
    df = pd.read_csv(csv_file)
    print(f"[OK] Loaded {len(df)} players\n")

    # Validate required columns
    required_cols = ['name', 'condition', 'round_type', 'color', 'element',
                     'exec_bucket', 'upside_bucket', 'chinese_zodiac']

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"[!] ERROR: Missing columns: {missing}")
        print(f"[!] Available columns: {df.columns.tolist()}")
        sys.exit(1)

    # Score each player
    print("="*100)
    print("SCORING RESULTS")
    print("="*100)
    print()

    results = []

    def round_to_bucket(value):
        """Round numeric value to nearest valid bucket (0, 25, 50, 75)"""
        if pd.isna(value):
            return 50
        v = int(value)
        buckets = [0, 25, 50, 75]
        return min(buckets, key=lambda x: abs(x - v))

    for idx, row in df.iterrows():
        player_dict = {
            'name': row['name'],
            'condition': row['condition'],
            'round_type': row['round_type'],
            'color': row['color'],
            'element': row['element'],
            'exec_bucket': round_to_bucket(row['exec_bucket']),
            'upside_bucket': round_to_bucket(row['upside_bucket']),
            'chinese_zodiac': row['chinese_zodiac'],
        }

        score = scorer.score_player(player_dict)
        results.append(score)

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('final_score', ascending=False)

    # Display summary
    print(results_df[[
        'name', 'final_score', 'blended_score', 'specialization_boost', 'score_source', 'has_specialization'
    ]].to_string(index=False))

    print()
    print("="*100)
    print("DETAILED BREAKDOWN (Top 5)")
    print("="*100)
    print()

    for idx, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
        print(f"{idx}. {row['name']:<25} -> {row['final_score']:>6.1f}%")
        print(f"   Model Signals:     {row['model_score']:>6.1f}% (Element: {row['element_score']:>6.1f}%, Zodiac: {row['zodiac_score']:>6.1f}%)")
        print(f"   Player History:    {row['player_history_score']:>6.1f}%")
        print(f"   Blended (70/30):   {row['blended_score']:>6.1f}%")

        if row['has_specialization']:
            print(f"   >>> SPECIALIZATION BOOST: +{row['specialization_boost']*100:>5.1f}pp")
            print(f"       (Player excels in this specific combo)")
        else:
            print(f"   (No specialization bonus for this combo)")

        print()

    # Export results
    output_file = csv_file.replace('.csv', '_scored.csv')
    results_df.to_csv(output_file, index=False)
    print(f"[OK] Full results exported to: {output_file}")
    print()

    # Matchup analysis if 2+ players
    if len(results_df) >= 2:
        print("="*100)
        print("2-BALL MATCHUP RECOMMENDATIONS")
        print("="*100)
        print()

        for i in range(min(5, len(results_df)-1)):
            p1 = results_df.iloc[i]
            p2 = results_df.iloc[i+1]

            diff = p1['final_score'] - p2['final_score']
            confidence = "HIGH" if abs(diff) > 5 else ("MEDIUM" if abs(diff) > 2.5 else "LOW")

            print(f"{p1['name']:<25} ({p1['final_score']:>6.1f}%)")
            print(f"  vs {p2['name']:<21} ({p2['final_score']:>6.1f}%)")
            print(f"  Differential: +{diff:>5.1f}pp | Confidence: {confidence}")

            if p1['has_specialization']:
                print(f"  >>> {p1['name']} has specialization in this combo")
            if p2['has_specialization']:
                print(f"  >>> {p2['name']} has specialization in this combo")

            print()

except FileNotFoundError:
    print(f"[!] File not found: {csv_file}")
    print()
    print("QUICK START:")
    print("1. Create a CSV file named 'players_to_score.csv' with the required columns")
    print("2. Run this script with the filename as argument:")
    print(f"   python player_screener.py players_to_score.csv")
    print()
    print("Or save to default location:")
    print(f"   {csv_file}")
    print()
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit(1)

print("="*100)
