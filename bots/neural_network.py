import json
import sys
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SoftmaxLayer
from pybrain.datasets import SupervisedDataSet

def load_training_data(file):
    data = open(file)
    return json.load(data)

# We always want the actor inputs be first
def put_index_first(arr, idx):
    return [arr[idx]] + arr[0:idx] + arr[idx+1:]

# 1 and 0 seems like good NN inputs
def map_to_binary(arr):
    return map(lambda e: int(e), arr)

# We don't want to train on 300 descrete values.. so let's make it 30
def bucketize(arr):
    return map(lambda e: e/10, arr)

# Maps game state to input that can be used to feed NN
def extract_winning_sample(game_info):
    winning_idx = map(lambda v: v > 0, game_info[15:]).index(True)
    return [game_info[winning_idx]] + bucketize(put_index_first(game_info[3:6], winning_idx)) + map_to_binary(put_index_first(game_info[6:9], winning_idx)) + bucketize(put_index_first(game_info[9:12], winning_idx))

training_data = load_training_data(sys.argv[1])
print "Training data size is %d" % len(training_data)

for i in range(5):
    print training_data[i]
    print extract_winning_sample(training_data[i])
    print "---"
