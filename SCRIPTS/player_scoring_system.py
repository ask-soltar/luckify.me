#!/usr/bin/env python3
"""
Player Scoring System for 2-Ball/3-Ball/Outrights Betting
Combines Element + Zodiac model validation into single score per player
"""

import pandas as pd
import json
from typing import Dict, List, Tuple

# ============================================================================
# VALIDATED SIGNALS DATABASE
# ============================================================================

ELEMENT_SIGNALS = {
    # (condition, round_type, color, element): win_rate
    ('Calm', 'Survival', 'Purple', 'Water'): 0.615,    # +11.5% edge
    ('Calm', 'Positioning', 'Green', 'Metal'): 0.613,  # +11.3% edge
    ('Calm', 'Closing', 'Blue', 'Fire'): 0.581,        # +8.1% edge
    ('Calm', 'Closing', 'Yellow', 'Metal'): 0.564,     # +6.4% edge
    ('Calm', 'Positioning', 'Green', 'Wood'): 0.564,   # +6.4% edge
    ('Calm', 'Survival', 'Purple', 'Fire'): 0.563,     # +6.3% edge
    ('Calm', 'Positioning', 'Purple', 'Wood'): 0.560,  # +6.0% edge
    ('Calm', 'Closing', 'Green', 'Earth'): 0.559,      # +5.9% edge
    ('Calm', 'Closing', 'Orange', 'Wood'): 0.546,      # +4.6% edge
    ('Calm', 'Closing', 'Purple', 'Fire'): 0.546,      # +4.6% edge
    ('Calm', 'Closing', 'Orange', 'Water'): 0.527,     # +2.7% edge
    ('Calm', 'Survival', 'Orange', 'Water'): 0.537,    # +3.7% edge
    ('Calm', 'Closing', 'Purple', 'Water'): 0.533,     # +3.3% edge
    ('Calm', 'Survival', 'Green', 'Earth'): 0.526,     # +2.6% edge
}

ZODIAC_SIGNALS = {
    # (condition, round_type, exec_bucket, upside_bucket, chinese_zodiac): win_rate
    ('Calm', 'Survival', 50, 75, 'Tiger'): 0.653,      # +15.3% edge
    ('Calm', 'Open', 50, 75, 'Rat'): 0.643,            # +14.3% edge
    ('Calm', 'Survival', 25, 50, 'Goat'): 0.642,       # +14.2% edge
    ('Calm', 'Survival', 50, 75, 'Snake'): 0.640,      # +14.0% edge
    ('Calm', 'REMOVE', 50, 50, 'Rabbit'): 0.636,       # +13.6% edge
    ('Calm', 'Positioning', 50, 50, 'Rat'): 0.635,     # +13.5% edge
    ('Calm', 'Open', 25, 75, 'Snake'): 0.633,          # +13.3% edge
    ('Calm', 'Open', 25, 50, 'Rooster'): 0.627,        # +12.7% edge
    ('Calm', 'Survival', 25, 75, 'Rat'): 0.620,        # +12.0% edge
    ('Calm', 'Positioning', 50, 75, 'Pig'): 0.618,     # +11.8% edge
    ('Calm', 'Open', 50, 75, 'Pig'): 0.613,            # +11.3% edge
    ('Calm', 'Survival', 75, 50, 'Rooster'): 0.606,    # +10.5% edge
    ('Calm', 'Positioning', 25, 50, 'Pig'): 0.601,     # +10.0% edge
    ('Moderate', 'Closing', 25, 50, 'Dragon'): 0.596,  # +9.5% edge
    ('Calm', 'Survival', 50, 50, 'Dog'): 0.591,        # +9.0% edge
    ('Calm', 'Open', 75, 50, 'Dragon'): 0.579,         # +7.5% edge
    ('Calm', 'Positioning', 50, 50, 'Goat'): 0.576,    # +7.1% edge
    ('Calm', 'Survival', 50, 50, 'Leo'): 0.574,        # +6.8% edge
    ('Calm', 'Closing', 50, 75, 'Monkey'): 0.572,      # +6.5% edge
    ('Moderate', 'Survival', 25, 75, 'Tiger'): 0.569,  # +6.2% edge
}

NEUTRAL_SCORE = 0.50  # Default if no validation

# ============================================================================
# PLAYER SCORING CLASS
# ============================================================================

