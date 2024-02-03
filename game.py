from player import Player
import random

class Player2(Player):
    def __init__(self, name, score):
        super().__init__(name, score)
        self.deck = []

class Game:
    def __init__(self, player1_name=None, player2_name=None):
        self.player1 = self.create_player(player1_name) if player1_name else None
        self.player2 = self.create_player(player2_name) if player2_name else None
        self.has_put_stack_player1 = False  # Initialize for player 1
        self.has_put_stack_player2 = False  # Initialize for player 2
        self.general_deck = None
        self.table = []
        self.current_player = self.player1


    def create_player(self, name, player_class=Player):
        return player_class(name, 0)

    def get_game_mode(self):
        if self.player2:
            return 'hotseat'
        # Add conditions for other game modes if needed

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
    
    def start_hotseat(self, player1_name, player2_name):
        self.player1 = self.create_player(player1_name)
        self.player2 = self.create_player(player2_name, player_class=Player2)

    def is_game_over(self):
        return not self.general_deck

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
        if not self.current_player:
            return  # No current player, do nothing

        # Draw 1 card when the button is pressed
        if not self.current_player.deck:
            # Shuffle the deck if not done already
            if not self.general_deck:
                self.create_deck()
            self.shuffle_deck()

            # Draw 6 cards at the beginning of the game
            self.current_player.deck = self.general_deck[:6]
            self.general_deck = self.general_deck[6:]
        else:
            # Draw 1 card if the deck already exists
            self.current_player.deck.append(self.general_deck.pop())

        # Switch to the next player's turn
        self.switch_to_next_player()

    def switch_to_next_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Inside the Game class in game.py
    def validate_combination(self, selected_cards_indices, stack_index, position):
        # Validate selected indices
        if not all(0 <= idx < len(self.current_player.deck) for idx in selected_cards_indices):
            return False, "Invalid card indices. Please select cards from your hand."

        # Validate stack index
        if not (0 <= stack_index < len(self.table)):
            return False, "Invalid stack index. Please select a valid stack."

        # Create a pile with selected cards from the player's hand
        selected_pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

        # Check if the ranks are sequential
        if not self.are_ranks_sequential(selected_pile):
            return False, "Invalid combination of cards. Please select a valid set of sequential cards."

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
    def are_ranks_sequential(self, pile):
        sorted_ranks = sorted(card['Value'] for card in pile)

        # Check if the ranks are sequential
        return all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, len(sorted_ranks)))


    def add_cards_to_stack(self, selected_cards_indices, stack_index):
        # Validate the combination
        first_card_rank = self.table[stack_index][0]['Value']
        max_player_card_rank = max(self.current_player.deck[idx]['Value'] for idx in selected_cards_indices)
        position = "front" if first_card_rank > max_player_card_rank else "end"

        success, message = self.validate_combination(selected_cards_indices, stack_index, position)

        # If the combination is valid and the respective player has put a new stack, proceed with adding cards to the stack
        if success:
            if self.current_player == self.player1 and self.has_put_stack_player1:
                # Create a pile with selected cards from the player's hand
                pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

                # Sort the pile in ascending order based on card values
                sorted_pile = sorted(pile, key=lambda x: x['Value'])

                # Add the cards to the specified position in the stack
                if position == "front":
                    self.table[stack_index] = sorted_pile + self.table[stack_index]
                elif position == "end":
                    self.table[stack_index] += sorted_pile

                # Remove the selected cards from the player's hand
                for idx in sorted(selected_cards_indices, reverse=True):
                    del self.current_player.deck[idx]

                # Switch to the next player's turn
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1

                return True, "Cards successfully added to the stack."

            elif self.current_player == self.player2 and self.has_put_stack_player2:
                # Create a pile with selected cards from the player's hand
                pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

                # Sort the pile in ascending order based on card values
                sorted_pile = sorted(pile, key=lambda x: x['Value'])

                # Add the cards to the specified position in the stack
                if position == "front":
                    self.table[stack_index] = sorted_pile + self.table[stack_index]
                elif position == "end":
                    self.table[stack_index] += sorted_pile

                # Remove the selected cards from the player's hand
                for idx in sorted(selected_cards_indices, reverse=True):
                    del self.current_player.deck[idx]

                # Switch to the next player's turn
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1

                return True, "Cards successfully added to the stack."

        # If the combination is not valid or the respective player hasn't put a new stack, return an error message
        return False, "Invalid combination of cards. Please select a valid set of cards or put a new stack first."
    
    def put_cards_on_table(self, selected_cards_indices):
            # Validate selected indices
            if not all(0 <= idx < len(self.current_player.deck) for idx in selected_cards_indices):
                return False, "Invalid card indices. Please select cards from your hand."

            # Create a pile with selected cards
            pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

            # Check if the pile is valid using is_valid function
            if not self.is_valid(pile):
                return False, "Invalid combination of cards. Please select a valid set of cards."

            # Sort the pile in ascending order based on card values
            sorted_pile = sorted(pile, key=lambda x: x['Value'])

            # Append the valid pile as a separate list to the table
            self.table.append(sorted_pile)

            # Set the respective player's has_put_stack to True
            if self.current_player == self.player1:
                self.has_put_stack_player1 = True
            elif self.current_player == self.player2:
                self.has_put_stack_player2 = True

            # Remove the selected cards from the player's hand
            for idx in sorted(selected_cards_indices, reverse=True):
                del self.current_player.deck[idx]

            # Switch to the next player's turn
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

            return True, "Cards successfully put on the table."
        

    def display_deck(self, deck):
         for card in deck:
             print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

    