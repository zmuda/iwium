class SimpleOdds:
    def __init__(self, possible_cards=range(10)):
        self.possible_cards = possible_cards
        self.cards_count = len(possible_cards)

    def winning_odds(self, card, players_count=2):
        tie_factor = 0.5
        odds = (len([1 for x in self.possible_cards if x < card]) + tie_factor) / self.cards_count
        return odds ** players_count

    def call_odds(self, card, at_table, to_call, players_count=2, ):
        odds = self.winning_odds(card, players_count)
        return bool((at_table + to_call) * odds > to_call)

class Player:
    def __init__(self):
        self.simple_odds = SimpleOdds()
        pass

    def name(self, index):
        self.me = index
        [self.opp1, self.opp2] = [i for i in range(3) if i != self.me]
        self.stack = 300

    def hand(self, card):
        self.card = card

    def bet1(self, min):
        calculated = self.simple_odds.winning_odds(self.card, 2) * self.stack / 10
        bet = max(int(calculated), min)
        return bet

    def bet1_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]
        my_bet = bets[self.me]
        self.at_table = sum(bets)
        self.to_call = max(opp1_bet, opp2_bet) - my_bet

    def call1(self, bet):
        do_call = self.simple_odds.call_odds(self.card, self.at_table, self.to_call, 2)
        return do_call

    def call1_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]
        self.players_count = sum([1 for x in [opp1_in_game, opp2_in_game] if x])

    def bet2(self, min):
        calculated = self.simple_odds.winning_odds(self.card, self.players_count) * self.stack
        bet = max(int(calculated), min)
        return bet

    def bet2_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]
        my_bet = bets[self.me]
        self.at_table = sum(bets)
        self.to_call = max(opp1_bet, opp2_bet) - my_bet

    def call2(self, bet):
        do_call = self.simple_odds.call_odds(self.card, self.at_table, self.to_call, self.players_count)
        return do_call

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
