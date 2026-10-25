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

The group test suite is split across the following modules:

- **M1 — Auth & Users** — `tests/test_m1_auth.py`
- **M2 — Documents** — `tests/test_m2_documents.py`
- **M3 — Attributes** — `tests/test_m3_attributes.py`
- **M4 — Search & Saved Views** — contributed by the other team member
- **M5 — Workflows & Matching** — `tests/test_m5_workflows.py`
- **M6 — Trash & Bulk Actions** — `tests/test_m6_trash_bulk.py`

This contribution adds M1, M3, and M5 tests. M2, M4, and M6 are owned by the
other team member.

### Test automation completed

- CSV-driven authentication challenge and MFA tests.
- Custom-field type validation tests.
- Workflow matching algorithm and consumption-filter tests.
- CSV-driven document path tests.
- Trash and bulk-action tests using simple mocked update calls.
- ECP and BVA design notes for each contribution.
- Separate pytest markers for each module.
- Parallel test execution configuration.
- Beginner-friendly viva notes.

### Documentation and evidence completed

- `docs/Paperless_Test_Workbook.xlsx`
- `docs/azka_test_design.md`
- `docs/musferah_test_design.md`
- `docs/musferah_test_cases.xlsx`
- `docs/azka_viva_notes.md`
- CSV test data in `test_data/`
- Test configuration files and execution instructions.

## Final group-level checks

- Complete any group-level summary report or contribution updates required by
  the instructor.
- Review all test cases, documentation, and naming consistency together.
- Verify the public repository before submitting its link on GCR.

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
uv run pytest -m attributes
uv run pytest -m documents
uv run pytest -m workflows
uv run pytest -m trash_bulk
```

Run tests in parallel:

```powershell
uv run pytest -n auto
```

The module-specific CSV inputs are stored in `test_data/`.