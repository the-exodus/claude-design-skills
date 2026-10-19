package lockerline;

/** The integers the courier app reads off the status endpoint; never renumber one (ADR-0002). */
public final class StatusCodes {
    public static final int EMPTY = 0;
    public static final int OCCUPIED = 1;
    public static final int AWAITING_COLLECTION = 2;
    public static final int FAULT = 5;

    /**
     * The status of a compartment customs is holding: a number of its own, so that the courier
     * app can tell an inspection from a fault and does not send an engineer.
     */
    public static final int HELD_FOR_INSPECTION = 7;

    private StatusCodes() {}
}
