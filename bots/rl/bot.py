from random import *

from pybrain.rl.agents import LearningAgent
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
from pybrain.rl.learners import ActionValueTable, Q

from bots.rl.rl import GameEnv, GameTask


class Player:
    def __init__(self):
        self.environment = GameEnv()

        av_table = ActionValueTable(self.environment.outdim, self.environment.indim)
        av_table.initialize(0.)  # todo: save & restore agents state
        learner = Q()
        learner._setExplorer(EpsilonGreedyExplorer())
        agent = LearningAgent(av_table, learner)

        self.agent = agent
        self.task = GameTask(self.environment)
        self.experiment = Experiment(self.task, self.agent)

    def name(self, index):
        self.me = index
        [self.opp1, self.opp2] = [i for i in range(3) if i != self.me]

    def hand(self, card):
        self.environment.reset()
        self.environment.setHand(card)
        self.environment.setStack(300)

    def bet1(self, min):
        self.environment.setPhase('bet-1')
        self.environment.setMinBet(min)
        self.experiment.doInteractions(1)
        bet = self.environment.getTranslatedAction()
        return bet

    def bet1_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]
        self.environment.setOpponentsBets(opp1_bet, opp2_bet)

    def call1(self, current_bet):
        self.environment.setPhase('call-1')
        self.environment.setToCall(current_bet)
        self.experiment.doInteractions(1)
        is_calling = self.environment.getTranslatedAction()
        return is_calling

    def call1_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]
        self.environment.setOpponentsFolded(not opp1_in_game, not opp2_in_game)

    def bet2(self, min):
        self.environment.setPhase('bet-2')
        self.environment.setMinBet(min)
        self.experiment.doInteractions(1)
        bet = self.environment.getTranslatedAction()
        return bet

    def bet2_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]
        self.environment.setOpponentsBets(opp1_bet, opp2_bet)

    def call2(self, current_bet):
        self.environment.setPhase('call-1')
        self.environment.setToCall(current_bet)
        self.experiment.doInteractions(1)
        is_calling = self.environment.getTranslatedAction()
        return is_calling

    def call2_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]

    def showdown(self, hand):
        opp1_hand = hand[self.opp1]
        opp2_hand = hand[self.opp2]

    def result(self, winnings):
        my_winnings = winnings[self.me]
        opp1_winnings = winnings[self.opp1]
        opp2_winnings = winnings[self.opp2]

        self.environment.setPhase('results')
        self.task.setWinnings(my_winnings)
        self.experiment.doInteractions(1)

        self.agent.learn()
        self.agent.reset()
