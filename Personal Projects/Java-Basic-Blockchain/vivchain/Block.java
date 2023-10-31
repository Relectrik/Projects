package vivchain;

import java.util.Date;
import java.util.ArrayList;

public class Block {
    // Fields
    public String hash;
    public String previousHash;
    public String merkleRoot;
    public ArrayList<Transaction> transactions = new ArrayList<Transaction>();
    private long timeStamp;
    private int constant;

    /**
     * Block constructor for blockchain
     * 
     * @param previousHash The previous block's hashcode
     */
    public Block(String previousHash) {
        this.previousHash = previousHash;
        this.timeStamp = new Date().getTime();
        this.hash = calculateHash();
    }

    /**
     * Function to calculate hash of new block
     * 
     * @return Uses SHA256 hashing algorithm to create a unique number that includes
     *         our timestamp, random constant, previous Hash and block's merkle root
     */
    public String calculateHash() {
        return StringUtil
                .applySha256(previousHash + Long.toString(timeStamp) + Integer.toString(constant) + merkleRoot);
    }

    /**
     * Function that actually tests different variable values to find the correct
     * hash for the block
     * 
     * @param difficulty Number of 0s to solve for at start of hash
     */
    public void mineBlock(int difficulty) {
        merkleRoot = StringUtil.getMerkleRoot(transactions);
        String target = new String(new char[difficulty]).replace('\0', '0');
        while (!hash.substring(0, difficulty).equals(target)) {
            constant++;
            hash = calculateHash();
        }
        System.out.println("Block Mined: " + hash);
    }

    /**
     * Add the transaction to the list of transactions in the block
     * 
     * @param transaction Transaction to be added
     * @return Boolean indicating whether it has been added or not
     */
    public boolean addTransaction(Transaction transaction) {
        if (transaction == null) {
            return false;
        }
        if (previousHash != "0") {
            if (transaction.processTransaction() != true) {
                System.out.println("Failure processing Transaction");
                return false;
            }
        }
        transactions.add(transaction);
        System.out.println("Transaction added to block.");
        return true;
    }

}