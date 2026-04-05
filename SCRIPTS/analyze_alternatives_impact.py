import csv
from datetime import datetime
from collections import defaultdict
import math

def reduce_to_single(num):
    """Reduce to single digit 1-9"""
    if num <= 0:
        return None
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

# Read PLAYERS sheet
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
                players_birth[player] = {
                    'month': birth_obj.month,
                    'day': birth_obj.day,
                    'year': birth_obj.year
                }
            except:
                pass

print(f"Loaded {len(players_birth)} players\n")

# Read Golf_Analytics
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"

data_by_dimensions = defaultdict(list)

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

            # Process R1 only for simplicity
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

            py = reduce_to_single(birth_month + birth_day + year)
            pm = reduce_to_single(birth_month + event_month)
            pd = reduce_to_single(event_month + event_day + py)

            record = {
                'lp': life_path,
                'pm': pm,
                'pd': pd,
                'py': py,
                'vs_avg': vs_avg,
                'beat_field': 1 if vs_avg > 0 else 0,
            }

            key = (cond, ttype, rtype)
            data_by_dimensions[key].append(record)

        except (ValueError, IndexError):
            continue

print(f"Processed {sum(len(v) for v in data_by_dimensions.values())} records\n")

# ============================================================================
# ALTERNATIVE 1: CONFIDENCE SCORING (Sample Size Adjustment)
# ============================================================================

print("=" * 140)
print("ALTERNATIVE 1: CONFIDENCE SCORING (Bayesian Shrinkage)")
print("=" * 140)

def analyze_with_confidence(data, metric_name):
    """Analyze with confidence intervals"""
    if not data:
        return None

    key = metric_name.lower()
    results = {}

    for value in range(1, 10):
        subset = [d for d in data if d[key] == value]
        if not subset or len(subset) < 3:
            continue

        n = len(subset)
        mean = sum(d['vs_avg'] for d in subset) / n
        variance = sum((d['vs_avg'] - mean) ** 2 for d in subset) / max(n - 1, 1)
        se = math.sqrt(variance / n) if n > 0 else 0
        ci_95 = 1.96 * se

        # Bayesian shrinkage: shrink noisy estimates toward grand mean
        grand_mean = sum(d['vs_avg'] for d in data) / len(data)
        reliability = n / (n + 30)  # More data = more weight to empirical mean
        shrunk_mean = reliability * mean + (1 - reliability) * grand_mean

        # Confidence flag
        if n < 30:
            confidence = "LOW"
        elif n < 100:
            confidence = "MEDIUM"
        elif n < 300:
            confidence = "HIGH"
        else:
            confidence = "VERY_HIGH"

        results[value] = {
            'n': n,
            'raw_mean': mean,
            'shrunk_mean': shrunk_mean,
            'ci_95': ci_95,
            'confidence': confidence,
        }

    return results

# Find a dimension combo with data
test_key = None
for key, data in data_by_dimensions.items():
    if len(data) > 100:
        test_key = key
        break

if not test_key:
    test_key = max(data_by_dimensions.items(), key=lambda x: len(x[1]))[0]

test_data = data_by_dimensions[test_key]

print(f"\nExample: {test_key[0]} + {test_key[1]} + {test_key[2]} ({len(test_data)} rounds)\n")
print(f"{'LP':<6} {'N':<6} {'Raw Mean':<12} {'95% CI':<12} {'Shrunk Mean':<12} {'Confidence':<12}")
print("-" * 80)

lp_results = analyze_with_confidence(test_data, 'lp')
for value in sorted(lp_results.keys()):
    r = lp_results[value]
    ci = f"+/- {r['ci_95']:.2f}"
    print(f"{value:<6} {r['n']:<6} {r['raw_mean']:>+.2f}      {ci:<12} {r['shrunk_mean']:>+.2f}       {r['confidence']:<12}")

# ============================================================================
# ALTERNATIVE 2: WIN RATE & KELLY ANALYSIS
# ============================================================================

print("\n\n" + "=" * 140)
print("ALTERNATIVE 2: WIN RATE & KELLY ANALYSIS (Betting Metrics)")
print("=" * 140)

