from PokerScoring import *
from CardDeck import *
# Class to handle player


class Player:
    def __init__(self, chips, player_n):
        # each player has id
        self.number = player_n
        # number of chips
        self.chips = chips
        # blinds
        self.blind = ""
        # and a hand, list of cards
        self.hand = []
        # add a score for a hand
        self.players_score = PokerScore()

    def turn(self, state):
        selection = ""
        if selection == "fold":
            return ["fold", self.hand]
        if selection == "raise":
            number = 0
            return ["raise", number]
        if selection == "call":
            return ["call", state.call_amount]
        if selection == "check":
            return ["check"]

    def set_blind(self, name):
        self.blind = name

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
            print(",",end="")
        print("")
        print("Best Hand: ", end="")
        self.players_score.print_strongest()
        print("")



