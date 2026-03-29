#!/usr/bin/env python3
"""
2-BALL MATCHUP SCREENER - V3

With Market-Based Edge Detection + Kelly Criterion Sizing

Input: CSV with Player A | ML | Condition | Round Type | [A attrs] | Player B | ML | Condition | Round Type | [B attrs]
Output: Side-by-side comparison showing our model % vs market implied % + Kelly bet sizing
"""

import pandas as pd
import sys
from player_scoring_system_v2 import PlayerScorerV2

scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)

print("="*160)
print("2-BALL MATCHUP SCREENER - V3 (MARKET-BASED EDGE)")
print("="*160)
print()

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'D:\\Projects\\luckify-me\\matchups.csv'

print(f"Loading: {input_file}\n")

def american_to_implied(odds):
    """Convert American odds to implied probability"""
    odds = float(odds)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

def kelly_criterion(edge, implied_prob):
    """
    Calculate Kelly fraction (full Kelly)
    edge = our predicted prob - market implied prob
    Returns as percentage of bankroll
    """
    if edge <= 0:
        return 0.0

    prob_win = implied_prob + edge
    prob_loss = 1 - prob_win

    # Kelly formula: f* = (bp - q) / b
    # Simplified for -110 odds (b=1): f* = 2p - 1
    # For general case with odds:
    if prob_win >= 1.0 or prob_win <= 0:
        return 0.0

    # Using simplified Kelly for even-money-ish bets
    kelly = prob_win - prob_loss
    return max(0, kelly)

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

    results = []

    for idx, row in df.iterrows():
        try:
            # Extract ML odds (need to handle column names carefully)
            # Looking for "ML" columns - there should be 2 (one for A, one for B)
            ml_cols = [c for c in df.columns if c == 'ML']

            if len(ml_cols) < 2:
                print(f"[!] Expected 2 ML columns, found {len(ml_cols)} at row {idx+1}")
                continue

            ml_a = row.iloc[df.columns.get_loc('Player A') + 1]  # ML is right after Player A
            ml_b = row.iloc[df.columns.get_loc('Player B') + 1]  # ML is right after Player B

            implied_a = american_to_implied(ml_a)
            implied_b = american_to_implied(ml_b)

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

            model_prob_a = score_a['final_score']
            model_prob_b = score_b['final_score']

            edge_a = model_prob_a - implied_a
            edge_b = model_prob_b - implied_b

            kelly_a = kelly_criterion(edge_a, implied_a) / 4  # Quarter Kelly
            kelly_b = kelly_criterion(edge_b, implied_b) / 4  # Quarter Kelly

            results.append({
                'matchup_num': idx + 1,
                'player_a': score_a['name'],
                'ml_a': ml_a,
                'implied_a': round(implied_a * 100, 1),
                'model_a': round(model_prob_a * 100, 1),
                'edge_a': round(edge_a * 100, 1),
                'kelly_a': round(kelly_a * 100, 2),
                'spec_a': 'YES' if score_a['has_specialization'] else '',
                'player_b': score_b['name'],
                'ml_b': ml_b,
                'implied_b': round(implied_b * 100, 1),
                'model_b': round(model_prob_b * 100, 1),
                'edge_b': round(edge_b * 100, 1),
                'kelly_b': round(kelly_b * 100, 2),
                'spec_b': 'YES' if score_b['has_specialization'] else '',
            })

        except Exception as e:
            print(f"[!] Error scoring matchup {idx+1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    # Display results
    print("="*160)
    print("MATCHUP RESULTS - SIDE BY SIDE")
    print("="*160)
    print()

    for _, row in results_df.iterrows():
        spec_a_str = " [SPEC]" if row['spec_a'] else ""
        spec_b_str = " [SPEC]" if row['spec_b'] else ""

        print(f"MATCHUP #{int(row['matchup_num'])}:")
        print()
        print(f"  {row['player_a']:<30} {spec_a_str}")
        print(f"    Market (ML {row['ml_a']:>5}): {row['implied_a']:>5.1f}% implied")
        print(f"    Our Model:          {row['model_a']:>5.1f}%")
        print(f"    Edge:               {row['edge_a']:>+5.1f}pp")
        print(f"    Quarter Kelly:      {row['kelly_a']:>5.2f}% of bankroll")
        print()
        print(f"  vs")
        print()
        print(f"  {row['player_b']:<30} {spec_b_str}")
        print(f"    Market (ML {row['ml_b']:>5}): {row['implied_b']:>5.1f}% implied")
        print(f"    Our Model:          {row['model_b']:>5.1f}%")
        print(f"    Edge:               {row['edge_b']:>+5.1f}pp")
        print(f"    Quarter Kelly:      {row['kelly_b']:>5.2f}% of bankroll")
        print()
        print("-" * 160)
        print()

    # Export
    output_file = input_file.replace('.csv', '_results_v3.csv')
    results_df.to_csv(output_file, index=False)
    print(f"[OK] Results exported to: {output_file}")
    print()

    # Summary
    print("="*160)
    print("SUMMARY")
    print("="*160)
    print()

    positive_edge_a = len(results_df[results_df['edge_a'] > 0])
    positive_edge_b = len(results_df[results_df['edge_b'] > 0])
    avg_edge_a = results_df['edge_a'].mean()
    avg_edge_b = results_df['edge_b'].mean()
    avg_kelly = (results_df['kelly_a'].mean() + results_df['kelly_b'].mean()) / 2

    print(f"Total Matchups:        {len(results_df)}")
    print(f"Player A Positive Edge: {positive_edge_a} ({positive_edge_a/len(results_df)*100:.0f}%)")
    print(f"Player B Positive Edge: {positive_edge_b} ({positive_edge_b/len(results_df)*100:.0f}%)")
    print()
    print(f"Avg Edge (A):          +{avg_edge_a:.1f}pp")
    print(f"Avg Edge (B):          +{avg_edge_b:.1f}pp")
    print(f"Avg Quarter Kelly:     {avg_kelly:.2f}%")
    print()

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
