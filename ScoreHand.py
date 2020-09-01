# generates all poker hands assigning score to each
from CardDeck import Deck
import itertools

from PokerScoring import PokerScore

myDeck = Deck()

new_list = list(map(lambda card: (card.val, card.suit), myDeck.cards))

straights = []
straight_flushes = []
flushes = []
four_kind = []
full_houses = []
three_kind = []
two_pairs = []
pairs = []
high_card = []


def connected(hand):
    vals = sorted(list(map(lambda x: x[0], hand)))
    if vals[4] == 12 and vals[0] == 0:
        check = list(range(vals[0], vals[0] + 4, 1))
        return vals[:-1] == check
    else:
        check = list(range(vals[0], vals[0] + 5, 1))
        return vals == check


def same_suit(hand):
    return len(set(map(lambda x: x[1], hand))) <= 1


def fours(hand):
    vals = list(map(lambda x: x[0], hand))
    for val in vals:
        if vals.count(val) == 4:
            return True
    return False


def full_house(hand):
    vals = list(map(lambda x: x[0], hand))
    three_flag = False
    two_flag = False
    for val in vals:
        if vals.count(val) == 3:
            three_flag = True
        if vals.count(val) == 2:
            two_flag = True
        if two_flag and three_flag:
            return True
    return False


def threes(hand):
    vals = list(map(lambda x: x[0], hand))
    for val in vals:
        if vals.count(val) == 3:
            return True
    return False


def two_twos(hand):
    vals = list(map(lambda x: x[0], hand))
    checked = set()
    c = 0
    for val in vals:
        if vals.count(val) == 2 and val not in checked:
            checked.add(val)
            c += 1
        if c == 2:
            return True
    return False


def twos(hand):
    vals = list(map(lambda x: x[0], hand))
    for val in vals:
        if vals.count(val) == 2:
            return True
    return False


def get_all():
    count = 0
    for hand in itertools.combinations(new_list, 5):
        count += 1
        if same_suit(hand) and connected(hand):
            straight_flushes.append(hand)

        elif fours(hand):
            four_kind.append(hand)

        elif full_house(hand):
            full_houses.append(hand)

        elif same_suit(hand):
            flushes.append(hand)

        elif connected(hand):
            straights.append(hand)

        elif threes(hand):
            three_kind.append(hand)

        elif two_twos(hand):
            two_pairs.append(hand)

        elif twos(hand):
            pairs.append(hand)

        else:
            high_card.append(hand)

    print("total hands: " + str(count))

    print("number of straight flushes: " + str(len(straight_flushes)))

    print("number of four of a kinds: " + str(len(four_kind)))

    print("number of full houses: " + str(len(full_houses)))

    print("number of flushes: " + str(len(flushes)))

    print("number of straights: " + str(len(straights)))

    print("number of three kinds: " + str(len(three_kind)))

    print("number of two pairs: " + str(len(two_pairs)))

    print("number of pairs: " + str(len(pairs)))

    print("number of high cards: " + str(len(high_card)))

    print(list(map(lambda x: x[0][0], straight_flushes)))


def score_straight(hand):
    not_ace_first = 1
    hand_list = sorted(list(map(lambda x: x[0], hand)))
    if hand_list[4] == 12 and hand_list[0] == 0:
        not_ace_first = 0
    return min(hand_list) + not_ace_first


def score_four_a_kind(hand):
    vals = list(map(lambda x: x[0], hand))
    checked = set()
    score = 0
    for val in vals:
        if vals.count(val) == 4 and val not in checked:
            score += val * 13
            checked.add(val)
        elif val not in checked:
            score += val
            checked.add(val)
    return score


def score_full_house(hand):
    vals = list(map(lambda x: x[0], hand))
    checked = set()
    score = 0
    for val in vals:
        if vals.count(val) == 3 and val not in checked:
            score += val * 13
            checked.add(val)
        elif val not in checked:
            score += val
            checked.add(val)
    return score


def score_flush(hand):
    hand_list = sorted(list(map(lambda x: x[0], hand)), reverse=True)
    score = 0
    base = 5
    for hand_val in hand_list:
        score += hand_val * 13 * base
        base -= 1
    return score


def score_three_kinds(hand):
    vals = sorted(list(map(lambda x: x[0], hand)), reverse=True)
    checked = set()
    score = 0
    base = 2
    for val in vals:
        if vals.count(val) == 3 and val not in checked:
            checked.add(val)
            score += val * 13 * 3
        elif val not in checked:
            score += val * 13 * base
            base -= 1
    return score


def score_two_pairs(hand):
    vals = sorted(list(map(lambda x: x[0], hand)), reverse=True)
    checked = set()
    score = 0
    base1 = 4
    base2 = 2
    for val in vals:
        if vals.count(val) == 2 and val not in checked:
            checked.add(val)
            score += val * 13 * base1
            base1 -= 1
        if val not in checked:
            score += val * 13 * base2
            base2 -= 1
    return score


def score_pairs(hand):
    vals = sorted(list(map(lambda x: x[0], hand)), reverse=True)
    checked = set()
    score = 0
    base = 3
    for val in vals:
        if vals.count(val) == 2 and val not in checked:
            checked.add(val)
            score += val * 13 * 4
        if val not in checked:
            score += val * 13 * base
            base -= 1
    return score


def score_high_card(hand):
    vals = sorted(list(map(lambda x: x[0], hand)), reverse=True)
    score = 0
    base = 5
    for val in vals:
        score += val * 13 * base
        base -= 1
    return score


def score_hand(hand):
    if same_suit(hand) and connected(hand):
        return "straight-flush", 7462 - 10 + score_straight(hand)

    elif fours(hand):
        return "four of a kind", 7462 - 10 - 156 + score_four_a_kind(hand)

    elif full_house(hand):
        return "full house", 7462 - 156 - 156 + score_full_house(hand)

    elif same_suit(hand):
        return "flush", 7462 - 156 - 156 - 1277 + score_flush(hand)

    elif connected(hand):
        return "straight", 7462 - 156 - 156 - 1277 - 10 + score_straight(hand)

    elif threes(hand):
        return "three of a kind", 7462 - 156 - 156 - 1277 - 10 - 858 + score_three_kinds(hand)

    elif two_twos(hand):
        return "two pair", 7462 - 156 - 156 - 1277 - 10 - 858 - 858 + score_two_pairs(hand)

    elif twos(hand):
        return "pair", 7462 - 156 - 156 - 1277 - 10 - 858 - 858 - 2860 + score_pairs(hand)

    else:
        return "high card", 7462 - 156 - 156 - 1277 - 10 - 858 - 858 - 2860 - 1277 + score_high_card(hand)
