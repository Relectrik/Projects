from pgmpy.models import BayesianNetwork # type: ignore
from pgmpy.factors.discrete import TabularCPD # type: ignore
import unittest
import pytest
from mab_sim import *
from statistics import mean

# ----------------------------------------------------------------
# Simulation Constants
# ----------------------------------------------------------------

# Set to True to see generated graphs / terminal output
VERBOSE = True
N = 1000
T = 1000

RND_ERR = "[X] For greedy moves, your agent must break ties in highest action-value at random"
REG_ERR = "[X] Your agent's cumulative regret should be near the threshold"
OPT_ERR = "[X] Your agent's probability of optimal action should be near this threshold"


# ----------------------------------------------------------------
# Simulation Helper Methods
# ----------------------------------------------------------------

def get_simple_sim() -> tuple[SimModel, list[str], list[int], list[str]]:
    '''
    Returns the simple sim Bayesian Network with only decision X and outcome Y,
    and regularly spaced reward distribution.
    
    Returns:
        tuple[SimModel, list[str], list[int], list[str]]:
            SimModel:
                The Bayesian Network encoding this simulation environment
            list[str]:
                The list of decision variable names
            list[int]:
                The list of decision variable cardinalities
            list[str]:
                The list of outcome variables (assumed to be just Y for this assignment)
    '''
    dec_vars = ["X"]
    dec_card = [4]
    out_vars = ["Y"]
    simple_sim = BayesianNetwork([('X', 'Y')])
    x_dist = TabularCPD('X', 4, [[0.25], [0.25], [0.25], [0.25]])
    y_dist = TabularCPD('Y', 2, 
                    # X = 0    1    2    3
                        [[0.4, 0.6, 0.3, 0.5], 
                         [0.6, 0.4, 0.7, 0.5]],
                        dec_vars, dec_card)
    
    simple_sim.add_cpds(x_dist, y_dist)
    
    sim_model = SimModel(simple_sim, dec_vars, out_vars, name="simple_sim")
    return sim_model, dec_vars, dec_card, out_vars

def get_simple_context_sim() -> tuple[SimModel, list[str], list[int], list[str], list[int], list[str]]:
    '''
    Returns the simplest contextual sim Bayesian Network with decision X, outcome Y,
    and context variable Z.
    
    Returns:
        tuple[SimModel, list[str], list[int], list[str]]:
            SimModel:
                The Bayesian Network encoding this simulation environment
            list[str]:
                The list of decision variable names
            list[int]:
                The list of decision variable cardinalities
            list[str]:
                The list of context variable names
            list[int]:
                The list of context variable cardinalities
            list[str]:
                The list of outcome variables (assumed to be just Y for this assignment)
    '''
    dec_vars = ["X"]
    dec_card = [2]
    context_vars = ["Z"]
    context_card = [2]
    out_vars = ["Y"]
    simple_context_sim = BayesianNetwork([('Z', 'X'), ('Z', 'Y'), ('X', 'Y')])
    z_dist = TabularCPD('Z', 2, [[0.5], [0.5]])
    x_dist = TabularCPD('X', 2,
                    # Z = 0     1
                        [[0.75, 0.4],
                         [0.25, 0.6]],
                         context_vars, context_card)
    y_dist = TabularCPD('Y', 2, 
                    # X = 0    0    1    1
                    # Z = 0    1    0    1
                        [[0.4, 0.6, 0.7, 0.5], 
                         [0.6, 0.4, 0.3, 0.5]],
                        dec_vars + context_vars, dec_card + context_card)
    
    simple_context_sim.add_cpds(z_dist, x_dist, y_dist)
    
    sim_model = SimModel(simple_context_sim, dec_vars, out_vars, name="simple_context_sim")
    return sim_model, dec_vars, dec_card, context_vars, context_card, out_vars

