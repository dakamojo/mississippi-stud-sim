# Mississippi Stud payout table (example, can be adjusted):
payout_table = {
    1: 500,   # Royal Flush
    2: 100,   # Straight Flush
    3: 40,    # Four of a Kind
    4: 10,    # Full House
    5: 6,     # Flush
    6: 4,     # Straight
    7: 3,     # Three of a Kind
    8: 2,     # Two Pair
    9: 1      # Pair of Jacks or Better
}

# Global counter for hand class outcomes
hand_class_counter = {
    'royal_flush': 0,
    'straight_flush': 0,
    'four_of_a_kind': 0,
    'full_house': 0,
    'flush': 0,
    'straight': 0,
    'three_of_a_kind': 0,
    'two_pair': 0,
    'pair_jacks_or_better': 0,
    'pair_6_to_10': 0,
    'loss': 0
}

from deuces import Deck, Evaluator

def simulate(number_of_hands):
    """
    Simulate a given number of hands.
    Args:
        number_of_hands (int): The number of hands to simulate.
    """
    # Reset hand_class_counter before each simulation
    for k in hand_class_counter:
        hand_class_counter[k] = 0
    simulation_payout = 0
    for i in range(number_of_hands):
        payout = simulate_hand()
        simulation_payout += payout
    print(f"Simulated {number_of_hands} hands.")
    print(f"Total payout/loss: {simulation_payout}")
    print("Hand class frequencies:")
    for k, v in hand_class_counter.items():
        print(f"  {k}: {v}")


