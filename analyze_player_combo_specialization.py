#!/usr/bin/env python3
"""
Identify Player Combo Specializations

For each player, find combos where they OUTPERFORM their baseline
These are betting targets: book prices baseline, we know the combo advantage

Approach:
1. Player baseline in condition (e.g., Rory in Calm: 60%)
2. Player in specific combo (e.g., Rory in Calm+Positioning+Green+Metal: 75%)
3. Delta = +15pp = Player specialty, book misprices
"""

import pandas as pd
import duckdb

print("="*100)
print("PLAYER COMBO SPECIALIZATION ANALYSIS")
print("="*100)
print()

# Load
csv_path = 'D:\\Projects\\luckify-me\\analysis_v2_with_chinese_zodiac.csv'
df = pd.read_csv(csv_path)

df['diff_course_avg'] = pd.to_numeric(df['diff_course_avg'], errors='coerce')
df['exec_bucket'] = pd.to_numeric(df['exec_bucket'], errors='coerce')
df['upside_bucket'] = pd.to_numeric(df['upside_bucket'], errors='coerce')
df = df.dropna(subset=['player_name', 'diff_course_avg', 'condition', 'round_type'])

df['is_good'] = df['diff_course_avg'] <= -2.0

print(f"[OK] {len(df):,} records, {df['player_name'].nunique()} players")

# Focus on Calm (most data)
calm = df[df['condition'] == 'Calm'].copy()
print(f"[OK] {len(calm):,} Calm records\n")

# DuckDB aggregation
con = duckdb.connect(':memory:')
con.register('calm', calm)

# Step 1: Player baseline by condition
baseline_query = """
SELECT
    player_name,
    'Calm' as condition,
    COUNT(*) as baseline_events,
    ROUND(SUM(CASE WHEN is_good THEN 1 ELSE 0 END) / COUNT(*), 3) as baseline_wr
FROM calm
GROUP BY player_name
"""

baseline = con.execute(baseline_query).fetchdf()
print(f"[*] Step 1: Player baselines in Calm condition")
print(f"    {len(baseline)} players with Calm records")
print(f"    Median baseline WR: {baseline['baseline_wr'].median()*100:.1f}%\n")

# Step 2: Player performance in specific combos
combo_query = """
SELECT
    player_name,
    condition,
    round_type,
    color,
    element,
    CAST(exec_bucket AS INT) as exec_bucket,
    CAST(upside_bucket AS INT) as upside_bucket,
    chinese_zodiac,
    COUNT(*) as combo_events,
    ROUND(SUM(CASE WHEN is_good THEN 1 ELSE 0 END) / COUNT(*), 3) as combo_wr
FROM calm
WHERE color IS NOT NULL AND color != ''
  AND element IS NOT NULL AND element != ''
  AND chinese_zodiac IS NOT NULL AND chinese_zodiac != ''
  AND round_type IS NOT NULL AND round_type != ''
GROUP BY player_name, condition, round_type, color, element, exec_bucket, upside_bucket, chinese_zodiac
HAVING COUNT(*) >= 5
"""

combos = con.execute(combo_query).fetchdf()
print(f"[*] Step 2: Player combo performance")
print(f"    {len(combos)} player-combo records (minimum 5 events)")
print(f"    Median combo events: {combos['combo_events'].median():.0f}\n")

# Step 3: Merge and calculate delta
print("[*] Step 3: Calculate specialization delta...")

# Merge baseline onto combos
combos = combos.merge(baseline[['player_name', 'baseline_wr']], on='player_name', how='left')

# Calculate delta
combos['delta'] = combos['combo_wr'] - combos['baseline_wr']
combos['delta_pct'] = (combos['delta'] * 100).round(1)

# Find specializations (positive deltas, significant sample)
specialists = combos[
    (combos['delta'] > 0.05) &  # At least +5pp above baseline
    (combos['combo_events'] >= 5)  # Minimum 5 events to be confident
].copy()

specialists = specialists.sort_values('delta', ascending=False)

print(f"    Found {len(specialists)} specialization opportunities (delta > +5pp)")
print(f"    Median delta: +{specialists['delta'].median()*100:.1f}pp\n")

# Step 4: Analyze top specializations
print("="*100)
print("TOP SPECIALIZATIONS (Where Book Likely Underprices)")
print("="*100)
print()

# Get top specialists by delta
top_specialists = specialists.nlargest(20, 'delta')

print(top_specialists[[
    'player_name', 'round_type', 'color', 'element', 'chinese_zodiac',
    'baseline_wr', 'combo_wr', 'delta_pct', 'combo_events'
]].to_string(index=False))

print()
print()

# Step 5: Understand the pattern
print("="*100)
print("PATTERN ANALYSIS")
print("="*100)
print()

# Which elements are strong?
elem_performance = specialists.groupby('element').agg({
    'delta': ['mean', 'count', 'max'],
    'combo_events': 'median'
}).round(3)
elem_performance.columns = ['avg_delta', 'count', 'max_delta', 'median_events']
elem_performance = elem_performance.sort_values('avg_delta', ascending=False)

print("Element performance (highest avg specialization):")
print(elem_performance.head(10))
print()

# Which round types?
rt_performance = specialists.groupby('round_type').agg({
    'delta': ['mean', 'count', 'max'],
}).round(3)
rt_performance.columns = ['avg_delta', 'count', 'max_delta']
rt_performance = rt_performance.sort_values('avg_delta', ascending=False)

print("Round Type performance:")
print(rt_performance)
print()

# Step 6: Create betting target list
print("="*100)
print("BETTING TARGETS: High Specialization + Confidence")
print("="*100)
print()

high_confidence = specialists[
    (specialists['delta'] >= 0.10) &  # At least +10pp
    (specialists['combo_events'] >= 8)  # Strong sample
].copy()

high_confidence = high_confidence.nlargest(30, 'delta')

if len(high_confidence) > 0:
    print(f"{len(high_confidence)} high-confidence targets found:\n")
    print(high_confidence[[
        'player_name', 'round_type', 'color', 'element',
        'baseline_wr', 'combo_wr', 'delta_pct', 'combo_events'
    ]].to_string(index=False))
else:
    print("No high-confidence targets (need delta >= +10pp AND events >= 8)")

print()

# Step 7: Export for integration
print("="*100)
print("EXPORT")
print("="*100)
print()

# Save all specializations
specialists.to_csv('D:\\Projects\\luckify-me\\player_combo_specializations.csv', index=False)
print(f"[OK] Exported {len(specialists)} specializations to player_combo_specializations.csv")

# Save high-confidence only
high_confidence.to_csv('D:\\Projects\\luckify-me\\player_combo_specializations_hc.csv', index=False)
print(f"[OK] Exported {len(high_confidence)} high-confidence targets to player_combo_specializations_hc.csv")

print()
print(f"Integration next: Use these combos in scoring system")
print(f"If player matches a specialization, boost their score by delta")
print()
