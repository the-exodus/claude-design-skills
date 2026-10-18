use std::time::Duration;

use cinder::schedule::{preset, Cone, Schedule, ScheduleError, Segment, KILN_LIMIT, MAX_SEGMENTS};
use cinder::temperature::QuarterDegrees;

fn segment(rate_celsius_per_hour: i32, target_celsius: i32, soak_minutes: u64) -> Segment {
    Segment {
        rate_per_hour: 4 * rate_celsius_per_hour,
        target: QuarterDegrees::from_celsius(target_celsius),
        soak: Duration::from_secs(soak_minutes * 60),
    }
}

#[test]
fn an_empty_schedule_is_rejected() {
    assert_eq!(Schedule::new(vec![]).unwrap_err(), ScheduleError::Empty);
}

#[test]
fn too_many_segments_are_rejected() {
    let segments = (0..=MAX_SEGMENTS as i32).map(|i| segment(100, 100 + i * 50, 0)).collect();
    assert_eq!(Schedule::new(segments).unwrap_err(), ScheduleError::TooManySegments);
}

#[test]
fn a_zero_rate_is_rejected() {
    let segments = vec![segment(100, 600, 0), segment(0, 600, 30)];
    assert_eq!(Schedule::new(segments).unwrap_err(), ScheduleError::ZeroRate { segment: 1 });
}

#[test]
fn a_rate_pointing_away_from_its_target_is_rejected() {
    let segments = vec![segment(100, 600, 0), segment(100, 500, 0)];
    assert_eq!(
        Schedule::new(segments).unwrap_err(),
        ScheduleError::RateAgainstTarget { segment: 1 }
    );
}

#[test]
fn heating_after_cooling_is_rejected() {
    let segments = vec![segment(100, 600, 0), segment(-100, 500, 0), segment(100, 700, 0)];
    assert_eq!(
        Schedule::new(segments).unwrap_err(),
        ScheduleError::HeatsAfterCooling { segment: 2 }
    );
}

#[test]
fn planned_duration_of_a_two_segment_schedule() {
    let schedule = Schedule::new(vec![segment(80, 100, 30), segment(-100, 50, 0)]).unwrap();
    assert_eq!(
        schedule.planned_duration(QuarterDegrees::from_celsius(20)),
        Duration::from_secs(90 * 60)
    );
}

// A preset whose cone peaked above the limit would be rejected at load and
// `preset` would panic on it, so every peak has to stay under the limit (0004).
#[test]
fn every_cone_peak_is_under_the_kiln_limit() {
    for cone in [Cone::C06, Cone::C04, Cone::C5, Cone::C6, Cone::C10] {
        assert!(cone.peak() <= KILN_LIMIT, "{cone:?}");
        let _ = preset(cone);
    }
}
