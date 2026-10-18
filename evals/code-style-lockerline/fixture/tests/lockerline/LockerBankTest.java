package lockerline;

import static lockerline.CompartmentSize.MEDIUM;
import static lockerline.CompartmentSize.SMALL;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;

/**
 * A drop-off is accepted only into an empty compartment of the right size, and the dwell clock
 * starts when the door latches, not at the scan. A collection code opens its compartment once;
 * three failed scans lock the compartment out until the next courier round.
 */
class LockerBankTest {
    private static final ZoneId OSLO = ZoneId.of("Europe/Oslo");
    private final FakeLockBoard board = new FakeLockBoard();

    private LockerBank bankWithOneEmpty(CompartmentSize size, Instant now) {
        Clock clock = Clock.fixed(now, ZoneOffset.UTC);
        LockerBank bank = new LockerBank(new ReservationLedger(), new DwellPolicy(OSLO), Runnable::run, clock);
        CompartmentController controller = new CompartmentController(board, bank, clock, "depot", 1);
        bank.attach(controller, new Compartment(new CompartmentId("depot", 1), size));
        return bank;
    }

    @Test
    void refuses_a_parcel_too_big_for_the_compartment() {
        // Arrange a bank with one empty small compartment
        var bank = bankWithOneEmpty(SMALL, Instant.parse("2026-03-02T09:00:00Z"));
        assertFalse(bank.acceptDropOff(new CompartmentId("depot", 1), MEDIUM, "courier-7"));
        assertEquals(0, board.releases);
    }

    @Test
    void dwell_clock_starts_at_the_latch() {
        var bank = bankWithOneEmpty(MEDIUM, Instant.parse("2026-03-02T09:00:00Z"));
        var id = new CompartmentId("depot", 1);
        assertTrue(bank.acceptDropOff(id, MEDIUM, "courier-7"));
        // The clock starts at the latch, not the scan (ADR-0004): here the scan is two minutes earlier
        Instant latched = Instant.parse("2026-03-02T09:02:00Z");
        bank.onDoorLatched(id, latched);
        assertFalse(new DwellPolicy(OSLO).returnToSender(latched, Instant.parse("2026-03-04T22:59:59Z")));
    }

    @Test
    void three_failed_scans_lock_the_compartment_out() {
        var bank = bankWithOneEmpty(MEDIUM, Instant.parse("2026-03-02T09:00:00Z"));
        var id = new CompartmentId("depot", 1);
        bank.acceptDropOff(id, MEDIUM, "courier-7");
        bank.onDoorLatched(id, Instant.parse("2026-03-02T09:02:00Z"));
        for (int i = 0; i < 3; i++) assertFalse(bank.onCodeScanned(id, "WRONG1"));
        assertEquals(1, board.releases); // only the courier's release; no scan opened the door
    }
}
