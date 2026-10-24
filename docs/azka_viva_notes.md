# Assignment 3 Viva Notes

These notes explain the work in simple terms. The tests are stored in the
`tests/` folder and use the real Paperless-ngx source code.

## What I did

I selected three areas from my assigned black-box testing work:

1. **M1 Auth & Users** — tested the authentication challenge returned for
   different authorization headers.
2. **M2 Documents** — tested whether a document path stays inside the safe
   originals directory.
3. **M6 Trash & Bulk Actions** — tested restoration of archive serial numbers
   for zero, one, and multiple documents.

## How pytest finds the application

The Paperless-ngx source is in a separate checkout. Before running tests, I
set this variable:

```powershell
$env:PAPERLESS_SOURCE_ROOT = "C:\Users\fazia\source\repos\paperless-ngx"
```

`conftest.py` adds the source `src` folder to Python's import path, selects
the Paperless Django settings, and starts Django. This lets the tests import
real classes such as `PaperlessBasicAuthentication` and
`validate_path_in_root`.

## Test structure

Each test file has three simple parts:

1. Import the function or class being tested.
2. Provide input data.
3. Assert the expected output or error.

For example, the document path test creates a temporary safe directory,
passes a path to the Paperless function, and checks whether the function
accepts it or raises `UnsafeFilePathError`.

## Parameterization

`pytest.mark.parametrize` runs the same test several times with different
inputs. This avoids writing almost identical test functions.

Example idea:

```python
@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("invoice.pdf", "inside"),
        ("../invoice.pdf", "outside"),
    ],
)
def test_path(path, expected):
    ...
```

The authentication tests use parameterization for Basic, lowercase Basic,
Bearer, empty, and missing authorization values. The document tests get
their values from `test_data/m2_path_cases.csv`.

## CSV test data

The CSV file is an external resource. It contains:

- normal file paths
- nested paths
- the root directory boundary
- parent-directory traversal
- an absolute outside path

The test reads each CSV row and checks the expected result. This satisfies the
data-driven testing requirement.

## ECP and BVA

### Equivalence Class Partitioning (ECP)

ECP divides inputs into groups that should behave similarly.

- Authentication headers are divided into Basic and non-Basic groups.
- Document paths are divided into safe and unsafe groups.
- Archive serial number backups are divided into empty, one-item, and
  multiple-item groups.

### Boundary Value Analysis (BVA)

BVA checks values at important limits.

- A path equal to the root is tested.
- A path one level above the root (`..`) is tested.
- A path with repeated traversal (`../../`) is tested.
- Empty backup data is tested.
- One and multiple backup entries are tested.

## Why mocks are used in M6

The bulk function normally updates database records. The purpose of this
unit test is to check that the correct document IDs and serial numbers are
sent to the update operation. A small mock records those calls so the test
does not need to change a real database.

In the viva, I can explain this as:

> “I replaced the database manager temporarily with a mock, called the
> function, and checked how many updates it requested and what values it used.”

## Test groups

The markers divide the tests into suites:

```powershell
uv run pytest -m auth
uv run pytest -m documents
uv run pytest -m trash_bulk
```

Run everything:

```powershell
uv run pytest
```

Run tests in parallel:

```powershell
uv run pytest -n 2
```

## Simple viva answers

**Why pytest?**  
Pytest has simple assertions, parameterization, markers, and good support for
running test files and test groups.

**What does a passing test mean?**  
It means the actual result matched the expected result for that input.

**What does a failing test mean?**  
It means the actual behavior did not match the expected behavior and needs
investigation.

**What is the difference between unit and black-box testing?**  
Black-box testing checks the application from the user's point of view.
Unit testing checks a smaller function or class directly.

**What did I contribute?**  
I created the test configuration, CSV-driven document tests, authentication
tests, trash/bulk tests, test design notes, and execution instructions for
M1, M2, and M6.
