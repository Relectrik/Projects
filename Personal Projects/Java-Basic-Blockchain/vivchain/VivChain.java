package vivchain;

import java.util.ArrayList;
import com.google.gson.GsonBuilder;
import java.util.Base64;
import java.security.Security;
import java.util.HashMap;

// Adapted heavily from https://medium.com/programmers-blockchain/creating-your-first-blockchain-with-java-part-2-transactions-2cdac335e0ce
// [CREDIT TO CODER KASS]
// Personal Project trying to improve my Java skills and see how it can be used to implement a simple blockchain

public class VivChain {

    public static ArrayList<Block> blockchain = new ArrayList<Block>();
    public static HashMap<String, TransactionOutput> UTXOs = new HashMap<String, TransactionOutput>();

    public static int difficulty = 2;
    public static float minimumTransaction = 0.1f;
    public static Wallet wallet_Alice;
    public static Wallet wallet_Bob;
    public static Transaction beginningTransaction;

    // Testing
    public static void main(String[] args) {
        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());

        wallet_Alice = new Wallet();
        wallet_Bob = new Wallet();
        Wallet coinbase = new Wallet();

        beginningTransaction = new Transaction(coinbase.publicKey, wallet_Alice.publicKey, 100f, null);
        beginningTransaction.generateSignature(coinbase.privateKey);
        beginningTransaction.transactionId = "0";
        beginningTransaction.outputs.add(new TransactionOutput(beginningTransaction.recipient,
                beginningTransaction.value, beginningTransaction.transactionId));
        UTXOs.put(beginningTransaction.outputs.get(0).id, beginningTransaction.outputs.get(0));

        System.out.println("Creating and Mining Genesis block... ");
        Block genesis = new Block("0");
        genesis.addTransaction(beginningTransaction);
        addBlock(genesis);

        Block block1 = new Block(genesis.hash);
        System.out.println("\nAlice's balance is: " + wallet_Alice.getBalance());
        System.out.println("\nAlice is attempting to send funds (40) to Bob...");
        block1.addTransaction(wallet_Alice.sendFunds(wallet_Bob.publicKey, 40f));
        addBlock(block1);
        System.out.println("\nAlice's balance is: " + wallet_Alice.getBalance());
        System.out.println("Bob's balance is: " + wallet_Bob.getBalance());

        Block block2 = new Block(block1.hash);
        System.out.println("\nAlice Attempting to send more funds (1000) than it has...");
        block2.addTransaction(wallet_Alice.sendFunds(wallet_Bob.publicKey, 1000f));
        addBlock(block2);
        System.out.println("\nAlice's balance is: " + wallet_Alice.getBalance());
        System.out.println("Bob's balance is: " + wallet_Bob.getBalance());

        Block block3 = new Block(block2.hash);
        System.out.println("\nBob is Attempting to send funds (20) to Alice...");
        block3.addTransaction(wallet_Bob.sendFunds(wallet_Alice.publicKey, 20));
        System.out.println("\nAlice's balance is: " + wallet_Alice.getBalance());
        System.out.println("Bob's balance is: " + wallet_Bob.getBalance());

        isChainValid();
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
        HashMap<String, TransactionOutput> tempUTXOs = new HashMap<String, TransactionOutput>();
        tempUTXOs.put(beginningTransaction.outputs.get(0).id, beginningTransaction.outputs.get(0));

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

            TransactionOutput tempOutput;
            for (int j = 0; j < currentBlock.transactions.size(); j++) {
                Transaction currentTransaction = currentBlock.transactions.get(j);

                if (!currentTransaction.verifySignature()) {
                    System.out.println("Signature on Transaction(" + j + ") is invalid");
                    return false;
                }
                if (currentTransaction.getInputsValue() != currentTransaction.getOutputsValue()) {
                    System.out.println("Inputs do not match outputs on Transaction (" + j + ")");
                    return false;
                }

                for (TransactionInput input : currentTransaction.inputs) {
                    tempOutput = tempUTXOs.get(input.transactionOutputId);

                    if (tempOutput == null) {
                        System.out.println("Referenced input on Transaction (" + j + ") does not exist");
                        return false;
                    }

                    if (input.UTXO.value != tempOutput.value) {
                        System.out.println("Referenced input Transaction (" + j + ") is invalid");
                        return false;
                    }

                    tempUTXOs.remove(input.transactionOutputId);
                }

                for (TransactionOutput output : currentTransaction.outputs) {
                    tempUTXOs.put(output.id, output);
                }

                if (currentTransaction.outputs.get(0).recipient != currentTransaction.recipient) {
                    System.out.println("Recipients do not match in Transaction (" + j + ")");
                    return false;
                }

                if (currentTransaction.outputs.get(1).recipient != currentTransaction.sender) {
                    System.out.println("Output 'change' is not sender in Transaction (" + j + ")");
                    return false;
                }
            }
        }
        System.out.println("Valid Blockchain");
        return true;
    }

    public static void addBlock(Block newBlock) {
        newBlock.mineBlock(difficulty);
        blockchain.add(newBlock);
    }
}
