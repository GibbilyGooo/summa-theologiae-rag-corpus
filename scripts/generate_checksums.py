#!/usr/bin/env python3
"""Generate SHA256SUMS for the public release payload."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "SHA256SUMS"
EXCLUDED_PARTS = {".git", "build", "__pycache__"}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main() -> int:
    paths = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != OUTPUT
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    ]
    lines = [f"{digest(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in sorted(paths)]
    OUTPUT.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT} with {len(lines)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
