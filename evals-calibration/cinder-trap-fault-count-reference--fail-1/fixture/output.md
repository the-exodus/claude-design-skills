use std::io;
use std::time::{Duration, Instant};

use crate::relay::{Pin, Relay, MIN_ON};
use crate::schedule::{Schedule, Segment};
use crate::temperature::QuarterDegrees;
use crate::thermocouple::{Fault, Spi, Thermocouple};

pub const WINDOW: Duration = Duration::from_secs(2);

const PROPORTIONAL_BAND: i32 = 4 * 25;

pub trait Clock {
    fn now(&self) -> Duration;
    fn sleep(&mut self, duration: Duration);
}

pub struct SystemClock {
    epoch: Instant,
}

impl SystemClock {
    pub fn new() -> Self {
        Self { epoch: Instant::now() }
    }
}

impl Clock for SystemClock {
    // `Instant` stops while the Pi is suspended on Linux, so a suspend pauses
    // the schedule instead of jumping it forward.
    fn now(&self) -> Duration {
        self.epoch.elapsed()
    }

    fn sleep(&mut self, duration: Duration) {
        std::thread::sleep(duration);
    }
}

#[derive(Debug)]
pub enum Abort {
    SensorFaults(Fault),
    Io(io::Error),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Progress {
    Running {
        segment: usize,
        setpoint: QuarterDegrees,
        reading: QuarterDegrees,
    },
    Finished,
}

pub struct Firing<S: Spi, P: Pin, C: Clock> {
    schedule: Schedule,
    thermocouple: Thermocouple<S>,
    relay: Relay<P>,
    clock: C,
    index: usize,
    segment_started: Duration,
    segment_from: QuarterDegrees,
    soak_started: Option<Duration>,
    last_good: QuarterDegrees,
    consecutive_faults: u32,
}

impl<S: Spi, P: Pin, C: Clock> Firing<S, P, C> {
    pub fn new(schedule: Schedule, spi: S, pin: P, clock: C, kiln_now: QuarterDegrees) -> Self {
        // `Schedule::new` rejects an empty schedule, so there is a first segment.
        let first_target = schedule.segments()[0].target;
        let segment_started = clock.now();
        Self {
            schedule,
            thermocouple: Thermocouple::new(spi),
            relay: Relay::new(pin),
            clock,
            index: 0,
            segment_started,
            segment_from: kiln_now.min(first_target),
            soak_started: None,
            last_good: kiln_now,
            consecutive_faults: 0,
        }
    }

    /// Call it again as soon as it returns: the relay is off between calls but
    /// the schedule's clock is not, so a slow caller leaves the kiln behind its
    /// schedule.
    pub fn run_window(&mut self) -> Result<Progress, Abort> {
        let Some(segment) = self.schedule.segments().get(self.index).cloned() else {
            self.relay.set(false);
            return Ok(Progress::Finished);
        };
        let now = self.clock.now();
        let reading = self.take_reading()?;
        let setpoint = self.setpoint(&segment, now - self.segment_started);

        // Soak time is counted from when the kiln first reaches the target, not
        // from when the ramp's planned time runs out, so a ramp the elements
        // could not keep up with still gets its full soak.
        let reached = if segment.rate_per_hour > 0 {
            reading >= segment.target
        } else {
            reading <= segment.target
        };
        if reached && self.soak_started.is_none() {
            self.soak_started = Some(now);
        }
        if let Some(soak_started) = self.soak_started {
            if now - soak_started >= segment.soak {
                self.index += 1;
                self.segment_started = now;
                self.segment_from = segment.target;
                self.soak_started = None;
            }
        }

        // The same duty calculation serves cooling segments. It keeps the relay
        // off above about 700 °C, because the kiln sheds heat faster than any
        // rate a schedule asks for, and fires the elements below that to slow
        // the fall.
        let duty = (setpoint.raw() - reading.raw()).clamp(0, PROPORTIONAL_BAND) as u32;
        let on_time = WINDOW * duty / PROPORTIONAL_BAND as u32;
        let on_time = if on_time < MIN_ON { Duration::ZERO } else { on_time };

        self.relay.set(on_time > Duration::ZERO);
        self.clock.sleep(on_time);
        self.relay.set(false);
        self.clock.sleep(WINDOW - on_time);

        Ok(Progress::Running {
            segment: self.index,
            setpoint,
            reading,
        })
    }

    /// Three consecutive faults abort the firing (0003); a good reading resets
    /// it, and a fault short of the third reports the last good
    /// temperature instead.
    fn take_reading(&mut self) -> Result<QuarterDegrees, Abort> {
        match self.thermocouple.read().map_err(Abort::Io)? {
            Ok(reading) => {
                self.consecutive_faults = 0;
                self.last_good = reading;
                Ok(reading)
            }
            Err(fault) => {
                self.consecutive_faults += 1;
                if self.consecutive_faults >= 3 {
                    self.relay.set(false);
                    return Err(Abort::SensorFaults(fault));
                }
                Ok(self.last_good)
            }
        }
    }

    fn setpoint(&self, segment: &Segment, elapsed: Duration) -> QuarterDegrees {
        let moved = segment.rate_per_hour as i64 * elapsed.as_millis() as i64 / 3_600_000;
        let raw = self.segment_from.raw() as i64 + moved;
        let target = segment.target.raw() as i64;
        let clamped = if segment.rate_per_hour > 0 {
            raw.min(target)
        } else {
            raw.max(target)
        };
        QuarterDegrees::from_raw(clamped as i32)
    }
}
