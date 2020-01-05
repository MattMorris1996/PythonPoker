from PokerPlayers import *
from CardDeck import *

# Main class interacts with the Deck the flop and the players
class Poker:
    def __init__(self, n_players, buy_in):
        self.players = []
        self.deck = Deck()
        self.flop = []
        for i in range(n_players):
            self.players.append(Player(buy_in, i))

    def deal(self):
        self.deck.shuffle()
        for j in range(2):
            for i in self.players:
                i.deal(self.deck.cards.pop())

        for x in range(5):
            self.flop.append(self.deck.cards.pop())

    def print_hands(self):
        for i in self.players:
            print("player", i.number + 1, end="")
            print(" chips", i.chips)
            for j in i.hand:
                j.print_card()
            print()

    def print_flop(self):
        print("The Flop")
        for i in self.flop:
            i.print_card()
            print(",", end="")
        print("")

    def score_hands(self):
        i = 0
        for player in self.players:
            print("player ", i)
            player.score_hand(self.flop)
            i = i + 1


PLAYERS = 10
BUY_IN = 1000

game = Poker(PLAYERS, BUY_IN)
game.deal()
game.print_hands()
game.print_flop()
game.score_hands()
