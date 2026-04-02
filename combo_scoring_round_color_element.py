"""
Combo Scoring System: Round Type × Color × Element × Condition
Simplified scoring focusing on core divination dimensions.

Tournament Type = S only
Uses model_error (actual - adj_his_par) as baseline
Edge = (% beats prediction by 2+) - (% misses prediction by 2+)
"""

import pandas as pd
import numpy as np

class ComboScoringRoundColorElement:
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

        # Calculate model error (actual vs prediction)
        self.df['model_error'] = self.df['off_par'] - self.df['adj_his_par']

        self.df = self.df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', 'color', 'wu_xing'])
        print(f"After dropping NaNs: {len(self.df)} rows\n")

    def calculate_combo_stats(self, combo_data):
        """Calculate stats for a combo"""
        if len(combo_data) == 0:
            return None

        good = len(combo_data[combo_data['model_error'] <= -2.0])
        bad = len(combo_data[combo_data['model_error'] >= 2.0])
        total = len(combo_data)

        if total < 2:
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

    def build_scoring_table(self):
        """Build scoring table: Round × Color × Element × Condition"""
        all_combos = []

        conditions = ['Calm', 'Moderate', 'Tough']

        for condition in conditions:
            print(f"Building {condition}...")

            data = self.df[self.df['condition'] == condition].copy()

            round_types = data['round_type'].dropna().unique()
            colors = data['color'].dropna().unique()
            elements = data['wu_xing'].dropna().unique()

            combo_count = 0

            for rt in round_types:
                if rt in ['REMOVE', 'Mixed', 'Elimination']:
                    continue

                for color in colors:
                    for element in elements:
                        combo_count += 1

                        mask = (
                            (data['round_type'] == rt) &
                            (data['color'] == color) &
                            (data['wu_xing'] == element)
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
                            'element': element,
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

    def report(self, df_combos, output_prefix='combo_scoring_rce'):
        """Generate scoring table report"""

        print(f"\n{'='*120}")
        print("COMBO SCORING SYSTEM — Round Type × Color × Element × Condition")
        print(f"{'='*120}\n")

        # Sort by absolute edge (signal strength)
        df_sorted = df_combos.reindex(
            df_combos['edge'].abs().sort_values(ascending=False).index
        )

        print(f"Total combos: {len(df_sorted)}")
        print(f"Positive edges (bet FOR): {len(df_sorted[df_sorted['edge'] > 0])}")
        print(f"Negative edges (bet AGAINST): {len(df_sorted[df_sorted['edge'] < 0])}")
        print(f"Neutral (edge = 0): {len(df_sorted[df_sorted['edge'] == 0])}")

        print(f"\n{'Edge':>6} {'N':>4} {'Good%':>6} {'Conf':>12} {'Round':<12} {'Color':<8} {'Element':<8} {'Condition':<10} {'Mean Err':>9}")
        print(f"{'-'*110}")

        for _, r in df_sorted.iterrows():
            sign = "+" if r['edge'] > 0 else ""
            print(f"{sign}{r['edge']:>5.1f}% {r['n']:>4} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['round_type']:<12} {r['color']:<8} {r['element']:<8} {r['condition']:<10} {r['mean_error']:>9.3f}")

        # Save to CSV
        csv_file = f'{output_prefix}_all_combos.csv'
        df_sorted.to_csv(csv_file, index=False)
        print(f"\n[OK] Saved all combos to: {csv_file}")

        # Summary statistics
        print(f"\n{'='*120}")
        print("SUMMARY STATISTICS")
        print(f"{'='*120}\n")

        print("Edge Distribution:")
        print(f"  Mean edge: {df_combos['edge'].mean():.2f}%")
        print(f"  Median edge: {df_combos['edge'].median():.2f}%")
        print(f"  Std Dev: {df_combos['edge'].std():.2f}%")
        print(f"  Range: {df_combos['edge'].min():.1f}% to {df_combos['edge'].max():.1f}%")

        print("\n\nBy Condition:")
        for cond in ['Calm', 'Moderate', 'Tough']:
            subset = df_combos[df_combos['condition'] == cond]
            pos = len(subset[subset['edge'] > 0])
            neg = len(subset[subset['edge'] < 0])
            print(f"  {cond:<10}: {len(subset):>3} combos | Positive: {pos:>3} | Negative: {neg:>3}")

        print("\n\nBy Element (across all conditions):")
        for elem in sorted(df_combos['element'].unique()):
            subset = df_combos[df_combos['element'] == elem]
            pos = len(subset[subset['edge'] > 0])
            neg = len(subset[subset['edge'] < 0])
            avg_edge = subset['edge'].mean()
            print(f"  {elem:<10}: {len(subset):>3} combos | Positive: {pos:>3} | Negative: {neg:>3} | Avg Edge: {avg_edge:>6.1f}%")

        print("\n\nBy Round Type (across all conditions):")
        for rt in sorted(df_combos['round_type'].unique()):
            subset = df_combos[df_combos['round_type'] == rt]
            pos = len(subset[subset['edge'] > 0])
            neg = len(subset[subset['edge'] < 0])
            avg_edge = subset['edge'].mean()
            print(f"  {rt:<15}: {len(subset):>3} combos | Positive: {pos:>3} | Negative: {neg:>3} | Avg Edge: {avg_edge:>6.1f}%")

        print("\n\nTop 20 Positive Signals (Bet FOR):")
        print(f"{'-'*110}")
        pos_signals = df_sorted[df_sorted['edge'] > 0].head(20)
        for idx, (_, r) in enumerate(pos_signals.iterrows(), 1):
            print(f"  {idx:>2}. {r['round_type']:<12} × {r['color']:<8} × {r['element']:<8} ({r['condition']:<10}): +{r['edge']:>5.1f}% (N={r['n']}, {r['confidence']})")

        print("\n\nTop 20 Negative Signals (Bet AGAINST):")
        print(f"{'-'*110}")
        neg_signals = df_sorted[df_sorted['edge'] < 0].head(20)
        for idx, (_, r) in enumerate(neg_signals.iterrows(), 1):
            print(f"  {idx:>2}. {r['round_type']:<12} × {r['color']:<8} × {r['element']:<8} ({r['condition']:<10}): {r['edge']:>5.1f}% (N={r['n']}, {r['confidence']})")


if __name__ == "__main__":
    try:
        analyzer = ComboScoringRoundColorElement('ANALYSIS_v3_export.csv')
        df_combos = analyzer.build_scoring_table()
        analyzer.report(df_combos)

        print("\n[OK] Scoring system complete!")
        print("\nFile generated:")
        print("  - combo_scoring_rce_all_combos.csv (all combos with edges)")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
