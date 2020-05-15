from PokerPlayers import *
from CardDeck import *
from PokerScoring import *
from random import *

# Main class interacts with the Deck the flop and the players
class Poker:
    def __init__(self, n_players, buy_in):
        self.deck = Deck()
        self.players = []

        self.flop = []
        self.flop_visible = []

        self.player_out = []

        self.pot = 0

        for i in range(n_players):
            self.players.append(Player(buy_in, i))

        #assign dealer to random player
        self.big_blind = randint(0, n_players-1)
        self.big_blind_amount = 10

        print(self.big_blind)
        self.players[(self.big_blind+2)%n_players].set_blind("dealer")
        self.players[(self.big_blind+1)%n_players].set_blind("small blind")
        self.players[self.big_blind].set_blind("big blind")

    def deal(self):
        self.deck.shuffle()
        for j in range(2):
            for i in self.players:
                i.deal(self.deck.cards.pop())

        for x in range(5):
            self.flop.append(self.deck.cards.pop())

    def print_hands(self):
        for i in self.players:
            print("player", i.number + 1, end=" " + i.blind)
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
            i = i + 1
            print("")
            print("Player: ", i)
            player.score(self.flop)
            player.get_strongest()
            player.show_down()

    def round_bet(self):
        for player in self.players:
            if selection == "fold":
                self.deck.cards.append(player.end())
                self.players.pop()
            if selection == "raise":
                amount = input("raise amount:")
                self.bet_amount = amount
                player.chips -= (self.call_amount + amount)
                self.pot += self.call_amount+amount
            if selection == "call":

            if selection == "raise":

if __name__ == '__main__':
    PLAYERS = 7
    BUY_IN = 1000

    game = Poker(PLAYERS, BUY_IN)
    game.deal()
    game.print_hands()
    game.print_flop()
    game.score_hands()

