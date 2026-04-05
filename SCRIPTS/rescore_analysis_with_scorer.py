"""
Rescore ANALYSIS data using Manual Analysis scoring lookup table.
Adds predicted scores for each player-round combo.
"""

import pandas as pd
import numpy as np

# Load the ANALYSIS data and scorer
analysis = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
scorer = pd.read_csv('Golf Historics v3 - Manual Anlysis.csv', low_memory=False)

print("=" * 100)
print("RESCORING ANALYSIS DATA WITH MANUAL SCORER")
print("=" * 100)
print(f"\nANALYSIS rows: {len(analysis)}")
print(f"SCORER rows: {len(scorer)}")

# Clean scorer: remove duplicate header columns (right side of table)
scorer_clean = scorer.iloc[:, :11].copy()  # Keep only: Color, Exec/Upside, bucket, Condition, RoundType, -2, 2, Win Ratio, Adj Win Ratio, %Score, Score
scorer_clean.columns = ['Color', 'Exec_Upside', 'Bucket', 'Condition', 'RoundType', 'Col_-2', 'Col_2', 'Win_Ratio', 'Adj_Win_Ratio', 'Percent_Score', 'Score']

print(f"\nSCORER columns: {scorer_clean.columns.tolist()}")

# Function to bucket a value
def get_bucket(value):
    if pd.isna(value):
        return None
    if value < 25:
        return '0-25'
    elif value < 50:
        return '25-50'
    elif value < 75:
        return '50-75'
    else:
        return '75-100'

# Add lookup columns to ANALYSIS
analysis['exec_bucket'] = analysis['exec'].apply(get_bucket)
analysis['upside_bucket'] = analysis['upside'].apply(get_bucket)

# Create lookup keys
analysis['exec_lookup_key'] = (
    analysis['color'].astype(str) + '|' +
    'Exec' + '|' +
    analysis['exec_bucket'].astype(str) + '|' +
    analysis['condition'].astype(str) + '|' +
    analysis['round_type'].astype(str)
)

analysis['upside_lookup_key'] = (
    analysis['color'].astype(str) + '|' +
    'Upside' + '|' +
    analysis['upside_bucket'].astype(str) + '|' +
    analysis['condition'].astype(str) + '|' +
    analysis['round_type'].astype(str)
)

# Create scorer lookup dictionary (using Exec)
scorer_clean['lookup_key'] = (
    scorer_clean['Color'].astype(str) + '|' +
    scorer_clean['Exec_Upside'].astype(str) + '|' +
    scorer_clean['Bucket'].astype(str) + '|' +
    scorer_clean['Condition'].astype(str) + '|' +
    scorer_clean['RoundType'].astype(str)
)

scorer_dict = {}
for _, row in scorer_clean.iterrows():
    key = row['lookup_key']
    scorer_dict[key] = {
        'win_ratio': row['Win_Ratio'],
        'adj_win_ratio': row['Adj_Win_Ratio'],
        'percent_score': row['Percent_Score'],
        'score': row['Score']
    }

print(f"Scorer lookup table size: {len(scorer_dict)} combinations")

# Lookup function
def lookup_score(lookup_key):
    if lookup_key in scorer_dict:
        return scorer_dict[lookup_key]
    return None

# Apply scoring
print("\nLooking up scores...")
analysis['predicted_exec_score'] = analysis['exec_lookup_key'].apply(
    lambda k: lookup_score(k)['score'] if lookup_score(k) else np.nan
)
analysis['predicted_exec_win_ratio'] = analysis['exec_lookup_key'].apply(
    lambda k: lookup_score(k)['win_ratio'] if lookup_score(k) else np.nan
)
analysis['predicted_upside_score'] = analysis['upside_lookup_key'].apply(
    lambda k: lookup_score(k)['score'] if lookup_score(k) else np.nan
)

# Count matches
exec_matches = analysis['predicted_exec_score'].notna().sum()
upside_matches = analysis['predicted_upside_score'].notna().sum()

print(f"Exec score matches: {exec_matches} / {len(analysis)} ({exec_matches/len(analysis)*100:.1f}%)")
print(f"Upside score matches: {upside_matches} / {len(analysis)} ({upside_matches/len(analysis)*100:.1f}%)")

# For analysis, use Exec-based scoring as primary
analysis['predicted_score'] = analysis['predicted_exec_score']
analysis['predicted_win_ratio'] = analysis['predicted_exec_win_ratio']

# Calculate error between predicted and actual performance
analysis['actual_win'] = (analysis['vs_avg'] > 0).astype(int)
analysis['score_difference'] = analysis['vs_avg'] - analysis['predicted_score']

# Summary statistics
print(f"\n{'=' * 100}")
print("SCORING ACCURACY")
print(f"{'=' * 100}")

valid_pred = analysis[analysis['predicted_score'].notna()].copy()

if len(valid_pred) > 0:
    mae = (valid_pred['score_difference'].abs()).mean()
    rmse = np.sqrt((valid_pred['score_difference'] ** 2).mean())

    print(f"\nPrediction Error:")
    print(f"  Mean Absolute Error: {mae:.3f}")
    print(f"  RMSE: {rmse:.3f}")
    print(f"  Mean predicted: {valid_pred['predicted_score'].mean():.3f}")
    print(f"  Mean actual: {valid_pred['vs_avg'].mean():.3f}")

    # By condition
    print(f"\nError by Condition:")
    for cond in ['Calm', 'Moderate', 'Tough']:
        cond_data = valid_pred[valid_pred['condition'] == cond]
        if len(cond_data) > 0:
            cond_mae = (cond_data['score_difference'].abs()).mean()
            print(f"  {cond}: MAE={cond_mae:.3f} (n={len(cond_data)})")

    # By round type
    print(f"\nError by Round Type:")
    for rt in ['Open', 'Positioning', 'Survival', 'Closing']:
        rt_data = valid_pred[valid_pred['round_type'] == rt]
        if len(rt_data) > 0:
            rt_mae = (rt_data['score_difference'].abs()).mean()
            print(f"  {rt}: MAE={rt_mae:.3f} (n={len(rt_data)})")

# Save rescored data
output_file = 'ANALYSIS_v3_RESCORED.csv'
cols_to_keep = list(analysis.columns[:33]) + [
    'predicted_score', 'predicted_win_ratio', 'score_difference', 'actual_win',
    'exec_bucket', 'upside_bucket'
]
cols_to_keep = [c for c in cols_to_keep if c in analysis.columns]

analysis[cols_to_keep].to_csv(output_file, index=False)
print(f"\n[DONE] Rescored data saved to: {output_file}")
print(f"  Original columns: 33")
print(f"  New columns: predicted_score, predicted_win_ratio, score_difference, actual_win, exec_bucket, upside_bucket")
