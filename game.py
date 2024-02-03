from player import Player
import random

class Game:
    def __init__(self, player1_name=None, player2_name=None):
        self.player1 = self.create_player(player1_name) if player1_name else None
        self.player2 = self.create_player(player2_name) if player2_name else None
        self.general_deck = None
        self.table = []

    def create_deck(self):
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.ranks_value = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
        self.general_deck = []

        for i in range(2):
            for suit in self.suits:
                for rank in self.ranks:
                    value = self.ranks_value[rank]
                    card_name = f"{rank} of {suit}"
                    self.general_deck.append({
                        'Suit': suit,
                        'Rank': rank,
                        'Value': value,
                        'DeckNumber': i + 1
                    })

        return self.general_deck



    def create_player(self, name):
        return Player(name, 0)
    
    def is_valid(self, pile, allow_single=False):
        num_cards = len(pile)

        if num_cards < 3 and not allow_single:
            return False

        suits_set = set(card['Suit'] for card in pile)
        values_set = set(card['Value'] for card in pile)

        # Check for three cards with the same rank but different suits
        if len(suits_set) == num_cards and len(values_set) == 1:
            return True

        # Check for consecutive cards with the same suit
        if len(suits_set) == 1 and len(values_set) == num_cards:
            sorted_values = sorted(values_set)
            if all(value in sorted_values for value in range(sorted_values[0], sorted_values[-1] + 1)):
                return True

        return False
    
    def shuffle_deck(self):
        random.shuffle(self.general_deck)
    
    def draw_cards(self):
        if not self.player1:
            self.player1 = self.create_player("Player 1")
        if not self.player1.deck:
            # Shuffle the deck if not done already
            if not self.general_deck:
                self.create_deck()
            self.shuffle_deck()
            
            # Draw 6 cards at the beginning of the game
            self.player1.deck = self.general_deck[:6]
            self.general_deck = self.general_deck[6:]
        else:
            # Draw 1 card if the deck already exists
            self.player1.deck.append(self.general_deck.pop())

    # Inside the Game class in game.py
    def validate_combination(self, selected_cards_indices, stack_index, position):
        # Validate selected indices
        if not all(0 <= idx < len(self.player1.deck) for idx in selected_cards_indices):
            return False, "Invalid card indices. Please select cards from your hand."

        # Validate stack index
        if not (0 <= stack_index < len(self.table)):
            return False, "Invalid stack index. Please select a valid stack."

        # Create a pile with selected cards from the player's hand
        selected_pile = [self.player1.deck[idx] for idx in selected_cards_indices]

        # Create a temporary deck for validation
        temp_deck = self.table[stack_index].copy()

        # Add the selected pile to the temporary deck based on the specified position
        if position == "front":
            temp_deck = selected_pile + temp_deck
        elif position == "end":
            temp_deck += selected_pile
        else:
            return False, "Invalid position. Please choose 'front' or 'end'."

        # Check if the combination is valid using the is_valid function
        if not self.is_valid(temp_deck, allow_single=True):
            return False, "Invalid combination of cards. Please select a valid set of cards."

        return True, "Combination is valid."

    # Inside the Game class in game.py
    def add_cards_to_stack(self, selected_cards_indices, stack_index):
        # Validate the combination
        first_card_rank = self.table[stack_index][0]['Value']
        max_player_card_rank = max(self.player1.deck[idx]['Value'] for idx in selected_cards_indices)
        position = "front" if first_card_rank > max_player_card_rank else "end"

        success, message = self.validate_combination(selected_cards_indices, stack_index, position)

        # If the combination is valid, proceed with adding cards to the stack
        if success:
            # Create a pile with selected cards from the player's hand
            pile = [self.player1.deck[idx] for idx in selected_cards_indices]

            # Add the cards to the specified position in the stack
            if position == "front":
                self.table[stack_index] = pile + self.table[stack_index]
            elif position == "end":
                self.table[stack_index] += pile

            # Remove the selected cards from the player's hand
            for idx in sorted(selected_cards_indices, reverse=True):
                del self.player1.deck[idx]

            return True, "Cards successfully added to the stack."

        # If the combination is not valid, return an error message
        return False, message

    
    def put_cards_on_table(self, selected_cards_indices):
        # Validate selected indices
        if not all(0 <= idx < len(self.player1.deck) for idx in selected_cards_indices):
            return False, "Invalid card indices. Please select cards from your hand."

        # Create a pile with selected cards
        pile = [self.player1.deck[idx] for idx in selected_cards_indices]

        # Check if the pile is valid using is_valid function
        if not self.is_valid(pile):
            return False, "Invalid combination of cards. Please select a valid set of cards."

        # Sort the pile in ascending order based on card values
        sorted_pile = sorted(pile, key=lambda x: x['Value'])

        # Append the valid pile as a separate list to the table
        self.table.append(sorted_pile)

        # Remove the selected cards from the player's hand
        for idx in sorted(selected_cards_indices, reverse=True):
            del self.player1.deck[idx]

        return True, "Cards successfully put on the table."
        

    def display_deck(self, deck):
         for card in deck:
             print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

    