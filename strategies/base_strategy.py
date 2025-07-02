"""
Base strategy class for Mississippi Stud betting decisions.
"""

from abc import ABC, abstractmethod
from config import STRATEGY_CONFIG


class BaseStrategy(ABC):
    """
    Abstract base class for Mississippi Stud strategies.
    All strategies must implement the three evaluation methods for each betting round.
    """
    
    def __init__(self, config=None):
        """
        Initialize the strategy with configuration.
        Args:
            config (dict): Optional configuration dictionary. If None, uses STRATEGY_CONFIG.
        """
        self.config = config or STRATEGY_CONFIG
    
    @abstractmethod
    def eval_step_1(self, hand):
        """
        Evaluate the player's hand after the first two cards are dealt (step 1).
        Args:
            hand (list): The player's hand (list of two cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the strategy.
        """
        pass
    
    @abstractmethod
    def eval_step_2(self, hand):
        """
        Evaluate the player's hand after the third card is dealt (step 2).
        Args:
            hand (list): The player's hand (list of three cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the strategy.
        """
        pass
    
    @abstractmethod
    def eval_step_3(self, hand):
        """
        Evaluate the player's hand after the fourth card is dealt (step 3).
        Args:
            hand (list): The player's hand (list of four cards).
        Returns:
            str: 'fold', 'bet1', or 'bet3' based on the strategy.
        """
        pass
