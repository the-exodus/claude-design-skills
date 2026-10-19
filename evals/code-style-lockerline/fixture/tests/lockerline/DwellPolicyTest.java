package lockerline;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.time.Instant;
import java.time.ZoneId;
import org.junit.jupiter.api.Test;

class DwellPolicyTest {
    // The bank's zone; clocks go forward on 2026-03-29, so that day is 23 hours long there
    private final DwellPolicy policy = new DwellPolicy(ZoneId.of("Europe/Oslo"));

    @Test
    void a_parcel_dropped_one_second_before_midnight_has_a_day_at_midnight() {
        Instant latched = Instant.parse("2026-03-02T22:59:59Z"); // 23:59:59 at the site
        assertEquals(1, policy.dwellDays(latched, Instant.parse("2026-03-02T23:00:00Z")));
    }

    @Test
    void the_short_day_counts_as_one() {
        Instant latched = Instant.parse("2026-03-28T12:00:00Z");
        assertEquals(2, policy.dwellDays(latched, Instant.parse("2026-03-30T08:00:00Z")));
    }
}
