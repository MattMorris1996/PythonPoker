import random

# Class to handle Cards (Suit and Value)
class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.faces = ["jack", "queen", "king", "ace"]

    # two cards are the same if the value and the suit are the same
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def print_card(self):
        print(" ", end="")
        if self.val < 9:
            print(self.val + 2, self.suits[self.suit], end="")
        else:
            print(self.faces[self.val - 9], self.suits[self.suit], end="")


# Class to handle deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.faces = ["jack", "queen", "king", "ace"]

        # Generate cards 13 cards in each of the 4 suits
        for i in range(4):
            for j in range(13):
                self.cards.append(Card(i, j))

    def print_all(self):
        for i, card in enumerate(self.cards):
            # printing number cards
            if card.val < 9:
                print(card.val + 2, self.suits[card.suit])
            # face card print "Jack" etc
            else:
                print(self.faces[card.val - 9], self.suits[card.suit])

    def shuffle(self):
        #shuffle cards by swapping two random cards
        for i in range(1000):
            a = random.randint(0, 51)
            b = random.randint(0, 51)
            self.cards[a], self.cards[b] = self.cards[b], self.cards[a]