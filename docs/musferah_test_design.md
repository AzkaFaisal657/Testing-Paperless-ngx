# Assignment 3 Test Design — Musferah

## Scope

This contribution covers the assigned Paperless-ngx modules:

| Module | Area | Test file |
| --- | --- | --- |
| M1 | Auth & Users | `tests/test_m1_auth.py` |
| M3 | Attributes | `tests/test_m3_attributes.py` |
| M5 | Workflows & Matching | `tests/test_m5_workflows.py` |

The tests import the Paperless-ngx source checkout through
`PAPERLESS_SOURCE_ROOT` and exercise application code rather than reimplementing
its behavior.

## Test design techniques

### M1 — Auth & Users

- **Equivalence partitioning:** Basic and non-Basic authorization schemes,
  malformed headers, empty headers, and absent headers are separate classes.
- **Boundary value analysis:** Basic scheme casing and the presence or absence
  of the authorization header are checked at their boundaries.
- **Authentication behavior:** A valid Basic-authenticated user is refused
  when MFA is enabled and returned when MFA is disabled.
- **Test data:** `test_data/m1_auth_cases.csv`.

### M3 — Attributes

- **Equivalence partitioning:** Each supported custom-field data type is an
  accepted class; an unknown data type is a rejected class.
- **Boundary value analysis:** A blank field name is rejected, while all
  supported values are passed through the serializer's choice validation.
- **Test data:** `test_data/m3_custom_field_types.csv`.

### M5 — Workflows & Matching

- **Equivalence partitioning:** Any-word, all-words, literal, and regular
  expression matching are exercised with both matching and non-matching
  document content.
- **Boundary value analysis:** Matching is checked with case sensitivity
  enabled and disabled. Workflow source, filename, and path filters are
  checked for matching, mismatching, and unconfigured cases.
- **Test data:**
  - `test_data/m5_workflow_matching_cases.csv`
  - `test_data/m5_workflow_filter_cases.csv`

## Execution

Run only the modules in this contribution:

```powershell
uv run pytest -m "auth or attributes or workflows"
```

Run them with the project's parallel test configuration:

```powershell
uv run pytest -n auto -m "auth or attributes or workflows"
```

The shared `conftest.py` requires `PAPERLESS_SOURCE_ROOT` to point to the
Paperless-ngx checkout containing its `src` directory.
