package lockerline;

public interface LockBoard {
    /**
     * The board answers ACK before the solenoid has moved, so true means only that the command
     * arrived; the latch sensor is the only evidence that the door opened.
     */
    boolean release(int door);

    boolean latched(int door);
}
