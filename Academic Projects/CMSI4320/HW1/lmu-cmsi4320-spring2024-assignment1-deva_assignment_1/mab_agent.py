"""
mab_agent.py

Agent specifications implementing Action Selection Rules covered
during the lectures... plus some opportunities to explore your
implementations!
"""

import numpy as np
import random
import itertools
import random

# ----------------------------------------------------------------
# MAB Agent Superclasses
# ----------------------------------------------------------------


class MABAgent:
    """
    MAB Agent superclass designed to abstract common components
    between individual bandit player subclasses (below)
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int]):
        """
        Initializes a new MABAgent given the list of decision variables it must choose
        at each round, and their corresponding cardinalities (i.e., how many values each
        has). Use this to initialize any attributes needed.

        Parameters:
            dec_vars (list[str]):
                The list of decision variables that your agent must choose from at
                each round of the MAB game
            dec_cards (list[int]):
                The list of decision variable cardinalities (i.e., how many values
                the variable can obtain through your choice), with each index
                corresponding to the variable's index in dec_vars

        [!] Each decision variable has choices in the range of their cardinality, e.g.,
        dec_vars =  ["X1", "X2"]
        dec_cards = [2, 4]
        => X1 has values {0, 1} and X2 has values {0, 1, 2, 3}

        [!] WARNING: For any given simulation, an agent is created ONCE and persists
        for ALL Monte Carlo repetitions, but will have its clear_history method called
        between rounds. Your agent should not remember anything between Monte Carlo
        repetitions.
        """
        self.dec_vars: list[str] = dec_vars
        self.dec_cards: list[int] = dec_cards
        self.history: dict[frozenset[tuple[str, int]], list[int]] = {}
        self.clear_history()

    def _cardinality_combinations(self, cards: list[int]) -> list[tuple]:
        """
        Helper method for creating our agent's history field attribute.
        Calculates all possible combinations between the dec_vars cardinalities.
        Each index of the tuple corresponds to its respective dec_var.

        ![EXAMPLE]:
            Tuple with (0,0) represents X1: 0 and X2: 0.

        Returns:
            list[tuple]:
                A list of tuples of ints that contains all possible cardinality combinations.
                The size of tuples are respective to the length of self.dec_vars and self.dec_cards.

        """
        return list(itertools.product(*[range(card) for card in cards]))

    def _populate_history(self, card_combos: list[tuple], vars: list[str]) -> None:
        """
        Helper method that populates our agent's history dictionary. Each action will be initialized with one win
        and one loss to avoid issues with dividing by zero when calculating the quality of that action (Q_t(a))
        later on.

        Parameters:
            card_combos (list[tuple]):
                List of tuples of ints that contains all possible cardinality combinations.
        """
        for card_combo in card_combos:
            action: dict[str, int] = {
                var: choice for var, choice in zip(vars, card_combo)
            }
            # Initialized each arm to have one win and one loss
            self.history[frozenset(action.items())] = [1, 2]

    def give_feedback(self, a_t: dict[str, int], r_t: int) -> None:
        """
        After your agent's choice a_t has been made in a given trial t, this method
        is called by the environment to tell you if you received a reward r_t or not.
        Used to update your agent's history following its choices.

        Parameters:
            a_t (dict[str, int]):
                A decision mapping of variable mapped to its chosen value, e.g.,
                {"X": 0}
            r_t (int):
                The Bernoulli (i.e., {0, 1}) reward associated with your choice
                for this round.

        [!] This method is called FOR you and should never be called internally

        [!] It's up to YOU to determine your history's data structure and how it's updated
        """
        pre_quality: list[int] = self.history[frozenset(a_t.items())]
        self.history[frozenset(a_t.items())] = [
            pre_quality[0] + r_t,
            pre_quality[1] + 1,
        ]

    def give_contextual_feedback(
        self, a_t: dict[str, int], c_t: dict[str, int], r_t: int
    ) -> None:
        """
        See @give_feedback, with the single addition of one parameter for the
        Contextual MAB problem:

        Added Parameters:
            c_t (dict[str, int]):
                The map of context variables and their observed values that were
                provided to the contextual_choose method before your agent made its
                decision, e.g., {"Z": 0, "W": 1}

        In this method, c_t is given, which represent pre-action covariates available to
        the agent through which to make more situation-specific choices. In an advertising
        context, these might be attributes like c_t = {"age": 21, "home_state": 31, ...}
        Since these were provided when your agent made its choice, it should remember those
        in some way.

        In other words, this method would behave exactly the same as give_feedback if
        c_t were the empty dictionary, but I've tried having just this method in the past
        and it was too confusing, so here we are!
        """
        combined_dict: dict[str, int] = a_t.copy()
        combined_dict.update(c_t)
        pre_quality: list[int] = self.history[frozenset(combined_dict.items())]
        self.history[frozenset(combined_dict.items())] = [
            pre_quality[0] + r_t,
            pre_quality[1] + 1,
        ]

    def clear_history(self) -> None:
        """
        Resets your agent's history between simulations.

        [!] No information is allowed to transfer between each of the N
        Monte Carlo repetitions.

        [!] Called by the environment following a Monte Carlo repetition, but you
        MAY also call this method, e.g., during your constructor, or override it
        in subclasses below.
        """
        self.history = {}
        cards_combos = self._cardinality_combinations(self.dec_cards)
        self._populate_history(cards_combos, self.dec_vars)

    def choose(self) -> dict[str, int]:
        """
        The choose method is called by the environment when it is time for the agent to
        make a decision, i.e., a choice of values for each decision variable.

        [!] Default behavior for the MABAgent superclass when asked to provide a choice:
        simply chooses at random. Should be overridden in MABAgent subclasses depending
        on the Action Selection Rule being implemented.

        Returns:
            dict[str, int]:
                The decision map representing your agent's choice at the current round,
                e.g., {"X": 0}
        """
        return self._get_random_choice()

    def contextual_choose(self, c_t: dict[str, int]) -> dict[str, int]:
        """
        See @choose, but with the addition of a context mapping to provide the state of
        pre-choice variables c_t that may be relevant to your agent's decision.

        In this method, c_t represents pre-action covariates available to
        the agent through which to make more situation-specific choices. In an advertising
        context, these might be attributes like c_t = {"age": 21, "home_state": 31, ...}

        Added Parameters:
            c_t (dict[str, int]):
                The map of context variables and their observed values that were
                provided to the contextual_choose method before your agent makes its
                decision, e.g., {"Z": 0, "W": 1}
        """
        return self._get_random_choice()

    def _greedy_choose(
        self, ASR: str = "", hyperparameter: float = 0.0, c_t: dict[str, int] = {}
    ) -> dict[str, int]:
        """
        Implements different types of Action Selection Rules (ASRs) based on the given ASR.

        Parameters:
            ASR (str):
                Desired ASR to perform.
            hyperparameter (float):
                The C value for the Upper Confidence Bound formula that the Custom
                and Contextual Agents use.
            c_t (dict[str, int]):
                Used by the Contextual Agent to select the best action given this context.

        Returns:
            dict[str, int]:
                The best action returned by the desired ASR.
        """
        quality_dict: dict[frozenset[tuple[str, int]], float] = {}

        filtered_dict = {
            key: value
            for key, value in self.history.items()
            if all(c_t.get(item[0], item[1]) == item[1] for item in key)
        }

        for action, pre_quality in filtered_dict.items():
            match ASR:
                case "Thompson":
                    quality_dict[action] = np.random.beta(
                        pre_quality[0], pre_quality[1] - pre_quality[0]
                    )
                case "UCB":
                    quality_dict[action] = (
                        pre_quality[0] / pre_quality[1]
                    ) + hyperparameter * np.sqrt(
                        np.log(self._total_trials()) / pre_quality[1]
                    )
                case _:
                    quality_dict[action] = pre_quality[0] / pre_quality[1]

        max_quality = quality_dict[max(quality_dict, key=lambda x: quality_dict[x])]
        quality_actions: list[frozenset[tuple[str, int]]] = []

        for action, quality in quality_dict.items():
            if quality == max_quality:
                quality_actions.append(action)

        optimal_action = dict(quality_actions[random.randrange(len(quality_actions))])
        stripped_action = {
            key: var for key, var in optimal_action.items() if key in self.dec_vars
        }
        return stripped_action

    def _get_random_choice(self) -> dict[str, int]:
        """
        See @choose, this helper will return a random action from amongst those possible.
        """
        return {
            self.dec_vars[ind]: random.randrange(self.dec_cards[ind])
            for ind in range(len(self.dec_vars))
        }

    def _total_trials(self) -> int:
        total_trials: int = 0
        for action, reward_trial in self.history.items():
            total_trials += reward_trial[1]

        return total_trials


# ----------------------------------------------------------------
# MAB Agent Subclasses
# ----------------------------------------------------------------


class GreedyAgent(MABAgent):
    """
    Greedy bandit player that, at every trial, selects the
    arm with the presently-highest Q_t(a) value

    [!] Performs no exploration
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int]):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.
        """
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - The greedy ASR
        """
        return self._greedy_choose()


