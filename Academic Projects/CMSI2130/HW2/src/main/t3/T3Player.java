package main.t3;

import java.util.*;

import org.w3c.dom.Node;

/**
 * Artificial Intelligence responsible for playing the game of T3!
 * Implements the alpha-beta-pruning mini-max search algorithm
 */
public class T3Player {
    
    /**
     * Workhorse of an AI T3Player's choice mechanics that, given a game state,
     * makes the optimal choice from that state as defined by the mechanics of the
     * game of Tic-Tac-Total. Note: In the event that multiple moves have
     * equivalently maximal minimax scores, ties are broken by move col, then row,
     * then move number in ascending order (see spec and unit tests for more info).
     * The agent will also always take an immediately winning move over a delayed
     * one (e.g., 2 moves in the future).
     * 
     * @param state
     *            The state from which the T3Player is making a move decision.
     * @return The T3Player's optimal action.
     */
    public T3Action choose (T3State state) {
        //Instantiate variables for comparison and return.
        Map<T3Action,T3State> possibleMoves = state.getTransitions();
        int bestUtility = Integer.MIN_VALUE;
        T3Action bestAction = null;
        
        //For loop through possible actions to return an instant-win, or if
        //there is no option for instant win, then run the alphabeta method
        //on the state.
        for (Map.Entry<T3Action,T3State> entry : possibleMoves.entrySet()) {
            if (entry.getValue().isWin()) {
                return entry.getKey();
            }
        }
        
        //Second for loop to check best move using alphabeta and send it back.
        for (Map.Entry<T3Action,T3State> entry : possibleMoves.entrySet()) {
            int minimax = alphabeta(Integer.MIN_VALUE, Integer.MAX_VALUE, false, entry.getValue());
            //Conditional to hold the best action thus far in the loop.
            if (minimax > bestUtility) {
                bestUtility = minimax;
                bestAction = entry.getKey();
                //If found the best move already, send it back for more efficiency.
                if (bestUtility == 1) {
                    break;
                }
            }
        }
        //Return the bestAction collected in the loop.
        return bestAction;
    }  
    
    /* 
     * Recursive minimax algorithm to return utility score of each move for our choose method to
     * evaluate and return back to user. Bubbles up the utility score from every terminal state
     * (win, loss or tie) back to the given state and then returns this utility.
     * 
     * @param alpha 
     *          Lower bound of values that get updated throughout recursion.
     * @param beta 
     *          Upper bound of values that get updated throughout recursion. 
     * @param boolean 
     *          True when it is a maximizing state, false when minimzing.
     * @param T3State
     *          Current board state that is passed in to evaluate its utility score.
     * @return returns a utility cost for the possible move. 
     */
    private static int alphabeta(int alpha, int beta, boolean maxTurn, T3State state) {
        //Conditionals for terminal states and corresponding utility values.
        if (state.isWin() && !maxTurn) {
            return 1;
        } if (state.isWin() && maxTurn) {
            return -1;
        } if (state.isTie()) {
            return 0;
        }
    	
        //If its a maximizing state, update alpha.
    	if (maxTurn) {
    	    int v = Integer.MIN_VALUE;
    	    for (Map.Entry<T3Action,T3State> entry : state.getTransitions().entrySet()) {
    	        v = Math.max(v, alphabeta(alpha, beta, false, entry.getValue()));
    	        alpha = Math.max(alpha, v);
    	        if (beta <= alpha) {
    	            break;
    	        }
    	    }
    	    return v;
    	}
    	
    	//If its a minimizing state, update beta. 
    	else {
    	    int v = Integer.MAX_VALUE;
    	    for (Map.Entry<T3Action,T3State> entry : state.getTransitions().entrySet()) {
    	        v = Math.min(v, alphabeta(alpha, beta, true, entry.getValue()));
    	        beta = Math.min(beta, v);
    	        if (beta <= alpha) {
    	            break;
    	        }
    	    }
    	    return v;
    	}
    }
}
