package lockerline;

import java.time.Instant;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;

public final class DwellPolicy {
    /**
     * Three days, as the receipt tells the customer. The courier round that empties returns runs
     * at 06:00, so a return marked at midnight waits for it.
     */
    static final int LIMIT_DAYS = 3;

    private final ZoneId site;

    public DwellPolicy(ZoneId site) {
        this.site = site;
    }

    /**
     * Counted in local calendar days at the bank's site from the door latching (ADR-0004), so a
     * parcel dropped at 23:59 has a dwell time of one day at midnight.
     */
    public int dwellDays(Instant latchedAt, Instant now) {
        return (int) ChronoUnit.DAYS.between(latchedAt.atZone(site).toLocalDate(), now.atZone(site).toLocalDate());
    }

    public boolean returnToSender(Instant latchedAt, Instant now) {
        return dwellDays(latchedAt, now) >= LIMIT_DAYS;
    }
}
