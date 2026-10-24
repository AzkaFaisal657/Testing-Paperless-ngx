from __future__ import annotations

import os
import sys
from pathlib import Path


source_root = Path(
    os.environ.get("PAPERLESS_SOURCE_ROOT", ""),
).expanduser()
if not source_root.is_dir():
    raise RuntimeError(
        "PAPERLESS_SOURCE_ROOT must point to the Paperless-ngx checkout",
    )

source_path = source_root / "src"
if not source_path.is_dir():
    raise RuntimeError(f"Paperless source directory does not exist: {source_path}")

sys.path.insert(0, str(source_path))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paperless.settings")
os.environ.setdefault(
    "PAPERLESS_SECRET_KEY",
    "assignment-local-only-change-this",
)
os.environ.setdefault("PAPERLESS_DBENGINE", "sqlite")
os.environ.setdefault("PAPERLESS_REDIS", "redis://localhost:6379")

import django

django.setup()
