# Homework 3
Early due date: 4/12/2021 at 11:59pm
Normal due date: 4/19/2021 at 11:59 pm

This Homework is to be completed individually. You may discuss ideas with fellow classmates, but you must credit them (write their name in a comment at the top of your code). You MAY NOT share your code, or look at another students code.

If you complete the assignment before the early due date, you will receive 10% multiplicative bonus (if you earned a 90% it would become a 99%). You must email me at the time of completion to receive these points. Under no circumstances will the early due date be extended, or extensions be granted. The normal due date is right after Easter break, hence the two deadlines. 

# Motivation

Have you ever been curious about how search engines show you suggested searches while you're typing? Google (and many other engines) use many heuristics (like your history) to determine what to show you. In this assignment, we'll be building a tree-based data structure that can perform a basic version of this "auto-complete" functionality.


# Choosing a data structure

When a problem is first described, hopefully the first thought that crosses your mind is of the data structures we've learned about thus far, and what might be most appropriate for the task at hand. If this is our first thought for solving the problem, we're already on the right track. Some things to consider while debating our choice of data structure:

1. We will add many search terms to our data structure, which will be Strings representing search queries.
2. Once our data structure is built, we should be able to quickly look up if any String is in our data structure
3. Additionally, given a beginning substring of a String, we need to determine the most likely finished string

Simply storing things in a list and then scanning the list might be the most simple approach, but this is expensive to store (we are not sharing common subsequences, especially for long strings), it is expensive to search, and struggles to suggest finished strings.

We might consider BST's, which would allow faster storage and search queries, but we still don't have an idea for how to handle our text suggestion.

Luckily for us, we are allowed to build our own data structures. We can take a BST, and make some changes to it to be better fit for this problem.

# Understanding Tries and Ternary Search Trees

Tries, also known as Prefix Trees, are a type of search tree, where items stored with are unique (keys) and have overlapping prefixes stored efficiently.

Ternary Search Trees are a space-efficient implementation of a Trie wherein each Node has at most 3 children with application-specific semantics for left, middle, and right children.

In our application, we want to store words in a space efficient manner, where we can query and find the most similar predicted word from only the beginning letters. We'll build a ternary search tree with the following properties:

1. Each node will store a single letter of a word in the collection
2. The "middle" reference of every node will point to the next letter in the word, in sequence (just like a linked list).
3. Certain words are prefixes of others (consider "it" and "its"), we'll mark certain nodes as "word ends" to indicate that letters collected along middle paths may legally stop at them.
4. The "left" and "right" reference of ever node are possibly null, but when non-null, points to nodes in which other words are to be formed using the previous middle path that led up to them as a prefix.
5. In particular, a node to the left of another node will posses a letter of a different word that is alphabetically less than its parent node, and a node to the right of another will possess a letter of another word that is alphabetically greater than the parent.
6. We then use these trees to form words by starting at the root, and "collect" letters along middle paths that match our query, and then do a binary search when the letters do not match at a node (look to the left if the letter is less than the current, or to the right when the letter is greater).

# Example

This is a possible structure of our ternary search tree. Notice that the order of adding items changes how the tree will look, but shouldn't change how it behaves overall.

