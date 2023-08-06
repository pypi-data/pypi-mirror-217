from __future__ import annotations

from datetime import date, datetime, time
from os import PathLike
from typing import Protocol
from tablib.core import Dataset

ValueT = int | float | str | bool | time | date | datetime

class ReadBuffer(Protocol):
    def seek(self) -> int: ...
    def read(self) -> bytes: ...

class CalamineError(Exception): ...

def load_dataset(
    dataset: Dataset,
    path_or_filelike: str | PathLike | ReadBuffer,
) -> None:
    """Determining type of pyobject and reading from it.

    Parameters
    ----------
    path_or_filelike :
        - path (string),
        - pathlike (pathlib.Path),
        - IO (must imlpement read/seek methods).
    """
