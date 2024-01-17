class Player:
    def __init__(self, name, card_num, deck=None):
        self.name = name
        self.card_num = card_num
        self.deck = deck if deck else {}

    def get_rid_of_card(self, num_of_cards_put_on_table):
        self.card_num -= num_of_cards_put_on_table

    def still_in_game(self):
        return self.card_num > 0

    def add_to_hand(self, cards):
        for card in cards:
            card_name = f"{card['Rank']} of {card['Suit']}"
            self.deck[card_name] = card

    def show_hand(self):
        return self.deck