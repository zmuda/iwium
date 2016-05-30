import pprint
import operator
from pybrain.rl.environments.environment import Environment
from pybrain.rl.environments.task import Task
from scipy import zeros


class GameTask(Task):
    def __init__(self, environment):
        super(GameTask, self).__init__(environment)
        self.env = environment

    def performAction(self, action):
        self.env.performAction(action)

    def getObservation(self):
        sensors = self.env.getSensors()
        return sensors

    def getReward(self):
        action = self.env.getSymbolicLastAction()

        wrong_action_penalty = -0.
        if self.env.phase in ['bet-1', 'bet-2']:
            if action in ['call']:
                return wrong_action_penalty

        if self.env.phase in ['call-1', 'call-2']:
            if action in self.env.POSSIBLE_BETS_THRESHOLDS.keys():
                return wrong_action_penalty

        if self.env.phase == 'results':
            return self.winnings / 600.

        return 0.

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim

    def setWinnings(self, my_winnings):
        self.winnings = my_winnings


class GameEnv(Environment):
    CARDS = range(0, 10)
    POSSIBLE_STATES = ['plays', 'folded']
    POSSIBLE_BETS_THRESHOLDS = {'-1+': -1,
                                '10+': 10, '40+': 40,
                                '80+': 80, '110+': 110,
                                '140+': 140, '170+': 170,
                                '200+': 200, '230+': 230,
                                '260+': 260, '290+': 290}

    def __init__(self):
        super(GameEnv, self).__init__()

        # discrete state space
        self.discreteStates = False
        # discrete action space
        self.discreteActions = False
        # number of possible actions for discrete action space
        self.numActions = None

        self._genPossibleActions()
        self._genPossibleStates()

        # the number of action values the environment accepts
        self.indim = len(self.actions)
        # the number of sensor values the environment produces
        self.outdim = len(self.states)

    def _bet(self, numeric):
        lesser = {k: v for k, v in self.POSSIBLE_BETS_THRESHOLDS.iteritems() if v <= numeric}
        sorted_lesser = sorted(lesser.items(), key=operator.itemgetter(1))
        symbolic = sorted_lesser[-1][0]
        return symbolic

    def _genPossibleActions(self):
        actions = ['fold', 'call'] + ['bet=' + bet for bet in self.POSSIBLE_BETS_THRESHOLDS.keys()]
        actions_map = dict()
        actions_reversed_map = dict()
        for i in xrange(len(actions)):
            actions_map[actions[i]] = float(i)
            actions_reversed_map[float(i)] = actions[i]
        self.actions = actions_map
        self.actions_reversed = actions_reversed_map
        return actions_map

    def _genPossibleStates(self):
        bet_ranges = self.POSSIBLE_BETS_THRESHOLDS.keys()

        bet1_STATES = [
            ['bet-1', card]
            for card in self.CARDS
            ]
        call1_STATES = [
            ['call-1', card, bet, op1, op2, op1_state, op2_state]
            for card in self.CARDS
            for bet in bet_ranges
            for op1 in bet_ranges
            for op2 in bet_ranges
            for op1_state in self.POSSIBLE_STATES
            for op2_state in self.POSSIBLE_STATES
            ]
        bet2_STATES = [
            ['bet-2', card, bet, op1, op2, op1_state, op2_state]
            for card in self.CARDS
            for bet in bet_ranges
            for op1 in bet_ranges
            for op2 in bet_ranges
            for op1_state in self.POSSIBLE_STATES
            for op2_state in self.POSSIBLE_STATES
            ]
        call2_STATES = [
            ['call-2', card, bet, op1, op2, op1_state, op2_state]
            for card in self.CARDS
            for bet in bet_ranges
            for op1 in bet_ranges
            for op2 in bet_ranges
            for op1_state in self.POSSIBLE_STATES
            for op2_state in self.POSSIBLE_STATES
            ]
        result_STATES = [
            ['results']
        ]

        states = bet1_STATES + call1_STATES + bet2_STATES + call2_STATES + result_STATES
        states_map = dict()
        for i in xrange(len(states)):
            states_map[str(states[i])] = float(i)

        self.states = states_map
        return states

    def getSensors(self):
        if self.phase == 'results':
            key = [self.phase]
        elif self.phase == 'bet-1':
            key = [self.phase, self.card]
        else:
            key = [
                self.phase,
                self.card,
                self._bet(self.own_bet),
                self._bet(self.opp_bets[0]),
                self._bet(self.opp_bets[1]),
                'folded' if self.opp_folded[0] else 'plays',
                'folded' if self.opp_folded[1] else 'plays',
            ]

        return [self.states[str(key)], ]

    def performAction(self, action):
        self.last_action = action

    def getTranslatedAction(self):
        action = self.getSymbolicLastAction()
        if action.startswith("bet="):
            action = action[4:]

        if self.phase in ['bet-1', 'bet-2']:
            if action in self.POSSIBLE_BETS_THRESHOLDS.keys():
                return self.POSSIBLE_BETS_THRESHOLDS[action]
            else:
                return -1

        if self.phase in ['call-1', 'call-2']:
            if action in self.POSSIBLE_BETS_THRESHOLDS.keys():
                return True
            else:
                return True if action == 'call' else 'fold'

    def getSymbolicLastAction(self):
        return self.actions_reversed[self.last_action[0]]

    def reset(self):
        self.card = -1
        self.stack = -1
        self.phase = -1
        self.min_bet = -1
        self.to_call = -1
        self.own_bet = -1
        self.opp_bets = [-1, -1]
        self.opp_folded = [-1, -1]

    def setHand(self, card):
        self.card = card

    def setStack(self, stack):
        self.stack = stack

    def setPhase(self, phase):
        self.phase = phase

    def setMinBet(self, min):
        self.min_bet = min

    def setOpponentsBets(self, opp1_bet, opp2_bet):
        self.opp_bets = [opp1_bet, opp2_bet]

    def setToCall(self, current_bet):
        self.to_call = current_bet

    def setOpponentsFolded(self, opp1_folded, opp2_folded):
        self.opp_folded = [opp1_folded, opp2_folded]
