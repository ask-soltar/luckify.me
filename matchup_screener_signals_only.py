"""
Signals-Only Matchup Screener
=============================

Evaluates 2-ball matchups ONLY based on validated signals from VALIDATED_SIGNALS.json
Ignores form, recent results, odds. Only cares: Does this player align with validated signals?

No edge unless signals align. Conservative by design.

Strategy:
- Evaluate each player's signal alignment (how many validated signals they hit)
- Score BET signals as +X, FADE signals as -X (to avoid)
- Only recommend if signal edge is clear
- Print signal breakdown so user understands WHY we're recommending
"""

import pandas as pd
import json
from datetime import datetime
import sys

# ============================================================================
# LOAD DATA
# ============================================================================

print("=" * 80)
print("SIGNALS-ONLY MATCHUP SCREENER")
print("=" * 80)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Load validated signals database
try:
    with open('VALIDATED_SIGNALS.json', 'r') as f:
        signals_db = json.load(f)
    print(f"[OK] Loaded {len(signals_db['signals_bet'])} BET signals")
    print(f"[OK] Loaded {len(signals_db['signals_fade'])} FADE signals")
except FileNotFoundError:
    print("[ERROR] VALIDATED_SIGNALS.json not found")
    sys.exit(1)

# Load ANALYSIS data
try:
    df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig')
    print(f"[OK] Loaded {len(df)} ANALYSIS rows")
except FileNotFoundError:
    print("[ERROR] ANALYSIS data not found")
    sys.exit(1)

print()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def evaluate_player_signals(player_name, round_idx, signals_bet, signals_fade):
    """
    Evaluate how many signals a player hits in a given round.

    round_idx: which round of the tournament (1-4)
    Returns: (bet_score, fade_score, bet_signals_hit, fade_signals_hit)
    """
    # Get player's row for this round (if exists)
    player_rounds = df[df['player_name'] == player_name]

    if len(player_rounds) == 0:
        return 0, 0, [], []

    # Use most recent round data (player might have multiple events)
    player_row = player_rounds.iloc[-1]

    bet_signals_hit = []
    fade_signals_hit = []
    bet_score = 0
    fade_score = 0

    # Check BET signals
    for signal in signals_bet:
        signal_hit = True

        # Check all conditions in signal
        for key, value in signal.items():
            if key in ['id', 'tier', 'effect', 'n', 'p_value', 'description', 'source', 'note']:
                continue

            # Map signal keys to dataframe columns
            col_mapping = {
                'color': 'color',
                'condition': 'condition',
                'round_type': 'round_type',
                'element': 'wu_xing',
                'exec_bucket': 'exec_bucket',
                'moon': 'moonwest',
                'moon_group': None,  # Computed below
                'horoscope': 'horoscope',
                'zodiac': 'zodiac',
            }

            if key == 'moon_group':
                # Map moonwest to group
                player_moon = str(player_row.get('moonwest', '')).strip()
                if value == 'Waxing' and player_moon in ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter']:
                    continue
                elif value == 'Waning' and player_moon in ['Waning Crescent', 'Waning Gibbous', 'Last Quarter']:
                    continue
                elif value == 'New Moon' and player_moon == 'New Moon':
                    continue
                elif value == 'Full Moon' and player_moon == 'Full Moon':
                    continue
                else:
                    signal_hit = False
                    break
            elif key in col_mapping and col_mapping[key]:
                col = col_mapping[key]
                player_val = str(player_row.get(col, '')).strip()
                if player_val != str(value).strip():
                    signal_hit = False
                    break

        if signal_hit:
            bet_signals_hit.append(signal['id'])
            bet_score += abs(signal['effect'])  # Weight by magnitude

    # Check FADE signals (subtract score to penalize)
    for signal in signals_fade:
        signal_hit = True

        for key, value in signal.items():
            if key in ['id', 'tier', 'effect', 'n', 'p_value', 'description', 'source', 'note']:
                continue

            col_mapping = {
                'color': 'color',
                'condition': 'condition',
                'round_type': 'round_type',
                'element': 'wu_xing',
                'exec_bucket': 'exec_bucket',
                'moon': 'moonwest',
                'horoscope': 'horoscope',
                'zodiac': 'zodiac',
            }

            if key in col_mapping and col_mapping[key]:
                col = col_mapping[key]
                player_val = str(player_row.get(col, '')).strip()
                if player_val != str(value).strip():
                    signal_hit = False
                    break

        if signal_hit:
            fade_signals_hit.append(signal['id'])
            fade_score += abs(signal['effect'])  # Penalty magnitude

    return bet_score, fade_score, bet_signals_hit, fade_signals_hit


