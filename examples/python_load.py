#!/usr/bin/env python3
"""Read a few records from the ordered Summa RAG shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path("data/rag/by-part"))
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    paths = sorted(args.path.glob("*.jsonl")) if args.path.is_dir() else [args.path]
    emitted = 0
    for path in paths:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                record = json.loads(line)
                print(
                    json.dumps(
                        {
                            "document_id": record["document_id"],
                            "citation": record["canonical_citation"],
                            "record_type": record["record_type"],
                            "retrieval_text": record["retrieval_text"][:240],
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                emitted += 1
                if emitted >= args.limit:
                    return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
