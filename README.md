# Paperless-ngx Unit Test Automation

This repository contains Azka's Assignment 3 contribution for Paperless-ngx:

- M1 Auth & Users
- M2 Documents
- M6 Trash & Bulk Actions

The tests exercise the real Paperless-ngx source. Set `PAPERLESS_SOURCE_ROOT`
to the local Paperless-ngx checkout before running them; the source checkout is
kept separate so this submission repository remains focused on test automation.

## Setup

From PowerShell:

```powershell
$env:PAPERLESS_SOURCE_ROOT = "C:\Users\fazia\source\repos\paperless-ngx"
$env:PAPERLESS_SECRET_KEY = "assignment-local-only-change-this"
uv sync --group test
```

The source checkout must have its development dependencies installed:

```powershell
cd $env:PAPERLESS_SOURCE_ROOT
uv sync --group dev
```

## Running the test suites

Run all Assignment 3 tests:

```powershell
cd C:\Users\fazia\Downloads\Testing-Paperless-ngx
uv run pytest
```

Run suites by module:

```powershell
uv run pytest -m auth
uv run pytest -m documents
uv run pytest -m trash_bulk
```

Run in parallel:

```powershell
uv run pytest -n auto
```

The CSV-driven tests read `test_data/m2_path_cases.csv`. Test design notes are
in `docs/azka_test_design.md`, and the Excel workbook is in `docs/`.