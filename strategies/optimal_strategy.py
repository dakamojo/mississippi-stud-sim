from .base_strategy import BaseStrategy
from utils.hand_analyzer import HandAnalyzer

class OptimalStrategy(BaseStrategy):
    """
    Optimal Strategy for Mississippi Stud based on mathematical analysis.
    This strategy follows proven optimal play for maximum expected value.
    """
    
    def __init__(self, config=None):
        """Initialize the Optimal Strategy."""
        self.analyzer = HandAnalyzer()
    
    def eval_step_1(self, hand):
        """Optimal evaluation for step 1 based on mathematical analysis."""
        card1, card2 = hand
        rank1 = card1 % 13
        rank2 = card2 % 13
        
        # Always bet 3x with pairs of 6s or better
        if rank1 == rank2 and rank1 >= 5:  # 6s or better
            return 'bet3'
        
        # Bet 1x with medium pairs (2s-5s)
        if rank1 == rank2 and rank1 >= 1:  # 3s-5s (rank 1-4)
            return 'bet1'
        
        # High card hands - bet 1x with Q-6 or better
        if sorted([rank1, rank2], reverse=True) >= [11, 5]:  # Q-6 or better
            return 'bet1'
        
        # Otherwise fold
        return 'fold'
    
    def eval_step_2(self, hand):
        """Optimal evaluation for step 2."""
        card1, card2, card3 = hand
        ranks = sorted([card1 % 13, card2 % 13, card3 % 13])
        
        # Always bet 3x with trips
        if ranks[0] == ranks[1] == ranks[2]:
            return 'bet3'
        
        # Always bet 3x with pairs of 6s or better
        pair_rank = self.analyzer.get_pair_rank([card1, card2, card3])
        if pair_rank is not None and pair_rank >= 5:  # 6s or better
            return 'bet3'
        
        # Bet 1x with pairs of 5s or lower
        if pair_rank is not None:
            return 'bet1'
        
        # High card hands - bet 1x with Q-6-4 or better
        if ranks >= [3, 5, 11]:  # Q-6-4 or better
            return 'bet1'
        
        # Check for flush draws and straight draws
        suits = [card1 // 13, card2 // 13, card3 // 13]
        if len(set(suits)) == 1:  # All same suit (flush draw)
            return 'bet1'
        
        # Check for open-ended straight draws
        if self.analyzer.has_straight_draw([card1, card2, card3]):
            return 'bet1'
        
        # Otherwise fold
        return 'fold'
    
    def eval_step_3(self, hand):
        """Optimal evaluation for step 3."""
        card1, card2, card3, card4 = hand
        ranks = sorted([card1 % 13, card2 % 13, card3 % 13, card4 % 13])
        
        # Always bet 3x with quads
        if ranks[0] == ranks[1] == ranks[2] == ranks[3]:
            return 'bet3'
        
        # Always bet 3x with trips
        trip_rank = self.analyzer.get_trips_rank([card1, card2, card3, card4])
        if trip_rank is not None:
            return 'bet3'
        
        # Always bet 3x with pairs of 6s or better
        pair_rank = self.analyzer.get_pair_rank([card1, card2, card3, card4])
        if pair_rank is not None and pair_rank >= 5:  # 6s or better
            return 'bet3'
        
        # Bet 1x with pairs of 5s or lower
        if pair_rank is not None:
            return 'bet1'
        
        # High card hands - bet 1x with Q-6-4-2 or better
        if ranks >= [1, 3, 5, 11]:  # Q-6-4-2 or better
            return 'bet1'
        
        # Check for flush draws (4 cards same suit)
        suits = [card1 // 13, card2 // 13, card3 // 13, card4 // 13]
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        if max(suit_counts.values()) >= 4:  # 4-card flush draw
            return 'bet1'
        
        # Check for straight draws
        if self.analyzer.has_straight_draw([card1, card2, card3, card4]):
            return 'bet1'
        
        # Otherwise fold
        return 'fold'
