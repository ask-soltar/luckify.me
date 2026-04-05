#!/usr/bin/env python3
"""
2-BALL MATCHUP SCREENER

Input: TSV/CSV with format:
Player A | Condition | Round Type | Color [A] | Element [A] | Exec A | Upside [A] | Zodiac [A] |
Player B | Condition | Round Type | Color [B] | Element [B] | Exec B | Upside [B] | Zodiac [B]

Each row = one matchup (A vs B)
Output: Scores, differential, winner, confidence
"""

import pandas as pd
import sys
from player_scoring_system_v2 import PlayerScorerV2

# Initialize scorer
scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)

print("="*140)
print("2-BALL MATCHUP SCREENER - V2 SCORING ENGINE")
print("="*140)
print()

# Load file
if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'D:\\Projects\\luckify-me\\matchups.csv'

print(f"Loading: {input_file}\n")

try:
    # Try reading as tab-separated first (Excel copy-paste format)
    try:
        df = pd.read_csv(input_file, sep='\t')
    except:
        # Fallback to comma-separated
        df = pd.read_csv(input_file)

    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()

    print(f"[OK] Loaded {len(df)} matchups\n")

    # Validate columns
    required_a = ['Player A', 'Condition', 'Round Type', 'Color [A]', 'Element [A]', 'Exec A', 'Upside [A]', 'Zodiac [A]']
    required_b = ['Player B', 'Condition', 'Round Type', 'Color [B]', 'Element [B]', 'Exec B', 'Upside [B]', 'Zodiac [B]']

    # Check for variations in column names
    cols_lower = [c.lower() for c in df.columns]

    # Find actual column names (exact match preferred)
    def find_col(patterns):
        # First try exact match
        for col in df.columns:
            if col in patterns:
                return col
        # Then try partial match
        for col in df.columns:
            col_lower = col.lower().strip()
            for pattern in patterns:
                if pattern.lower() in col_lower:
                    return col
        return None

    player_a_col = find_col(['Player A'])
    player_b_col = find_col(['Player B'])
    condition_col = find_col(['Condition'])
    round_type_col = find_col(['Round Type'])

    # Color columns
    color_a_col = find_col(['Color [A]'])
    color_b_col = find_col(['Color [B]'])

    # Element columns
    elem_a_col = find_col(['Element [A]'])
    elem_b_col = find_col(['Element [B]'])

    # Exec columns
    exec_a_col = find_col(['Exec A'])
    exec_b_col = find_col(['Exec B'])

    # Upside columns
    upside_a_col = find_col(['Upside [A]'])
    upside_b_col = find_col(['Upside [B]'])

    # Zodiac columns
    zodiac_a_col = find_col(['Zodiac [A]'])
    zodiac_b_col = find_col(['Zodiac [B]'])

    # Helper to round buckets
    def round_to_bucket(value):
        if pd.isna(value):
            return 50
        v = int(float(value))
        buckets = [0, 25, 50, 75]
        return min(buckets, key=lambda x: abs(x - v))

    # Score each matchup
    results = []

    for idx, row in df.iterrows():
        player_a_dict = {
            'name': row[player_a_col],
            'condition': row[condition_col],
            'round_type': row[round_type_col],
            'color': row[color_a_col],
            'element': row[elem_a_col],
            'exec_bucket': round_to_bucket(row[exec_a_col]),
            'upside_bucket': round_to_bucket(row[upside_a_col]),
            'chinese_zodiac': row[zodiac_a_col],
        }

        player_b_dict = {
            'name': row[player_b_col],
            'condition': row[condition_col],
            'round_type': row[round_type_col],
            'color': row[color_b_col],
            'element': row[elem_b_col],
            'exec_bucket': round_to_bucket(row[exec_b_col]),
            'upside_bucket': round_to_bucket(row[upside_b_col]),
            'chinese_zodiac': row[zodiac_b_col],
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

    results_df = pd.DataFrame(results)

    # Display results
    print("="*140)
    print("MATCHUP RESULTS")
    print("="*140)
    print()

    for _, row in results_df.iterrows():
        spec_a_str = " [SPEC]" if row['spec_a'] else ""
        spec_b_str = " [SPEC]" if row['spec_b'] else ""

        # Create matchup string: "Player A vs Player B"
        matchup_str = f"{row['player_a']} ({row['score_a']:.1f}%){spec_a_str} vs {row['player_b']} ({row['score_b']:.1f}%){spec_b_str}"

        print(f"{int(row['matchup_num']):2}. {matchup_str:<95} | +{row['differential']:.1f}pp | {row['confidence']}")
        print()

    # Export results
    output_file = input_file.replace('.csv', '_results.csv').replace('.tsv', '_results.csv')
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

    print("Avg Differential: +{:.1f}pp".format(results_df['differential'].mean()))
    print()

except FileNotFoundError:
    print(f"[!] File not found: {input_file}")
    print()
    print("QUICK START:")
    print("1. Copy your matchup data (Player A vs Player B format)")
    print("2. Paste into Excel or CSV file")
    print("3. Run: python matchup_screener.py your_file.csv")
    print()
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
