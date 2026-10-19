package lockerline;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;

final class CollectionCodes {
    private static final String ALPHABET = "ACDEFHJKMNPRTUVWXY34679"; // no character a customer can misread on the thermal receipt

    /**
     * Six characters: the scanner's keypad fallback gives up after eight seconds, and six is what
     * customers in the field trial typed in that time.
     */
    static final int LENGTH = 6;

    private final SecureRandom random = new SecureRandom();

    char[] next() {
        char[] code = new char[LENGTH];
        for (int i = 0; i < LENGTH; i++) code[i] = ALPHABET.charAt(random.nextInt(ALPHABET.length()));
        return code;
    }

    static boolean matches(char[] expected, String scanned) {
        if (expected == null) return false;
        byte[] a = new String(expected).getBytes(StandardCharsets.US_ASCII);
        byte[] b = scanned.getBytes(StandardCharsets.US_ASCII);
        // See ADR-0003.
        return MessageDigest.isEqual(a, b);
    }
}
