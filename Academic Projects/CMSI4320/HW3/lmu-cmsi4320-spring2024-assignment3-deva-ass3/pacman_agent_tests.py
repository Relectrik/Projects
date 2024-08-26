'''
Contains a variety of tests to validate the inner-workings of your
Pacman Trainer system
'''
import pandas as pd
import math
import itertools
import unittest
import pytest
import torch
from environment import *
from reinforcement_trainer import *

# Maze Prefabs
# -------------------------------------------------------------------------------------------------

TINIEST_MAZE = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXXXOXXXX",
     "XXXXPXXXX",
     "XXXX.XXXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]
    
TINY_MAZE = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXXXOXXXX",
     "XXXXPXXXX",
     "XXXXOXXXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]

PANIC_MAZE = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXX.O.XXX",
     "XXX.PGXXX",
     "XXX.O.XXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]

BASIC_MAZE = \
    ["XXXXXXXXX",
     "X..O...PX",
     "X.......X",
     "X..XXXO.X",
     "XO.....OX",
     "X.......X",
     "XXXXXXXXX"]

GHOST_MAZE = \
    ["XXXXXXXXX",
     "X..O...PX",
     "X.......X",
     "X..XXXO.X",
     "XO.....OX",
     "X......GX",
     "XXXXXXXXX"]

# Sample Transition Next States
# -------------------------------------------------------------------------------------------------

EATING_TRANSITION = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXXXPXXXX",
     "XXXX.XXXX",
     "XXXXOXXXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]

DED_TRANSITION = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXX.O.XXX",
     "XXX..DXXX",
     "XXX.O.XXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]
    
LIV_REW_TRANSITION = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXX.O.XXX",
     "XXXP.GXXX",
     "XXX.O.XXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]
    
FINISHED_TRANSITION = \
    ["XXXXXXXXX",
     "XXXXXXXXX",
     "XXXXPXXXX",
     "XXXX.XXXX",
     "XXXX.XXXX",
     "XXXXXXXXX",
     "XXXXXXXXX"]

