#!/usr/bin/env python3
"""
Analyze Color × Personal Day combos segmented by CONDITION (Calm, Moderate, Tough).

Input: Golf Historics v3 - ANALYSIS (7).csv
Filters: Round Type (Open/Positioning/Closing/Survival), Tournament Type (S/NS)

Output:
- color_personalday_by_condition.csv — all combos × conditions
- color_personalday_condition_report.txt — detailed report
"""

import pandas as pd
import numpy as np
import duckdb
from collections import defaultdict

# Load data
print("Loading Golf Historics v3 - ANALYSIS (7).csv...")
df = pd.read_csv("Golf Historics v3 - ANALYSIS (7).csv")

print(f"Total rows: {len(df)}")
print(f"Columns: {df.shape[1]}")

# Verify key columns exist
key_cols = ['color', 'Personal Day', 'condition', 'round_type', 'tournament_type', 'vs_avg']
missing = [c for c in key_cols if c not in df.columns]
if missing:
    print(f"ERROR: Missing columns: {missing}")
    print(f"Available columns: {list(df.columns)}")
    exit(1)

# Filter by Round Type and Tournament Type
print("\nFiltering by Round Type (Open/Positioning/Closing/Survival) and Tournament Type (S/NS)...")
valid_rounds = ['Open', 'Positioning', 'Closing', 'Survival']
valid_tournaments = ['S', 'NS']

df_filtered = df[
    (df['round_type'].isin(valid_rounds)) &
    (df['tournament_type'].isin(valid_tournaments))
].copy()

print(f"After filtering: {len(df_filtered)} rows")

# Clean Personal Day (convert to int, drop nulls/invalid)
df_filtered['Personal Day'] = pd.to_numeric(df_filtered['Personal Day'], errors='coerce')
df_filtered = df_filtered.dropna(subset=['Personal Day'])
df_filtered['Personal Day'] = df_filtered['Personal Day'].astype(int)

print(f"After dropping invalid Personal Day: {len(df_filtered)} rows")

# Clean vs_avg (convert to float, drop nulls/invalid)
df_filtered['vs_avg'] = pd.to_numeric(df_filtered['vs_avg'], errors='coerce')
df_filtered = df_filtered.dropna(subset=['vs_avg'])

# Verify condition column values
print(f"\nUnique conditions: {df_filtered['condition'].unique()}")
print(f"Condition counts:\n{df_filtered['condition'].value_counts()}")

# Create DuckDB connection
conn = duckdb.connect(":memory:")
conn.register("data", df_filtered)

# Define top 15 and worst 5 combos
top_15_combos = [
    ('Red', 4), ('Red', 8), ('Red', 9),
    ('Green', 2), ('Green', 11), ('Green', 22),
    ('Purple', 1), ('Purple', 3), ('Purple', 11),
    ('Orange', 1), ('Orange', 33),
    ('Yellow', 22),
    ('Blue', 2), ('Blue', 7), ('Blue', 12)
]

worst_5_combos = [
    ('Red', 7), ('Pink', 6), ('Brown', 2), ('Brown', 22), ('Brown', 11)
]

all_combos = top_15_combos + worst_5_combos

# Analyze each combo × condition
results = []
report_lines = []

print("\n" + "="*80)
print("ANALYZING COLOR × PERSONAL DAY COMBOS BY CONDITION")
print("="*80)

