import random


# Class to handle Cards (Suit and Value)
class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.faces = ["jack", "queen", "king", "ace"]

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
        # shuffle cards by swapping two random cards
        for i in range(1000):
            a = random.randint(0, 51)
            b = random.randint(0, 51)
            self.cards[a], self.cards[b] = self.cards[b], self.cards[a]


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

    def connectivity(self, cards):
        output = []
        temp = []
        for each in range(len(cards)):
            # print("")
            for index in range(len(cards) - each):
                card = cards[each + index]
                temp.append(card)
                if each + index + 1 < len(cards):
                    next_card = cards[each + index + 1]
                    # check connectivity
                    if card.val + 1 == next_card.val:
                        # print(" ->", end="")
                        print("", end="")
                    else:
                        if len(temp) > 4:
                            copy = temp.copy()
                            output.append(copy)
                        temp.clear()
                        break
        return output
        # print("")

    def duplicates(self, cards):
        output = []
        temp = []
        for each in range(len(cards)):
            # print("")
            for index in range(len(cards) - each):
                card = cards[each + index]
                temp.append(card)
                # card.print_card()
                if each + index + 1 < len(cards):
                    next_card = cards[each + index + 1]
                    # check connectivity
                    if card.val == next_card.val:
                        # print("*", end=str(len(temp)))
                        print("", end="")
                    else:
                        # print("", end=str(len(temp)))
                        if len(temp) > 1:
                            output.append(temp.copy())
                        temp = []
                        break
        # print("")
        # print("output",len(output))
        return output

    def suitedness(self, cards):
        output = []
        hearts = []
        diamonds = []
        clubs = []
        spade = []

        suit_list = [hearts, diamonds, clubs, spade]

        for card in cards:
            val = card.suit
            suit_list[val].append(card)

        for suit in suit_list:
            length = len(suit)
            if len(suit) >= 5:
                for i in range(6 - length):
                    output.append(suit[i:i + 5].copy())
            for card in suit:
                card.print_card()
                print(" *", end="")
            if len(suit) > 0:
                print("")

        return output;

    def score_hand(self, flop):
        # using current cards of flop determine a 'score' to weight the strength of the hand
        all_cards = self.hand + flop
        all_cards.sort(key=lambda card: card.val)
        flushes = self.suitedness(all_cards)
        straights = self.connectivity(all_cards)
        duplicates = self.duplicates(all_cards)

        print("straight flush:")
        for straight_hands in straights:
            print("hand: ")
            for flush_hands in flushes:
                if flush_hands == straight_hands:
                    for cards in flush_hands:
                        cards.print_card()
            print("")

        print("full house:")

        print("flushes:")
        for hands in flushes:
            print("hand: ")
            for cards in hands:
                cards.print_card()
            print("")

        print("straights:")
        for hands in straights:
            print("hand: ")
            for cards in hands:
                cards.print_card()
            print("")

        print("duplicates")
        for hands in duplicates:
            print("hand: ")
            for cards in hands:
                cards.print_card()
            print("")
        print("")


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
