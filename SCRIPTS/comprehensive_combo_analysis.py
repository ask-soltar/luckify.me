"""
Comprehensive Combo Analysis - All Dimensions
Tests every available combination across:
- Round Type (Survival, Positioning, Closing)
- Color (all 6 colors)
- Exec Bucket (0-25, 25-50, 50-75, 75-100)
- Upside Bucket (0-25, 25-50, 50-75, 75-100)
- Gap Bucket (20+, 10-20, 0-10, -10-0, -20--10, <-20)

Filter: Tournament Type = S only, Separated by Condition (Calm, Moderate, Tough)
Thresholds: Good ≤ -2.0, Bad ≥ +2.0
Confidence: N≥30 (HIGH), N=15-30 (EXPLORATORY), N<15 (WEAK)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from itertools import product

class ComprehensiveComboAnalysis:
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

        if total < 15:  # Skip very small samples (below exploratory threshold)
            return None

        good_rate = good / total if total > 0 else 0
        bad_rate = bad / total if total > 0 else 0

        # Edge = good% - bad% (how much better than neutral)
        edge = (good_rate - bad_rate) * 100

        # Stability = ratio of test to baseline (simplified without train/test split)
        # Here we'll use consistency: std dev of off_par (lower = more stable)
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

    def analyze_condition(self, condition_name):
        """Comprehensive analysis for one condition"""
        data = self.conditions[condition_name]
        results = []

        print(f"\n{'='*100}")
        print(f"ANALYZING {condition_name.upper()}")
        print(f"{'='*100}\n")

        # Add buckets to data
        data['exec_bucket'] = data['exec'].apply(lambda x: self.bucket_value(x, 'exec'))
        data['upside_bucket'] = data['upside'].apply(lambda x: self.bucket_value(x, 'upside'))
        data['gap_bucket'] = data['gap'].apply(lambda x: self.bucket_value(x, 'gap'))

        # Get unique values
        round_types = data['round_type'].dropna().unique()
        colors = data['color'].dropna().unique()
        exec_buckets = data['exec_bucket'].dropna().unique()
        upside_buckets = data['upside_bucket'].dropna().unique()
        gap_buckets = data['gap_bucket'].dropna().unique()

        print(f"Dimensions found:")
        print(f"  Round Types: {len(round_types)} ({list(round_types)})")
        print(f"  Colors: {len(colors)}")
        print(f"  Exec Buckets: {len(exec_buckets)}")
        print(f"  Upside Buckets: {len(upside_buckets)}")
        print(f"  Gap Buckets: {len(gap_buckets)}")

        combo_count = 0
        found_count = 0

        # Test all combinations that exist in data
        for rt in round_types:
            for color in colors:
                for exec_b in exec_buckets:
                    if pd.isna(exec_b):
                        continue
                    for upside_b in upside_buckets:
                        if pd.isna(upside_b):
                            continue
                        for gap_b in gap_buckets:
                            if pd.isna(gap_b):
                                continue

                            combo_count += 1

                            # Filter for this combo
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

                            found_count += 1

                            # Confidence level
                            if stats['n'] >= 30:
                                confidence = 'HIGH'
                            elif stats['n'] >= 15:
                                confidence = 'EXPLORATORY'
                            else:
                                confidence = 'WEAK'

                            results.append({
                                'condition': condition_name,
                                'round_type': rt,
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
                                'avg_off_par': stats['avg_off_par'],
                                'consistency': stats['consistency'],
                                'confidence': confidence
                            })

        print(f"Tested {combo_count} theoretical combos, found {found_count} with N>=15")

        # Sort by edge (descending)
        results_sorted = sorted(results, key=lambda x: x['edge'], reverse=True)

        return results_sorted

    def run_all(self):
        """Run analysis for all conditions"""
        all_results = {}

        for condition in ['Calm', 'Moderate', 'Tough']:
            results = self.analyze_condition(condition)
            all_results[condition] = results

        return all_results

    def report(self, all_results, output_prefix='combo_analysis'):
        """Generate comprehensive reports"""

        # Print top signals per condition
        print(f"\n{'='*100}")
        print("TOP SIGNALS BY CONDITION")
        print(f"{'='*100}\n")

        for condition in ['Calm', 'Moderate', 'Tough']:
            results = all_results[condition]
            if not results:
                print(f"{condition}: No signals found\n")
                continue

            print(f"\n{condition.upper()} - Top 20 Signals")
            print(f"{'-'*100}")
            print(f"{'Edge':>6} {'N':>5} {'Good%':>6} {'Confidence':>12} {'Round':>12} {'Color':>8} {'Exec':>8} {'Upside':>8} {'Gap':>10}")
            print(f"{'-'*100}")

            for i, r in enumerate(results[:20]):
                print(f"{r['edge']:>6.1f}% {r['n']:>5} {r['good_rate']:>6.1f}% {r['confidence']:>12} {r['round_type']:>12} {r['color']:>8} {r['exec_bucket']:>8} {r['upside_bucket']:>8} {r['gap_bucket']:>10}")

        # Save to CSV
        all_combos = []
        for condition, results in all_results.items():
            for r in results:
                all_combos.append(r)

        df_output = pd.DataFrame(all_combos)
        csv_file = f'{output_prefix}_all_combos.csv'
        df_output.to_csv(csv_file, index=False)
        print(f"\n[OK] Saved all combos to: {csv_file}")

        # Save JSON summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'filter': 'Tournament Type = S only',
            'thresholds': {'good': '≤ -2.0', 'bad': '≥ +2.0'},
            'conditions': {}
        }

        for condition in ['Calm', 'Moderate', 'Tough']:
            results = all_results[condition]
            summary['conditions'][condition] = {
                'total_combos_found': len(results),
                'top_5_signals': [
                    {
                        'edge': r['edge'],
                        'n': r['n'],
                        'good_rate': r['good_rate'],
                        'confidence': r['confidence'],
                        'combo': f"{r['round_type']} × {r['color']} × {r['exec_bucket']} exec × {r['upside_bucket']} upside × {r['gap_bucket']} gap"
                    }
                    for r in results[:5]
                ]
            }

        json_file = f'{output_prefix}_summary.json'
        with open(json_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"[OK] Saved summary to: {json_file}")

        return df_output

    def compare_to_previous(self, df_output):
        """Compare new signals to previous 3 winning signals"""
        previous_winners = [
            ('Calm', 'Closing', 'Purple', '75-100', '75-100', None, '+4.6%'),  # Approximation
            ('Calm', 'Closing', 'Green', '50-75', '75-100', None, '+5.9%'),    # Approximation
            ('Moderate', 'Closing', 'Blue', '75-100', '75-100', None, '+5.5%') # Approximation
        ]

        print(f"\n{'='*100}")
        print("COMPARISON TO PREVIOUS WINNING SIGNALS")
        print(f"{'='*100}\n")

        # Find how many new signals beat the minimum previous edge (+4.6%)
        beat_minimum = df_output[df_output['edge'] >= 4.6]
        print(f"Signals beating previous minimum edge (+4.6%): {len(beat_minimum)}")
        print(f"Total signals found: {len(df_output)}")
        print(f"Percentage beating previous: {len(beat_minimum)/len(df_output)*100:.1f}%\n")


if __name__ == "__main__":
    try:
        analyzer = ComprehensiveComboAnalysis('ANALYSIS_v3_export.csv')
        all_results = analyzer.run_all()
        df_output = analyzer.report(all_results)
        analyzer.compare_to_previous(df_output)

        print("\n[OK] Comprehensive combo analysis complete!")
        print("Files generated:")
        print("  - combo_analysis_all_combos.csv (all signals)")
        print("  - combo_analysis_summary.json (top 5 per condition)")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nMake sure you've exported ANALYSIS v3 as CSV:")
        print("  Google Sheets -> ANALYSIS sheet -> File -> Download -> CSV")
        print("  Save as: ANALYSIS_v3_export.csv in d:\\Projects\\luckify-me\\")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