![Image borrowed from Andrew Forney](https://forns.lmu.build/assets/images/fall-2016/cmsi-281/hw/ternary-tree-hw4.PNG)

- Practice: Try to add another word to the tree
- Practice: Step by step explain how we would query the tree to check if it contains a word


So knowing how our data structure should work, lets think again about how we are going to be using it:
1. Insert search terms into our ternary trie to follow the structure above.
2. After terms have been inserted, we may query the tree in a variety of ways, like checking if a term exists of asking it to fill-in the missing letters of some prefix.


# Adding to a Ternary Trie

Adding can be implemented either iteratively or recursively.

Think about adding a new term to our Ternary Trie as being similar to adding to a Binary Search Tree.

Consider any new term that you're adding as a composite of: newTerm = termPrefix + termSuffix, where some part of the newTerm's prefix may already be stored within the Trie, and thus we just need to find where the unstored termSuffix should go.

Using this assumption, our high level steps are:
1. Traverse the existing Trie for as much of the already-stored prefix for the term that we want to add as we can.
2. Along the way, we'll discover one of the following cases to be true:
	* The newTerm is a prefix of an existing term (in which case, we simply mark the Node corresponding with the final letter as a wordEnd)
	* There is some part of the newTerm that is not stored within the trie already, which will be the termSuffix, i.e., all letters in the newTerm that aren't already stored in prefix-format.


See the example below for a trace of inserting the word "bard".
![enter image description here](https://forns.lmu.build/assets/images/fall-2021/cmsi-2120/week-10/trie-ex-add.png)



# Querying Ternary Trie
Querying can be implemented either iteratively or recursively.

Querying the Trie can take a number of different forms:
* Ask if the tree contains a specific search term
* Ask the tree to provide a suggested search term based on a given query (which is possibly just a fragment of a contained search term)
* Ask the tree to provide a sorted list of all contained search terms



# Specifications
- Implement the TernaryTreeTextFiller class that uses a Ternary Search Tree to provide the behavior described above/below. Each method is weighted equally for determining your final score on this assignment.

Your TernaryTreeTextFiller class will implement the provided TextFiller interface.
All inserted search terms and query terms are to be referenced in their normalized format (see helper methods).

The methods include:

- int size();
	- Returns the number of stored items inside of the TextFiller. Same as asking for the number of nodes that are the end of words.
- boolean empty();
	- Returns true if the TextFiller has no search terms stored, false otherwise
- void add(String toAdd);
	- Adds the given search term toAdd to the TextFiller by the method specified in the document above.
	- If the desired string toAdd already exists inside of TextFiller, do nothing.
	- Note that the order in which terms are inserted to the Ternary Tree may influence what will be output in the textFill method below.
	- Additionally, the order in which things are added can influence the efficiency of each operation if the tree becomes too linear. Although not desirable, you do NOT need to balance your tree to guarantee performance.
- boolean contains(String query);
	- Returns true if the given query String exists within the TextFiller, false otherwise
- String textFill(String query);
	- Returns the first* search term contained in the TextFiller that possesses the query as a prefix (e.g. "it" is a prefix of "it"[exact match] and "item" [first two letters]).
	- In the event that the given query is a prefix for more than one stored search term, any appropriate matching terms are acceptable.
	- See the unit tests in the skeleton for examples of this behavior (e.g. unit tests with "goad" vs "goat").
	- In the event that the given query is a prefix for NO search term, return null.
- List<String> getSortedLIst();
	- Returns an ArrayList of Strings consisting of the alphabetically sorted search terms within this TextFiller.
	- Alphabetic sorting is the same as how a dictionary sorts its entries, so for example "ass" is considered a predecessor to "at", even though it has more letters.
	- See the unit tests below for examples of this behavior.



# Provided Helper methods
- String normalizeTerm(String s);
	- Throws IllegalArgumentException(); when s is null or empty.
	- Used to normalize arguments to all of the assignment methods, as well as how the terms are stored.
- int compareChars(char c1, char c2);
	- Compares two characters and returns an integer representing their alphabetical ordering. In particular:
		- returns some integer less than 0 whenever c1 alphabetically preceeds c2.
		- Returns 0 whenever c1 is the same character as c2.
		- Returns some integer greater than 0 whenever c1 alphabetically follows c2.
	- This method is useful for constructing and then navigating your ternary search tree.



# Assumptions
To simplify the assignment, assume the following:
- There will be no punctuation, spaces, or numbers in any of the arguments to any of the above methods.
- You need make no assumptions about the order in which search terms are added to the TextFiller so long as the above requirements are met (meaning: unbalanaced ternary trees will not be penalized).


# Unit Tests
Use the provided unit tests in the solution skeleton. I would also advise testing some edge cases, including:
- Inserting words of various sizes, including those of 1, 2, 3, etc. letters long
- Adding words that are prefixes of existing words in the tree, and adding words that are extensions of existing words
- Adding a duplicate word (nothing should happen)
- Adding words that share various prefixes with others already in the tree.


# Solution Restrictions
**Important! Violating any restriction here will net you a 0 on the assignment.**
- You may not use **ANY** data structure from the Java collections framework in your solution (with the exception of an ArrayList within the getSortedList method). Elsewhere you may not use any data structure or algorithm that you did not create yourself. When in doubt, ask!
- You may not add any methods or fields to the TextFiller class' public interface. You may, however, add any private fields or methods that you like.
- Your classes and therefore source files must be named exactly as described above (and in the solution skeleton), and your submission should mimic the solution skeleton's package structure.


# Hints
The implementation of this assignment requires you to make some design decisions. However, here are some hints for how you might structure your own.
- The above methods can be implemented iteratively or using recursion, though some methods will be much easier with a clever choice of one over the other.
- Want to use recursion to implement a method but need different parameters? Make a private helper method and then just call that helper method from the public one!
- If attempting to solve add iteratively, consider separating the task into 2 steps:
	 1.  find the prefix of the newTerm already stored within, and then 
	 2. add any new Nodes in a subtree consisting of the remaining suffix (like the example in the first part of the spec with "bard")
- If attempting to solve add recursively, consider adding Nodes in a fashion similar to how we recursively added Nodes to our simple Binary Search Tree of ints during class.
- Although there are only a few methods for you to implement in this assignment, beware: some of the algorithms may feel non-trivial, especially if you are unused to recursion. Leave yourself ample time to test, debug, and ask questions.

Assignment created by Andrew Forney
