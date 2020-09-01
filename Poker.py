from PokerPlayers import *
from CardDeck import *
from PokerScoring import *
from random import *

# Main class interacts with the Deck the flop and the players
class Poker:
    def __init__(self, n_players, buy_in):
        self.deck = Deck()
        self.number_players = n_players

        self.players = []
        self.players_folded = set()

        self.n_round = 0
        self.player_id_turn = 0
        self.n_player_active = n_players

        self.blind = 10
        self.call_amount = self.blind
        self.pot = 0
        self.check_flag = False

        self.flop = []
        self.turn = []
        self.river = []

        self.dealer_cards = self.flop + self.turn + self.river

        self.burn = []

        for i in range(n_players):
            p = Player(buy_in, i)
            self.players.append(p)

        self.dealer_id = randint(0, self.number_players - 1)
        self.dealer = self.players[self.dealer_id]

        self.big_blind_id = (self.dealer_id + 1) % self.number_players
        self.small_blind_id = (self.dealer_id + 2) % self.number_players
        self.lead_bet_id = self.big_blind_id

    def Game(self):
        # Pre Flop
        self.deal_hands()
        self.round(round='start')
        # Flop
        self.deal_flop()
        self.round()
        # Turn
        self.deal_turn()
        self.round()
        # River
        self.deal_river()
        self.round()
        # The showdown
        self.score_hands()

    def next_player(self):
        self.player_id_turn = (self.player_id_turn + 1) % self.number_players
        while self.player_id_turn in self.players_folded:
            self.player_id_turn = (self.player_id_turn + 1) % self.number_players

    def round_init(self, pre_flop=False):
        if pre_flop:
            # pre flop take blinds and decide player 1
            self.player_id_turn = self.big_blind_id
            self.players[self.big_blind_id].bet(self.blind)
            self.pot += self.blind
            self.players[self.small_blind_id].bet(self.blind // 2)
            self.pot += self.blind//2
            self.player_id_turn = (self.big_blind_id + 1) % self.number_players
            self.check_flag = False
        else:
            # set check flag and get first player id
            self.check_flag = True
            self.player_id_turn = (self.dealer_id + 1) % self.number_players
            while self.player_id_turn in self.players_folded:
                self.player_id_turn = (self.player_id_turn + 1) % self.number_players
            self.lead_bet_id = self.player_id_turn

    def process_player_turn(self, option):
        move = option[0]
        if move == 'raise':
            amount = option[1]
            self.call_amount = option[2]
            self.players[self.player_id_turn].bet(amount)
            self.lead_bet_id = self.player_id_turn
            self.check_flag = False
        elif move == 'call':
            amount = option[1]
            self.players[self.player_id_turn].bet(amount)
            self.pot += amount
            self.check_flag = False
        elif move == 'fold':
            self.deck.cards += self.players[self.player_id_turn].fold()
            self.players_folded.add(self.player_id_turn)
            self.check_flag = False
        elif move == 'check':
            self.check_flag = True

    def round(self, round='None'):
        # round1 start with player to left of bb
        # players can call raise or fold
        # big blind can check or raise
        # round does not progress until all player have bet the max amount
        # round2 onwards play starts from big blind or first player to left
        # players can check raise call or fold
        # next round if all players check or all player bet the match bets

        if round == 'start':
            # lead bet id is the big blind

            self.round_init(pre_flop=True)

            while 1:
                # player is told information about the current bet, player can raise or call if player raises he
                # takes over as the lead bet and BB can no longer check to progress the round

                # skip folder player
                pre_flop_check = self.player_id_turn == self.big_blind_id == self.lead_bet_id
                # get players option if player is big blind offer check option
                option = self.players[self.player_id_turn].turn(
                    check=pre_flop_check,
                    flop=self.flop + self.turn + self.river,
                    call_amount=self.call_amount,
                    pot_size=self.pot
                )

                # obtain move from option tuple
                self.process_player_turn(option)
                self.next_player()

                # check for break conditions
                # if players have completed betting and lead bet is not big blind
                if self.player_id_turn == self.lead_bet_id != self.big_blind_id:
                    print("all players completed betting round")
                    break

                if self.check_flag:
                    print("BB check")
                    break
        else:
            # lead bet id is the big blind
            self.round_init()
            while 1:
                # player is told information about the current bet, player can raise or call if player raises he takes over as the lead bet
                # and BB can no longer check to progress the round
                # if players have completed betting and lead bet is not big blind
                # get players option if player is big blind offer check option
                option = self.players[self.player_id_turn].turn(
                    check=self.check_flag,
                    call_amount=self.call_amount,
                    pot_size=self.pot,
                    flop = self.flop + self.turn + self.river
                )

                # obtain move from option tuple
                self.process_player_turn(option)
                self.next_player()

                if self.player_id_turn == self.lead_bet_id:
                    print("players have completed betting")
                    break

    def deal_flop(self):
        for i in range(3):
            self.flop.append(self.deck.cards.pop())

    def deal_turn(self):
        self.turn.append(self.deck.cards.pop())

    def deal_river(self):
        self.river.append(self.deck.cards.pop())

    def deal_hands(self):  # shuffle deck and deal two cards too all players
        self.deck.shuffle()
        for j in range(2):
            for i in self.players:
                i.deal(self.deck.cards.pop())

    def print_hands(self):  # print all hands
        for i in self.players:
            print("player", i.number + 1, end=" ")
            print(" chips", i.chips)
            for j in i.hand:
                j.print_card()
            print()

    def print_flop(self):
        print("The Flop")
        for i in self.flop:
            i.print_card()
            print(",", end="")
        for i in self.turn:
            i.print_card()
            print(",", end="")
        for i in self.river:
            i.print_card()
            print(",", end="")
        print("")

    def score_hands(self):
        i = 0
        winning_hand = ("Winning Hand", 0, None)
        for player in self.players:
            i = i + 1
            score = player.score(self.flop + self.turn + self.river)
            if score[1] > winning_hand[1]:
                winning_hand = score, i - 1

        print(winning_hand)



if __name__ == '__main__':
    PLAYERS = 3
    BUY_IN = 1000

    game = Poker(PLAYERS, BUY_IN)
    game.Game()

    # game.deal()
    # game.print_hands()
    # game.print_flop()
    # game.score_hands()