class EpsilonGreedyAgent(MABAgent):
    """
    Exploratory bandit player that makes the greedy choice with
    probability 1-epsilon, and chooses randomly with probability
    epsilon
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int], epsilon: float):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.

        Added Parameters from Superclass:
            epsilon (float):
                The probability that the agent takes an exploratory move rather than
                an exploitative one.
        """
        self.epsilon: float = epsilon
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - The epsilon-greedy ASR
        """
        if random.random() < self.epsilon:
            return self._get_random_choice()
        else:
            return self._greedy_choose()


class EpsilonFirstAgent(MABAgent):
    """
    Exploratory bandit player that takes the first epsilon*T
    trials to randomly explore, and thereafter chooses greedily
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int], explore_until_t: int):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.

        Added Parameters from Superclass:
            explore_until_t (int):
                The number of trials that this agent will spend exploring arms randomly
                before selecting arms greedily
        """
        self.explore_until_t: int = explore_until_t
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - The epsilon-first ASR
        """

        if self._total_trials() < self.explore_until_t:
            return self._get_random_choice()
        else:
            return self._greedy_choose()


class EpsilonDecreasingAgent(MABAgent):
    """
    Exploratory bandit player that acts like epsilon-greedy but
    with a decreasing value of epsilon over time
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int], decay_rate: float):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.

        Added Parameters from Superclass:
            decay_rate (float):
                The decay rate of this agent's exploration chance, such that after every
                trial, the decay rate decreases by this factor. E.g., a decay_rate of
                0.9 means that a current exploration chance of 0.9 will become 0.81 after
                this trial.
        """

        self.decay_rate: float = decay_rate
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - The epsilon-decreasing ASR
        """
        if random.random() < self.decay_rate ** self._total_trials():
            return self._get_random_choice()
        else:
            return self._greedy_choose()


class TSAgent(MABAgent):
    """
    Thompson Sampling bandit player that self-adjusts exploration
    vs. exploitation by sampling arm qualities from successes
    summarized by a corresponding beta distribution
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int]):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.
        """
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - The Thompson Sampling / Bayesian Update Rule ASR
        """
        return self._greedy_choose(ASR="Thompson")


