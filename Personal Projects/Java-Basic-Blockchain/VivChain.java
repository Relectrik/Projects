import java.util.ArrayList;
import com.google.gson.GsonBuilder;

public class VivChain {

    public static ArrayList<Block> blockchain = new ArrayList<Block>();
    public static int difficulty = 1;

    public static void main(String[] args) {
        blockchain.add(new Block("First block", "0"));
        System.out.println("Trying to mine block 1...");
        blockchain.get(0).mineBlock(difficulty);

        blockchain.add(new Block("second block", blockchain.get(blockchain.size() - 1).hash));
        System.out.println("Trying to mine block 2...");
        blockchain.get(1).mineBlock(difficulty);

        blockchain.add(new Block("third block", blockchain.get(blockchain.size() - 1).hash));
        System.out.println("Trying to mine block 3...");
        blockchain.get(2).mineBlock(difficulty);

        System.out.println("\nBlockchain is Valid:" + isChainValid());

        String blockchainJson = new GsonBuilder().setPrettyPrinting().create().toJson(blockchain);
        System.out.println("\nCurrent blockchain: ");
        System.out.println(blockchainJson);
    }

    /**
     * Checks if chain is valid by comparing hash values of previous and current
     * blocks but also checks if a block has yet to be mined
     * 
     * @return Boolean value indiciating validity of blockchain
     */
    public static Boolean isChainValid() {
        Block currentBlock;
        Block previousBlock;
        String hashTarget = new String(new char[difficulty]).replace('\0', '0');

        for (int i = 1; i < blockchain.size(); i++) {
            currentBlock = blockchain.get(i);
            previousBlock = blockchain.get(i - 1);

            if (!currentBlock.hash.equals(currentBlock.calculateHash())) {
                System.out.println("Current hashes NOT equal");
                return false;
            }

            if (!previousBlock.hash.equals(currentBlock.previousHash)) {
                System.out.println("Previous hashes NOT equal");
                return false;
            }

            if (!currentBlock.hash.substring(0, difficulty).equals(hashTarget)) {
                System.out.println("This block hasn't been mined");
                return false;
            }
        }
        return true;
    }
}
