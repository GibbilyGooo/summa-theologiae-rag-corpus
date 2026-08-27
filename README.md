# Summa Theologiae Canonical RAG Corpus

A validated, citation-preserving, vendor-neutral retrieval corpus of St. Thomas Aquinas's *Summa Theologiae*, prepared for Catholic AI, theological research, education, search, and citation-grounded generation.

This repository was prepared for [Theology AI](https://theologyai.net) by AD IPSUM and is released publicly for the service of the Church and the wider research community.

## What is included

- **24,611 canonical retrieval records**
- **23,997 article-section records** covering objections, sed contra, respondeo, and replies
- **614 part and question prologues**
- All five divisions: I, I-II, II-II, III, and the Supplement
- **2,517,850 source-text words**
- Stable document IDs and canonical citations
- Source-text SHA-256 hashes for incremental indexing
- Five ordered, ingestion-ready shards in `data/rag/by-part/`
- A dependency-free script that reconstructs the byte-identical unified stream
- Provenance, recovery evidence, audit reports, and page-image verification for manually resolved cases
- No embeddings, vector database, model dependency, or deployment configuration

## Why this corpus exists

General-purpose language models often explain Aquinas competently but retrieve the wrong locus, omit an objection or reply, confuse question prologues with article text, or cite a question without identifying the supporting article. This corpus preserves Aquinas's argumentative structure and supplies stable metadata suitable for citation-bound generation.

## Quick start

Validate the repository using only the Python standard library:

```bash
python scripts/validate_corpus.py
```

Read the first few ingestion records:

```bash
python examples/python_load.py --limit 3
```

Each line in the ordered files under `data/rag/by-part/` is an independent JSON object. Embed `retrieval_text`; retain the remaining fields as searchable/filterable metadata.

```python
import glob, json

for path in sorted(glob.glob("data/rag/by-part/*.jsonl")):
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            vector_text = record["retrieval_text"]
            citation = record["canonical_citation"]
            document_id = record["document_id"]
```

Rebuild the original single-file stream when an ingestion tool expects one file:

```bash
python scripts/build_unified_rag.py
```

The resulting `build/records.jsonl` has SHA-256 `2a3e874d1dbec3722df093c9c22ecf90a80d700c7db90c5dcaca35c128a6e788`.

## Recommended retrieval design

1. Combine lexical and dense retrieval over `retrieval_text`.
2. Preserve filters for part, question, article, section, record type, and semantic role.
3. Boost question prologues for questions about Aquinas's scope or order.
4. Expand article hits to nearby objections, sed contra, respondeo, and replies when synthesis requires the full argument.
5. Rerank only the fused candidate set.
6. Permit the answer model to cite only loci present in the retrieved evidence packet.

See [the ingestion contract](docs/INGESTION_CONTRACT.md) and [retrieval guide](docs/RETRIEVAL_GUIDE.md) for implementation details.

## Repository layout

```text
data/core/          Source-preserving article-section records by Summa part
data/prologues/     Part and question prologues
data/rag/by-part/   Ordered, normalized ingestion shards
metadata/           Release and ingestion manifests
provenance/         Recovery evidence and source research
reports/            Independent validation results
docs/               Schema, validation, and retrieval guidance
scripts/            Dependency-free validation tooling
examples/           Minimal loading example
```

## Validation status

The frozen source release and normalized ingestion layer both passed their final audits:

- 24,611 records
- 24,611 stable document IDs
- Canonical ordering: PASS
- Source-text traceability: PASS
- Hard validation issues: 0
- Embeddings created: no
- Vector database created: no

The validator in this repository independently recomputes record counts, IDs, source-text hashes, canonical ordering, source references, and the frozen ingestion-file hash.

## Text, sources, and rights

The underlying English translation is the public-domain Dominican Fathers translation first published in the early twentieth century. New Advent was the primary digital transcription source for the article-section layer; historical print scans and CCEL were used for verification and prologue recovery. New Advent's online edition and website carry their own copyright notices and are fully credited here.

See [COPYRIGHT_AND_SOURCES.md](COPYRIGHT_AND_SOURCES.md) before redistributing or republishing the corpus. This repository does not include New Advent website code, layout, advertising, or navigation material.

The repository's original code and documentation are available under the MIT License. To the extent AD IPSUM owns copyright in the original corpus organization and metadata, those data-layer rights are dedicated under CC0 1.0. No ownership is asserted over Aquinas's text or the historical Dominican translation.

## Citation

Use the metadata in [CITATION.cff](CITATION.cff), or cite:

> AD IPSUM. *Summa Theologiae Canonical RAG Corpus*, version 3.0.0, 2026.

When quoting Aquinas, cite the canonical *Summa* locus as well, for example `ST I, q.14, a.13`.

## Contributions

Corrections are welcome when supported by a page image, historical edition, or other verifiable source witness. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Important scope note

This is a retrieval corpus, not an official critical edition and not a substitute for theological judgment. The Supplement is included and identified as such. Applications should distinguish Aquinas's theological authority from the authority of Scripture and the Magisterium.
