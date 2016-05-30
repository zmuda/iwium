import os
import subprocess


def prepare_nn_input(bot1, bot2, bot3):
    if os.path.exists("GAME_STATES.out"):
        os.remove("GAME_STATES.out")
    if os.path.exists("GAME_STATES_RND.out"):
        os.remove("GAME_STATES_RND.out")
    subprocess.call(['python', 'state_dumping_runner.py', bot1, bot2, bot3])
    os.rename("GAME_STATES.out", "GAME_STATES_RND.out")


custom = 'bots.custom_reinforcement'
static = 'bots.simple_odds'
reinforced = 'bots.rl.bot'
nn = 'bots.nn.bot'

subprocess.call(['python', 'experiment_runner.py', static, static, custom])

subprocess.call(['python', 'experiment_runner.py', custom, custom, reinforced])
subprocess.call(['python', 'experiment_runner.py', static, static, reinforced])

prepare_nn_input(custom, custom, custom)
subprocess.call(['python', 'experiment_runner.py', custom, custom, nn])
prepare_nn_input(static, static, static)
subprocess.call(['python', 'experiment_runner.py', static, static, nn])
prepare_nn_input(reinforced, reinforced, reinforced)
subprocess.call(['python', 'experiment_runner.py', reinforced, reinforced, nn])

prepare_nn_input(static, static, static)
subprocess.call(['python', 'experiment_runner.py', reinforced, reinforced, nn, 'true'])