from PokerScoring import *
from CardDeck import *

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

        self.folded = False

        self.current_bet = 0

    def console_ui(self, flop=[], pot_size=0, call_amount=0, check=False):
        print("|---------------------------------------------|")
        print("Flop: ")
        print("     ", end="")
        for card in flop:
            card.print_card()

        print("\n\nPot Size: " + str(pot_size))
        print("Chips: " + str(self.chips))
        print("Current Bet: " + str(self.current_bet))
        print("Call Amount: " + str(call_amount))

        print("\nYour Cards: ")
        print("     ", end="")
        for card in self.hand:
            card.print_card()
        print("\n\nOptions:")
        options = set()
        print("     Fold: 1")
        options.add(1)
        print("     Raise: 2")
        options.add(2)

        if self.current_bet != call_amount:
            print("     Call: 3")
            options.add(3)

        if check:
            print("     Check: 4")
            options.add(4)

        selection = int(input("\nEnter: "))
        while selection not in options:
            print("Option not available!")
            selection = int(input("\nEnter: "))

        if selection == 1:
            return ('fold',0)
        if selection == 3:
            delta = call_amount - self.current_bet
            return ('call',delta)
        if selection == 2:
            delta = call_amount - self.current_bet
            x = input("Enter raise amount: ")
            return ('raise', int(x) + delta, self.current_bet + int(x) + delta)
        if selection == 4:
            return ('check',0)



    def turn(self, call_amount=0, check=False, flop=None, blind=0, pot_size=0): #Based on state of poker round, return desired turn
            return self.console_ui(flop=flop, pot_size=pot_size,call_amount=call_amount, check=check)

    def bet(self, amount):
        if self.chips - amount < 0:
            amount = self.chips
            self.chips = 0
        self.chips -= amount
        self.current_bet += amount
        return self.current_bet

    def deal(self, card): #Recieve two cards from the deck
        # when player is dealt a card append to hand
        self.hand.append(card)

    def fold(self):
        self.folded = True
        return self.end()

    def end(self): #Return cards to the deck
        # return hand to deck
        return [self.hand.pop(), self.hand.pop()]

    def score(self, flop):
        self.players_score.score(flop, self.hand)

    def get_strongest(self): #Find strongest hand
        self.players_score.find_strongest()

    def show_down(self): #Display Cards and strongest Hands
        print("Hand: ", end="")
        for card in self.hand:
            card.print_card()
            print(",", end="")
        print("")
        print("Best Hand: ", end="")
        self.players_score.print_strongest()
        print("")

if __name__ == '__main__':
    player = Player(100, 1)
    bet = player.turn(10, True)
