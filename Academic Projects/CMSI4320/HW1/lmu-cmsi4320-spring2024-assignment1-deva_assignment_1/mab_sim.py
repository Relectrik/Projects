'''
mab_sim.py

Simulation suite for comparing different Action Selection Rule
performance on traditional Multi-Armed Bandit Problems
'''

import pandas as pd
import numpy as np
import plotly as py # type: ignore
import plotly.graph_objs as go # type: ignore
import multiprocessing
import numpy.typing as npt
from plotly import subplots
from joblib import Parallel, delayed # type: ignore
from mab_agent import *
from sim_model import *

# ----------------------------------------------------------------
# Simulation Constants
# ----------------------------------------------------------------

# Number of cores to run parallel sims upon
N_CORES: int = min(multiprocessing.cpu_count()-1, 4) if multiprocessing.cpu_count() > 1 else 1

# Colors for the graphs (you don't need to change these unless
# you're an art snob)
agent_colors: list[str] = [
    ('rgb(255, 0, 0)'),
    ('rgb(0, 0, 255)'),
    ('rgb(255, 165, 0)'),
    ('rgb(255, 0, 255)'),
    ('rgb(0, 255, 128)'),
    ('rgb(128, 0, 0)'),
    ('rgb(0, 128, 0)'),
    ('rgb(0, 0, 128)')
]

# ----------------------------------------------------------------
# Simulation Functions
# ----------------------------------------------------------------

def run_sim (agents: list[MABAgent],
             agent_names: list[str],
             sim_model: SimModel,
             N: int,
             T: int,
             SIM_NAME: str = "cmsi4320-ass1-sims",
             verbose: bool = False,
             contexts: bool = False) -> tuple[npt.NDArray, npt.NDArray]:
    '''
    Responsible for running the entirety of the MAB simulation, which proceeds in the following steps:
    1. Initializes the bandit agents ONCE
    2. In parallel, runs N Monte Carlo repetitions/rounds of T trials (see @run_sim_round)
    3. After receiving the cumulative regret and probability of optimal action for all n repetitions,
       averages those for display in a graph if VERBOSE has been set to True
    4. Returns the average cumulative regret and probability of optimal action, by time step t
    
    Parameters:
        agents (list[MABAgent]):
            All MAB agents compared in this simulation as indicated by index in this list
        agent_names (list[str]):
            String identifiers for different agents and their associated parameters, e.g.,
            "epsilon-greedy-e=0.1", used in the graph outputs
        sim_model (SimModel):
            The probabilistic model used to determine and simulate choice / covariate outcomes
        N (int):
            The number of Monte Carlo repetitions to run; lower = faster but less accurate average
        T (int):
            The number of trials per n in N to run; higher = more time to learn / play
        SIM_NAME (str):
            The name of this simulation as it will appear in any output file naming like graphs
        verbose (bool):
            Whether or not the simulation will print out relevant details as its running and produce
            a graph summary at its conclusion
        contexts (bool):
            Whether or not context variables will be drawn from the simulation model for any non-
            decision nor outcome variables. If True, these are provided as pre-choice variables to
            the deciding agent before each trial.
    
    Returns:
        tuple[npt.NDArray, npt.NDArray]:
            A 2-tuple consisting of 2 numpy arrays designating the average regret and probability of
            optimal action by each agent by row
    '''
    
    if verbose:
        print()
        print("=== MAB Simulations Beginning ===")
    
    # Record-keeping data structures across MC simulations
    AG_COUNT = len(agents)
    round_reg = np.zeros((AG_COUNT, T))
    round_opt = np.zeros((AG_COUNT, T))
    cum_reg   = np.zeros((AG_COUNT, T))
    
    # MAIN WORKHORSE - Runs MC repetitions of simulations in parallel:
    sim_results = Parallel(n_jobs=N_CORES, verbose=1)(delayed(run_sim_round)(agents, sim_model, T, contexts) for i in range(N))
    for (ind, r) in enumerate(sim_results):
        round_reg += r[0]
        round_opt += r[1]

    # Reporting phase:
    for a in range(AG_COUNT):
        cum_reg[a] = np.array([np.sum(round_reg[a, 0:i+1]) for i in range(T)])
    cum_reg = cum_reg / N
    cum_opt = round_opt / N
    
    if verbose:
        gen_graph(T, SIM_NAME, cum_reg, cum_opt, agent_names, agent_colors)
        print("[!] Simulations Completed")
    
    return (cum_reg, cum_opt)

