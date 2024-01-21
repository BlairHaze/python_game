import random
from player import Player

class Game:

    def __init__(self):
        self.player1 = None
        self.player2 = None
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

        if len(pile) < 3:
            return False
        
        self.are_they_the_same_suit = False
        self.are_they_all_different_suits = False

        # Checking if the suits are unique
        self.unique_suits = {card['Suit'] for card in pile}
        if len(self.unique_suits) == len(pile):
            self.are_they_all_different_suits = True

        
        # Check if all cards in the pile have the same suit
        first_card_suit = pile[0]['Suit']

        for card in pile[1:]:
            if card['Suit'] != first_card_suit:
                self.are_they_the_same_suit = False

        # Check if the cards are in a valid sequence of same suits and sequential values
        if self.are_they_the_same_suit == True:
            ranks = [card['Value'] for card in pile]
            sorted_ranks = sorted(ranks)
            if sorted_ranks != ranks:
                return False
        
        # Check if the pile contains a valid combination of different suits and same values
        if self.are_they_all_different_suits == True:
            first_card_value = pile[0]['Value']
            for card in pile[1:]:
                if card['Value'] != first_card_value:
                    return False
                
        return True
    
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
    
    def put_cards_on_table(self):

        print("Player 1's Current Hand:")
        self.display_deck(self.player1.deck)

        # Get input from the player for the cards to put on the table
        selected_cards_indices = input("Enter the indices of cards to put on the table (comma-separated): ").split(',')
        selected_cards_indices = [int(idx.strip()) for idx in selected_cards_indices]

        # Validate selected indices
        if not all(0 <= idx < len(self.player1.deck) for idx in selected_cards_indices):
            print("Invalid card indices. Please select cards from your hand.")
            return

        # Create a pile with selected cards
        pile = [self.player1.deck[idx] for idx in selected_cards_indices]

        # Check if the pile is valid using is_valid function
        if not self.is_valid(pile):
            print("Invalid combination of cards. Please select a valid set of cards.")
            return

        # Update the table with the valid pile
        self.table.extend(pile)

        # Remove the selected cards from the player's hand
        for idx in sorted(selected_cards_indices, reverse=True):
            del self.player1.deck[idx]

        print("Cards successfully put on the table.")
            

    def display_deck(self, deck):
        for card in deck:
            print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

# Example usage
game_instance = Game()



game_instance.draw_cards()
print("Player 1's Deck after drawing cards:")
game_instance.display_deck(game_instance.player1.deck)

print("General deck:")
game_instance.display_deck(game_instance.general_deck)


game_instance.draw_cards()
print("Player 1's Deck after drawing cards:")
game_instance.display_deck(game_instance.player1.deck)

game_instance.put_cards_on_table()
print("Table after putting cards:")
game_instance.display_deck(game_instance.table)

print("Player 1's Deck after putting cards on the table:")
game_instance.display_deck(game_instance.player1.deck)

print("General deck:")
game_instance.display_deck(game_instance.general_deck)


# # Put cards on the table
# game_instance.put_cards_on_table()

# # Display the current table
# print("Table:")
# for pile in game_instance.table:
#     print(pile)


# game_instance.put_cards_on_table()

# print("Table:")
# for pile in game_instance.table:
#     print(pile)
