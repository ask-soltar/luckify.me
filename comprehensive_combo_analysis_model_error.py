"""
Structured Combo Analysis — Model Error Baseline
Uses adj_his_par (player history + tour average shrinkage) as centerline.
Measures: Can this combo predict rounds better than the model?

Edge = (% rounds beating prediction by 2+) - (% rounds missing prediction by 2+)
Good = actual_off_par <= (adj_his_par - 2)  [beats model by 2+ strokes]
Bad = actual_off_par >= (adj_his_par + 2)   [misses model by 2+ strokes]

This is the true predictive signal, not absolute par comparison.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class StructuredComboAnalysisModelError:
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

        # Separate by condition
        self.conditions = {
            'Calm': self.df[self.df['condition'] == 'Calm'].copy(),
            'Moderate': self.df[self.df['condition'] == 'Moderate'].copy(),
            'Tough': self.df[self.df['condition'] == 'Tough'].copy()
        }

        for cond, data in self.conditions.items():
            print(f"{cond}: {len(data)} rows")

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
        """Calculate edge based on model error (actual vs adj_his_par)"""
        if len(combo_data) == 0:
            return None

        good = len(combo_data[combo_data['model_error'] <= -2.0])
        bad = len(combo_data[combo_data['model_error'] >= 2.0])
        total = len(combo_data)

        if total < 15:
            return None

        good_rate = good / total if total > 0 else 0
        bad_rate = bad / total if total > 0 else 0

        edge = (good_rate - bad_rate) * 100
        mean_error = combo_data['model_error'].mean()
        consistency = combo_data['model_error'].std()

        return {
            'n': total,
            'good': good,
            'bad': bad,
            'good_rate': good_rate * 100,
            'bad_rate': bad_rate * 100,
            'edge': edge,
            'mean_error': mean_error,
            'consistency': consistency
        }

    def get_exec_upside_pairs(self):
        """Define meaningful exec/upside pairs"""
        return [
            ('0-25', '0-25', 'Low'),
            ('25-50', '25-50', 'Mid-Low'),
            ('25-50', '50-75', 'Mid-Balanced'),
            ('50-75', '25-50', 'Mid-Balanced'),
            ('50-75', '50-75', 'Mid-High'),
            ('75-100', '75-100', 'High'),
            ('75-100', '50-75', 'High-Mixed'),
            ('50-75', '75-100', 'High-Mixed'),
        ]

    def analyze_layer_1(self, condition_name):
        """Layer 1: Round Type × Condition"""
        data = self.conditions[condition_name]
        results = []

        print(f"\n{'='*100}")
        print(f"LAYER 1: ROUND TYPE × {condition_name.upper()}")
        print(f"{'='*100}\n")

        round_types = data['round_type'].dropna().unique()

        for rt in round_types:
            if rt in ['REMOVE']:
                continue

            mask = data['round_type'] == rt
            combo_data = data[mask]

            stats = self.calculate_combo_stats(combo_data)
            if stats is None:
                continue

            confidence = 'HIGH' if stats['n'] >= 30 else ('EXPLORATORY' if stats['n'] >= 15 else 'WEAK')

            results.append({
                'condition': condition_name,
                'round_type': rt,
                'color': None,
                'exec_upside': None,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'mean_error': stats['mean_error'],
                'confidence': confidence
            })

        results_sorted = sorted(results, key=lambda x: x['edge'], reverse=True)

        print(f"{'Round Type':<15} {'N':>5} {'Mean Error':>11} {'Edge':>6} {'Confidence':>12}")
        print(f"{'-'*60}")
        for r in results_sorted:
            print(f"{r['round_type']:<15} {r['n']:>5} {r['mean_error']:>11.3f} {r['edge']:>6.1f}% {r['confidence']:>12}")

        return results_sorted

    def analyze_layer_2_for_round(self, condition_name, round_type):
        """Layer 2: Add Color"""
        data = self.conditions[condition_name]
        mask = data['round_type'] == round_type
        data = data[mask]

        results = []
        colors = data['color'].dropna().unique()

        for color in colors:
            color_data = data[data['color'] == color]
            stats = self.calculate_combo_stats(color_data)
            if stats is None:
                continue

            confidence = 'HIGH' if stats['n'] >= 30 else ('EXPLORATORY' if stats['n'] >= 15 else 'WEAK')

            results.append({
                'condition': condition_name,
                'round_type': round_type,
                'color': color,
                'exec_upside': None,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'mean_error': stats['mean_error'],
                'confidence': confidence
            })

        return sorted(results, key=lambda x: x['edge'], reverse=True)

    def analyze_layer_3_for_color(self, condition_name, round_type, color):
        """Layer 3: Add Exec/Upside pairs"""
        data = self.conditions[condition_name]
        mask = (data['round_type'] == round_type) & (data['color'] == color)
        data = data[mask]

        data['exec_bucket'] = data['exec'].apply(lambda x: self.bucket_value(x, 'exec'))
        data['upside_bucket'] = data['upside'].apply(lambda x: self.bucket_value(x, 'upside'))

        results = []
        pairs = self.get_exec_upside_pairs()

        for exec_b, upside_b, pair_label in pairs:
            pair_data = data[(data['exec_bucket'] == exec_b) & (data['upside_bucket'] == upside_b)]
            stats = self.calculate_combo_stats(pair_data)
            if stats is None:
                continue

            confidence = 'HIGH' if stats['n'] >= 30 else ('EXPLORATORY' if stats['n'] >= 15 else 'WEAK')

            results.append({
                'condition': condition_name,
                'round_type': round_type,
                'color': color,
                'exec_upside': f"{exec_b}x{upside_b}({pair_label})",
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'mean_error': stats['mean_error'],
                'confidence': confidence
            })

        return sorted(results, key=lambda x: x['edge'], reverse=True)

    def run_structured(self):
        """Run analysis layer by layer"""
        all_results = {}
        best_signals = []

        for condition in ['Calm', 'Moderate', 'Tough']:
            print(f"\n\n{'#'*100}")
            print(f"# CONDITION: {condition.upper()}")
            print(f"{'#'*100}")

            # Layer 1
            layer1 = self.analyze_layer_1(condition)
            all_results[f'{condition}_layer1'] = layer1

            # Top 3 round types
            top_rounds = [r['round_type'] for r in layer1[:3] if r['edge'] > 0]

            for rt in top_rounds:
                print(f"\n{'='*100}")
                print(f"LAYER 2: + COLOR (Round Type = {rt})")
                print(f"{'='*100}\n")

                layer2 = self.analyze_layer_2_for_round(condition, rt)

                print(f"{'Color':<10} {'N':>5} {'Mean Err':>10} {'Edge':>6} {'Confidence':>12}")
                print(f"{'-'*55}")
                for r in layer2[:10]:
                    if r['edge'] > 0:
                        print(f"{r['color']:<10} {r['n']:>5} {r['mean_error']:>10.3f} {r['edge']:>6.1f}% {r['confidence']:>12}")
                        best_signals.append(r)

                # Top 2 colors
                top_colors = [c['color'] for c in layer2[:2] if c['edge'] > 0]

                for color in top_colors:
                    print(f"\n{'='*100}")
                    print(f"LAYER 3: + EXEC/UPSIDE (Round = {rt}, Color = {color})")
                    print(f"{'='*100}\n")

                    layer3 = self.analyze_layer_3_for_color(condition, rt, color)

                    print(f"{'Exec/Upside':<25} {'N':>5} {'Mean Err':>10} {'Edge':>6} {'Conf':>12}")
                    print(f"{'-'*65}")
                    for r in layer3[:8]:
                        if r['edge'] > 0:
                            print(f"{r['exec_upside']:<25} {r['n']:>5} {r['mean_error']:>10.3f} {r['edge']:>6.1f}% {r['confidence']:>12}")
                            best_signals.append(r)

        return all_results, best_signals

    def report_summary(self, best_signals):
        """Generate summary of best signals"""
        print(f"\n\n{'='*100}")
        print("FINAL BETTING SIGNALS (Model Error Baseline)")
        print(f"{'='*100}\n")

        # Group by condition
        for condition in ['Calm', 'Moderate', 'Tough']:
            cond_signals = [s for s in best_signals if s['condition'] == condition and s['edge'] > 0]
            cond_signals = sorted(cond_signals, key=lambda x: x['edge'], reverse=True)

            if cond_signals:
                print(f"\n{condition.upper()} (Best signals)")
                print(f"{'-'*100}")
                for i, sig in enumerate(cond_signals[:5]):
                    combo = f"{sig['round_type']} x {sig['color']}"
                    if sig['exec_upside']:
                        combo += f" x {sig['exec_upside']}"
                    print(f"  #{i+1}: {combo}")
                    print(f"       Edge: {sig['edge']:>6.1f}% | Mean Error: {sig['mean_error']:>6.3f} | N={sig['n']} ({sig['confidence']})")


if __name__ == "__main__":
    try:
        analyzer = StructuredComboAnalysisModelError('ANALYSIS_v3_export.csv')
        all_results, best_signals = analyzer.run_structured()
        analyzer.report_summary(best_signals)

        print("\n[OK] Model error analysis complete!")
        print("Note: Edge now reflects prediction accuracy vs adj_his_par baseline")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV:")
        print("  Google Sheets -> ANALYSIS sheet -> File -> Download -> CSV")
        print("  Save as: ANALYSIS_v3_export.csv in d:\\Projects\\luckify-me\\")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
