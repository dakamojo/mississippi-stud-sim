from deuces import Deck, Evaluator, Card
from config import (
    PAYOUT_TABLE, 
    ROYAL_FLUSH_PAYOUT,
    DEFAULT_BET, 
    HAND_OUTCOMES, 
    STRATEGY_CONFIG,
    SIMULATION_CONFIG
)

# Global counter for hand class outcomes
hand_class_counter = {outcome: 0 for outcome in HAND_OUTCOMES}

class PointStrategy:
    """
    The Point Strategy for Mississippi Stud betting decisions.
    This strategy assigns point values to cards and makes betting decisions
    based on hand strength and accumulated points.
    """
    
    def __init__(self, config=None):
        """Initialize the Point Strategy with configuration."""
        self.config = config or STRATEGY_CONFIG
    
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
        elif self._card_points(card1) + self._card_points(card2) >= self.config['step1_bet_threshold']:
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
        card1, card2, card3 = hand
        ranks = [card1 % 13, card2 % 13, card3 % 13]
        # Check for trips first
        if ranks[0] == ranks[1] == ranks[2]:
            return 'bet3'  # Trips
        # Check for a pair of sixes or better
        for i in range(3):
            for j in range(i+1, 3):
                if ranks[i] == ranks[j] and ranks[i] >= self.config['min_push_pair_rank']:
                    return 'bet3'  # Pair of sixes or higher
        # Check for any other pair
        for i in range(3):
            for j in range(i+1, 3):
                if ranks[i] == ranks[j]:
                    return 'bet1'  # Any other pair
        if self._card_points(card1) + self._card_points(card2) + self._card_points(card3) >= self.config['step2_bet_threshold']:
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
        card1, card2, card3, card4 = hand
        ranks = [card1 % 13, card2 % 13, card3 % 13, card4 % 13]
        # Check for quads
        if len(set(ranks)) == 1:
            return 'bet3'  # Four of a kind
        # Check for trips
        for i in range(4):
            for j in range(i+1, 4):
                for k in range(j+1, 4):
                    if ranks[i] == ranks[j] == ranks[k]:
                        return 'bet3'  # Trips
        # Check for a pair of sixes or better
        for i in range(4):
            for j in range(i+1, 4):
                if ranks[i] == ranks[j] and ranks[i] >= self.config['min_push_pair_rank']:
                    return 'bet3'  # Pair of sixes or higher
        # Check for any other pair
        for i in range(4):
            for j in range(i+1, 4):
                if ranks[i] == ranks[j]:
                    return 'bet1'  # Any other pair
        if sum(self._card_points(card) for card in hand) >= self.config['step3_bet_threshold']:
            return 'bet1'
        else:
            return 'fold'

    def _card_points(self, card):
        """
        Returns the point value of a card for Mississippi Stud strategy:
        - 0 if the card is low (2-5)
        - 1 if the card is medium (6-10)
        - 2 if the card is high (J-A)
        Args:
            card (int): The integer-encoded card from deuces.
        Returns:
            int: The point value of the card.
        """
        rank = card % 13
        # deuces: 0=2, 1=3, 2=4, 3=5, 4=6, 5=7, 6=8, 7=9, 8=10, 9=J, 10=Q, 11=K, 12=A
        if 4 <= rank <= 8:  # 6-10
            return self.config['card_points']['push_cards']
        elif rank >= 9:  # J-A
            return self.config['card_points']['high_cards']
        else:  # 2-5
            return self.config['card_points']['low_cards']

class ConservativeStrategy:
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
    
    def _card_points(self, card):
        """Use same point system as Point Strategy."""
        rank = card % 13
        if 4 <= rank <= 8:  # 6-10
            return self.config['card_points']['push_cards']
        elif rank >= 9:  # J-A
            return self.config['card_points']['high_cards']
        else:  # 2-5
            return self.config['card_points']['low_cards']

# Strategy factory - makes it easy to add new strategies
STRATEGIES = {
    'point': PointStrategy,
    'conservative': ConservativeStrategy
}

def get_strategy(strategy_name='point', config=None):
    """
    Get a strategy instance by name.
    Args:
        strategy_name (str): Name of the strategy to use.
        config (dict): Optional configuration for the strategy.
    Returns:
        Strategy instance.
    """
    if strategy_name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(STRATEGIES.keys())}")
    return STRATEGIES[strategy_name](config)

