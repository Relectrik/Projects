package vivchain;

import java.security.*;
import java.util.ArrayList;

public class Transaction {
    public String transactionId;
    public PublicKey sender;
    public PublicKey recipient;
    public float value;
    public byte[] signature;

    public ArrayList<TransactionInput> inputs = new ArrayList<TransactionInput>();
    public ArrayList<TransactionOutput> outputs = new ArrayList<TransactionOutput>();

    private static int sequence = 0;

    /**
     * Transaction object constructor
     * 
     * @param from   Public Key of Sender
     * @param to     Public Key of recipient
     * @param value  Amount of funds to be transferred
     * @param inputs References to previous transactions as proof of funds
     */
    public Transaction(PublicKey from, PublicKey to, float value, ArrayList<TransactionInput> inputs) {
        this.sender = from;
        this.recipient = to;
        this.value = value;
        this.inputs = inputs;
    }

    /**
     * Calculates transaction hash code which will be used as the transaction's ID
     * 
     * @return The Hash code
     */
    private String calculateHash() {
        sequence++;
        return StringUtil.applySha256(StringUtil.getStringFromKey(sender) + StringUtil.getStringFromKey(recipient)
                + Float.toString(value) + sequence);
    }

    /**
     * Generates the signature of transaction and changes the field accordingly.
     * 
     * @param privateKey Private Key of sender
     */
    public void generateSignature(PrivateKey privateKey) {
        String data = StringUtil.getStringFromKey(sender) + StringUtil.getStringFromKey(recipient)
                + Float.toString(value);
        signature = StringUtil.applyECDSASig(privateKey, data);
    }

    /**
     * Verifies the signature of transaction to avoid fraudulent transcations.
     * 
     * @return Returns a Boolean indicating the validity of the transaction.
     */
    public boolean verifySignature() {
        String data = StringUtil.getStringFromKey(sender) + StringUtil.getStringFromKey(recipient)
                + Float.toString(value);
        return StringUtil.verifyECDSASig(sender, data, signature);
    }

    /**
     * Performs checks to see if the transaction can be processed:
     * 1. Checks if signature can be verified. If not return false.
     * 2. Checks if sum of input(UTXOs) values is less than set minimum transaction.
     * If so, return false.
     * 3. If neither false, checks go through, perform necessary additions to
     * TransactionInput and TransactionOutput, and also remove transaction inputs
     * from UTXO lists (as spent) then return true (Transaction CAN be
     * processed)
     * 
     * @return Boolean indicating whether transacation is okay.
     */
    public boolean processTransaction() {
        if (!verifySignature()) {
            System.out.println("Transaction signature failed to verify");
            return false;
        }

        for (TransactionInput input : inputs) {
            input.UTXO = VivChain.UTXOs.get(input.transactionOutputId);
        }

        if (getInputsValue() < VivChain.minimumTransaction) {
            System.out.println("Transaction Input is too small: " + getInputsValue());
            return false;
        }

        float leftOver = getInputsValue() - value;
        transactionId = calculateHash();
        outputs.add(new TransactionOutput(this.recipient, value, transactionId));
        outputs.add(new TransactionOutput(this.sender, value, transactionId));

        for (TransactionOutput output : outputs) {
            VivChain.UTXOs.put(output.id, output);
        }

        for (TransactionInput input : inputs) {
            if (input.UTXO == null) {
                continue;
            }
            VivChain.UTXOs.remove(input.UTXO.id);
        }

        return true;
    }

    /**
     * Calculates sum of input values
     * 
     * @return Sum of inputs
     */
    public float getInputsValue() {
        float total = 0;
        for (TransactionInput input : inputs) {
            if (input.UTXO == null) {
                continue;
            }
            total += input.UTXO.value;
        }
        return total;
    }

    /**
     * Calculates sum of output values
     * 
     * @return Sum of outputs
     */
    public float getOutputsValue() {
        float total = 0;
        for (TransactionOutput output : outputs) {
            total += output.value;
        }
        return total;
    }
}
