# Retrieval Guide

## Minimal indexing profile

- Index: the ordered files in `data/rag/by-part/` (or rebuild one stream with `python scripts/build_unified_rag.py`)
- Primary key: `document_id`
- Embedding/lexical field: `retrieval_text`
- Metadata: every remaining field
- Incremental update key: `source_text_sha256`

## Hybrid retrieval

Dense retrieval is useful for conceptual questions such as divine simplicity, analogy, providence, virtue, or sacramental causality. Lexical retrieval is important for exact loci, Latin terms, named objections, Scripture references, and article titles. Fuse both result sets before reranking.

## Structural expansion

When one article section is retrieved, consider retrieving siblings sharing the same part/question/article:

- objections define the difficulty;
- sed contra supplies the counter-authority;
- respondeo contains Aquinas's central determination; and
- replies answer individual objections.

Do not always inject every sibling. Expand when the user asks for a complete argument, an objection/reply analysis, or a precision metaphysical explanation.

Question prologues should receive a boost for questions about the organization, scope, or distinctions of a treatise. They should not displace a directly responsive article merely because they share vocabulary.

## Citation-bound generation

Pass selected records to the answer model with `document_id`, `canonical_citation`, and source text. Require citations to be drawn only from those records. Validate citations after generation against the evidence packet.

## Authority context

The *Summa Theologiae* is a premier theological source, not an act of the Magisterium. Catholic applications should route doctrinal questions to appropriate Catechism, conciliar, papal, and dicastery sources when authoritative teaching is required, using Aquinas for theological explanation and synthesis.
