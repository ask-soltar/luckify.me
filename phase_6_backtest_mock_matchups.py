"""
Phase 6: Backtest Mock Matchups vs -110 Market
Game Theory Approach: Find and quantify market inefficiencies

Test on 2025-2026 data only (avoids historical bias)
Flat $100 bets on +EV opportunities
Market baseline: -110 (52.38% to break even)
"""

import pandas as pd
import numpy as np

print("Loading 2025-2026 data...")
residuals = pd.read_csv('residual_table.csv')
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')

# Filter to 2025-2026 only
analysis = analysis[analysis['year'].isin([2025, 2026])]
residuals = residuals[residuals['year'].isin([2025, 2026])]

print(f"Residuals (2025-2026): {len(residuals)} player-rounds")
print(f"Analysis (2025-2026): {len(analysis)} records")

# Load fair odds model
fair_odds = pd.read_csv('matchup_fair_odds_optimized.csv')
player_vol = pd.read_csv('player_volatility_table.csv')

# Condition averages
condition_avgs = analysis.groupby('condition')['player_hist_par'].mean().to_dict()

# Merge residuals with player data for shrinkage calculation
merged = residuals.merge(
    analysis[['player_id', 'event_id', 'year', 'round_num', 'player_hist_par', 'player_his_cnt']],
    on=['player_id', 'event_id', 'year', 'round_num'],
    how='inner'
)

merged = merged.dropna(subset=['projected_vs_par', 'actual_vs_par', 'condition', 'player_hist_par', 'player_his_cnt'])

print(f"Merged 2025-2026 data: {len(merged)} player-rounds")

# Recalculate with optimized shrinkage (param 50)
SHRINKAGE_PARAM = 50
merged['condition_avg'] = merged['condition'].map(condition_avgs)
merged['projected_vs_par_opt'] = (
    (merged['player_hist_par'] * merged['player_his_cnt'] +
     merged['condition_avg'] * SHRINKAGE_PARAM) /
    (merged['player_his_cnt'] + SHRINKAGE_PARAM)
)

# Add volatility tier
merged = merged.merge(player_vol[['player_id', 'reliability', 'resid_n']], on='player_id', how='left')

# Generate all 2-ball matchups for 2025-2026
print("\nGenerating 2025-2026 matchups...")
matchups = []

for (event_id, year, round_num), group in merged.groupby(['event_id', 'year', 'round_num']):
    field_avg = group['projected_vs_par_opt'].mean()
    players_list = group.to_dict('records')

    for i in range(len(players_list)):
        for j in range(i + 1, len(players_list)):
            pa = players_list[i]
            pb = players_list[j]

            # Calculate EVs
            ev_a = field_avg - pa['projected_vs_par_opt']
            ev_b = field_avg - pb['projected_vs_par_opt']
            relative_ev = ev_a - ev_b

            # Bucket for lookup
            ev_bucket = (relative_ev / 0.25).round() * 0.25

            # Look up fair probability
            fair_row = fair_odds[fair_odds['ev_bucket'] == ev_bucket]
            if fair_row.empty:
                continue

            fair_prob_a = fair_row['p_a_win'].values[0]

            # Actual outcome
            actual_a = pa['actual_vs_par']
            actual_b = pb['actual_vs_par']
            a_wins = 1 if actual_a < actual_b else 0

            matchups.append({
                'event_id': event_id,
                'year': year,
                'round_num': round_num,
                'player_a': pa['player_name'],
                'player_b': pb['player_name'],
                'tier_a': pa['reliability'],
                'tier_b': pb['reliability'],
                'sample_n_a': pa['resid_n'],
                'sample_n_b': pb['resid_n'],
                'relative_ev': relative_ev,
                'ev_bucket': ev_bucket,
                'fair_prob_a': fair_prob_a,
                'actual_a_wins': a_wins,
            })

matchups_df = pd.DataFrame(matchups)
print(f"Total 2025-2026 matchups generated: {len(matchups_df):,}")

# Market model: -110 = 52.38% to break even
MARKET_PROB = 110 / (110 + 100)  # 0.5238
print(f"\nMarket baseline: -110 (implied {MARKET_PROB:.1%})")

# Identify +EV opportunities (where our fair > market prob)
matchups_df['is_plus_ev'] = matchups_df['fair_prob_a'] > MARKET_PROB

# Simulate flat $100 bets
BET_SIZE = 100
matchups_df['bet_outcome'] = matchups_df['actual_a_wins'] * BET_SIZE - ~matchups_df['actual_a_wins'] * BET_SIZE

print("\n=== BACKTEST RESULTS (2025-2026) ===")
print(f"Total matchups: {len(matchups_df):,}")

# Overall stats
plus_ev_matches = matchups_df[matchups_df['is_plus_ev']]
print(f"Matchups with +EV: {len(plus_ev_matches):,} ({len(plus_ev_matches)/len(matchups_df)*100:.1f}%)")

