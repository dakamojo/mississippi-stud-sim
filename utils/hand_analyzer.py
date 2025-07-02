"""
Hand analysis utilities for Mississippi Stud strategies.
"""

from collections import Counter
from typing import List, Tuple, Optional, Dict


class HandAnalyzer:
    """
    Utility class for analyzing poker hands in Mississippi Stud.
    Provides common hand analysis functions used by multiple strategies.
    """
    
    @staticmethod
    def get_rank_counts(ranks: List[int]) -> Dict[int, int]:
        """
        Get the count of each rank in the hand.
        Args:
            ranks (List[int]): List of card ranks.
        Returns:
            Dict[int, int]: Dictionary mapping rank to count.
        """
        return dict(Counter(ranks))
    
    @staticmethod
    def has_pair(ranks: List[int], min_rank: Optional[int] = None) -> Tuple[bool, Optional[int]]:
        """
        Check if the hand has a pair, optionally of minimum rank.
        Args:
            ranks (List[int]): List of card ranks.
            min_rank (Optional[int]): Minimum rank for the pair. If None, any pair counts.
        Returns:
            Tuple[bool, Optional[int]]: (has_pair, pair_rank). pair_rank is None if no pair found.
        """
        rank_counts = HandAnalyzer.get_rank_counts(ranks)
        for rank, count in rank_counts.items():
            if count >= 2 and (min_rank is None or rank >= min_rank):
                return True, rank
        return False, None
    
    @staticmethod
    def has_trips(ranks: List[int]) -> Tuple[bool, Optional[int]]:
        """
        Check if the hand has three of a kind.
        Args:
            ranks (List[int]): List of card ranks.
        Returns:
            Tuple[bool, Optional[int]]: (has_trips, trips_rank). trips_rank is None if no trips found.
        """
        rank_counts = HandAnalyzer.get_rank_counts(ranks)
        for rank, count in rank_counts.items():
            if count >= 3:
                return True, rank
        return False, None
    
    @staticmethod
    def has_quads(ranks: List[int]) -> Tuple[bool, Optional[int]]:
        """
        Check if the hand has four of a kind.
        Args:
            ranks (List[int]): List of card ranks.
        Returns:
            Tuple[bool, Optional[int]]: (has_quads, quads_rank). quads_rank is None if no quads found.
        """
        rank_counts = HandAnalyzer.get_rank_counts(ranks)
        for rank, count in rank_counts.items():
            if count >= 4:
                return True, rank
        return False, None
    
    @staticmethod
    def has_flush_draw(suits: List[int], min_suited: int = 3) -> bool:
        """
        Check if the hand has a flush draw (multiple cards of same suit).
        Args:
            suits (List[int]): List of card suits.
            min_suited (int): Minimum number of suited cards required.
        Returns:
            bool: True if flush draw exists, False otherwise.
        """
        suit_counts = Counter(suits)
        return max(suit_counts.values()) >= min_suited
    
    @staticmethod
    def count_high_cards(ranks: List[int], min_rank: int = 9) -> int:
        """
        Count the number of high cards (default: Jack or higher).
        Args:
            ranks (List[int]): List of card ranks.
            min_rank (int): Minimum rank to be considered high (default: 9 = Jack).
        Returns:
            int: Number of high cards.
        """
        return sum(1 for rank in ranks if rank >= min_rank)
    
    @staticmethod
    def has_straight_draw(cards: List[int]) -> bool:
        """
        Check if the hand has a straight draw potential.
        Args:
            cards (List[int]): List of cards (full card values, not just ranks).
        Returns:
            bool: True if straight draw exists, False otherwise.
        """
        ranks = [card % 13 for card in cards]
        return HandAnalyzer._has_straight_draw_from_ranks(ranks, 3)
    
    @staticmethod
    def _has_straight_draw_from_ranks(ranks: List[int], cards_needed: int = 3) -> bool:
        """
        Check if the hand has a straight draw potential from ranks.
        Args:
            ranks (List[int]): List of card ranks.
            cards_needed (int): Minimum consecutive cards needed to consider it a draw.
        Returns:
            bool: True if straight draw exists, False otherwise.
        """
        sorted_ranks = sorted(set(ranks))
        
        if len(sorted_ranks) < cards_needed:
            return False
        
        # Check for consecutive ranks
        for i in range(len(sorted_ranks) - cards_needed + 1):
            consecutive = True
            for j in range(cards_needed - 1):
                if sorted_ranks[i + j + 1] != sorted_ranks[i + j] + 1:
                    consecutive = False
                    break
            
            if consecutive:
                # Check if this can be extended (for open-ended draws)
                if cards_needed == 3:
                    # For 3-card draws, check if extendable on either end
                    if sorted_ranks[i] > 0 or sorted_ranks[i + cards_needed - 1] < 12:
                        return True
                else:
                    # For 4+ card draws, already a strong draw
                    return True
        
        # Special case for low ace straights (A-2-3, A-2-3-4, etc.)
        if 12 in sorted_ranks:  # Ace present
            low_ranks = [r for r in sorted_ranks if r <= 3]
            if len(low_ranks) >= cards_needed - 1:
                return True
        
        return False
    
    @staticmethod
    def get_pair_rank(cards: List[int]) -> Optional[int]:
        """
        Get the rank of a pair in the hand, if one exists.
        Args:
            cards (List[int]): List of cards (full card values, not just ranks).
        Returns:
            Optional[int]: The rank of the pair, or None if no pair found.
        """
        ranks = [card % 13 for card in cards]
        _, pair_rank = HandAnalyzer.has_pair(ranks)
        return pair_rank
    
    @staticmethod
    def get_trips_rank(cards: List[int]) -> Optional[int]:
        """
        Get the rank of trips in the hand, if they exist.
        Args:
            cards (List[int]): List of cards (full card values, not just ranks).
        Returns:
            Optional[int]: The rank of the trips, or None if no trips found.
        """
        ranks = [card % 13 for card in cards]
        _, trips_rank = HandAnalyzer.has_trips(ranks)
        return trips_rank
    
    @staticmethod
    def get_quads_rank(cards: List[int]) -> Optional[int]:
        """
        Get the rank of quads in the hand, if they exist.
        Args:
            cards (List[int]): List of cards (full card values, not just ranks).
        Returns:
            Optional[int]: The rank of the quads, or None if no quads found.
        """
        ranks = [card % 13 for card in cards]
        _, quads_rank = HandAnalyzer.has_quads(ranks)
        return quads_rank
