use cinder::temperature::QuarterDegrees;
use cinder::thermocouple::{decode, Fault};

// Frames captured from the studio kiln's amplifier: probe at room temperature,
// probe in boiling water, and probe unplugged.
const ROOM: u32 = 0x015C_1610;
const BOILING: u32 = 0x063C_1780;
const UNPLUGGED: u32 = 0x0001_1611;

#[test]
fn room_temperature_frame_decodes() {
    assert_eq!(decode(ROOM), Ok(QuarterDegrees::from_raw(87)));
}

#[test]
fn boiling_water_frame_decodes() {
    assert_eq!(decode(BOILING), Ok(QuarterDegrees::from_raw(399)));
}

#[test]
fn unplugged_probe_is_an_open_circuit() {
    assert_eq!(decode(UNPLUGGED), Err(Fault::OpenCircuit));
}

#[test]
fn below_zero_keeps_its_sign() {
    let frame = ((-41i32) as u32) << 18;
    assert_eq!(decode(frame), Ok(QuarterDegrees::from_raw(-41)));
}
