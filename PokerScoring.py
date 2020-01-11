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


def score_hand(flop, hand):
    # using current cards of flop determine a 'score' to weight the strength of the hand
    all_cards = hand + flop
    all_cards.sort(key=lambda card: card.val)

    all_duplicates = duplicates(all_cards)

    print(len(all_duplicates))

    for hand in all_duplicates:
        for card in hand:
            card.print_card()
        print("")
