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
    
    def is_valid(self, pile):
        if len(pile) != 3:
            return False

        suits_set = set(card['Suit'] for card in pile)
        values_set = set(card['Value'] for card in pile)

        # Check for three cards with the same rank but different suits
        if len(suits_set) == 3 and len(values_set) == 1:
            return True

        # Check for three consecutive cards with the same suit
        if len(suits_set) == 1 and len(values_set) == 3:
            sorted_values = sorted(values_set)
            if sorted_values[2] - sorted_values[0] == 2:
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
    
    def put_cards_on_table(self, selected_cards_indices):
        # Validate selected indices
        if not all(0 <= idx < len(self.player1.deck) for idx in selected_cards_indices):
            return False, "Invalid card indices. Please select cards from your hand."

        # Create a pile with selected cards
        pile = [self.player1.deck[idx] for idx in selected_cards_indices]

        # Check if the pile is valid using is_valid function
        if not self.is_valid(pile):
            return False, "Invalid combination of cards. Please select a valid set of cards."

        # Append the valid pile as a separate list to the table
        self.table.append(pile)

        # Remove the selected cards from the player's hand
        for idx in sorted(selected_cards_indices, reverse=True):
            del self.player1.deck[idx]

        return True, "Cards successfully put on the table."          

#     def display_table_deck(self, deck):
#         for i, pile in enumerate(deck, start=1):
#             print(f"Pile {i}:")
#             for card in pile:
#                 print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

    def display_deck(self, deck):
         for card in deck:
             print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

    

# # Example usage
# game_instance = Game()



# game_instance.draw_cards()
# print("Player 1's Deck after drawing cards:")
# game_instance.display_deck(game_instance.player1.deck)

# print("General deck:")
# game_instance.display_deck(game_instance.general_deck)


# game_instance.draw_cards()
# print("Player 1's Deck after drawing cards:")
# game_instance.display_deck(game_instance.player1.deck)

# for i in range(10):


#     game_instance.put_cards_on_table()
#     print("Table after putting cards:")
#     game_instance.display_table_deck(game_instance.table)


# print("Player 1's Deck after putting cards on the table:")
# game_instance.display_deck(game_instance.player1.deck)

# print("General deck:")
# game_instance.display_deck(game_instance.general_deck)


# # # Put cards on the table
# # game_instance.put_cards_on_table()

# # # Display the current table
# # print("Table:")
# # for pile in game_instance.table:
# #     print(pile)


# # game_instance.put_cards_on_table()

# # print("Table:")
# # for pile in game_instance.table:
# #     print(pile)