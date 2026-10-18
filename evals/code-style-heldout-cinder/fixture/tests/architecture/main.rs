mod layering;

use std::fs;
use std::path::PathBuf;

// Paths are relative to the crate root, which is the working directory cargo
// runs integration tests in.
fn source_files() -> Vec<(PathBuf, String)> {
    let mut files: Vec<(PathBuf, String)> = fs::read_dir("src")
        .unwrap()
        .map(|entry| entry.unwrap().path())
        .filter(|path| path.extension().is_some_and(|ext| ext == "rs"))
        .map(|path| {
            let text = fs::read_to_string(&path).unwrap();
            (path, text)
        })
        .collect();
    files.sort();
    files
}
