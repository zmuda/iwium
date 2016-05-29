from random import *
import neural_network


class Player:
    def bet1_data(self):
        return [self.card]

    def call1_data(self):
        return self.bet1_data() + [self.my_bet, self.opp1_bet, self.opp2_bet]

    def bet2_data(self):
        return self.call1_data() + [1, int(self.opp1_in_game), int(self.opp2_in_game)]

    def call2_data(self):
        return self.bet2_data() + [self.my_bet2, self.opp1_bet2, self.opp2_bet2]

    def name(self, index):
        self.me = index
        [self.opp1, self.opp2] = [i for i in range(3) if i != self.me]
        self.stack = 300

    def __init__(self):
        training_data = neural_network.load_training_data("GAME_STATES_RND.out")
        self.bid1_nn = neural_network.build_bid1_nn(training_data)
        self.call1_nn = neural_network.build_call1_nn(training_data)
        self.bid2_nn = neural_network.build_bid2_nn(training_data)
        self.call2_nn = neural_network.build_call2_nn(training_data)

    def hand(self, card):
        self.card = card

    def bet1(self, min):
        print 'Bet1data', self.bet1_data()
        self.my_bet = max(int(self.bid1_nn.activate(tuple(self.bet1_data()))[0]), min)
        print 'My bet is', self.my_bet
        return self.my_bet

    def bet1_info(self, bets):
        self.opp1_bet = bets[self.opp1]
        self.opp2_bet = bets[self.opp2]

    def call1(self, bet):
        print 'Call1data', self.call1_data()
        result = self.call1_nn.activate(tuple(self.call1_data()))[0]
        print 'Should stay', result
        return result > 0.16

    def call1_info(self, in_game):
        self.opp1_in_game = in_game[self.opp1]
        self.opp2_in_game = in_game[self.opp2]

    def bet2(self, min):
        print 'Bet2data', self.bet2_data()
        self.my_bet2 = max(int(self.bid2_nn.activate(tuple(self.bet2_data()))[0]), min)
        print 'My bet is', self.my_bet2
        return self.my_bet2

    def bet2_info(self, bets):
        self.opp1_bet2 = bets[self.opp1]
        self.opp2_bet2 = bets[self.opp2]

    def call2(self, bet):
        print 'Call2data', self.call2_data()
        result = self.call2_nn.activate(tuple(self.call2_data()))[0]
        print 'Should stay', result
        return result > 0.08

    def call2_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]

    def showdown(self, hand):
        opp1_hadd = hand[self.opp1]
        opp2_hand = hand[self.opp2]

    def result(self, winnings):
        my_winnings = winnings[self.me]
        opp1_winnings = winnings[self.opp1]
        opp2_winnings = winnings[self.opp2]
