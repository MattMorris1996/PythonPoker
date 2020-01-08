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
        next_card_val = 0
        card_val = 0
        window = iter(range(len(cards)))
        for i in window:
            first = 1
            for index in range(len(cards) - i):
                card = cards[i + index]
                card_val = card.val + 1
                if i + index < len(cards) - 1:
                    next_card = cards[i + index + 1]
                    next_card_val = next_card.val
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

        print("len of output", len(output));
        return output

    def duplicates(self, cards):
        output = []
        temp = []
        window = iter(range(len(cards)))
        for i in window:
            for index in range(len(cards) - i):
                card = cards[i + index]
                if i + index + 1 < len(cards):
                    next_card = cards[i + index + 1]
                    # check connectivity
                    temp.append(card)
                    if card.val == next_card.val:

                        print("", end="")
                    else:
                        if len(temp) > 1:
                            output.append(temp.copy())
                        temp = []
                        break
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
                for i in range(length - 5):
                    output.append(suit[i:i + 5].copy())

        return output

    def full_house(self, duplicates):
        threes = []
        doubles = []
        output = []
        temp = []
        for hands in duplicates:
            if len(hands) == 3:
                threes.append(hands)
            if len(hands) == 2:
                threes.append(doubles)

        for tris in threes:
            for duos in doubles:
                temp = tris + duos
                output.append(temp.copy())
                temp = []

        print("length of output", len(output))
        return output



    def score_hand(self, flop):
        # using current cards of flop determine a 'score' to weight the strength of the hand
        all_cards = self.hand + flop
        all_cards.sort(key=lambda card: card.val)
        flushes = self.suitedness(all_cards)
        straights = self.connectivity(all_cards)
        duplicates = self.duplicates(all_cards)
        full_houses = self.full_house(duplicates)

        print("straight flush:")
        for straight_hands in straights:
            print("hand: ")
            for flush_hands in flushes:
                if flush_hands == straight_hands:
                    for cards in flush_hands:
                        cards.print_card()
            print("")

        print("full houses:")
        for hands in full_houses:
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

        print("duplicates:")
        for hands in duplicates:
            print("hand: ")
            for cards in hands:
                cards.print_card()
            print("")
        print("")
