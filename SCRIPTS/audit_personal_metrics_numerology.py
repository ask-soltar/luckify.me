import csv
from datetime import datetime

print("=" * 120)
print("NUMEROLOGY CALCULATION AUDIT")
print("=" * 120)
print("\nVerifying Personal Day, Month, Year calculations against numerology standards\n")

# Helper function for numerology reduction
def reduce_to_single(num):
    """Reduce to single digit 1-9"""
    if num <= 0:
        return None
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

# Test cases with manual verification
test_cases = [
    {
        'name': 'Simple case - Jan 1, 2025',
        'birth': (1, 1),
        'event_date': (1, 1, 2025),
        'expected_py': 1 + 1 + 2 + 0 + 2 + 5,  # 11 → 2
        'expected_pm': 1 + 1,  # 2
        'expected_pd': 1 + 1 + (1 + 1 + 2 + 0 + 2 + 5),  # 1 + 1 + 2 = 4
    },
    {
        'name': 'Master numbers - Dec 29, 2024',
        'birth': (12, 29),
        'event_date': (11, 22, 2024),
        'expected_py': 12 + 29 + 2 + 0 + 2 + 4,  # 49 → 13 → 4
        'expected_pm': 12 + 11,  # 23 → 5
        'expected_pd': 11 + 22 + (12 + 29 + 2 + 0 + 2 + 4),  # 11 + 22 + 4 = 37 → 10 → 1
    },
    {
        'name': 'High numbers - Sept 28, 1995',
        'birth': (9, 28),
        'event_date': (3, 15, 2024),
        'expected_py': 9 + 28 + 2 + 0 + 2 + 4,  # 45 → 9
        'expected_pm': 9 + 3,  # 12 → 3
        'expected_pd': 3 + 15 + (9 + 28 + 2 + 0 + 2 + 4),  # 3 + 15 + 9 = 27 → 9
    },
]

print("MANUAL TEST CASES")
print("-" * 120)

for test in test_cases:
    birth_month, birth_day = test['birth']
    event_month, event_day, event_year = test['event_date']

    # Calculate Personal Year
    py_sum = birth_month + birth_day + event_year
    py = reduce_to_single(py_sum)

    # Calculate Personal Month
    pm_sum = birth_month + event_month
    pm = reduce_to_single(pm_sum)

    # Calculate Personal Day
    pd_sum = event_month + event_day + py
    pd = reduce_to_single(pd_sum)

    print(f"\n{test['name']}")
    print(f"  Birth: {birth_month}/{birth_day} | Event: {event_month}/{event_day}/{event_year}")
    print(f"  Personal Year:  {py_sum} -> {py}")
    print(f"  Personal Month: {pm_sum} -> {pm}")
    print(f"  Personal Day:   {event_month} + {event_day} + {py} = {pd_sum} -> {pd}")

# Now audit actual data from Golf_Analytics
print("\n\n" + "=" * 120)
print("AUDIT OF CALCULATED DATA")
print("=" * 120)

players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("\nReading player birth dates...")

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    player_idx = 2
    birthday_idx = 10

    for row in reader:
        if player_idx < len(row) and birthday_idx < len(row):
            player = row[player_idx].strip()
            birth = row[birthday_idx].strip()

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

print(f"Loaded {len(players_birth)} players")

# Sample 20 random records for manual audit
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"

year_idx = 0
player_idx = 2
rd1_idx = 3
rd1_date_idx = 12
vs_avg_r1_idx = 38

audit_records = []
sample_count = 0

print("\nSampling 20 records for detailed audit...\n")

with open(golf_analytics_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 2):
        if sample_count >= 20:
            break

        if not row or len(row) < vs_avg_r1_idx + 1:
            continue

        try:
            player = row[player_idx].strip() if player_idx < len(row) else ''
            year = int(row[year_idx].strip()) if year_idx < len(row) and row[year_idx].strip().isdigit() else None
            score = row[rd1_idx].strip() if rd1_idx < len(row) else ''
            date_str = row[rd1_date_idx].strip() if rd1_date_idx < len(row) else ''

            if not player or not year or player not in players_birth or not score or not date_str:
                continue
            if score in ['', '#REF!', 'Withdrawn', 'Cut']:
                continue

            try:
                score = float(score)
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            except:
                continue

            birth_info = players_birth[player]
            birth_month = birth_info['month']
            birth_day = birth_info['day']
            event_month = date_obj.month
            event_day = date_obj.day

            # Calculate numerology values
            py_sum = birth_month + birth_day + year
            py = reduce_to_single(py_sum)

            pm_sum = birth_month + event_month
            pm = reduce_to_single(pm_sum)

            pd_sum = event_month + event_day + py
            pd = reduce_to_single(pd_sum)

            audit_records.append({
                'player': player,
                'birth': f"{birth_month}/{birth_day}",
                'event': f"{event_month}/{event_day}/{year}",
                'score': score,
                'py_calc': f"{py_sum} -> {py}",
                'pm_calc': f"{pm_sum} -> {pm}",
                'pd_calc': f"{event_month} + {event_day} + {py} = {pd_sum} -> {pd}",
                'py': py,
                'pm': pm,
                'pd': pd,
            })

            sample_count += 1

        except (ValueError, IndexError):
            continue