for color, day in all_combos:
    combo_label = f"{color} × Day {day}"
    print(f"\n{combo_label}")
    print("-" * 60)

    combo_data = {
        'Combo': combo_label,
        'Color': color,
        'Personal_Day': day
    }

    for condition in ['Calm', 'Moderate', 'Tough']:
        # Query: % beating field avg (vs_avg > 0) for this combo × condition
        query = f"""
        SELECT
            COUNT(*) as total_count,
            SUM(CASE WHEN vs_avg > 0 THEN 1 ELSE 0 END) as beats_count,
            ROUND(100.0 * SUM(CASE WHEN vs_avg > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_beats,
            ROUND(AVG(vs_avg), 2) as avg_vs_avg,
            ROUND(STDDEV(vs_avg), 2) as std_vs_avg
        FROM data
        WHERE color = '{color}'
          AND "Personal Day" = {day}
          AND condition = '{condition}'
        """

        result = conn.execute(query).fetchall()
        if result:
            row = result[0]
            total, beats, pct, avg_v, std_v = row

            if total and total > 0 and pct is not None:
                combo_data[f'{condition}_count'] = total
                combo_data[f'{condition}_beats_pct'] = pct if pct is not None else None
                combo_data[f'{condition}_avg_vs_avg'] = avg_v if avg_v is not None else None
                combo_data[f'{condition}_std_vs_avg'] = std_v if std_v is not None else None

                if pct is not None and avg_v is not None and std_v is not None:
                    print(f"  {condition:12s}: {pct:6.1f}% (n={total:5d}) beats field | avg vs_avg: {avg_v:+6.2f} ± {std_v:5.2f}")
                else:
                    print(f"  {condition:12s}: {total} rows but missing pct/avg/std")
            else:
                combo_data[f'{condition}_count'] = 0
                combo_data[f'{condition}_beats_pct'] = None
                combo_data[f'{condition}_avg_vs_avg'] = None
                combo_data[f'{condition}_std_vs_avg'] = None
                print(f"  {condition:12s}: NO DATA")
        else:
            combo_data[f'{condition}_count'] = 0
            combo_data[f'{condition}_beats_pct'] = None
            combo_data[f'{condition}_avg_vs_avg'] = None
            combo_data[f'{condition}_std_vs_avg'] = None
            print(f"  {condition:12s}: NO DATA")

    # Determine pattern
    calm_pct = combo_data.get('Calm_beats_pct')
    mod_pct = combo_data.get('Moderate_beats_pct')
    tough_pct = combo_data.get('Tough_beats_pct')

    valid_pcts = [p for p in [calm_pct, mod_pct, tough_pct] if p is not None]

    if not valid_pcts:
        pattern = "INSUFFICIENT DATA"
    elif len(valid_pcts) == 3:
        # All three conditions have data
        if calm_pct > 55 and mod_pct > 55 and tough_pct > 55:
            pattern = "CONSISTENT STRONG (all >55%)"
        elif calm_pct < 45 and mod_pct < 45 and tough_pct < 45:
            pattern = "CONSISTENT WEAK (all <45%)"
        elif calm_pct > 55 and tough_pct < 45:
            pattern = "CONDITION-DEPENDENT: Strong on Calm, weak on Tough"
        elif calm_pct < 45 and tough_pct > 55:
            pattern = "SWITCHES DIRECTION: Weak on Calm, strong on Tough"
        elif abs(calm_pct - mod_pct) < 5 and abs(mod_pct - tough_pct) < 5:
            pattern = "FLAT ACROSS CONDITIONS (within ±5%)"
        else:
            pattern = "MIXED PATTERN"
    elif len(valid_pcts) == 2:
        pattern = "LIMITED DATA (only 2 conditions)"
    else:
        pattern = "VERY LIMITED DATA (only 1 condition)"

    combo_data['Pattern'] = pattern
    print(f"  STATUS: {pattern}")

    results.append(combo_data)
    report_lines.append(f"{combo_label:20s} | {pattern}")

# Create results dataframe
results_df = pd.DataFrame(results)

# Save detailed CSV
print("\n" + "="*80)
print("Saving results to color_personalday_by_condition.csv...")
results_df.to_csv("color_personalday_by_condition.csv", index=False)
print(f"Saved {len(results_df)} combos")

