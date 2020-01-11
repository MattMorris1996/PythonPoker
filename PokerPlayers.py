# Class to handle player

class Player:
    def __init__(self, chips, player_n):
        # each player has id
        self.number = player_n
        # number of chips
        self.chips = chips
        # and a hand, list of cards
        self.hand = []

    def deal(self, card):
        # when player is dealt a card append to hand
        self.hand.append(card)

    def end(self):
        # return hand to deck
        return [self.hand.pop(), self.hand.pop()]

