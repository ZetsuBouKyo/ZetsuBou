use pyo3::prelude::*;
use std::collections::HashMap;
use std::ffi::OsStr;
use std::{fs, io, path::Path};
pub trait FileExtension {
    fn has_extension<S: AsRef<str>>(&self, extensions: &[S]) -> bool;
}

impl<P: AsRef<Path>> FileExtension for P {
    fn has_extension<S: AsRef<str>>(&self, extensions: &[S]) -> bool {
        if let Some(ref extension) = self.as_ref().extension().and_then(OsStr::to_str) {
            return extensions
                .iter()
                .any(|x| x.as_ref().eq_ignore_ascii_case(extension));
        }

        false
    }
}

fn look_through(
    p: &Path,
    current_depth: i64,
    depth: i64,
    stat: &mut HashMap<&str, usize>,
) -> Result<String, io::Error> {
    if p.is_dir() {
        for entry in fs::read_dir(p)? {
            let entry = entry?;
            let next_path = entry.path();
            if next_path.is_dir() {
                let next_depth = current_depth + 1;
                // if next_depth == depth {
                //     continue;
                // }
                if current_depth == depth {
                    *stat.get_mut("num_galleries").unwrap() += 1;
                }
                look_through(&next_path, next_depth, depth, stat)?;
            } else {
                let size = next_path.metadata().unwrap().len();
                *stat.get_mut("size").unwrap() += usize::try_from(size).unwrap();
                if next_path.has_extension(&["mp4"]) {
                    *stat.get_mut("num_mp4s").unwrap() += 1;
                }

                if current_depth == depth {
                    if next_path.has_extension(&["png", "jpg", "jpeg", "gif", "bmp", "webp"]) {
                        *stat.get_mut("num_images").unwrap() += 1;
                    }
                    *stat.get_mut("num_files").unwrap() += 1;
                } else if current_depth > depth {
                    *stat.get_mut("num_files").unwrap() += 1;
                }
            }
        }
    }
    let stat_str = serde_json::to_string(&stat).unwrap();
    // println!("{}", stat_str);
    Ok(stat_str)
}

#[pyfunction]
fn standalone_stat(p: String, depth: i64) -> PyResult<String> {
    let path = Path::new(&p);
    let cur: i64 = 0;

    let mut stat = HashMap::<&str, usize>::new();
    stat.insert("size", 0);
    stat.insert("num_files", 0);
    stat.insert("num_images", 0);
    stat.insert("num_mp4s", 0);
    stat.insert("num_galleries", 0);

    let stat_str = look_through(path, cur, depth, &mut stat).unwrap();
    Ok(stat_str)
}

#[pymodule]
fn zetsubou(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(standalone_stat, m)?)?;
    Ok(())
}
