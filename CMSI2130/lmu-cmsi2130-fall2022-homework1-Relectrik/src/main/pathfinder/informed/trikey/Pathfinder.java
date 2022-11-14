package main.pathfinder.informed.trikey;

import java.util.*;

/**
 * Maze Pathfinding algorithm that implements a basic, uninformed, breadth-first
 * tree search.
 */
public class Pathfinder {

    /**
     * Given a MazeProblem, which specifies the actions and transitions available in
     * the search, returns a solution to the problem as a sequence of actions that
     * leads from the initial state to the collection of all three key pieces.
     * 
     * @param problem A MazeProblem that specifies the maze, actions, transitions.
     * @return A List of Strings representing actions that solve the problem of the
     *         format: ["R", "R", "L", ...]
     */
    public static List<String> solve(MazeProblem problem) {
    	//Initialize Data Structures
    	PriorityQueue <SearchTreeNode> frontier = new PriorityQueue<SearchTreeNode>();
    	Set <SearchTreeNode> graveyard = new HashSet<SearchTreeNode>();
    	
    	//Adding initial node to frontier
        frontier.add(new SearchTreeNode(problem.getInitial(), null, null, 0, 0, new HashSet<MazeState>(0)));
        
        //While loop to begin our maze traversal.
        while (!frontier.isEmpty()) {
            SearchTreeNode parent = frontier.poll();
            graveyard.add(parent);            
            
            //First conditional to check if current state is a keyState and update our set of keysFound.
            if (problem.getKeyStates().contains(parent.state)) {
            	parent.keysFound.add(parent.state);
        	}
            
            //Conditional to return solution during expansion.
            if (problem.getKeyTiles().size() == parent.keysFound.size()) {
				System.out.println(solution(parent));
				return solution(parent);
        	}
            
            //Loop through possible moves to then create a new node for the move.
            for (Map.Entry<String,MazeState> entry : problem.getTransitions(parent.state).entrySet()) {
                MazeState currPosition = entry.getValue();
                SearchTreeNode currNode = new SearchTreeNode(currPosition, entry.getKey(), parent, getPastCost(parent, problem) + problem.getCost(currPosition), ManhattanCost(currPosition, problem.getKeyStates()), new HashSet<MazeState>(parent.keysFound));
            	
                //Necessary condition so that we do not have repeats and infinite loop.
            	if (!graveyard.contains(currNode)) {
            		frontier.add(currNode);  
        		}            	
    		}
    	}
        //Null return if no solution is found.
		return null;
	}
        
    /*
     * This helper method allows me to get the cost from one node to another in order to
     * obtain the Manhattan distance from currPosition to a keyPosition to use in the heuristic
     * evaluation when choosing which transition to take. 
     * @param takes two MazeStates, the first one is the goal state, and the second one is the current one.
     * @return The cost to go from current position to goal (Manhattan distance).
     */
    
    private static List<String> solution(SearchTreeNode currNode) {
        List <String> solution = new LinkedList<String>();
        
        while(currNode.parent != null) {
          solution.add(0, currNode.action);
          currNode = currNode.parent;
        }
      return solution;
    	
    }
    
    
    /*
     * This helper method retrieves the past cost that stays with the node as we iterate through the tree for our heuristic to function.
     * @param Takes the parent node for its state and its cost up till now, and problem to call getCost on the state.
     * @return Returns cost up till now and adds the parent's cost to it.
     */
    
    private static int getPastCost(SearchTreeNode parent, MazeProblem problem) {
    	return problem.getCost(parent.state) + parent.totalCost;
    
    }

    /*
     * The helper method gives us the cost to the nearest goal state that is updated as we find more keyStates.
     * It does so by giving us an estimate distance between the keyState and current position and then returning
     * a cost of 1 per block moved. I hope you will appreciate the initial cost used to compare.
     * @param Takes the current position in the maze (a state) and the set of states to find the closest one from the current position.
     * @return Returns an estimate cost to the nearest goal state.
     */
    
    private static int ManhattanCost (MazeState currPosition, Set <MazeState> states) {
    	int cost = 42069;
    	
    	for (MazeState state : states) {
    		int manhattan = Math.abs(currPosition.col() - state.col()) + Math.abs(currPosition.row() - state.row());
    		if (manhattan < cost) {
    			cost = manhattan;
    		}
    	}
    	return cost;
    }
    
    
    /**
     * SearchTreeNode private static nested class that is used in the Search
     * algorithm to construct the Search tree.
     * [!] You may do whatever you want with this class -- in fact, you'll need 
     * to add a lot for a successful and efficient  solution!
     */
    private static class SearchTreeNode implements Comparable<SearchTreeNode>{

        MazeState state;
        String action;
        SearchTreeNode parent;
        int totalCost;
        Set <MazeState> keysFound;

        /**
         * Constructs a new SearchTreeNode to be used in the Search Tree.
         * 
         * @param state  The MazeState (row, col) that this node represents.
         * @param action The action that *led to* this state / node.
         * @param parent Reference to parent SearchTreeNode in the Search Tree.
         */
        SearchTreeNode(MazeState state, String action, SearchTreeNode parent, int pastCost, int futureCost, Set<MazeState> keysFound) {
            this.state = state;
            this.action = action;
            this.parent = parent;
            this.keysFound = keysFound;
            this.totalCost = futureCost + pastCost;
        }

        /*
         * Override for our frontier's priorityQueue. The compareTo method allows us to set the priority of nodes, so that the frontier
         * will automatically bubble up the nodes with the lowest heuristic cost so that it always make efficient moves toward the 
         * keyState.
         */
        
		@Override
		public int compareTo(SearchTreeNode o) {
			if (this.totalCost > o.totalCost) {
				return 1;
			}
			else if (o.totalCost > this.totalCost){
				return -1;
			}
			else {
				return 0;
			}
			
		}
		
		/*
		 * Override equals so that our .contains method can correctly check the parameters required for the node's uniqueness. If we do
		 * not have this override, the graveyard and frontier could have identical "looking" nodes because .contains won't know what to look for.
		 * However, with this, we are specifically comparing the state and set of keysFound, which is most likely unique for all nodes.
		 */
		
		@Override
	    public boolean equals(Object other) {
	        SearchTreeNode otherSearchTreeNode = (SearchTreeNode)other;
	        if (otherSearchTreeNode.keysFound.equals(this.keysFound) && otherSearchTreeNode.state.equals(this.state)) {
	        	return true;
	        }
	        return false;
		}
    
		/*
		 * Override for hashCode to make our Override for equals function.
		 */
		
		@Override 
		public int hashCode() {
			return state.hashCode();
		}

}
    }
