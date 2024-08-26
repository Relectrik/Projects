from pgmpy.models import BayesianNetwork # type: ignore
from pgmpy.factors.discrete import TabularCPD # type: ignore
from pgmpy.sampling import BayesianModelSampling # type: ignore
from pgmpy.factors.discrete import State
from pgmpy.inference import VariableElimination # type: ignore
import pandas as pd
import numpy as np
import itertools
import os

class SimModel:
    
    def __init__(self, model: "BayesianNetwork", dec_vars: list[str], outcome_vars: list[str], name: str="SimModel"):
        '''
        Creates a new Simulation Model that is used to determine relationships and sampled outcomes
        between the given decision variables, outcome variables, and covariates (= every other variable
        in the model that isn't a decision nor outcome).
        
        Parameters:
            model (BayesianNetwork):
                pgmpy Bayesian Network used to perform the sampling of any variables in the system
            dec_vars (list[str]):
                The decision variables that the agent will choose values from at each trial
            outcome_vars (list[str]):
                The outcome variables that the agent will receive feedback on after choosing at each trial
            name (str):
                The name of this simulation model such that if pre-generated samples are available
                for it to speed up the simulation, will search the /dat/ subdirectory for files named:
                name + "_samples.csv"
        '''
        self.name = name
        self.model = model
        self.dec_vars = dec_vars
        self.dec_cards = [model.get_cpds(dec).variable_card for dec in dec_vars]
        self.outcome_vars = outcome_vars
        self.covariates = [cpd.variable for cpd in model.get_cpds() if cpd.variable not in dec_vars + outcome_vars]
        self.sampler = BayesianModelSampling(model)
        self.inference = VariableElimination(model)
        self.optimal_choices: dict[frozenset, tuple[dict[str, int], float]] = dict()
        self.reward_dists: dict[frozenset, list[float]] = dict()
        
        # If pregenerated context samples are available, the sim will run considerably quicker
        self.pregen_samples = None
        path = "./dat/" + name + "_samples.csv"
        if os.path.isfile(path):
            self.pregen_samples = pd.read_csv(path)
    
    def _get_dec_combos(self) -> list[tuple[str, int]]:
        '''
        Helper to return all combinations of decision variables and their assigned values, useful for
        iterating over all possibilities.
        
        Returns:
            Generator for: list[tuple[str, int]]:
                Generator for list of variable-action tuples in the decision dictionary's items() 
        '''
        dec_vals = [list(range(card)) for card in self.dec_cards]
        # Open mypy bug: error in returned type for itertools product with repeat arg
        return itertools.product(*dec_vals) # type: ignore
    
    def _get_state_from_dict(self, evidence: dict[str, int]) -> list[State]:
        '''
        Returns a pgmpy State representing an evidence assignment used in the sampling methods.
        
        Returns:
            list[State]:
                List of State variables like State("X", 0) for when variable X = 0
        '''
        return [State(key, val) for key, val in evidence.items()]
    
    def get_covariate_sample(self) -> dict[str, int]:
        '''
        Returns a sample of this model's covariates, viz., any variable that is neither decision
        nor outcome, assumed to all be pre-treatment, pre-outcome variables (i.e., not descendants
        of either).
        
        Returns:
            dict[str, int]:
                Possible dictionary of state variables as sampled from the network, e.g.,
                {"Z": 0, "W": 1}
        '''
        if len(self.covariates) == 0:
            return dict()
        sample: dict[str, int] = self.sampler.forward_sample(size=1, show_progress=False)[self.covariates].to_dict("index")[0] if self.pregen_samples is None else self.pregen_samples.sample(n=1, ignore_index=True).to_dict("index")[0]
        return sample
    
    def _get_reward_dist(self, evidence: dict[str, int], frozen_ev: frozenset) -> list[float]:
        '''
        Helper to return the reward distribution associated with the given evidence, which
        consists of the union of choice variables x_t and covariates z_t.
        
        [!] In future causality-related lessons, will need to separate these!
        
        Parameters:
            evidence: dict[str, int]:
                The combined evidence dictionary consisting of {**x_t, **z_t}
            frozen_ev: frozenset:
                The frozenset version of evidence, useful for checking cached computations
        
        Returns:
            list[float]:
                The probability distribution P(Y_t | x_t, z_t), e.g., if there was
                an 80% likelihood of winning with chosen action x_t and covariates z_t:
                Y =  0    1
                    [0.2, 0.8]
        '''
        result: list[float] = self.inference.query(variables=self.outcome_vars, evidence=evidence, show_progress=False).values
        self.reward_dists[frozen_ev] = result
        return result
    
    def get_outcome_sample(self, choice: dict[str, int], covariates: dict[str, int]) -> dict[str, int]:
        '''
        Given the pre-choice covariates z_t and chosen action x_t, returns a sample of the outcome
        variable y_t consistent with the distribution P(Y_t | x_t, z_t)
        
        Parameters:
            choice (dict[str, int]):
                Dictionary mapping each decision variable to its elected choice value
            covariates (dict[str, int]):
                Dictionary mapping each context variable to its value for this outcome sample
        
        Returns:
            dict[str, int]:
                Outcome variable Y mapped to its sampled value given the choice and corresponding covariates
        '''
        new_ev = {**choice, **covariates}
        frozen_ev = frozenset(new_ev.items())
        reward_dist = self.reward_dists[frozen_ev] if frozen_ev in self.reward_dists else self._get_reward_dist(new_ev, frozen_ev)
        sample = np.random.choice([0, 1], p=reward_dist)
        return {"Y": sample}
    
    def get_optimal_choice(self, covariates: dict[str, int]) -> tuple[dict[str, int], float]:
        '''
        Given the current state of covariates (if any), determines what the analytical optimal
        action would be that maximizes reward chance.
        
        Parameters:
            covariates (dict[str, int]):
                Current state of any covariates mapped to their values
        
        Returns:
            tuple[dict[str, int], float]:
                dict[str, int]:
                    The best action combination for the given covariates, e.g., {"X": 1}
                float:
                    The expected reward associated with that best action
        '''
        frozen_covariates = frozenset(covariates.items())
        if frozen_covariates in self.optimal_choices:
            return self.optimal_choices[frozen_covariates]
        
        dec_combos = self._get_dec_combos()
        best_combo, best_score = None, -float("inf")
        for combo in dec_combos:
            dec_dict = {dec: combo[ind] for ind, dec in enumerate(self.dec_vars)}
            new_ev = {**dec_dict, **covariates}
            query = self.inference.query(variables=self.outcome_vars, evidence=new_ev)
            outcome_prob = query.values[1]
            if outcome_prob > best_score:
                best_combo, best_score = dec_dict, outcome_prob
        
        # See note on _get_dec_combos re: mypy bug ignored here
        self.optimal_choices[frozen_covariates] = (best_combo, best_score) # type: ignore
        return (best_combo, best_score) # type: ignore
