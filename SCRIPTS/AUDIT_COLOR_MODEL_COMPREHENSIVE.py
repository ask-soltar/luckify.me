"""
COMPREHENSIVE AUDIT: Color-Based Top 40 Prediction Model
Check every assumption, filter, calculation, and potential source of bias
"""

import pandas as pd
import numpy as np

df_raw = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

print("=" * 180)
print("COMPREHENSIVE MODEL AUDIT: COLOR PREDICTION FOR TOP 40")
print("=" * 180)

# ============================================================================
# AUDIT 1: Data Quality and Filters
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 1: DATA QUALITY AND FILTERS")
print("=" * 180)

print(f"\nRaw data:")
print(f"  Total records: {len(df_raw)}")
print(f"  Date range: {df_raw['year'].min():.0f} - {df_raw['year'].max():.0f}")
print(f"  Columns: {list(df_raw.columns)}")

print(f"\nTournament type distribution:")
print(df_raw['tournament_type'].value_counts())

print(f"\nRound type distribution:")
print(df_raw['round_type'].value_counts())

print(f"\nAfter filtering to tournament_type=='S' and round_type!='REMOVE':")
df_filtered = df_raw[(df_raw['tournament_type'] == 'S') & (df_raw['round_type'] != 'REMOVE')].copy()
print(f"  Records: {len(df_filtered)} ({len(df_filtered)/len(df_raw)*100:.1f}% of raw)")

print(f"\nWhat are we EXCLUDING?")
excluded = df_raw[(df_raw['tournament_type'] != 'S') | (df_raw['round_type'] == 'REMOVE')]
print(f"  Non-S tournaments: {(df_raw['tournament_type'] != 'S').sum()} records")
print(f"  REMOVE rounds: {(df_raw['round_type'] == 'REMOVE').sum()} records")
print(f"  Total excluded: {len(excluded)} ({len(excluded)/len(df_raw)*100:.1f}%)")

# ============================================================================
# AUDIT 2: Color Assignment Logic
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 2: COLOR ASSIGNMENT LOGIC")
print("=" * 180)

print(f"\nQuestion: How many rounds does each player play per (event, year)?")
sample_player_event = df_filtered[df_filtered['event_name'] == df_filtered['event_name'].iloc[0]]
sample_player = sample_player_event[sample_player_event['player_name'] == sample_player_event['player_name'].iloc[0]]
print(f"\nSample: {sample_player_event['event_name'].iloc[0]}, {sample_player['player_name'].iloc[0] if len(sample_player) > 0 else 'N/A'}")
print(f"  Records: {len(sample_player)}")
print(f"  Round numbers: {sorted(sample_player['round_num'].unique())}")

print(f"\nColor distribution within sample player:")
if len(sample_player) > 0:
    print(df_filtered[['player_name', 'event_name', 'round_num', 'color']].head(20))

print(f"\n[AUDIT QUESTION] For each player-event-round combo, is there exactly 1 record?")
player_event_round_counts = df_filtered.groupby(['player_name', 'event_name', 'year', 'round_num']).size()
print(f"  Distribution of records per player-event-round:")
print(f"    Min: {player_event_round_counts.min()}")
print(f"    Max: {player_event_round_counts.max()}")
print(f"    Mean: {player_event_round_counts.mean():.2f}")
if (player_event_round_counts > 1).sum() > 0:
    print(f"    [WARNING] {(player_event_round_counts > 1).sum()} combos have >1 record (duplicates?)")
    print(f"    Examples:")
    print(player_event_round_counts[player_event_round_counts > 1].head())

# ============================================================================
# AUDIT 3: The Core Metric - vs_avg
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 3: THE CORE METRIC - vs_avg")
print("=" * 180)

print(f"\n[CRITICAL] What exactly is vs_avg?")
print(f"  Definition from earlier: Score vs venue field average (NOT par)")
print(f"  Used for: Ranking players within each tournament")

print(f"\nDistribution of vs_avg:")
print(f"  Min: {df_filtered['vs_avg'].min():.3f}")
print(f"  Max: {df_filtered['vs_avg'].max():.3f}")
print(f"  Mean: {df_filtered['vs_avg'].mean():.3f}")
print(f"  Median: {df_filtered['vs_avg'].median():.3f}")
print(f"  Std Dev: {df_filtered['vs_avg'].std():.3f}")
print(f"  NaN values: {df_filtered['vs_avg'].isna().sum()}")

