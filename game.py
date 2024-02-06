from player import Player
import random
import itertools

class Player2(Player):
    def __init__(self, name, score):
        super().__init__(name, score)
        self.deck = []
class Game:
    def __init__(self, player1_name=None, player2_name=None):
        self.player1 = self.create_player(player1_name) if player1_name else None
        self.player2 = self.create_player(player2_name) if player2_name else None
        self.both_players_drew_cards = False 
        self.has_put_stack_player1 = False 
        self.has_put_stack_player2 = False  
        self.which_stack = None
        self.general_deck = None
        self.table = []
        self.current_player = self.player1

    def create_player(self, name, player_class=Player):
        return player_class(name, 0)

    def get_game_mode(self):
        if self.player2 and self.player2.name == 'Computer':
            return 'singleplayer'
        elif self.player2.name:
            return 'hotseat'

    def is_general_deck_empty(self):
        if self.general_deck:
            return False
        else:
            return True

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
    
    def start_singleplayer(self, player_name):
        self.player1 = self.create_player(player_name)
        self.player2 = self.create_player("Computer", player_class=Player2)

    def find_valid_combinations(self, player_deck):
        valid_combinations = []

        for stack_index, stack in enumerate(self.table):
            for i in range(len(player_deck)):
                for j in range(i + 2, len(player_deck) + 1):
                    selected_cards_indices = list(range(i, j))
                    temp_deck = stack + [player_deck[idx] for idx in selected_cards_indices]

                    if self.is_valid(temp_deck, allow_single=True):
                        valid_combinations.append({
                            'indices': selected_cards_indices,
                            'stack_index': stack_index
                        })

        return valid_combinations


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

        if len(suits_set) == num_cards and len(values_set) == 1:
            return True

        if len(suits_set) == 1 and len(values_set) == num_cards:
            sorted_values = sorted(values_set)
            if all(value in sorted_values for value in range(sorted_values[0], sorted_values[-1] + 1)):
                return True

        return False
    
    def shuffle_deck(self):
        random.shuffle(self.general_deck)
    
    def draw_cards(self):
        if not self.current_player:
            return 

        if not self.current_player.deck:
            if not self.general_deck:
                self.create_deck()
            self.shuffle_deck()

            self.current_player.deck = self.general_deck[:6]
            self.general_deck = self.general_deck[6:]
        else:
            self.current_player.deck.append(self.general_deck.pop())

        if all(player.deck for player in [self.player1, self.player2]):
            self.both_players_drew_cards = True

        self.switch_to_next_player()

        if self.current_player.name == "Computer":
            self.draw_cards_for_computer()

    def draw_cards_for_computer(self):
        if self.is_game_over():
            self.draw_cards()
        if not self.current_player.deck:
            self.current_player.deck = self.general_deck[:6]
            self.general_deck = self.general_deck[6:]
        else:
            find_table_stack = self.find_table_stack()
            first_valid_combination = self.find_first_valid_combination()
            if find_table_stack:
                selected_indices = find_table_stack
                success, message = self.add_cards_to_stack(selected_indices, self.which_stack)
                if success:
                    return
            if first_valid_combination:
                selected_indices = [self.current_player.deck.index(card) for card in first_valid_combination]
                success, message = self.put_cards_on_table(selected_indices)
                if success:
                    return
            self.current_player.deck.append(self.general_deck.pop())

        if all(player.deck for player in [self.player1, self.player2]):
            self.both_players_drew_cards = True

        if all(player.deck for player in [self.player1, self.player2]):
            self.both_players_drew_cards = True

        self.switch_to_next_player()

    def switch_to_next_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def validate_combination(self, selected_cards_indices, stack_index, position):
        if not all(0 <= idx < len(self.current_player.deck) for idx in selected_cards_indices):
            return False, "Invalid card indices. Please select cards from your hand."

        if not (0 <= stack_index < len(self.table)):
            return False, "Invalid stack index. Please select a valid stack."

        selected_pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

        if not self.are_ranks_sequential(selected_pile):
            return False, "Invalid combination of cards. Please select a valid set of sequential cards."

        temp_deck = self.table[stack_index].copy()

        if position == "front":
            temp_deck = selected_pile + temp_deck
        elif position == "end":
            temp_deck += selected_pile
        else:
            return False, "Invalid position. Please choose 'front' or 'end'."

        if not self.is_valid(temp_deck, allow_single=True):
            return False, "Invalid combination of cards. Please select a valid set of cards."

        return True, "Combination is valid."

    def are_ranks_sequential(self, pile):
        sorted_ranks = sorted(card['Value'] for card in pile)

        return all(sorted_ranks[i] == sorted_ranks[i - 1] + 1 for i in range(1, len(sorted_ranks)))


    def add_cards_to_stack(self, selected_cards_indices, stack_index):
        if not (0 <= stack_index < len(self.table)):
            return False, f"Invalid stack index. Please provide a stack index between 0 and {len(self.table) - 1}."

        first_card_rank = self.table[stack_index][0]['Value']
        if not selected_cards_indices:
            return False, "No cards selected. Please select cards to add to the stack."
        max_player_card_rank = max(self.current_player.deck[idx]['Value'] for idx in selected_cards_indices)
        position = "front" if first_card_rank > max_player_card_rank else "end"

        success, message = self.validate_combination(selected_cards_indices, stack_index, position)

        # If the combination is valid and the respective player has put a new stack, proceed with adding cards to the stack
        if success:
            if self.current_player == self.player1 and self.has_put_stack_player1:

                pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

                sorted_pile = sorted(pile, key=lambda x: x['Value'])

                if position == "front":
                    self.table[stack_index] = sorted_pile + self.table[stack_index]
                elif position == "end":
                    self.table[stack_index] += sorted_pile

                for idx in sorted(selected_cards_indices, reverse=True):
                    del self.current_player.deck[idx]

                self.current_player = self.player2 if self.current_player == self.player1 else self.player1

                if self.current_player == self.player2 and self.player2.name == "Computer":
                    self.draw_cards_for_computer()

                return True, "Cards successfully added to the stack."

            elif self.current_player == self.player2 and self.has_put_stack_player2:

                pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

                sorted_pile = sorted(pile, key=lambda x: x['Value'])

                if position == "front":
                    self.table[stack_index] = sorted_pile + self.table[stack_index]
                elif position == "end":
                    self.table[stack_index] += sorted_pile

                for idx in sorted(selected_cards_indices, reverse=True):
                    del self.current_player.deck[idx]

                self.current_player = self.player2 if self.current_player == self.player1 else self.player1

                return True, "Cards successfully added to the stack."

        return False, "Invalid combination of cards. Please select a valid set of cards or put a new stack first."
    
    def put_cards_on_table(self, selected_cards_indices):
            if not all(0 <= idx < len(self.current_player.deck) for idx in selected_cards_indices):
                return False, "Invalid card indices. Please select cards from your hand."

            pile = [self.current_player.deck[idx] for idx in selected_cards_indices]

            if not self.is_valid(pile):
                return False, "Invalid combination of cards. Please select a valid set of cards."

            sorted_pile = sorted(pile, key=lambda x: x['Value'])

            self.table.append(sorted_pile)

            if self.current_player == self.player1:
                self.has_put_stack_player1 = True
            elif self.current_player == self.player2:
                self.has_put_stack_player2 = True

            for idx in sorted(selected_cards_indices, reverse=True):
                del self.current_player.deck[idx]

            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

            if self.current_player == self.player2 and self.player2.name == "Computer":
                self.draw_cards_for_computer()

            return True, "Cards successfully put on the table."
        

    def display_deck(self, deck):
         for card in deck:
             print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

    def find_first_valid_combination(self):
        if self.current_player == self.player1 and self.player2.name != "Computer":
            return None

        for r in range(3, len(self.current_player.deck) + 1):
            for indices in itertools.combinations(range(len(self.current_player.deck)), r):

                pile = [self.current_player.deck[idx] for idx in indices]

                if self.is_valid(pile, allow_single=True):
                    sorted_pile = sorted(pile, key=lambda x: x['Value'])
                    return sorted_pile  

        return None  
    
    def find_table_stack(self):

        if self.current_player == self.player1 and self.player2.name != "Computer":
            return None

        for table_stack in self.table:
            for card_index, card in enumerate(self.current_player.deck):
                temp_stack = table_stack + [card]

                sorted_stack = sorted(temp_stack, key=lambda x: x['Value'])
                
                self.which_stack = self.table.index(table_stack)

                if self.is_valid(sorted_stack):
                    valid_indices = [card_index]  

                    for additional_card_index, additional_card in enumerate(self.current_player.deck):
                        extended_stack = sorted_stack + [additional_card]
                        extended_stack = sorted(extended_stack, key=lambda x: x['Value'])

                        if self.is_valid(extended_stack):
                            valid_indices.append(additional_card_index) 

                    return valid_indices  

        return None  


    

    










  

    