"""
Pacman Agent employing a PacNet trained in another module to
navigate perilous ghostly pellet mazes.
"""

import time
import random
import numpy as np
import torch
from os.path import exists
from torch import nn
from pathfinder import *
from queue import Queue
from constants import *
from reinforcement_trainer import *
from maze_problem import *


class PacmanAgent:
    """
    Deep learning Pacman agent that employs PacNet DQNs.
    """

    def __init__(
        self,
        maze: list[str],
        is_training: bool = Constants.TRAINING,
        fresh_start: bool = False,
    ):
        """
        Initializes the PacmanAgent with any attributes needed to make decisions;
        for the deep-learning implementation, this includes initializing the
        policy DQN (+ target DQN, ReplayMemory, and optimizer if training) and
        any other attributes needed to perform

        :maze: The maze on which this agent is to operate. Must be the same maze
        structure as the one on which this agent's model was trained.
        :is_training: Whether or not the agent is in training mode
        :fresh_start: Whether or not to load any previous parameters or memories;
        defaults to False, but can be set to True for testing
        """
        # [!] TODO: Problem 1
        self.step: int = 0
        self.maze: list[str] = maze
        self.policy_net: PacNet = PacNet(self.maze).to(Constants.DEVICE)
        if not fresh_start:
            self.policy_net.load()
        self.is_training: bool = is_training

        if is_training:
            self.memory: ReplayMemory = ReplayMemory()
            if len(self.memory) > 0 and not fresh_start:
                self.memory.load()
            self.target_net: PacNet = PacNet(self.maze).to(Constants.DEVICE)
            self.target_net.load_from_pacnet(self.policy_net)
            self.optimizer = torch.optim.AdamW(self.policy_net.parameters())
        return

    def choose_action(
        self, state: MazeProblem, legal_actions: dict[str, list[str]]
    ) -> str:
        """
        Returns an action from the options in Constants.MOVES based on the agent's
        perception (the current maze) and legal actions available. If training,
        must manage the explore vs. exploit dilemma through some form of ASR.

        :state: The current maze state in which to act
        :legal_actions: Map of legal actions to their next agent states
        :return: Action choice from the set (i.e., keys) of legal_actions
        """
        # [!] TODO: Problem 2
        float_maze = ReplayMemory.vectorize_maze(state.get_maze()).to(Constants.DEVICE)
        float_maze = float_maze.unsqueeze(0)
        movesRanked = {}
        legal_indices = [Constants.MOVES.index(i) for i in legal_actions.keys()]
        epsilon = .2 if Constants.GAMES_RUN < 200 else Constants.EPS_GREEDY ** (Constants.GAMES_RUN /3)
        if self.is_training:
            if random.random() < epsilon:
                return random.choice(list(legal_actions.keys()))
            else:
                with torch.no_grad():
                    for i in legal_indices:
                        movesRanked[Constants.MOVES[i]] = self.policy_net(float_maze)[
                            0
                        ][i]
                    return max(movesRanked, key=movesRanked.get)
        else:
            with torch.no_grad():
                for i in legal_indices:
                    movesRanked[Constants.MOVES[i]] = self.policy_net(float_maze)[0][i]
                return max(movesRanked, key=movesRanked.get)

    def get_reward(
        self, state: MazeProblem, action: str, next_state: MazeProblem
    ) -> float:
        """
        The reward function that determines the numerical desirability of the
        given transition from state -> next_state with the chosen action.

        :state: state at which the transition begun
        :action: the action the agent chose from state
        :next_state: the state at which the agent began its next turn
        :returns: R(s, a, s') for the given transition
        """
        # [!] TODO: Problem 3
        if next_state.get_win_state():
            return 1.0
        elif next_state.get_death_state():
            return -1.0
        elif next_state.get_timeout_state():
            return -1.0
        elif len(state.get_pellets()) > len(next_state.get_pellets()):
            return 0.15
        else:
            return -0.06

    def give_transition(
        self,
        state: MazeProblem,
        action: str,
        next_state: MazeProblem,
        is_terminal: bool,
    ) -> None:
        """
        Called by the Environment after both Pacman and ghosts have moved on a
        given turn, supplying the transition that was observed, which can then
        be added to the training agent's memory and the model optimized. Also
        responsible for periodically updating the target network.

        [!] If not training, this method should do nothing (and simply return).

        :state: state at which the transition begun
        :action: the action the agent chose from state
        :next_state: the state at which the agent began its next turn
        :is_terminal: whether or not next_state is a terminal state
        """
        # [!] TODO: Problem 4
        if self.is_training:
            self.step += 1
            reward = self.get_reward(state, action, next_state)
            self.memory.push(state, action, next_state, reward, is_terminal)
            self.optimize_model()
            if self.step % Constants.TARGET_UPDATE == 0:
                print("target net updated")
                self.target_net.load_from_pacnet(self.policy_net)
        return
        

    def give_terminal(self) -> None:
        """
        Called by the Environment upon reaching any of the terminal states:
          - Winning (eating all of the pellets)
          - Dying (getting eaten by a ghost)
          - Timing out (taking more than Constants.MAX_MOVES number of turns)
        Useful for cleaning up fields, saving weights and memories to disk if
        desired, etc.

        [!] If not training, this method should do nothing (and simply return).

        [!] You DO NOT need to modify this method; it works as-is
        """
        if not self.is_training:
            return
        if Constants.GAMES_RUN % Constants.SAVE_AFTER_N_GAMES == 0:
            if Constants.VERBOSE:
                print(
                    "\n[...] Checkpoint! Saving policy net weights and replay memory..."
                )
            self.policy_net.save()
            self.memory.save()
            if Constants.VERBOSE:
                print("[>>>] Saving complete!\n")
        Constants.GAMES_RUN += 1

    def optimize_model(self) -> None:
        """
        Primary workhorse for training the policy DQN. Samples a mini-batch of
        episodes from the ReplayMemory and then takes a step of the optimizer
        to train the DQN weights.

        [!] If not training OR fewer episodes than Constants.BATCH_SIZE have
        been recorded, this method should do nothing (and simply return).
        """
        # [!] TODO: Problem 5
        if not self.is_training or Constants.BATCH_SIZE > len(self.memory):
            return
        samples = self.memory.sample(Constants.BATCH_SIZE)
        batched_samples = Episode(*zip(*samples))

        batch_states = torch.cat([ReplayMemory.vectorize_maze(s.get_maze()).unsqueeze(0).to(Constants.DEVICE) for s in batched_samples.state]).to(Constants.DEVICE)
        batch_actions = torch.stack([torch.tensor(Constants.MOVES.index(a), dtype=int, device=Constants.DEVICE).unsqueeze(0) for a in batched_samples.action]).to(Constants.DEVICE)
        s_a_values = self.policy_net(batch_states).gather(1, batch_actions)

        batch_next_states = torch.cat([ReplayMemory.vectorize_maze(ns.get_maze()).unsqueeze(0).to(Constants.DEVICE) for ns, is_terminal in zip(batched_samples.next_state, batched_samples.is_terminal) if not is_terminal ]).to(Constants.DEVICE)
        batch_rewards = torch.stack([torch.tensor(r, device=Constants.DEVICE) for r in batched_samples.reward]).to(Constants.DEVICE)

        non_term_next_state_mask = torch.cat([torch.tensor(not t, dtype=torch.bool, device=Constants.DEVICE).unsqueeze(0) for t in batched_samples.is_terminal])
        next_state_values = torch.zeros(Constants.BATCH_SIZE).to(Constants.DEVICE)
        with torch.no_grad():
            next_state_values[non_term_next_state_mask] = self.target_net(batch_next_states).max(1).values.to(Constants.DEVICE)
        expected_s_a_vals = (next_state_values * Constants.GAMMA) + batch_rewards

        criterion = nn.SmoothL1Loss()
        loss = criterion(s_a_values, expected_s_a_vals.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()

        self.optimizer.step()
