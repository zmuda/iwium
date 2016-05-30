import copy
import random


class Round:
    def __init__(self):
        self.first_bets = None
        self.second_bets = None
        self.first_calls = None
        self.second_calls = None
        self.hand = None


class Context:
    def __init__(self):
        self.history = []

        self.id = -1
        self.he = -2
        self.she = -3

        self.stack = 300
        self.possible_cards = range(10)
        self.cards_count = 10

        self.hePlays = True
        self.shePlays = True

        self.myBets = -1
        self.heBets = -1
        self.sheBets = -1

        self.card = -1

        self.round_record = Round()
        self.history = []

    def init_round(self):
        self.hePlays = True
        self.shePlays = True
        self.myBets = -1
        self.heBets = -1
        self.sheBets = -1
        self.card = -1
        self.round_record = Round()

    def active_players(self):
        active_players = 0
        active_players += 1 if self.hePlays else 0
        active_players += 1 if self.shePlays else 0
        return active_players

    def total_bets(self):
        return self.heBets + self.sheBets + self.myBets

    def to_call(self):
        return max(self.heBets, self.sheBets) - self.myBets

    def set_id_mapping(self, my_id):
        self.id = my_id
        [self.he, self.she] = [i for i in range(3) if i != my_id]

    def set_mapped_bets(self, bets):
        self.heBets = bets[self.he]
        self.sheBets = bets[self.she]
        self.myBets = bets[self.id]

    def store_first_bets(self, bets):
        self.round_record.first_bets = copy.copy(bets)

    def store_second_bets(self, bets):
        self.round_record.second_bets = copy.copy(bets)

    def update_with_cards(self, hand):
        self.round_record.hand = copy.copy(hand)
        self.history.append(self.round_record)
        if len(self.history) > 1000:
            self.history.pop(0)
        self.round_record = None

    def set_presence(self, in_game):
        self.hePlays = in_game[self.he]
        self.shePlays = in_game[self.she]

    def store_first_calls(self, in_game):
        self.round_record.first_calls = copy.copy(in_game)

    def store_second_calls(self, in_game):
        self.round_record.second_calls = copy.copy(in_game)


class SimpleHistoryBasedOdds:
    def __init__(self, possible_cards=range(10)):
        share_on_tie = 0.5
        self.simple_odds = [
            (len([1 for x in possible_cards if x < card]) + share_on_tie) / len(possible_cards)
            for card in possible_cards
            ]

    def winning_odds(self, ctx):
        tie_factor = 0.5
        simple_odds = (len([1 for x in ctx.possible_cards if x < ctx.card]) + tie_factor) / ctx.cards_count
        return simple_odds ** ctx.active_players()

    def pot_odds(self, to_gain, actual_bet, required_bet, card, active_players):
        odds = self.simple_odds[card]
        odds = odds ** active_players
        to_call = required_bet - actual_bet
        return (to_gain + to_call) * odds / to_call

    def expected_for_cards(self, player, ctx, get_value=None):
        per_card = {i: [] for i in ctx.possible_cards}
        for round in ctx.history:
            card = round.hand[player]
            if card is not None:
                per_card[card].append(get_value(round))

        medians_per_card = {i: sorted(j)[len(j) / 2] for i, j in per_card.iteritems() if len(j) > 0}
        return medians_per_card

    def expected_bet1_for_cards(self, player, ctx):
        return self.expected_for_cards(player, ctx, lambda round: round.first_bets[player])

    def expected_bet2_ratio_for_cards(self, player, ctx):
        get_ratio = lambda round: float(round.second_bets[player]) / max(round.first_bets)
        return self.expected_for_cards(player, ctx, get_ratio)

    def history_based_odds(self, player, ctx, get_estimated=None):
        medians_per_card = self.expected_for_cards(player, ctx, get_estimated)
        actual = get_estimated(ctx.round_record)

        distances = {k: abs(v - actual) for k, v in medians_per_card.iteritems()}
        max_distance = max(distances.values()) if len(distances) > 0 else 0

        factors = {k: max_distance - v for k, v in distances.iteritems()}
        total = sum(factors.values()) if len(factors) > 0 else 0

        probs = {k: float(v) / total if total > 0 else 0.1 for k, v in factors.iteritems()}
        winning_prob = sum([v for k, v in probs.iteritems() if k < ctx.card]) + probs.get(ctx.card, 0) / 2
        return winning_prob

    def history_based_call_odds1(self, player, ctx):
        return self.history_based_odds(player, ctx, lambda round: round.first_bets[player])

    def history_based_call_odds2(self, player, ctx):
        get_ratio = lambda round: float(round.second_bets[player]) / max(round.first_bets)
        return self.history_based_odds(player, ctx, get_ratio)

    def call_odds1(self, ctx):
        historical_odds = self.history_based_call_odds1(ctx.he, ctx) * self.history_based_call_odds1(ctx.she, ctx)
        odds = self.winning_odds(ctx) / 4 + historical_odds / 4 * 3
        odds += random.uniform(-.05, .05)

        result = (ctx.total_bets() + ctx.to_call()) * odds > ctx.to_call()
        return bool(result)

    def call_odds2(self, ctx):
        historical_odds = 1
        if ctx.hePlays:
            historical_odds *= self.history_based_call_odds2(ctx.he, ctx)
        if ctx.shePlays:
            historical_odds *= self.history_based_call_odds2(ctx.she, ctx)

        odds = self.winning_odds(ctx) / 1 + historical_odds / 4 * 3
        odds += random.uniform(-.05, .05)

        result = (ctx.total_bets() + ctx.to_call()) * odds > ctx.to_call()
        return bool(result)


class Player:
    def __init__(self):
        self.simple_odds = SimpleHistoryBasedOdds()
        self.ctx = Context()

    def name(self, index):
        self.ctx.set_id_mapping(index)

    def hand(self, card):
        self.ctx.init_round()
        self.ctx.card = card

    def bet1(self, min):
        return min

    def bet1_info(self, bets):
        self.ctx.set_mapped_bets(bets)
        self.ctx.store_first_bets(bets)

    def call1(self, bet):
        return self.simple_odds.call_odds1(self.ctx)

    def call1_info(self, in_game):
        self.ctx.store_first_calls(in_game)
        self.ctx.set_presence(in_game)

    def bet2(self, min):
        calculated = self.simple_odds.winning_odds(self.ctx) * self.ctx.stack
        return max(int(calculated), min)

    def bet2_info(self, bets):
        self.ctx.set_mapped_bets(bets)
        self.ctx.store_second_bets(bets)

    def call2(self, bet):
        return self.simple_odds.call_odds2(self.ctx)

    def call2_info(self, in_game):
        self.ctx.store_second_calls(in_game)
        self.ctx.set_presence(in_game)

    def showdown(self, hand):
        self.ctx.update_with_cards(hand)

    def result(self, winnings):
        pass
