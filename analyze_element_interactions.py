import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv')

# Filter out 2026 and rows with missing wu_xing
df = df[df['year'] != 2026]
df = df.dropna(subset=['wu_xing'])

print(f"Total records (excluding 2026): {len(df)}")
print(f"Wu Xing distribution:")
print(df['wu_xing'].value_counts())
print()

# ============================================================================
# PART 1: Individual Element Performance vs All Others
# ============================================================================

print("=" * 130)
print("PART 1: INDIVIDUAL ELEMENT PERFORMANCE (By Element vs All Others)")
print("=" * 130)
print()

elements = ['Wood', 'Water', 'Fire', 'Metal', 'Earth']
element_results = []

for element in elements:
    element_data = df[df['wu_xing'] == element]
    other_data = df[df['wu_xing'] != element]

    if len(element_data) == 0:
        continue

    elem_avg_off_par = element_data['off_par'].mean()
    elem_win_rate = (element_data['off_par'] > 0).sum() / len(element_data) * 100

    other_avg_off_par = other_data['off_par'].mean()
    other_win_rate = (other_data['off_par'] > 0).sum() / len(other_data) * 100

    off_par_diff = elem_avg_off_par - other_avg_off_par
    win_rate_diff = elem_win_rate - other_win_rate

    element_results.append({
        'element': element,
        'count': len(element_data),
        'pct_of_data': round(len(element_data) / len(df) * 100, 1),
        'avg_off_par': round(elem_avg_off_par, 3),
        'vs_others_avg_off_par': round(other_avg_off_par, 3),
        'off_par_advantage': round(off_par_diff, 3),
        'win_rate_%': round(elem_win_rate, 1),
        'vs_others_win_rate_%': round(other_win_rate, 1),
        'win_rate_advantage_%': round(win_rate_diff, 1),
    })

elem_df = pd.DataFrame(element_results).sort_values('off_par_advantage', ascending=False)

for idx, row in elem_df.iterrows():
    print(f"{row['element'].upper()}")
    print(f"  Sample size: {row['count']} rounds ({row['pct_of_data']}% of data)")
    print(f"  Off-par: {row['avg_off_par']} (vs others: {row['vs_others_avg_off_par']}, advantage: {row['off_par_advantage']})")
    print(f"  Win rate: {row['win_rate_%']}% (vs others: {row['vs_others_win_rate_%']}%, advantage: {row['win_rate_advantage_%']}%)")
    print()

# ============================================================================
# PART 2: Wu Xing Cycle Support Test
# ============================================================================

print("=" * 130)
print("PART 2: WU XING SUPPORT RELATIONSHIPS (Matchups)")
print("=" * 130)
print()
print("Wu Xing cycle: Water -> Wood -> Fire -> Earth -> Metal -> Water (cycle)")
print("Support: Element on left feeds/supports element on right")
print()

support_pairs = [
    ('Water', 'Wood', 'Water feeds Wood (nourishes growth)'),
    ('Wood', 'Fire', 'Wood feeds Fire (combustion)'),
    ('Fire', 'Earth', 'Fire feeds Earth (ash creates soil)'),
    ('Earth', 'Metal', 'Earth feeds Metal (ore in earth)'),
    ('Metal', 'Water', 'Metal feeds Water (liquifies/holds water)'),
]

opposition_pairs = [
    ('Wood', 'Metal', 'Metal cuts Wood'),
    ('Water', 'Fire', 'Water extinguishes Fire'),
    ('Fire', 'Earth', 'Fire controlled by Earth'),
    ('Earth', 'Water', 'Water floods Earth'),
    ('Metal', 'Wood', 'Metal opposes Wood'),
]

print("SUPPORT PAIRS (Does supported element outperform supporter?):")
print()

support_results = []

