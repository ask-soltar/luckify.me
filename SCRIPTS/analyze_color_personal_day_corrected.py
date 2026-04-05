"""
Color × Personal Day combo analysis with CORRECTED INTERPRETATION.

In this dataset:
- negative (score - course_avg < 0) = beats field average = GOOD
- positive (score - course_avg > 0) = underperforms = BAD

Standard filters:
- Condition: Calm, Moderate, Tough
- Round Type: Open, Positioning, Closing, Survival
- Tournament Type: S, NS only
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
df = pd.read_csv("Golf Historics v3 - ANALYSIS (7).csv")

print(f"Total records: {len(df)}")

# Apply standard filters
print("\nApplying standard filters...")

# Filter 1: Conditions
valid_conditions = {'Calm', 'Moderate', 'Tough'}
df = df[df['condition'].isin(valid_conditions)].copy()
print(f"After condition filter: {len(df)}")

# Filter 2: Round types
valid_round_types = {'Open', 'Positioning', 'Closing', 'Survival'}
df = df[df['round_type'].isin(valid_round_types)].copy()
print(f"After round_type filter: {len(df)}")

# Filter 3: Tournament types (S, NS only)
valid_tournament_types = {'S', 'NS'}
df = df[df['tournament_type'].isin(valid_tournament_types)].copy()
print(f"After tournament_type filter: {len(df)}")

# Filter 4: vs_avg must not be null (required for analysis)
df = df[df['vs_avg'].notna()].copy()
print(f"After vs_avg not-null filter: {len(df)}")

# Filter 5: color and Personal Day must not be null
df = df[df['color'].notna() & df['Personal Day'].notna()].copy()
print(f"After color and Personal Day not-null: {len(df)}")

# Convert vs_avg to numeric (may have come in as string)
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df = df[df['vs_avg'].notna()].copy()
print(f"After vs_avg numeric conversion: {len(df)}")

# Convert Personal Day to numeric
df['Personal Day'] = pd.to_numeric(df['Personal Day'], errors='coerce')
df = df[df['Personal Day'].notna()].copy()
print(f"After Personal Day numeric conversion: {len(df)}")

filtered_count = len(df)
original_count = 77155
print(f"\nFinal filtered set: {filtered_count} records ({100*filtered_count/original_count:.1f}% of {original_count})")

# Create combos
print("\nAnalyzing Color × Personal Day combos...")

combo_stats = {}

for (color, pd_val), group in df.groupby(['color', 'Personal Day']):
    vs_avg_vals = group['vs_avg'].values

    # Count beating field avg (negative vs_avg = good)
    num_beating = (vs_avg_vals < 0).sum()
    pct_beating = 100 * num_beating / len(vs_avg_vals)

    # Mean performance
    mean_perf = vs_avg_vals.mean()

    # Std dev (variance)
    std_dev = vs_avg_vals.std()

    # Min/max for range
    min_val = vs_avg_vals.min()
    max_val = vs_avg_vals.max()

    # Classify stability
    if std_dev < 0.5:
        stability = "Rock Solid"
    elif std_dev < 0.8:
        stability = "Consistent"
    elif std_dev < 1.2:
        stability = "Moderate"
    elif std_dev < 1.6:
        stability = "Volatile"
    else:
        stability = "Erratic"

    combo_stats[(color, pd_val)] = {
        'color': color,
        'personal_day': pd_val,
        'count': len(vs_avg_vals),
        'pct_beating_avg': pct_beating,
        'num_beating': num_beating,
        'mean_performance': mean_perf,
        'std_dev': std_dev,
        'min_val': min_val,
        'max_val': max_val,
        'stability': stability,
    }

print(f"Total combos found: {len(combo_stats)}")

# Convert to DataFrame for easier sorting
results_df = pd.DataFrame(combo_stats.values())

# Sort by % beating field avg (higher is better, lower mean is better)
# Primary sort: highest % beating avg
# Secondary sort: lowest std dev (most stable)
results_df['sort_key'] = results_df['pct_beating_avg'] * 1000 - results_df['std_dev']
results_df = results_df.sort_values('sort_key', ascending=False).reset_index(drop=True)

# Add ranking
results_df['rank'] = range(1, len(results_df) + 1)

# Create verdict column
def get_verdict(row):
    pct = row['pct_beating_avg']
    std = row['std_dev']
    mean = row['mean_performance']

    # Classify quality tiers
    if pct >= 56:
        tier = "PREMIER EDGE"
    elif pct >= 54:
        tier = "STRONG EDGE"
    elif pct >= 52:
        tier = "MODERATE EDGE"
    elif pct >= 50:
        tier = "SLIGHT EDGE"
    elif pct >= 48:
        tier = "NEUTRAL"
    else:
        tier = "WEAKNESS"

    # Add stability note
    if std < 0.5:
        note = f"Highly predictable"
    elif std < 0.8:
        note = f"Very predictable"
    elif std < 1.2:
        note = f"Reasonably predictable"
    else:
        note = f"Less predictable"

    # Format range
    range_str = f"{row['min_val']:.2f} to {row['max_val']:.2f}"

    return f"{tier} ({note})"

results_df['verdict'] = results_df.apply(get_verdict, axis=1)

# Format typical range (mean ± 1 std dev)
results_df['typical_range'] = results_df.apply(
    lambda row: f"{row['mean_performance'] - row['std_dev']:.2f} to {row['mean_performance'] + row['std_dev']:.2f}",
    axis=1
)

# Save to CSV with key metrics
output_df = results_df[[
    'rank', 'color', 'personal_day', 'count',
    'pct_beating_avg', 'num_beating',
    'mean_performance', 'std_dev', 'typical_range',
    'min_val', 'max_val', 'stability', 'verdict'
]].copy()

output_df.columns = [
    'Rank', 'Color', 'Personal Day', 'Sample Size',
    '% Beating Field Avg', '# Beating Field Avg',
    'Mean Performance', 'Std Dev', 'Typical Range (±1σ)',
    'Min', 'Max', 'Stability', 'Verdict'
]

# Save
output_path = "color_personalday_combos_corrected.csv"
output_df.to_csv(output_path, index=False)
print(f"\nResults saved to: {output_path}")

# Display top 15 and bottom 15
print("\n" + "="*120)
print("TOP 15 COMBOS (Best signals)")
print("="*120)

for idx, row in output_df.head(15).iterrows():
    print(f"\n{int(row['Rank'])}. {row['Color']} x Day {int(row['Personal Day'])}")
    print(f"   Beats field avg: {row['% Beating Field Avg']:.2f}% ({int(row['# Beating Field Avg'])} rounds)")
    print(f"   Mean performance: {row['Mean Performance']:.3f}")
    print(f"   Typical range: {row['Typical Range (±1σ)']}")
    print(f"   Stability: {row['Stability']} (stddev={row['Std Dev']:.3f})")
    print(f"   Verdict: {row['Verdict']}")

print("\n" + "="*120)
print("BOTTOM 15 COMBOS (Worst signals)")
print("="*120)

for idx, row in output_df.tail(15).iterrows():
    print(f"\n{int(row['Rank'])}. {row['Color']} x Day {int(row['Personal Day'])}")
    print(f"   Beats field avg: {row['% Beating Field Avg']:.2f}% ({int(row['# Beating Field Avg'])} rounds)")
    print(f"   Mean performance: {row['Mean Performance']:.3f}")
    print(f"   Typical range: {row['Typical Range (±1σ)']}")
    print(f"   Stability: {row['Stability']} (stddev={row['Std Dev']:.3f})")
    print(f"   Verdict: {row['Verdict']}")

# Summary statistics
print("\n" + "="*120)
print("SUMMARY STATISTICS")
print("="*120)
print(f"Total combos analyzed: {len(output_df)}")
print(f"Combos with >55% field beat rate (strong edge): {len(output_df[output_df['% Beating Field Avg'] > 55])}")
print(f"Combos with <48% field beat rate (weakness): {len(output_df[output_df['% Beating Field Avg'] < 48])}")
print(f"Average std dev across all combos: {output_df['Std Dev'].mean():.3f}")
print(f"Best stability (lowest std dev): {output_df['Std Dev'].min():.3f}")
print(f"Worst stability (highest std dev): {output_df['Std Dev'].max():.3f}")

# Distribution by stability
print(f"\nDistribution by stability:")
for stab in ['Rock Solid', 'Consistent', 'Moderate', 'Volatile', 'Erratic']:
    count = len(output_df[output_df['Stability'] == stab])
    print(f"  {stab}: {count} combos")

print("\nAnalysis complete!")