def run_sim_round (agents: list[MABAgent], sim_model: SimModel, T: int, contexts: bool = False) -> tuple[npt.NDArray, npt.NDArray]:
    '''
    Runs a single Monte Carlo iteration of the simulation consisting of T trials, and the following steps:
    1. Clears the agents' histories so that no memory of past repetitions can infect this one.
    2. For each trial, first generates any context variables c_t that will be sent to all agents (if this is
       a contextual bandit problem)
    3. Next, requests the action choice a_t from each agent in response to that c_t
    4. A reward r_t is nondeterministically computed (i.e., even the best action may not always pay out)
       [!] Importantly: this is assumed to be a Bernoulli reward, i.e., either 0 or 1
    5. Sends feedback to the agent on its choice with all of {a_t, c_t, r_t} so that it can updates its memory
    6. Computes the optimal action and corresponding pseudo-regret for this round and logs this for each agent
    
    Parameters:
        agents (list[MABAgent]):
            All MAB agents compared in this simulation as indicated by index in this list
        sim_model (SimModel):
            The probabilistic model used to determine and simulate choice / covariate outcomes
        T (int):
            The number of trials per n in N to run; higher = more time to learn / play
        contexts (bool):
            Whether or not context variables will be drawn from the simulation model for any non-
            decision nor outcome variables. If True, these are provided as pre-choice variables to
            the deciding agent before each trial.
    
    Returns:
        tuple[npt.NDArray, npt.NDArray]:
            A 2-tuple consisting of 2 numpy arrays designating the average regret and probability of
            optimal action by each agent by row
    '''
    AG_COUNT = len(agents)
    
    ag_reg = np.zeros((AG_COUNT, T))
    ag_opt = np.zeros((AG_COUNT, T))
    
    # Reset agent histories for this MC repetition
    for a in agents:
        a.clear_history()
        
    # Create context vectors a priori for fair comparison of agents
    for t in range(T):
        # Select covariates if this is a contextual problem
        c_t = sim_model.get_covariate_sample() if contexts else dict()
        
        # Find the optimal action and reward rate for this t
        best_a_t, best_reward = sim_model.get_optimal_choice(c_t)
        
        # Determine chosen action and reward for each agent
        # within this trial, t
        for a_ind, ag in enumerate(agents):
            a_t = ag.contextual_choose(c_t) if contexts else ag.choose()
            # Assumes rewards are summative for outcome variables
            r_t = sum(sim_model.get_outcome_sample(a_t, c_t).values())
            ag.give_contextual_feedback(a_t, c_t, r_t) if contexts else ag.give_feedback(a_t, r_t) 
            reg_t = best_reward - r_t
            ag_reg[a_ind, t] += reg_t
            ag_opt[a_ind, t] += int(a_t == best_a_t)
                
    return (ag_reg, ag_opt)

def gen_graph (T: int, SIM_NAME: str, cum_reg: npt.NDArray, cum_opt: npt.NDArray, names: list[str], colors: list[str]) -> None:
    '''
    Reporting mechanism that generates graphical reports on the probability that each agent takes the optimal action and the
    agent's cumulative regret, both as a function of the current trial, t
    
    Parameters:
        T (int):
            The number of trials per n in N to run; higher = more time to learn / play
        SIM_NAME (str):
            The name of this simulation as it will appear in any output file naming like graphs
        names (list[str]):
            String identifiers for different agents and their associated parameters, e.g.,
            "epsilon-greedy-e=0.1", used in the graph outputs
        colors (list[str]):
            The colors of each graph associated with each compared agent, by corresponding index
    '''
    AG_COUNT = cum_reg.shape[0]
    fig = subplots.make_subplots(rows=1, cols=2, subplot_titles=('Probability of Optimal Action', 'Cumulative Regret'))
    fig['layout']['xaxis1'].update(title='Trial', range=[0, T])
    fig['layout']['xaxis2'].update(title='Trial', range=[0, T])
    fig['layout']['yaxis1'].update(title='Probability of Optimal Action', range=[0, 1])
    fig['layout']['yaxis2'].update(title='Cumulative Regret')
    
    # Plot cumulative regret
    for a in range(AG_COUNT):
        trace = go.Scatter(
            x = list(range(T)),
            y = cum_opt[a, :],
            line = dict(
                color = colors[a]
            ),
            name = names[a]
        )
        fig.add_trace(trace, 1, 1)
        
    # Plot optimal arm choice
    for a in range(AG_COUNT):
        trace = go.Scatter(
            x = list(range(T)),
            y = cum_reg[a, :],
            line = dict(
                color = colors[a]
            ),
            name = "[REG]" + names[a],
            showlegend = False
        )
        fig.add_trace(trace, 1, 2)
    
    py.offline.plot(fig, filename=("./plots/cumu_reg_" + SIM_NAME + ".html"))

