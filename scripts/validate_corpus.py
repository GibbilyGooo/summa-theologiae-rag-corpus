#!/usr/bin/env python3
"""Portable integrity validator for the public Summa RAG corpus."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "data" / "core"
PROLOGUES = ROOT / "data" / "prologues"
RAG = ROOT / "data" / "rag" / "records.jsonl"
RAG_SHARDS = ROOT / "data" / "rag" / "by-part"
MANIFEST = ROOT / "metadata" / "ingestion_manifest.json"
EXPECTED_CORE = 23_997
EXPECTED_PROLOGUES = 614
EXPECTED_TOTAL = 24_611


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_files(paths: list[Path]) -> str:
    result = hashlib.sha256()
    for path in paths:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                result.update(block)
    return result.hexdigest()


def load_jsonl(path: Path, issues: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append(f"{path.relative_to(ROOT)}:{line_number}: {exc}")
                continue
            if not isinstance(value, dict):
                issues.append(f"{path.relative_to(ROOT)}:{line_number}: record is not an object")
                continue
            records.append(value)
    return records


def main() -> int:
    issues: list[str] = []
    sources: dict[str, list[dict[str, Any]]] = {}

    core_count = 0
    for path in sorted(CORE.glob("*.jsonl")):
        records = load_jsonl(path, issues)
        sources[f"core/{path.name}"] = records
        core_count += len(records)

    prologue_count = 0
    for path in sorted(PROLOGUES.glob("*.jsonl")):
        records = load_jsonl(path, issues)
        sources[f"prologues/{path.name}"] = records
        prologue_count += len(records)

    shard_paths = sorted(RAG_SHARDS.glob("*.jsonl"))
    rag_paths = shard_paths if shard_paths else [RAG]
    rag_records: list[dict[str, Any]] = []
    for path in rag_paths:
        rag_records.extend(load_jsonl(path, issues))
    document_ids: set[str] = set()
    sort_keys: list[str] = []

    for position, record in enumerate(rag_records, 1):
        document_id = record.get("document_id")
        if not isinstance(document_id, str) or not document_id:
            issues.append(f"RAG line {position}: missing document_id")
        elif document_id in document_ids:
            issues.append(f"RAG line {position}: duplicate document_id {document_id}")
        else:
            document_ids.add(document_id)

        sort_key = record.get("canonical_sort_key")
        if not isinstance(sort_key, str) or not sort_key:
            issues.append(f"RAG line {position}: missing canonical_sort_key")
        else:
            sort_keys.append(sort_key)

        relpath = record.get("source_relpath")
        line_number = record.get("source_line_number")
        source_records = sources.get(str(relpath))
        if source_records is None:
            issues.append(f"RAG line {position}: unknown source {relpath}")
            continue
        if not isinstance(line_number, int) or not 1 <= line_number <= len(source_records):
            issues.append(f"RAG line {position}: invalid source line {line_number}")
            continue

        source = source_records[line_number - 1]
        text = source.get("text")
        if not isinstance(text, str) or not text:
            issues.append(f"RAG line {position}: source text is empty")
            continue
        if digest_text(text) != record.get("source_text_sha256"):
            issues.append(f"RAG line {position}: source text hash mismatch")
        if source.get("canonical_citation") != record.get("canonical_citation"):
            issues.append(f"RAG line {position}: canonical citation mismatch")

    if core_count != EXPECTED_CORE:
        issues.append(f"core record count {core_count} != {EXPECTED_CORE}")
    if prologue_count != EXPECTED_PROLOGUES:
        issues.append(f"prologue record count {prologue_count} != {EXPECTED_PROLOGUES}")
    if len(rag_records) != EXPECTED_TOTAL:
        issues.append(f"RAG record count {len(rag_records)} != {EXPECTED_TOTAL}")
    if core_count + prologue_count != EXPECTED_TOTAL:
        issues.append("canonical source total does not equal expected total")
    if sort_keys != sorted(sort_keys) or len(sort_keys) != len(set(sort_keys)):
        issues.append("canonical sort keys are not strictly ordered and unique")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    observed_rag_hash = digest_files(rag_paths)
    if observed_rag_hash != manifest.get("ingestion_file_sha256"):
        issues.append("ingestion file SHA-256 does not match manifest")
    if manifest.get("embedding_status") != "NOT_EMBEDDED":
        issues.append("manifest embedding status is unexpected")
    if manifest.get("vector_database_status") != "NOT_CREATED":
        issues.append("manifest vector database status is unexpected")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "core_records": core_count,
        "prologue_records": prologue_count,
        "rag_records": len(rag_records),
        "unique_document_ids": len(document_ids),
        "ingestion_file_sha256": observed_rag_hash,
        "hard_issues": len(issues),
        "issues": issues[:100],
        "issues_truncated": max(0, len(issues) - 100),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
