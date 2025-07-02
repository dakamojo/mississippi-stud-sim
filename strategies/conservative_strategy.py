from .base_strategy import BaseStrategy
from config import STRATEGY_CONFIG

class ConservativeStrategy(BaseStrategy):
    """
    A Conservative Strategy for Mississippi Stud betting decisions.
    This strategy is more conservative than the Point Strategy and only
    makes larger bets with very strong hands.
    """
    
    def __init__(self, config=None):
        """Initialize the Conservative Strategy with configuration."""
        self.config = config or STRATEGY_CONFIG
    
    def eval_step_1(self, hand):
        """Conservative evaluation for step 1 - only bet on strong hands."""
        card1, card2 = hand
        rank1 = card1 % 13
        rank2 = card2 % 13
        
        # Only bet big on high pairs (10s or better)
        if rank1 == rank2:
            if rank1 >= 8:  # 10s or better
                return 'bet3'
            elif rank1 >= self.config['min_push_pair_rank']:
                return 'bet1'  # 6-9 pairs
            else:
                return 'fold'  # Lower pairs
        # Very conservative - only bet on two high cards
        elif rank1 >= 9 and rank2 >= 9:  # Both Jacks or higher
            return 'bet1'
        else:
            return 'fold'
    
    def eval_step_2(self, hand):
        """Conservative evaluation for step 2."""
        card1, card2, card3 = hand
        ranks = [card1 % 13, card2 % 13, card3 % 13]
        
        # Check for trips
        if ranks[0] == ranks[1] == ranks[2]:
            return 'bet3'
        # Check for high pairs only
        for i in range(3):
            for j in range(i+1, 3):
                if ranks[i] == ranks[j]:
                    if ranks[i] >= 8:  # 10s or better
                        return 'bet3'
                    elif ranks[i] >= self.config['min_push_pair_rank']:
                        return 'bet1'  # 6-9 pairs
                    else:
                        return 'fold'  # Lower pairs
        # Very conservative - only continue with 3 high cards
        high_cards = sum(1 for rank in ranks if rank >= 9)
        if high_cards >= 3:
            return 'bet1'
        else:
            return 'fold'
    
    def eval_step_3(self, hand):
        """Conservative evaluation for step 3."""
        card1, card2, card3, card4 = hand
        ranks = [card1 % 13, card2 % 13, card3 % 13, card4 % 13]
        
        # Check for quads
        if len(set(ranks)) == 1:
            return 'bet3'
        # Check for trips
        for i in range(4):
            for j in range(i+1, 4):
                for k in range(j+1, 4):
                    if ranks[i] == ranks[j] == ranks[k]:
                        return 'bet3'
        # Check for high pairs only
        for i in range(4):
            for j in range(i+1, 4):
                if ranks[i] == ranks[j]:
                    if ranks[i] >= 8:  # 10s or better
                        return 'bet3'
                    elif ranks[i] >= self.config['min_push_pair_rank']:
                        return 'bet1'  # 6-9 pairs
                    else:
                        return 'fold'  # Lower pairs
        # Very conservative - only continue with mostly high cards
        high_cards = sum(1 for rank in ranks if rank >= 9)
        if high_cards >= 3:
            return 'bet1'
        else:
            return 'fold'