print(f"\nSample vs_avg values:")
print(df_filtered[['player_name', 'event_name', 'round_num', 'score', 'vs_avg']].head(10))

print(f"\n[AUDIT QUESTION] Is vs_avg actually field-relative, or is it something else?")
print(f"  Checking: Do higher vs_avg values correlate with better finishing positions?")

# Check a single tournament
sample_event = df_filtered['event_name'].iloc[0]
sample_year = df_filtered[df_filtered['event_name'] == sample_event]['year'].iloc[0]
sample_round = 1
sample_data = df_filtered[(df_filtered['event_name'] == sample_event) &
                          (df_filtered['year'] == sample_year) &
                          (df_filtered['round_num'] == sample_round)].copy()

if len(sample_data) > 0:
    sample_data = sample_data.sort_values('vs_avg', ascending=False)
    print(f"\nSample event: {sample_event} {sample_year:.0f}, R{sample_round}")
    print(f"  Top 5 by vs_avg:")
    print(sample_data[['player_name', 'score', 'vs_avg']].head(5))
    print(f"  Bottom 5 by vs_avg:")
    print(sample_data[['player_name', 'score', 'vs_avg']].tail(5))

# ============================================================================
# AUDIT 4: Top 40 Definition
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 4: TOP 40 DEFINITION")
print("=" * 180)

print(f"\n[CRITICAL QUESTION] Is 'top 40' literally 40 players, or a percentage?")
print(f"  Our approach: literally 40 players (regardless of field size)")
print(f"  This means: top 40 of 100 = 40%, top 40 of 160 = 25%, top 40 of 50 = 80%")

print(f"\nField size distribution:")
for year in sorted(df_filtered['year'].unique()):
    year_data = df_filtered[df_filtered['year'] == year]
    r1_fields = []
    for event in year_data['event_name'].unique():
        event_data = year_data[year_data['event_name'] == event]
        r1_count = len(event_data[event_data['round_num'] == 1]['player_name'].unique())
        if r1_count > 0:
            r1_fields.append(r1_count)
    if r1_fields:
        print(f"  {year:.0f}: R1 avg field = {np.mean(r1_fields):.0f} (range {min(r1_fields)}-{max(r1_fields)})")

print(f"\n[AUDIT QUESTION] Should we use fixed 40 players, or fixed percentage (e.g., top 33%)?")
print(f"  Recommendation: Use PERCENTAGE for consistency across different field sizes")

# ============================================================================
# AUDIT 5: Circular Logic Check
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 5: CIRCULAR LOGIC CHECK")
print("=" * 180)

print(f"\nOur methodology:")
print(f"  1. Rank players by vs_avg (how much they beat field average)")
print(f"  2. Take top 40")
print(f"  3. Check: what % have each color?")
print(f"  4. Score = finish_rate - mean")

print(f"\n[AUDIT QUESTION] Are we using the SAME metric to filter and rank?")
print(f"  vs_avg = score - field_avg")
print(f"  Ranking by vs_avg = directly using this metric")
print(f"  Result: We're ranking by the same thing we're analyzing")
print(f"  Potential issue: If color correlated with score (not vs_avg), we'd miss it")

print(f"\n[RECOMMENDATION] Also test with alternative ranking metrics:")
print(f"  - Rank by actual score (not vs_avg)")
print(f"  - Rank by off_par (score - par)")
print(f"  - Compare results to check for robustness")

# ============================================================================
# AUDIT 6: Sample Size and Statistical Validity
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 6: SAMPLE SIZE AND STATISTICAL VALIDITY")
print("=" * 180)

print(f"\nFor R2, color distribution:")
r2_data = df_filtered[df_filtered['round_num'] == 2]
r2_by_event_year = []

for event in df_filtered['event_name'].unique():
    for year in df_filtered[df_filtered['event_name'] == event]['year'].unique():
        event_year = r2_data[(r2_data['event_name'] == event) & (r2_data['year'] == year)]
        if len(event_year) >= 30:
            for color in event_year['color'].unique():
                color_count = len(event_year[event_year['color'] == color])
                r2_by_event_year.append({
                    'color': color,
                    'count': color_count,
                })

if r2_by_event_year:
    r2_dist = pd.DataFrame(r2_by_event_year).groupby('color')['count'].describe()
    print(f"\nColor counts per tournament instance (R2):")
    print(r2_dist)

