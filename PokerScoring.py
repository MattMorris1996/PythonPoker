from CardDeck import *


class PokerScore:
    def __init__(self):
        self.flop = []
        self.hand = []
        self.straight_flushes = []
        self.fours = []
        self.full_houses = []
        self.flushes = []
        self.straights = []
        self.threes = []
        self.pairs = []
        self.twos = []
        self.all_cards = []
        self.strongest = []
        self.strongest_type = ""
        self.strongest_score = 0  # scoring function required future task quite complex

    def score(self, flop, hand):
        self.flop = flop
        self.hand = hand
        self.all_cards = hand + flop
        self.all_cards.sort(key=lambda card: card.val)

        all_duplicates = duplicates(self.all_cards)

        self.flushes = same_suit(self.all_cards)
        self.straights = connectivity(self.all_cards)

        self.straight_flushes = connected_flushes(self.flushes, self.straights)
        self.fours = four_kind(all_duplicates)
        self.threes = three_kind(all_duplicates)
        self.twos = pair(all_duplicates)

        self.full_houses = full_house(self.threes, self.twos)
        self.pairs = two_pair(self.twos)

    def find_strongest(self):
        # straight flushes
        if self.straight_flushes.__len__() > 0:
            self.strongest = self.straight_flushes[0]
            self.strongest_type = "Straight Flush"
        elif self.fours.__len__() > 0:
            self.strongest = self.fours[0]
            self.strongest_type = "Four Of A Kind"
        elif self.full_houses.__len__() > 0:
            self.strongest = self.full_houses[0]
            self.strongest_type = "Full House"
        elif self.flushes.__len__() > 0:
            self.strongest = self.flushes[0]
            self.strongest_type = "Flush"
        elif self.straights.__len__() > 0:
            self.strongest = self.straights[0]
            self.strongest_type = "Straight"
        elif self.threes.__len__() > 0:
            self.strongest = self.threes[0]
            self.strongest_type = "Three Of A Kind"
        elif self.pairs.__len__() > 0:
            self.strongest = self.pairs[0]
            self.strongest_type = "Two Pair"
        elif self.twos.__len__() > 0:
            self.strongest = self.twos[0]
            self.strongest_type = "Pair"
        else:
            self.strongest.append(self.all_cards[self.all_cards.__len__()-1])
            self.strongest_type = "High Card"

    def print_strongest(self):
        print(self.strongest_type)
        for card in self.strongest:
            card.print_card()


def connectivity(cards):
    output = []
    temp = []
    for i in range(len(cards)):
        first = 1
        for index in range(len(cards) - i):
            card = cards[i + index]
            if i + index < len(cards) - 1:
                next_card = cards[i + index + 1]
                # check connectivity
                if (card.val + 1) == next_card.val:
                    if first:
                        temp.append(card)
                        first = 0
                    temp.append(next_card)
                else:
                    break
                if len(temp) == 5:
                    output.append(temp.copy())
                    break
        temp = []
    return output


def duplicates(cards):
    output = []
    temp = []
    for i in range(len(cards)):
        first = 1
        for index in range(len(cards) - i):
            card = cards[i + index]
            if i + index + 1 < len(cards):
                next_card = cards[i + index + 1]
                # check connectivity
                if card.val == next_card.val:
                    if first:
                        temp.append(card)
                        first = 0
                    temp.append(next_card)
                else:
                    break
        if len(temp) > 1:
            output.append(temp.copy())
            temp = []
    return output


def same_suit(cards):
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
            for i in range(length - 4):
                output.append(suit[i:i + 5].copy())

    return output


def full_house(threes, twos):
    output = []
    temp = []

    for three in threes:
        for two in twos:
            # prevent a three and a pair of the same value combining to form a full house
            if three[0].val != two[0].val:
                temp = three + two
                output.append(temp.copy())
                temp = []
    return output


def two_pair(twos):
    output = []
    temp = []
    for two1 in twos:
        for two2 in twos:
            # prevent a two pairs of the same value combining to form a two pair
            if two1[0] != two2[0]:
                temp = two1 + two2
                output.append(temp.copy())
                temp = []
    return output


def four_kind(all_duplicates):
    output = []
    for hands in all_duplicates:
        if len(hands) == 4:
            output.append(hands)
    return output


def three_kind(all_duplicates):
    output = []
    for hands in all_duplicates:
        if len(hands) == 3:
            output.append(hands)
    return output


def pair(all_duplicates):
    output = []
    for hands in all_duplicates:
        if len(hands) == 2:
            output.append(hands)
    return output


def connected_flushes(flushes, straights):
    output = []

    for flush in flushes:
        for straight in straights:
            if straight == flush:
                output.append(straight)

    return output
