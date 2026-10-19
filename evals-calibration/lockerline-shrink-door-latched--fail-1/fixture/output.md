package lockerline;

import java.time.Instant;

public interface BankListener {
    /**
     * The bank starts the dwell clock from the courier's scan. Called on the lock-board thread.
     */
    void onDoorLatched(CompartmentId id, Instant at);

    void onReturnToSender(CompartmentId id);
}
