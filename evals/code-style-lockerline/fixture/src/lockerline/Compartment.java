package lockerline;

import java.time.Instant;

public final class Compartment {
    private final CompartmentId id;
    private final CompartmentSize size;
    private Instant latchedAt;

    /**
     * Held only until the door is opened with it, then cleared, so that a reprinted receipt
     * cannot open the compartment a second time.
     */
    private char[] collectionCode;

    Compartment(CompartmentId id, CompartmentSize size) {
        this.id = id;
        this.size = size;
    }

    public CompartmentId id() {
        return id;
    }

    /** Returns the compartment's size. */
    public CompartmentSize size() {
        return size;
    }

    public boolean isEmpty() {
        return latchedAt == null;
    }

    Instant latchedAt() {
        return latchedAt;
    }

    char[] collectionCode() {
        return collectionCode;
    }

    void occupy(Instant latchedAt, char[] collectionCode) {
        this.latchedAt = latchedAt;
        this.collectionCode = collectionCode;
    }

    void empty() {
        latchedAt = null;
        collectionCode = null;
    }
}
