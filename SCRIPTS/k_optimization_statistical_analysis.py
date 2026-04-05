"""
K-Optimization: Statistical Sensitivity Analysis
Without match outcomes, we analyze how k values affect adj_his_par distribution.

IMPORTANT: This is statistical analysis only, NOT prediction validation.
Future work: When match outcomes are available, use Option A (actual backtesting).
"""

import pandas as pd
import numpy as np
from scipy import stats
import json
from datetime import datetime

# Google Sheets API setup (assumes you have service account credentials)
# For now, assuming you'll export ANALYSIS v3 as CSV
# To use API: from google.oauth2.service_account import Credentials

class KOptimizationAnalyzer:
    def __init__(self, analysis_csv_path, tour_stats_csv_path=None):
        """Load ANALYSIS v3 data and TOUR_STATS"""
        self.df = pd.read_csv(analysis_csv_path)
        # Ensure year is numeric
        self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')

        # Load TOUR_STATS if provided, else create mock data
        if tour_stats_csv_path:
            self.tour_stats = pd.read_csv(tour_stats_csv_path)
        else:
            # Mock TOUR_STATS (you'll need to export the real one)
            self.tour_stats = pd.DataFrame({
                'Condition': ['Calm', 'Moderate', 'Tough'],
                'Tour_Avg_OffPar': [0.5, -0.5, -1.0]  # Default estimates
            })

        # Join tour stats to main dataframe
        self.df = self.df.merge(
            self.tour_stats,
            left_on='condition',
            right_on='Condition',
            how='left'
        )

        self.results = {}

    def filter_data(self):
        """Split into training (2022-2024) and test (2025-2026)"""
        # Assuming 'year' column exists in ANALYSIS
        self.train = self.df[self.df['year'].isin([2022, 2023, 2024])].copy()
        self.test = self.df[self.df['year'].isin([2025, 2026])].copy()

        print(f"Training data: {len(self.train)} rows (2022-2024)")
        print(f"Test data: {len(self.test)} rows (2025-2026)")

    def calculate_adj_his_par(self, data, player_hist_par, player_his_cnt, tour_avg, k):
        """
        Recalculate adj_his_par for given k value.
        Formula: (player_hist_par * player_his_cnt + tour_avg * k) / (player_his_cnt + k)
        """
        # Handle divisions by zero / null values
        denominator = player_his_cnt + k
        result = np.where(
            denominator > 0,
            (player_hist_par * player_his_cnt + tour_avg * k) / denominator,
            np.nan
        )
        return result

    def analyze_k_value(self, k, test_data=True):
        """Analyze statistical properties for a specific k value"""
        data = self.test if test_data else self.train

        # Calculate adj_his_par with this k
        # Columns: player_hist_par (AA), player_his_cnt (AB), Tour_Avg_OffPar (from TOUR_STATS merge)
        adj_his_par = self.calculate_adj_his_par(
            data,
            data['player_hist_par'].values,
            data['player_his_cnt'].values,
            data['Tour_Avg_OffPar'].fillna(0).values,  # Use merged tour stats, default to 0 if missing
            k
        )

        # Filter valid values (non-NaN, non-null off_par)
        valid_vals = adj_his_par[~np.isnan(adj_his_par)]

        if len(valid_vals) == 0:
            return None

        # Calculate statistics
        stats_dict = {
            'k': k,
            'n_samples': len(valid_vals),
            'mean': float(np.mean(valid_vals)),
            'std': float(np.std(valid_vals)),
            'variance': float(np.var(valid_vals)),
            'min': float(np.min(valid_vals)),
            'max': float(np.max(valid_vals)),
            'median': float(np.median(valid_vals)),
            'q25': float(np.percentile(valid_vals, 25)),
            'q75': float(np.percentile(valid_vals, 75)),
            'skewness': float(stats.skew(valid_vals)),
            'kurtosis': float(stats.kurtosis(valid_vals)),
            'range': float(np.max(valid_vals) - np.min(valid_vals))
        }

        return stats_dict

    def optimize(self, k_range=range(10, 101, 5)):
        """Test k values and analyze sensitivity"""
        print(f"\n{'='*70}")
        print("K-VALUE STATISTICAL SENSITIVITY ANALYSIS")
        print(f"{'='*70}\n")

        test_results = []
        train_results = []

        for k in k_range:
            # Analyze on test data (2025-2026)
            test_stats = self.analyze_k_value(k, test_data=True)
            if test_stats:
                test_results.append(test_stats)
                print(f"K={k:3d} | Mean={test_stats['mean']:7.3f} | Std={test_stats['std']:6.3f} | "
                      f"Skew={test_stats['skewness']:6.3f} | Range={test_stats['range']:8.2f}")

            # Also analyze on train data for reference
            train_stats = self.analyze_k_value(k, test_data=False)
            if train_stats:
                train_results.append(train_stats)

        self.test_results_df = pd.DataFrame(test_results)
        self.train_results_df = pd.DataFrame(train_results)

        return test_results, train_results

    def report(self, output_file='k_optimization_report.json'):
        """Generate audit report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'methodology': 'Statistical Sensitivity Analysis (No Match Outcomes)',
            'disclaimer': 'This analysis shows distribution changes across k values. '
                         'It does NOT validate prediction accuracy without match outcomes.',
            'future_optimization': 'When match outcomes are available (2025-2026), '
                                  'use Option A: Backtest each k against actual results.',
            'training_period': '2022-2024',
            'test_period': '2025-2026',
            'training_n': len(self.train),
            'test_n': len(self.test),
            'k_range': list(self.test_results_df['k'].astype(int)),
            'test_results': self.test_results_df.to_dict('records'),
            'summary': {
                'k_with_min_variance': int(self.test_results_df.loc[self.test_results_df['variance'].idxmin(), 'k']),
                'k_with_max_range': int(self.test_results_df.loc[self.test_results_df['range'].idxmax(), 'k']),
                'k_with_min_skew': int(self.test_results_df.loc[self.test_results_df['skewness'].abs().idxmin(), 'k']),
            }
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*70}")
        print("REPORT SAVED")
        print(f"{'='*70}")
        print(f"File: {output_file}")
        print(f"\nSUMMARY:")
        print(f"  K with minimum variance: {report['summary']['k_with_min_variance']}")
        print(f"  K with maximum range: {report['summary']['k_with_max_range']}")
        print(f"  K with minimum skewness: {report['summary']['k_with_min_skew']}")
        print(f"\nIMPORTANT: These are statistical properties, not predictive metrics.")
        print(f"Recommendation: Choose k based on:")
        print(f"  1. Variance (lower = more stable shrinkage)")
        print(f"  2. Skewness (closer to 0 = more normal distribution)")
        print(f"  3. Domain intuition about player par variance")


if __name__ == "__main__":
    # Load data (export ANALYSIS v3 as CSV first)
    try:
        analyzer = KOptimizationAnalyzer(
            'ANALYSIS_v3_export.csv',
            'TOUR_STATS_export.csv'  # Optional: export TOUR_STATS as CSV too
        )
        print(f"\nLoaded ANALYSIS with columns: {list(analyzer.df.columns)[:20]}...")

        analyzer.filter_data()
        test_results, train_results = analyzer.optimize()
        analyzer.report()
        print("\n✓ Analysis complete!")
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you've exported:")
        print("  1. ANALYSIS sheet → ANALYSIS_v3_export.csv")
        print("  2. TOUR_STATS sheet → TOUR_STATS_export.csv (optional)")
    except KeyError as e:
        print(f"\n✗ Column not found: {e}")
        print(f"\nAvailable columns: {list(analyzer.df.columns)}")
        print("\nCommon column names expected:")
        print("  - 'year' or 'Year'")
        print("  - 'condition' or 'Condition'")
        print("  - 'player_hist_par' or similar")
        print("  - 'player_his_cnt' or similar")
