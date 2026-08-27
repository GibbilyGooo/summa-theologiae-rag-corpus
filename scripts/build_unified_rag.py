#!/usr/bin/env python3
"""Rebuild the byte-identical unified RAG stream from ordered GitHub shards."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARDS = ROOT / "data" / "rag" / "by-part"
EXPECTED_SHA256 = "2a3e874d1dbec3722df093c9c22ecf90a80d700c7db90c5dcaca35c128a6e788"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "records.jsonl",
        help="Destination for the rebuilt unified stream",
    )
    args = parser.parse_args()

    paths = sorted(SHARDS.glob("*.jsonl"))
    if not paths:
        raise SystemExit(f"No shards found in {SHARDS}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    with args.output.open("wb") as destination:
        for path in paths:
            with path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    destination.write(block)
                    digest.update(block)

    observed = digest.hexdigest()
    if observed != EXPECTED_SHA256:
        args.output.unlink(missing_ok=True)
        raise SystemExit(f"SHA-256 mismatch: {observed}")

    print(f"Wrote {args.output}")
    print(f"SHA-256 {observed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
