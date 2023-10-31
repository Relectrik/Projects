package vivchain;

public class TransactionInput {
    public String transactionOutputId;
    public TransactionOutput UTXO;

    /**
     * Constructor for Transaction Inputs (References to previous transactions)
     * 
     * @param transactionOutputId Reference to TransactionOutput
     */
    public TransactionInput(String transactionOutputId) {
        this.transactionOutputId = transactionOutputId;
    }
}
