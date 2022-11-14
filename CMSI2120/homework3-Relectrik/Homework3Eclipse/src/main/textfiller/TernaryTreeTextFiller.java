package main.textfiller;

import java.util.*;

/**
 * A ternary-search-tree implementation of a text-autocompletion
 * trie, a simplified version of some autocomplete software.
 * @author Vivek Dhingra
 */
public class TernaryTreeTextFiller implements TextFiller {

    // Fields
    // -----------------------------------------------------------
    private TTNode root;
    private int size;
    
    // Constructor
    // -----------------------------------------------------------
    public TernaryTreeTextFiller () {
        this.root = null;
        this.size = 0;
    }
    
    
    // Methods
    // -----------------------------------------------------------
    
    public int size () {
        return size;
    }

    public boolean empty () {
        if (this.root == null) {
        	return true;
        }
        else {
        	return false;
        }

    }
    
    public void add (String toAdd) {
    	int counter = size;
    	this.root = insert(toAdd, 0, this.root, counter);	
    }
    
    public boolean contains (String query) {
    	if (query == null || query.isEmpty()) {
    		return false;
    	}

    	return search(query, 0, this.root);

    }
    
    public String textFill (String query) {
    	String auto = " ";
    	String finalword = " ";
    	String start = autocompletestring(query, 0, this.root, auto);
    	TTNode nodestart = autocompletenode(query, 0, this.root);
    	String autocomplete = autocomplete(nodestart, finalword);
    	if (start == null) {
    		return autocomplete;
    	}
    	else {
    		return start + autocomplete;
    	}
    }
    
    public List<String> getSortedList () {
    	ArrayList<String> sorted = new ArrayList<String>();
    	printAllWords(this.root, "", sorted);
    	return sorted;
    }
    
    
    // Private Helper Methods
    // -----------------------------------------------------------
    
    /**
     * Normalizes a term to either add or search for in the tree,
     * since we do not want to allow the addition of either null or
     * empty strings within, including empty spaces at the beginning
     * or end of the string (spaces in the middle are fine, as they
     * allow our tree to also store multi-word phrases).
     * @param s The string to sanitize
     * @return The sanitized version of s
     */
    private String normalizeTerm (String s) {
        // Edge case handling: empty Strings illegal
        if (s == null || s.equals("")) {
            throw new IllegalArgumentException();
        }
        return s.trim().toLowerCase();
    }
    
    /**
     * Given two characters, c1 and c2, determines whether c1 is
     * alphabetically less than, greater than, or equal to c2
     * @param c1 The first character
     * @param c2 The second character
     * @return
     *   - some int less than 0 if c1 is alphabetically less than c2
     *   - 0 if c1 is equal to c2
     *   - some int greater than 0 if c1 is alphabetically greater than c2
     */
    private int compareChars (char c1, char c2) {
        return Character.toLowerCase(c1) - Character.toLowerCase(c2);
    }
    
    // [!] Add your own helper methods here!
    // method to add a term to tree recursively
   private TTNode insert(String word, int index, TTNode node, int counter) {	   
	   	word = normalizeTerm(word);
	   	char i = word.charAt(index);
    	if (node == null) {
    		node = new TTNode(i, false);
    	}
    	if (compareChars(i, node.letter) < 0) {
    		node.left = insert(word, index, node.left, counter);
    	}
    	else if (compareChars(i, node.letter) > 0) {
    		node.right = insert(word, index, node.right, counter);
    	}
    	else if (index < word.length() - 1) {
    		node.mid = insert(word, index + 1, node.mid, counter);
    	}
    	else { 
        	if (search(word, 0, this.root) == false) {
        		size++;
        		//this.words[counter] = word;
        	}
    		node.wordEnd = true;
    	}
    	return node; 
    }
   // method to search through tree given a string
    private boolean search (String word, int index, TTNode node) {
    	if (node == null) {
    		return false;
    	}
    	if (word == null) {
    		return false;
    	}
    	char i = word.charAt(index);
    	if (compareChars(i, node.letter) < 0) {
    		return search(word, index, node.left);
    	}
    	if(compareChars(i, node.letter) > 0) {
    		return search(word, index, node.right);
    	}
    	if (index < word.length() - 1) {
    		return search(word, index + 1, node.mid);
    	}
    	return node.wordEnd;
    	
    }
    //to return first part of string
    private String autocompletestring (String word, int index, TTNode node, String auto) {
    	if (node == null) {
    		return null;
    	}
    	char i = word.charAt(index);
    	if (compareChars(i, node.letter) < 0) {
    		return autocompletestring(word, index, node.left, auto);
    	}
    	if(compareChars(i, node.letter) > 0) {
    		return autocompletestring(word, index, node.right, auto);
    	}
    	if (index == word.length() - 1) {
    		return auto.replaceAll("\\s", "");
    	}
    	return autocompletestring(word, index + 1, node.mid, auto + node.letter);
    	
    }
    //autocomplete method to return node after prefix string has been inserted
    private TTNode autocompletenode (String word, int index, TTNode node) {
    	if (node == null) {
    		return null;
    	}
    	char i = word.charAt(index);
    	if (compareChars(i, node.letter) < 0) {
    		return autocompletenode(word, index, node.left);
    	}
    	if(compareChars(i, node.letter) > 0) {
    		return autocompletenode(word, index, node.right);
    	}
    	if (index == word.length() - 1) {
    		return node;
    	}
    	return autocompletenode(word, index + 1, node.mid);
    	
    }
    
    //autocomplete method to return second part of string taking the final node after prefix
    private String autocomplete(TTNode node, String finalword) {
    	if (node == null) {
    		return null;
    	}
    	
    	else if (node.wordEnd == false){
    		finalword = finalword + node.letter;
    		return autocomplete(node.mid, finalword);
    	}
    	

    	else {
    		return finalword.replaceAll("\\s", "") + node.letter;
    	}
    	
    }
    
    // Method to traverse through tree using inorder traversal and adding it to arraylist
    private void printAllWords(TTNode node, String word, ArrayList<String> finalwords) {
    	if (node == null) {
    		return;
    	}
    	printAllWords(node.left, word, finalwords);
    	word = word + node.letter;
    	if (node.wordEnd == true) {
    		finalwords.add(word);
    	}
    	printAllWords(node.mid, word, finalwords);
    	word = word.substring(0, word.length()-1);
    	printAllWords(node.right, word, finalwords);

		
    	
    }
    
    
    // TTNode Internal Storage
    // -----------------------------------------------------------
    
    /**
     * Internal storage of textfiller search terms
     * as represented using a Ternary Tree (TT) with TTNodes
     * [!] Note: these are currently implemented for the base-assignment;
     *     those endeavoring the extra-credit may need to make changes
     *     below (primarily to the fields and constructor)
     */
    private class TTNode {
        
        boolean wordEnd;
        char letter;
        TTNode left, mid, right;
        
        /**
         * Constructs a new TTNode containing the given character
         * and whether or not it represents a word-end, which can
         * then be added to the existing tree.
         * @param letter Letter to store at this node
         * @param wordEnd Whether or not this is a word-ending letter
         */
        TTNode (char letter, boolean wordEnd) {
            this.letter  = letter;
            this.wordEnd = wordEnd;
        }
        
    }
}
    

