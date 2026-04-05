"""
3-Ball P&L Validation with Moneyline
Calculates profit/loss based on ML odds
Win: profit = ML value
Loss: profit = -100
2-way push: profit = ML / 2
3-way push: profit = 0
"""

import pandas as pd
import re

# Load scored matchups
scored_file = 'matchup3b_scored_3ball.csv'
df_scored = pd.read_csv(scored_file)
print(f"Loaded: {scored_file}")

# Load original data with ML
matchup_file = 'matchup3b.csv'
df_matchup = pd.read_csv(matchup_file, sep='\t' if '\t' in open(matchup_file).readline() else ',')
df_matchup.columns = df_matchup.columns.str.strip()
print(f"Loaded: {matchup_file}")

# Merge scored with ML data
df_scored = df_scored.merge(
    df_matchup[['Player A', 'Player B', 'Player C', 'Winner', 'ML A', 'ML B', 'ML C']],
    left_on=['player_a', 'player_b', 'player_c'],
    right_on=['Player A', 'Player B', 'Player C'],
    how='left'
)

print(f"\nMatched: {df_scored['ML A'].notna().sum()} / {len(df_scored)}\n")

# Map best player letter to name and ML
def get_best_player_info(row):
    player_map = {'A': row['player_a'], 'B': row['player_b'], 'C': row['player_c']}
    ml_map = {'A': row['ML A'], 'B': row['ML B'], 'C': row['ML C']}
    best_letter = row['best_player']
    return {
        'name': player_map.get(best_letter),
        'ml': ml_map.get(best_letter)
    }

# Calculate P&L
results = []

for _, row in df_scored.iterrows():
    best_info = get_best_player_info(row)
    predicted_player = best_info['name']
    predicted_ml = best_info['ml']

    rec = str(row['recommendation']).strip()

    # Skip logic
    if 'SKIP' in rec:
        result_type = 'SKIP'
        pl = 0
        continue

    # Parse moneyline (can be positive or negative)
    try:
        ml_value = float(predicted_ml)
    except:
        result_type = 'NO_ML'
        pl = 0
        continue

    # Convert ML to profit per $100 bet
    if ml_value >= 0:
        # Positive ML: +150 means $150 profit on $100 bet
        ml_profit_factor = ml_value / 100
    else:
        # Negative ML: -150 means you need $150 to win $100
        ml_profit_factor = 100 / abs(ml_value)

    # Determine result and P&L
    if row['is_push']:
        if row['push_type'] == '2-way':
            # 2-way push: check if predicted player was in the push
            winner_raw = str(row['winner_raw']).strip()
            match = re.search(r'Push\s*\(\s*(.+?)\s*/\s*(.+?)\s*\)', winner_raw)
            if match:
                push_player_1 = match.group(1).strip()
                push_player_2 = match.group(2).strip()

                if predicted_player == push_player_1 or predicted_player == push_player_2:
                    # Half win: ML / 2
                    pl = (ml_profit_factor * 100) / 2
                    result_type = '2WAY_PUSH_WIN'
                else:
                    # Loss
                    pl = -100
                    result_type = '2WAY_PUSH_LOSS'
            else:
                result_type = 'UNKNOWN'
                pl = 0
        else:
            # 3-way push
            pl = 0
            result_type = '3WAY_PUSH'
    else:
        # Clear winner
        if predicted_player == row['actual_winner']:
            pl = ml_profit_factor * 100
            result_type = 'WIN'
        else:
            pl = -100
            result_type = 'LOSS'

    results.append({
        'player_a': row['player_a'],
        'player_b': row['player_b'],
        'player_c': row['player_c'],
        'prediction': predicted_player,
        'predicted_ml': predicted_ml,
        'actual_winner': row['actual_winner'],
        'is_push': row['is_push'],
        'recommendation': rec,
        'edge': row['best_vs_second'],
        'result_type': result_type,
        'pl': pl
    })

df_results = pd.DataFrame(results)

# Analysis
print("="*140)
print("3-BALL P&L ANALYSIS (with Moneyline)")
print("="*140)

# Total P&L
graded = df_results[~df_results['result_type'].isin(['SKIP', 'NO_ML', 'UNKNOWN', '3WAY_PUSH'])]

if len(graded) > 0:
    total_pl = graded['pl'].sum()
    win_count = len(graded[graded['result_type'] == 'WIN'])
    loss_count = len(graded[graded['result_type'] == 'LOSS'])
    push_count = len(graded[graded['result_type'] == '2WAY_PUSH_WIN'])
    push_loss = len(graded[graded['result_type'] == '2WAY_PUSH_LOSS'])

    print(f"\nTotal graded: {len(graded)}")
    print(f"  Wins: {win_count}")
    print(f"  Losses: {loss_count}")
    print(f"  2-way push (won): {push_count}")
    print(f"  2-way push (lost): {push_loss}")

    print(f"\nTotal P&L: ${total_pl:,.2f}")
    print(f"Average bet: ${total_pl / len(graded):,.2f}")
    print(f"ROI: {(total_pl / len(graded)) / 100 * 100:.1f}%")

    # By signal strength
    print(f"\n" + "="*140)
    print("P&L BY SIGNAL STRENGTH")
    print("="*140)

    for signal in ['STRONG', 'MODERATE', 'SLIGHT']:
        signal_data = graded[graded['recommendation'].str.contains(signal, na=False)]
        if len(signal_data) > 0:
            signal_pl = signal_data['pl'].sum()
            signal_avg = signal_pl / len(signal_data)
            print(f"\n{signal}:")
            print(f"  Bets: {len(signal_data)}")
            print(f"  Total P&L: ${signal_pl:,.2f}")
            print(f"  Per bet: ${signal_avg:,.2f}")
            print(f"  Win%: {len(signal_data[signal_data['result_type'].isin(['WIN', '2WAY_PUSH_WIN'])]) / len(signal_data) * 100:.1f}%")

# Save results
output_file = scored_file.replace('.csv', '_with_pl.csv')
df_results.to_csv(output_file, index=False)
print(f"\n[OK] P&L results saved to: {output_file}")
