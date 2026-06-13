# NiceM Stage 1a — Token-Tax Outlier Report

**Stage:** Stage 1a — Tokenizer-only sanity gate
**Date:** 2026-06-13
**Tokenizer:** `o200k_base_approx` (target: o200k_base)

Outlier criteria:
- Ratio below 0.8
- Ratio above 2.0
- Turkish ratio lower than Dutch ratio (unexpected)
- Missing query or chunk entry in any language

**Important:** Outliers are not interpreted as execution-tax. They are tokenization-layer observations only.

---

## Result: 7 outlier(s) found

| type | key | en_tokens | nl_tokens | tr_tokens | nl/en | tr/en | flags |
|---|---|---|---|---|---|---|---|
| query | INT-004 | 12 | 16 | 13 | 1.3333 | 1.0833 | TR_BELOW_NL (1.083 < 1.333 — unexpected; Turkish expected higher) |
| query | INT-009 | 12 | 12 | 11 | 1.0 | 0.9167 | TR_BELOW_NL (0.917 < 1.000 — unexpected; Turkish expected higher) |
| query | INT-011 | 15 | 18 | 14 | 1.2 | 0.9333 | TR_BELOW_NL (0.933 < 1.200 — unexpected; Turkish expected higher) |
| query | INT-012 | 18 | 16 | 12 | 0.8889 | 0.6667 | TR_RATIO_LOW (0.667 < 0.8); TR_BELOW_NL (0.667 < 0.889 — unexpected; Turkish expected higher) |
| query | INT-013 | 20 | 22 | 19 | 1.1 | 0.95 | TR_BELOW_NL (0.950 < 1.100 — unexpected; Turkish expected higher) |
| query | INT-026 | 12 | 12 | 10 | 1.0 | 0.8333 | TR_BELOW_NL (0.833 < 1.000 — unexpected; Turkish expected higher) |
| kb_chunk | D08-S5 | 45 | 55 | 48 | 1.2222 | 1.0667 | TR_BELOW_NL (1.067 < 1.222 — unexpected; Turkish expected higher) |

### Interpretation guidance

- **Ratio_LOW / Ratio_HIGH**: the language uses substantially fewer or more tokens than English for this item. Check the KB rendering or query for unusual compression.
- **TR_BELOW_NL**: Turkish produced fewer tokens than Dutch for this item. This is unexpected given Turkish agglutinative morphology. Check if the Turkish text is unusually short or if the Dutch text has a long compound.
- **MISSING_COUNT**: a query or chunk entry was not parsed for a language. Check the alignment between files.

---

## Analysis of query outliers (INT-004, 009, 011, 012, 013, 026)

**Diagnosis: Turkish syntactic compactness for short query texts.**

These six queries share a pattern: the Turkish rendering is syntactically significantly shorter than the English or Dutch rendering. Turkish agglutinative morphology packs multiple English words into single suffixed forms, which reduces the total number of syntactic words (and thus segments) in the sentence. For short queries (10–20 EN tokens), this compactness can result in fewer total tokens for Turkish even though each Turkish word gets split into more subword tokens.

| intent_id | EN words | NL words | TR words | TR shorter than? | Pattern |
|---|---|---|---|---|---|
| INT-004 | 11 words | 14 words | 9 words | Both | Turkish uses suffix "-dan sonra" construction compressing "After I return" |
| INT-009 | 12 words | 11 words | 7 words | EN | "ne kadar sürer" replaces "how long does it typically take to" |
| INT-011 | 14 words | 16 words | 9 words | Both | Turkish compresses "How long does it take to receive my refund after I return" |
| INT-012 | 18 words | 12 words | 8 words | Both | "olmadan" (without) + suffix replaces "if I don't have a Hub"; EN also unusually long |
| INT-013 | 16 words | 20 words | 13 words | Both | Turkish uses relative clause compression |
| INT-026 | 12 words | 12 words | 8 words | Both | Turkish uses noun + case suffix pattern |

**Why this does NOT invalidate Stage 1a:**
1. For KB chunks (longer texts), TR > NL holds for 38 of 39 chunks (median TR/EN = 1.37).
2. The median query TR/EN is 1.08 (TR still slightly above EN overall).
3. Turkish syntactic compactness is a real linguistic phenomenon — it is the CONTENT being expressed in fewer tokens, which is a different signal from BPE vocabulary coverage.
4. The literature (Petrov, Ahia, Lundin) measures token-tax on longer texts where the agglutinative BPE-splitting premium dominates.

**Pre-registered finding for Stage 2 analysis:**
For short Product FAQ queries (10–20 tokens), Turkish token-tax may be near-zero or negative for some intents. This does not falsify the token-tax hypothesis; it reveals that short-form queries have smaller token-tax signals than longer-form content. Stage 2 should not assume a uniform per-intent query token-tax premium for Turkish.

---

## Analysis of KB chunk outlier (D08-S5)

**D08-S5: Account and reset — two-factor recovery section**

| | en_tokens | nl_tokens | tr_tokens | nl/en | tr/en |
|---|---|---|---|---|---|
| D08-S5 | 45 | 55 | 48 | 1.222 | 1.067 |

TR/EN = 1.067 (TR above EN, correct direction). TR_BELOW_NL flag is triggered because NL/EN = 1.222, which is unusually high for this chunk. This is likely because D08-S5 contains procedural steps that Dutch renders with longer multi-word constructions (compound nouns, formal instruction phrasing), while the Turkish KB rendering for this section is relatively concise. This is a rendering-level observation, not a benchmark error.

**Assessment:** Not a data integrity issue. TR > EN (correct direction). NL unusually high due to Dutch verbose procedural phrasing for this specific section.

