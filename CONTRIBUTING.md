# Contributing

Corrections, validation improvements, additional source witnesses, and vendor-neutral retrieval examples are welcome.

## Text corrections

Every proposed text correction should include:

1. the exact `document_id` and `canonical_citation`;
2. the current text;
3. the proposed text;
4. a stable source URL, scan identifier, and page/leaf number; and
5. an explanation of whether the discrepancy is transcription, OCR, punctuation, structure, or edition variation.

Do not silently modernize spelling, punctuation, Scripture references, or theological terminology. Edition variants should be documented rather than collapsed without evidence.

## Schema changes

Schema changes must preserve stable document IDs or supply an explicit migration map. Retrieval conveniences belong in derived fields; source-preserving text should remain unchanged.

## Validation

Run before submitting changes:

```bash
python scripts/validate_corpus.py
```

The validator must finish with `PASS` and zero hard issues.