class PlayerScorer:
    """Score players based on Element + Zodiac models blended with player historical performance"""

    def __init__(self, enable_player_history=True, player_tables_dir='D:\\Projects\\luckify-me\\player_tables'):
        self.element_signals = ELEMENT_SIGNALS
        self.zodiac_signals = ZODIAC_SIGNALS
        self.enable_player_history = enable_player_history
        self.player_history = {}

        # Load player historical tables if enabled
        if enable_player_history:
            try:
                import pandas as pd
                self.player_baseline = pd.read_csv(f'{player_tables_dir}\\player_baseline.csv')

                # Load and rename condition table (dimension_value -> condition)
                self.player_by_condition = pd.read_csv(f'{player_tables_dir}\\player_by_condition.csv')
                self.player_by_condition = self.player_by_condition.rename(columns={'dimension_value': 'condition'})

                # Load and rename round_type table (dimension_value -> round_type)
                self.player_by_round_type = pd.read_csv(f'{player_tables_dir}\\player_by_round_type.csv')
                self.player_by_round_type = self.player_by_round_type.rename(columns={'dimension_value': 'round_type'})

                # Load composite condition_roundtype table
                self.player_by_condition_roundtype = pd.read_csv(f'{player_tables_dir}\\player_by_condition_roundtype.csv')

                # Load zodiac table (already has correct column name)
                self.player_by_zodiac = pd.read_csv(f'{player_tables_dir}\\player_by_zodiac.csv')

                # Build lookup dicts for fast access
                self._build_history_lookups()
                print(f"[OK] Loaded player history tables ({len(self.player_baseline)} players)")

            except Exception as e:
                print(f"[!] Could not load player history: {e}")
                print(f"[!] Scoring will use model signals only (no player affinity)")
                self.enable_player_history = False

    def _build_history_lookups(self):
        """Build efficient lookup dictionaries for player history data"""
        # Baseline lookup: player_name -> row dict
        for _, row in self.player_baseline.iterrows():
            self.player_history[row['player_name']] = {
                'baseline': row.to_dict()
            }

        # Condition lookup
        for _, row in self.player_by_condition.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_condition' not in self.player_history[name]:
                self.player_history[name]['by_condition'] = {}
            self.player_history[name]['by_condition'][row['condition']] = row.to_dict()

        # Round type lookup
        for _, row in self.player_by_round_type.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_roundtype' not in self.player_history[name]:
                self.player_history[name]['by_roundtype'] = {}
            self.player_history[name]['by_roundtype'][row['round_type']] = row.to_dict()

        # Condition x RoundType lookup (most important)
        for _, row in self.player_by_condition_roundtype.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_cond_rt' not in self.player_history[name]:
                self.player_history[name]['by_cond_rt'] = {}
            key = (row['condition'], row['round_type'])
            self.player_history[name]['by_cond_rt'][key] = row.to_dict()

        # Zodiac lookup
        for _, row in self.player_by_zodiac.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_zodiac' not in self.player_history[name]:
                self.player_history[name]['by_zodiac'] = {}
            self.player_history[name]['by_zodiac'][row['chinese_zodiac']] = row.to_dict()

    def get_element_score(self, condition: str, round_type: str, color: str, element: str) -> float:
        """Get Element model score for a player combo"""
        key = (condition, round_type, color, element)
        return self.element_signals.get(key, NEUTRAL_SCORE)

    def get_zodiac_score(self, condition: str, round_type: str, exec_bucket: int,
                        upside_bucket: int, chinese_zodiac: str) -> float:
        """Get Zodiac model score for a player combo"""
        key = (condition, round_type, exec_bucket, upside_bucket, chinese_zodiac)
        return self.zodiac_signals.get(key, NEUTRAL_SCORE)

    def get_player_affinity_adjustment(self, player_name: str, condition: str,
                                       round_type: str, chinese_zodiac: str) -> dict:
        """
        Get player-specific historical win rate adjustments
        Returns dict with historical scores and confidence flags
        """
        if not self.enable_player_history or player_name not in self.player_history:
            return {
                'has_data': False,
                'cond_rt_win_rate': None,
                'cond_win_rate': None,
                'rt_win_rate': None,
                'zodiac_win_rate': None,
                'baseline_win_rate': None,
            }

        history = self.player_history[player_name]

        result = {'has_data': True}

        # Condition x RoundType (most specific, highest weight)
        if 'by_cond_rt' in history and (condition, round_type) in history['by_cond_rt']:
            data = history['by_cond_rt'][(condition, round_type)]
            result['cond_rt_win_rate'] = data.get('win_rate', None)
            result['cond_rt_events'] = data.get('events', 0)
        else:
            result['cond_rt_win_rate'] = None
            result['cond_rt_events'] = 0

        # Condition only
        if 'by_condition' in history and condition in history['by_condition']:
            data = history['by_condition'][condition]
            result['cond_win_rate'] = data.get('win_rate', None)
            result['cond_events'] = data.get('events', 0)
        else:
            result['cond_win_rate'] = None
            result['cond_events'] = 0

        # RoundType only
        if 'by_roundtype' in history and round_type in history['by_roundtype']:
            data = history['by_roundtype'][round_type]
            result['rt_win_rate'] = data.get('win_rate', None)
            result['rt_events'] = data.get('events', 0)
        else:
            result['rt_win_rate'] = None
            result['rt_events'] = 0

        # Zodiac
        if 'by_zodiac' in history and chinese_zodiac in history['by_zodiac']:
            data = history['by_zodiac'][chinese_zodiac]
            result['zodiac_win_rate'] = data.get('win_rate', None)
            result['zodiac_events'] = data.get('events', 0)
        else:
            result['zodiac_win_rate'] = None
            result['zodiac_events'] = 0

        # Baseline (career average)
        if 'baseline' in history:
            result['baseline_win_rate'] = history['baseline'].get('career_win_rate', None)
            result['baseline_events'] = history['baseline'].get('career_events', 0)
        else:
            result['baseline_win_rate'] = None
            result['baseline_events'] = 0

        return result

    def score_player(self, player: Dict) -> Dict:
        """
        Score a single player combining model signals + player historical affinity

        Expected player dict:
        {
            'name': 'Player Name',
            'condition': 'Calm',
            'round_type': 'Positioning',
            'color': 'Green',
            'element': 'Metal',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Rat'
        }
        """
        # Layer 1: Model Signals
        element_score = self.get_element_score(
            player['condition'],
            player['round_type'],
            player['color'],
            player['element']
        )

        zodiac_score = self.get_zodiac_score(
            player['condition'],
            player['round_type'],
            player['exec_bucket'],
            player['upside_bucket'],
            player['chinese_zodiac']
        )

        # Combined model score: 60% Element (higher transfer), 40% Zodiac
        model_score = (element_score * 0.6) + (zodiac_score * 0.4)

        # Layer 2: Player Historical Affinity
        affinity = self.get_player_affinity_adjustment(
            player['name'],
            player['condition'],
            player['round_type'],
            player['chinese_zodiac']
        )

        # Blend model score with player history (if available)
        if affinity['has_data'] and affinity['cond_rt_win_rate'] is not None:
            # Use condition x roundtype as primary affinity (highest specificity)
            player_score = affinity['cond_rt_win_rate']
            final_score = (model_score * 0.7) + (player_score * 0.3)  # 70% model, 30% player history
            affinity_source = 'cond_rt'
        elif affinity['has_data'] and affinity['cond_win_rate'] is not None:
            # Fallback to condition-only
            player_score = affinity['cond_win_rate']
            final_score = (model_score * 0.75) + (player_score * 0.25)  # 75% model, 25% player
            affinity_source = 'condition'
        elif affinity['has_data'] and affinity['baseline_win_rate'] is not None:
            # Fallback to baseline (career average)
            player_score = affinity['baseline_win_rate']
            final_score = (model_score * 0.85) + (player_score * 0.15)  # 85% model, 15% baseline
            affinity_source = 'baseline'
        else:
            # No player history available, use model score only
            final_score = model_score
            affinity_source = 'none'

        # Convert from win rate (0.5-0.65) to readable percentage (50-65)
        final_score_pct = final_score * 100

        # Check for overlap (both models validating)
        overlap = (element_score > NEUTRAL_SCORE) and (zodiac_score > NEUTRAL_SCORE)

        return {
            'name': player['name'],
            'element_score': element_score * 100,
            'zodiac_score': zodiac_score * 100,
            'model_score': model_score * 100,
            'player_affinity_score': (affinity['cond_rt_win_rate'] * 100 if affinity['cond_rt_win_rate'] else None),
            'combined_score': final_score_pct,
            'affinity_source': affinity_source,
            'overlap': overlap,
            'element_validated': element_score > NEUTRAL_SCORE,
            'zodiac_validated': zodiac_score > NEUTRAL_SCORE,
            'has_player_history': affinity['has_data'],
        }

    def score_tournament(self, players: List[Dict]) -> pd.DataFrame:
        """Score all players in a tournament"""
        scored = [self.score_player(p) for p in players]
        df = pd.DataFrame(scored)
        df = df.sort_values('combined_score', ascending=False).reset_index(drop=True)
        return df

    def calculate_differential(self, scorer_player: Dict, opponent_player: Dict) -> float:
        """Calculate differential between two players (positive = first player favored)"""
        scorer = self.score_player(scorer_player)
        opponent = self.score_player(opponent_player)
        return scorer['combined_score'] - opponent['combined_score']

    def rank_matchups_2ball(self, players: List[Dict]) -> pd.DataFrame:
        """Generate ranked 2-ball matchups"""
        scored_df = self.score_tournament(players)

        matchups = []
        for i in range(len(scored_df)):
            for j in range(i + 1, len(scored_df)):
                player1 = scored_df.iloc[i]
                player2 = scored_df.iloc[j]

                differential = player1['combined_score'] - player2['combined_score']

                matchups.append({
                    'player_1': player1['name'],
                    'player_1_score': round(player1['combined_score'], 1),
                    'player_2': player2['name'],
                    'player_2_score': round(player2['combined_score'], 1),
                    'differential': round(abs(differential), 1),
                    'favorite': player1['name'] if differential > 0 else player2['name'],
                    'p1_overlap': player1['overlap'],
                    'p2_overlap': player2['overlap'],
                })

        matchups_df = pd.DataFrame(matchups)
        matchups_df = matchups_df.sort_values('differential', ascending=False)
        return matchups_df

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_tournament():
    """Example tournament scoring with player history integration"""

    # Example player data for a tournament with Calm conditions
    players = [
        {
            'name': 'Rory McIlroy',
            'condition': 'Calm',
            'round_type': 'Positioning',
            'color': 'Green',
            'element': 'Metal',
            'exec_bucket': 75,
            'upside_bucket': 75,
            'chinese_zodiac': 'Rat',
        },
        {
            'name': 'Jon Rahm',
            'condition': 'Calm',
            'round_type': 'Positioning',
            'color': 'Blue',
            'element': 'Fire',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Dragon',
        },
        {
            'name': 'Scottie Scheffler',
            'condition': 'Calm',
            'round_type': 'Closing',
            'color': 'Purple',
            'element': 'Water',
            'exec_bucket': 75,
            'upside_bucket': 50,
            'chinese_zodiac': 'Tiger',
        },
        {
            'name': 'Tiger Woods',
            'condition': 'Calm',
            'round_type': 'Survival',
            'color': 'Purple',
            'element': 'Fire',
            'exec_bucket': 50,
            'upside_bucket': 25,
            'chinese_zodiac': 'Monkey',
        },
        {
            'name': 'Max Homa',
            'condition': 'Calm',
            'round_type': 'Closing',
            'color': 'Yellow',
            'element': 'Metal',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Snake',
        },
    ]

    scorer = PlayerScorer(enable_player_history=True)

    print("="*120)
    print("TOURNAMENT PLAYER SCORES (With Player History Affinity)")
    print("="*120)

    scored_df = scorer.score_tournament(players)
    print(scored_df[['name', 'model_score', 'player_affinity_score', 'combined_score', 'affinity_source', 'has_player_history']].to_string(index=False))

    print("\n" + "="*120)
    print("RANKED 2-BALL MATCHUPS (Top 10 by Differential)")
    print("="*120)

    matchups_df = scorer.rank_matchups_2ball(players)
    top_matchups = matchups_df.head(10)

    for idx, (_, matchup) in enumerate(top_matchups.iterrows(), 1):
        overlap_str = "(BOTH VALIDATED)" if (matchup['p1_overlap'] and matchup['p2_overlap']) else ""
        print(f"{idx:2}. {matchup['player_1']:<20} ({matchup['player_1_score']:.1f}) vs "
              f"{matchup['player_2']:<20} ({matchup['player_2_score']:.1f}) "
              f"| Differential: +{matchup['differential']:.1f} | {overlap_str}")

    return scored_df, matchups_df

if __name__ == "__main__":
    scored, matchups = example_tournament()
