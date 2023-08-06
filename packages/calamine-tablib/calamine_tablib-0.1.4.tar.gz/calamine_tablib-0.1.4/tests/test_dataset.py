from io import BytesIO
from pathlib import Path

import pytest
from calamine_tablib import monkeypatches  # noqa
from tablib import Dataset

PATH = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    "obj",
    [
        open(PATH / "base.xlsx", "rb"),
        BytesIO(open(PATH / "base.xlsx", "rb").read()),
    ],
)
def test_fast_xlsx_format(obj):
    dataset = Dataset()
    dataset.load(obj, format="fast_xlsx")
