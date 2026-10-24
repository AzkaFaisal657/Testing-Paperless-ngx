# Paperless-ngx — Assignment 3

## Assignment requirements

Assignment 3 requires the group to:

1. Select and set up an open-source Python project.
2. Write automated unit tests for selected modules.
3. Apply test design techniques such as Equivalence Class Partitioning (ECP)
   and Boundary Value Analysis (BVA).
4. Write at least four test cases in an Excel workbook.
5. Read test data from an external resource such as a CSV file.
6. Configure separate test suites and test groups.
7. Use parameterized, data-driven tests where appropriate.
8. Configure tests to run in parallel.
9. Add setup documentation and the recorded setup video.
10. Commit the completed work to the group repository.

## Work established so far

### Project and environment

- Paperless-ngx was selected as the open-source Python application.
- The application was set up and run locally with Docker.
- The test project uses pytest and integrates with the Paperless-ngx source.

### Assigned unit-test modules

This contribution covers:

- **M1 — Auth & Users**
- **M2 — Documents**
- **M6 — Trash & Bulk Actions**

The tests are located in:

- `tests/test_m1_auth.py`
- `tests/test_m2_documents.py`
- `tests/test_m6_trash_bulk.py`

### Test automation completed

- Parameterized authentication tests.
- CSV-driven document path tests.
- Trash and bulk-action tests using simple mocked update calls.
- ECP and BVA design notes.
- Separate pytest markers for each module.
- Parallel test execution configuration.
- Beginner-friendly viva notes.

The current automated suite contains 22 tests. The suite has been verified to
pass in both normal and parallel execution.

### Documentation and evidence completed

- `docs/Paperless_Test_Workbook.xlsx`
- `docs/azka_test_design.md`
- `docs/azka_viva_notes.md`
- `test_data/m2_path_cases.csv`
- Test configuration files and execution instructions.

## Work still to be added

- Partner's unit tests for her assigned modules.
- Recorded setup video.
- Any final group-level summary report or contribution updates required by the
  instructor.
- Final review of all test cases, documentation, and naming consistency.
- Final public-repository check before submitting the repository link on GCR.

## Running the tests

Install the test dependencies:

```powershell
uv sync --group test
```

Set `PAPERLESS_SOURCE_ROOT` to the root of the Paperless-ngx source checkout
and set `PAPERLESS_SECRET_KEY` to a non-default development value.

Run all tests:

```powershell
uv run pytest
```

Run an individual module:

```powershell
uv run pytest -m auth
uv run pytest -m documents
uv run pytest -m trash_bulk
```

Run tests in parallel:

```powershell
uv run pytest -n auto
```

Test data for the document suite is stored in
`test_data/m2_path_cases.csv`.