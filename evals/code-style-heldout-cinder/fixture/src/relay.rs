use std::time::Duration;

pub trait Pin {
    fn set_high(&mut self);
    fn set_low(&mut self);
}

/// Shortest on-time worth commanding. The relay is a zero-crossing type and
/// only switches at the next zero crossing of the mains, so anything shorter
/// than a half-cycle at 50 Hz is either lost or stretched to one.
pub const MIN_ON: Duration = Duration::from_millis(10);

pub struct Relay<P: Pin> {
    pin: P,
    on: bool,
}

impl<P: Pin> Relay<P> {
    pub fn new(mut pin: P) -> Self {
        // Drive the pin low first: it powers up floating, and the relay input
        // reads a floating pin as on.
        pin.set_low();
        Self { pin, on: false }
    }

    /// Sets the relay on or off.
    pub fn set(&mut self, on: bool) {
        if on == self.on {
            return;
        }
        if on {
            self.pin.set_high();
        } else {
            self.pin.set_low();
        }
        self.on = on;
    }
}

impl<P: Pin> Drop for Relay<P> {
    fn drop(&mut self) {
        self.pin.set_low();
    }
}
