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

def reduce_with_master(num):
    """Reduce to single digit 1-9, preserving master numbers (11, 22, 33)"""
    if num <= 0:
        return None
    if num in [11, 22, 33]:
        return num
    while num > 9:
        if num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num

def get_numerological_attributes(value):
    """Return numerological attributes of a number (1-9, or master numbers)"""
    attrs = {}

    # Master number
    attrs['is_master'] = value in [11, 22, 33]

    # Parity (odd/even, Yin/Yang)
    attrs['parity'] = 'Odd' if value % 2 == 1 else 'Even'
    attrs['yin_yang'] = 'Yang' if value % 2 == 1 else 'Yin'

    # Cardinal numbers (1, 4, 7 are cardinal in numerology)
    attrs['is_cardinal'] = value in [1, 4, 7]

    # Cycle position (where in 9-year cycle)
    if value <= 9:
        attrs['cycle_position'] = 'Early' if value in [1, 2, 3] else 'Middle' if value in [4, 5, 6] else 'Late'
    else:
        # Master numbers treated as advanced cycle
        attrs['cycle_position'] = 'Advanced'

    # Friendly/Challenging pairs (numerological harmony)
    friendly = {
        1: [1, 9, 5],
        2: [2, 8, 4, 7],
        3: [3, 9, 6],
        4: [4, 1, 8],
        5: [5, 1, 2, 9],
        6: [6, 3, 9],
        7: [7, 2, 4],
        8: [8, 2, 4],
        9: [9, 1, 3, 6],
        11: [2, 11, 29],
        22: [4, 22, 40],
        33: [3, 6, 33],
    }
    attrs['friendly_with'] = friendly.get(value, [])

    # Number meaning/archetype
    meanings = {
        1: 'Leadership',
        2: 'Harmony',
        3: 'Creativity',
        4: 'Foundation',
        5: 'Change',
        6: 'Balance',
        7: 'Spirituality',
        8: 'Power',
        9: 'Completion',
        11: 'Intuition',
        22: 'Master Builder',
        33: 'Master Compassion',
    }
    attrs['meaning'] = meanings.get(value, 'Unknown')

    return attrs

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

# Read Golf_Analytics with numerological dimensions
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

            # R1 data only
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

            # Calculate numerological values
            py = reduce_to_single(birth_month + birth_day + year)
            pm = reduce_to_single(birth_month + event_month)
            pd = reduce_to_single(event_month + event_day + py)

            # Also calculate with master numbers preserved
            py_master = reduce_with_master(birth_month + birth_day + year)
            pm_master = reduce_with_master(birth_month + event_month)
            pd_master = reduce_with_master(event_month + event_day + py)

            record = {
                'lp': life_path,
                'pm': pm,
                'pd': pd,
                'py': py,
                'pm_master': pm_master,
                'pd_master': pd_master,
                'py_master': py_master,
                'vs_avg': vs_avg,
                'beat_field': 1 if vs_avg > 0 else 0,
            }

            # Add numerological attribute keys
            if life_path:
                lp_attrs = get_numerological_attributes(life_path)
                record['lp_parity'] = lp_attrs['parity']
                record['lp_cardinal'] = lp_attrs['is_cardinal']
                record['lp_cycle'] = lp_attrs['cycle_position']

            if pm:
                pm_attrs = get_numerological_attributes(pm)
                record['pm_parity'] = pm_attrs['parity']
                record['pm_master'] = pm_attrs['is_master']

            if pd:
                pd_attrs = get_numerological_attributes(pd)
                record['pd_parity'] = pd_attrs['parity']
                record['pd_master'] = pd_attrs['is_master']

            if py:
                py_attrs = get_numerological_attributes(py)
                record['py_parity'] = py_attrs['parity']
                record['py_master'] = py_attrs['is_master']

            # Create dimension keys combining traditional + numerological
            base_key = (cond, ttype, rtype)

            # Add numerological dimensions
            if 'lp_parity' in record:
                parity_key = (cond, ttype, rtype, 'LP_' + record['lp_parity'])
                data_by_dimensions[parity_key].append(record)

            # Cardinal vs non-cardinal
            if 'lp_cardinal' in record:
                cardinal_key = (cond, ttype, rtype, 'LP_' + ('Cardinal' if record['lp_cardinal'] else 'Non-Cardinal'))
                data_by_dimensions[cardinal_key].append(record)

            # PD with master numbers
            if pd_master in [11, 22, 33]:
                master_key = (cond, ttype, rtype, 'PD_Master')
                data_by_dimensions[master_key].append(record)
            else:
                non_master_key = (cond, ttype, rtype, 'PD_Non-Master')
                data_by_dimensions[non_master_key].append(record)

            # PM parity
            if 'pm_parity' in record:
                pm_parity_key = (cond, ttype, rtype, 'PM_' + record['pm_parity'])
                data_by_dimensions[pm_parity_key].append(record)

            # Base dimension
            data_by_dimensions[base_key].append(record)

        except (ValueError, IndexError):
            continue

