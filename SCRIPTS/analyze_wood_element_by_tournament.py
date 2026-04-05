import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv')

# Filter out 2026 and rows with missing wu_xing
df = df[df['year'] != 2026]
df = df.dropna(subset=['wu_xing'])

print(f"Total records (excluding 2026): {len(df)}")
print(f"Years in data: {sorted(df['year'].unique())}")
print(f"Wu Xing elements: {df['wu_xing'].unique()}\n")

# Separate Wood vs non-Wood players
df['is_wood'] = df['wu_xing'] == 'Wood'

results = []

# Analyze by tournament
tournaments = df['event_name'].unique()

for tournament in sorted(tournaments):
    tour_data = df[df['event_name'] == tournament]

    wood_players = tour_data[tour_data['is_wood'] == True]
    non_wood_players = tour_data[tour_data['is_wood'] == False]

    if len(wood_players) == 0 or len(non_wood_players) == 0:
        continue  # Skip tournaments with only one element type

    # Calculate metrics for Wood players
    wood_avg_off_par = wood_players['off_par'].mean()
    wood_avg_vs_avg = wood_players['vs_avg'].mean()
    wood_count = len(wood_players)
    wood_wins = (wood_players['off_par'] > 0).sum()  # off_par > 0 = beat par

    # Calculate metrics for non-Wood players
    non_wood_avg_off_par = non_wood_players['off_par'].mean()
    non_wood_avg_vs_avg = non_wood_players['vs_avg'].mean()
    non_wood_count = len(non_wood_players)
    non_wood_wins = (non_wood_players['off_par'] > 0).sum()

    # Calculate win rates (% of rounds beating par)
    wood_win_rate = (wood_wins / wood_count * 100) if wood_count > 0 else 0
    non_wood_win_rate = (non_wood_wins / non_wood_count * 100) if non_wood_count > 0 else 0

    # Edge calculation
    off_par_diff = wood_avg_off_par - non_wood_avg_off_par
    vs_avg_diff = wood_avg_vs_avg - non_wood_avg_vs_avg
    win_rate_diff = wood_win_rate - non_wood_win_rate

    results.append({
        'tournament': tournament,
        'wood_count': wood_count,
        'non_wood_count': non_wood_count,
        'wood_avg_off_par': round(wood_avg_off_par, 3),
        'non_wood_avg_off_par': round(non_wood_avg_off_par, 3),
        'off_par_diff': round(off_par_diff, 3),
        'wood_avg_vs_avg': round(wood_avg_vs_avg, 3),
        'non_wood_avg_vs_avg': round(non_wood_avg_vs_avg, 3),
        'vs_avg_diff': round(vs_avg_diff, 3),
        'wood_win_rate_%': round(wood_win_rate, 1),
        'non_wood_win_rate_%': round(non_wood_win_rate, 1),
        'win_rate_diff_%': round(win_rate_diff, 1),
    })

# Convert to DataFrame for display
results_df = pd.DataFrame(results)

# Sort by off_par_diff to show biggest Wood advantages
results_df_sorted = results_df.sort_values('off_par_diff', ascending=False)

print("=" * 130)
print("WOOD vs NON-WOOD ELEMENT PERFORMANCE BY TOURNAMENT (Years != 2026)")
print("=" * 130)
print()

# Display formatted table
for idx, row in results_df_sorted.iterrows():
    print(f"Tournament: {row['tournament']}")
    print(f"  Sample sizes: Wood={row['wood_count']}, Non-Wood={row['non_wood_count']}")
    print(f"  Off-Par: Wood avg={row['wood_avg_off_par']}, Non-Wood avg={row['non_wood_avg_off_par']}, Diff={row['off_par_diff']}")
    print(f"  Vs Avg: Wood avg={row['wood_avg_vs_avg']}, Non-Wood avg={row['non_wood_avg_vs_avg']}, Diff={row['vs_avg_diff']}")
    print(f"  Win Rates: Wood={row['wood_win_rate_%']}%, Non-Wood={row['non_wood_win_rate_%']}%, Diff={row['win_rate_diff_%']}%")
    print()

print("=" * 130)
print("SUMMARY STATISTICS")
print("=" * 130)
print(f"Tournaments analyzed: {len(results_df)}")
print(f"Mean off_par difference (Wood - Non-Wood): {results_df['off_par_diff'].mean():.3f}")
print(f"Median off_par difference: {results_df['off_par_diff'].median():.3f}")
print(f"Tournaments where Wood outperforms: {(results_df['off_par_diff'] > 0).sum()}/{len(results_df)}")
print(f"Mean win rate difference: {results_df['win_rate_diff_%'].mean():.1f}%")
print()

# Save detailed results to CSV
results_df_sorted.to_csv('wood_element_tournament_analysis.csv', index=False)
print("[OK] Detailed results saved to: wood_element_tournament_analysis.csv")
