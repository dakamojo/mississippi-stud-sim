"""
Configuration settings for Mississippi Stud Simulator
"""

# Mississippi Stud payout table (multipliers for bet amount)
# Using deuces hand class numbers: 1=Straight Flush (includes Royal), 2=Quads, etc.
# Royal Flush is distinguished by score=1 within Straight Flush class
PAYOUT_TABLE = {
    1: 100,   # Straight Flush (Royal Flush gets 500x, handled specially)
    2: 40,    # Four of a Kind
    3: 10,    # Full House
    4: 6,     # Flush
    5: 4,     # Straight
    6: 3,     # Three of a Kind
    7: 2,     # Two Pair
    8: 1      # One Pair (Jacks or Better - handled specially)
}

# Royal Flush payout (when score=1 and class=1)
ROYAL_FLUSH_PAYOUT = 500

# Default betting configuration
DEFAULT_BET = 1

# Hand outcome categories for tracking
HAND_OUTCOMES = [
    'royal_flush',
    'straight_flush',
    'four_of_a_kind',
    'full_house',
    'flush',
    'straight',
    'three_of_a_kind',
    'two_pair',
    'pair_jacks_or_better',
    'pair_6_to_10',
    'high_card',
    'loss'
]

# Strategy parameters for betting decisions
STRATEGY_CONFIG = {
    # Card point values for strategy calculation
    'card_points': {
        'low_cards': 0,      # 2-5 (ranks 0-3)
        'push_cards': 1,     # 6-10 (ranks 4-8) 
        'high_cards': 2      # J-A (ranks 9-12)
    },
    
    # Betting thresholds
    'step1_bet_threshold': 3,    # Total card points needed to bet on step 1
    'step2_bet_threshold': 4,    # Total card points needed to bet on step 2
    'step3_bet_threshold': 5,    # Total card points needed to bet on step 3
    
    # Pair thresholds (using rank values: 0=2, 1=3, ..., 12=A)
    'min_push_pair_rank': 4,     # Minimum rank for "push pair" (6 or better)
    'min_high_pair_rank': 9,  # Minimum rank for high pair (J or better)
}

# Simulation defaults
SIMULATION_CONFIG = {
    'default_hands': 100,
    'show_each_hand': False,
    'verbose_output': True
}

# Rank mappings for easier understanding
RANK_NAMES = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
SUIT_NAMES = ['c', 'd', 'h', 's']  # clubs, diamonds, hearts, spades
