import random

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.faces = ["jack", "queen", "king", "ace"]

    def print_card(self):
        if self.val < 9:
            print(self.val + 2, self.suits[self.suit])
        else:
            print(self.faces[self.val - 9], self.suits[self.suit])


class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.faces = ["jack", "queen", "king", "ace"]

        for i in range(4):
            for j in range(13):
                self.cards.append(Card(i, j))

    def print_all(self):
        for i, card in enumerate(self.cards):
            if card.val < 9:
                print(card.val + 2, self.suits[card.suit])
            else:
                print(self.faces[card.val - 9], self.suits[card.suit])

    def shuffle(self):
        for i in range(1000):
            a = random.randint(0, 51)
            b = random.randint(0, 51)

            self.cards[a], self.cards[b] = self.cards[b], self.cards[a]

class Player:
    def __init__(self, chips, player_n):
        self.number = player_n
        self.chips = chips
        self.hand = []

    def deal(self, card):
        self.hand.append(card)

    def end(self):
        return [self.hand.pop(), self.hand.pop()]


    def score_hand(self, flop):
        all_cards = self.hand + flop
        all_cards.sort(key=lambda x: x.val)
        score = 0
        if (all_cards[0].val + 1) == all_cards[1].val:
            all_cards[0].print_card()
        for i in range(1,len(all_cards)-1):
                if (all_cards[i].val + 1) == all_cards[i+1].val:
                    all_cards[i].print_card()
                elif (all_cards[i].val - 1) == all_cards[i-1].val:
                    all_cards[i].print_card()
        if (all_cards[len(all_cards)-1].val - 1) == all_cards[len(all_cards)-1 - 1].val:
            all_cards[len(all_cards)-1].print_card()

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

    def score_hands(self):
        i = 0
        for player in self.players:
            print("player ", i)
            player.score_hand(self.flop)
            i = i + 1


game = Poker(2, 1000)
game.deal()
game.print_hands()
game.print_flop()
game.score_hands()
