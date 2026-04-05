import csv
from datetime import datetime
import statistics
import math

def reduce_with_master(num):
    if num <= 0:
        return None
    if num in [11, 22, 33]:
        return num
    while num > 9:
        if num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num

# ============================================================================
# Load player birth data
# ============================================================================
players_birth = {}
with open("d:/Projects/luckify-me/Golf Historics v3 - Golf_Analytics.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        player = row[2].strip() if len(row) > 2 else ''
        birth = row[10].strip() if len(row) > 10 else ''
        if player and birth and player not in players_birth:
            try:
                birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                players_birth[player] = {'month': birth_obj.month, 'day': birth_obj.day, 'year': birth_obj.year}
            except:
                pass

# ============================================================================
# Extract Calm + Closing data
# ============================================================================

calm_closing_all = []
calm_closing_pd22 = []

with open("d:/Projects/luckify-me/Golf Historics v3 - Golf_Analytics.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)

    for row in reader:
        if not row or len(row) < 50:
            continue

        try:
            player = row[2].strip() if len(row) > 2 else ''
            if not player or player not in players_birth:
                continue

            # Process closing round (R4 = column 6)
            date_str = row[15].strip() if len(row) > 15 else ''  # P = R4 date
            score_str = row[6].strip() if len(row) > 6 else ''   # G = R4 score
            vs_avg_str = row[41].strip() if len(row) > 41 else ''  # AP = R4 vs_avg
            cond_str = row[45].strip() if len(row) > 45 else ''  # AT = R4 condition
            rtype_str = row[49].strip() if len(row) > 49 else ''  # AX = R4 round type

            if not date_str or score_str in ['', '#REF!', 'Withdrawn', 'Cut']:
                continue
            if vs_avg_str in ['', '#REF!']:
                continue
            if cond_str != 'Calm' or rtype_str != 'Closing':
                continue

            try:
                score = float(score_str)
                vs_avg = float(vs_avg_str)
                event_date = datetime.strptime(date_str, '%m/%d/%Y')
            except:
                continue

            # Calculate PD
            birth_info = players_birth[player]
            py = reduce_with_master(birth_info['month'] + birth_info['day'] + event_date.year)
            if not py:
                continue
            pd = reduce_with_master(event_date.month + event_date.day + py)

            record = {
                'player': player,
                'vs_avg': vs_avg,
                'score': score,
                'pd': pd,
                'date': date_str,
                'beat_field': 1 if vs_avg > 0 else 0,
            }

            calm_closing_all.append(record)

            if pd == 22:
                calm_closing_pd22.append(record)

        except (ValueError, IndexError):
            continue

print("=" * 140)
print("VALIDATION: CALM + CLOSING + PERSONAL DAY 22 SIGNAL")
print("=" * 140)
print()

if not calm_closing_all or not calm_closing_pd22:
    print("ERROR: Insufficient data")
    exit(1)

# ============================================================================
# Statistical Analysis
# ============================================================================

baseline_vs_avg = statistics.mean([r['vs_avg'] for r in calm_closing_all])
baseline_std = statistics.stdev([r['vs_avg'] for r in calm_closing_all])
baseline_n = len(calm_closing_all)

pd22_vs_avg = statistics.mean([r['vs_avg'] for r in calm_closing_pd22])
pd22_std = statistics.stdev([r['vs_avg'] for r in calm_closing_pd22]) if len(calm_closing_pd22) > 1 else 0
pd22_n = len(calm_closing_pd22)

baseline_wr = sum(r['beat_field'] for r in calm_closing_all) / baseline_n * 100
pd22_wr = sum(r['beat_field'] for r in calm_closing_pd22) / pd22_n * 100

edge_vs_avg = pd22_vs_avg - baseline_vs_avg

print("SAMPLE SIZE & DESCRIPTIVE STATISTICS:")
print(f"  Calm + Closing (Baseline): n={baseline_n}, vs_avg={baseline_vs_avg:+.3f} +/- {baseline_std:.3f}, WR={baseline_wr:.1f}%")
print(f"  Calm + Closing + PD22:     n={pd22_n}, vs_avg={pd22_vs_avg:+.3f} +/- {pd22_std:.3f}, WR={pd22_wr:.1f}%")
print()

# ============================================================================
# Statistical Significance Testing
# ============================================================================

# 1. T-Test (do means differ significantly?)
mean_diff = edge_vs_avg
pooled_std = math.sqrt((baseline_std**2 + pd22_std**2) / 2)
se = pooled_std * math.sqrt(1/baseline_n + 1/pd22_n)
t_stat = mean_diff / se if se > 0 else 0
df = baseline_n + pd22_n - 2

print("STATISTICAL SIGNIFICANCE (T-Test):")
print(f"  Mean difference: {edge_vs_avg:+.3f}")
print(f"  Standard error: {se:.3f}")
print(f"  t-statistic: {t_stat:.3f}")
print(f"  degrees of freedom: {df}")

# Approximate p-value for t-distribution (rough check)
# For df > 30 and |t| > 1.96, p < 0.05
if abs(t_stat) > 1.96:
    significance = "SIGNIFICANT (p < 0.05)"
elif abs(t_stat) > 1.645:
    significance = "MARGINALLY SIGNIFICANT (p < 0.10)"
else:
    significance = "NOT SIGNIFICANT (p >= 0.10)"

print(f"  Result: {significance}")
print()

# 2. Effect Size (Cohen's d)
cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
print("EFFECT SIZE (Cohen's d):")
print(f"  Cohen's d: {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    effect_label = "negligible"
elif abs(cohens_d) < 0.5:
    effect_label = "small"
elif abs(cohens_d) < 0.8:
    effect_label = "medium"
else:
    effect_label = "large"
print(f"  Interpretation: {effect_label} effect")
print()

# 3. Win Rate Edge (Binomial Test proxy)
p_baseline = baseline_wr / 100
p_pd22 = pd22_wr / 100
wr_diff = p_pd22 - p_baseline
se_wr = math.sqrt(p_baseline * (1 - p_baseline) / baseline_n + p_pd22 * (1 - p_pd22) / pd22_n)
z_stat = wr_diff / se_wr if se_wr > 0 else 0

print("WIN RATE EDGE (Z-Test):")
print(f"  Baseline WR: {baseline_wr:.1f}%")
print(f"  PD22 WR: {pd22_wr:.1f}%")
print(f"  Difference: {wr_diff*100:+.1f}pp")
print(f"  Z-statistic: {z_stat:.3f}")

if abs(z_stat) > 1.96:
    wr_significance = "SIGNIFICANT (p < 0.05)"
elif abs(z_stat) > 1.645:
    wr_significance = "MARGINALLY SIGNIFICANT (p < 0.10)"
else:
    wr_significance = "NOT SIGNIFICANT (p >= 0.10)"

print(f"  Result: {wr_significance}")
print()

# ============================================================================
# Confidence Intervals
# ============================================================================

print("CONFIDENCE INTERVALS (95%):")
# CI for mean difference
ci_lower = edge_vs_avg - 1.96 * se
ci_upper = edge_vs_avg + 1.96 * se
print(f"  vs_avg edge: [{ci_lower:+.3f}, {ci_upper:+.3f}]")

# CI for win rate difference
ci_wr_lower = wr_diff - 1.96 * se_wr
ci_wr_upper = wr_diff + 1.96 * se_wr
print(f"  WR edge: [{ci_wr_lower*100:+.1f}pp, {ci_wr_upper*100:+.1f}pp]")
print()

# ============================================================================
# Historical Stability (Year-by-year)
# ============================================================================

print("YEAR-BY-YEAR BREAKDOWN (Calm + Closing + PD22):")
print()

by_year = {}
for record in calm_closing_pd22:
    year = record['date'].split('/')[-1]  # Extract year from MM/DD/YYYY
    if year not in by_year:
        by_year[year] = []
    by_year[year].append(record)

for year in sorted(by_year.keys()):
    year_data = by_year[year]
    year_avg = statistics.mean([r['vs_avg'] for r in year_data])
    year_wr = sum(r['beat_field'] for r in year_data) / len(year_data) * 100
    print(f"  {year}: vs_avg={year_avg:+.3f}, WR={year_wr:.1f}%, n={len(year_data)}")

print()

# ============================================================================
# VERDICT
# ============================================================================

print("=" * 140)
print("VERDICT")
print("=" * 140)
print()

print("SIGNAL STRENGTH:")
if abs(cohens_d) >= 0.5:
    strength = "STRONG"
elif abs(cohens_d) >= 0.2:
    strength = "MODERATE"
else:
    strength = "WEAK"

print(f"  Effect size: {strength} (Cohen's d = {cohens_d:.3f})")

print("\nSTATISTICAL SIGNIFICANCE:")
print(f"  vs_avg edge: {significance}")
print(f"  WR edge: {wr_significance}")

print("\nPRACTICAL SIGNIFICANCE:")
if edge_vs_avg > 0:
    print(f"  +{edge_vs_avg:.3f} vs_avg edge per round")
    annual_edge = edge_vs_avg * 100 * 52  # Assume ~52 rounds/year
    print(f"  ~{annual_edge:.0f} points edge per season (52 rounds)")
    print(f"  Win rate: {pd22_wr:.1f}% vs {baseline_wr:.1f}% baseline = {wr_diff*100:+.1f}pp")
else:
    print(f"  {edge_vs_avg:.3f} vs_avg edge (NEGATIVE)")

print("\nRECOMMENDATION:")
if edge_vs_avg > 0 and pd22_n >= 100:
    print("  DEPLOYABLE - Sufficient sample size, positive edge, coherent context (Calm+Closing)")
elif edge_vs_avg > 0 and pd22_n >= 50:
    print("  MONITOR - Positive edge but moderate sample size; collect more data before high-conviction betting")
else:
    print("  EXPLORATORY - Interesting pattern but insufficient confidence for primary betting")

print()
