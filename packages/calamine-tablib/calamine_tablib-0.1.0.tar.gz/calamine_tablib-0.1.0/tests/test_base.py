from io import BytesIO
from pathlib import Path

import pytest
from tablib import Dataset
from calamine_tablib import load_dataset

PATH = Path(__file__).parent / "data"

@pytest.mark.parametrize(
    "obj",
    [
        PATH / "base.xlsx",
        (PATH / "base.xlsx").as_posix(),
        open(PATH / "base.xlsx", "rb"),
        BytesIO(open(PATH / "base.xlsx", "rb").read()),
    ],
)
def test_path_or_filelike(obj):
    dataset = Dataset()
    load_dataset(dataset, obj)


def test_path_or_filelike_error():
    with pytest.raises(TypeError):
        load_dataset(Dataset(), object())
