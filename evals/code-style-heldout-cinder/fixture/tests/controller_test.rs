mod support;

use std::time::Duration;

use cinder::controller::{Abort, Firing, Progress};
use cinder::schedule::{preset, Cone, Schedule, Segment};
use cinder::temperature::QuarterDegrees;
use support::{encode, Bench, OPEN_CIRCUIT};

// The bench kiln gains 2 °C for every second the relay is on and loses 1 °C for
// every second it is off, so it can always outrun the schedule: these tests see
// what the controller does, not what a slow kiln does.

fn short_schedule() -> Schedule {
    Schedule::new(vec![Segment {
        rate_per_hour: 4 * 600,
        target: QuarterDegrees::from_celsius(100),
        soak: Duration::from_secs(60),
    }])
    .unwrap()
}

fn run_to_end<S, P, C>(firing: &mut Firing<S, P, C>)
where
    S: cinder::thermocouple::Spi,
    P: cinder::relay::Pin,
    C: cinder::controller::Clock,
{
    loop {
        match firing.run_window() {
            Ok(Progress::Finished) => return,
            Ok(Progress::Running { .. }) => {}
            Err(abort) => panic!("firing aborted: {abort:?}"),
        }
    }
}

#[test]
fn a_preset_runs_to_completion() {
    let bench = Bench::at(20);
    let mut firing = Firing::new(preset(Cone::C06), bench.spi(), bench.pin(), bench.clock(), bench.kiln());
    run_to_end(&mut firing);
    assert!(!bench.relay_on());
}

#[test]
fn the_relay_is_off_between_windows() {
    let bench = Bench::at(20);
    let mut firing = Firing::new(short_schedule(), bench.spi(), bench.pin(), bench.clock(), bench.kiln());
    for _ in 0..10 {
        firing.run_window().unwrap();
        assert!(!bench.relay_on());
    }
}

#[test]
fn the_kiln_reaches_the_target_before_the_soak_ends() {
    let bench = Bench::at(20);
    let mut firing = Firing::new(short_schedule(), bench.spi(), bench.pin(), bench.clock(), bench.kiln());
    run_to_end(&mut firing);
    assert!(bench.kiln() >= QuarterDegrees::from_celsius(95));
}

// A firing aborts on the third consecutive fault, and a good reading in between
// starts the count again.
#[test]
fn three_consecutive_faults_abort_the_firing() {
    let bench = Bench::at(20);
    let room = encode(bench.kiln());
    bench.queue_frames(&[OPEN_CIRCUIT, OPEN_CIRCUIT, room, OPEN_CIRCUIT, OPEN_CIRCUIT, OPEN_CIRCUIT]);
    let mut firing = Firing::new(short_schedule(), bench.spi(), bench.pin(), bench.clock(), bench.kiln());
    for _ in 0..5 {
        assert!(firing.run_window().is_ok());
    }
    assert!(matches!(firing.run_window(), Err(Abort::SensorFaults(_))));
    assert!(!bench.relay_on());
}