print(f"Processed across {len(data_by_dimensions)} numerological dimensions\n")

# Analysis function
def analyze_numerological(data, metric_name='lp'):
    """Analyze metric performance within dimension"""
    if not data or len(data) < 5:
        return None

    wins = sum(d['beat_field'] for d in data)
    wr = wins / len(data) * 100
    baseline = sum(d['vs_avg'] for d in data) / len(data)

    return {
        'n': len(data),
        'baseline_vs_avg': baseline,
        'win_rate': wr,
        'total_wins': wins,
    }

# ============================================================================
# NUMEROLOGICAL DIMENSIONAL ANALYSIS
# ============================================================================

print("=" * 150)
print("NUMEROLOGICAL DIMENSIONAL ANALYSIS")
print("=" * 150)

# Simplified - report directly from data_by_dimensions

# Report by numerological dimension type
print("\n" + "=" * 150)
print("1. LIFE PATH PARITY ANALYSIS (Odd/Even Energy)")
print("=" * 150)

for condition in ['Calm', 'Moderate', 'Tough']:
    for ttype in ['S', 'NS']:
        for rtype in ['Open', 'Positioning', 'Closing']:
            base_key = (condition, ttype, rtype)

            lp_odd_key = (condition, ttype, rtype, 'LP_Odd')
            lp_even_key = (condition, ttype, rtype, 'LP_Even')

            odd_data = data_by_dimensions[lp_odd_key]
            even_data = data_by_dimensions[lp_even_key]

            if not odd_data or not even_data or len(odd_data) < 10 or len(even_data) < 10:
                continue

            odd_result = analyze_numerological(odd_data)
            even_result = analyze_numerological(even_data)

            print(f"\n{condition} + {ttype} + {rtype}:")
            print(f"  LP Odd  (Yang):  WR={odd_result['win_rate']:>5.1f}%, vs_avg={odd_result['baseline_vs_avg']:>+.2f}, n={odd_result['n']}")
            print(f"  LP Even (Yin):   WR={even_result['win_rate']:>5.1f}%, vs_avg={even_result['baseline_vs_avg']:>+.2f}, n={even_result['n']}")
            print(f"  Difference:      WR={odd_result['win_rate']-even_result['win_rate']:>+.1f}pp, vs_avg={odd_result['baseline_vs_avg']-even_result['baseline_vs_avg']:>+.2f}")

print("\n" + "=" * 150)
print("2. LIFE PATH CARDINAL vs NON-CARDINAL ANALYSIS (Foundational Numbers)")
print("=" * 150)
print("Cardinal: 1 (Leadership), 4 (Foundation), 7 (Spirituality)")
print("Non-Cardinal: 2, 3, 5, 6, 8, 9")

for condition in ['Calm', 'Moderate', 'Tough']:
    for ttype in ['S', 'NS']:
        for rtype in ['Open', 'Positioning', 'Closing']:
            cardinal_key = (condition, ttype, rtype, 'LP_Cardinal')
            non_cardinal_key = (condition, ttype, rtype, 'LP_Non-Cardinal')

            cardinal_data = data_by_dimensions[cardinal_key]
            non_cardinal_data = data_by_dimensions[non_cardinal_key]

            if not cardinal_data or not non_cardinal_data or len(cardinal_data) < 10 or len(non_cardinal_data) < 10:
                continue

            cardinal_result = analyze_numerological(cardinal_data)
            non_cardinal_result = analyze_numerological(non_cardinal_data)

            print(f"\n{condition} + {ttype} + {rtype}:")
            print(f"  Cardinal (1/4/7):     WR={cardinal_result['win_rate']:>5.1f}%, vs_avg={cardinal_result['baseline_vs_avg']:>+.2f}, n={cardinal_result['n']}")
            print(f"  Non-Cardinal (2-9):   WR={non_cardinal_result['win_rate']:>5.1f}%, vs_avg={non_cardinal_result['baseline_vs_avg']:>+.2f}, n={non_cardinal_result['n']}")
            print(f"  Difference:           WR={cardinal_result['win_rate']-non_cardinal_result['win_rate']:>+.1f}pp, vs_avg={cardinal_result['baseline_vs_avg']-non_cardinal_result['baseline_vs_avg']:>+.2f}")

