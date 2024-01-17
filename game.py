import random
from player import Player

class Game:

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.general_deck = None

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        general_deck = []

        for i in range(2):
            for suit in suits:
                for rank in ranks:
                    card_name = f"{rank} of {suit} ({i + 1})"
                    general_deck.append({
                        'Suit': suit,
                        'Rank': rank,
                        'DeckNumber': i + 1
                    })

        return general_deck

    def create_player(self, name):
        return Player(name, 0)

    def draw_cards(self, player, num_cards=1):
        if not self.general_deck:
            self.general_deck = self.create_deck()
            num_cards = 7

        # Sprawdzamy, czy talia ogólna nie jest pusta
        if not self.general_deck:
            print("No cards left in the deck.")
            return

        # Losujemy karty i dodajemy do talii gracza
        drawn_cards = random.sample(self.general_deck, min(num_cards, len(self.general_deck)))
        player.add_to_hand(drawn_cards)

        # Usuwamy wylosowane karty z talii ogólnej
        self.general_deck = [card for card in self.general_deck if card not in drawn_cards]

        print("Remaining cards in general deck:")
        for card in self.general_deck:
            print(f"{card['Rank']} of {card['Suit']}")
        print("\n")

    # def select_cards(self):
        

    # def is_valid_combination(self):

    # def edit_set_on_table(self):

    

# Przykładowe użycie
game_instance = Game()
player_instance = game_instance.create_player("Player1")

# Rysowanie pięciu kart dla gracza
game_instance.draw_cards(player_instance)

# Wyświetlenie talii gracza
print(f"{player_instance.name}'s hand: {player_instance.show_hand()}")