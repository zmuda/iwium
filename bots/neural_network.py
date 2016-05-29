import json
import sys

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SigmoidLayer, TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

def load_training_data(file):
    data = open(file)
    return json.load(data)

# We always want the actor inputs be first
def put_index_first(arr, idx):
    return [arr[idx]] + arr[0:idx] + arr[idx+1:]

# 1 and 0 seems like good NN inputs
def map_to_binary(arr):
    return map(lambda e: int(e), arr)

# Maps game state to input that can be used to feed NN
def extract_sample(game_info, winning=True):
    if not (game_info[15] > 0 or game_info[16] > 0 or game_info[17] > 0):
        # bad lack
        winning_idx = 0
    else:
        winning_idx = map(lambda v: v > 0, game_info[15:]).index(winning)

    return [game_info[winning_idx]] + put_index_first(game_info[3:6], winning_idx) + map_to_binary(put_index_first(game_info[6:9], winning_idx)) + put_index_first(game_info[9:12], winning_idx)

# Datesets constructoes
def build_bid1_nn(training_data):
    ds = SupervisedDataSet(1, 1)
    for game_state in training_data:
        winning_sample = extract_sample(game_state)
        ds.addSample((winning_sample[0],), (winning_sample[1],))
    net = buildNetwork(1, 1)
    trainer = BackpropTrainer(net, ds)
    for i in range(10):
        trainer.train()
    return net

def build_bid2_nn(training_data):
    ds = SupervisedDataSet(7, 1)
    for game_state in training_data:
        winning_sample = extract_sample(game_state)
        ds.addSample(tuple(winning_sample[0:7]), (winning_sample[8],))
    net = buildNetwork(7, 9, 1, bias=True)
    trainer = BackpropTrainer(net, ds)
    for i in range(10):
        trainer.train()
    return net


def build_call1_nn(training_data):
    ds = SupervisedDataSet(4, 1)
    for game_state in training_data:
        winning_sample = extract_sample(game_state)
        ds.addSample(tuple(winning_sample[0:4]), 1)

    for game_state in training_data:
        loosing_sample = extract_sample(game_state, False)
        ds.addSample(tuple(loosing_sample[0:4]), 0)

    net = buildNetwork(4, 6, 1, bias=True, outclass=SigmoidLayer)
    trainer = BackpropTrainer(net, ds)
    for i in range(10):
        trainer.train()
    return net

def build_call2_nn(training_data):
    ds = SupervisedDataSet(10, 1)
    for game_state in training_data:
        winning_sample = extract_sample(game_state)
        ds.addSample(tuple(winning_sample[0:10]), 1)

    for game_state in training_data:
        loosing_sample = extract_sample(game_state, False)
        ds.addSample(tuple(loosing_sample[0:10]), 0)

    net = buildNetwork(10, 12, 1, bias=True, outclass=SigmoidLayer)
    trainer = BackpropTrainer(net, ds)
    for i in range(10):
        trainer.train()
    return net

# Here comes the testing part
if __name__ == "__main__":
    training_data = load_training_data(sys.argv[1])
    print "Training data size is %d" % len(training_data)

    print "This is how extracing samples work"
    for i in range(5):
        print training_data[i]
        print extract_sample(training_data[i])
        print "---"

    print "Time for some NN!"
    net = build_call2_nn(training_data)
    print net.params
    print(net.activate((5, 100, 200, 300, 1, 1, 1, 200, 200, 300)))
