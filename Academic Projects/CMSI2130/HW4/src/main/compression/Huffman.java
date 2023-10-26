package main.compression;

import java.util.*;
import java.util.Map.Entry;
import java.io.ByteArrayOutputStream; // Optional

/**
 * Huffman instances provide reusable Huffman Encoding Maps for
 * compressing and decompressing text corpi with comparable
 * distributions of characters.
 */
public class Huffman {
    
    // -----------------------------------------------
    // Construction
    // -----------------------------------------------

    private HuffNode trieRoot;
    // TreeMap chosen here just to make debugging easier
    private TreeMap<Character, String> encodingMap;
    // Character that represents the end of a compressed transmission
    private static final char ETB_CHAR = 23;
    
    /**
     * Creates the Huffman Trie and Encoding Map using the character
     * distributions in the given text corpus
     * 
     * @param corpus A String representing a message / document corpus
     *        with distributions over characters that are implicitly used
     *        throughout the methods that follow. Note: this corpus ONLY
     *        establishes the Encoding Map; later compressed corpi may
     *        differ.
     */
    public Huffman (String corpus) {
    	Map<Character, Integer> charFrequency = frequencyMap(corpus);
    	PriorityQueue<HuffNode> nodePriority = fillPriorityQueue(charFrequency);
    	
    	trieConstruction(nodePriority);
    	this.trieRoot = nodePriority.poll();
    	this.encodingMap = new TreeMap<>();
    	encodeTrie(this.trieRoot, "");
	}
    
    /*
     * Creates a map of frequency of each character in the corpus to be compressed
     * 
     * @param corpus A String representing a message / document corpus
     *        with distributions over characters that are implicitly used
     *        throughout the methods that follow.
 *     @return A frequency map of how often each character appears in the corpus.
     */
    private Map<Character, Integer> frequencyMap (String corpus) {
    	corpus += ETB_CHAR;
		Map<Character, Integer> letterFrequency = new HashMap<Character, Integer>();
    	
    	for (char letter : corpus.toCharArray()) {
    		if (letterFrequency.containsKey(letter)) {
                letterFrequency.put(letter, letterFrequency.get(letter) + 1);
    		}
    		
    		else {
    			letterFrequency.put(letter, 1);
    		}
    	}
    	return letterFrequency;
	}
    
    /*
     * Fills up the Priority Queue ready to sort and create the Huffman Trie
     * 
     * @param Takes the frequency map of characters in corpus created earlier.
     * @return Returns a Priority Queue of nodes to create the Huffman Trie for
     * 		   compression and decompression.
     */
    private PriorityQueue<HuffNode> fillPriorityQueue(Map<Character, Integer> frequencyMap) {
    	PriorityQueue<HuffNode> priorityFrequency = new PriorityQueue<HuffNode>();
    	
    	for (Entry<Character, Integer> entry : frequencyMap.entrySet()) {
    		priorityFrequency.add(new HuffNode(entry.getKey(), entry.getValue()));
    	}
    	return priorityFrequency;
    }
    
    /*
     * Constructs the Huffman Trie
     * 
     * @param Takes the Priority Queue with our sorted nodes to build the Trie
     */
    private void trieConstruction(PriorityQueue<HuffNode> priorityFrequency) {
    	while (priorityFrequency.size() > 1) {
    		HuffNode zeroChild = priorityFrequency.poll();
    		HuffNode oneChild = priorityFrequency.poll();
    		HuffNode parent = new HuffNode(zeroChild.character, (zeroChild.count + oneChild.count));
    		parent.zeroChild = zeroChild;
    		parent.oneChild = oneChild;
    		priorityFrequency.add(parent);
    	}
    }
    	
    /*
     * Uses the built Huffman Trie in the stack to populate the encodingMap
     * 
     * @param Takes in the root node so that it can recurse over every node
     * 		  and populate the encodingMap with the characters and their 
     * 		  corresponding bitcodes.
     */
	private void encodeTrie(HuffNode currNode, String bitcode) {
		//Base Case
		if (currNode.isLeaf()) {
			encodingMap.put(currNode.character, bitcode);
			return;
		}
		
		//If the zeroChild is not null, recurse there, and add to our bitcode.
		if (currNode.zeroChild != null) {
			encodeTrie(currNode.zeroChild, bitcode + "0");
		}
		
		//If the oneChild is not null, recurse there, and add to our bitcode.
		if (currNode.oneChild != null) {
			encodeTrie(currNode.oneChild, bitcode + "1");
		}
	}
    
    // -----------------------------------------------
    // Compression
    // -----------------------------------------------
    
    /**
     * Compresses the given String message / text corpus into its Huffman coded
     * bitstring, as represented by an array of bytes. Uses the encodingMap
     * field generated during construction for this purpose.
     * 
     * @param message String representing the corpus to compress.
     * @return {@code byte[]} representing the compressed corpus with the
     *         Huffman coded bytecode. Formatted as:
     *         (1) the bitstring containing the message itself, (2) possible
     *         0-padding on the final byte.
     */
    public byte[] compress (String message) {
		List<String> results = listOfPaddedBytes(message);
		ByteArrayOutputStream output = new ByteArrayOutputStream();
		
		for (String bytecode : results) {
			output.write((byte) Integer.parseInt(bytecode, 2));
		}
		
		return output.toByteArray();
    }
    
