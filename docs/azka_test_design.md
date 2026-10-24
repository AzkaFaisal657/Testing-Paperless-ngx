# Assignment 3 Test Design — Azka

## Scope

This contribution covers the modules assigned to Azka in the updated
workbook:

| Module | Application area | Test file |
| --- | --- | --- |
| M1 | Auth & Users | `tests/test_m1_auth.py` |
| M2 | Documents | `tests/test_m2_documents.py` |
| M6 | Trash & Bulk Actions | `tests/test_m6_trash_bulk.py` |

The tests import the actual Paperless-ngx source checkout through
`PAPERLESS_SOURCE_ROOT`; no application logic is duplicated in this repository.

## Test design techniques

### M1 Auth & Users

- **Equivalence partitioning:** Basic, Bearer, empty, and missing authorization
  headers are separate classes.
- **Boundary value analysis:** Header scheme matching is checked in both normal
  and lowercase forms; development authentication is checked for HTTP versus
  HTTPS, correct versus incorrect ports, and debug enabled versus disabled.
- **Expected outcomes:** Basic headers use the Basic challenge; all other
  classes use token authentication; development auto-authentication is limited
  to the intended local origin and staff-user condition.

### M2 Documents

- **Equivalence partitioning:** A path inside the originals root and paths
  outside it are tested separately.
- **Boundary value analysis:** The CSV includes the root itself, a direct file,
  nested directories, parent traversal, repeated traversal, and an absolute
  external path.
- **Expected outcomes:** Safe paths are accepted; unsafe paths raise
  `UnsafeFilePathError` before a write can occur.

### M6 Trash & Bulk Actions

- **Equivalence partitioning:** Empty, null-ASN, one-entry, and multi-entry
  restoration maps are covered.
- **Boundary value analysis:** ASN values include `None`, zero, a normal
  positive value, and a high document ID.
- **Expected outcomes:** Each backup entry produces exactly one targeted update,
  and null values remain null rather than being silently converted.

## Traceability

The CSV cases use IDs `EP-01` through `BVA-05`. The workbook in `docs/` retains
the earlier black-box test cases and ownership record for the same M1, M2, and
M6 modules.