def analyze_kelly(data, metric_name):
    """Analyze win rate and calculate Kelly optimal fraction"""
    if not data:
        return None

    key = metric_name.lower()
    results = {}

    for value in range(1, 10):
        subset = [d for d in data if d[key] == value]
        if not subset or len(subset) < 3:
            continue

        # Win rate (beat field average)
        wins = sum(d['beat_field'] for d in subset)
        win_rate = wins / len(subset)
        loss_rate = 1 - win_rate

        if win_rate < 0.01 or win_rate > 0.99:
            kelly = None  # Kelly undefined at extremes
        else:
            # Kelly = (p*b - q) / b where p=win%, q=loss%, b=odds
            # Simplified: Kelly = (p - q) / 2 for fair odds
            kelly = (win_rate - loss_rate)

        # Expected value: average win - average loss
        wins_subset = [d['vs_avg'] for d in subset if d['vs_avg'] > 0]
        loss_subset = [d['vs_avg'] for d in subset if d['vs_avg'] < 0]

        avg_win = sum(wins_subset) / len(wins_subset) if wins_subset else 0
        avg_loss = sum(loss_subset) / len(loss_subset) if loss_subset else 0
        ev = win_rate * avg_win - loss_rate * abs(avg_loss)

        results[value] = {
            'n': len(subset),
            'win_rate': win_rate * 100,
            'loss_rate': loss_rate * 100,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'ev': ev,
            'kelly_pct': kelly * 100 if kelly else None,
        }

    return results

print(f"\nExample: {test_key[0]} + {test_key[1]} + {test_key[2]} ({len(test_data)} rounds)\n")
print(f"{'LP':<6} {'WR%':<8} {'LR%':<8} {'Avg Win':<10} {'Avg Loss':<10} {'EV':<8} {'Kelly%':<10}")
print("-" * 90)

lp_kelly = analyze_kelly(test_data, 'lp')
for value in sorted(lp_kelly.keys()):
    r = lp_kelly[value]
    kelly_str = f"{r['kelly_pct']:.1f}%" if r['kelly_pct'] else "N/A"
    print(f"{value:<6} {r['win_rate']:>6.1f}% {r['loss_rate']:>6.1f}% {r['avg_win']:>+9.2f} {r['avg_loss']:>+9.2f} {r['ev']:>+7.2f} {kelly_str:<10}")

# ============================================================================
# ALTERNATIVE 3: METRIC SYNERGY ANALYSIS
# ============================================================================

print("\n\n" + "=" * 140)
print("ALTERNATIVE 3: METRIC SYNERGY (Combinations)")
print("=" * 140)

def analyze_synergy(data):
    """Test if metric combinations outperform individual metrics"""
    if not data or len(data) < 50:
        return None

    results = {}

    # Individual metric performance
    for metric_name in ['lp', 'pm', 'pd', 'py']:
        key = metric_name.lower()
        combos = defaultdict(list)

        for d in data:
            if d[key]:
                combos[d[key]].append(d)

        best_value = max(combos.items(), key=lambda x: sum(y['vs_avg'] for y in x[1]) / len(x[1]))
        results[metric_name] = {
            'best_value': best_value[0],
            'best_mean': sum(y['vs_avg'] for y in best_value[1]) / len(best_value[1]),
            'best_n': len(best_value[1]),
        }

    # Now test combination: best_lp + best_pm
    best_lp = results['lp']['best_value']
    best_pm = results['pm']['best_value']
    best_pd = results['pd']['best_value']
    best_py = results['py']['best_value']

    combo_lp_pm = [d for d in data if d['lp'] == best_lp and d['pm'] == best_pm]
    combo_lp_pd = [d for d in data if d['lp'] == best_lp and d['pd'] == best_pd]
    combo_all = [d for d in data if d['lp'] == best_lp and d['pm'] == best_pm and d['pd'] == best_pd and d['py'] == best_py]

    results['combo_lp+pm'] = {
        'mean': sum(d['vs_avg'] for d in combo_lp_pm) / len(combo_lp_pm) if combo_lp_pm else 0,
        'n': len(combo_lp_pm),
        'synergy': (sum(d['vs_avg'] for d in combo_lp_pm) / len(combo_lp_pm) if combo_lp_pm else 0) - (results['lp']['best_mean'] + results['pm']['best_mean']) / 2,
    }

    results['combo_lp+pd'] = {
        'mean': sum(d['vs_avg'] for d in combo_lp_pd) / len(combo_lp_pd) if combo_lp_pd else 0,
        'n': len(combo_lp_pd),
        'synergy': (sum(d['vs_avg'] for d in combo_lp_pd) / len(combo_lp_pd) if combo_lp_pd else 0) - (results['lp']['best_mean'] + results['pd']['best_mean']) / 2,
    }

    results['combo_all'] = {
        'mean': sum(d['vs_avg'] for d in combo_all) / len(combo_all) if combo_all else 0,
        'n': len(combo_all),
    }

    return results

