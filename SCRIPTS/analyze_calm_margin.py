#!/usr/bin/env python3
"""
Analyze patterns in Calm conditions at different thresholds.
Focus on "margin" matchups that qualify at lower thresholds but not higher ones.
"""

import pandas as pd

# Load scored data
df = pd.read_csv('2ball_scored_35_65.csv')

# Filter for graded Calm only
calm = df[(df['actual_winner'] != 'Push') & (df['condition'] == 'Calm')].copy()

print("="*70)
print("CALM CONDITION THRESHOLD ANALYSIS")
print("="*70)

# Category 1: 5.0-5.5 (qualify at 5.0 but not 5.5)
margin_5_0_to_5_5 = calm[(calm['difference'] >= 5.0) & (calm['difference'] < 5.5)].copy()

# Category 2: 5.5-6.0
margin_5_5_to_6_0 = calm[(calm['difference'] >= 5.5) & (calm['difference'] < 6.0)].copy()

# Category 3: 6.0+
high_6_plus = calm[calm['difference'] >= 6.0].copy()

# Category 4: 4.5-5.0
margin_4_5_to_5_0 = calm[(calm['difference'] >= 4.5) & (calm['difference'] < 5.0)].copy()

print("\n" + "MATCHUP DISTRIBUTION BY DIFFERENCE RANGE".center(70))
print("-"*70)

categories = [
    ("4.5-5.0", margin_4_5_to_5_0),
    ("5.0-5.5", margin_5_0_to_5_5),
    ("5.5-6.0", margin_5_5_to_6_0),
    ("6.0+", high_6_plus)
]

for label, data in categories:
    if len(data) > 0:
        wins = len(data[data['correct'] == True])
        win_rate = (wins / len(data)) * 100
        print(f"{label:>8}: {len(data):3.0f} matchups, {wins:3.0f} wins, {win_rate:5.1f}% win rate")

# Deep dive into 5.0-5.5 (the margin that gets cut at 5.5)
print("\n" + "="*70)
print("DEEP DIVE: 5.0-5.5 Range (Margin Matchups)")
print("="*70)

print(f"\nTotal in 5.0-5.5: {len(margin_5_0_to_5_5)}")
print(f"Wins: {len(margin_5_0_to_5_5[margin_5_0_to_5_5['correct']==True])}")
print(f"Losses: {len(margin_5_0_to_5_5[margin_5_0_to_5_5['correct']==False])}")
print(f"Win Rate: {(len(margin_5_0_to_5_5[margin_5_0_to_5_5['correct']==True])/len(margin_5_0_to_5_5)*100):.1f}%")

# By round type
print(f"\nBy Round Type (5.0-5.5):")
for round_type in ['Open', 'Positioning', 'Closing']:
    subset = margin_5_0_to_5_5[margin_5_0_to_5_5['round_type'] == round_type]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        print(f"  {round_type:12}: {len(subset):2.0f} matchups, {wins:2.0f} wins, {(wins/len(subset)*100):5.1f}% win rate")

# Sample losses in 5.0-5.5
print(f"\n" + "="*70)
print("LOSING MATCHUPS IN 5.0-5.5 RANGE (Why they fail)")
print("="*70)

losses_5_0_to_5_5 = margin_5_0_to_5_5[margin_5_0_to_5_5['correct'] == False].copy()

if len(losses_5_0_to_5_5) > 0:
    print(f"\nSample of {min(10, len(losses_5_0_to_5_5))} losses in 5.0-5.5 range:")
    for idx, (_, row) in enumerate(losses_5_0_to_5_5.head(10).iterrows(), 1):
        print(f"\n{idx}. {row['player_a']} vs {row['player_b']}")
        print(f"   Round Type: {row['round_type']}")
        print(f"   Prediction: {row['prediction']} (Score: {row['score_a']:6.2f})")
        print(f"   Actual Winner: {row['actual_winner']} (Score: {row['score_b']:6.2f})")
        print(f"   Difference: {row['difference']:.2f}")

# Pattern analysis
print(f"\n" + "="*70)
print("PATTERN SUMMARY: Why Higher Thresholds Hurt Calm")
print("="*70)

threshold_5_data = calm[calm['difference'] >= 5.0]
threshold_5_5_data = calm[calm['difference'] >= 5.5]
threshold_6_data = calm[calm['difference'] >= 6.0]

print(f"\nThreshold >= 5.0: {len(threshold_5_data):3.0f} qualified, {(len(threshold_5_data[threshold_5_data['correct']==True])/len(threshold_5_data)*100):5.1f}% win")
print(f"Threshold >= 5.5: {len(threshold_5_5_data):3.0f} qualified, {(len(threshold_5_5_data[threshold_5_5_data['correct']==True])/len(threshold_5_5_data)*100):5.1f}% win")
print(f"Threshold >= 6.0: {len(threshold_6_data):3.0f} qualified, {(len(threshold_6_data[threshold_6_data['correct']==True])/len(threshold_6_data)*100):5.1f}% win")

print(f"\nKey Insight:")
print(f"  - Moving from 5.0 to 5.5 removes {len(threshold_5_data) - len(threshold_5_5_data):2.0f} matchups")
print(f"  - Those margin matchups (5.0-5.5) have {(len(margin_5_0_to_5_5[margin_5_0_to_5_5['correct']==True])/len(margin_5_0_to_5_5)*100):.1f}% win rate")
print(f"  - By removing them, we lose the good ones and don't remove enough bad ones")

# Compare win rates with and without the margin
included_wins = len(threshold_5_data[threshold_5_data['correct'] == True])
excluded_wins = len(threshold_5_5_data[threshold_5_5_data['correct'] == True])
margin_wins = included_wins - excluded_wins

print(f"\nMargin matchups (5.0-5.5):")
print(f"  Wins in margin: {margin_wins}")
print(f"  Losses in margin: {len(margin_5_0_to_5_5) - margin_wins}")

# Show if higher thresholds remove more losers than winners
all_wins_5 = len(threshold_5_data[threshold_5_data['correct'] == True])
all_losses_5 = len(threshold_5_data[threshold_5_data['correct'] == False])
wins_5_5 = len(threshold_5_5_data[threshold_5_5_data['correct'] == True])
losses_5_5 = len(threshold_5_5_data[threshold_5_5_data['correct'] == False])

margin_wins = all_wins_5 - wins_5_5
margin_losses = all_losses_5 - losses_5_5

print(f"\nWhen raising threshold to 5.5, we remove:")
print(f"  {margin_wins} wins (good predictions we throw away)")
print(f"  {margin_losses} losses (bad predictions we eliminate)")
print(f"  Net: {margin_wins - margin_losses:+d} (losing {abs(margin_wins - margin_losses)} predictions of higher quality)")
