#!/usr/bin/env python3
"""
Populate Player-Specific Layer Tables from ANALYSIS_v2

Tier 1: player_baseline (career stats)
Tier 2: player_by_condition, player_by_round_type, player_by_color, player_by_element, player_by_exec_upside, player_by_zodiac
Tier 3: player_by_condition_roundtype, player_by_color_element, player_by_exec_upside_zodiac

Priority 1 (MVP): Tier 1 + player_by_condition + player_by_round_type + player_by_condition_roundtype
Expected output: 5 CSV files ready for integration into scoring system
"""

import duckdb
import pandas as pd
from datetime import datetime
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

# Google Sheets connection (ANALYSIS_v2)
SHEET_ID = "1MhV3Fa1u6UHhEA8gGNqJ-BoGaNkNJPqfZqHmLQWhyqA"
SHEET_NAME = "ANALYSIS_v2"

# Output directory
OUTPUT_DIR = "D:\\Projects\\luckify-me\\player_tables"

# Thresholds
GOOD_THRESHOLD = -2.0   # diff_course_avg <= -2.0
BAD_THRESHOLD = 2.0     # diff_course_avg >= +2.0

print("="*80)
print("PLAYER-SPECIFIC LAYER POPULATION")
print("="*80)
print(f"Data source: ANALYSIS_v2 (Google Sheets)")
print(f"Output directory: {OUTPUT_DIR}")
print(f"Good threshold: <= {GOOD_THRESHOLD}")
print(f"Bad threshold: >= {BAD_THRESHOLD}")
print()

# =============================================================================
# LOAD DATA FROM GOOGLE SHEETS
# =============================================================================

print("[1/5] Loading ANALYSIS_v2 from Google Sheets...")

# Load from local export (created during ANALYSIS_v2 data population)
csv_path = 'D:\\Projects\\luckify-me\\analysis_v2_with_chinese_zodiac.csv'

try:
    df = pd.read_csv(csv_path)
    print(f"   [OK] Loaded {len(df):,} rows from {csv_path}")
    print(f"   [OK] Columns: {', '.join(df.columns[:10])}...")

except FileNotFoundError:
    print(f"   [!] CSV not found at {csv_path}")
    print(f"   [!] Make sure ANALYSIS_v2 with Chinese Zodiac is exported:")
    print(f"       {csv_path}")
    sys.exit(1)

except Exception as e2:
    print(f"   [!] Failed to load data: {e2}")
    sys.exit(1)

print()

# =============================================================================
# DATA VALIDATION
# =============================================================================

print("[2/5] Validating data...")

required_cols = ['player_name', 'diff_course_avg', 'condition', 'round_type',
                 'color', 'element', 'exec_bucket', 'upside_bucket', 'chinese_zodiac']

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    print(f"   [!] Missing columns: {missing_cols}")
    print(f"   Available columns: {df.columns.tolist()}")
else:
    print(f"   [OK] All required columns present")

# Clean data types
df['diff_course_avg'] = pd.to_numeric(df['diff_course_avg'], errors='coerce')
df['exec_bucket'] = pd.to_numeric(df['exec_bucket'], errors='coerce')
df['upside_bucket'] = pd.to_numeric(df['upside_bucket'], errors='coerce')

# Remove nulls in key columns
initial_count = len(df)
df = df.dropna(subset=['player_name', 'diff_course_avg'])
print(f"   [OK] {initial_count:,} -> {len(df):,} rows after removing nulls")

print()

# =============================================================================
# BUILD TIER 1: PLAYER BASELINE
# =============================================================================

print("[3/5] Building Tier 1: player_baseline...")

con = duckdb.connect(':memory:')

# Register dataframe
con.register('analysis', df)

baseline_query = """
SELECT
    player_name,
    COUNT(*) as career_events,
    ROUND(AVG(diff_course_avg), 3) as career_avg_score,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY diff_course_avg), 3) as career_median_score,
    ROUND(STDDEV_POP(diff_course_avg), 3) as career_std_dev,

    SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) as career_good_count,
    SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) as career_bad_count,
    SUM(CASE WHEN diff_course_avg > ? AND diff_course_avg < ? THEN 1 ELSE 0 END) as career_neutral_count,

    ROUND(SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as career_win_rate,
    ROUND(SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as career_loss_rate,

    ROUND(1 - (STDDEV_POP(diff_course_avg) / (MAX(diff_course_avg) - MIN(diff_course_avg))), 3) as career_consistency,
    ? as data_source

FROM analysis
GROUP BY player_name
ORDER BY career_events DESC
"""