print(f"\nExample: {test_key[0]} + {test_key[1]} + {test_key[2]} ({len(test_data)} rounds)\n")

synergy = analyze_synergy(test_data)

print("Individual Metrics (Best Values):")
print(f"  LP{synergy['lp']['best_value']}: {synergy['lp']['best_mean']:>+.2f} vs_avg (n={synergy['lp']['best_n']})")
print(f"  PM{synergy['pm']['best_value']}: {synergy['pm']['best_mean']:>+.2f} vs_avg (n={synergy['pm']['best_n']})")
print(f"  PD{synergy['pd']['best_value']}: {synergy['pd']['best_mean']:>+.2f} vs_avg (n={synergy['pd']['best_n']})")
print(f"  PY{synergy['py']['best_value']}: {synergy['py']['best_mean']:>+.2f} vs_avg (n={synergy['py']['best_n']})")

print(f"\nMetric Combinations:")
lp_pm_expected = (synergy['lp']['best_mean'] + synergy['pm']['best_mean']) / 2
lp_pm_actual = synergy['combo_lp+pm']['mean']
lp_pm_synergy = lp_pm_actual - lp_pm_expected

print(f"  LP{synergy['lp']['best_value']} + PM{synergy['pm']['best_value']}:")
print(f"    Expected (average): {lp_pm_expected:>+.2f}")
print(f"    Actual: {lp_pm_actual:>+.2f}")
print(f"    Synergy: {lp_pm_synergy:>+.2f} {'(AMPLIFIES)' if lp_pm_synergy > 0.05 else '(NEUTRAL)' if abs(lp_pm_synergy) < 0.05 else '(CANCELS)'} (n={synergy['combo_lp+pm']['n']})")

lp_pd_expected = (synergy['lp']['best_mean'] + synergy['pd']['best_mean']) / 2
lp_pd_actual = synergy['combo_lp+pd']['mean']
lp_pd_synergy = lp_pd_actual - lp_pd_expected

print(f"\n  LP{synergy['lp']['best_value']} + PD{synergy['pd']['best_value']}:")
print(f"    Expected (average): {lp_pd_expected:>+.2f}")
print(f"    Actual: {lp_pd_actual:>+.2f}")
print(f"    Synergy: {lp_pd_synergy:>+.2f} {'(AMPLIFIES)' if lp_pd_synergy > 0.05 else '(NEUTRAL)' if abs(lp_pd_synergy) < 0.05 else '(CANCELS)'} (n={synergy['combo_lp+pd']['n']})")

print(f"\n  All four (LP{synergy['lp']['best_value']} + PM{synergy['pm']['best_value']} + PD{synergy['pd']['best_value']} + PY{synergy['py']['best_value']}):")
print(f"    Performance: {synergy['combo_all']['mean']:>+.2f} vs_avg (n={synergy['combo_all']['n']})")

print("\n" + "=" * 140)
print("SUMMARY")
print("=" * 140)
print("""
Three Alternative Approaches Demonstrated:

1. CONFIDENCE SCORING:
   - Adjusts for sample size (small samples = less reliable)
   - Uses Bayesian shrinkage to reduce noise
   - Flags findings as LOW/MEDIUM/HIGH confidence
   > Use this to ignore fluky findings from tiny samples

2. WIN RATE & KELLY:
   - Calculates betting edge as % win rate, not just average
   - Computes optimal bet size (Kelly %)
   - Shows expected value per matchup
   > Use this to size bets and assess betting edge

3. METRIC SYNERGY:
   - Tests if combining metrics amplifies or cancels signal
   - Detects positive (amplifying) vs negative (canceling) interactions
   - Determines if metrics are complementary or redundant
   > Use this to decide which metric combinations to use

Next: Implement across all dimension combos to find most robust, high-confidence, high-EV signals.
""")
