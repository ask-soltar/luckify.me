#!/usr/bin/env python3
"""
MATCHUP REPORT GENERATOR - High Confidence Bets Only

Creates a beautiful, organized report of HIGH confidence matchups
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
    print("╔" + "═"*138 + "╗")
    print("║" + " "*138 + "║")
    print("║" + "HIGH CONFIDENCE MATCHUPS - SOLTAR GOLF 2026".center(138) + "║")
    print("║" + " "*138 + "║")
    print("╚" + "═"*138 + "╝")
    print()

    for idx, (_, row) in enumerate(high.iterrows(), 1):
        spec_indicator = " 🎯 SPECIALIZATION BONUS" if (row['spec_a'] == 'YES' or row['spec_b'] == 'YES') else ""

        print(f"  ┌─ BET #{idx} ─────────────────────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"  │                                                                                                                   │")
        print(f"  │  {row['player_a']:<30} ({row['score_a']:>5.1f}%)     vs     {row['player_b']:<30} ({row['score_b']:>5.1f}%)  │")
        print(f"  │                                                                                                                   │")
        print(f"  │  Differential:  +{row['differential']:.1f}pp  |  Confidence: HIGH{spec_indicator}                                     │")
        print(f"  │                                                                                                                   │")
        print(f"  └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
        print()

    print()
    print("╔" + "═"*138 + "╗")
    print("║" + " "*138 + "║")
    print("║  SUMMARY".ljust(139) + "║")
    print("║" + " "*138 + "║")
    print("║  Total High Confidence Matchups: {:>3}                                                                               │".format(len(high)))
    print("║  Average Differential:           +{:.1f}pp                                                                              │".format(high['differential'].mean()))
    print("║  Highest Edge:                   +{:.1f}pp ({} vs {})                                                    │".format(
        high['differential'].max(),
        high.iloc[0]['player_a'],
        high.iloc[0]['player_b']
    ))
    print("║" + " "*138 + "║")
    print("╚" + "═"*138 + "╝")
    print()

    # Detailed breakdown table
    print("═"*138)
    print("DETAILED BREAKDOWN")
    print("═"*138)
    print()

    print(f"{'#':<3} {'Favorite':<32} {'Score':<8} {'vs':<3} {'Underdog':<32} {'Score':<8} {'Edge':<8} {'Notes':<20}")
    print("-"*138)

    for idx, (_, row) in enumerate(high.iterrows(), 1):
        notes = "[SPEC]" if (row['spec_a'] == 'YES' or row['spec_b'] == 'YES') else ""

        if row['score_a'] > row['score_b']:
            fav = row['player_a'][:31]
            fav_score = f"{row['score_a']:.1f}%"
            dog = row['player_b'][:31]
            dog_score = f"{row['score_b']:.1f}%"
        else:
            fav = row['player_b'][:31]
            fav_score = f"{row['score_b']:.1f}%"
            dog = row['player_a'][:31]
            dog_score = f"{row['score_a']:.1f}%"

        print(f"{idx:<3} {fav:<32} {fav_score:<8} vs  {dog:<32} {dog_score:<8} +{row['differential']:<6.1f} {notes:<20}")

    print()

    # Export HIGH only
    output_file = input_file.replace('_results.csv', '_HIGH_CONFIDENCE.csv')
    high.to_csv(output_file, index=False)
    print(f"✓ HIGH confidence results exported to: {output_file}")
    print()

except FileNotFoundError:
    print(f"[!] File not found: {input_file}")
    print()
    print("Usage: python matchup_report.py <results_file.csv>")
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit(1)