def print_matchup_analysis(p1_name, p2_name, p1_bet, p1_fade, p1_bet_sigs, p1_fade_sigs,
                          p2_bet, p2_fade, p2_bet_sigs, p2_fade_sigs):
    """Print detailed matchup analysis."""

    p1_net = p1_bet - p1_fade
    p2_net = p2_bet - p2_fade
    edge = abs(p1_net - p2_net)

    print(f"\n[MATCHUP] {p1_name} vs {p2_name}")
    print("-" * 80)

    print(f"\n{p1_name}:")
    print(f"  BET signals:  {len(p1_bet_sigs):2d} hit | Score: {p1_bet:6.3f}")
    print(f"  FADE signals: {len(p1_fade_sigs):2d} hit | Score: {p1_fade:6.3f}")
    print(f"  NET SCORE: {p1_net:+6.3f}")
    if p1_bet_sigs:
        print(f"  BET signals: {', '.join(p1_bet_sigs[:3])}" + ("..." if len(p1_bet_sigs) > 3 else ""))
    if p1_fade_sigs:
        print(f"  FADE signals: {', '.join(p1_fade_sigs)}")

    print(f"\n{p2_name}:")
    print(f"  BET signals:  {len(p2_bet_sigs):2d} hit | Score: {p2_bet:6.3f}")
    print(f"  FADE signals: {len(p2_fade_sigs):2d} hit | Score: {p2_fade:6.3f}")
    print(f"  NET SCORE: {p2_net:+6.3f}")
    if p2_bet_sigs:
        print(f"  BET signals: {', '.join(p2_bet_sigs[:3])}" + ("..." if len(p2_bet_sigs) > 3 else ""))
    if p2_fade_sigs:
        print(f"  FADE signals: {', '.join(p2_fade_sigs)}")

    print(f"\n[RECOMMENDATION]")
    if edge < 0.1:
        print(f"  PASS - No clear signal edge (diff: {edge:.3f})")
    elif p1_net > p2_net:
        tier = "BET" if edge > 0.3 else "LEAN"
        print(f"  {tier} {p1_name} | Signal edge: {edge:.3f}")
    else:
        tier = "BET" if edge > 0.3 else "LEAN"
        print(f"  {tier} {p2_name} | Signal edge: {edge:.3f}")

    print()


# ============================================================================
# SAMPLE MATCHUP ANALYSIS
# ============================================================================

# Example: Get two recent Orange players and analyze
orange_players = df[df['color'] == 'Orange'].groupby('player_name').size().sort_values(ascending=False).head(10)

if len(orange_players) >= 2:
    p1_name = orange_players.index[0]
    p2_name = orange_players.index[1]

    p1_bet, p1_fade, p1_bet_sigs, p1_fade_sigs = evaluate_player_signals(
        p1_name, 1, signals_db['signals_bet'], signals_db['signals_fade']
    )
    p2_bet, p2_fade, p2_bet_sigs, p2_fade_sigs = evaluate_player_signals(
        p2_name, 1, signals_db['signals_bet'], signals_db['signals_fade']
    )

    print("=" * 80)
    print("EXAMPLE MATCHUP ANALYSIS (Top 2 Orange Players)")
    print("=" * 80)
    print_matchup_analysis(p1_name, p2_name, p1_bet, p1_fade, p1_bet_sigs, p1_fade_sigs,
                          p2_bet, p2_fade, p2_bet_sigs, p2_fade_sigs)

# ============================================================================
# ARCHITECTURE NOTES
# ============================================================================

print("\n" + "=" * 80)
print("SCREENER ARCHITECTURE")
print("=" * 80)
print("""
Design:
1. Load VALIDATED_SIGNALS.json (centralized signal database)
2. For each player in matchup, evaluate:
   - Which BET signals they hit (sum their magnitudes)
   - Which FADE signals they hit (subtract magnitudes)
   - NET SCORE = BET score - FADE score
3. Compare NET SCORE between players
4. Recommend if edge is clear (>0.3)

How to add new signals:
1. Edit VALIDATED_SIGNALS.json
2. Add signal with id, tier, conditions, effect, source
3. Re-run screener (Python loads updated JSON)
4. No code changes needed

Design principles:
- Conservative: Only bet when signals clearly align
- Transparent: Show which signals drive recommendation
- Modular: Easy to add/remove signals
- Signals-first: Ignore form, odds, recent performance
""")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Load specific matchup file (CSV with player1, player2, event, date)
2. Score all matchups using signal framework
3. Filter for high-confidence recommendations
4. Output: CSV with matchup, recommendation, signal breakdown

Ready to integrate with real matchup data.
""")

print("\n[DONE] Signals-only screener ready for deployment")
print("=" * 80)
