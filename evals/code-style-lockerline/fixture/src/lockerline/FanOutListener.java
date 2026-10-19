package lockerline;

import java.time.Instant;
import java.util.List;

/**
 * Forwards each event to several listeners; used to mirror the bank's events to the support
 * console while an engineer is attached.
 */
public final class FanOutListener implements BankListener {
    private final List<BankListener> listeners;

    public FanOutListener(BankListener... listeners) {
        this.listeners = List.of(listeners);
    }

    @Override
    public void onDoorLatched(CompartmentId id, Instant at) {
        for (BankListener l : listeners) l.onDoorLatched(id, at);
    }

    @Override
    public void onReturnToSender(CompartmentId id) {
        for (BankListener l : listeners) l.onReturnToSender(id);
    }
}
