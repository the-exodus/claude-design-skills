package lockerline;

import java.util.HashSet;
import java.util.Set;

/**
 * A lock board the test drives: every release answers ACK at once, and a latch only reads as
 * open once the test says so, as the real sensor does after the solenoid has moved.
 */
final class FakeLockBoard implements LockBoard {
    private final Set<Integer> open = new HashSet<>();
    int releases;

    @Override
    public boolean release(int door) {
        releases++;
        return true;
    }

    @Override
    public boolean latched(int door) {
        return !open.contains(door);
    }

    void open(int door) {
        open.add(door);
    }

    void close(int door) {
        open.remove(door);
    }
}
