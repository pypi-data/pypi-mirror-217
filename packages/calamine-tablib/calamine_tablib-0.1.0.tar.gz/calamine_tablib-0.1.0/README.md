# `calamine-tablib`

A fast excel format for tablib.

Based on [`calamine`](https://github.com/tafia/calamine) and [`pyexcelerate`](https://github.com/kz26/PyExcelerate).

Code referenced from [`python-calamine`](https://github.com/dimastbk/python-calamine)

## Usage

Register the new format `fast_xlsx` importing this monkeypatch

```python
# __init__.py

from calamine_tablib import monkeypatches  # noqa This module does patching for tablib
```

And then use the format as usual:

```python
dataset = Dataset()

# to import via calamine
dataset.load(file, format="fast_xlsx")
```
