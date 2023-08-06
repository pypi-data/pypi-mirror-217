use pyo3::{prelude::*, types::PyList};
use types::{CalamineSheet, CellValue};

mod types;
mod utils;
use crate::types::{CalamineError, CalamineWorkbook};

fn save_to_dataset(dataset: PyObject, sheet: CalamineSheet) -> PyResult<()> {
    let range = sheet.range.to_owned();
    Python::with_gil(|py| {
        let tablib = py.import("tablib.core")?;
        let row_class = tablib.getattr("Row")?;

        let list = PyList::empty(py);
        for (i, line) in range.rows().enumerate() {
            let line_cast = line.iter().map(|cell| cell.into()).collect::<Vec<CellValue>>();
            if i == 0 {
                dataset.setattr(py, "headers", line_cast)?;
                continue;
            }
            let row = row_class.call0()?;
            row.setattr("_row", line_cast)?;
            list.append(row)?;
        }

        dataset.setattr(py,"title", sheet.name)?;
        dataset.setattr(py, "_data", list)?;
        Ok(())
    })
}

#[pyfunction]
fn load_dataset(dataset: PyObject, path_or_filelike: PyObject) -> PyResult<()> {
    let mut wb = CalamineWorkbook::from_object(path_or_filelike)?;
    let sheet = wb.get_sheet_by_index(0)?;
    save_to_dataset(dataset, sheet)?;
    Ok(())
}

#[pymodule]
fn _calamine_tablib(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_dataset, m)?)?;
    m.add("CalamineError", py.get_type::<CalamineError>())?;
    Ok(())
}