print(f"\n[AUDIT QUESTION] Minimum sample size:")
print(f"  Brown in R4: only {30} records across entire dataset")
print(f"  Can we trust a signal from 30 records? Probably not.")
print(f"  Recommendation: Only use colors with 500+ records minimum")

# ============================================================================
# AUDIT 7: Confounding Factors
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 7: CONFOUNDING FACTORS")
print("=" * 180)

print(f"\n[AUDIT QUESTION] Does color correlate with other predictive factors?")

# Check if color correlates with skill level
print(f"\nDo good players have certain colors?")
df_filtered['quality'] = df_filtered['vs_avg']  # Higher = better
color_quality = df_filtered.groupby('color')['quality'].agg(['mean', 'count'])
print(color_quality.sort_values('mean', ascending=False))

print(f"\n[CRITICAL] If certain colors appear more often in good players,")
print(f"we're not measuring color effect, we're measuring player quality!")

# Check if color varies by tournament/season
print(f"\nDo certain colors dominate certain tournaments?")
for event in df_filtered['event_name'].unique()[:5]:
    event_data = df_filtered[df_filtered['event_name'] == event]
    color_pct = (event_data['color'].value_counts() / len(event_data) * 100).round(1)
    print(f"  {event}: {dict(color_pct)}")

# ============================================================================
# AUDIT 8: Out-of-Sample Validation
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 8: OUT-OF-SAMPLE VALIDATION")
print("=" * 180)

print(f"\n[CRITICAL] Have we tested this model on data it hasn't seen?")
print(f"  Current approach: Analyze all 2022-2025 data, assume pattern holds")
print(f"  Problem: If we run the model on 2024-2025, does it predict 2025 better?")
print(f"  Solution: Train on 2022-2024, test on 2025")

print(f"\nYear distribution in dataset:")
print(df_filtered['year'].value_counts().sort_index())

# ============================================================================
# AUDIT 9: Effect Size vs Noise
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT 9: EFFECT SIZE vs NOISE")
print("=" * 180)

print(f"\nAfter frequency adjustment:")
print(f"  Most color edges: ±0.00 to ±0.03 (essentially zero)")
print(f"  Exception: A few rare colors have ±0.05-0.10 edges")
print(f"  But rare colors are unreliable (30-100 records)")

print(f"\n[CRITICAL QUESTION] Are we detecting real signal, or statistical noise?")
print(f"  With 30+ tournaments × 4 rounds × 8 colors = 960 independent tests")
print(f"  Chance of finding spurious signal (Type I error): Very high!")
print(f"  Recommendation: Apply Bonferroni correction or use very strict p-values")

# ============================================================================
# AUDIT 10: Summary
# ============================================================================

print(f"\n{'=' * 180}")
print("AUDIT SUMMARY: CRITICAL ISSUES")
print("=" * 180)

issues = [
    ("TOP 40 DEFINITION", "Using fixed 40 players (not %) means top 40 is 25%-80% depending on field"),
    ("CIRCULAR LOGIC", "Ranking by vs_avg directly; should test with alternative metrics"),
    ("SAMPLE SIZE", "Rare colors (Brown=30, Pink=108) too small for reliable signals"),
    ("CONFOUNDING", "Better players may have certain colors; color effect may be proxy for skill"),
    ("STATISTICAL VALIDITY", "960+ independent tests; high chance of Type I error (false positives)"),
    ("OUT-OF-SAMPLE", "No validation on future data; may not generalize"),
    ("EFFECT SIZE", "Most edges ±0.00-0.03; barely above noise after frequency adjustment"),
]

for i, (issue, description) in enumerate(issues, 1):
    print(f"\n{i}. {issue}")
    print(f"   {description}")

print(f"\n{'=' * 180}")
print("VERDICT")
print("=" * 180)

print(f"""
The current model has SIGNIFICANT WEAKNESSES:

1. Effect sizes are too small (0-3%) to be reliable after adjustment
2. Circular logic in ranking metric (vs_avg) needs verification
3. Rare colors unreliable; should exclude colors with <500 records
4. Confounding factors not controlled (skill level correlates with color?)
5. No out-of-sample validation

RECOMMENDATION:
Before using this model for betting, we should:
a) Train on 2022-2024, test predictions on 2025 data
b) Control for player skill level
c) Use percentage-based top 40 (not fixed 40 players)
d) Only include colors with 500+ sample size
e) Compare vs alternative ranking metrics (actual score, off_par)
f) Apply statistical corrections for multiple testing

CURRENT STATUS: NOT READY FOR PRODUCTION
""")

print("\n")