for supporter, supported, description in support_pairs:
    supporter_data = df[df['wu_xing'] == supporter]
    supported_data = df[df['wu_xing'] == supported]

    if len(supporter_data) == 0 or len(supported_data) == 0:
        continue

    supp_avg = supporter_data['off_par'].mean()
    supp_win = (supporter_data['off_par'] > 0).sum() / len(supporter_data) * 100

    supd_avg = supported_data['off_par'].mean()
    supd_win = (supported_data['off_par'] > 0).sum() / len(supported_data) * 100

    diff_off_par = supd_avg - supp_avg
    diff_win = supd_win - supp_win

    support_results.append({
        'supporter': supporter,
        'supported': supported,
        'supporter_off_par': round(supp_avg, 3),
        'supported_off_par': round(supd_avg, 3),
        'off_par_diff': round(diff_off_par, 3),
        'supporter_win_%': round(supp_win, 1),
        'supported_win_%': round(supd_win, 1),
        'win_rate_diff_%': round(diff_win, 1),
        'description': description,
    })

supp_df = pd.DataFrame(support_results).sort_values('off_par_diff', ascending=False)

for idx, row in supp_df.iterrows():
    print(f"{row['supporter']} -> {row['supported']}: {row['description']}")
    print(f"  {row['supporter']}: off_par={row['supporter_off_par']}, win_rate={row['supporter_win_%']}%")
    print(f"  {row['supported']}: off_par={row['supported_off_par']}, win_rate={row['supported_win_%']}%")
    print(f"  Difference: {row['supported']} is {row['off_par_diff']:+.3f} ahead in off_par, {row['win_rate_diff_%']:+.1f}% in win rate")
    print()

# ============================================================================
# PART 3: Opposition Pairs
# ============================================================================

print("=" * 130)
print("PART 3: OPPOSITION PAIRS (Who wins in conflict?)")
print("=" * 130)
print()

opp_results = []

for elem1, elem2, description in opposition_pairs:
    data1 = df[df['wu_xing'] == elem1]
    data2 = df[df['wu_xing'] == elem2]

    if len(data1) == 0 or len(data2) == 0:
        continue

    avg1 = data1['off_par'].mean()
    win1 = (data1['off_par'] > 0).sum() / len(data1) * 100

    avg2 = data2['off_par'].mean()
    win2 = (data2['off_par'] > 0).sum() / len(data2) * 100

    diff_off_par = avg1 - avg2
    diff_win = win1 - win2

    opp_results.append({
        'elem1': elem1,
        'elem2': elem2,
        'elem1_off_par': round(avg1, 3),
        'elem2_off_par': round(avg2, 3),
        'off_par_diff': round(diff_off_par, 3),
        'elem1_win_%': round(win1, 1),
        'elem2_win_%': round(win2, 1),
        'win_rate_diff_%': round(diff_win, 1),
        'description': description,
    })

opp_df = pd.DataFrame(opp_results).sort_values('off_par_diff', ascending=False)

for idx, row in opp_df.iterrows():
    winner = row['elem1'] if row['off_par_diff'] > 0 else row['elem2']
    print(f"{row['elem1']} vs {row['elem2']}: {row['description']}")
    print(f"  {row['elem1']}: off_par={row['elem1_off_par']}, win_rate={row['elem1_win_%']}%")
    print(f"  {row['elem2']}: off_par={row['elem2_off_par']}, win_rate={row['elem2_win_%']}%")
    print(f"  Winner: {winner} ({row['off_par_diff']:+.3f} off_par, {row['win_rate_diff_%']:+.1f}% win rate)")
    print()

# ============================================================================
# PART 4: Save Results
# ============================================================================

elem_df.to_csv('element_individual_performance.csv', index=False)
supp_df.to_csv('element_support_pairs.csv', index=False)
opp_df.to_csv('element_opposition_pairs.csv', index=False)

print("=" * 130)
print("[OK] Results saved:")
print("  - element_individual_performance.csv")
print("  - element_support_pairs.csv")
print("  - element_opposition_pairs.csv")
print("=" * 130)