baseline_df = con.execute(
    baseline_query,
    [GOOD_THRESHOLD, BAD_THRESHOLD, GOOD_THRESHOLD, BAD_THRESHOLD,
     GOOD_THRESHOLD, BAD_THRESHOLD, "ANALYSIS_v2"]
).fetchdf()

baseline_df.insert(0, 'player_id', range(1001, 1001 + len(baseline_df)))
baseline_df.insert(2, 'updated_at', datetime.now().isoformat())

print(f"   [OK] Created baseline for {len(baseline_df)} players")
print(f"   Sample:")
print(baseline_df[['player_id', 'player_name', 'career_events', 'career_avg_score', 'career_win_rate']].head(3).to_string(index=False))

player_id_map = dict(zip(baseline_df['player_name'], baseline_df['player_id']))

print()

# =============================================================================
# BUILD TIER 2 & 3: DIMENSIONAL BREAKDOWNS
# =============================================================================

print("[4/5] Building Tier 2-3 tables...")

def create_dimensional_table(dimension_col, table_name):
    """Generic function to create single-dimension breakdown tables"""

    query = f"""
    SELECT
        player_name,
        {dimension_col} as dimension_value,
        COUNT(*) as events,
        ROUND(AVG(diff_course_avg), 3) as avg_score,
        ROUND(SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as win_rate,
        SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) as good_count,
        SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) as bad_count
    FROM analysis
    WHERE {dimension_col} IS NOT NULL AND {dimension_col} != ''
    GROUP BY player_name, {dimension_col}
    ORDER BY player_name, events DESC
    """

    result_df = con.execute(query, [GOOD_THRESHOLD, GOOD_THRESHOLD, BAD_THRESHOLD]).fetchdf()
    result_df['player_id'] = result_df['player_name'].map(player_id_map)
    result_df = result_df[['player_id', 'player_name', 'dimension_value', 'events', 'avg_score', 'win_rate', 'good_count', 'bad_count']]

    return result_df

# Tier 2 tables
print("   Creating player_by_condition...")
player_by_condition = create_dimensional_table("condition", "player_by_condition")
print(f"      [OK] {len(player_by_condition)} rows")

print("   Creating player_by_round_type...")
player_by_round_type = create_dimensional_table("round_type", "player_by_round_type")
print(f"      [OK] {len(player_by_round_type)} rows")

print("   Creating player_by_color...")
player_by_color = create_dimensional_table("color", "player_by_color")
print(f"      [OK] {len(player_by_color)} rows")

print("   Creating player_by_element...")
player_by_element = create_dimensional_table("element", "player_by_element")
print(f"      [OK] {len(player_by_element)} rows")

print("   Creating player_by_exec_upside...")
query = """
SELECT
    player_name,
    CAST(exec_bucket AS INT) as exec_bucket,
    CAST(upside_bucket AS INT) as upside_bucket,
    COUNT(*) as events,
    ROUND(AVG(diff_course_avg), 3) as avg_score,
    ROUND(SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as win_rate,
    SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) as good_count,
    SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) as bad_count
FROM analysis
WHERE exec_bucket IS NOT NULL AND upside_bucket IS NOT NULL
GROUP BY player_name, exec_bucket, upside_bucket
ORDER BY player_name, events DESC
"""
player_by_exec_upside = con.execute(query, [GOOD_THRESHOLD, GOOD_THRESHOLD, BAD_THRESHOLD]).fetchdf()
player_by_exec_upside['player_id'] = player_by_exec_upside['player_name'].map(player_id_map)
player_by_exec_upside = player_by_exec_upside[['player_id', 'player_name', 'exec_bucket', 'upside_bucket', 'events', 'avg_score', 'win_rate', 'good_count', 'bad_count']]
print(f"      [OK] {len(player_by_exec_upside)} rows")

