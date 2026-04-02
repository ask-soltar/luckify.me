import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv')

# Filter out 2026 and rows with missing wu_xing or color
df = df[df['year'] != 2026]
df = df.dropna(subset=['wu_xing', 'color'])

print(f"Total records (excluding 2026): {len(df)}")
print(f"Years in data: {sorted(df['year'].unique())}")
print(f"Colors in data: {sorted(df['color'].unique())}")
print()

# ============================================================================
# ANALYSIS: Wood Element Players (wu_xing=Wood) by Color
# ============================================================================

print("=" * 130)
print("WOOD ELEMENT PLAYERS (wu_xing=Wood) PERFORMANCE BY COLOR")
print("=" * 130)
print()

wood_players = df[df['wu_xing'] == 'Wood']
print(f"Total Wood element rounds: {len(wood_players)}")
print()

color_results = []

for color in sorted(wood_players['color'].unique()):
    color_data = wood_players[wood_players['color'] == color]

    if len(color_data) == 0:
        continue

    # Wood element metrics for this color
    wood_avg_off_par = color_data['off_par'].mean()
    wood_avg_exec = color_data['exec'].mean()
    wood_avg_upside = color_data['upside'].mean()
    wood_wins = (color_data['off_par'] > 0).sum()
    wood_win_rate = wood_wins / len(color_data) * 100

    # Compare to non-Wood for this color
    non_wood_color = df[(df['wu_xing'] != 'Wood') & (df['color'] == color)]
    non_wood_avg_off_par = non_wood_color['off_par'].mean()
    non_wood_win_rate = (non_wood_color['off_par'] > 0).sum() / len(non_wood_color) * 100

    off_par_diff = wood_avg_off_par - non_wood_avg_off_par
    win_rate_diff = wood_win_rate - non_wood_win_rate

    color_results.append({
        'color': color,
        'wood_count': len(color_data),
        'wood_avg_off_par': round(wood_avg_off_par, 3),
        'wood_avg_exec': round(wood_avg_exec, 1),
        'wood_avg_upside': round(wood_avg_upside, 1),
        'wood_win_rate_%': round(wood_win_rate, 1),
        'non_wood_off_par': round(non_wood_avg_off_par, 3),
        'non_wood_win_rate_%': round(non_wood_win_rate, 1),
        'off_par_advantage': round(off_par_diff, 3),
        'win_rate_advantage_%': round(win_rate_diff, 1),
    })

color_df = pd.DataFrame(color_results).sort_values('off_par_advantage', ascending=False)

print("Wood Element Players by Color (sorted by off-par advantage vs non-Wood):")
print()

for idx, row in color_df.iterrows():
    print(f"{row['color'].upper()}")
    print(f"  Sample: {row['wood_count']} rounds")
    print(f"  Off-par: {row['wood_avg_off_par']} (Exec: {row['wood_avg_exec']}, Upside: {row['wood_avg_upside']})")
    print(f"  Win rate: {row['wood_win_rate_%']}%")
    print(f"  vs Non-Wood: {row['off_par_advantage']:+.3f} off-par ({row['non_wood_off_par']}), {row['win_rate_advantage_%']:+.1f}% win rate")
    print()

# ============================================================================
# BREAKDOWN: Wood Years (if detectable from year patterns)
# ============================================================================

print("=" * 130)
print("YEAR ELEMENT BREAKDOWN (Heavenly Stem cycle: every 10 years repeats)")
print("=" * 130)
print()

# Heavenly Stem cycle: year % 10 maps to element
# 0,1 = Metal, 2,3 = Water, 4,5 = Wood, 6,7 = Fire, 8,9 = Earth
stem_map = {
    0: 'Metal', 1: 'Metal',
    2: 'Water', 3: 'Water',
    4: 'Wood',  5: 'Wood',
    6: 'Fire',  7: 'Fire',
    8: 'Earth', 9: 'Earth',
}

df['year_stem'] = df['year'].apply(lambda x: stem_map[x % 10])

print("Years in data by Heavenly Stem:")
year_stems = df.groupby(['year', 'year_stem']).size().reset_index(name='count')
print(year_stems.to_string(index=False))
print()

# Analyze Wood years specifically
wood_years_data = df[df['year_stem'] == 'Wood']
print(f"Records in Wood years (2024-2025): {len(wood_years_data)}")
print()

print("Wood Element Players in Wood Years by Color:")
print()

wood_elem_wood_year = wood_years_data[wood_years_data['wu_xing'] == 'Wood']

wood_year_color_results = []

for color in sorted(wood_elem_wood_year['color'].unique()):
    color_data = wood_elem_wood_year[wood_elem_wood_year['color'] == color]

    if len(color_data) == 0:
        continue

    avg_off_par = color_data['off_par'].mean()
    avg_exec = color_data['exec'].mean()
    avg_upside = color_data['upside'].mean()
    win_rate = (color_data['off_par'] > 0).sum() / len(color_data) * 100

    # Compare to non-Wood in Wood years
    non_wood_wood_year = wood_years_data[(wood_years_data['wu_xing'] != 'Wood') & (wood_years_data['color'] == color)]
    if len(non_wood_wood_year) > 0:
        non_wood_off_par = non_wood_wood_year['off_par'].mean()
        non_wood_win_rate = (non_wood_wood_year['off_par'] > 0).sum() / len(non_wood_wood_year) * 100
        off_par_diff = avg_off_par - non_wood_off_par
        win_rate_diff = win_rate - non_wood_win_rate
    else:
        non_wood_off_par = np.nan
        non_wood_win_rate = np.nan
        off_par_diff = np.nan
        win_rate_diff = np.nan

    wood_year_color_results.append({
        'color': color,
        'count': len(color_data),
        'avg_off_par': round(avg_off_par, 3),
        'avg_exec': round(avg_exec, 1),
        'avg_upside': round(avg_upside, 1),
        'win_rate_%': round(win_rate, 1),
        'vs_non_wood_off_par': round(off_par_diff, 3) if not np.isnan(off_par_diff) else 'N/A',
        'vs_non_wood_win_rate_%': round(win_rate_diff, 1) if not np.isnan(win_rate_diff) else 'N/A',
    })

wood_year_color_df = pd.DataFrame(wood_year_color_results)
if len(wood_year_color_df) > 0:
    wood_year_color_df = wood_year_color_df.sort_values('avg_off_par', ascending=False, na_position='last')

    for idx, row in wood_year_color_df.iterrows():
        print(f"{row['color'].upper()}")
        print(f"  Sample: {row['count']} rounds (in Wood years 2024-2025)")
        print(f"  Off-par: {row['avg_off_par']} (Exec: {row['avg_exec']}, Upside: {row['avg_upside']})")
        print(f"  Win rate: {row['win_rate_%']}%")
        if row['vs_non_wood_off_par'] != 'N/A':
            print(f"  vs Non-Wood: {row['vs_non_wood_off_par']:+.3f} off-par, {row['vs_non_wood_win_rate_%']:+.1f}% win rate")
        print()

# ============================================================================
# Save Results
# ============================================================================

color_df.to_csv('wood_element_by_color.csv', index=False)
if len(wood_year_color_df) > 0:
    wood_year_color_df.to_csv('wood_element_in_wood_years_by_color.csv', index=False)

print("=" * 130)
print("[OK] Results saved:")
print("  - wood_element_by_color.csv (all years)")
print("  - wood_element_in_wood_years_by_color.csv (2024-2025 Wood years only)")
print("=" * 130)
