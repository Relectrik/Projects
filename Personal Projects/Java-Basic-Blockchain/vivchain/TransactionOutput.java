package vivchain;

import java.security.PublicKey;

public class TransactionOutput {
    public String id;
    public PublicKey recipient;
    public float value;
    public String parentTransactionId;

    /**
     * Creates TransactionOutput object that will show final amount sent to each
     * party from the transaction
     * 
     * @param recipient           Public Key of recipient
     * @param value               Value to be sent
     * @param parentTransactionId ID of Transaction this output was created in
     */
    public TransactionOutput(PublicKey recipient, float value, String parentTransactionId) {
        this.recipient = recipient;
        this.value = value;
        this.parentTransactionId = parentTransactionId;
        this.id = StringUtil
                .applySha256(StringUtil.getStringFromKey(recipient) + Float.toString(value) + parentTransactionId);
    }

    /**
     * Check if keys match and thus if coin belongs to you
     * 
     * @param publicKey Public key of recipient
     * @return Boolean indicating whether the keys match
     */
    public boolean isMine(PublicKey publicKey) {
        return (publicKey.equals(recipient));
    }
}