print("\n" + "=" * 150)
print("3. MASTER NUMBERS in PERSONAL DAY (11, 22, 33 - Spiritual Amplification)")
print("=" * 150)

for condition in ['Calm', 'Moderate', 'Tough']:
    for ttype in ['S', 'NS']:
        for rtype in ['Open', 'Positioning', 'Closing']:
            master_key = (condition, ttype, rtype, 'PD_Master')
            non_master_key = (condition, ttype, rtype, 'PD_Non-Master')

            master_data = data_by_dimensions[master_key]
            non_master_data = data_by_dimensions[non_master_key]

            if not master_data or not non_master_data or len(master_data) < 5 or len(non_master_data) < 10:
                continue

            master_result = analyze_numerological(master_data)
            non_master_result = analyze_numerological(non_master_data)

            print(f"\n{condition} + {ttype} + {rtype}:")
            print(f"  Master (PD 11/22/33): WR={master_result['win_rate']:>5.1f}%, vs_avg={master_result['baseline_vs_avg']:>+.2f}, n={master_result['n']}")
            print(f"  Regular (PD 1-9):     WR={non_master_result['win_rate']:>5.1f}%, vs_avg={non_master_result['baseline_vs_avg']:>+.2f}, n={non_master_result['n']}")
            print(f"  Difference:           WR={master_result['win_rate']-non_master_result['win_rate']:>+.1f}pp, vs_avg={master_result['baseline_vs_avg']-non_master_result['baseline_vs_avg']:>+.2f}")

print("\n" + "=" * 150)
print("4. PERSONAL MONTH PARITY (Energy Alignment by Month)")
print("=" * 150)

for condition in ['Calm', 'Moderate', 'Tough']:
    for ttype in ['S', 'NS']:
        for rtype in ['Open', 'Positioning', 'Closing']:
            pm_odd_key = (condition, ttype, rtype, 'PM_Odd')
            pm_even_key = (condition, ttype, rtype, 'PM_Even')

            pm_odd = data_by_dimensions[pm_odd_key]
            pm_even = data_by_dimensions[pm_even_key]

            if not pm_odd or not pm_even or len(pm_odd) < 10 or len(pm_even) < 10:
                continue

            pm_odd_result = analyze_numerological(pm_odd)
            pm_even_result = analyze_numerological(pm_even)

            print(f"\n{condition} + {ttype} + {rtype}:")
            print(f"  PM Odd  (Yang):  WR={pm_odd_result['win_rate']:>5.1f}%, vs_avg={pm_odd_result['baseline_vs_avg']:>+.2f}, n={pm_odd_result['n']}")
            print(f"  PM Even (Yin):   WR={pm_even_result['win_rate']:>5.1f}%, vs_avg={pm_even_result['baseline_vs_avg']:>+.2f}, n={pm_even_result['n']}")

print("\n" + "=" * 150)
print("SUMMARY: STRONGEST NUMEROLOGICAL SIGNALS")
print("=" * 150)

print("""
Key Numerological Concepts Being Tested:

1. PARITY (Odd/Even, Yang/Yin):
   - Odd numbers (1,3,5,7,9) = Yang energy (active, expanding)
   - Even numbers (2,4,6,8) = Yin energy (receptive, contracting)
   - Signal: Do certain parities perform better in different conditions?

2. CARDINAL NUMBERS (1, 4, 7):
   - 1: Leadership, independence, initiation
   - 4: Stability, foundation, structure
   - 7: Spirituality, introspection, analysis
   - Signal: Do foundational numbers provide more stability/predictability?

3. MASTER NUMBERS (11, 22, 33):
   - Represent amplified or spiritual versions of base numbers
   - 11: Intuition (vs 2)
   - 22: Master Builder (vs 4)
   - 33: Master Compassion (vs 6)
   - Signal: Do master numbers show heightened performance (or volatility)?

4. NUMEROLOGICAL CYCLES:
   - Early cycle (1,2,3): Beginning, emergence, growth
   - Middle cycle (4,5,6): Consolidation, activity, balance
   - Late cycle (7,8,9): Spirituality, completion, closure
   - Signal: Different phases of 9-year cycle perform differently by condition

Next: Test specific number COMBINATIONS (harmonic pairs) and LP compatibility scoring.
""")