    /*
     * Helper method to allow us to pad bytes with "0"s
     * 
     * @param The string of bits to pad
     * @param Boolean for whether we prepend or append to the string.
     * @return Returns the padded byte string
     */
    private String padBytes(String toPad, boolean prepend) {
    	if (prepend) {
    		StringBuilder sb = new StringBuilder(toPad);
        	while (sb.length() % 8 != 0) {
    			sb.insert(0, "0");
    		}
        	toPad = sb.toString();
    	}
    	
    	else {
    		while (toPad.length() % 8 != 0) {
    			toPad += "0";
    		}
    	}
    	return toPad;
    }
    
    /*
     * Bytes are formed by 8 bits, and we can't output a byte with less or more than 8 bits,
     * so we sort a bunch of bits into a list of bytes.
     * 
     * @param A string of a bunch of bits
     * @return A list of bytes
     */
    private List<String> listOfPaddedBytes(String message) {
    	message += ETB_CHAR;
    	String compressed = "";
    	
    	for (char c : message.toCharArray()) {
    		compressed += encodingMap.get(c);
    	}
    	
    	compressed = padBytes(compressed, false);
        
        return Arrays.asList(compressed.split("(?<=\\G.{" + 8 + "})"));
    }
    
    // -----------------------------------------------
    // Decompression
    // -----------------------------------------------
    
    /**
     * Decompresses the given compressed array of bytes into their original,
     * String representation. Uses the trieRoot field (the Huffman Trie) that
     * generated the compressed message during decoding.
     * 
     * @param compressedMsg {@code byte[]} representing the compressed corpus with the
     *        Huffman coded bytecode. Formatted as:
     *        (1) the bitstring containing the message itself, (2) possible
     *        0-padding on the final byte.
     * @return Decompressed String representation of the compressed bytecode message.
     */
    public String decompress (byte[] compressedMsg) {
    	String compressed = "";
    	
    	for (int i = 0; i < compressedMsg.length; i++) {
    		compressed += Integer.toBinaryString(compressedMsg[i] & 0xff);
    	}
    	
    	compressed = padBytes(compressed, true);
    	    	
    	return decompressRecursively(trieRoot, compressed, 0, "");
    }
    
    
    /*
     * Decompresses the string by traversing the Huffman Trie recursively
     * 
     * @param Starts at the root node and iterates over the compressed string and follows
     * 		  the path dependent on the string of bytes it is iterating through.
     * @return Returns the decompressed string
     */
    public String decompressRecursively (HuffNode currNode, String compressed, int i, String decompressed) {
    	if (currNode.isLeaf() && currNode.character == ETB_CHAR) {
    		return decompressed;
    	}
    	
    	else if (currNode.isLeaf()) {
    		return decompressRecursively(trieRoot, compressed, i, decompressed + currNode.character);
    	}
    	
    	else if (compressed.charAt(i) == '0') {
    		return decompressRecursively(currNode.zeroChild, compressed, i + 1, decompressed);
    	}
    	
    	else if (compressed.charAt(i) == '1') {
    		return decompressRecursively(currNode.oneChild, compressed, i + 1, decompressed);
    	}
    	return decompressed;
    }
    
    
    // -----------------------------------------------
    // Huffman Trie
    // -----------------------------------------------
    
    /**
     * Huffman Trie Node class used in construction of the Huffman Trie.
     * Each node is a binary (having at most a left (0) and right (1) child), contains
     * a character field that it represents, and a count field that holds the 
     * number of times the node's character (or those in its subtrees) appear 
     * in the corpus.
     */
    private static class HuffNode implements Comparable<HuffNode> {
        
        HuffNode zeroChild, oneChild;
        char character;
        int count;
        
        HuffNode (char character, int count) {
            this.count = count;
            this.character = character;
        }
        
        public boolean isLeaf () {
            return this.zeroChild == null && this.oneChild == null;
        }
        
        public int compareTo (HuffNode other) {
        	if (this.count != other.count) {
        		return this.count - other.count;
        	}
        	else {
        		return this.character - other.character;
        	}
        }
        
    }

}

// ===================================================
// >>> [KT] Summary
// A great submission that shows strong command of
// programming fundamentals, really great style,
// and a good grasp on the problem and supporting
// theory of compression algos. Indeed, there is definitely
// a lot to like in what you have above, but
// I think you could have tested it a little more just
// to round out the several edge cases that evaded your
// detection. Give yourself more time to test + debug
// future submissions and you'll be golden!
// ---------------------------------------------------
// >>> [KT] Style Checklist
// [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
//
// [X] Variables and helper methods named and used well
// [X] Proper and consistent indentation and spacing
// [X] Proper JavaDocs provided for ALL methods
// [X] Logic is adequately simplified
// [X] Code repetition is kept to a minimum
// ---------------------------------------------------
// Correctness:          92.5 / 100 (-1.5 / missed unit test)
// Style Penalty:       -0 (Nice!)
// Total:                92.5 / 100
// ===================================================
