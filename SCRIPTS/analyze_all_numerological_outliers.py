import csv
from datetime import datetime
from collections import defaultdict
import math

def reduce_to_single(num):
    if num <= 0:
        return None
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

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

# Read PLAYERS
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        player = row[2].strip() if len(row) > 2 else ''
        birth = row[10].strip() if len(row) > 10 else ''
        if player and birth and player not in players_birth:
            try:
                birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                players_birth[player] = {'month': birth_obj.month, 'day': birth_obj.day, 'year': birth_obj.year}
            except:
                pass

print(f"Loaded {len(players_birth)} players\n")

# Read Golf_Analytics
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"
all_records = []

with open(golf_analytics_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in enumerate(reader, 2):
        if not row[1] or len(row[1]) < 71:
            continue

        try:
            player = row[1][2].strip()
            year = int(row[1][0].strip()) if row[1][0].strip().isdigit() else None

            if not player or not year or player not in players_birth:
                continue

            birth_info = players_birth[player]
            birth_month = birth_info['month']
            birth_day = birth_info['day']

            life_path_str = row[1][62].strip() if len(row[1]) > 62 else ''
            life_path = int(life_path_str) if life_path_str and life_path_str.isdigit() else None

            tournament_type = row[1][70].strip() if len(row[1]) > 70 else ''
            ttype = tournament_type if tournament_type in ['S', 'NS'] else 'Other'

            score_str = row[1][3].strip() if len(row[1]) > 3 else ''
            vs_avg_str = row[1][38].strip() if len(row[1]) > 38 else ''

            if not score_str or score_str in ['', '#REF!', 'Withdrawn', 'Cut']:
                continue
            if not vs_avg_str or vs_avg_str in ['', '#REF!']:
                continue

            try:
                score = float(score_str)
                vs_avg = float(vs_avg_str)
            except:
                continue

            date_str = row[1][12].strip() if len(row[1]) > 12 else ''
            if not date_str:
                continue

            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                event_month = date_obj.month
                event_day = date_obj.day
            except:
                continue

            condition = row[1][42].strip() if len(row[1]) > 42 else ''
            round_type = row[1][46].strip() if len(row[1]) > 46 else ''

            if not condition or not round_type:
                continue

            if 'calm' in condition.lower():
                cond = 'Calm'
            elif 'moderate' in condition.lower():
                cond = 'Moderate'
            elif 'tough' in condition.lower():
                cond = 'Tough'
            else:
                continue

            if 'open' in round_type.lower():
                rtype = 'Open'
            elif 'positioning' in round_type.lower():
                rtype = 'Positioning'
            elif 'closing' in round_type.lower():
                rtype = 'Closing'
            else:
                continue

            # Calculate all numerological values
            py = reduce_to_single(birth_month + birth_day + year)
            pm = reduce_to_single(birth_month + event_month)
            pd = reduce_to_single(event_month + event_day + py)

            py_master = reduce_with_master(birth_month + birth_day + year)
            pm_master = reduce_with_master(birth_month + event_month)
            pd_master = reduce_with_master(event_month + event_day + py)

            # Build comprehensive record
            record = {
                'cond': cond,
                'ttype': ttype,
                'rtype': rtype,
                'lp': life_path,
                'pm': pm,
                'pd': pd,
                'py': py,
                'pm_master': pm_master,
                'pd_master': pd_master,
                'py_master': py_master,
                'vs_avg': vs_avg,
                'above_2': 1 if vs_avg > 2 else 0,
                'below_neg2': 1 if vs_avg < -2 else 0,
                'between': 1 if -2 <= vs_avg <= 2 else 0,
            }

            # Numerological attributes
            if life_path:
                record['lp_parity'] = 'Odd' if life_path % 2 == 1 else 'Even'
                record['lp_cardinal'] = 'Cardinal' if life_path in [1, 4, 7] else 'Non-Cardinal'
                record['lp_cycle'] = 'Early' if life_path in [1, 2, 3] else 'Middle' if life_path in [4, 5, 6] else 'Late'

            if pm:
                record['pm_parity'] = 'Odd' if pm % 2 == 1 else 'Even'
                record['pm_is_master'] = pm_master in [11, 22, 33]

            if pd:
                record['pd_parity'] = 'Odd' if pd % 2 == 1 else 'Even'
                record['pd_is_master'] = pd_master in [11, 22, 33]

            if py:
                record['py_parity'] = 'Odd' if py % 2 == 1 else 'Even'
                record['py_is_master'] = py_master in [11, 22, 33]

            all_records.append(record)

        except (ValueError, IndexError):
            continue

print(f"Loaded {len(all_records)} records\n")

# ============================================================================
# OUTLIER ANALYSIS: Find combinations that deviate significantly
# ============================================================================

def find_outliers_for_dimension(records, filter_keys, metric_name='lp'):
    """
    Find outliers: combinations where performance deviates from baseline
    """
    if not records or len(records) < 10:
        return None

    # Calculate baseline
    baseline_above_2_pct = sum(r['above_2'] for r in records) / len(records) * 100
    baseline_below_neg2_pct = sum(r['below_neg2'] for r in records) / len(records) * 100
    baseline_between_pct = sum(r['between'] for r in records) / len(records) * 100
    baseline_vs_avg = sum(r['vs_avg'] for r in records) / len(records)

    # Break down by metric value
    by_value = defaultdict(list)
    for r in records:
        value = r.get(metric_name)
        if value:
            by_value[value].append(r)

    outliers = []

    for value, subset in by_value.items():
        if len(subset) < 5:
            continue

        # Calculate metrics
        above_2_pct = sum(r['above_2'] for r in subset) / len(subset) * 100
        below_neg2_pct = sum(r['below_neg2'] for r in subset) / len(subset) * 100
        between_pct = sum(r['between'] for r in subset) / len(subset) * 100
        vs_avg = sum(r['vs_avg'] for r in subset) / len(subset)

        # Deviation from baseline
        deviation_above = above_2_pct - baseline_above_2_pct
        deviation_below = below_neg2_pct - baseline_below_neg2_pct
        deviation_vs_avg = vs_avg - baseline_vs_avg

        # Flag outliers (deviation > 5pp or > 0.15 vs_avg)
        is_outlier = abs(deviation_above) > 5 or abs(deviation_below) > 5 or abs(deviation_vs_avg) > 0.15

        if is_outlier:
            outliers.append({
                'value': value,
                'n': len(subset),
                'above_2_pct': above_2_pct,
                'below_neg2_pct': below_neg2_pct,
                'between_pct': between_pct,
                'vs_avg': vs_avg,
                'dev_above': deviation_above,
                'dev_below': deviation_below,
                'dev_vs_avg': deviation_vs_avg,
                'baseline_above': baseline_above_2_pct,
                'baseline_below': baseline_below_neg2_pct,
                'baseline_vs_avg': baseline_vs_avg,
            })

    return sorted(outliers, key=lambda x: abs(x['dev_vs_avg']), reverse=True)

# ============================================================================
# SYSTEMATIC OUTLIER SEARCH
# ============================================================================

print("=" * 160)
print("COMPREHENSIVE NUMEROLOGICAL OUTLIER ANALYSIS (+2/-2 Thresholds)")
print("=" * 160)

all_outliers = []

# For each base dimension combo, find outliers across ALL numerological attributes
for cond in ['Calm', 'Moderate', 'Tough']:
    for ttype in ['S', 'NS']:
        for rtype in ['Open', 'Positioning', 'Closing']:
            # Filter to this dimension
            base_data = [r for r in all_records if r['cond'] == cond and r['ttype'] == ttype and r['rtype'] == rtype]

            if len(base_data) < 20:
                continue

            print(f"\n{cond} + {ttype} + {rtype} (n={len(base_data)} rounds)")
            print("-" * 160)

            # Check each numerological metric
            metrics_to_check = [
                ('lp', 'Life Path'),
                ('pm', 'Personal Month'),
                ('pd', 'Personal Day'),
                ('py', 'Personal Year'),
            ]

            for metric_key, metric_label in metrics_to_check:
                outliers = find_outliers_for_dimension(base_data, None, metric_key)

                if not outliers:
                    continue

                print(f"\n  {metric_label} OUTLIERS:")
                for outlier in outliers[:3]:  # Top 3
                    dev_sign = '+' if outlier['dev_vs_avg'] > 0 else ''
                    conf = 'HIGH' if outlier['n'] >= 50 else 'MEDIUM' if outlier['n'] >= 20 else 'LOW'

                    print(f"    {metric_label[0]}{outlier['value']}: " +
                          f"vs_avg={outlier['vs_avg']:>+.2f} (baseline {outlier['baseline_vs_avg']:>+.2f}, " +
                          f"dev={dev_sign}{outlier['dev_vs_avg']:+.2f}) | " +
                          f"Above+2: {outlier['above_2_pct']:.0f}% (base {outlier['baseline_above']:.0f}%) | " +
                          f"n={outlier['n']} [{conf}]")

                    all_outliers.append({
                        'combo': f"{cond}+{ttype}+{rtype}",
                        'metric': f"{metric_label[0]}{outlier['value']}",
                        'vs_avg': outlier['vs_avg'],
                        'dev_vs_avg': outlier['dev_vs_avg'],
                        'above_2_pct': outlier['above_2_pct'],
                        'n': outlier['n'],
                        'confidence': conf,
                    })

# ============================================================================
# SUMMARY: TOP OUTLIERS ACROSS ALL DIMENSIONS
# ============================================================================

print("\n\n" + "=" * 160)
print("TOP 30 OUTLIERS (Ranked by Deviation)")
print("=" * 160)

sorted_outliers = sorted(all_outliers, key=lambda x: abs(x['dev_vs_avg']), reverse=True)

print(f"\n{'Dimension':<25} {'Metric':<10} {'vs_avg':<10} {'Deviation':<12} {'Above+2%':<10} {'Sample':<10} {'Confidence':<12}")
print("-" * 160)

for i, outlier in enumerate(sorted_outliers[:30], 1):
    print(f"{i:2d}. {outlier['combo']:<22} {outlier['metric']:<10} " +
          f"{outlier['vs_avg']:>+.2f}     {outlier['dev_vs_avg']:>+.2f}pp    " +
          f"{outlier['above_2_pct']:>5.0f}%     n={outlier['n']:<4d}   {outlier['confidence']:<12}")

# ============================================================================
# CATEGORY: STRONG POSITIVE OUTLIERS (Beat expectations significantly)
# ============================================================================

print("\n\n" + "=" * 160)
print("STRONG POSITIVE OUTLIERS (Performance Exceeds Expectations)")
print("=" * 160)

positive_outliers = [o for o in sorted_outliers if o['dev_vs_avg'] > 0.15]

for outlier in positive_outliers[:15]:
    print(f"{outlier['combo']:<25} {outlier['metric']:<10} " +
          f"vs_avg={outlier['vs_avg']:>+.2f} (+{outlier['dev_vs_avg']:.2f}pp above baseline) " +
          f"| Above+2: {outlier['above_2_pct']:.0f}% | n={outlier['n']} [{outlier['confidence']}]")

# ============================================================================
# CATEGORY: STRONG NEGATIVE OUTLIERS (Underperform expectations)
# ============================================================================

print("\n\n" + "=" * 160)
print("STRONG NEGATIVE OUTLIERS (Performance Lags Expectations)")
print("=" * 160)

negative_outliers = [o for o in sorted_outliers if o['dev_vs_avg'] < -0.15]

for outlier in negative_outliers[:15]:
    print(f"{outlier['combo']:<25} {outlier['metric']:<10} " +
          f"vs_avg={outlier['vs_avg']:>+.2f} ({outlier['dev_vs_avg']:.2f}pp below baseline) " +
          f"| Above+2: {outlier['above_2_pct']:.0f}% | n={outlier['n']} [{outlier['confidence']}]")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n\n" + "=" * 160)
print("SUMMARY STATISTICS")
print("=" * 160)

high_conf = [o for o in sorted_outliers if o['confidence'] == 'HIGH']
med_conf = [o for o in sorted_outliers if o['confidence'] == 'MEDIUM']
low_conf = [o for o in sorted_outliers if o['confidence'] == 'LOW']

positive = [o for o in sorted_outliers if o['dev_vs_avg'] > 0.15]
negative = [o for o in sorted_outliers if o['dev_vs_avg'] < -0.15]

print(f"""
Total Outliers Found: {len(sorted_outliers)}

By Confidence:
  HIGH (n>=50):     {len(high_conf)} ({len(high_conf)/len(sorted_outliers)*100:.0f}%)
  MEDIUM (n>=20):   {len(med_conf)} ({len(med_conf)/len(sorted_outliers)*100:.0f}%)
  LOW (n<20):       {len(low_conf)} ({len(low_conf)/len(sorted_outliers)*100:.0f}%)

By Direction:
  Positive (beat baseline): {len(positive)} ({len(positive)/len(sorted_outliers)*100:.0f}%)
  Negative (lag baseline):  {len(negative)} ({len(negative)/len(sorted_outliers)*100:.0f}%)

Strongest Signal (Highest Deviation):
  Combo: {sorted_outliers[0]['combo']}
  Metric: {sorted_outliers[0]['metric']}
  vs_avg: {sorted_outliers[0]['vs_avg']:+.2f}
  Deviation: {sorted_outliers[0]['dev_vs_avg']:+.2f}pp
  Confidence: {sorted_outliers[0]['confidence']}
  Sample: n={sorted_outliers[0]['n']}
""")

print("=" * 160)