def simulate(number_of_hands, show_each_hand=False, strategy_name='point'):
    """
    Simulate a given number of hands.
    Args:
        number_of_hands (int): The number of hands to simulate.
        show_each_hand (bool): If True, print the result of each hand.
        strategy_name (str): Name of the strategy to use.
    """
    for k in hand_class_counter:
        hand_class_counter[k] = 0
    simulation_payout = 0
    strategy = get_strategy(strategy_name)
    for i in range(number_of_hands):
        payout, hand_result, hand = simulate_hand(strategy=strategy, return_cards=True)
        simulation_payout += payout
        if show_each_hand:
            hand_str = ' '.join(Card.int_to_str(c) for c in hand)
            print(f"{i+1:3}: [{hand_str}] {hand_result} (payout: {payout}) | simulation_payout: {simulation_payout}")
    print(f"Simulated {number_of_hands} hands.")
    print(f"Total payout/loss: {simulation_payout}")
    print("Hand class frequencies:")
    for k, v in hand_class_counter.items():
        print(f"  {k}: {v}")


def simulate_hand(strategy=None, return_cards=False):
    """
    Simulate a single hand. Always returns (payout, hand_result).
    """
    if strategy is None:
        strategy = get_strategy('point')
    
    bet_amount = DEFAULT_BET
    deck = Deck()
    deck.shuffle()
    # Draw two cards for the hand
    hand = [deck.draw(1), deck.draw(1)]
    result = strategy.eval_step_1(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        if return_cards:
            return -bet_amount, 'folded pre-flop', hand[:2]
        return -bet_amount, 'folded pre-flop'
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw third card and evaluate step 2
    hand.append(deck.draw(1))
    result = strategy.eval_step_2(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        if return_cards:
            return -bet_amount, 'folded after 3rd card', hand[:3]
        return -bet_amount, 'folded after 3rd card'
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw fourth card and evaluate step 3
    hand.append(deck.draw(1))
    result = strategy.eval_step_3(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        if return_cards:
            return -bet_amount, 'folded after 4th card', hand[:4]
        return -bet_amount, 'folded after 4th card'
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw fifth card and evaluate as a poker hand
    hand.append(deck.draw(1))
    evaluator = Evaluator()
    # Mississippi Stud: evaluate all 5 cards as the player's hand, with an empty board
    score = evaluator.evaluate([], hand)
    hand_class = evaluator.get_rank_class(score)
    payout_factor = 0
    outcome_key = None
    hand_desc = evaluator.class_to_string(hand_class)
    
    if hand_class in PAYOUT_TABLE and hand_class != 9:  # 9 = High Card
        # Check for Royal Flush (score=1 within Straight Flush class)
        if hand_class == 1 and score == 1:
            payout_factor = ROYAL_FLUSH_PAYOUT
            outcome_key = 'royal_flush'
        elif hand_class == 8:  # One Pair - check rank for payout eligibility
            ranks = [card % 13 for card in hand]
            rank_counts = {r: ranks.count(r) for r in set(ranks)}
            pair_rank = [r for r, c in rank_counts.items() if c == 2]
            if pair_rank and pair_rank[0] >= STRATEGY_CONFIG['min_high_pair_rank']:
                # Jacks or better - pays
                payout_factor = PAYOUT_TABLE[8]
                outcome_key = 'pair_jacks_or_better'
                hand_desc = 'Pair Jacks or Better'
            elif pair_rank and STRATEGY_CONFIG['min_push_pair_rank'] <= pair_rank[0] <= 8:
                # Push pair (6-10) - no payout but no loss
                outcome_key = 'pair_6_to_10'
                hand_class_counter[outcome_key] += 1
                if return_cards:
                    return 0, 'Pair 6 to 10', hand
                return 0, 'Pair 6 to 10'
            else:
                # Lower pairs (2-5) - loss
                outcome_key = 'loss'
                hand_class_counter[outcome_key] += 1
                if return_cards:
                    return -bet_amount, 'loss (pair 2-5)', hand
                return -bet_amount, 'loss (pair 2-5)'
        else:
            # All other paying hands
            payout_factor = PAYOUT_TABLE.get(hand_class, 0)
            hand_class_to_outcome = {
                1: 'straight_flush',
                2: 'four_of_a_kind',
                3: 'full_house',
                4: 'flush',
                5: 'straight',
                6: 'three_of_a_kind',
                7: 'two_pair'
            }
            outcome_key = hand_class_to_outcome.get(hand_class)
    else:
        # High card - always a loss
        outcome_key = 'high_card'
        hand_class_counter[outcome_key] += 1
        if return_cards:
            return -bet_amount, 'loss (high card)', hand
        return -bet_amount, 'loss (high card)'
    
    if outcome_key:
        hand_class_counter[outcome_key] += 1
    
    if payout_factor > 0:
        payout = payout_factor * bet_amount
        if return_cards:
            return payout, hand_desc, hand
        return payout, hand_desc
    else:
        if return_cards:
            return -bet_amount, hand_desc, hand
        return -bet_amount, hand_desc

if __name__ == "__main__":
    # Run the simulation using configuration defaults
    simulate(
        SIMULATION_CONFIG['default_hands'], 
        show_each_hand=SIMULATION_CONFIG['show_each_hand'],
        strategy_name='point'
    )
