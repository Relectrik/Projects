package vivchain;

import java.security.*;
import java.security.spec.ECGenParameterSpec;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Wallet {
    public PrivateKey privateKey;
    public PublicKey publicKey;

    public HashMap<String, TransactionOutput> UTXOs = new HashMap<String, TransactionOutput>();

    public Wallet() {
        generateKeyPair();
    }

    /**
     * Generates private and public keys for wallet, and changes Wallet's fields
     * appropriately
     */
    public void generateKeyPair() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDSA", "BC");
            SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
            ECGenParameterSpec ecSpec = new ECGenParameterSpec("prime192v1");

            keyGen.initialize(ecSpec, random);
            KeyPair keyPair = keyGen.generateKeyPair();

            privateKey = keyPair.getPrivate();
            publicKey = keyPair.getPublic();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Returns balance and stores UTXOs owned by the wallet in the fields of the
     * object
     * 
     * @return Balance of wallet
     */
    public float getBalance() {
        float total = 0;
        for (Map.Entry<String, TransactionOutput> entry : VivChain.UTXOs.entrySet()) {
            TransactionOutput UTXO = entry.getValue();
            if (UTXO.isMine(publicKey)) {
                UTXOs.put(UTXO.id, UTXO);
                total += UTXO.value;
            }
        }
        return total;
    }

    /**
     * Generates and returns a new transaction from this wallet
     * 
     * @param recipient PublicKey of wallet receiving the transaction
     * @param value     Value to send
     * @return Transaction object from this wallet
     */
    public Transaction sendFunds(PublicKey _recipient, float value) {
        if (getBalance() < value) {
            System.out.println("You're broke lol. Transaction cannot go through.");
            return null;
        }

        ArrayList<TransactionInput> inputs = new ArrayList<TransactionInput>();

        float total = 0;
        for (Map.Entry<String, TransactionOutput> entry : UTXOs.entrySet()) {
            TransactionOutput UTXO = entry.getValue();
            total += UTXO.value;
            inputs.add(new TransactionInput(UTXO.id));
            if (total > value) {
                break;
            }
        }

        Transaction newTransaction = new Transaction(publicKey, _recipient, value, inputs);
        newTransaction.generateSignature(privateKey);

        for (TransactionInput input : inputs) {
            UTXOs.remove(input.transactionOutputId);
        }
        return newTransaction;
    }
}
