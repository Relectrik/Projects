package main.distle;

import java.util.*;

public class EditDistanceUtils {
    
    /**
     * Returns the completed Edit Distance memoization structure, a 2D array
     * of ints representing the number of string manipulations required to minimally
     * turn each subproblem's string into the other.
     * 
     * @param s0 String to transform into other
     * @param s1 Target of transformation
     * @return Completed Memoization structure for editDistance(s0, s1)
     */
    public static int[][] getEditDistTable (String s0, String s1) {
    	//Initialize 2D Array
        int[][] editDistTable = new int[s0.length()+1][s1.length()+1];
        
        //Nested for loop through the 2D Array to fill it out
        for (int row = 0; row < editDistTable.length; row++) {
        	for (int col = 0; col < editDistTable[row].length; col++) {
        		
        		//Filling base-case gutters
        		if (row == 0 || col == 0) {
        			editDistTable[row][col] = row + col;
        		}
        		
        		//If not a gutter
        		else {
        			//Condition to check if we can even transpose
        			if (row > 1 && col > 1) {
        				//Transposition & Replacement
        				if (s0.charAt(row - 1) == s1.charAt(col - 2) && s0.charAt(row - 2) == s1.charAt(col - 1) && s0.charAt(row - 1) == s1.charAt(col - 1)){
        					editDistTable[row][col] = Math.min(editDistTable[row-2][col-2] + 1, Math.min(editDistTable[row-1][col-1], Math.min(editDistTable[row-1][col] + 1, editDistTable[row][col-1] + 1)));
        					continue;
        				}
        				//Transposition
        				if (s0.charAt(row - 1) == s1.charAt(col - 2) && s0.charAt(row - 2) == s1.charAt(col - 1)){
        					editDistTable[row][col] = Math.min(editDistTable[row-2][col-2] + 1, Math.min(editDistTable[row-1][col-1]+1, Math.min(editDistTable[row-1][col] + 1, editDistTable[row][col-1] + 1)));
        					continue;
        				}
        			}
        			
        			//Replacement
        			if (s0.charAt(row - 1) == s1.charAt(col - 1)) {
        				editDistTable[row][col] = Math.min(editDistTable[row-1][col-1], Math.min(editDistTable[row-1][col] + 1, editDistTable[row][col-1] + 1));
        				continue;
        			}
        			
        			else {
        				//Most likely case when the letters do not match.
        				editDistTable[row][col] = Math.min(editDistTable[row-1][col-1] + 1, Math.min(editDistTable[row-1][col] + 1, editDistTable[row][col-1] + 1));
        			}
        		}
        	}
        }
        return editDistTable; 
    }
    
    /**
     * Returns one possible sequence of transformations that turns String s0
     * into s1. The list is in top-down order (i.e., starting from the largest
     * subproblem in the memoization structure) and consists of Strings representing
     * the String manipulations of:
     * <ol>
     *   <li>"R" = Replacement</li>
     *   <li>"T" = Transposition</li>
     *   <li>"I" = Insertion</li>
     *   <li>"D" = Deletion</li>
     * </ol>
     * In case of multiple minimal edit distance sequences, returns a list with
     * ties in manipulations broken by the order listed above (i.e., replacements
     * preferred over transpositions, which in turn are preferred over insertions, etc.)
     * @param s0 String transforming into other
     * @param s1 Target of transformation
     * @param table Precomputed memoization structure for edit distance between s0, s1
     * @return List that represents a top-down sequence of manipulations required to
     * turn s0 into s1, e.g., ["R", "R", "T", "I"] would be two replacements followed
     * by a transposition, then insertion.
     */
    public static List<String> getTransformationList (String s0, String s1, int[][] table) {
    	//Calling helper method to recurse
    	return recursiveHelper(s0.length(), s1.length(), new ArrayList<String>(), s0, s1);
    }
    
