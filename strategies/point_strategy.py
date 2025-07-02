"""
Point Strategy for Mississippi Stud betting decisions.
"""

from strategies.base_strategy import BaseStrategy
from utils.hand_analyzer import HandAnalyzer


def card_points(card, config):
    """
    Returns the point value of a card for Mississippi Stud strategy.
    Args:
        card (int): The integer-encoded card from deuces.
        config (dict): Strategy configuration containing point values.
    Returns:
        int: The point value of the card.
    """
    rank = card % 13
    # deuces: 0=2, 1=3, 2=4, 3=5, 4=6, 5=7, 6=8, 7=9, 8=10, 9=J, 10=Q, 11=K, 12=A
    if 4 <= rank <= 8:  # 6-10
        return config['card_points']['push_cards']
    elif rank >= 9:  # J-A
        return config['card_points']['high_cards']
    else:  # 2-5
        return config['card_points']['low_cards']


class PointStrategy(BaseStrategy):
    """
    The Point Strategy for Mississippi Stud betting decisions.
    This strategy assigns point values to cards and makes betting decisions
    based on hand strength and accumulated points.
    """
    
    def eval_step_1(self, hand):
        """
        Evaluate the player's hand after the first two cards are dealt (step 1).
        Args:
            hand (list): The player's hand (list of two cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the hand.
        """
        card1, card2 = hand
        rank1 = card1 % 13
        rank2 = card2 % 13
        
        if rank1 == rank2:
            if rank1 >= self.config['min_push_pair_rank']:
                return 'bet3'  # Pair of sixes or higher
            else:
                return 'bet1'  # Lower pairs
        elif card_points(card1, self.config) + card_points(card2, self.config) >= self.config['step1_bet_threshold']:
            return 'bet1'
        else:
            return 'fold'

    def eval_step_2(self, hand):
        """
        Evaluate the player's hand after the third card is dealt (step 2).
        Args:
            hand (list): The player's hand (list of three cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the hand.
        """
        ranks = [card % 13 for card in hand]
        
        # Check for trips first
        has_trips, _ = HandAnalyzer.has_trips(ranks)
        if has_trips:
            return 'bet3'
        
        # Check for a pair of sixes or better
        has_high_pair, pair_rank = HandAnalyzer.has_pair(ranks, self.config['min_push_pair_rank'])
        if has_high_pair:
            return 'bet3'
        
        # Check for any other pair
        has_any_pair, _ = HandAnalyzer.has_pair(ranks)
        if has_any_pair:
            return 'bet1'
        
        # Check point total
        total_points = sum(card_points(card, self.config) for card in hand)
        if total_points >= self.config['step2_bet_threshold']:
            return 'bet1'
        else:
            return 'fold'

    def eval_step_3(self, hand):
        """
        Evaluate the player's hand after the fourth card is dealt (step 3).
        Args:
            hand (list): The player's hand (list of four cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the hand.
        """
        ranks = [card % 13 for card in hand]
        
        # Check for quads
        has_quads, _ = HandAnalyzer.has_quads(ranks)
        if has_quads:
            return 'bet3'
        
        # Check for trips
        has_trips, _ = HandAnalyzer.has_trips(ranks)
        if has_trips:
            return 'bet3'
        
        # Check for a pair of sixes or better
        has_high_pair, _ = HandAnalyzer.has_pair(ranks, self.config['min_push_pair_rank'])
        if has_high_pair:
            return 'bet3'
        
        # Check for any other pair
        has_any_pair, _ = HandAnalyzer.has_pair(ranks)
        if has_any_pair:
            return 'bet1'
        
        # Check point total
        total_points = sum(card_points(card, self.config) for card in hand)
        if total_points >= self.config['step3_bet_threshold']:
            return 'bet1'
        else:
            return 'fold'
