# Deterministic RAG Ingestion Contract

## Purpose

This directory prepares the verified Summa corpus for ingestion while **not** creating embeddings or a vector database. `records.jsonl` is the canonical ingestion stream; source corpus files remain unchanged elsewhere in this release.

## Required ingestion behavior

Load records in `canonical_sort_key` order. Use `document_id` as the immutable vector-store primary key and use `source_text_sha256` to make re-indexing incremental. Embed `retrieval_text`, while preserving `canonical_citation`, `part`, `question`, `article`, `section`, `record_type`, `semantic_role`, and `parent_question_id` as metadata.

Question prologues are deliberately distinct from article sections. For queries about order, scope, distinctions, or how Aquinas frames a treatise, boost `record_type = question_prologue` and optionally include the adjacent article sections. For article-specific objections and replies, filter or rerank on article and section metadata.

## Recommended retrieval architecture

1. **Lexical retrieval** over `retrieval_text` for names, citations, Latin terms, and exact formulations.
2. **Dense retrieval** over the same field for conceptual and analogical metaphysical questions.
3. **Metadata-aware fusion** that raises part/question prologues for structural questions and article sections for argumentative questions.
4. **Cross-encoder or LLM reranking** restricted to the fused candidate set.
5. **Citation-bound generation** that returns canonical citations from selected records and does not cite passages absent from retrieval.

## Not yet performed

No embedding model, vector database, hybrid-search engine, reranker, or chat model has been selected or configured in this release. The next implementation decision should be a benchmarked retrieval profile, not blind bulk embedding.
