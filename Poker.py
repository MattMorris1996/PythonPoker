from PokerPlayers import *
from CardDeck import *
from random import *


# Main class interacts with the Deck the flop and the players
class Poker:
    def __init__(self, n_players, buy_in):
        self.deck = Deck()
        self.number_players = n_players

        self.players = []

        self.players_active = set(list(range(self.number_players)))

        self.player_id_turn = 0

        self.blind = 10
        self.call_amount = self.blind

        self.pot = 0
        self.check_flag = False

        self.flop = []
        self.turn = []
        self.river = []

        self.burn = []

        for i in range(n_players):
            p = Player(buy_in, i, ai=1)
            self.players.append(p)

        self.dealer_id = randint(0, self.number_players - 1)

        self.big_blind_id = (self.dealer_id + 1) % self.number_players
        self.small_blind_id = (self.dealer_id + 2) % self.number_players
        self.lead_bet_id = self.big_blind_id

    def GameInit(self):
        # reset folded players
        self.players_active = set(list(range(self.number_players)))

        # move dealer one position
        self.dealer_id = (1 + self.dealer_id) % self.number_players

        # set blinds
        self.big_blind_id = (self.dealer_id + 1) % self.number_players
        self.small_blind_id = (self.dealer_id + 2) % self.number_players
        self.lead_bet_id = self.big_blind_id

        self.call_amount = self.blind

        self.flop = []
        self.turn = []
        self.river = []

        self.pot = 0
        self.check_flag = False

    def Game(self):
        # Pre Flop
        for i in range(10000):
            self.GameInit()
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
            winner = self.score_hands()
            self.game_end(winner)

        for p in self.players:
            print("Player " + str(p.number) + " win rate:")
            print(p.wins/(p.losses + p.wins))

    def game_end(self, winning_player_id):
        print("Player " + str(winning_player_id) + " Wins!")
        player = self.players[winning_player_id]

        for p in self.players:
            if p.number == winning_player_id:
                p.wins += 1
            else:
                p.losses += 1

        player.chips += self.pot
        self.pot = 0

        for id in self.players_active:
            self.deck.cards += self.players[id].fold()

        self.deck.cards += self.flop + self.river + self.turn + self.burn

        assert (len(self.deck.cards) == 52)

    def next_player(self):
        self.player_id_turn = (self.player_id_turn + 1) % self.number_players
        while self.player_id_turn not in self.players_active:
            self.player_id_turn = (self.player_id_turn + 1) % self.number_players

    def round_init(self, pre_flop=False):
        if pre_flop:
            # pre flop take blinds and decide player 1
            self.players[self.big_blind_id].bet(self.blind)
            self.pot += self.blind

            self.players[self.small_blind_id].bet(self.blind // 2)
            self.pot += self.blind // 2

            self.player_id_turn = (self.big_blind_id + 1) % self.number_players
            self.check_flag = False
        else:
            # set check flag and get first player id
            self.check_flag = True
            self.player_id_turn = (self.dealer_id + 1) % self.number_players
            while self.player_id_turn not in self.players_active:
                self.player_id_turn = (self.player_id_turn + 1) % self.number_players
            self.lead_bet_id = self.player_id_turn

    def process_player_turn(self, option):
        move = option[0]
        if move == 'raise':
            amount = option[1]
            self.call_amount = option[2]
            self.players[self.player_id_turn].bet(amount)
            self.lead_bet_id = self.player_id_turn
            self.pot += amount
            self.check_flag = False
        elif move == 'call':
            amount = option[1]
            self.players[self.player_id_turn].bet(amount)
            self.pot += amount
            self.check_flag = False
        elif move == 'fold':
            self.deck.cards += self.players[self.player_id_turn].fold()
            self.players_active.remove(self.player_id_turn)
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

                if len(self.players_active) <= 1:
                    print("all players folded")
                    break
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
                if len(self.players_active) <= 1:
                    print("all players folded")
                    break
                # player is told information about the current bet, player can raise or call if player raises he takes over as the lead bet
                # and BB can no longer check to progress the round
                # if players have completed betting and lead bet is not big blind
                # get players option if player is big blind offer check option
                option = self.players[self.player_id_turn].turn(
                    check=self.check_flag,
                    call_amount=self.call_amount,
                    pot_size=self.pot,
                    flop=self.flop + self.turn + self.river
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
        winning_hand = ("Winning Hand", 0, None)
        for p in self.players:
            score = p.score(self.flop + self.turn + self.river)
            if score[1] > winning_hand[1]:
                winning_hand = score + tuple([p.number])
        return winning_hand[2]


if __name__ == '__main__':
    PLAYERS = 8
    BUY_IN = 1000

    game = Poker(PLAYERS, BUY_IN)
    game.Game()

    # game.deal()
    # game.print_hands()
    # game.print_flop()
    # game.score_hands()
