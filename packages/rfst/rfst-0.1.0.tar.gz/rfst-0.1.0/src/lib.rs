use pyo3::prelude::*;
use std::fs;
use std::io::Read;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
struct File {
    file: fs::File,
}

#[pymethods]
impl File {
    #[new]
    fn open(path: &str) -> Self {
        Self {
            file: fs::File::open(path).unwrap()
        }
    }

    fn read(&mut self)-> PyResult<Vec<u8>> {
        let mut buffer = Vec::new();
        self.file.read_to_end(&mut buffer).unwrap();
        Ok(buffer)
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn rfst(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<File>()?;
    Ok(())
}
