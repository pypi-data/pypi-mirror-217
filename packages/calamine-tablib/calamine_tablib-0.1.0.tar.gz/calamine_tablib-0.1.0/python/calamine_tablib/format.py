import itertools
from io import BytesIO

from pyexcelerate import Workbook
from tablib.formats._xlsx import XLSXFormat
from calamine_tablib import load_dataset

class FastXLSXFormat(XLSXFormat):
    """XLSX format."""

    title = "fast_xlsx"

    @classmethod
    def import_set(cls, dset, in_stream, headers=True, read_only=True, skip_lines=0):
        """Returns databook from XLS stream."""

        dset.wipe()
        load_dataset(dset, in_stream)

    @classmethod
    def export_set(
        cls, dataset, freeze_panes=True, invalid_char_subst="-", escape=False
    ):
        """Returns XLSX representation of Dataset."""
        title = dataset.title or "Sheet1"
        wb = Workbook()
        wb.new_sheet(title, data=itertools.chain([dataset.headers], dataset))
        stream = BytesIO()
        wb.save(stream)
        return stream.getvalue()

    @classmethod
    def export_book(
        cls, databook, freeze_panes=True, invalid_char_subst="-", escape=False
    ):
        """Returns XLSX representation of DataBook."""
        assert len(databook._datasets) == 1
        return cls.export_set(databook._datasets[0], freeze_panes)
