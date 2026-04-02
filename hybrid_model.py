import pandas as pd
import numpy as np
from scipy.optimize import minimize
from player_scoring_system_v2 import PlayerScorerV2

scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)
matchups = pd.read_csv('texas_childrens_round4_3ball.csv')
analysis = pd.read_csv('analysis_v2_with_element.csv')

def american_to_implied(odds):
    odds = float(odds)
    return abs(odds) / (abs(odds) + 100) if odds < 0 else 100 / (odds + 100)

def round_to_bucket(value):
    if pd.isna(value):
        return 50
    try:
        v = int(float(value))
        return min([0, 25, 50, 75], key=lambda x: abs(x - v))
    except:
        return 50

print("BUILDING HYBRID MODEL (Par + Model Scores)")
print("=" * 80)
print()

training_data = []

for idx, row in matchups.iterrows():
    players = [row['Player [A]'], row['Player [B]'], row['Player [C]']]
    ml_odds = [row['ML [A]'], row['ML [B]'], row['ML [C]']]
    condition, round_type = row['Condition'], row['Round Type']
    
    # Market probs
    impl = [american_to_implied(ml) for ml in ml_odds]
    impl_norm = [p / sum(impl) for p in impl]
    
    # Model scores
    player_dicts = [
        {'name': row['Player [A]'], 'condition': condition, 'round_type': round_type,
         'color': row['Color [A]'], 'element': row['Element [A]'],
         'exec_bucket': round_to_bucket(row['Exec [A]']), 'upside_bucket': round_to_bucket(row['Upside [A]']),
         'chinese_zodiac': row['Zodiac [A]']},
        {'name': row['Player [B]'], 'condition': condition, 'round_type': round_type,
         'color': row['Color [B]'], 'element': row['Element [B]'],
         'exec_bucket': round_to_bucket(row['Exec [B]']), 'upside_bucket': round_to_bucket(row['Upside [B]']),
         'chinese_zodiac': row['Zodiac [B]']},
        {'name': row['Player [C]'], 'condition': condition, 'round_type': round_type,
         'color': row['Color [C]'], 'element': row['Element [C]'],
         'exec_bucket': round_to_bucket(row['Exec [C]']), 'upside_bucket': round_to_bucket(row['Upside [C]']),
         'chinese_zodiac': row['Zodiac [C]']}
    ]
    
    try:
        scores = [scorer.score_player(pd) for pd in player_dicts]
        model_scores = [s['final_score'] / 100 if s['final_score'] > 1 else s['final_score'] for s in scores]
        
        # Par scores
        par_scores = []
        for player in players:
            match = analysis[(analysis['player_name'] == player) & (analysis['condition'] == condition) & (analysis['round_type'] == round_type)]
            par_scores.append(match.iloc[0]['Adj_his_par'] if len(match) > 0 else None)
        
        if None not in par_scores:
            par_normalized = [-p for p in par_scores]
            par_sum = sum(par_normalized)
            par_probs = [p / par_sum for p in par_normalized]
            
            for i in range(3):
                training_data.append({'model_score': model_scores[i], 'par_prob': par_probs[i], 'market_prob': impl_norm[i]})
    except:
        pass

print(f"Collected {len(training_data)} player-level data points\n")

def hybrid_loss(weights):
    w1, w2 = weights
    w3 = 1.0 - w1 - w2
    total_error = sum((w1 * dp['model_score'] + w2 * dp['par_prob'] + w3 * (1/3) - dp['market_prob']) ** 2 for dp in training_data)
    return total_error

result = minimize(hybrid_loss, [0.5, 0.3], bounds=[(0, 1), (0, 1)], method='L-BFGS-B')
w1_opt, w2_opt = result.x
w3_opt = 1.0 - w1_opt - w2_opt

print(f"OPTIMAL WEIGHTS:")
print(f"  Model Score Weight:    {w1_opt:.3f}")
print(f"  Par Probability Weight: {w2_opt:.3f}")
print(f"  Baseline Weight:        {w3_opt:.3f}")
print(f"  MSE: {result.fun:.6f}\n")

rmse = np.sqrt(result.fun / len(training_data))
print(f"RMSE: {rmse:.3f} ({rmse*100:.1f}pp)\n")