print("   Creating player_by_zodiac...")
player_by_zodiac = create_dimensional_table("chinese_zodiac", "player_by_zodiac")
player_by_zodiac = player_by_zodiac.rename(columns={'dimension_value': 'chinese_zodiac'})
print(f"      [OK] {len(player_by_zodiac)} rows")

# Tier 3 composite tables (highest priority)
print("   Creating player_by_condition_roundtype...")
query = """
SELECT
    player_name,
    condition,
    round_type,
    COUNT(*) as events,
    ROUND(AVG(diff_course_avg), 3) as avg_score,
    ROUND(SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as win_rate,
    SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) as good_count,
    SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) as bad_count
FROM analysis
WHERE condition IS NOT NULL AND condition != '' AND round_type IS NOT NULL AND round_type != ''
GROUP BY player_name, condition, round_type
ORDER BY player_name, events DESC
"""
player_by_condition_roundtype = con.execute(query, [GOOD_THRESHOLD, GOOD_THRESHOLD, BAD_THRESHOLD]).fetchdf()
player_by_condition_roundtype['player_id'] = player_by_condition_roundtype['player_name'].map(player_id_map)
player_by_condition_roundtype = player_by_condition_roundtype[['player_id', 'player_name', 'condition', 'round_type', 'events', 'avg_score', 'win_rate', 'good_count', 'bad_count']]
print(f"      [OK] {len(player_by_condition_roundtype)} rows")

print("   Creating player_by_color_element...")
query = """
SELECT
    player_name,
    color,
    element,
    COUNT(*) as events,
    ROUND(AVG(diff_course_avg), 3) as avg_score,
    ROUND(SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) / COUNT(*), 3) as win_rate,
    SUM(CASE WHEN diff_course_avg <= ? THEN 1 ELSE 0 END) as good_count,
    SUM(CASE WHEN diff_course_avg >= ? THEN 1 ELSE 0 END) as bad_count
FROM analysis
WHERE color IS NOT NULL AND color != '' AND element IS NOT NULL AND element != ''
GROUP BY player_name, color, element
ORDER BY player_name, events DESC
"""
player_by_color_element = con.execute(query, [GOOD_THRESHOLD, GOOD_THRESHOLD, BAD_THRESHOLD]).fetchdf()
player_by_color_element['player_id'] = player_by_color_element['player_name'].map(player_id_map)
player_by_color_element = player_by_color_element[['player_id', 'player_name', 'color', 'element', 'events', 'avg_score', 'win_rate', 'good_count', 'bad_count']]
print(f"      [OK] {len(player_by_color_element)} rows")

print()

# =============================================================================
# BUILD TIER 4: RECENT FORM
# =============================================================================

print("[5/5] Building Tier 4: player_recent_form...")

query = """
WITH ranked_events AS (
    SELECT
        player_name,
        diff_course_avg,
        ROW_NUMBER() OVER (PARTITION BY player_name ORDER BY event_date DESC, round_number DESC) as rn
    FROM analysis
    WHERE event_date IS NOT NULL
),
form_windows AS (
    SELECT
        player_name,
        -- Last 4 events
        ROUND(AVG(CASE WHEN rn <= 4 THEN diff_course_avg END), 3) as last_4_avg_score,
        COUNT(CASE WHEN rn <= 4 THEN 1 END) as last_4_events,
        ROUND(SUM(CASE WHEN rn <= 4 AND diff_course_avg <= ? THEN 1 ELSE 0 END) /
              NULLIF(COUNT(CASE WHEN rn <= 4 THEN 1 END), 0), 3) as last_4_win_rate,
        -- Last 8 events
        ROUND(AVG(CASE WHEN rn <= 8 THEN diff_course_avg END), 3) as last_8_avg_score,
        COUNT(CASE WHEN rn <= 8 THEN 1 END) as last_8_events,
        ROUND(SUM(CASE WHEN rn <= 8 AND diff_course_avg <= ? THEN 1 ELSE 0 END) /
              NULLIF(COUNT(CASE WHEN rn <= 8 THEN 1 END), 0), 3) as last_8_win_rate,
        -- Last 12 events
        ROUND(AVG(CASE WHEN rn <= 12 THEN diff_course_avg END), 3) as last_12_avg_score,
        COUNT(CASE WHEN rn <= 12 THEN 1 END) as last_12_events,
        ROUND(SUM(CASE WHEN rn <= 12 AND diff_course_avg <= ? THEN 1 ELSE 0 END) /
              NULLIF(COUNT(CASE WHEN rn <= 12 THEN 1 END), 0), 3) as last_12_win_rate
    FROM ranked_events
    GROUP BY player_name
)
SELECT
    player_name,
    last_4_avg_score,
    last_4_win_rate,
    last_4_events,
    last_8_avg_score,
    last_8_win_rate,
    last_8_events,
    last_12_avg_score,
    last_12_win_rate,
    last_12_events,
    ROUND(COALESCE(last_4_avg_score, 0) - (SELECT AVG(diff_course_avg) FROM analysis WHERE player_name = form_windows.player_name), 3) as momentum_4,
    ROUND(COALESCE(last_8_avg_score, 0) - (SELECT AVG(diff_course_avg) FROM analysis WHERE player_name = form_windows.player_name), 3) as momentum_8,
    ROUND(COALESCE(last_12_avg_score, 0) - (SELECT AVG(diff_course_avg) FROM analysis WHERE player_name = form_windows.player_name), 3) as momentum_12
FROM form_windows
ORDER BY player_name
"""