if len(plus_ev_matches) > 0:
    win_rate_plus_ev = plus_ev_matches['actual_a_wins'].mean()
    roi_plus_ev = plus_ev_matches['bet_outcome'].sum() / (len(plus_ev_matches) * BET_SIZE)
    cumulative_pl = plus_ev_matches['bet_outcome'].sum()

    print(f"\nOn +EV bets only:")
    print(f"  Win rate: {win_rate_plus_ev:.1%}")
    print(f"  ROI: {roi_plus_ev:.1%} (${cumulative_pl:+.0f} on ${len(plus_ev_matches)*BET_SIZE:,.0f} wagered)")

    # By sample quality tier (game theory lens)
    print(f"\n=== GAME THEORY: BY SAMPLE QUALITY ===")

    for tier in ['WEAK', 'MEDIUM', 'STRONG']:
        tier_data = plus_ev_matches[plus_ev_matches['tier_a'] == tier]
        if len(tier_data) > 0:
            win_rate = tier_data['actual_a_wins'].mean()
            roi = tier_data['bet_outcome'].sum() / (len(tier_data) * BET_SIZE)
            pl = tier_data['bet_outcome'].sum()

            print(f"\n{tier} sample players (N={tier_data['sample_n_a'].mean():.0f} avg):")
            print(f"  Matchups: {len(tier_data):,}")
            print(f"  Win rate: {win_rate:.1%}")
            print(f"  ROI: {roi:.1%}")
            print(f"  P&L: ${pl:+.0f}")

    # By EV magnitude
    print(f"\n=== BY EV MAGNITUDE ===")

    # Bucket by relative EV size
    plus_ev_matches_copy = plus_ev_matches.copy()
    plus_ev_matches_copy['ev_magnitude'] = plus_ev_matches_copy['relative_ev'].abs()
    plus_ev_matches_copy['ev_size_bucket'] = pd.cut(
        plus_ev_matches_copy['ev_magnitude'],
        bins=[0, 0.5, 1.0, 2.0, 100],
        labels=['Small (0-0.5)', 'Medium (0.5-1.0)', 'Large (1.0-2.0)', 'XLarge (2.0+)']
    )

    for bucket in ['Small (0-0.5)', 'Medium (0.5-1.0)', 'Large (1.0-2.0)', 'XLarge (2.0+)']:
        bucket_data = plus_ev_matches_copy[plus_ev_matches_copy['ev_size_bucket'] == bucket]
        if len(bucket_data) > 0:
            win_rate = bucket_data['actual_a_wins'].mean()
            roi = bucket_data['bet_outcome'].sum() / (len(bucket_data) * BET_SIZE)

            print(f"{bucket}: {len(bucket_data):,} bets, {win_rate:.1%} win rate, {roi:.1%} ROI")

    # Cumulative P&L chart
    print(f"\n=== CUMULATIVE P&L (Top 20 Matchups) ===")
    sample_matches = plus_ev_matches.head(20).copy()
    sample_matches['cumulative_pl'] = sample_matches['bet_outcome'].cumsum()
    for idx, row in sample_matches.iterrows():
        print(f"  Match {idx+1}: {row['player_a']:20s} vs {row['player_b']:20s} | PL: ${row['cumulative_pl']:+7.0f}")

    # Game theory insights
    print(f"\n=== GAME THEORY INSIGHTS ===")

    # Where is the market most inefficient?
    weak_roi = plus_ev_matches[plus_ev_matches['tier_a'] == 'WEAK']['bet_outcome'].sum() / \
              (len(plus_ev_matches[plus_ev_matches['tier_a'] == 'WEAK']) * BET_SIZE) \
              if len(plus_ev_matches[plus_ev_matches['tier_a'] == 'WEAK']) > 0 else 0

    strong_roi = plus_ev_matches[plus_ev_matches['tier_a'] == 'STRONG']['bet_outcome'].sum() / \
                (len(plus_ev_matches[plus_ev_matches['tier_a'] == 'STRONG']) * BET_SIZE) \
                if len(plus_ev_matches[plus_ev_matches['tier_a'] == 'STRONG']) > 0 else 0

    print(f"Weak-sample edge ROI: {weak_roi:.1%}")
    print(f"Strong-sample edge ROI: {strong_roi:.1%}")
    print(f"Efficiency gap: {(weak_roi - strong_roi):.1%}")
    efficiency_gap_direction = int(np.sign(weak_roi - strong_roi) + 1)
    interpretations = ['less efficient on strong samples', 'equally efficient', 'less efficient on weak samples']
    print(f"\nInterpretation: Market is {interpretations[efficiency_gap_direction]}")

else:
    print("\nNo +EV opportunities found in 2025-2026 data")

# Save detailed results
matchups_df.to_csv('backtest_results_2025_2026.csv', index=False)
print(f"\nDetailed results saved to backtest_results_2025_2026.csv")
