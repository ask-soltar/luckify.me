#!/usr/bin/env python3
"""
MATCHUP REPORT GENERATOR - High Confidence Bets Only (ASCII version)
"""

import pandas as pd
import sys

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'soltar_matchups_results.csv'

try:
    # Load results
    df = pd.read_csv(input_file)

    # Filter HIGH confidence only
    high = df[df['confidence'] == 'HIGH'].copy()
    high = high.sort_values('differential', ascending=False).reset_index(drop=True)

    print()
    print("="*150)
    print("HIGH CONFIDENCE MATCHUPS - SOLTAR GOLF 2026".center(150))
    print("="*150)
    print()

    for idx, (_, row) in enumerate(high.iterrows(), 1):
        spec_indicator = " [SPECIALIZATION BONUS]" if (row['spec_a'] == 'YES' or row['spec_b'] == 'YES') else ""

        print(f"BET #{idx}")
        print("-"*150)
        print(f"  {row['player_a']:<35} ({row['score_a']:>5.1f}%)     vs     {row['player_b']:<35} ({row['score_b']:>5.1f}%)")
        print()
        print(f"  DIFFERENTIAL: +{row['differential']:.1f}pp  |  CONFIDENCE: HIGH{spec_indicator}")
        print()
        print()

    print("="*150)
    print("SUMMARY".ljust(151))
    print("="*150)
    print()
    print(f"Total High Confidence Bets:  {len(high)}")
    print(f"Average Differential:        +{high['differential'].mean():.1f}pp")
    print(f"Highest Edge:                +{high['differential'].max():.1f}pp  ({high.iloc[0]['player_a']} vs {high.iloc[0]['player_b']})")
    print()
    print()

    # Detailed breakdown table
    print("="*150)
    print("DETAILED BREAKDOWN")
    print("="*150)
    print()

    print(f"{'BET':<5} {'FAVORITE':<40} {'SCORE':<8} {'vs':<5} {'UNDERDOG':<40} {'SCORE':<8} {'EDGE':<10} {'NOTES':<15}")
    print("-"*150)

    for idx, (_, row) in enumerate(high.iterrows(), 1):
        notes = "[SPEC]" if (row['spec_a'] == 'YES' or row['spec_b'] == 'YES') else ""

        if row['score_a'] > row['score_b']:
            fav = row['player_a'][:39]
            fav_score = f"{row['score_a']:.1f}%"
            dog = row['player_b'][:39]
            dog_score = f"{row['score_b']:.1f}%"
        else:
            fav = row['player_b'][:39]
            fav_score = f"{row['score_b']:.1f}%"
            dog = row['player_a'][:39]
            dog_score = f"{row['score_a']:.1f}%"

        print(f"#{idx:<4} {fav:<40} {fav_score:<8} vs  {dog:<40} {dog_score:<8} +{row['differential']:<8.1f} {notes:<15}")

    print()
    print("="*150)
    print()

    # Export HIGH only
    output_file = input_file.replace('_results.csv', '_HIGH_ONLY.csv')
    high.to_csv(output_file, index=False)
    print(f"[OK] HIGH confidence results exported to: {output_file}")
    print()

except FileNotFoundError:
    print(f"[!] File not found: {input_file}")
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit(1)
