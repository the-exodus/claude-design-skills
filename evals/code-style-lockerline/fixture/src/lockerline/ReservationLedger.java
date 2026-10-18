package lockerline;

import java.util.HashMap;
import java.util.Map;

final class ReservationLedger {
    /**
     * Held across the check and the insert: two couriers scanning the same compartment within a
     * second is the normal case at the depot bank.
     */
    private final Object lock = new Object();

    private final Map<CompartmentId, String> openByCompartment = new HashMap<>();

    boolean reserve(CompartmentId id, String courier) {
        synchronized (lock) {
            if (openByCompartment.containsKey(id)) return false;
            openByCompartment.put(id, courier);
            return true;
        }
    }

    void free(CompartmentId id) {
        synchronized (lock) {
            openByCompartment.remove(id);
        }
    }
}