def simulate_hand():
    """
    Simulate a single hand.
    """
    bet_amount = 2
    deck = Deck()
    deck.shuffle()
    # Draw two cards for the hand
    hand = [deck.draw(1), deck.draw(1)]
    result = eval_step_1(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        return -bet_amount
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw third card and evaluate step 2
    hand.append(deck.draw(1))
    result = eval_step_2(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        return -bet_amount
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw fourth card and evaluate step 3
    hand.append(deck.draw(1))
    result = eval_step_3(hand)
    if result == 'fold':
        hand_class_counter['loss'] += 1
        return -bet_amount
    elif result == 'bet3':
        bet_amount += 3
    elif result == 'bet1':
        bet_amount += 1
    # Draw fifth card and evaluate as a poker hand
    hand.append(deck.draw(1))
    evaluator = Evaluator()
    board = hand[2:]  # The last three cards are the board in Mississippi Stud
    player_hand = hand[:2]
    score = evaluator.evaluate(board, player_hand)
    hand_class = evaluator.get_rank_class(score)
    # Mississippi Stud payout calculation fix
    payout_factor = 0
    outcome_key = None
    if hand_class in payout_table and hand_class != 9:
        payout_factor = payout_table[hand_class]
        key_map = {
            1: 'royal_flush',
            2: 'straight_flush',
            3: 'four_of_a_kind',
            4: 'full_house',
            5: 'flush',
            6: 'straight',
            7: 'three_of_a_kind',
            8: 'two_pair',
        }
        outcome_key = key_map.get(hand_class, None)
    elif hand_class == 9:
        ranks = [card % 13 for card in hand]
        rank_counts = {r: ranks.count(r) for r in set(ranks)}
        pair_rank = [r for r, c in rank_counts.items() if c == 2]
        if pair_rank and pair_rank[0] >= 9:  # J=9, Q=10, K=11, A=12
            payout_factor = payout_table[9]
            outcome_key = 'pair_jacks_or_better'
        elif pair_rank and 4 <= pair_rank[0] <= 8:  # 6=4, 7=5, 8=6, 9=7, 10=8
            outcome_key = 'pair_6_to_10'
            hand_class_counter[outcome_key] += 1
            return 0
        else:
            outcome_key = 'loss'
            hand_class_counter[outcome_key] += 1
            return -bet_amount
    else:
        outcome_key = 'loss'
    if outcome_key:
        hand_class_counter[outcome_key] += 1
    if payout_factor > 0:
        # Payout is payout_factor * bet_amount (all bets), per your variant
        payout = payout_factor * bet_amount
        return payout
    else:
        return -bet_amount

def eval_step_1(hand):
    """
    Evaluate the player's hand after the first two cards are dealt (step 1).
    Args:
        hand (list): The player's hand (list of two cards).
    Returns:
        str: 'fold', 'betx1', or 'betx3' based on the hand.
    """
    card1, card2 = hand
    rank1 = card1 % 13
    rank2 = card2 % 13
    # Removed unused variables suit1 and suit2
    if rank1 == rank2:
        if rank1 >= 4:  # 6 is rank 4 (0=2, 1=3, 2=4, 3=5, 4=6, ...)
            return 'bet3'  # Pair of sixes or higher
        else:
            return 'bet1'  # Lower pairs
    elif card_points(card1) + card_points(card2) >= 3:
        return 'bet1'
    else:
        return 'fold'

def eval_step_2(hand):
    """
    Evaluate the player's hand after the third card is dealt (step 2).
    Args:
        hand (list): The player's hand (list of three cards).
    Returns:
        str: 'fold', 'betx1', or 'betx3' based on the hand.
    """
    card1, card2, card3 = hand
    ranks = [card1 % 13, card2 % 13, card3 % 13]
    # Check for trips first
    if ranks[0] == ranks[1] == ranks[2]:
        return 'bet3'  # Trips
    # Check for a pair of sixes or better
    for i in range(3):
        for j in range(i+1, 3):
            if ranks[i] == ranks[j] and ranks[i] >= 4:  # 4=6, 5=7, ...
                return 'bet3'  # Pair of sixes or higher
    # Check for any other pair
    for i in range(3):
        for j in range(i+1, 3):
            if ranks[i] == ranks[j]:
                return 'bet1'  # Any other pair
    if card_points(card1) + card_points(card2) + card_points(card3) >= 4:
        return 'bet1'
    else:
        return 'fold'

def eval_step_3(hand):
    """
    Evaluate the player's hand after the fourth card is dealt (step 3).
    Args:
        hand (list): The player's hand (list of four cards).
    Returns:
        str: 'fold', 'betx1', or 'betx3' based on the hand.
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
            if ranks[i] == ranks[j] and ranks[i] >= 4:
                return 'bet3'  # Pair of sixes or higher
    # Check for any other pair
    for i in range(4):
        for j in range(i+1, 4):
            if ranks[i] == ranks[j]:
                return 'bet1'  # Any other pair
    if sum(card_points(card) for card in hand) >= 5:
        return 'bet1'
    else:
        return 'fold'

def card_points(card):
    """
    Returns the point value of a card for Mississippi Stud strategy:
    - 1 if the card is between 6 and 10 (inclusive)
    - 2 if the card is greater than 10 (J, Q, K, A)
    - 0 otherwise
    Args:
        card (int): The integer-encoded card from deuces.
    Returns:
        int: The point value of the card.
    """
    rank = card % 13
    # deuces: 0=2, 1=3, 2=4, 3=5, 4=6, 5=7, 6=8, 7=9, 8=10, 9=J, 10=Q, 11=K, 12=A
    if 4 <= rank <= 8:
        return 1  # 6-10
    elif rank >= 9:
        return 2  # J, Q, K, A
    else:
        return 0

if __name__ == "__main__":
    # Run the simulation 10 times with 100 hands each, aggregate statistics and show payout per run
    runs = 10
    hands_per_run = 100
    grand_aggregate_counter = {k: 0 for k in hand_class_counter}
    payouts = []
    for run in range(runs):
        print(f"\n--- Simulation Run {run+1} ---")
        # Capture payout for this run
        from contextlib import redirect_stdout
        import io
        f = io.StringIO()
        with redirect_stdout(f):
            simulate(hands_per_run)
        output = f.getvalue().splitlines()
        # Find payout line
        payout = None
        for line in output:
            if line.startswith("Total payout/loss:"):
                payout = int(line.split(":")[1].strip())
                break
        payouts.append(payout)
        # Print the output for this run
        print("\n".join(output))
        # After each run, add to grand totals
        for k in hand_class_counter:
            grand_aggregate_counter[k] += hand_class_counter[k]
    print(f"\nPayout for each run: {payouts}")
    print(f"Average payout per run: {sum(payouts)/len(payouts):.2f}")
    print(f"\nAggregated results over {runs} runs of {hands_per_run} hands each:")
    for k, v in grand_aggregate_counter.items():
        print(f"  {k}: {v}")
