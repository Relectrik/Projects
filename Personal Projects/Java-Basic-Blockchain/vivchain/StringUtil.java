package vivchain;

import java.security.*;
import java.util.Base64;
import java.util.*;

public class StringUtil {
    /**
     * Applies SHA-256 Hashing algorithm to our block's data
     * 
     * @param input String of data
     * @return Hashcode for block
     */
    public static String applySha256(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(input.getBytes("UTF-8"));
            StringBuffer hexString = new StringBuffer();
            for (int i = 0; i < hash.length; i++) {
                String hex = Integer.toHexString(0xff & hash[i]);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Unique signature from sender to ensure that the unique transaction the sender
     * intends actually takes place.
     *
     * @param privateKey Private Key of sender
     * @param input      Data inclusive of both sender and recipients' private keys
     *                   and value to be sent
     * @return
     */
    public static byte[] applyECDSASig(PrivateKey privateKey, String input) {
        Signature dsa;
        byte[] output = new byte[0];
        try {
            dsa = Signature.getInstance("ECDSA", "BC");
            dsa.initSign(privateKey);
            byte[] strByte = input.getBytes();
            dsa.update(strByte);
            byte[] realSig = dsa.sign();
            output = realSig;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return output;
    }

    /**
     * Verify the signature of the transaction
     * 
     * @param publicKey Public Key of sender
     * @param data      Data inclusive of both sender and recipients' private keys
     *                  and value to be sent
     * @param signature Signature established earlier to compare to
     * @return Boolean indicating validity of signature
     */
    public static boolean verifyECDSASig(PublicKey publicKey, String data, byte[] signature) {
        try {
            Signature ecdsaVerify = Signature.getInstance("ECDSA", "BC");
            ecdsaVerify.initVerify(publicKey);
            ecdsaVerify.update(data.getBytes());
            return ecdsaVerify.verify(signature);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Encodes a key into a String
     * 
     * @param key A Private or Public Key to encode
     * @return String version of key
     */
    public static String getStringFromKey(Key key) {
        return Base64.getEncoder().encodeToString(key.getEncoded());
    }

    /**
     * Simple mathematical way to verify the data on a Merkle tree. Used in
     * cryptocurrency to make sure data blocks passed between people are unaltered
     * 
     * @param transactions List of transactions
     * @return The merkleroot
     */
    public static String getMerkleRoot(ArrayList<Transaction> transactions) {
        int count = transactions.size();
        ArrayList<String> previousTreeLayer = new ArrayList<String>();
        for (Transaction transaction : transactions) {
            previousTreeLayer.add(transaction.transactionId);
        }
        ArrayList<String> treeLayer = previousTreeLayer;
        while (count > 1) {
            treeLayer = new ArrayList<String>();
            for (int i = 0; i < previousTreeLayer.size(); i++) {
                treeLayer.add(applySha256(previousTreeLayer.get(i - 1) + previousTreeLayer.get(i)));
            }
            count = treeLayer.size();
            previousTreeLayer = treeLayer;
        }
        String merkleRoot = (treeLayer.size() == 1) ? treeLayer.get(0) : "";
        return merkleRoot;
    }
}
