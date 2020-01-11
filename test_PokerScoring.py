import unittest
import PokerScoring
import CardDeck
import random


class TestPokerHands(unittest.TestCase):
    def setUp(self):
        # suit values
        diamonds = 0
        hearts = 1
        spade = 2
        clubs = 3

        # duplicates setup
        self.multiples = [CardDeck.Card(diamonds, 4),CardDeck.Card(hearts, 4),CardDeck.Card(spade, 4),CardDeck.Card(clubs, 4)]

        # full house setup
        self.doubles = [[CardDeck.Card(diamonds, 4), CardDeck.Card(spade, 4)],[CardDeck.Card(hearts, 1), CardDeck.Card(clubs, 1)]]
        self.doubles_same = [[CardDeck.Card(diamonds, 4), CardDeck.Card(spade, 4)],[CardDeck.Card(hearts, 0), CardDeck.Card(clubs, 0)]]
        self.only_triples = [[CardDeck.Card(diamonds, 0), CardDeck.Card(spade, 0),CardDeck.Card(hearts, 0)]]

        self.straight_test = []
        # straight setup
        for i in range(7):
            self.straight_test.append(CardDeck.Card(clubs, i))

        self.flush_test = []
        # flush setup
        for i in range(7):
            self.flush_test.append(CardDeck.Card(hearts, random.randint(0, 13)))

        # straight flush setup
        self.straights = []
        self.flushes = []
        straight = []
        flush = []

        # generate straight flush
        for i in range(5):
            straight.append(CardDeck.Card(hearts, i))

        for i in range(5):
            flush.append(CardDeck.Card(hearts, i))

        self.flushes.append(flush)
        self.straights.append(straight)

        pass

    def test_duplicates(self):
        dupl = PokerScoring.duplicates(self.multiples)
        self.assertEqual(3, len(dupl))

    def test_full_house(self):

        # test doubles and triples with unique values
        full_house = PokerScoring.full_house(self.only_triples, self.doubles)
        self.assertEqual(2, len(full_house))
        for hands in full_house:
            self.assertEqual(5, len(hands))

        # test doubles and triples where values arent unique
        full_house = PokerScoring.full_house(self.only_triples, self.doubles_same)
        self.assertEqual(1, len(full_house))
        for hands in full_house:
            self.assertEqual(5, len(hands))

    def test_two_pair(self):

    def test_straights(self):
        straights = PokerScoring.connectivity(self.straight_test)
        self.assertEqual(3, len(straights))
        for straight in straights:
            self.assertEqual(5, len(straight))

    def test_flushes(self):
        flushes = PokerScoring.same_suit(self.flush_test)
        self.assertEqual(3, len(flushes))
        for flush in flushes:
            self.assertEqual(5, len(flush))

    def test_straight_flush(self):
        straight_flushes = PokerScoring.connected_flushes(self.flushes, self.straights)
        self.assertEqual(1, len(straight_flushes))

    def test_four_kind(self):

    def test_three_kind(self):

    def test_pair(self):