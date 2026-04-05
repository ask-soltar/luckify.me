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

# Load historical player data
print("Loading historical player data...")
historical_df = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition_roundtype.csv')
print(f"[OK] Loaded {len(historical_df)} historical records\n")

print("="*160)
print("2-BALL MATCHUP SCREENER - V3 (MARKET-BASED EDGE WITH HISTORICAL VALIDATION)")
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

def kelly_criterion(our_prob, market_implied_prob, odds):
    """
    Calculate Kelly fraction for 2-ball matchup
    our_prob = our model probability of winning
    market_implied_prob = market implied probability
    odds = American odds (e.g., -120, +100)
    Returns as percentage of bankroll
    """
    if our_prob <= market_implied_prob:
        return 0.0

    edge = our_prob - market_implied_prob

    # Convert American odds to decimal
    if odds < 0:
        decimal_odds = 1 + (100 / abs(odds))
    else:
        decimal_odds = 1 + (odds / 100)

    # Kelly formula: f* = (p * b - 1) / (b - 1)
    # where p = probability, b = decimal odds
    if decimal_odds <= 1:
        return 0.0

    kelly = (our_prob * decimal_odds - 1) / (decimal_odds - 1)
    return max(0, kelly)

try:
    # Load CSV
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()

    print(f"[OK] Loaded {len(df)} matchups")
    print(f"[OK] Columns: {df.columns.tolist()}\n")

    # Helper to get historical win rate
    def get_historical_wr(player_name, condition, round_type):
        """Get player's historical win rate for condition+roundtype combo"""
        match = historical_df[
            (historical_df['player_name'] == player_name) &
            (historical_df['condition'] == condition) &
            (historical_df['round_type'] == round_type)
        ]
        if len(match) > 0:
            row = match.iloc[0]
            return row['win_rate'], int(row['events'])
        return None, 0

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

            # Get historical data for validation
            hist_a, n_a = get_historical_wr(score_a['name'], row['Condition'], row['Round Type'])
            hist_b, n_b = get_historical_wr(score_b['name'], row['Condition'], row['Round Type'])

            # Historical matchup edge (if both have data)
            historical_edge = None
            data_quality = 'LIMITED'

            if hist_a is not None and hist_b is not None:
                if n_a >= 5 and n_b >= 5:
                    historical_edge = hist_a - hist_b
                    data_quality = 'FULL'
                else:
                    historical_edge = hist_a - hist_b
                    data_quality = 'LIMITED'

            # Matchup differentials
            market_diff = implied_a - implied_b
            model_diff = model_prob_a - model_prob_b
            matchup_edge = model_diff - market_diff

            # Determine which side has edge and if we can Kelly
            if matchup_edge > 0:
                bet_side = 'A'
            else:
                bet_side = 'B'
                matchup_edge = abs(matchup_edge)

            # Determine data quality level
            if hist_a is None or hist_b is None:
                data_quality = 'VERY LIMITED'
            elif n_a < 2 or n_b < 2:
                data_quality = 'VERY LIMITED'
            elif n_a < 5 or n_b < 5:
                data_quality = 'LIMITED'
            else:
                data_quality = 'FULL'

            # Kelly sizing and action determination
            if bet_side == 'A':
                kelly_full = kelly_criterion(model_prob_a, implied_a, ml_a)
            else:
                kelly_full = kelly_criterion(model_prob_b, implied_b, ml_b)

            kelly_qtr = kelly_full / 4

            # Action based on edge and data quality
            if matchup_edge < 0.01:  # Essentially zero or negative edge
                action_type = 'PASS'
                kelly_qtr = 0.0
            elif data_quality == 'FULL':
                action_type = 'KELLY'
            else:
                action_type = 'LEAN'

            results.append({
                'matchup_num': idx + 1,
                'player_a': score_a['name'],
                'ml_a': ml_a,
                'implied_a': round(implied_a * 100, 1),
                'model_a': round(model_prob_a * 100, 1),
                'n_a': n_a,
                'hist_a': round(hist_a * 100, 1) if hist_a is not None else None,
                'spec_a': 'YES' if score_a['has_specialization'] else '',
                'player_b': score_b['name'],
                'ml_b': ml_b,
                'implied_b': round(implied_b * 100, 1),
                'model_b': round(model_prob_b * 100, 1),
                'n_b': n_b,
                'hist_b': round(hist_b * 100, 1) if hist_b is not None else None,
                'spec_b': 'YES' if score_b['has_specialization'] else '',
                'matchup_edge': round(matchup_edge * 100, 1),
                'historical_edge': round(historical_edge * 100, 1) if historical_edge is not None else None,
                'bet_side': bet_side,
                'kelly_full': round(kelly_full * 100, 2),
                'kelly_qtr': round(kelly_qtr * 100, 2),
                'action_type': action_type,
                'data_quality': data_quality,
            })

        except Exception as e:
            print(f"[!] Error scoring matchup {idx+1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    # Display results
    print("="*160)
    print("MATCHUP RESULTS - MARKET EDGE ANALYSIS")
    print("="*160)
    print()

    for _, row in results_df.iterrows():
        spec_a_str = " [SPEC]" if row['spec_a'] else ""
        spec_b_str = " [SPEC]" if row['spec_b'] else ""

        hist_a_str = f"{row['hist_a']:.1f}% (N={int(row['n_a'])})" if row['hist_a'] is not None else "No Data"
        hist_b_str = f"{row['hist_b']:.1f}% (N={int(row['n_b'])})" if row['hist_b'] is not None else "No Data"

        print(f"MATCHUP #{int(row['matchup_num'])}:")
        print()
        print(f"  {row['player_a']:<30} {spec_a_str}")
        print(f"    Market (ML {row['ml_a']:>5}): {row['implied_a']:>5.1f}% implied")
        print(f"    Our Model:          {row['model_a']:>5.1f}%")
        print(f"    Historical:         {hist_a_str}")
        print()
        print(f"  vs")
        print()
        print(f"  {row['player_b']:<30} {spec_b_str}")
        print(f"    Market (ML {row['ml_b']:>5}): {row['implied_b']:>5.1f}% implied")
        print(f"    Our Model:          {row['model_b']:>5.1f}%")
        print(f"    Historical:         {hist_b_str}")
        print()
        print(f"  MODEL EDGE:       {row['matchup_edge']:>+5.1f}pp (favor {row['bet_side']})")
        if row['historical_edge'] is not None:
            print(f"  HISTORICAL EDGE:  {row['historical_edge']:>+5.1f}pp")
        print(f"  DATA QUALITY:     {row['data_quality']}")
        print(f"  FULL KELLY:       {row['kelly_qtr'] * 4:>5.2f}% → 1/4 KELLY: {row['kelly_qtr']:>5.2f}%")
        print(f"  ACTION:           {row['action_type']}")
        print()
        print("-" * 160)
        print()

    # Export
    output_file = input_file.replace('.csv', '_results_v3.csv')
    results_df.to_csv(output_file, index=False)
    print(f"[OK] Results exported to: {output_file}")
    print()

    # Bet Summary
    print("="*160)
    print("BET SUMMARY - ACTIONABLE RECOMMENDATIONS")
    print("="*160)
    print()

    for _, row in results_df.iterrows():
        edge = row['matchup_edge']
        kelly = row['kelly_qtr']
        side = row['bet_side']
        player = row['player_a'] if side == 'A' else row['player_b']
        spec = f" [SPEC]" if (row['spec_a'] if side == 'A' else row['spec_b']) else ""
        action = row['action_type']
        quality = row['data_quality']

        if action == 'PASS':
            recommendation = f"PASS - No edge"
        elif action == 'LEAN':
            if quality == 'VERY LIMITED':
                recommendation = f"LEAN {side} {edge:+.1f}pp on {player}{spec} [{quality}]"
            else:
                recommendation = f"LEAN {side} {edge:+.1f}pp on {player}{spec} [LIMITED]"
        else:  # KELLY
            if kelly < 0.25:
                recommendation = f"SMALL - 1/4 Kelly {kelly:.2f}% on {player}{spec}"
            elif kelly < 0.5:
                recommendation = f"SMALL - 1/4 Kelly {kelly:.2f}% on {player}{spec}"
            elif kelly < 1.0:
                recommendation = f"MEDIUM - 1/4 Kelly {kelly:.2f}% on {player}{spec}"
            else:
                recommendation = f"LARGE - 1/4 Kelly {kelly:.2f}% on {player}{spec}"

        print(f"#{int(row['matchup_num']):2}: {recommendation}")

    print()
    print("="*160)
    print("SUMMARY")
    print("="*160)
    print()

    positive_edges = len(results_df[results_df['matchup_edge'] > 0])
    full_data = len(results_df[results_df['data_quality'] == 'FULL'])
    limited_data = len(results_df[results_df['data_quality'] == 'LIMITED'])
    very_limited = len(results_df[results_df['data_quality'] == 'VERY LIMITED'])

    kelly_count = len(results_df[results_df['action_type'] == 'KELLY'])
    lean_count = len(results_df[results_df['action_type'] == 'LEAN'])
    pass_count = len(results_df[results_df['action_type'] == 'PASS'])

    avg_edge = results_df['matchup_edge'].mean()
    kelly_bets = results_df[results_df['action_type'] == 'KELLY']
    avg_kelly = kelly_bets['kelly_qtr'].mean() if len(kelly_bets) > 0 else 0
    total_kelly = kelly_bets['kelly_qtr'].sum() if len(kelly_bets) > 0 else 0

    print(f"Total Matchups:              {len(results_df)}")
    print(f"Positive Edges:              {positive_edges} ({positive_edges/len(results_df)*100:.0f}%)")
    print()
    print(f"DATA QUALITY BREAKDOWN:")
    print(f"  Full (N>=5 both):          {full_data} ({full_data/len(results_df)*100:.0f}%)")
    print(f"  Limited (one <5):          {limited_data} ({limited_data/len(results_df)*100:.0f}%)")
    print(f"  Very Limited (one <2):     {very_limited} ({very_limited/len(results_df)*100:.0f}%)")
    print()
    print(f"ACTION BREAKDOWN:")
    print(f"  Kelly (sized):             {kelly_count} ({kelly_count/len(results_df)*100:.0f}%)")
    print(f"  Lean (directional):        {lean_count} ({lean_count/len(results_df)*100:.0f}%)")
    print(f"  Pass (no edge):            {pass_count} ({pass_count/len(results_df)*100:.0f}%)")
    print()
    print(f"Avg Model Edge:              +{avg_edge:.1f}pp")
    print(f"Avg 1/4 Kelly (Kelly only):  {avg_kelly:.2f}%")
    print(f"Total Bankroll Allocation:   {total_kelly:.2f}%")
    print()

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
