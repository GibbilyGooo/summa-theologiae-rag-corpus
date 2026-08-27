#!/usr/bin/env python3
"""Split a unified Summa RAG JSONL stream into deterministic part shards."""

from __future__ import annotations

import argparse
import json
from contextlib import ExitStack
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PART_FILES = {
    "I": "01-I.jsonl",
    "I-II": "02-I-II.jsonl",
    "II-II": "03-II-II.jsonl",
    "III": "04-III.jsonl",
    "Supplement": "05-Supplement.jsonl",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, default=ROOT / "data" / "rag" / "records.jsonl")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data" / "rag" / "by-part")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    counts = {part: 0 for part in PART_FILES}
    with ExitStack() as stack:
        outputs = {
            part: stack.enter_context((args.output_dir / filename).open("wb"))
            for part, filename in PART_FILES.items()
        }
        with args.source.open("rb") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                part = record.get("part")
                if part not in outputs:
                    raise SystemExit(f"Line {line_number}: unexpected part {part!r}")
                outputs[part].write(line)
                counts[part] += 1

    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
