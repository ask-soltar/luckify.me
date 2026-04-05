#!/usr/bin/env python3
"""
Player Scoring System v2: With Combo Specialization Boost

Layers:
1. Model Signals (Element + Zodiac) - baseline validation
2. Player Historical Affinity (condition/roundtype) - what book prices
3. Combo Specialization Boost - EDGE: player outperforms baseline in THIS specific combo
"""

import pandas as pd
import json
from typing import Dict, List, Tuple

# ============================================================================
# VALIDATED SIGNALS (From earlier backtests)
# ============================================================================

ELEMENT_SIGNALS = {
    ('Calm', 'Survival', 'Purple', 'Water'): 0.615,
    ('Calm', 'Positioning', 'Green', 'Metal'): 0.613,
    ('Calm', 'Closing', 'Blue', 'Fire'): 0.581,
    ('Calm', 'Closing', 'Yellow', 'Metal'): 0.564,
    ('Calm', 'Positioning', 'Green', 'Wood'): 0.564,
    ('Calm', 'Survival', 'Purple', 'Fire'): 0.563,
    ('Calm', 'Positioning', 'Purple', 'Wood'): 0.560,
    ('Calm', 'Closing', 'Green', 'Earth'): 0.559,
    ('Calm', 'Closing', 'Orange', 'Wood'): 0.546,
    ('Calm', 'Closing', 'Purple', 'Fire'): 0.546,
    ('Calm', 'Closing', 'Orange', 'Water'): 0.527,
    ('Calm', 'Survival', 'Orange', 'Water'): 0.537,
    ('Calm', 'Closing', 'Purple', 'Water'): 0.533,
    ('Calm', 'Survival', 'Green', 'Earth'): 0.526,
}

ZODIAC_SIGNALS = {
    ('Calm', 'Survival', 50, 75, 'Tiger'): 0.653,
    ('Calm', 'Open', 50, 75, 'Rat'): 0.643,
    ('Calm', 'Survival', 25, 50, 'Goat'): 0.642,
    ('Calm', 'Survival', 50, 75, 'Snake'): 0.640,
    ('Calm', 'Positioning', 50, 50, 'Rat'): 0.635,
    ('Calm', 'Open', 25, 75, 'Snake'): 0.633,
    ('Calm', 'Open', 25, 50, 'Rooster'): 0.627,
    ('Calm', 'Survival', 25, 75, 'Rat'): 0.620,
    ('Calm', 'Positioning', 50, 75, 'Pig'): 0.618,
    ('Calm', 'Open', 50, 75, 'Pig'): 0.613,
    ('Calm', 'Survival', 75, 50, 'Rooster'): 0.606,
    ('Calm', 'Positioning', 25, 50, 'Pig'): 0.601,
    ('Moderate', 'Closing', 25, 50, 'Dragon'): 0.596,
    ('Calm', 'Survival', 50, 50, 'Dog'): 0.591,
    ('Calm', 'Open', 75, 50, 'Dragon'): 0.579,
    ('Calm', 'Positioning', 50, 50, 'Goat'): 0.576,
    ('Calm', 'Survival', 50, 50, 'Leo'): 0.574,
    ('Calm', 'Closing', 50, 75, 'Monkey'): 0.572,
    ('Moderate', 'Survival', 25, 75, 'Tiger'): 0.569,
}

NEUTRAL_SCORE = 0.50

# ============================================================================
# PLAYER SCORING CLASS V2
# ============================================================================