    /**
     * Returns one possible sequence of transformations that turns String s0
     * into s1. The list is in top-down order (i.e., starting from the largest
     * subproblem in the memoization structure) and consists of Strings representing
     * the String manipulations of:
     * <ol>
     *   <li>"R" = Replacement</li>
     *   <li>"T" = Transposition</li>
     *   <li>"I" = Insertion</li>
     *   <li>"D" = Deletion</li>
     * </ol>
     * In case of multiple minimal edit distance sequences, returns a list with
     * ties in manipulations broken by the order listed above (i.e., replacements
     * preferred over transpositions, which in turn are preferred over insertions, etc.)
     * @param int row to keep track of what row we're at through the recursion
     * @param int col to keep track of what column we're at through the recursion
     * @param List to update through the recursion
     * @param s0 String transforming into other
     * @param s1 Target of transformation
     * @return List that represents a top-down sequence of manipulations required to
     * turn s0 into s1, e.g., ["R", "R", "T", "I"] would be two replacements followed
     * by a transposition, then insertion.
     */
    private static List<String> recursiveHelper(int row, int col, List<String> list, String s0, String s1) {
    	//Initializing the Edit Distance Table created by the two strings
    	int[][] table = getEditDistTable(s0, s1);
    	
    	//If we reach the base case (0, 0), return.
    	if (row == 0 && col == 0) {
    		return list;
    	}
    	//If we are at the 0th row, keep adding "I" to the list until we get back to the base case.
    	else if (row == 0) {
    		list.add("I");
    		recursiveHelper(row, col-1, list, s0, s1);
    	}
    	//If we are at the 0th column, keep adding "D" until we get back to the base case.
    	else if (col == 0) {
    		list.add("D");
    		recursiveHelper(row-1, col, list, s0, s1);
    	}
    	//If it's the same letter, don't add to the list and recurse to top-left cell.
    	else if (s0.charAt(row-1) == s1.charAt(col-1)) {
    		recursiveHelper(row-1, col-1, list, s0, s1);
    	}
    	
    	//If the transposition exists in the first place.
    	else if (row > 1 && col > 1){
    		//If there is a transposition present in the strings
    		if (s0.charAt(row - 1) == s1.charAt(col - 2) && s0.charAt(row - 2) == s1.charAt(col - 1)){
				if (table[row][col] == table[row-1][col-1] + 1) {
					list.add("R");
					recursiveHelper(row - 1, col - 1, list, s0, s1);
				}
				else if (table[row][col] == table[row-2][col-2] + 1) {
					list.add("T");
					recursiveHelper(row - 2, col - 2, list, s0, s1);
				}
				else if (table[row][col] == table[row][col-1] + 1) {
					list.add("I");
					recursiveHelper(row, col - 1, list, s0, s1);
				}
				else if (table[row][col] == table[row-1][col] + 1) {
					list.add("D");
					recursiveHelper(row - 1, col, list, s0, s1);
				}
    		}
    		
    		//Most often case (no transposition or replacement present in the characters)
    		else {
    			if (table[row][col] == table[row-1][col-1] + 1) {
    				list.add("R");
    				recursiveHelper(row - 1, col - 1, list, s0, s1);
    			}
    			else if (table[row][col] == table[row][col-1] + 1) {
    				list.add("I");
    				recursiveHelper(row, col - 1, list, s0, s1);
    			}
    			else if (table[row][col] == table[row-1][col] + 1) {
    				list.add("D");
    				recursiveHelper(row - 1, col, list, s0, s1);
    			}
    		}
    	}
		//Most often case (no transposition or replacement present in the characters)
    	else {
			if (table[row][col] == table[row-1][col-1] + 1) {
				list.add("R");
				recursiveHelper(row - 1, col - 1, list, s0, s1);
			}
			else if (table[row][col] == table[row][col-1] + 1) {
				list.add("I");
				recursiveHelper(row, col - 1, list, s0, s1);
			}
			else if (table[row][col] == table[row-1][col] + 1) {
				list.add("D");
				recursiveHelper(row - 1, col, list, s0, s1);
			}
		}
		return list;
	}
    
    /**
     * Returns the edit distance between the two given strings: an int
     * representing the number of String manipulations (Insertions, Deletions,
     * Replacements, and Transpositions) minimally required to turn one into
     * the other.
     * 
     * @param s0 String to transform into other
     * @param s1 Target of transformation
     * @return The minimal number of manipulations required to turn s0 into s1
     */
    public static int editDistance (String s0, String s1) {
        if (s0.equals(s1)) { return 0; }
        return getEditDistTable(s0, s1)[s0.length()][s1.length()];
    }
    
    /**
     * See {@link #getTransformationList(String s0, String s1, int[][] table)}.
     */
    public static List<String> getTransformationList (String s0, String s1) {
        return getTransformationList(s0, s1, getEditDistTable(s0, s1));
    }

}
