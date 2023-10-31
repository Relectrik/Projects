"""
ad_engine.py
Advertisement Selection Engine that employs a Decision Network
to Maximize Expected Utility associated with different Decision
variables in a stochastic reasoning environment.

Solution Amended from Legendary N2A Team
> Warning: not a great amendment: was just playing with some
  settings to get the new pgmpy library working
"""
import itertools
import pandas as pd
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


class AdEngine:
    def __init__(
        self,
        data: "pd.DataFrame",
        structure: list[tuple[str, str]],
        dec_vars: list[str],
        util_map: dict[str, dict[int, int]],
    ):
        """
        Responsible for initializing the Decision Network of the
        AdEngine by taking in the dataset, structure of network,
        any decision variables, and a map of utilities

        Parameters:
            data (pd.DataFrame):
                Pandas data frame containing all data on which the decision
                network's chance-node parameters are to be learned
            structure (list[tuple[str, str]]):
                The Bayesian Network's structure, a list of tuples denoting
                the edge directions where each tuple is (parent, child)
            dec_vars (list[str]):
                list of string names of variables to be
                considered decision variables for the agent. Example:
                ["Ad1", "Ad2"]
            util_map (dict[str, dict[int, int]]):
                Discrete, tabular, utility map whose keys
                are variables in network that are parents of a utility node, and
                values are dictionaries mapping that variable's values to a utility
                score, for example:
                  {
                    "X": {0: 20, 1: -10}
                  }
                represents a utility node with single parent X whose value of 0
                has a utility score of 20, and value 1 has a utility score of -10
        """
        self.data: "pd.DataFrame" = data
        self.network: "BayesianNetwork" = BayesianNetwork(structure)
        self.network.fit(data)
        self.exact_inf: "VariableElimination" = VariableElimination(self.network)

        self.util_map: dict[str, dict[int, int]] = util_map

        self.dec_nodes: set[str] = set(dec_vars)
        self.util_nodes: set[str] = set(util_map.keys())
        self.nodes: set[str] = set(data.columns) - self.dec_nodes

    def meu(self, evidence: dict[str, int]) -> tuple[dict[str, int], float]:
        """
        Computes the Maximum Expected Utility (MEU) defined as the choice of
        decision variable values that maximize expected utility of any evaluated
        chance nodes given in the agent's utility map.

        Parameters:
            evidence (dict[str, int]):
                dict mapping network variables to their observed values,
                of the format: {"Obs1": val1, "Obs2": val2, ...}

        Returns:
            tuple[dict[str, int], float]:
                A 2-tuple of the format (a*, MEU) where:
                [0] is a dictionary mapping decision variables to their MEU states
                [1] is the MEU value (a float) of that decision combo
        """

        curr_a_star: dict[str, int] = {}
        curr_meu: float = -1.0

        for decisions in self.get_dec_combos():
            eu: float = self.eu({**evidence, **decisions})

            if eu > curr_meu:
                curr_a_star = decisions
                curr_meu = eu

        return (curr_a_star, curr_meu)

    def vpi(self, potential_evidence: str, observed_evidence: dict[str, int]) -> float:
        """
        Given some observed demographic "evidence" about a potential
        consumer, returns the Value of Perfect Information (VPI)
        that would be received on the given "potential" evidence about
        that consumer.

        Parameters:
            potential_evidence (str):
                string representing the variable name of the variable
                under consideration for potentially being obtained
            observed_evidence (tuple[dict[str, int], float]):
                dict mapping network variables
                to their observed values, of the format:
                {"Obs1": val1, "Obs2": val2, ...}

        Returns:
            float:
                float value indicating the VPI(potential | observed)
        """

        curr_meu: float = self.meu(observed_evidence)[1]
        new_meu: float = 0.0

        for possibility in sorted(self.data[potential_evidence].unique()):
            new_meu += (
                self.meu({**observed_evidence, potential_evidence: possibility})[1]
                * self.exact_inf.query(
                    variables={potential_evidence: possibility},
                    evidence=observed_evidence,
                ).values[possibility]
            )

        return 0 if ((new_meu - curr_meu) < 0) else (new_meu - curr_meu)

    def most_likely_consumer(self, evidence: dict[str, int]) -> dict[str, int]:
        """
        Given some known traits about a particular consumer, makes the best guess
        of the values of any remaining hidden variables and returns the completed
        data point as a dictionary of variables mapped to their most likely values.
        (Observed evidence will always have the same values in the output).

        Parameters:
            evidence (dict[str, int]):
                dict mapping network variables
                to their observed values, of the format:
                {"Obs1": val1, "Obs2": val2, ...}

        Returns:
            dict[str, int]:
                The most likely values of all variables given what's already
                known about the consumer.
        """

        return {
            **self.exact_inf.map_query(
                [
                    variable
                    for variable in self.nodes
                    if variable not in evidence.keys()
                ],
                evidence,
            ),
            **evidence,
        }

    # Helper methods
    def get_dec_combos(self) -> list[dict[str, int]]:
        """
        Helper method that returns all possible value combinations of the variables in
        self.dec_nodes. Does not have parameters because it accesses self.dec_nodes
        and self.data directly.

        Returns:
            list[dict[str, int]]:
                A list containing all combinations of decision node variables.
                Each combination is stored as a dictionary that maps the decision
                variable to its value.
        """
        return [
            dict(zip(self.dec_nodes, combo))
            for combo in itertools.product(
                *[sorted(self.data[decision].unique()) for decision in self.dec_nodes]
            )
        ]

    def eu(self, evidence: dict[str, int]) -> float:
        """
        Helper method to calculate the expected utility given some evidence.

        Args:
            evidence (dict[str, int]): The known evidence variables, passed in from meu().

        Returns:
            float: The calculated estimated utility value.
        """
        jpt = self.exact_inf.query(self.util_nodes, evidence=evidence)

        total_utility = 0
        for node in self.util_nodes:
            for outcome in self.util_map[node]:
                total_utility += jpt.values[outcome] * self.util_map[node][outcome]

        return total_utility
