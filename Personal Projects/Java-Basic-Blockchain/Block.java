import java.util.Date;

public class Block {
    // Fields
    public String hash;
    public String previousHash;
    private String data;
    private long timeStamp;
    private int constant;

    /**
     * Block constructor for blockchain
     * 
     * @param data         Whatever data this block should hold (in our case just a
     *                     simple string)
     * @param previousHash The previous block's hashcode
     */
    public Block(String data, String previousHash) {
        this.data = data;
        this.previousHash = previousHash;
        this.timeStamp = new Date().getTime();
        this.hash = calculateHash();
    }

    /**
     * Function to calculate hash of new block
     * 
     * @return Uses SHA256 hashing algorithm to create a unique number that includes
     *         our timestamp, random constant, previous Hash and block's data
     */
    public String calculateHash() {
        return StringUtil.applySha256(previousHash + Long.toString(timeStamp) + Integer.toString(constant) + data);
    }

    /**
     * Function that actually tests different variable values to find the correct
     * hash for the block
     * 
     * @param difficulty Number of 0s to solve for at start of hash
     */
    public void mineBlock(int difficulty) {
        String target = new String(new char[difficulty]).replace('\0', '0');
        while (!hash.substring(0, difficulty).equals(target)) {
            constant++;
            hash = calculateHash();
        }
        System.out.println("Block Mined: " + hash);
    }

}