class CustomAgent(MABAgent):
    """
    Custom agent that manages the explore vs. exploit dilemma via
    your own strategy, or by implementing a strategy you discovered
    that is not amongst those above!
    """

    def __init__(self, dec_vars: list[str], dec_cards: list[int]):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.
        """
        self.hyperparameter = 0.55
        MABAgent.__init__(self, dec_vars, dec_cards)

    def choose(self) -> dict[str, int]:
        """
        See @MABAgent.choose

        This particular subclass overriding of the choose method performs the following:
        - Your own custom MAB agent! OR
        - An implementation of an ASR that is not one of the above
        - Must outperform the Thompson Sampling agent on select unit tests
        """
        return self._greedy_choose(ASR="UCB", hyperparameter=self.hyperparameter)


class ContextualAgent(MABAgent):
    """
    Custom agent that plays the Contextual MAB game, accepting some
    context covariates c_t before each decision.

    [!] Still inherits from MABAgent, but you may wish to override
    parts of the superclass' constructor like the history attribute!
    """

    def __init__(
        self,
        dec_vars: list[str],
        dec_cards: list[int],
        context_vars: list[str],
        context_cards: list[int],
    ):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.

        Added Parameters from Superclass:
            context_vars (list[str]):
                A list of context variables that are available to the agent to make their
                decision at each trial, e.g., ["W", "S"]
            context_cards (list[int]):
                A list of variable cardinalities belonging to each context variable by
                index in which they appear in context_vars.
        """
        self.dec_vars: list[str] = dec_vars
        self.dec_cards: list[int] = dec_cards
        self.history: dict[frozenset[tuple[str, int]], list[int]] = {}
        self.context_vars: list[str] = context_vars
        self.context_cards: list[int] = context_cards

        self.hyperparameter = 0.55

        if len(self.context_cards) != len(self.context_vars):
            self.context_cards = self.context_cards * len(self.context_vars)

        self.clear_history()

    def clear_history(self) -> None:
        """
        Resets your agent's history between simulations.

        [!] No information is allowed to transfer between each of the N
        Monte Carlo repetitions.

        [!] Called by the environment following a Monte Carlo repetition, but you
        MAY also call this method, e.g., during your constructor, or override it
        in subclasses below.
        """
        self.history = {}
        self._populate_history(
            self._cardinality_combinations(self.dec_cards + self.context_cards),
            self.dec_vars + self.context_vars,
        )

    def contextual_choose(self, c_t: dict[str, int]) -> dict[str, int]:
        """
        See @MABAgent.contextual_choose
        """
        return self._greedy_choose(
            ASR="UCB", hyperparameter=self.hyperparameter, c_t=c_t
        )


class ContextBlindAgent(TSAgent):
    """
    [!] This agent is given as a "control" comparison for the contextual bandit
    problem and thus need/should NOT be modified.
    """

    def __init__(
        self,
        dec_vars: list[str],
        dec_cards: list[int],
        context_vars: list[str],
        context_cards: list[int],
    ):
        """
        See @MABAgent.__init__

        Can be used to initialize any other attributes needed for this agent's ASR.

        Added Parameters from Superclass:
            context_vars (list[str]):
                A list of context variables that are available to the agent to make their
                decision at each trial, e.g., ["W", "S"]
            context_cards (list[int]):
                A list of variable cardinalities belonging to each context variable by
                index in which they appear in context_vars.
        """
        TSAgent.__init__(self, dec_vars, dec_cards)

    def give_contextual_feedback(
        self, a_t: dict[str, int], c_t: dict[str, int], r_t: int
    ) -> None:
        """
        See @MABAgent.give_contextual_feedback
        """
        self.give_feedback(a_t, r_t)
