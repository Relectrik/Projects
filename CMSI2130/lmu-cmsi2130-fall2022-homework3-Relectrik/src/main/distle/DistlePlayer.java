package main.distle;

import static main.distle.EditDistanceUtils.*;
import java.util.*;

/**
 * AI Distle Player! Contains all logic used to automagically play the game of
 * Distle with frightening accuracy (hopefully).
 */
public class DistlePlayer {
	int turn = 0, wordLength;
	Set<String> dictionaryUsed;
	Random rng;
	
    /**
     * Constructs a new DistlePlayer.
     * [!] You MAY NOT change this signature, meaning it may not accept any arguments.
     * Still, you can use this constructor to initialize any fields that need to be,
     * though you may prefer to do this in the {@link #startNewGame(Set<String> dictionary, int maxGuesses)}
     * method.
     */
    public DistlePlayer () {
    }
    
    /**
     * Called at the start of every new game of Distle, and parameterized by the
     * dictionary composing all possible words that can be used as guesses / one of
     * which is the correct.
     * 
     * @param dictionary The dictionary from which the correct answer and guesses
     * can be drawn.
     * @param maxGuesses The max number of guesses available to the player.
     */
    public void startNewGame (Set<String> dictionary, int maxGuesses) {
    	dictionaryUsed = dictionary;
    	this.rng = new Random();
    }
    
    /**
     * Requests a new guess to be made in the current game of Distle. Uses the
     * DistlePlayer's fields to arrive at this decision.
     * 
     * @return The next guess from this DistlePlayer.
     */
    public String makeGuess () {
    	//Dictionary 6 Guess
//    	if (turn == 0 && dictionaryUsed.size() == 27190) {
//    		return "soiree";
//    	}
//    	//Dictionary 10 Guess
//    	else if (turn == 0 && dictionaryUsed.size() == 101009) {
//    		return "simulation";
//    	}
//    	//Dictionary 14 Guess
//    	else if (turn == 0 && dictionaryUsed.size() == 112424) {
//    		return "slaughterhouse";
//    	}
//        //Arbitrary Dictionary Guess
//    	else if (turn == 0) {
//    		return "tares";
//    	}
//    	
//    	else {
//    		//After initial guess and feedback has ruled out certain words,
//    		//loop through dictionary to see what word matches the parameters.
//    		for (String word : dictionaryUsed) {
//    			if (word.length() == wordLength) {
//    				return word;
//    			}
//    		}
//    		return null;
//    	}
        return this.dictionaryUsed.stream().skip(this.rng.nextInt(this.dictionaryUsed.size())).findFirst().orElse(null);

    }
    
    /**
     * Called by the DistleGame after the DistlePlayer has made an incorrect guess. The
     * feedback furnished is as follows:
     * <ul>
     *   <li>guess, the player's incorrect guess (repeated here for convenience)</li>
     *   <li>editDistance, the numerical edit distance between the guess and secret word</li>
     *   <li>transforms, a list of top-down transforms needed to turn the guess into the secret word</li>
     * </ul>
     * [!] This method should be used by the DistlePlayer to update its fields and plan for
     * the next guess to be made.
     * 
     * @param guess The last, incorrect, guess made by the DistlePlayer
     * @param editDistance Numerical distance between the guess and the secret word
     * @param transforms List of top-down transforms needed to turn the guess into the secret word
     */
    public void getFeedback (String guess, int editDistance, List<String> transforms) {
    	//Remove previous guess from dictionary
    	dictionaryUsed.remove(guess);
    	
    	//Based on "I"s and "D"s change the length of the word that it should be.
        wordLength = guess.length();
    	for (String transformation : transforms) {
    		if (transformation == "I") {
    			wordLength++;
    		}
    		if (transformation == "D") {
    			wordLength--;
    		}	
    	}
    	//Loop through dictionary to add to words ruled out to improve our filter.
    	Iterator<String> iterator = dictionaryUsed.iterator();
    	while (iterator.hasNext()) {
    	String word = iterator.next();
    		if (!getTransformationList(guess, word, getEditDistTable(guess, word)).equals(transforms)) {
    			iterator.remove();
    		}
    	}
    	//Increment turn
    	turn++;  
    }
    
}