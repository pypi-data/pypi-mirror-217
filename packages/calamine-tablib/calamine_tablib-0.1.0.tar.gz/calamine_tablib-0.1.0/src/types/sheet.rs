use calamine::{DataType, Range};
use pyo3::prelude::*;

#[pyclass]
pub struct CalamineSheet {
    #[pyo3(get)]
    pub name: String,
    pub range: Range<DataType>,
}

impl CalamineSheet {
    pub fn new(name: String, range: Range<DataType>) -> Self {
        CalamineSheet { name, range }
    }
}

