use std::fmt;

/// A temperature in quarter-degrees Celsius. The thermocouple amplifier
/// resolves 0.25 °C, so every reading is a whole number of quarter-degrees and
/// arithmetic on them is exact (0001).
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct QuarterDegrees(i32);

impl QuarterDegrees {
    pub const fn from_raw(raw: i32) -> Self {
        Self(raw)
    }

    pub const fn from_celsius(celsius: i32) -> Self {
        Self(celsius * 4)
    }

    /// Returns the raw quarter-degree count.
    pub const fn raw(self) -> i32 {
        self.0
    }

    pub const fn saturating_add(self, other: Self) -> Self {
        Self(self.0.saturating_add(other.0))
    }
}

impl fmt::Display for QuarterDegrees {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{:02} °C", self.0.div_euclid(4), self.0.rem_euclid(4) * 25)
    }
}