class PacTrainerTests(unittest.TestCase):
    '''
    Simple checkpoint unit tests for the Pacman Trainer and Agent
    '''
    
    def test_pacman_agent_init(self) -> None:
        agent = PacmanAgent(BASIC_MAZE, is_training = False)
        
        self.assertTrue(hasattr(agent, "policy_net"), "[X] Make sure to save your agent's policy network named, exactly, self.policy_net in __int__")
        self.assertFalse(hasattr(agent, "target_net"), "[X] Your agent's target_net should be initialized ONLY when training, i.e., when Constants.TRAINING is True")
        self.assertFalse(hasattr(agent, "memory"), "[X] Your agent's replay memory should be initialized ONLY when training, i.e., when Constants.TRAINING is True")
        self.assertFalse(hasattr(agent, "optimizer"), "[X] Your agent's optimizer should be initialized ONLY when training, i.e., when Constants.TRAINING is True")
        
        agent = PacmanAgent(BASIC_MAZE, is_training = True)
        self.assertTrue(hasattr(agent, "policy_net"), "[X] Make sure to save your agent's policy network named, exactly, self.policy_net in __int__")
        self.assertTrue(hasattr(agent, "target_net"), "[X] Make sure to save your agent's target network named, exactly, self.target_net in __int__")
        self.assertTrue(hasattr(agent, "memory"), "[X] Make sure to save your agent's replay memory named, exactly, self.memory in __int__")
        self.assertTrue(hasattr(agent, "optimizer"), "[X] Make sure to save your agent's optimizer named, exactly, self.optimizer in __int__")
        self.assertEqual(PacNet, type(agent.policy_net))
        self.assertEqual(PacNet, type(agent.target_net))
        self.assertEqual(ReplayMemory, type(agent.memory))
        
        agent = PacmanAgent(BASIC_MAZE, is_training=True, fresh_start=True)
        self.assertEqual(0, len(agent.memory), "[X] Remember that you should only load any previous data when the fresh_start parameter is set to False")
    
    def test_pacman_agent_choose(self) -> None:
        # Run these a few times to make sure you're not just getting lucky
        for _ in range(10):
            agent = PacmanAgent(TINY_MAZE, is_training=True, fresh_start=True)
            mp = MazeProblem(TINY_MAZE)
            self.assertIn(agent.choose_action(mp, dict(mp.legal_actions(mp.get_player_loc()))), {"U", "D"}, "[X] Your agent is not returning a legal action when asked to choose or is erroring out in choose_action")
            agent = PacmanAgent(BASIC_MAZE, is_training=True, fresh_start=True)
            mp = MazeProblem(BASIC_MAZE)
            self.assertIn(agent.choose_action(mp, dict(mp.legal_actions(mp.get_player_loc()))), {"D", "L"}, "[X] Your agent is not returning a legal action when asked to choose or is erroring out in choose_action")
    
    def test_pacman_agent_reward(self) -> None:
        agent = PacmanAgent(TINY_MAZE, is_training=True, fresh_start=True)
        self.assertLess(0, agent.get_reward(MazeProblem(TINY_MAZE), "U", MazeProblem(EATING_TRANSITION)), "[X] You should have some positive reward for eating a pellet")
        agent = PacmanAgent(PANIC_MAZE, is_training=True, fresh_start=True)
        self.assertGreater(0, agent.get_reward(MazeProblem(PANIC_MAZE), "R", MazeProblem(DED_TRANSITION)), "[X] You should have some negative reward for dying")
        self.assertGreater(0, agent.get_reward(MazeProblem(PANIC_MAZE), "L", MazeProblem(LIV_REW_TRANSITION)), "[X] You'll probably want a tiny, negative living reward to Pacman doesn't dilly-dally")
    
    def test_pacman_agent_transition(self) -> None:
        agent = PacmanAgent(TINY_MAZE, is_training=True, fresh_start=True)
        self.assertEqual(0, len(agent.memory), "[X] Your agent's memory should be wiped clean at the start when the fresh_start parameter is True in __init__")
        agent.give_transition(MazeProblem(TINY_MAZE), "U", MazeProblem(EATING_TRANSITION), is_terminal=False)
        self.assertLess(0, len(agent.memory), "[X] Following a given transition, your agent's memory should store the new Episode")
        curr_len = len(agent.memory)
        agent.give_transition(MazeProblem(PANIC_MAZE), "R", MazeProblem(DED_TRANSITION), is_terminal=True)
        self.assertLess(curr_len, len(agent.memory), "[X] Following a given transition, your agent's memory should store the new Episode")
        
    def test_pacman_agent_optimization(self) -> None:
        # Changing constants lul I'm bad
        Constants.PARAM_PATH = "./dat/params_test_optimization.pth"
        Constants.MEM_PATH = "./dat/mem_test_optimization.pkl"
        agent = PacmanAgent(TINIEST_MAZE, is_training=True, fresh_start=True)
        og_params = str(agent.policy_net.state_dict())
        
        # Add a bunch of pretend transitions to the agent's experience and make sure the
        # optimization loop is at least changing the weights!
        # [!] Warning: this doesn't necessarily mean those changes are correct!
        for _ in range(Constants.BATCH_SIZE * 3):
            agent.give_transition(MazeProblem(TINIEST_MAZE), "U", MazeProblem(FINISHED_TRANSITION), is_terminal=False)
        
        self.assertNotEqual(str(agent.policy_net.state_dict()), og_params, "[X] Your agent was given enough episodes to start training, but its weights never changed")
        
        # ...and if we give it a BUNCH of samples that all say there's a positive reward with the same thing...
        # It SHOULD then make the optimal action to move up in the same situation!
        SAMPLE_SIZE = Constants.TARGET_UPDATE + Constants.BATCH_SIZE * 10
        for _ in range(SAMPLE_SIZE):
            agent.give_transition(MazeProblem(TINIEST_MAZE), "U", MazeProblem(FINISHED_TRANSITION), is_terminal=True)
            agent.give_terminal()
        
        # Now, make a new agent that _should_ load those weights trained from before and now chooses only
        # by exploit (i.e., no exploring possible, only greedy moves)
        agent = PacmanAgent(TINIEST_MAZE, is_training=False, fresh_start=False)
        mp = MazeProblem(TINIEST_MAZE)
        self.assertEqual("U", agent.choose_action(mp, dict(mp.legal_actions(mp.get_player_loc()))), "[X] Your agent had enough episodes rewarding it for moving up in this scenario to know that moving up is good")
        
        # Lastly, just make sure that when training is turned off, your weights are not changing too
        og_params = str(agent.policy_net.state_dict())
        for _ in range(Constants.BATCH_SIZE * 3):
            agent.give_transition(MazeProblem(TINIEST_MAZE), "U", MazeProblem(FINISHED_TRANSITION), is_terminal=False)
        self.assertEqual(str(agent.policy_net.state_dict()), og_params, "[X] Your agent should not adjust its weights when the constructor's is_training parameter is given False")
    
    def test_pacman_agent_full_training_basic(self) -> None:
        # Time to spin it up on the real deal!
        Constants.PARAM_PATH = "./dat/params_test_training_basic.pth"
        Constants.MEM_PATH = "./dat/mem_test_training_basic.pkl"
        agent = PacmanAgent(BASIC_MAZE, is_training=True, fresh_start=True)
        results = run_training_loop(maze=BASIC_MAZE, n_games=200, verbose=False, gui=False, agent=agent, sim_name="training_basic_sim")
        self.assertLess(0.95, results["pell_ema"], "[X] Your agent should be eating all of the pellets consistently after this much training")
        self.assertLess(0.95, results["win_ema"], "[X] Your agent should be winning consistently after this much training")
        self.assertGreater(0.12, results["move_ema"], "[X] Your agent is taking too many moves to win")
    
    def test_pacman_agent_full_training_ghost(self) -> None:
        # Ready to face your ghosts?
        Constants.PARAM_PATH = "./dat/params_test_training_ghost.pth"
        Constants.MEM_PATH = "./dat/mem_test_training_ghost.pkl"
        agent = PacmanAgent(GHOST_MAZE, is_training=True, fresh_start=True)
        results = run_training_loop(maze=GHOST_MAZE, n_games=4000, verbose=False, gui=False, agent=agent, sim_name="training_ghost_sim")
        # Note: lesser requirements for pellet and move EMA because of difficult maze during training
        # wherein even a single wrong exploration will send your agent asunder! The deployment tests that
        # follow will test without exploration
        self.assertLess(0.5, results["pell_ema"], "[X] Your agent should be eating all of the pellets consistently after this much training")
        self.assertGreater(0.20, results["move_ema"], "[X] Your agent is taking too many moves to win")
        
    def test_pacman_agent_full_deployment_basic(self) -> None:
        Constants.PARAM_PATH = "./dat/params_pellets_final.pth"
        Constants.MEM_PATH = "./dat/mem_test_deployment_basic.pkl"
        agent = PacmanAgent(BASIC_MAZE, is_training=False, fresh_start=False)
        results = run_training_loop(maze=BASIC_MAZE, n_games=50, verbose=False, gui=False, agent=agent, sim_name="deployment_basic_sim")
        self.assertLess(0.95, results["pell_ema"], "[X] Your agent should be eating all of the pellets consistently after this much training")
        self.assertLess(0.95, results["win_ema"], "[X] Your agent should be winning consistently after this much training")
        self.assertGreater(0.12, results["move_ema"], "[X] Your agent is taking too many moves to win")
        
    def test_pacman_agent_full_deployment_ghost(self) -> None:
        # Ready to face your ghosts?
        Constants.PARAM_PATH = "./dat/params_ghosty_final.pth"
        Constants.MEM_PATH = "./dat/mem_test_training_ghost.pkl"
        agent = PacmanAgent(GHOST_MAZE, is_training=False, fresh_start=False)
        results = run_training_loop(maze=GHOST_MAZE, n_games=50, verbose=False, gui=False, agent=agent, sim_name="deployment_ghost_sim")
        self.assertLess(0.9, results["pell_ema"], "[X] Your agent should be eating all of the pellets consistently after this much training")
        self.assertLess(0.9, results["win_ema"], "[X] Your agent should be winning consistently after this much training")
        self.assertGreater(0.20, results["move_ema"], "[X] Your agent is taking too many moves to win")
        
if __name__ == '__main__':
    unittest.main()
