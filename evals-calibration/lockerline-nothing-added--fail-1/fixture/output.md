package lockerline;

import java.time.Clock;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.logging.Logger;

/**
 * State changes only on the bank's own executor, never on the lock-board thread, which is why
 * every listener call is posted to it. A refused drop-off keeps its reservation for the courier's next try.
 */
public final class LockerBank implements BankListener {
    private static final Logger LOG = Logger.getLogger(LockerBank.class.getName());

    private final Map<CompartmentId, Compartment> compartments = new HashMap<>();
    private final Map<CompartmentId, Integer> failedScans = new HashMap<>();
    private final ReservationLedger ledger; // at most one open reservation per compartment: the ledger's lock holds that, not this class
    private final CollectionCodes codes = new CollectionCodes();
    private final DwellPolicy dwell;
    private final Executor executor;
    private final Clock clock;
    private CompartmentController controller;

    LockerBank(ReservationLedger ledger, DwellPolicy dwell, Executor executor, Clock clock) {
        this.ledger = ledger;
        this.dwell = dwell;
        this.executor = executor;
        this.clock = clock;
    }

    void attach(CompartmentController controller, Compartment... all) {
        this.controller = controller;
        for (Compartment c : all) compartments.put(c.id(), c);
    }

    public boolean acceptDropOff(CompartmentId id, CompartmentSize parcelSize, String courier) {
        Compartment c = compartments.get(id);
        if (c == null || !c.isEmpty() || c.size().compareTo(parcelSize) < 0) {
            LOG.info(() -> "refused drop-off at " + id);
            return false;
        }
        if (!ledger.reserve(id, courier)) return false;
        return controller.release(id.door());
    }

    @Override
    public void onDoorLatched(CompartmentId id, Instant at) {
        executor.execute(() -> {
            Compartment c = compartments.get(id);
            if (c != null && c.isEmpty()) completeDropOff(c, at);
        });
    }

    private void completeDropOff(Compartment c, Instant latchedAt) {
        c.occupy(latchedAt, codes.next());
        ledger.free(c.id());
        LOG.info(() -> "drop-off at " + c.id());
    }

    /**
     * The scanned code is compared with the compartment's code in constant time, since anyone
     * standing at the bank can time the scanner's beep.
     */
    public boolean onCodeScanned(CompartmentId id, String code) {
        Compartment c = compartments.get(id);
        if (c == null || !CollectionCodes.matches(c.collectionCode(), code)) {
            int failed = failedScans.merge(id, 1, Integer::sum);
            if (failed >= 3) lockOut(id); // three tries, as the printed receipt promises
            return false;
        }
        failedScans.remove(id);
        c.empty();
        return controller.release(id.door());
    }

    @Override
    public void onReturnToSender(CompartmentId id) {
        LOG.info(() -> "return to sender at " + id);
    }

    void sweep() {
        Instant now = clock.instant();
        for (Compartment c : compartments.values()) {
            if (!c.isEmpty() && dwell.returnToSender(c.latchedAt(), now)) onReturnToSender(c.id());
        }
    }

    private void lockOut(CompartmentId id) {
        LOG.warning(() -> "locked out " + id);
    }
}
