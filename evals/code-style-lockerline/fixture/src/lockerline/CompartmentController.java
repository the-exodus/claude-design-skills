package lockerline;

import java.time.Clock;
import java.util.HashMap;
import java.util.Map;

/**
 * Runs on the lock board's own thread. It reports to the bank through BankListener and never
 * calls the courier API (ADR-0001).
 */
public final class CompartmentController implements Runnable {
    private final LockBoard board;
    private final BankListener listener;
    private final Clock clock;
    private final String bank;
    private final int doors;
    private final Map<Integer, Boolean> lastLatched = new HashMap<>();

    public CompartmentController(LockBoard board, BankListener listener, Clock clock, String bank, int doors) {
        this.board = board;
        this.listener = listener;
        this.clock = clock;
        this.bank = bank;
        this.doors = doors;
    }

    /** Polls every 200 ms: the board raises no interrupt when a latch changes. */
    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            for (int door = 1; door <= doors; door++) {
                boolean latched = board.latched(door);
                if (latched && !lastLatched.getOrDefault(door, true)) {
                    listener.onDoorLatched(new CompartmentId(bank, door), clock.instant());
                }
                lastLatched.put(door, latched);
            }
            sleep(200);
        }
    }

    public boolean release(int door) {
        sleep(40); // the board drops a command that arrives within 30 ms of the one before
        return board.release(door);
    }

    private static void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