# Create summary report
print("Saving report to color_personalday_condition_report.txt...")
with open("color_personalday_condition_report.txt", "w") as f:
    f.write("COLOR × PERSONAL DAY ANALYSIS BY CONDITION\n")
    f.write("="*80 + "\n")
    f.write(f"Input: Golf Historics v3 - ANALYSIS (7).csv\n")
    f.write(f"Total rows: {len(df)}\n")
    f.write(f"Filtered (Round Type + Tournament Type): {len(df_filtered)} rows\n")
    f.write(f"\nFilters applied:\n")
    f.write(f"  - Round Type: {valid_rounds}\n")
    f.write(f"  - Tournament Type: {valid_tournaments}\n")
    f.write("\n" + "="*80 + "\n")
    f.write("SUMMARY: TOP 15 COMBOS\n")
    f.write("="*80 + "\n")

    for i, combo in enumerate(top_15_combos, 1):
        color, day = combo
        combo_label = f"{color} × Day {day}"
        row = results_df[results_df['Combo'] == combo_label]
        if not row.empty:
            row = row.iloc[0]
            f.write(f"\n{i}. {combo_label}\n")
            f.write(f"   Calm:      {row.get('Calm_beats_pct', 'N/A'):>6}% (n={int(row.get('Calm_count', 0))})\n")
            f.write(f"   Moderate:  {row.get('Moderate_beats_pct', 'N/A'):>6}% (n={int(row.get('Moderate_count', 0))})\n")
            f.write(f"   Tough:     {row.get('Tough_beats_pct', 'N/A'):>6}% (n={int(row.get('Tough_count', 0))})\n")
            f.write(f"   Pattern:   {row['Pattern']}\n")

    f.write("\n" + "="*80 + "\n")
    f.write("WORST 5 COMBOS\n")
    f.write("="*80 + "\n")

    for i, combo in enumerate(worst_5_combos, 1):
        color, day = combo
        combo_label = f"{color} × Day {day}"
        row = results_df[results_df['Combo'] == combo_label]
        if not row.empty:
            row = row.iloc[0]
            f.write(f"\n{i}. {combo_label}\n")
            f.write(f"   Calm:      {row.get('Calm_beats_pct', 'N/A'):>6}% (n={int(row.get('Calm_count', 0))})\n")
            f.write(f"   Moderate:  {row.get('Moderate_beats_pct', 'N/A'):>6}% (n={int(row.get('Moderate_count', 0))})\n")
            f.write(f"   Tough:     {row.get('Tough_beats_pct', 'N/A'):>6}% (n={int(row.get('Tough_count', 0))})\n")
            f.write(f"   Pattern:   {row['Pattern']}\n")

    f.write("\n" + "="*80 + "\n")
    f.write("KEY FINDINGS\n")
    f.write("="*80 + "\n")

    # Identify patterns
    consistent_strong = [r for r in results if 'STRONG' in r['Pattern']]
    consistent_weak = [r for r in results if 'WEAK' in r['Pattern']]
    condition_dependent = [r for r in results if 'CONDITION-DEPENDENT' in r['Pattern']]
    switches = [r for r in results if 'SWITCHES' in r['Pattern']]

    f.write(f"\nConsistent Strong (all conditions >55%): {len(consistent_strong)}\n")
    for r in consistent_strong:
        f.write(f"  - {r['Combo']}\n")

    f.write(f"\nConsistent Weak (all conditions <45%): {len(consistent_weak)}\n")
    for r in consistent_weak:
        f.write(f"  - {r['Combo']}\n")

    f.write(f"\nCondition-Dependent (varies significantly): {len(condition_dependent)}\n")
    for r in condition_dependent:
        f.write(f"  - {r['Combo']}: {r['Pattern']}\n")

    f.write(f"\nSwitches Direction: {len(switches)}\n")
    for r in switches:
        f.write(f"  - {r['Combo']}: {r['Pattern']}\n")

print("Report saved.\n")

# Display summary
print("="*80)
print("PATTERN SUMMARY")
print("="*80)
consistent_strong = results_df[results_df['Pattern'].str.contains('STRONG', na=False)]
consistent_weak = results_df[results_df['Pattern'].str.contains('WEAK', na=False)]
condition_dep = results_df[results_df['Pattern'].str.contains('CONDITION-DEPENDENT', na=False)]
switches = results_df[results_df['Pattern'].str.contains('SWITCHES', na=False)]

print(f"Consistent Strong (>55% all): {len(consistent_strong)}")
print(f"Consistent Weak (<45% all):   {len(consistent_weak)}")
print(f"Condition-Dependent:          {len(condition_dep)}")
print(f"Switches Direction:           {len(switches)}")
print(f"Other/Insufficient:           {len(results_df) - len(consistent_strong) - len(consistent_weak) - len(condition_dep) - len(switches)}")

print("\nAnalysis complete. Files generated:")
print("  - color_personalday_by_condition.csv")
print("  - color_personalday_condition_report.txt")