class PlayerScorerV2:
    """Score players with combo specialization boost layer"""

    def __init__(self, enable_player_history=True, enable_specialization=True,
                 player_tables_dir='D:\\Projects\\luckify-me\\player_tables',
                 specialization_file='D:\\Projects\\luckify-me\\player_combo_specializations_hc.csv'):

        self.element_signals = ELEMENT_SIGNALS
        self.zodiac_signals = ZODIAC_SIGNALS
        self.enable_player_history = enable_player_history
        self.enable_specialization = enable_specialization
        self.player_history = {}
        self.specializations = {}

        # Load player history
        if enable_player_history:
            try:
                self.player_baseline = pd.read_csv(f'{player_tables_dir}\\player_baseline.csv')
                self.player_by_cond_rt = pd.read_csv(f'{player_tables_dir}\\player_by_condition_roundtype.csv')
                self.player_by_condition = pd.read_csv(f'{player_tables_dir}\\player_by_condition.csv')
                self.player_by_condition = self.player_by_condition.rename(columns={'dimension_value': 'condition'})

                self._build_history_lookups()
                print(f"[OK] Loaded player history: {len(self.player_baseline)} players")

            except Exception as e:
                print(f"[!] Could not load player history: {e}")
                self.enable_player_history = False

        # Load specializations
        if enable_specialization:
            try:
                spec_df = pd.read_csv(specialization_file)
                for _, row in spec_df.iterrows():
                    key = (row['player_name'], row['condition'], row['round_type'],
                           row['color'], row['element'], row['chinese_zodiac'])
                    self.specializations[key] = {
                        'baseline_wr': row['baseline_wr'],
                        'combo_wr': row['combo_wr'],
                        'delta': row['delta'],
                        'combo_events': row['combo_events'],
                    }

                print(f"[OK] Loaded {len(self.specializations)} specializations")

            except Exception as e:
                print(f"[!] Could not load specializations: {e}")
                self.enable_specialization = False

    def _build_history_lookups(self):
        """Build efficient lookup dictionaries"""
        for _, row in self.player_baseline.iterrows():
            self.player_history[row['player_name']] = {'baseline': row.to_dict()}

        for _, row in self.player_by_condition.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_condition' not in self.player_history[name]:
                self.player_history[name]['by_condition'] = {}
            self.player_history[name]['by_condition'][row['condition']] = row.to_dict()

        for _, row in self.player_by_cond_rt.iterrows():
            name = row['player_name']
            if name not in self.player_history:
                self.player_history[name] = {}
            if 'by_cond_rt' not in self.player_history[name]:
                self.player_history[name]['by_cond_rt'] = {}
            key = (row['condition'], row['round_type'])
            self.player_history[name]['by_cond_rt'][key] = row.to_dict()

    def get_element_score(self, condition: str, round_type: str, color: str, element: str) -> float:
        key = (condition, round_type, color, element)
        return self.element_signals.get(key, NEUTRAL_SCORE)

    def get_zodiac_score(self, condition: str, round_type: str, exec_bucket: int,
                        upside_bucket: int, chinese_zodiac: str) -> float:
        key = (condition, round_type, exec_bucket, upside_bucket, chinese_zodiac)
        return self.zodiac_signals.get(key, NEUTRAL_SCORE)

    def get_specialization_boost(self, player_name: str, condition: str, round_type: str,
                                 color: str, element: str, chinese_zodiac: str) -> Dict:
        """Check if player has a known specialization in this combo"""
        if not self.enable_specialization:
            return {'has_specialization': False, 'boost': 0, 'delta': 0}

        key = (player_name, condition, round_type, color, element, chinese_zodiac)

        if key in self.specializations:
            spec = self.specializations[key]
            return {
                'has_specialization': True,
                'boost': spec['delta'],
                'delta': spec['delta'] * 100,
                'combo_wr': spec['combo_wr'] * 100,
                'combo_events': spec['combo_events'],
            }

        return {'has_specialization': False, 'boost': 0, 'delta': 0}

    def score_player(self, player: Dict) -> Dict:
        """Score with all 3 layers"""

        # Layer 1: Model signals
        element_score = self.get_element_score(
            player['condition'], player['round_type'], player['color'], player['element']
        )

        zodiac_score = self.get_zodiac_score(
            player['condition'], player['round_type'],
            player['exec_bucket'], player['upside_bucket'], player['chinese_zodiac']
        )

        model_score = (element_score * 0.6) + (zodiac_score * 0.4)

        # Layer 2: Player history
        if self.enable_player_history and player['name'] in self.player_history:
            history_data = self.player_history[player['name']]
            if 'by_cond_rt' in history_data and (player['condition'], player['round_type']) in history_data['by_cond_rt']:
                player_wr = history_data['by_cond_rt'][(player['condition'], player['round_type'])]['win_rate']
            elif 'by_condition' in history_data and player['condition'] in history_data['by_condition']:
                player_wr = history_data['by_condition'][player['condition']]['win_rate']
            elif 'baseline' in history_data:
                player_wr = history_data['baseline']['career_win_rate']
            else:
                player_wr = NEUTRAL_SCORE
        else:
            player_wr = NEUTRAL_SCORE

        # Blend layers 1 + 2
        blended_score = (model_score * 0.7) + (player_wr * 0.3)

        # Layer 3: Combo specialization boost
        specialization = self.get_specialization_boost(
            player['name'], player['condition'], player['round_type'],
            player['color'], player['element'], player['chinese_zodiac']
        )

        # Apply specialization boost: add delta to blended score
        if specialization['has_specialization']:
            final_score = blended_score + specialization['boost']
            # Cap at 0.95 (don't claim >95%)
            final_score = min(final_score, 0.95)
            spec_source = 'SPECIALIZATION'
        else:
            final_score = blended_score
            spec_source = 'history'

        return {
            'name': player['name'],
            'element_score': element_score * 100,
            'zodiac_score': zodiac_score * 100,
            'model_score': model_score * 100,
            'player_history_score': player_wr * 100,
            'blended_score': blended_score * 100,
            'specialization_boost': specialization['delta'],
            'final_score': final_score * 100,
            'score_source': spec_source,
            'has_specialization': specialization['has_specialization'],
        }

    def score_tournament(self, players: List[Dict]) -> pd.DataFrame:
        scored = [self.score_player(p) for p in players]
        df = pd.DataFrame(scored)
        df = df.sort_values('final_score', ascending=False).reset_index(drop=True)
        return df

    def rank_matchups_2ball(self, players: List[Dict]) -> pd.DataFrame:
        scored_df = self.score_tournament(players)

        matchups = []
        for i in range(len(scored_df)):
            for j in range(i + 1, len(scored_df)):
                p1 = scored_df.iloc[i]
                p2 = scored_df.iloc[j]

                differential = p1['final_score'] - p2['final_score']

                matchups.append({
                    'player_1': p1['name'],
                    'player_1_score': round(p1['final_score'], 1),
                    'player_1_spec': 'YES' if p1['has_specialization'] else 'no',
                    'player_2': p2['name'],
                    'player_2_score': round(p2['final_score'], 1),
                    'player_2_spec': 'YES' if p2['has_specialization'] else 'no',
                    'differential': round(abs(differential), 1),
                    'favorite': p1['name'] if differential > 0 else p2['name'],
                })

        matchups_df = pd.DataFrame(matchups)
        matchups_df = matchups_df.sort_values('differential', ascending=False)
        return matchups_df

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_tournament():
    """Test with combo-specialization-boosted scoring"""

    players = [
        {
            'name': 'Taylor Pendrith',
            'condition': 'Calm',
            'round_type': 'Open',
            'color': 'Yellow',
            'element': 'Metal',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Rat',
        },
        {
            'name': 'Andrew Novak',
            'condition': 'Calm',
            'round_type': 'Open',
            'color': 'Purple',
            'element': 'Wood',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Rat',
        },
        {
            'name': 'Rory McIlroy',
            'condition': 'Calm',
            'round_type': 'Open',
            'color': 'Yellow',
            'element': 'Earth',
            'exec_bucket': 75,
            'upside_bucket': 75,
            'chinese_zodiac': 'Snake',
        },
        {
            'name': 'Jon Rahm',
            'condition': 'Calm',
            'round_type': 'Open',
            'color': 'Blue',
            'element': 'Fire',
            'exec_bucket': 50,
            'upside_bucket': 50,
            'chinese_zodiac': 'Dog',
        },
    ]

    scorer = PlayerScorerV2(enable_player_history=True, enable_specialization=True)

    print()
    print("="*120)
    print("V2 SCORING WITH SPECIALIZATION BOOST")
    print("="*120)
    print()

    scored_df = scorer.score_tournament(players)
    print(scored_df[[
        'name', 'blended_score', 'specialization_boost', 'final_score', 'score_source', 'has_specialization'
    ]].to_string(index=False))

    print()
    print("="*120)
    print("TOP 2-BALL MATCHUPS")
    print("="*120)
    print()

    matchups_df = scorer.rank_matchups_2ball(players)
    print(matchups_df.to_string(index=False))

    return scored_df, matchups_df

if __name__ == "__main__":
    scored, matchups = example_tournament()
