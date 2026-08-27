# Validation

The source release passed separate merge, recovery, page-image, and RAG-ingestion audits. The public validator performs an additional portable check using only Python's standard library.

Run:

```bash
python scripts/validate_corpus.py
```

It verifies:

- all JSONL files parse;
- canonical source record count is 24,611;
- core count is 23,997 and prologue count is 614;
- ingestion count is 24,611;
- document IDs are unique;
- canonical sort keys are strictly ordered and unique;
- each ingestion record resolves to its declared source line;
- `source_text_sha256` matches the source text;
- canonical citations match their source records;
- the frozen ingestion stream hash matches the release manifest; and
- no embedding or vector database is represented as having been created.

The validator prints JSON and exits nonzero on any hard issue.
