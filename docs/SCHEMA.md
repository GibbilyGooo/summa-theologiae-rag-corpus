# Corpus Schema

## Source-preserving records

Files in `data/core/` use:

| Field | Meaning |
|---|---|
| `work` | Work title |
| `author` | Thomas Aquinas |
| `part` | I, I-II, II-II, III, or Supplement |
| `question` | Question number |
| `article` | Article number |
| `article_title` | Article title |
| `section` | Objection, sed contra, respondeo, or reply identifier |
| `canonical_citation` | Human-readable canonical locus |
| `text` | Source-preserving English text |

Files in `data/prologues/` use the same basic fields. Part prologues may have null question/article values; question prologues have a question number and null article.

## Ingestion records

`data/rag/records.jsonl` contains one normalized record per source record:

| Field | Meaning |
|---|---|
| `schema_version` | Ingestion schema version |
| `document_id` | Immutable vector/index primary key |
| `corpus_release` | Frozen source release |
| `canonical_sort_key` | Deterministic global ordering |
| `record_type` | Article section, question prologue, or part prologue |
| `semantic_role` | Retrieval role |
| `source_relpath` | Canonical source file |
| `source_line_number` | One-indexed JSONL source line |
| `source_text_sha256` | SHA-256 of source `text` |
| `canonical_citation` | Citation to return with evidence |
| `part`, `question`, `article`, `section` | Structural filters |
| `parent_question_id` | Question grouping key where applicable |
| `retrieval_text` | Text recommended for lexical/dense indexing |

## Stability rules

- Treat `document_id` as immutable.
- Treat `source_text_sha256` as the incremental-reindex signal.
- Do not fabricate article-level metadata for part/question prologues.
- Keep question prologues distinct from the first article of a question.
- Preserve source order using `canonical_sort_key`.