def get_advanced_context_sim() -> tuple[SimModel, list[str], list[int], list[str], list[int], list[str]]:
    '''
    Returns a more advanced contextual sim Bayesian Network with decision X, outcome Y,
    and context variables S, R, W, Z.
    
    Returns:
        tuple[SimModel, list[str], list[int], list[str]]:
            SimModel:
                The Bayesian Network encoding this simulation environment
            list[str]:
                The list of decision variable names
            list[int]:
                The list of decision variable cardinalities
            list[str]:
                The list of context variable names
            list[int]:
                The list of context variable cardinalities
            list[str]:
                The list of outcome variables (assumed to be just Y for this assignment)
    '''
    dec_vars = ["X"]
    dec_card = [2]
    context_vars = ["S", "R", "W", "Z"]
    context_card = [2]
    out_vars = ["Y"]
    simple_context_sim = BayesianNetwork([('Z', 'X'), ('R', 'X'), ('Z', 'Y'), ('S', 'Y'), ('W', 'Z'), ('W', 'S'), ('X', 'Y')])
    r_dist = TabularCPD('R', 2, [[0.3], [0.7]])
    w_dist = TabularCPD('W', 2, [[0.6], [0.4]])
    z_dist = TabularCPD('Z', 2,
                    # W = 0     1
                        [[0.75, 0.4],
                         [0.25, 0.6]],
                         ["W"], context_card)
    s_dist = TabularCPD('S', 2,
                    # W = 0     1
                        [[0.5, 0.2],
                         [0.5, 0.8]],
                         ["W"], context_card)
    x_dist = TabularCPD('X', 2,
                    # R = 0    0    1    1
                    # Z = 0    1    0    1
                        [[0.4, 0.6, 0.7, 0.5], 
                         [0.6, 0.4, 0.3, 0.5]],
                         ["R", "Z"], context_card*2)
    y_dist = TabularCPD('Y', 2, 
                    # X = 0    0    0    0    1    1    1    1
                    # Z = 0    0    1    1    0    0    1    1
                    # S = 0    1    0    1    0    1    0    1
                        [[0.4, 0.8, 0.5, 0.1, 0.7, 0.1, 0.3, 0.5], 
                         [0.6, 0.2, 0.5, 0.9, 0.3, 0.9, 0.7, 0.5]],
                        ["X", "Z", "S"], context_card*3)
    
    simple_context_sim.add_cpds(w_dist, r_dist, s_dist, z_dist, x_dist, y_dist)
    
    sim_model = SimModel(simple_context_sim, dec_vars, out_vars, name="advanced_context_sim")
    return sim_model, dec_vars, dec_card, context_vars, context_card, out_vars


# ----------------------------------------------------------------
# Unit Tests
# ----------------------------------------------------------------

