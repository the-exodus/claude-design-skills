use crate::source_files;

// No public function in `src/` takes or returns a float: temperatures cross
// module boundaries as `QuarterDegrees` (0001).
#[test]
fn no_float_in_a_public_signature() {
    for (path, text) in source_files() {
        for line in text.lines().map(str::trim_start) {
            if line.starts_with("pub fn") || line.starts_with("pub const fn") {
                assert!(
                    !line.contains("f32") && !line.contains("f64"),
                    "{}: {line}",
                    path.display()
                );
            }
        }
    }
}

// Only `relay.rs` calls `set_high` or `set_low`, so nothing switches the
// elements except through `Relay` (0002).
#[test]
fn only_the_relay_drives_the_pin() {
    for (path, text) in source_files() {
        if path.ends_with("relay.rs") {
            continue;
        }
        assert!(
            !text.contains("set_high(") && !text.contains("set_low("),
            "{}",
            path.display()
        );
    }
}
