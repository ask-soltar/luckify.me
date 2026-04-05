"""
K-Optimization: Leave-One-Out Cross-Validation
Tests each k value by predicting held-out rounds using other rounds from same player-condition.

This is statistically valid WITHOUT match outcomes.
Measures: Can k predict player's actual off_par performance?
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class KOptimizationLOOCV:
    def __init__(self, analysis_csv_path):
        """Load ANALYSIS v3 data"""
        self.df = pd.read_csv(analysis_csv_path)
        # Ensure year is numeric
        self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')

        print(f"Loaded {len(self.df)} rows from ANALYSIS v3")
        print(f"Columns: {list(self.df.columns)[:10]}...\n")

    def filter_training_data(self):
        """Use 2022-2024 for training"""
        self.train = self.df[self.df['year'].isin([2022, 2023, 2024])].copy()
        self.train = self.train.dropna(subset=['player_hist_par', 'player_his_cnt', 'condition', 'off_par'])
        self.train = self.train[self.train['off_par'] != ""]
        self.train['off_par'] = pd.to_numeric(self.train['off_par'], errors='coerce')
        self.train = self.train.dropna(subset=['off_par'])

        print(f"Training data: {len(self.train)} rounds (2022-2024)")
        print(f"Conditions breakdown:")
        print(self.train['condition'].value_counts())

    def calculate_adj_his_par(self, player_hist_par, player_his_cnt, tour_avg, k):
        """
        Shrinkage formula: (player_hist_par * player_his_cnt + tour_avg * k) / (player_his_cnt + k)
        """
        denominator = player_his_cnt + k
        if denominator <= 0:
            return np.nan
        return (player_hist_par * player_his_cnt + tour_avg * k) / denominator

    def leave_one_out_cv(self, k, tour_stats_dict):
        """
        Leave-One-Out Cross-Validation for a specific k value.
        For each player-condition: remove one round, predict using others, compare vs actual off_par.
        """
        errors = []
        predictions = []
        actuals = []

        # Group by player and condition
        for (player, condition), group in self.train.groupby(['player_name', 'condition']):
            if len(group) < 2:  # Need at least 2 rounds to do LOO
                continue

            tour_avg = tour_stats_dict.get(condition, 0)  # Default to 0 if not found

            # Leave-One-Out: iterate through each round
            for idx, test_row in group.iterrows():
                # Get training rows (all except this one)
                train_rows = group.drop(idx)

                # Calculate player avg from training rounds
                player_hist_par = train_rows['off_par'].mean()
                player_hist_cnt = len(train_rows)

                # Predict using shrinkage formula
                predicted_adj_par = self.calculate_adj_his_par(
                    player_hist_par, player_hist_cnt, tour_avg, k
                )

                # Compare to actual
                actual_off_par = test_row['off_par']

                if not np.isnan(predicted_adj_par) and not np.isnan(actual_off_par):
                    error = abs(predicted_adj_par - actual_off_par)
                    errors.append(error)
                    predictions.append(predicted_adj_par)
                    actuals.append(actual_off_par)

        if len(errors) == 0:
            return None

        # Calculate metrics
        mae = np.mean(errors)
        rmse = np.sqrt(np.mean(np.array(errors) ** 2))
        median_error = np.median(errors)

        return {
            'k': k,
            'n_predictions': len(errors),
            'mae': float(mae),
            'rmse': float(rmse),
            'median_error': float(median_error),
            'min_error': float(np.min(errors)),
            'max_error': float(np.max(errors)),
            'std_error': float(np.std(errors))
        }

    def build_tour_stats(self):
        """Calculate tour average off_par by condition from training data"""
        tour_stats = {}
        for condition in self.train['condition'].unique():
            condition_data = self.train[self.train['condition'] == condition]
            avg_off_par = condition_data['off_par'].mean()
            tour_stats[condition] = avg_off_par
            print(f"  {condition}: avg off_par = {avg_off_par:.3f}")

        return tour_stats

    def optimize(self, k_range=None):
        """Test all k values with LOO CV"""
        if k_range is None:
            # Test lower values: 0.5, 1, 2, 3, 5, 7.5, 10, 15, 20, 30, 50, 100
            k_range = [0.5, 1, 2, 3, 5, 7.5, 10, 15, 20, 30, 50, 75, 100]

        print(f"\n{'='*80}")
        print("LEAVE-ONE-OUT CROSS-VALIDATION (LOO CV)")
        print(f"{'='*80}\n")

        print("Building tour statistics from training data...")
        tour_stats = self.build_tour_stats()

        print(f"\nRunning LOO CV for k values {min(k_range)}-{max(k_range)}...\n")

        results = []
        for k in k_range:
            result = self.leave_one_out_cv(k, tour_stats)
            if result:
                results.append(result)
                # Format k value (handle floats like 7.5)
                k_str = f"{k:.1f}" if isinstance(k, float) and k % 1 != 0 else f"{int(k)}"
                print(f"K={k_str:>5} | MAE={result['mae']:.4f} | RMSE={result['rmse']:.4f} | "
                      f"n={result['n_predictions']:5d} | Median={result['median_error']:.4f}")

        self.results_df = pd.DataFrame(results)
        return results

    def report(self, output_file='k_optimization_loocv_report.json'):
        """Generate comprehensive report"""
        best_mae_idx = self.results_df['mae'].idxmin()
        best_rmse_idx = self.results_df['rmse'].idxmin()
        best_median_idx = self.results_df['median_error'].idxmin()

        best_mae_k = int(self.results_df.loc[best_mae_idx, 'k'])
        best_rmse_k = int(self.results_df.loc[best_rmse_idx, 'k'])
        best_median_k = int(self.results_df.loc[best_median_idx, 'k'])

        report = {
            'timestamp': datetime.now().isoformat(),
            'methodology': 'Leave-One-Out Cross-Validation',
            'description': 'For each player-condition, removes one round and predicts using others. '
                          'Measures prediction error across all k values.',
            'training_period': '2022-2024',
            'k_range': list(self.results_df['k'].astype(int)),
            'results': self.results_df.to_dict('records'),
            'best_k_by_mae': best_mae_k,
            'best_mae_value': float(self.results_df.loc[best_mae_idx, 'mae']),
            'best_k_by_rmse': best_rmse_k,
            'best_rmse_value': float(self.results_df.loc[best_rmse_idx, 'rmse']),
            'best_k_by_median': best_median_k,
            'best_median_value': float(self.results_df.loc[best_median_idx, 'median_error']),
            'recommendation': f'Use K={best_mae_k} (minimizes Mean Absolute Error)'
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*80}")
        print("RESULTS")
        print(f"{'='*80}\n")

        print(f"Best K by Mean Absolute Error (MAE): K={best_mae_k} (MAE={self.results_df.loc[best_mae_idx, 'mae']:.4f})")
        print(f"Best K by RMSE:                       K={best_rmse_k} (RMSE={self.results_df.loc[best_rmse_idx, 'rmse']:.4f})")
        print(f"Best K by Median Error:               K={best_median_k} (Median={self.results_df.loc[best_median_idx, 'median_error']:.4f})")

        print(f"\n{'='*80}")
        print(f"RECOMMENDATION: Use K={best_mae_k}")
        print(f"{'='*80}\n")

        print(f"Current setting: K=50")
        current_mae = self.results_df[self.results_df['k'] == 50]['mae'].values
        if len(current_mae) > 0:
            improvement = ((current_mae[0] - self.results_df.loc[best_mae_idx, 'mae']) / current_mae[0] * 100)
            print(f"Improvement over K=50: {improvement:.1f}% error reduction\n")

        print(f"Report saved to: {output_file}")


if __name__ == "__main__":
    try:
        analyzer = KOptimizationLOOCV('ANALYSIS_v3_export.csv')
        analyzer.filter_training_data()
        results = analyzer.optimize()
        analyzer.report()
        print("\n✓ LOO CV analysis complete!")

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV:")
        print("  Google Sheets → ANALYSIS sheet → File → Download → CSV")
        print("  Save as: ANALYSIS_v3_export.csv in d:\\Projects\\luckify-me\\")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
