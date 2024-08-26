# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import mdp, util
from typing import *  # for the type hints
from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
    * Please read learningAgents.py before reading this.*

    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.
    """

    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount=0.9, iterations=100):
        """
        Your value iteration agent should take an mdp on
        construction, run the indicated number of iterations
        and then act according to the resulting policy.

        Some useful mdp methods you will use:
            mdp.getStates()
            mdp.getPossibleActions(state)
            mdp.getTransitionStatesAndProbs(state, action)
            mdp.getReward(state, action, nextState)
            mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self) -> None:
        """
        Run the value iteration algorithm. Note that in standard
        value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        states: list[tuple[int, int]] = self.mdp.getStates()
        for _ in range(self.iterations):
            current_values = util.Counter()
            for state in states:
                if self.mdp.isTerminal(state):
                    current_values[state] = 0.0
                    continue
                state_q_vals: list[float] = []
                for action in self.mdp.getPossibleActions(state):
                    state_q_val: float = self.computeQValueFromValues(state, action)
                    state_q_vals.append(state_q_val)
                current_values[state] = max(state_q_vals)
            self.values = current_values

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action) -> float:
        """
        Compute the Q-value of action in state from the
        value function stored in self.values.
        """
        transitions_and_probs: list[tuple[tuple[int, int], float]] = (
            self.mdp.getTransitionStatesAndProbs(state, action)
        )
        q_value: float = 0.0
        for next_state, probability in transitions_and_probs:
            immediate_reward: float = self.mdp.getReward(state, action, next_state)
            disocunted_prev_val: float = self.discount * self.values[next_state]
            q_value += probability * (immediate_reward + disocunted_prev_val)
        return q_value

    def computeActionFromValues(self, state) -> (str | None):
        """
        The policy is the best action in the given state
        according to the values currently stored in self.values.

        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None
        possible_actions: Sequence[str] = self.mdp.getPossibleActions(state)
        actions_mapped_to_vals: dict[str, float] = {
            action: self.computeQValueFromValues(state, action)
            for action in possible_actions
        }
        return max(actions_mapped_to_vals, key=lambda key : actions_mapped_to_vals[key])

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
