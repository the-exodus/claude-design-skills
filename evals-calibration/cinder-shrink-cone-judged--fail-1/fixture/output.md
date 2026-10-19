use std::time::Duration;

use crate::temperature::QuarterDegrees;

/// The kiln's rated maximum. The elements are rated higher, but the lid brick
/// is not.
pub const KILN_LIMIT: QuarterDegrees = QuarterDegrees::from_celsius(1300);

pub const MAX_SEGMENTS: usize = 8;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Segment {
    /// Quarter-degrees per hour. Positive heats and negative cools; never zero,
    /// and the sign must agree with the direction from the previous segment's
    /// target to this one's. `Schedule::new` checks both.
    pub rate_per_hour: i32,
    pub target: QuarterDegrees,
    pub soak: Duration,
}

#[derive(Debug, PartialEq, Eq)]
pub enum ScheduleError {
    Empty,
    TooManySegments,
    ZeroRate { segment: usize },
    RateAgainstTarget { segment: usize },
    HeatsAfterCooling { segment: usize },
    AboveKilnLimit { segment: usize },
}

#[derive(Clone, Debug)]
pub struct Schedule {
    segments: Vec<Segment>,
}

impl Schedule {
    /// Checks a schedule once, at load, so that the controller can follow it
    /// without re-checking anything (0004).
    pub fn new(segments: Vec<Segment>) -> Result<Self, ScheduleError> {
        if segments.is_empty() {
            return Err(ScheduleError::Empty);
        }
        if segments.len() > MAX_SEGMENTS {
            return Err(ScheduleError::TooManySegments);
        }
        let mut cooled = false;
        for (i, segment) in segments.iter().enumerate() {
            if segment.rate_per_hour == 0 {
                return Err(ScheduleError::ZeroRate { segment: i });
            }
            if segment.target > KILN_LIMIT {
                return Err(ScheduleError::AboveKilnLimit { segment: i });
            }
            let heats = segment.rate_per_hour > 0;
            let rises = i == 0 || segment.target > segments[i - 1].target;
            if heats != rises {
                return Err(ScheduleError::RateAgainstTarget { segment: i });
            }
            if heats && cooled {
                return Err(ScheduleError::HeatsAfterCooling { segment: i });
            }
            cooled |= !heats;
        }
        Ok(Self { segments })
    }

    pub fn segments(&self) -> &[Segment] {
        &self.segments
    }

    /// Planned duration of the heating segments, ramps plus soaks, for a kiln
    /// starting at `from`. The display's end-time estimate is built on it.
    pub fn planned_duration(&self, from: QuarterDegrees) -> Duration {
        let mut at = from;
        let mut total = Duration::ZERO;
        for segment in self.segments.iter().take_while(|s| s.rate_per_hour > 0) {
            let distance = (segment.target.raw() - at.raw()).max(0) as u64;
            let ramp_secs = distance * 3600 / segment.rate_per_hour as u64;
            total += Duration::from_secs(ramp_secs) + segment.soak;
            at = segment.target;
        }
        total
    }
}

/// A cone a preset can fire to. An enum rather than plain numbers so that a
/// preset cannot name a cone with no known peak.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Cone {
    C06,
    C04,
    C5,
    C6,
    C10,
}

impl Cone {
    /// Peak temperature at a 60 °C/h final ramp, from the cone maker's chart.
    pub const fn peak(self) -> QuarterDegrees {
        QuarterDegrees::from_celsius(match self {
            Cone::C06 => 999,
            Cone::C04 => 1060,
            Cone::C5 => 1196,
            Cone::C6 => 1222,
            Cone::C10 => 1285,
        })
    }
}

pub fn preset(cone: Cone) -> Schedule {
    let peak = cone.peak();
    Schedule::new(vec![
        Segment {
            rate_per_hour: 4 * 100,
            target: QuarterDegrees::from_celsius(600),
            soak: Duration::ZERO,
        },
        Segment {
            rate_per_hour: 4 * 150,
            target: peak.saturating_add(QuarterDegrees::from_celsius(-100)),
            soak: Duration::ZERO,
        },
        Segment {
            rate_per_hour: 4 * 60,
            target: peak,
            soak: Duration::from_secs(10 * 60),
        },
        Segment {
            rate_per_hour: -4 * 150,
            target: QuarterDegrees::from_celsius(760),
            soak: Duration::ZERO,
        },
    ])
    .expect("presets are valid")
}
