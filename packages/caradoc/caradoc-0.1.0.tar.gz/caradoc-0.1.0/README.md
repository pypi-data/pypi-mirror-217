# Caradoc

Python utilities for doing data analysis. Named for [Caradoc Vreichvras](https://en.wikipedia.org/wiki/Caradoc), a knight of the round table.

Currently includes two utilities:

## `FinancialYear`

Represents a Financial Year, from a string in the format "2020-21".

### Usage:

```python
from caradoc import FinancialYear

fy = FinancialYear("2020-21")

fy + 1  # FinancialYear("2021-22")
fy - 1  # FinancialYear("2019-20")

str(fy)  # "2020-21"
int(fy)  # 2020
```

Create from date or year

```python
from datetime import date
from caradoc import FinancialYear

fy = FinancialYear.from_date(date(2020, 1, 1))
str(fy)  # "2019-20"

fy = FinancialYear.from_int(2020)
str(fy)  # "2020-21"
```

Useful utilities:

```python
from caradoc import FinancialYear

fy = FinancialYear("2020-21")

fy.previous_n_years(4)  # [
#    FinancialYear("2016-17"),
#    FinancialYear("2017-18"),
#    FinancialYear("2018-19"),
#    FinancialYear("2019-20"),
#    FinancialYear("2020-21")
# ]

FinancialYear.range("2018-19", "2020-21")  # [
#    FinancialYear("2018-19"),
#    FinancialYear("2019-20"),
#    FinancialYear("2020-21"),
# ]

d = date(2021, 6, 1)
d in FinancialYear("2021-22")  # True
d in FinancialYear("2020-22")  # False
```

Currently years are hardcoded to end on 31st March but this will be changed.


## `ExcelTable`

Represents a table in an Excel workbook.

The table itself is a pandas DataFrame. The DataFrame index is not written to the Excel file.

Allows for specifying a title, summary and notes for the table.

### Parameters

- `df`: pandas DataFrame
- `title`: Optional title for the table
- `summary`: Optional summary for the table
- `notes`: Optional notes for the table

### Methods

- `to_excel_table()`: Writes just the datatable (`df`) to an Excel file as a Table (with filters)
- `to_excel()`: Writes the table to an Excel file as a Table, with the
    title and summary as a header and the notes as a footer.

### Usage

```python
from caradoc import ExcelTable
import pandas as pd

df = pd.DataFrame({"alice": [1, 2, 3], "bob": [4, 5, 6]})
et = ExcelTable(
    df,
    title="Test Table"
)
with pd.ExcelWriter("test_file.xlsx", engine="auto") as writer:
    et.to_excel(writer, "test_sheet")
```

Output looks something like:

|   | A          | B   |
|---|------------|-----|
| 1 | Test Table |     |
| 2 |            |     |
| 3 | Alice      | Bob |
| 4 | 1          |   4 |
| 5 | 2          |   5 |
| 6 | 3          |   6 |

You can also include a summary (underneath the title) and notes (underneath the table) using `summary=` and `notes=`

## `DataOutput`

Represents a collection of ExcelTables to be written to an Excel file.

### Methods

- `add_table()`: Adds a table to the DataOutput
- `write()`: Writes the DataOutput to an Excel file

### Usage

```python
from caradoc import DataOutput, ExcelTable
import pandas as pd

output = DataOutput()

df1 = pd.DataFrame({"alice": [1, 2, 3], "bob": [4, 5, 6]})
table1 = ExcelTable(
    df1,
    title="Test Table"
)

output.add_table("test_sheet", table1)

df2 = pd.DataFrame({"alice": [1, 2, 3], "bob": [4, 5, 6]})
output.add_table("test_sheet", df2, title="Test Table 2")

output.write("test_file.xlsx")
```

Output of `test_file.xlsx` will be an excel workbook with a sheet called "test_sheet". The sheet will have two tables, each table with a title and spacing between them.

## Development

### Run tests

Tests can be run with `pytest`:

```bash
hatch run test
```

### Test coverage

```bash
hatch run cov-html
```

### Run typing checks

```bash
hatch run lint:typing
```

### Linting

Black and ruff should be run before committing any changes.

```bash
hatch run lint:style
```

### Run all checks at once

```sh
hatch run lint:all
```

## Publish to pypi

```bash
python -m build
twine upload dist/*
git tag v<VERSION_NUMBER>
git push origin v<VERSION_NUMBER>
```

## Install development version

The development requirements are installed using `pip install -r dev-requirements.txt`.

Any additional requirements for the module itself must be added to
`install_requires` in `setup.py`. You should then generate a new 
`requirements.txt` using using [`pip-tools`](https://github.com/jazzband/pip-tools) (`pip-compile`). You can then run `pip-sync` to install the 
requirement.

Any additional development requirements must be added to `dev-requirements.in`
and then the `dev-requirements.txt` should be generated using `pip-compile dev-requirements.in`. You can then install the development requirements using
`pip-sync dev-requirements.txt`.