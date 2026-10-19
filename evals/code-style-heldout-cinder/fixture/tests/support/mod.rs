#![allow(dead_code)]

use std::cell::RefCell;
use std::collections::VecDeque;
use std::io;
use std::rc::Rc;
use std::time::Duration;

use cinder::controller::Clock;
use cinder::relay::Pin;
use cinder::temperature::QuarterDegrees;
use cinder::thermocouple::Spi;

pub const OPEN_CIRCUIT: u32 = (1 << 16) | 0b001;

pub fn encode(temperature: QuarterDegrees) -> u32 {
    (temperature.raw() as u32) << 18
}

struct State {
    now: Duration,
    kiln_millidegrees: i64,
    relay_on: bool,
    queued_frames: VecDeque<u32>,
}

#[derive(Clone)]
pub struct Bench(Rc<RefCell<State>>);

impl Bench {
    pub fn at(celsius: i32) -> Self {
        Bench(Rc::new(RefCell::new(State {
            now: Duration::ZERO,
            kiln_millidegrees: celsius as i64 * 1000,
            relay_on: false,
            queued_frames: VecDeque::new(),
        })))
    }

    pub fn kiln(&self) -> QuarterDegrees {
        QuarterDegrees::from_raw((self.0.borrow().kiln_millidegrees * 4 / 1000) as i32)
    }

    pub fn relay_on(&self) -> bool {
        self.0.borrow().relay_on
    }

    pub fn queue_frames(&self, frames: &[u32]) {
        self.0.borrow_mut().queued_frames.extend(frames);
    }

    pub fn spi(&self) -> BenchSpi {
        BenchSpi(self.clone())
    }

    pub fn pin(&self) -> BenchPin {
        BenchPin(self.clone())
    }

    pub fn clock(&self) -> BenchClock {
        BenchClock(self.clone())
    }
}

pub struct BenchSpi(Bench);

impl Spi for BenchSpi {
    fn read_u32(&mut self) -> io::Result<u32> {
        let queued = self.0 .0.borrow_mut().queued_frames.pop_front();
        Ok(queued.unwrap_or_else(|| encode(self.0.kiln())))
    }
}

pub struct BenchPin(Bench);

impl Pin for BenchPin {
    fn set_high(&mut self) {
        self.0 .0.borrow_mut().relay_on = true;
    }

    fn set_low(&mut self) {
        self.0 .0.borrow_mut().relay_on = false;
    }
}

pub struct BenchClock(Bench);

impl Clock for BenchClock {
    fn now(&self) -> Duration {
        self.0 .0.borrow().now
    }

    fn sleep(&mut self, duration: Duration) {
        let mut state = self.0 .0.borrow_mut();
        let ms = duration.as_millis() as i64;
        let change = if state.relay_on { 2 * ms } else { -ms };
        state.kiln_millidegrees = (state.kiln_millidegrees + change).max(20_000);
        state.now += duration;
    }
}