try:
    player_recent_form = con.execute(query, [GOOD_THRESHOLD, GOOD_THRESHOLD, GOOD_THRESHOLD]).fetchdf()

    # Add trend detection
    player_recent_form['trend_direction'] = player_recent_form.apply(
        lambda row: 'UP' if row['momentum_4'] > 0.3 else ('DOWN' if row['momentum_4'] < -0.3 else 'FLAT'),
        axis=1
    )

    player_recent_form['trend_strength'] = player_recent_form['momentum_4'].abs() / (player_recent_form['momentum_4'].abs().max() + 0.01)
    player_recent_form['trend_strength'] = player_recent_form['trend_strength'].clip(0, 1).round(2)

    player_recent_form['player_id'] = player_recent_form['player_name'].map(player_id_map)
    player_recent_form['updated_at'] = datetime.now().isoformat()

    # Reorder columns
    col_order = ['player_id', 'player_name', 'last_4_avg_score', 'last_4_win_rate', 'last_4_events',
                 'last_8_avg_score', 'last_8_win_rate', 'last_8_events',
                 'last_12_avg_score', 'last_12_win_rate', 'last_12_events',
                 'momentum_4', 'momentum_8', 'momentum_12', 'trend_direction', 'trend_strength', 'updated_at']
    player_recent_form = player_recent_form[col_order]

    print(f"   [OK] Created form tracking for {len(player_recent_form)} players")
    print(f"   Sample:")
    print(player_recent_form[['player_name', 'last_4_avg_score', 'momentum_4', 'trend_direction']].head(3).to_string(index=False))

except Exception as e:
    print(f"   [!] Error creating recent_form (continuing): {e}")
    player_recent_form = pd.DataFrame()

print()

# =============================================================================
# EXPORT TO CSV
# =============================================================================

print("Exporting to CSV...")

# Create output directory if needed
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = {
    'player_baseline.csv': baseline_df,
    'player_by_condition.csv': player_by_condition,
    'player_by_round_type.csv': player_by_round_type,
    'player_by_color.csv': player_by_color,
    'player_by_element.csv': player_by_element,
    'player_by_exec_upside.csv': player_by_exec_upside,
    'player_by_zodiac.csv': player_by_zodiac,
    'player_by_condition_roundtype.csv': player_by_condition_roundtype,
    'player_by_color_element.csv': player_by_color_element,
    'player_recent_form.csv': player_recent_form,
}

for filename, data in files.items():
    path = f"{OUTPUT_DIR}\\{filename}"
    data.to_csv(path, index=False)
    print(f"  [OK] {filename:40s} ({len(data):6,} rows)")

print()
print("="*80)
print("SUCCESS: All player tables created")
print("="*80)
print()
print("NEXT STEPS:")
print("1. Review the CSV files in:", OUTPUT_DIR)
print("2. Validate data quality (spot-check against raw ANALYSIS_v2)")
print("3. Integrate player_baseline into player_scoring_system.py")
print("4. Update scoring formula to blend model scores + player historical rates")
print()
