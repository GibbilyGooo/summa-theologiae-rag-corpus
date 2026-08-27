# RAG Ingestion Status

The verified Summa corpus is complete, canonically ordered, and accompanied by a deterministic ingestion stream at `rag_staging/records.jsonl`.

The corpus is **not yet embedded**, and no vector database, sparse index, reranker, or chat model has been selected. This is intentional: the next step is a retrieval-quality benchmark and infrastructure decision, not irreversible bulk indexing.

Use `rag_staging/INGESTION_CONTRACT.md` and `rag_staging/ingestion_manifest.json` as the authoritative handoff for vectorization.
