use std::fs::File;
use std::io::{BufReader, Cursor, Read};
use std::path::PathBuf;

use calamine::{open_workbook_auto, open_workbook_auto_from_rs, Reader, Sheets, Error};
use pyo3::prelude::*;
use pyo3::types::PyString;
use pyo3_file::PyFileLikeObject;

use crate::utils::err_to_py;

use super::{CalamineError, CalamineSheet};

pub enum SheetsEnum {
    File(Sheets<BufReader<File>>),
    FileLike(Sheets<Cursor<Vec<u8>>>),
}

impl SheetsEnum {
    fn sheet_names(&self) -> &[String] {
        match self {
            SheetsEnum::File(f) => f.sheet_names(),
            SheetsEnum::FileLike(f) => f.sheet_names(),
        }
    }
    fn worksheet_range(
        &mut self,
        name: &str,
    ) -> Option<Result<calamine::Range<calamine::DataType>, Error>> {
        match self {
            SheetsEnum::File(f) => f.worksheet_range(name),
            SheetsEnum::FileLike(f) => f.worksheet_range(name),
        }
    }
    fn worksheet_range_at(
        &mut self,
        index: usize,
    ) -> Option<Result<calamine::Range<calamine::DataType>, Error>> {
        match self {
            SheetsEnum::File(f) => f.worksheet_range_at(index),
            SheetsEnum::FileLike(f) => f.worksheet_range_at(index),
        }
    }
}

pub struct CalamineWorkbook {
    pub sheets: SheetsEnum,
    pub sheet_names: Vec<String>,
}

impl CalamineWorkbook {
    pub fn get_sheet_by_name(&mut self, name: &str) -> PyResult<CalamineSheet> {
        let range = self
            .sheets
            .worksheet_range(name)
            .unwrap_or_else(|| Err(Error::Msg("Workbook is empty")))
            .map_err(err_to_py)?;
        Ok(CalamineSheet::new(name.to_owned(), range))
    }

    pub fn get_sheet_by_index(&mut self, index: usize) -> PyResult<CalamineSheet> {
        let name = self
            .sheet_names
            .get(index)
            .ok_or_else(|| CalamineError::new_err("Workbook is empty"))?
            .to_string();
        let range = self
            .sheets
            .worksheet_range_at(index)
            .unwrap_or_else(|| Err(Error::Msg("Workbook is empty")))
            .map_err(err_to_py)?;
        Ok(CalamineSheet::new(name, range))
    }

    pub fn from_object(path_or_filelike: PyObject) -> PyResult<Self> {
        Python::with_gil(|py| {
            if let Ok(string_ref) = path_or_filelike.downcast::<PyString>(py) {
                return Self::from_path(string_ref.to_string_lossy().to_string().as_str());
            }

            if let Ok(string_ref) = path_or_filelike.extract::<PathBuf>(py) {
                return Self::from_path(string_ref.to_string_lossy().to_string().as_str());
            }

            Self::from_filelike(path_or_filelike)
        })
    }

    pub fn from_filelike(filelike: PyObject) -> PyResult<Self> {
        let mut buf = vec![];
        PyFileLikeObject::with_requirements(filelike, true, false, true)?.read_to_end(&mut buf)?;
        let reader = Cursor::new(buf);
        let sheets = SheetsEnum::FileLike(open_workbook_auto_from_rs(reader).map_err(err_to_py)?);
        let sheet_names = sheets.sheet_names().to_owned();

        Ok(Self {
            sheets,
            sheet_names,
        })
    }

    pub fn from_path(path: &str) -> PyResult<Self> {
        let sheets = SheetsEnum::File(open_workbook_auto(path).map_err(err_to_py)?);
        let sheet_names = sheets.sheet_names().to_owned();

        Ok(Self {
            sheets,
            sheet_names,
        })
    }
}