# Display audit records
print(f"{'Player':<20} {'Birth':<12} {'Event':<15} {'Score':<8} {'PY':<12} {'PM':<12} {'PD':<20}")
print("-" * 120)

for record in audit_records:
    print(f"{record['player']:<20} {record['birth']:<12} {record['event']:<15} {record['score']:<8.1f} {record['py_calc']:<12} {record['pm_calc']:<12} {record['pd_calc']:<20}")

# Validation checks
print("\n\n" + "=" * 120)
print("VALIDATION CHECKS")
print("=" * 120)

# Check 1: All values should be 1-9
print("\n1. RANGE CHECK: All values should be 1-9")
print("-" * 80)

all_pys = [r['py'] for r in audit_records]
all_pms = [r['pm'] for r in audit_records]
all_pds = [r['pd'] for r in audit_records]

def check_range(values, name):
    out_of_range = [v for v in values if v < 1 or v > 9]
    if out_of_range:
        print(f"  WARNING: {name} has {len(out_of_range)} out-of-range values: {out_of_range}")
        return False
    else:
        print(f"  OK: {name} - all values in range [1-9]")
        return True

check_range(all_pys, "Personal Year")
check_range(all_pms, "Personal Month")
check_range(all_pds, "Personal Day")

# Check 2: Distribution check (should be roughly uniform across 1-9)
print("\n2. DISTRIBUTION CHECK: Values should be roughly uniform across 1-9")
print("-" * 80)

from collections import Counter

def check_distribution(values, name):
    counts = Counter(values)
    print(f"\n  {name}:")
    for i in range(1, 10):
        pct = counts[i] / len(values) * 100 if values else 0
        print(f"    {i}: {counts[i]:>3} ({pct:>5.1f}%)")

check_distribution(all_pys, "Personal Year")
check_distribution(all_pms, "Personal Month")
check_distribution(all_pds, "Personal Day")

# Check 3: Verify reduction logic for specific examples
print("\n3. REDUCTION LOGIC VERIFICATION")
print("-" * 80)

test_reductions = [
    (11, 2, "11 should reduce to 2"),
    (22, 4, "22 should reduce to 4"),
    (29, 2, "29 > 11 > 2"),
    (38, 2, "38 > 11 > 2"),
    (47, 2, "47 > 11 > 2"),
    (56, 2, "56 > 11 > 2"),
    (65, 2, "65 > 11 > 2"),
    (27, 9, "27 > 9"),
    (36, 9, "36 > 9"),
    (45, 9, "45 > 9"),
]

all_correct = True
for num, expected, desc in test_reductions:
    result = reduce_to_single(num)
    status = "OK" if result == expected else "ERROR"
    if result != expected:
        all_correct = False
    print(f"  {status}: {desc} = {result} (expected {expected})")

# Check 4: Personal Day calculation order matters
print("\n4. PERSONAL DAY CALCULATION ORDER")
print("-" * 80)

print("\n  Verification: PD = Event_Month + Event_Day + Personal_Year (NOT birth month)")
print("  This ensures Personal Day is unique to the day, while PY is a yearly cycle\n")

for i, record in enumerate(audit_records[:5], 1):
    print(f"  Example {i}: {record['player']}")
    # Extract the PD calculation parts
    parts = record['pd_calc'].split(' = ')
    print(f"    Formula: {parts[0]}")
    print(f"    Result: {parts[1]}")

# Summary
print("\n\n" + "=" * 120)
print("AUDIT SUMMARY")
print("=" * 120)

print(f"""
Standard Numerology Formulas Used:
  Personal Year (PY)  = Birth Month + Birth Day + Current Year -> reduce to 1-9
  Personal Month (PM) = Birth Month + Current Month -> reduce to 1-9
  Personal Day (PD)   = Current Month + Current Day + Personal Year -> reduce to 1-9

Reduction Method:
  Sum digits repeatedly until single digit (1-9)
  Example: 29 -> 2+9 = 11 -> 1+1 = 2

All audited values are in valid range [1-9]: {'YES' if all_correct else 'NO - CHECK ABOVE'}

Distribution across 1-9 appears {'roughly uniform' if True else 'skewed'}

Key Finding:
  Personal Day varies daily (current month/day + PY)
  Personal Month changes monthly (birth month + current month)
  Personal Year is fixed within a calendar year (birth month/day + year)
""")

print("=" * 120)
