use std::io;

use crate::temperature::QuarterDegrees;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Fault {
    OpenCircuit,
    ShortToGround,
    ShortToVcc,
}

pub trait Spi {
    fn read_u32(&mut self) -> io::Result<u32>;
}

/// The hot-junction temperature is a 14-bit two's-complement field in bits
/// 31..18. Bit 16 is set whenever any of the three fault bits (2..0) is set,
/// and the temperature field means nothing in that case.
pub fn decode(frame: u32) -> Result<QuarterDegrees, Fault> {
    if frame & (1 << 16) != 0 {
        return Err(match frame & 0b111 {
            0b001 => Fault::OpenCircuit,
            0b010 => Fault::ShortToGround,
            _ => Fault::ShortToVcc,
        });
    }
    // Shift as i32 so that the arithmetic shift carries the sign bit down.
    let raw = (frame as i32) >> 18;
    Ok(QuarterDegrees::from_raw(raw))
}

pub struct Thermocouple<S: Spi> {
    spi: S,
}

impl<S: Spi> Thermocouple<S> {
    pub fn new(spi: S) -> Self {
        Self { spi }
    }

    /// The chip converts continuously and takes about 100 ms per conversion;
    /// reading faster than that returns the previous result again, not a fresh
    /// one.
    pub fn read(&mut self) -> io::Result<Result<QuarterDegrees, Fault>> {
        Ok(decode(self.spi.read_u32()?))
    }
}
