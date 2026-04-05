#!/usr/bin/env python3
"""
2-BALL MATCHUP SCREENER - V2

Robust version with better column handling
"""

import pandas as pd
import sys
from player_scoring_system_v2 import PlayerScorerV2

scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)

print("="*140)
print("2-BALL MATCHUP SCREENER - V2 SCORING ENGINE")
print("="*140)
print()

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'D:\\Projects\\luckify-me\\matchups.csv'

print(f"Loading: {input_file}\n")

try:
    # Load CSV
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()

    print(f"[OK] Loaded {len(df)} matchups")
    print(f"[OK] Columns: {df.columns.tolist()}\n")

    # Helper to round buckets
    def round_to_bucket(value):
        if pd.isna(value):
            return 50
        try:
            v = int(float(value))
            buckets = [0, 25, 50, 75]
            return min(buckets, key=lambda x: abs(x - v))
        except:
            return 50

    # Score each matchup
    results = []

    for idx, row in df.iterrows():
        try:
            player_a_dict = {
                'name': row['Player A'],
                'condition': row['Condition'],
                'round_type': row['Round Type'],
                'color': row['Color [A]'],
                'element': row['Element [A]'],
                'exec_bucket': round_to_bucket(row['Exec A']),
                'upside_bucket': round_to_bucket(row['Upside [A]']),
                'chinese_zodiac': row['Zodiac [A]'],
            }

            player_b_dict = {
                'name': row['Player B'],
                'condition': row['Condition'],
                'round_type': row['Round Type'],
                'color': row['Color [B]'],
                'element': row['Element [B]'],
                'exec_bucket': round_to_bucket(row['Exec B']),
                'upside_bucket': round_to_bucket(row['Upside [B]']),
                'chinese_zodiac': row['Zodiac [B]'],
            }

            score_a = scorer.score_player(player_a_dict)
            score_b = scorer.score_player(player_b_dict)

            differential = score_a['final_score'] - score_b['final_score']

            if differential > 0:
                winner = score_a['name']
                confidence = 'HIGH' if abs(differential) > 5 else ('MEDIUM' if abs(differential) > 2.5 else 'LOW')
            else:
                winner = score_b['name']
                confidence = 'HIGH' if abs(differential) > 5 else ('MEDIUM' if abs(differential) > 2.5 else 'LOW')

            results.append({
                'matchup_num': idx + 1,
                'player_a': score_a['name'],
                'score_a': round(score_a['final_score'], 1),
                'spec_a': 'YES' if score_a['has_specialization'] else '',
                'player_b': score_b['name'],
                'score_b': round(score_b['final_score'], 1),
                'spec_b': 'YES' if score_b['has_specialization'] else '',
                'differential': round(abs(differential), 1),
                'winner': winner,
                'confidence': confidence,
            })

        except Exception as e:
            print(f"[!] Error scoring matchup {idx+1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    # Display results
    print("="*140)
    print("MATCHUP RESULTS")
    print("="*140)
    print()

    for _, row in results_df.iterrows():
        spec_a_str = " [SPEC]" if row['spec_a'] else ""
        spec_b_str = " [SPEC]" if row['spec_b'] else ""

        matchup_str = f"{row['player_a']} ({row['score_a']:.1f}%){spec_a_str} vs {row['player_b']} ({row['score_b']:.1f}%){spec_b_str}"

        print(f"{int(row['matchup_num']):2}. {matchup_str:<95} | +{row['differential']:.1f}pp | {row['confidence']}")

    print()

    # Export
    output_file = input_file.replace('.csv', '_results.csv')
    results_df.to_csv(output_file, index=False)
    print(f"[OK] Results exported to: {output_file}")
    print()

    # Summary
    print("="*140)
    print("SUMMARY")
    print("="*140)
    print()

    high_conf = len(results_df[results_df['confidence'] == 'HIGH'])
    med_conf = len(results_df[results_df['confidence'] == 'MEDIUM'])
    low_conf = len(results_df[results_df['confidence'] == 'LOW'])
    with_spec = len(results_df[(results_df['spec_a'] == 'YES') | (results_df['spec_b'] == 'YES')])

    print(f"Total Matchups:        {len(results_df)}")
    print(f"High Confidence:       {high_conf} ({high_conf/len(results_df)*100:.0f}%)")
    print(f"Medium Confidence:     {med_conf} ({med_conf/len(results_df)*100:.0f}%)")
    print(f"Low Confidence:        {low_conf} ({low_conf/len(results_df)*100:.0f}%)")
    print(f"With Specialization:   {with_spec} ({with_spec/len(results_df)*100:.0f}%)")
    print()
    print(f"Avg Differential: +{results_df['differential'].mean():.1f}pp")
    print()

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
