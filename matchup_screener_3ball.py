#!/usr/bin/env python3
"""
3-BALL MATCHUP SCREENER

Breaks 3-ball into 3x 2-ball matchups, scores each, combines edges
Output: All component matchups + combined player values + Kelly sizing
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
print("3-BALL MATCHUP SCREENER - COMPONENT 2-BALL BREAKDOWN")
print("="*160)
print()

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'D:\\Projects\\luckify-me\\matchups_3ball.csv'

print(f"Loading: {input_file}\n")

def american_to_implied(odds):
    """Convert American odds to implied probability"""
    odds = float(odds)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

def kelly_criterion(our_prob, market_implied_prob, odds):
    """Calculate Kelly fraction for 2-ball matchup"""
    if our_prob <= market_implied_prob:
        return 0.0

    # Convert American odds to decimal
    if odds < 0:
        decimal_odds = 1 + (100 / abs(odds))
    else:
        decimal_odds = 1 + (odds / 100)

    if decimal_odds <= 1:
        return 0.0

    kelly = (our_prob * decimal_odds - 1) / (decimal_odds - 1)
    return max(0, kelly)

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

def round_to_bucket(value):
    """Round to nearest bucket"""
    if pd.isna(value):
        return 50
    try:
        v = int(float(value))
        buckets = [0, 25, 50, 75]
        return min(buckets, key=lambda x: abs(x - v))
    except:
        return 50

try:
    # Load CSV
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()

    print(f"[OK] Loaded {len(df)} 3-ball matchups")
    print(f"[OK] Columns: {df.columns.tolist()}\n")

    results = []

    for idx, row in df.iterrows():
        try:
            # Extract data for all 3 players
            player_a_dict = {
                'name': row['Player [A]'],
                'condition': row['Condition'],
                'round_type': row['Round Type'],
                'color': row['Color [A]'],
                'element': row['Element [A]'],
                'exec_bucket': round_to_bucket(row['Exec [A]']),
                'upside_bucket': round_to_bucket(row['Upside [A]']),
                'chinese_zodiac': row['Zodiac [A]'],
            }

            player_b_dict = {
                'name': row['Player [B]'],
                'condition': row['Condition'],
                'round_type': row['Round Type'],
                'color': row['Color [B]'],
                'element': row['Element [B]'],
                'exec_bucket': round_to_bucket(row['Exec [B]']),
                'upside_bucket': round_to_bucket(row['Upside [B]']),
                'chinese_zodiac': row['Zodiac [B]'],
            }

            player_c_dict = {
                'name': row['Player [C]'],
                'condition': row['Condition'],
                'round_type': row['Round Type'],
                'color': row['Color [C]'],
                'element': row['Element [C]'],
                'exec_bucket': round_to_bucket(row['Exec [C]']),
                'upside_bucket': round_to_bucket(row['Upside [C]']),
                'chinese_zodiac': row['Zodiac [C]'],
            }

            # Score all 3 players
            score_a = scorer.score_player(player_a_dict)
            score_b = scorer.score_player(player_b_dict)
            score_c = scorer.score_player(player_c_dict)

            model_prob_a = score_a['final_score']
            model_prob_b = score_b['final_score']
            model_prob_c = score_c['final_score']

            # Normalize if scores are > 1 (raw strength scores vs probabilities)
            if model_prob_a > 1:
                model_prob_a = model_prob_a / 100
            if model_prob_b > 1:
                model_prob_b = model_prob_b / 100
            if model_prob_c > 1:
                model_prob_c = model_prob_c / 100

            # Extract ML odds for all 3
            ml_a = row['ML [A]']
            ml_b = row['ML [B]']
            ml_c = row['ML [C]']

            implied_a = american_to_implied(ml_a)
            implied_b = american_to_implied(ml_b)
            implied_c = american_to_implied(ml_c)

            # Normalize market odds to remove vig (sum to 1.0)
            implied_total = implied_a + implied_b + implied_c
            implied_a = implied_a / implied_total
            implied_b = implied_b / implied_total
            implied_c = implied_c / implied_total

            # Calculate 3x 2-ball edges
            # A vs B
            edge_a_vs_b = model_prob_a - model_prob_b
            market_diff_ab = implied_a - implied_b
            edge_ab = edge_a_vs_b - market_diff_ab

            # A vs C
            edge_a_vs_c = model_prob_a - model_prob_c
            market_diff_ac = implied_a - implied_c
            edge_ac = edge_a_vs_c - market_diff_ac

            # B vs C
            edge_b_vs_c = model_prob_b - model_prob_c
            market_diff_bc = implied_b - implied_c
            edge_bc = edge_b_vs_c - market_diff_bc

            # Combine edges for each player
            combined_edge_a = edge_ab + edge_ac
            combined_edge_b = -edge_ab + edge_bc
            combined_edge_c = -edge_ac - edge_bc

            # Determine best pick
            edges = [combined_edge_a, combined_edge_b, combined_edge_c]
            players = [score_a['name'], score_b['name'], score_c['name']]
            max_edge_idx = edges.index(max(edges))
            best_player = players[max_edge_idx]
            best_combined_edge = edges[max_edge_idx]

            # Get historical data for data quality
            hist_a, n_a = get_historical_wr(score_a['name'], row['Condition'], row['Round Type'])
            hist_b, n_b = get_historical_wr(score_b['name'], row['Condition'], row['Round Type'])
            hist_c, n_c = get_historical_wr(score_c['name'], row['Condition'], row['Round Type'])

            # Determine data quality
            all_n = [n_a, n_b, n_c]
            if any(n < 2 for n in all_n):
                data_quality = 'VERY LIMITED'
            elif any(n < 5 for n in all_n):
                data_quality = 'LIMITED'
            else:
                data_quality = 'FULL'

            # Filter: Individual player edge (model - market)
            model_scores = [model_prob_a, model_prob_b, model_prob_c]
            implied_probs = [implied_a, implied_b, implied_c]
            players_list = [score_a['name'], score_b['name'], score_c['name']]
            hist_wrs = [hist_a, hist_b, hist_c]
            ml_odds = [ml_a, ml_b, ml_c]

            # Calculate individual edge for each player
            individual_edges = [
                model_scores[i] - implied_probs[i] for i in range(3)
            ]

            # Find player with highest positive edge
            best_edge_idx = individual_edges.index(max(individual_edges))
            best_edge_player = players_list[best_edge_idx]
            best_edge_value = individual_edges[best_edge_idx]
            best_hist_wr = hist_wrs[best_edge_idx]
            best_implied = implied_probs[best_edge_idx]
            best_ml = ml_odds[best_edge_idx]

            # Override best_pick with highest individual edge player
            best_player = best_edge_player
            best_combined_edge = best_edge_value

            # Qualify if edge > 0 and historical supports it
            qualifies = (best_edge_value > 0) and (best_hist_wr is not None) and (best_hist_wr > best_implied)

            # Kelly sizing on best pick (highest edge player)
            kelly_full = kelly_criterion(model_scores[best_edge_idx], best_implied, best_ml)
            kelly_qtr = kelly_full / 4

            # For display
            both_agree = "YES" if best_edge_value > 0 else "NO"
            market_undervalues = "YES" if (best_hist_wr is not None and best_hist_wr > best_implied) else "NO"

            # Action determination
            if best_combined_edge < 0.01:
                action_type = 'PASS'
                kelly_qtr = 0.0
            elif data_quality == 'FULL':
                action_type = 'KELLY'
            else:
                action_type = 'LEAN'

            # Only add to results if qualifies
            if qualifies:
                results.append({
                'matchup_num': idx + 1,
                'player_a': score_a['name'],
                'model_a': round(model_prob_a * 100, 1),
                'implied_a': round(implied_a * 100, 1),
                'n_a': n_a,
                'player_b': score_b['name'],
                'model_b': round(model_prob_b * 100, 1),
                'implied_b': round(implied_b * 100, 1),
                'n_b': n_b,
                'player_c': score_c['name'],
                'model_c': round(model_prob_c * 100, 1),
                'implied_c': round(implied_c * 100, 1),
                'n_c': n_c,
                'edge_ab': round(edge_ab * 100, 1),
                'edge_ac': round(edge_ac * 100, 1),
                'edge_bc': round(edge_bc * 100, 1),
                'combined_edge_a': round(combined_edge_a * 100, 1),
                'combined_edge_b': round(combined_edge_b * 100, 1),
                'combined_edge_c': round(combined_edge_c * 100, 1),
                'best_pick': best_player,
                'best_combined_edge': round(best_combined_edge * 100, 1),
                'kelly_full': round(kelly_full * 100, 2),
                'kelly_qtr': round(kelly_qtr * 100, 2),
                'data_quality': data_quality,
                'action_type': action_type,
                'both_agree': 'YES' if both_agree else 'NO',
                'market_undervalues': 'YES' if market_undervalues else 'NO',
            })

        except Exception as e:
            print(f"[!] Error scoring 3-ball {idx+1}: {e}")
            continue

    results_df = pd.DataFrame(results)

    # Display results
    print("="*160)
    print("3-BALL MATCHUP RESULTS")
    print("="*160)
    print()

    for _, row in results_df.iterrows():
        print(f"MATCHUP #{int(row['matchup_num'])}:")
        print()
        print(f"  Players: {row['player_a']} (N={int(row['n_a'])}) vs {row['player_b']} (N={int(row['n_b'])}) vs {row['player_c']} (N={int(row['n_c'])})")
        print()
        print(f"  MODEL SCORES:")
        print(f"    {row['player_a']:<30} {row['model_a']:>5.1f}% (Market: {row['implied_a']:>5.1f}%)")
        print(f"    {row['player_b']:<30} {row['model_b']:>5.1f}% (Market: {row['implied_b']:>5.1f}%)")
        print(f"    {row['player_c']:<30} {row['model_c']:>5.1f}% (Market: {row['implied_c']:>5.1f}%)")
        print()
        print(f"  COMPONENT 2-BALL EDGES:")
        print(f"    {row['player_a']:<15} vs {row['player_b']:<15} {row['edge_ab']:>+6.1f}pp")
        print(f"    {row['player_a']:<15} vs {row['player_c']:<15} {row['edge_ac']:>+6.1f}pp")
        print(f"    {row['player_b']:<15} vs {row['player_c']:<15} {row['edge_bc']:>+6.1f}pp")
        print()
        print(f"  COMBINED 3-BALL VALUES:")
        print(f"    {row['player_a']:<30} {row['combined_edge_a']:>+6.1f}pp")
        print(f"    {row['player_b']:<30} {row['combined_edge_b']:>+6.1f}pp")
        print(f"    {row['player_c']:<30} {row['combined_edge_c']:>+6.1f}pp")
        print()
        print(f"  BEST PICK: {row['best_pick']} ({row['best_combined_edge']:+.1f}pp combined edge)")
        print(f"  DATA QUALITY: {row['data_quality']}")
        print(f"  KELLY: Full {row['kelly_full']:.2f}% -> 1/4 Kelly {row['kelly_qtr']:.2f}%")
        print(f"  ACTION: {row['action_type']}")
        print()
        print("-" * 160)
        print()

    # Export
    output_file = input_file.replace('.csv', '_results_3ball.csv')
    results_df.to_csv(output_file, index=False)
    print(f"[OK] Results exported to: {output_file}")
    print()

    # Recommended Bets Summary
    print("="*160)
    print("RECOMMENDED BETS")
    print("="*160)
    print()

    if len(results_df) > 0:
        print(f"{'#':<3} {'PLAYER':<30} {'MODEL':<8} {'MARKET':<8} {'EDGE':<8} {'REASON':<25} {'1/4 KELLY':<10}")
        print("-" * 160)

        for idx, row in results_df.iterrows():
            best_player = row['best_pick']
            if best_player == row['player_a']:
                model_val = row['model_a']
                market_val = row['implied_a']
            elif best_player == row['player_b']:
                model_val = row['model_b']
                market_val = row['implied_b']
            else:
                model_val = row['model_c']
                market_val = row['implied_c']

            reason = "Both Agree" if row['both_agree'] == 'YES' else "Market Undervalues"

            print(f"{int(row['matchup_num']):<3} {best_player:<30} {model_val:>6.1f}% {market_val:>6.1f}% {row['best_combined_edge']:>+7.1f}pp {reason:<25} {row['kelly_qtr']:>8.2f}%")

        print()
        print(f"Total Recommended Bets:     {len(results_df)}")
        print(f"Total 1/4 Kelly Allocation: {results_df['kelly_qtr'].sum():.2f}%")
        print()
    else:
        print("No bets meet filtering criteria (model highest + historic +EV)")
        print()

    # Summary
    print("="*160)
    print("SUMMARY")
    print("="*160)
    print()

    kelly_count = len(results_df[results_df['action_type'] == 'KELLY'])
    lean_count = len(results_df[results_df['action_type'] == 'LEAN'])
    pass_count = len(results_df[results_df['action_type'] == 'PASS'])
    avg_edge = results_df['best_combined_edge'].mean()
    kelly_bets = results_df[results_df['action_type'] == 'KELLY']
    total_kelly = kelly_bets['kelly_qtr'].sum() if len(kelly_bets) > 0 else 0

    print(f"Total 3-Ball Matchups:    {len(results_df)}")
    print(f"Positive Best Edges:      {len(results_df[results_df['best_combined_edge'] > 0])} ({len(results_df[results_df['best_combined_edge'] > 0])/len(results_df)*100:.0f}%)")
    print()
    print(f"Kelly Bets:               {kelly_count}")
    print(f"Lean Picks:               {lean_count}")
    print(f"Pass (no edge):           {pass_count}")
    print()
    print(f"Avg Best Combined Edge:   {avg_edge:+.1f}pp")
    print(f"Total 1/4 Kelly:          {total_kelly:.2f}%")
    print()

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
