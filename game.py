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
    
    def draw_cards(self):
        pass
    
    def put_cards_on_table(self):
        input_pile = input("Write the names of the cards you want to put on the table (comma separated), example: queen of hearts, 2 of diamonds, 7 of spades\n")
        # Convert string representation of cards to list of dictionaries
        self.pile = [{'Suit': card.split(' of ')[1], 'Rank': card.split(' of ')[0]} for card in input_pile.split(',')]
        
        self.valid = self.is_valid(self.pile)

        if self.valid:
            self.table.append(self.pile)
        else:
            print("The combination is invalid")
            

    def display_deck(self, deck):
        for card in deck:
            print(f"{card['Rank']} of {card['Suit']} (Value: {card['Value']})")

# Example usage
game_instance = Game()

# Create and display the deck
deck = game_instance.create_deck()
print("Created Deck:")
game_instance.display_deck(deck)

# Put cards on the table
game_instance.put_cards_on_table()

# Display the current table
print("Table:")
for pile in game_instance.table:
    print(pile)


game_instance.put_cards_on_table()

print("Table:")
for pile in game_instance.table:
    print(pile)
