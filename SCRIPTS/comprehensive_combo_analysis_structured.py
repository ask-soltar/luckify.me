"""
Structured Combo Analysis — Build from Foundation Up
Tests combinations in logical layers:
1. Round Type × Condition (foundation)
2. + Color (adds rhythm signal)
3. + Exec/Upside Pairs (correlated, tested together)
4. + Gap (refinement)

Exec/Upside pairs (not all 12 combos):
- Low: (0-25, 0-25)
- Mid-Low: (25-50, 25-50)
- Mid: (25-50, 50-75), (50-75, 25-50)
- Mid-High: (50-75, 50-75)
- High: (75-100, 75-100)
- Mixed: (75-100, 50-75), (50-75, 75-100)

Filter: Tournament Type = S only
Thresholds: Good ≤ -2.0, Bad ≥ +2.0
Confidence: N≥30 (HIGH), N=15-30 (EXPLORATORY), N<15 (WEAK)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from itertools import product

class StructuredComboAnalysis:
    def __init__(self, analysis_csv_path):
        """Load and filter ANALYSIS v3 data"""
        self.df = pd.read_csv(analysis_csv_path)
        print(f"Loaded {len(self.df)} total rows")

        # Filter for Tournament Type = S only
        self.df = self.df[self.df['tournament_type'] == 'S'].copy()
        print(f"After S filter: {len(self.df)} rows")

        # Ensure numeric columns
        self.df['off_par'] = pd.to_numeric(self.df['off_par'], errors='coerce')
        self.df['exec'] = pd.to_numeric(self.df['exec'], errors='coerce')
        self.df['upside'] = pd.to_numeric(self.df['upside'], errors='coerce')
        self.df['gap'] = pd.to_numeric(self.df['gap'], errors='coerce')

        self.df = self.df.dropna(subset=['off_par', 'condition', 'round_type', 'color'])
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
        """Calculate edge and stability for a combo"""
        if len(combo_data) == 0:
            return None

        good = len(combo_data[combo_data['off_par'] <= -2.0])
        bad = len(combo_data[combo_data['off_par'] >= 2.0])
        total = len(combo_data)

        if total < 15:
            return None

        good_rate = good / total if total > 0 else 0
        bad_rate = bad / total if total > 0 else 0

        edge = (good_rate - bad_rate) * 100
        consistency = combo_data['off_par'].std()

        return {
            'n': total,
            'good': good,
            'bad': bad,
            'good_rate': good_rate * 100,
            'bad_rate': bad_rate * 100,
            'edge': edge,
            'consistency': consistency,
            'avg_off_par': combo_data['off_par'].mean()
        }

    def get_exec_upside_pairs(self):
        """Define meaningful exec/upside pairs (not all 12)"""
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
        """Layer 1: Round Type × Condition (foundation)"""
        data = self.conditions[condition_name]
        results = []

        print(f"\n{'='*100}")
        print(f"LAYER 1: ROUND TYPE × {condition_name.upper()}")
        print(f"{'='*100}\n")

        round_types = data['round_type'].dropna().unique()

        for rt in round_types:
            if rt in ['REMOVE']:  # Skip non-playable round types
                continue

            mask = data['round_type'] == rt
            combo_data = data[mask]

            stats = self.calculate_combo_stats(combo_data)
            if stats is None:
                continue

            confidence = 'HIGH' if stats['n'] >= 30 else ('EXPLORATORY' if stats['n'] >= 15 else 'WEAK')

            results.append({
                'layer': 1,
                'condition': condition_name,
                'round_type': rt,
                'color': None,
                'exec_upside': None,
                'gap_bucket': None,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'confidence': confidence
            })

        results_sorted = sorted(results, key=lambda x: x['edge'], reverse=True)

        print(f"{'Round Type':<15} {'N':>5} {'Good%':>6} {'Confidence':>12} {'Edge':>6}")
        print(f"{'-'*50}")
        for r in results_sorted:
            print(f"{r['round_type']:<15} {r['n']:>5} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['edge']:>6.1f}%")

        return results_sorted

    def analyze_layer_2_for_round(self, condition_name, round_type):
        """Layer 2: Add Color to best round types"""
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
                'layer': 2,
                'condition': condition_name,
                'round_type': round_type,
                'color': color,
                'exec_upside': None,
                'gap_bucket': None,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'consistency': stats['consistency'],
                'confidence': confidence
            })

        return sorted(results, key=lambda x: x['edge'], reverse=True)

    def analyze_layer_3_for_color(self, condition_name, round_type, color):
        """Layer 3: Add Exec/Upside pairs to best colors"""
        data = self.conditions[condition_name]
        mask = (data['round_type'] == round_type) & (data['color'] == color)
        data = data[mask]

        # Add buckets
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
                'layer': 3,
                'condition': condition_name,
                'round_type': round_type,
                'color': color,
                'exec_upside': f"{exec_b}×{upside_b}({pair_label})",
                'gap_bucket': None,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'consistency': stats['consistency'],
                'confidence': confidence
            })

        return sorted(results, key=lambda x: x['edge'], reverse=True)

    def analyze_layer_4_for_pair(self, condition_name, round_type, color, exec_b, upside_b):
        """Layer 4: Add Gap buckets to best pairs"""
        data = self.conditions[condition_name]
        data['exec_bucket'] = data['exec'].apply(lambda x: self.bucket_value(x, 'exec'))
        data['upside_bucket'] = data['upside'].apply(lambda x: self.bucket_value(x, 'upside'))
        data['gap_bucket'] = data['gap'].apply(lambda x: self.bucket_value(x, 'gap'))

        mask = (
            (data['round_type'] == round_type) &
            (data['color'] == color) &
            (data['exec_bucket'] == exec_b) &
            (data['upside_bucket'] == upside_b)
        )
        data = data[mask]

        results = []
        gap_buckets = data['gap_bucket'].dropna().unique()

        for gap_b in gap_buckets:
            gap_data = data[data['gap_bucket'] == gap_b]
            stats = self.calculate_combo_stats(gap_data)
            if stats is None:
                continue

            confidence = 'HIGH' if stats['n'] >= 30 else ('EXPLORATORY' if stats['n'] >= 15 else 'WEAK')

            results.append({
                'layer': 4,
                'condition': condition_name,
                'round_type': round_type,
                'color': color,
                'exec_bucket': exec_b,
                'upside_bucket': upside_b,
                'gap_bucket': gap_b,
                'n': stats['n'],
                'good': stats['good'],
                'bad': stats['bad'],
                'good_rate': stats['good_rate'],
                'bad_rate': stats['bad_rate'],
                'edge': stats['edge'],
                'consistency': stats['consistency'],
                'confidence': confidence
            })

        return sorted(results, key=lambda x: x['edge'], reverse=True)

    def run_structured(self):
        """Run analysis layer by layer, focusing on top signals at each level"""
        all_results = {}

        for condition in ['Calm', 'Moderate', 'Tough']:
            print(f"\n\n{'#'*100}")
            print(f"# CONDITION: {condition.upper()}")
            print(f"{'#'*100}")

            # Layer 1: Foundation
            layer1 = self.analyze_layer_1(condition)
            all_results[f'{condition}_layer1'] = layer1

            # For top 3 round types, go to Layer 2
            top_rounds = [r['round_type'] for r in layer1[:3]]

            for rt in top_rounds:
                print(f"\n{'='*100}")
                print(f"LAYER 2: + COLOR (Round Type = {rt})")
                print(f"{'='*100}\n")

                layer2 = self.analyze_layer_2_for_round(condition, rt)
                all_results[f'{condition}_{rt}_layer2'] = layer2

                print(f"{'Color':<10} {'N':>5} {'Good%':>6} {'Confidence':>12} {'Edge':>6}")
                print(f"{'-'*50}")
                for r in layer2[:10]:  # Show top 10 colors
                    print(f"{r['color']:<10} {r['n']:>5} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['edge']:>6.1f}%")

                # For top 2 colors, go to Layer 3
                top_colors = [c['color'] for c in layer2[:2]]

                for color in top_colors:
                    print(f"\n{'='*100}")
                    print(f"LAYER 3: + EXEC/UPSIDE PAIRS (Round = {rt}, Color = {color})")
                    print(f"{'='*100}\n")

                    layer3 = self.analyze_layer_3_for_color(condition, rt, color)
                    all_results[f'{condition}_{rt}_{color}_layer3'] = layer3

                    print(f"{'Exec/Upside':<30} {'N':>5} {'Good%':>6} {'Confidence':>12} {'Edge':>6}")
                    print(f"{'-'*70}")
                    for r in layer3[:8]:  # Show top 8 pairs
                        print(f"{r['exec_upside']:<30} {r['n']:>5} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['edge']:>6.1f}%")

                    # For top pair, go to Layer 4
                    if layer3:
                        top_pair = layer3[0]
                        exec_b = top_pair['exec_upside'].split('(')[0].split('×')[0]
                        upside_b = top_pair['exec_upside'].split('(')[0].split('×')[1]

                        print(f"\n{'='*100}")
                        print(f"LAYER 4: + GAP (Round = {rt}, Color = {color}, Exec/Upside = {exec_b}×{upside_b})")
                        print(f"{'='*100}\n")

                        layer4 = self.analyze_layer_4_for_pair(condition, rt, color, exec_b, upside_b)
                        all_results[f'{condition}_{rt}_{color}_{exec_b}_{upside_b}_layer4'] = layer4

                        print(f"{'Gap':<12} {'N':>5} {'Good%':>6} {'Confidence':>12} {'Edge':>6}")
                        print(f"{'-'*50}")
                        for r in layer4:
                            print(f"{r['gap_bucket']:<12} {r['n']:>5} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['edge']:>6.1f}%")

        return all_results

    def report_summary(self, all_results):
        """Generate summary of best signals per condition"""
        print(f"\n\n{'='*100}")
        print("FINAL SUMMARY: TOP SIGNALS BY CONDITION")
        print(f"{'='*100}\n")

        best_by_condition = {}

        for condition in ['Calm', 'Moderate', 'Tough']:
            layer1_key = f'{condition}_layer1'
            layer1 = all_results.get(layer1_key, [])

            if not layer1:
                continue

            print(f"\n{condition.upper()} — Layer 1 (Round Type Foundation)")
            print(f"{'-'*60}")
            for r in layer1[:5]:
                print(f"  {r['round_type']:<15} Edge: {r['edge']:>6.1f}% (N={r['n']}, {r['confidence']})")

            # Find best layer 4 signals
            layer4_signals = []
            for key, results in all_results.items():
                if 'layer4' in key and condition in key:
                    layer4_signals.extend(results)

            if layer4_signals:
                layer4_signals = sorted(layer4_signals, key=lambda x: x['edge'], reverse=True)
                print(f"\n{condition.upper()} — Best Full Combos (Layer 4)")
                print(f"{'-'*100}")
                for i, r in enumerate(layer4_signals[:3]):
                    print(f"  #{i+1}: {r['round_type']} × {r['color']} × {r['exec_bucket']}/{r['upside_bucket']} × {r['gap_bucket']}")
                    print(f"      Edge: {r['edge']:>6.1f}% (N={r['n']}, {r['confidence']})")

            best_by_condition[condition] = layer4_signals[:3] if layer4_signals else []

        return best_by_condition


if __name__ == "__main__":
    try:
        analyzer = StructuredComboAnalysis('ANALYSIS_v3_export.csv')
        all_results = analyzer.run_structured()
        best = analyzer.report_summary(all_results)

        print("\n[OK] Structured combo analysis complete!")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV:")
        print("  Google Sheets -> ANALYSIS sheet -> File -> Download -> CSV")
        print("  Save as: ANALYSIS_v3_export.csv in d:\\Projects\\luckify-me\\")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
