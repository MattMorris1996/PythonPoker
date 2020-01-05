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
