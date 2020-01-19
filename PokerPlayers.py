from PokerScoring import *
from CardDeck import *
# Class to handle player


class Player:
    def __init__(self, chips, player_n):
        # each player has id
        self.number = player_n
        # number of chips
        self.chips = chips
        # and a hand, list of cards
        self.hand = []
        # add a score for a hand
        self.players_score = PokerScore()

    def deal(self, card):
        # when player is dealt a card append to hand
        self.hand.append(card)

    def end(self):
        # return hand to deck
        return [self.hand.pop(), self.hand.pop()]

    def score(self, flop):
        self.players_score.score(flop, self.hand)

    def get_strongest(self):
        self.players_score.find_strongest()

    def show_down(self):
        print("Hand: ", end="")
        for card in self.hand:
            card.print_card()
        print("")
        print("Best Hand: ")
        self.players_score.print_strongest()
        print("")



