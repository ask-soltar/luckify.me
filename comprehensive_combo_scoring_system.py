"""
Comprehensive Combo Scoring System
Builds complete scoring table with ALL combos (positive and negative edges).
Useful for: betting FOR positive combos, betting AGAINST negative combos.

Output: CSV with all combos ranked by signal strength (absolute edge).
"""

import pandas as pd
import numpy as np
from datetime import datetime

class ComboScoringSystem:
    def __init__(self, analysis_csv_path):
        """Load and filter ANALYSIS v3 data"""
        self.df = pd.read_csv(analysis_csv_path)
        print(f"Loaded {len(self.df)} total rows")

        # Filter for Tournament Type = S only
        self.df = self.df[self.df['tournament_type'] == 'S'].copy()
        print(f"After S filter: {len(self.df)} rows")

        # Ensure numeric columns
        self.df['off_par'] = pd.to_numeric(self.df['off_par'], errors='coerce')
        self.df['adj_his_par'] = pd.to_numeric(self.df['adj_his_par'], errors='coerce')
        self.df['exec'] = pd.to_numeric(self.df['exec'], errors='coerce')
        self.df['upside'] = pd.to_numeric(self.df['upside'], errors='coerce')
        self.df['gap'] = pd.to_numeric(self.df['gap'], errors='coerce')

        # Calculate model error (actual vs prediction)
        self.df['model_error'] = self.df['off_par'] - self.df['adj_his_par']

        self.df = self.df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', 'color'])
        print(f"After dropping NaNs: {len(self.df)} rows\n")

    def bucket_value(self, value, bucket_type='exec'):
        """Assign value to bucket"""
        if pd.isna(value):
            return None

        if bucket_type in ['exec', 'upside']:
            if value < 25:
                return '0-25'
            elif value < 50:
                return '25-50'
            elif value < 75:
                return '50-75'
            else:
                return '75-100'

        elif bucket_type == 'gap':
            if value >= 20:
                return '20+'
            elif value >= 10:
                return '10-20'
            elif value >= 0:
                return '0-10'
            elif value >= -10:
                return '-10-0'
            elif value >= -20:
                return '-20--10'
            else:
                return '<-20'

        return None

    def calculate_combo_stats(self, combo_data):
        """Calculate stats for a combo"""
        if len(combo_data) == 0:
            return None

        good = len(combo_data[combo_data['model_error'] <= -2.0])
        bad = len(combo_data[combo_data['model_error'] >= 2.0])
        total = len(combo_data)

        if total < 2:  # Allow any sample size for comprehensive scoring
            return None

        good_rate = good / total if total > 0 else 0
        bad_rate = bad / total if total > 0 else 0

        edge = (good_rate - bad_rate) * 100
        mean_error = combo_data['model_error'].mean()

        # Confidence level
        if total >= 30:
            confidence = 'HIGH'
        elif total >= 15:
            confidence = 'EXPLORATORY'
        else:
            confidence = 'WEAK'

        return {
            'n': total,
            'good': good,
            'bad': bad,
            'good_rate': good_rate * 100,
            'bad_rate': bad_rate * 100,
            'edge': edge,
            'mean_error': mean_error,
            'confidence': confidence
        }

    def get_exec_upside_pairs(self):
        """Define meaningful exec/upside pairs"""
        return [
            ('0-25', '0-25', 'Low'),
            ('25-50', '25-50', 'Mid-Low'),
            ('25-50', '50-75', 'Mid-Bal'),
            ('50-75', '25-50', 'Mid-Bal'),
            ('50-75', '50-75', 'Mid-High'),
            ('75-100', '75-100', 'High'),
            ('75-100', '50-75', 'High-Mix'),
            ('50-75', '75-100', 'High-Mix'),
        ]

    def build_scoring_table(self):
        """Build comprehensive scoring table"""
        all_combos = []

        # Layer 3: Round Type × Color × Exec/Upside (skip Gap for sample size)
        for condition in ['Calm', 'Moderate', 'Tough']:
            print(f"Building {condition}...")

            data = self.df[self.df['condition'] == condition].copy()

            # Add buckets
            data['exec_bucket'] = data['exec'].apply(lambda x: self.bucket_value(x, 'exec'))
            data['upside_bucket'] = data['upside'].apply(lambda x: self.bucket_value(x, 'upside'))

            round_types = data['round_type'].dropna().unique()
            colors = data['color'].dropna().unique()
            pairs = self.get_exec_upside_pairs()

            combo_count = 0

            for rt in round_types:
                if rt in ['REMOVE', 'Mixed', 'Elimination']:
                    continue

                for color in colors:
                    for exec_b, upside_b, pair_label in pairs:
                        combo_count += 1

                        mask = (
                            (data['round_type'] == rt) &
                            (data['color'] == color) &
                            (data['exec_bucket'] == exec_b) &
                            (data['upside_bucket'] == upside_b)
                        )

                        combo_data = data[mask]

                        if len(combo_data) == 0:
                            continue

                        stats = self.calculate_combo_stats(combo_data)
                        if stats is None:
                            continue

                        all_combos.append({
                            'condition': condition,
                            'round_type': rt,
                            'color': color,
                            'exec': exec_b,
                            'upside': upside_b,
                            'n': stats['n'],
                            'good': stats['good'],
                            'bad': stats['bad'],
                            'good_rate': stats['good_rate'],
                            'bad_rate': stats['bad_rate'],
                            'edge': stats['edge'],
                            'mean_error': stats['mean_error'],
                            'confidence': stats['confidence']
                        })

            print(f"  Tested {combo_count} theoretical combos, found {len([c for c in all_combos if c['condition'] == condition])}")

        return pd.DataFrame(all_combos)

    def build_scoring_table_with_gap(self):
        """Build scoring table including Gap buckets (smaller samples)"""
        all_combos = []

        for condition in ['Calm', 'Moderate', 'Tough']:
            print(f"Building {condition}...")

            data = self.df[self.df['condition'] == condition].copy()

            # Add buckets
            data['exec_bucket'] = data['exec'].apply(lambda x: self.bucket_value(x, 'exec'))
            data['upside_bucket'] = data['upside'].apply(lambda x: self.bucket_value(x, 'upside'))
            data['gap_bucket'] = data['gap'].apply(lambda x: self.bucket_value(x, 'gap'))

            round_types = data['round_type'].dropna().unique()
            colors = data['color'].dropna().unique()
            pairs = self.get_exec_upside_pairs()

            for rt in round_types:
                if rt in ['REMOVE', 'Mixed', 'Elimination']:
                    continue

                for color in colors:
                    for exec_b, upside_b, pair_label in pairs:
                        gap_buckets = data[
                            (data['round_type'] == rt) &
                            (data['color'] == color) &
                            (data['exec_bucket'] == exec_b) &
                            (data['upside_bucket'] == upside_b)
                        ]['gap_bucket'].dropna().unique()

                        for gap_b in gap_buckets:
                            mask = (
                                (data['round_type'] == rt) &
                                (data['color'] == color) &
                                (data['exec_bucket'] == exec_b) &
                                (data['upside_bucket'] == upside_b) &
                                (data['gap_bucket'] == gap_b)
                            )

                            combo_data = data[mask]

                            if len(combo_data) == 0:
                                continue

                            stats = self.calculate_combo_stats(combo_data)
                            if stats is None:
                                continue

                            all_combos.append({
                                'condition': condition,
                                'round_type': rt,
                                'color': color,
                                'exec': exec_b,
                                'upside': upside_b,
                                'gap': gap_b,
                                'n': stats['n'],
                                'good': stats['good'],
                                'bad': stats['bad'],
                                'good_rate': stats['good_rate'],
                                'bad_rate': stats['bad_rate'],
                                'edge': stats['edge'],
                                'mean_error': stats['mean_error'],
                                'confidence': stats['confidence']
                            })

        return pd.DataFrame(all_combos)

    def report(self, df_combos_layer3, df_combos_layer4, output_prefix='combo_scoring'):
        """Generate scoring tables"""

        print(f"\n{'='*100}")
        print("COMBO SCORING SYSTEM — LAYER 3 (Round × Color × Exec/Upside)")
        print(f"{'='*100}\n")

        # Sort by absolute edge (signal strength)
        df_combos_layer3_sorted = df_combos_layer3.reindex(
            df_combos_layer3['edge'].abs().sort_values(ascending=False).index
        )

        print(f"Total combos: {len(df_combos_layer3_sorted)}")
        print(f"Positive edges (bet FOR): {len(df_combos_layer3_sorted[df_combos_layer3_sorted['edge'] > 0])}")
        print(f"Negative edges (bet AGAINST): {len(df_combos_layer3_sorted[df_combos_layer3_sorted['edge'] < 0])}")

        print(f"\n{'Edge':>6} {'N':>4} {'Mean Err':>9} {'Good%':>6} {'Conf':>12} {'Round':<12} {'Color':<8} {'Exec/Upside':<15} {'Condition':<10}")
        print(f"{'-'*110}")

        for _, r in df_combos_layer3_sorted.head(50).iterrows():
            eu = f"{r['exec']}/{r['upside']}"
            sign = "+" if r['edge'] > 0 else ""
            print(f"{sign}{r['edge']:>5.1f}% {r['n']:>4} {r['mean_error']:>9.3f} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['round_type']:<12} {r['color']:<8} {eu:<15} {r['condition']:<10}")

        # Save Layer 3 to CSV
        csv_file_3 = f'{output_prefix}_layer3_all_combos.csv'
        df_combos_layer3_sorted.to_csv(csv_file_3, index=False)
        print(f"\n[OK] Saved Layer 3 (all combos) to: {csv_file_3}")

        # Layer 4 summary
        print(f"\n{'='*100}")
        print("COMBO SCORING SYSTEM — LAYER 4 (Round × Color × Exec/Upside × Gap)")
        print(f"{'='*100}\n")

        df_combos_layer4_sorted = df_combos_layer4.reindex(
            df_combos_layer4['edge'].abs().sort_values(ascending=False).index
        )

        print(f"Total combos: {len(df_combos_layer4_sorted)}")
        print(f"Positive edges (bet FOR): {len(df_combos_layer4_sorted[df_combos_layer4_sorted['edge'] > 0])}")
        print(f"Negative edges (bet AGAINST): {len(df_combos_layer4_sorted[df_combos_layer4_sorted['edge'] < 0])}")

        print(f"\n{'Edge':>6} {'N':>4} {'Mean Err':>9} {'Good%':>6} {'Conf':>12} {'Round':<12} {'Color':<8} {'Exec/Upside':<15} {'Gap':<10} {'Condition':<10}")
        print(f"{'-'*130}")

        for _, r in df_combos_layer4_sorted.head(50).iterrows():
            eu = f"{r['exec']}/{r['upside']}"
            sign = "+" if r['edge'] > 0 else ""
            print(f"{sign}{r['edge']:>5.1f}% {r['n']:>4} {r['mean_error']:>9.3f} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['round_type']:<12} {r['color']:<8} {eu:<15} {r['gap']:<10} {r['condition']:<10}")

        # Save Layer 4 to CSV
        csv_file_4 = f'{output_prefix}_layer4_all_combos.csv'
        df_combos_layer4_sorted.to_csv(csv_file_4, index=False)
        print(f"\n[OK] Saved Layer 4 (all combos) to: {csv_file_4}")

        # Summary statistics
        print(f"\n{'='*100}")
        print("SUMMARY STATISTICS")
        print(f"{'='*100}\n")

        print("Layer 3 Edge Distribution:")
        print(f"  Mean edge: {df_combos_layer3['edge'].mean():.2f}%")
        print(f"  Median edge: {df_combos_layer3['edge'].median():.2f}%")
        print(f"  Std Dev: {df_combos_layer3['edge'].std():.2f}%")
        print(f"  Range: {df_combos_layer3['edge'].min():.1f}% to {df_combos_layer3['edge'].max():.1f}%")

        print("\nLayer 4 Edge Distribution:")
        print(f"  Mean edge: {df_combos_layer4['edge'].mean():.2f}%")
        print(f"  Median edge: {df_combos_layer4['edge'].median():.2f}%")
        print(f"  Std Dev: {df_combos_layer4['edge'].std():.2f}%")
        print(f"  Range: {df_combos_layer4['edge'].min():.1f}% to {df_combos_layer4['edge'].max():.1f}%")

        # Breakdown by condition
        print("\n\nBy Condition (Layer 3):")
        for cond in ['Calm', 'Moderate', 'Tough']:
            subset = df_combos_layer3[df_combos_layer3['condition'] == cond]
            pos = len(subset[subset['edge'] > 0])
            neg = len(subset[subset['edge'] < 0])
            print(f"  {cond:<10}: {len(subset):>3} combos | Positive: {pos:>3} | Negative: {neg:>3}")


if __name__ == "__main__":
    try:
        analyzer = ComboScoringSystem('ANALYSIS_v3_export.csv')

        print("\n[Step 1/2] Building Layer 3 (Round × Color × Exec/Upside)...")
        df_layer3 = analyzer.build_scoring_table()

        print("\n[Step 2/2] Building Layer 4 (+ Gap buckets)...")
        df_layer4 = analyzer.build_scoring_table_with_gap()

        analyzer.report(df_layer3, df_layer4)

        print("\n[OK] Scoring system complete!")
        print("\nFiles generated:")
        print("  - combo_scoring_layer3_all_combos.csv (all combos without gap)")
        print("  - combo_scoring_layer4_all_combos.csv (all combos with gap)")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