class MABTests(unittest.TestCase):
    """
    Unit tests for validating the MAB agent functionality. Notes:
    - If this is the set of tests provided in the solution skeleton, it represents an
      incomplete set that you are expected to add to to adequately test your submission!
    - Your correctness score on the assignment will be assessed by a more complete,
      grading set of unit tests.
    - A portion of your style grade will also come from proper type hints; remember to
      validate your submission using `mypy .` and ensure that no issues are found.
    """
    
    def test_mab_agents_greedy_random(self) -> None:
        '''
        Ensures that the greedy choice breaks ties in highest action-value
        at random, since all arms at the first choice will always have
        equal value. 
        '''
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                GreedyAgent(dec_vars, dec_card)
            ],
            agent_names = [
                "Greedy"
            ],
            sim_model = sim_model,
            N = N,
            T = 1,
            SIM_NAME = self._testMethodName,
            verbose = False,
            contexts = False
        )
        self.assertAlmostEqual(0.25, cum_opt[0][-1], delta=0.05, msg=RND_ERR)
        
    def test_mab_agents_greedy_full(self) -> None:
        '''
        Tests the greedy agent's ability to get lucky with its "exploration"
        but will, on average, fail to converge to the optimal action since it
        has no real exploration policy
        '''
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                GreedyAgent(dec_vars, dec_card)
            ],
            agent_names = [
                "Greedy"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        self.assertAlmostEqual(60, cum_reg[0][-1], delta=10, msg=REG_ERR)
        self.assertAlmostEqual(0.58, cum_opt[0][-1], delta=0.05, msg=OPT_ERR)
    
    def test_mab_agents_epsilon_greedy_random(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                EpsilonGreedyAgent(dec_vars, dec_card, 0.10)
            ],
            agent_names = [
                "e-Greedy, e=0.10"
            ],
            sim_model = sim_model,
            N = N,
            T = 1,
            SIM_NAME = self._testMethodName,
            verbose = False,
            contexts = False
        )
        self.assertAlmostEqual(0.25, cum_opt[0][-1], delta=0.05, msg=RND_ERR)
    
    def test_mab_agents_epsilon_greedy_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                EpsilonGreedyAgent(dec_vars, dec_card, 0.02),
                EpsilonGreedyAgent(dec_vars, dec_card, 0.05),
                EpsilonGreedyAgent(dec_vars, dec_card, 0.15),
                EpsilonGreedyAgent(dec_vars, dec_card, 0.25)
            ],
            agent_names = [
                "e-Greedy, e=0.02",
                "e-Greedy, e=0.05",
                "e-Greedy, e=0.15",
                "e-Greedy, e=0.25"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        # Performance of the e=0.02 agent
        self.assertAlmostEqual(0.75, cum_opt[0][-1], delta=0.05, msg=OPT_ERR)
        # Performance of the e=0.05 agent, by contrast!
        self.assertAlmostEqual(0.82, cum_opt[1][-1], delta=0.05, msg=OPT_ERR)
        
    def test_mab_agents_epsilon_first_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                EpsilonFirstAgent(dec_vars, dec_card, 10),
                EpsilonFirstAgent(dec_vars, dec_card, 50),
                EpsilonFirstAgent(dec_vars, dec_card, 100),
                EpsilonFirstAgent(dec_vars, dec_card, 200)
            ],
            agent_names = [
                "e-First, e=10",
                "e-First, e=50",
                "e-First, e=100",
                "e-First, e=200"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        # Performance of the e=50 agent
        self.assertAlmostEqual(0.83, cum_opt[1][-1], delta=0.10, msg=OPT_ERR)
        self.assertAlmostEqual(27, cum_reg[1][-1], delta=10, msg=REG_ERR)
        # Performance of the e=100 agent
        self.assertAlmostEqual(0.82, cum_opt[2][-1], delta=0.10, msg=OPT_ERR)
        self.assertAlmostEqual(27, cum_reg[2][-1], delta=10, msg=REG_ERR)
        
    def test_mab_agents_epsilon_decreasing_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                EpsilonDecreasingAgent(dec_vars, dec_card, 0.995),
                EpsilonDecreasingAgent(dec_vars, dec_card, 0.992),
                EpsilonDecreasingAgent(dec_vars, dec_card, 0.990),
                EpsilonDecreasingAgent(dec_vars, dec_card, 0.985)
            ],
            agent_names = [
                "e-Decreasing, decay=0.995",
                "e-Decreasing, decay=0.992",
                "e-Decreasing, decay=0.990",
                "e-Decreasing, decay=0.985",
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        self.assertAlmostEqual(0.91, cum_opt[1][-1], delta=0.05, msg=OPT_ERR)
        self.assertAlmostEqual(25, cum_reg[1][-1], delta=8, msg=REG_ERR)
        self.assertAlmostEqual(0.91, cum_opt[2][-1], delta=0.05, msg=OPT_ERR)
        self.assertAlmostEqual(25, cum_reg[2][-1], delta=8, msg=REG_ERR)
    
    def test_mab_agents_thompson_sampling_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                TSAgent(dec_vars, dec_card)
            ],
            agent_names = [
                "TS"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        self.assertAlmostEqual(0.95, cum_opt[0][-1], delta=0.05, msg=OPT_ERR)
        self.assertAlmostEqual(24, cum_reg[0][-1], delta=4, msg=REG_ERR)
        
    def test_mab_agents_comparison_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                GreedyAgent(dec_vars, dec_card),
                EpsilonGreedyAgent(dec_vars, dec_card, 0.05),
                EpsilonFirstAgent(dec_vars, dec_card, 100),
                EpsilonDecreasingAgent(dec_vars, dec_card, 0.992),
                TSAgent(dec_vars, dec_card)
            ],
            agent_names = [
                "Greedy",
                "epsilon-Greedy, e=0.05",
                "epsilon-First, t=100",
                "epsilon-Decreasing, decay=0.992",
                "TS",
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        
    def test_mab_agents_custom_full(self) -> None:
        sim_model, dec_vars, dec_card, out_vars = get_simple_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                TSAgent(dec_vars, dec_card),
                CustomAgent(dec_vars, dec_card)
            ],
            agent_names = [
                "TS",
                "Custom"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = False
        )
        self.assertGreater(cum_reg[0][-1], cum_reg[1][-1], "[X] Your custom agent's regret must outperform the Thompson sampler for T=1000")
        
    def test_mab_agents_context_basic(self) -> None:
        sim_model, dec_vars, dec_card, context_vars, context_card, out_vars = get_simple_context_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                ContextBlindAgent(dec_vars, dec_card, context_vars, context_card),
                ContextualAgent(dec_vars, dec_card, context_vars, context_card)
            ],
            agent_names = [
                "Context-blind",
                "Context-sensitive"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = True
        )
        self.assertGreater(cum_reg[0][-1], cum_reg[1][-1], "[X] Your context-sensitive agent's regret must outperform the context-blind")
        self.assertGreater(30, cum_reg[1][-1], msg=REG_ERR)
        
    def test_mab_agents_context_advanced(self) -> None:
        sim_model, dec_vars, dec_card, context_vars, context_card, out_vars = get_advanced_context_sim()
        (cum_reg, cum_opt) = run_sim(
            agents = [
                ContextBlindAgent(dec_vars, dec_card, context_vars, context_card),
                ContextualAgent(dec_vars, dec_card, context_vars, context_card)
            ],
            agent_names = [
                "Context-blind",
                "Context-sensitive"
            ],
            sim_model = sim_model,
            N = N,
            T = T,
            SIM_NAME = self._testMethodName,
            verbose = VERBOSE,
            contexts = True
        )
        self.assertGreater(cum_reg[0][-1], cum_reg[1][-1], "[X] Your context-sensitive agent's regret must outperform the context-blind")
        self.assertGreater(40, cum_reg[1][-1], msg=REG_ERR)
    
if __name__ == '__main__':
    unittest.main()