package lockerline;

import java.time.Instant;

public interface BankListener {
    /**
     * The door has latched and the sensor's debounce has run: the bank starts the dwell clock
     * from this moment, not from the courier's scan. Called on the lock-board thread.
     */
    void onDoorLatched(CompartmentId id, Instant at);

    void onReturnToSender(CompartmentId id);
}
