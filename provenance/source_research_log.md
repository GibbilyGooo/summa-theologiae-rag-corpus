# Browser-verified source findings — 2026-08-26

1. Internet Archive candidate `summatheologicao0015taqu` is visibly titled *The Summa Theologica of St. Thomas Aquinas: Part III. QQ. I–XXVI*, has metadata date 1924-01-01, publisher Burns Oates & Washbourne, English language, volume 15, and exposes public full text, hOCR, PDF, and page-image derivative links. It is a recoverable historical witness but fails the chosen strict 1920–1922 edition window on metadata; it is therefore a discovery/cross-check source only unless its scan itself establishes an eligible edition state.

2. The Documenta Catholica Omnia full-English PDF endpoint opened successfully as a browser PDF. It requires local document extraction and title-page review before it can be considered a source; no edition claim has been accepted from it.

## Additional stream-verified scan findings

- `summatheologi08thom` is a scan of *Part II (First Part), Third Number, QQ. XC–CXIV*, translated by the Fathers of the English Dominican Province, carrying a 1915 imprint and preserving the Q.90 introductory material. It is an English-Dominican primary witness but not a 1920–1922 calendar-year witness.
- `summatheologicao0015taqu` is a scan of *Part III, QQ. I–XXVI* with a 1913 imprimatur, the statement **“Second and Revised Edition,”** and the English Dominican translator credit. It preserves the Third Part prologue and the Q.1 introduction.
- `summatheologi18thom` is a scan of *Third Part, Fourth Number, QQ. LXXXIV–Supplement XXXIII*, with a 1917 imprint and the English Dominican translator credit. It preserves the Q.84 introductory material and the Supplement transition.

## Policy clarification required for accurate metadata

The historic English Dominican series was issued/reissued volume by volume over multiple years. The evidence now shows that **“Second and Revised Edition” is a series/edition-lineage statement, not a guarantee that every admissible physical volume bears a 1920–1922 calendar imprint.** The source policy should therefore be expressed as: *English Dominican Province translation; scan-backed original historical volume; the exact volume-level edition/imprint captured verbatim in provenance metadata.* The final merged corpus must never label every recovered item merely “1920” if the underlying volume itself says 1913, 1915, 1917, 1921, 1922, 1924, or 1927.

## Secondary comparison transcript

CCEL exposes clean, per-question introduction pages under the `summa.{part}_Q{n}.html` pattern. Tests for I-II Q.90, II-II Q.1, III Q.27, and Supplement Q.1 confirm that it preserves the full question introduction and enumerated points of inquiry. CCEL expressly identifies its text as the **Benziger Bros. edition, 1947**. It will therefore be used only as a secondary structural/textual comparison witness to identify and correct OCR defects in the historic scan-derived text. It will not be represented as the source edition for final recovered chunks.

## Final low-similarity diagnostics

Direct inspection of the final ten source contexts shows that the historical scan text matches the clean English-Dominican comparison text in substance. The low automated similarity scores arose because some scan volumes label the first article simply **“Article.”** (rather than “First Article”) or render a question numeral inaccurately (for example, Supplement Q.69 appears as `QUESTION UNIX.`), causing the generic boundary detector to carry article text into the comparison segment. Representative direct scan evidence confirms exact prologue text for I Q.110, I-II Q.110, II-II Q.5, II-II Q.80, II-II Q.128, II-II Q.143, II-II Q.159, III Q.29, and Supplement Q.50; the Supplement Q.69 source context identifies the expected resurrection treatise but requires the adjusted `Article.` delimiter. These are parser-boundary issues, not source availability or translation-family conflicts.

## Page-image verification limitation

An attempt to open the Internet Archive page viewer for the final manual-review sample (II-II Q.5) timed out in the available browsing environment. This failure is recorded rather than retried. The final three exceptional records are admitted only on the basis of directly retained historical OCR context showing the complete question heading, prologue text, and opening article boundary. Their provenance flags will state `historical_ocr_manual_review: PASS` and `page_image_verification: NOT_COMPLETED_ARCHIVE_VIEWER_TIMEOUT`; the final report will not claim visual page-image verification for these three records.
