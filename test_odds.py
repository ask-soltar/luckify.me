import pandas as pd

def american_to_implied(odds):
    """Convert American odds to implied probability"""
    odds = float(odds)
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    else:
        return 100 / (odds + 100)

# Load input
df = pd.read_csv('texas_childrens_round4_3ball.csv')

print("ODDS CALIBRATION CHECK")
print("=" * 100)
print()

# Sample first 5 matchups
for idx, row in df.head(5).iterrows():
    print(f"MATCHUP {idx + 1}: {row['Player [A]']} vs {row['Player [B]']} vs {row['Player [C]']}")
    print()
    
    # Get raw odds
    ml_a = row['ML [A]']
    ml_b = row['ML [B]']
    ml_c = row['ML [C]']
    
    # Convert to implied
    impl_a = american_to_implied(ml_a)
    impl_b = american_to_implied(ml_b)
    impl_c = american_to_implied(ml_c)
    
    print(f"  {row['Player [A]']:<20} ML: {ml_a:>6} -> {impl_a*100:>6.2f}% implied")
    print(f"  {row['Player [B]']:<20} ML: {ml_b:>6} -> {impl_b*100:>6.2f}% implied")
    print(f"  {row['Player [C]']:<20} ML: {ml_c:>6} -> {impl_c*100:>6.2f}% implied")
    
    # Check if they sum to more than 100% (vig)
    total_implied = impl_a + impl_b + impl_c
    vig = (total_implied - 1.0) * 100
    print(f"  Total Implied: {total_implied*100:.1f}% (Vig: {vig:.1f}%)")
    print()
