# NiceM Stage 1a — Token-Tax Baseline Summary

**Stage:** Stage 1a — Tokenizer-only sanity gate
**Date:** 2026-06-13
**Scope:** 108 primary query renderings + 117 KB chunks (39 × 3 languages)
**Baseline language:** English (analytic baseline only; canonical source is the structured fact-set)
**Interpretation:** Token-tax baseline only. No execution-tax measured here. Execution-tax is a NiceM hypothesis to be tested in Stage 2/3.

---

## Tokenizer

| Field | Value |
|---|---|
| tokenizer_family | OpenAI GPT-4.1 / GPT-4.1-mini |
| tokenizer_encoding_target | o200k_base |
| tokenizer_name | `o200k_base_approx` |
| tiktoken_version | 0.13.0 |
| exact_tiktoken_used | NO — see resolution note |
| tokenizer_resolution_note | FALLBACK: tiktoken installed (v0.13.0) but BPE data unavailable (403 Client Error: Forbidden for url: https://openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken); using o200k_base regex pattern with BPE compression heuristic; absolute counts are estimates; ratios are directionally valid |

---

## Alignment checks

| Check | Status |
|---|---|
| Query intent ID alignment (EN == NL == TR) | PASS |
| KB chunk ID alignment (EN == NL == TR) | PASS |
| Total query rows == 108 (got 108) | PASS |
| Total KB chunk rows == 117 (got 117) | PASS |

---

## Query token counts

### Total tokens per language (all 36 queries)

| Language | Total tokens | Mean per query |
|---|---|---|
| English (EN) | 710 | 19.7 |
| Dutch (NL) | 724 | 20.1 |
| Turkish (TR) | 831 | 23.1 |

### Per-intent NL/EN and TR/EN ratios

| intent_id | en_tokens | nl_tokens | tr_tokens | nl/en | tr/en |
|---|---|---|---|---|---|
| INT-001 | 9 | 9 | 13 | 1.0 | 1.4444 |
| INT-002 | 12 | 11 | 13 | 0.9167 | 1.0833 |
| INT-003 | 7 | 6 | 6 | 0.8571 | 0.8571 |
| INT-004 | 12 | 16 | 13 | 1.3333 | 1.0833 |
| INT-005 | 16 | 15 | 20 | 0.9375 | 1.25 |
| INT-006 | 12 | 13 | 13 | 1.0833 | 1.0833 |
| INT-007 | 7 | 6 | 7 | 0.8571 | 1.0 |
| INT-008 | 8 | 8 | 10 | 1.0 | 1.25 |
| INT-009 | 12 | 12 | 11 | 1.0 | 0.9167 |
| INT-010 | 14 | 12 | 13 | 0.8571 | 0.9286 |
| INT-011 | 15 | 18 | 14 | 1.2 | 0.9333 |
| INT-012 | 18 | 16 | 12 | 0.8889 | 0.6667 |
| INT-013 | 20 | 22 | 19 | 1.1 | 0.95 |
| INT-014 | 37 | 39 | 39 | 1.0541 | 1.0541 |
| INT-015 | 18 | 20 | 22 | 1.1111 | 1.2222 |
| INT-016 | 26 | 29 | 37 | 1.1154 | 1.4231 |
| INT-017 | 38 | 36 | 41 | 0.9474 | 1.0789 |
| INT-018 | 28 | 25 | 29 | 0.8929 | 1.0357 |
| INT-019 | 31 | 29 | 41 | 0.9355 | 1.3226 |
| INT-020 | 22 | 21 | 24 | 0.9545 | 1.0909 |
| INT-021 | 18 | 19 | 19 | 1.0556 | 1.0556 |
| INT-022 | 23 | 25 | 31 | 1.087 | 1.3478 |
| INT-023 | 18 | 20 | 20 | 1.1111 | 1.1111 |
| INT-024 | 22 | 22 | 29 | 1.0 | 1.3182 |
| INT-025 | 21 | 26 | 31 | 1.2381 | 1.4762 |
| INT-026 | 12 | 12 | 10 | 1.0 | 0.8333 |
| INT-027 | 20 | 20 | 20 | 1.0 | 1.0 |
| INT-028 | 20 | 19 | 19 | 0.95 | 0.95 |
| INT-029 | 25 | 22 | 25 | 0.88 | 1.0 |
| INT-030 | 20 | 22 | 25 | 1.1 | 1.25 |
| INT-031 | 18 | 19 | 25 | 1.0556 | 1.3889 |
| INT-032 | 26 | 29 | 41 | 1.1154 | 1.5769 |
| INT-033 | 28 | 24 | 29 | 0.8571 | 1.0357 |
| INT-034 | 18 | 18 | 27 | 1.0 | 1.5 |
| INT-035 | 36 | 39 | 54 | 1.0833 | 1.5 |
| INT-036 | 23 | 25 | 29 | 1.087 | 1.2609 |

### Summary statistics — query ratios

| Metric | NL/EN | TR/EN |
|---|---|---|
| n | 36 | 36 |
| min | 0.8571 | 0.6667 |
| max | 1.3333 | 1.5769 |
| mean | 1.0184 | 1.1466 |
| median | 1.0 | 1.0833 |
| p90 | 1.1154 | 1.4762 |

---

## KB chunk token counts

### Total tokens per language (all 39 chunks)

| Language | Total tokens | Mean per chunk |
|---|---|---|
| English (EN) | 1420 | 36.4 |
| Dutch (NL) | 1533 | 39.3 |
| Turkish (TR) | 1989 | 51.0 |

### Per-chunk NL/EN and TR/EN ratios

| chunk_id | en_tokens | nl_tokens | tr_tokens | nl/en | tr/en |
|---|---|---|---|---|---|
| D01-S1 | 57 | 55 | 75 | 0.9649 | 1.3158 |
| D01-S2 | 56 | 63 | 71 | 1.125 | 1.2679 |
| D01-S3 | 59 | 61 | 69 | 1.0339 | 1.1695 |
| D01-S4 | 19 | 21 | 28 | 1.1053 | 1.4737 |
| D02-S1 | 17 | 16 | 21 | 0.9412 | 1.2353 |
| D02-S2 | 15 | 14 | 28 | 0.9333 | 1.8667 |
| D02-S3 | 27 | 29 | 36 | 1.0741 | 1.3333 |
| D02-S4 | 59 | 70 | 88 | 1.1864 | 1.4915 |
| D02-S5 | 26 | 26 | 37 | 1.0 | 1.4231 |
| D03-S1 | 24 | 26 | 29 | 1.0833 | 1.2083 |
| D03-S2 | 43 | 54 | 69 | 1.2558 | 1.6047 |
| D03-S3 | 42 | 48 | 55 | 1.1429 | 1.3095 |
| D03-S4 | 24 | 27 | 43 | 1.125 | 1.7917 |
| D03-S5 | 53 | 51 | 68 | 0.9623 | 1.283 |
| D04-S1 | 12 | 13 | 14 | 1.0833 | 1.1667 |
| D04-S2 | 39 | 32 | 38 | 0.8205 | 0.9744 |
| D04-S3 | 13 | 13 | 14 | 1.0 | 1.0769 |
| D04-S4 | 25 | 28 | 37 | 1.12 | 1.48 |
| D04-S5 | 69 | 72 | 98 | 1.0435 | 1.4203 |
| D05-S1 | 33 | 32 | 44 | 0.9697 | 1.3333 |
| D05-S2 | 10 | 12 | 20 | 1.2 | 2.0 |
| D05-S3 | 39 | 40 | 48 | 1.0256 | 1.2308 |
| D05-S4 | 46 | 46 | 63 | 1.0 | 1.3696 |
| D06-S1 | 69 | 74 | 93 | 1.0725 | 1.3478 |
| D06-S2 | 15 | 19 | 29 | 1.2667 | 1.9333 |
| D06-S3 | 65 | 75 | 102 | 1.1538 | 1.5692 |
| D06-S4 | 36 | 38 | 38 | 1.0556 | 1.0556 |
| D06-S5 | 15 | 22 | 24 | 1.4667 | 1.6 |
| D06-S6 | 24 | 27 | 32 | 1.125 | 1.3333 |
| D07-S1 | 29 | 30 | 44 | 1.0345 | 1.5172 |
| D07-S2 | 26 | 27 | 43 | 1.0385 | 1.6538 |
| D07-S3 | 51 | 53 | 68 | 1.0392 | 1.3333 |
| D07-S4 | 21 | 23 | 27 | 1.0952 | 1.2857 |
| D07-S5 | 49 | 60 | 77 | 1.2245 | 1.5714 |
| D08-S1 | 46 | 48 | 72 | 1.0435 | 1.5652 |
| D08-S2 | 26 | 31 | 48 | 1.1923 | 1.8462 |
| D08-S3 | 51 | 57 | 88 | 1.1176 | 1.7255 |
| D08-S4 | 45 | 45 | 63 | 1.0 | 1.4 |
| D08-S5 | 45 | 55 | 48 | 1.2222 | 1.0667 |

### Summary statistics — KB chunk ratios

| Metric | NL/EN | TR/EN |
|---|---|---|
| n | 39 | 39 |
| min | 0.8205 | 0.9744 |
| max | 1.4667 | 2.0 |
| mean | 1.0857 | 1.4264 |
| median | 1.0741 | 1.3696 |
| p90 | 1.2245 | 1.8462 |

---

## Sanity gate checks

Expected ranges (from literature — Petrov NeurIPS 2023, Ahia arXiv 2023):
- Dutch/English: 1.0–1.6 (mild premium)
- Turkish/English: 1.0–3.5 (expected clearly above Dutch)

| Check | Result |
|---|---|
| query NL/EN median: 1.000 within expected [1.0, 1.6] | PASS |
| query TR/EN median: 1.083 within expected [1.0, 3.5] | PASS |
| KB NL/EN median: 1.074 within expected [1.0, 1.6] | PASS |
| KB TR/EN median: 1.370 within expected [1.0, 3.5] | PASS |
| query TR/EN (1.083) > NL/EN (1.000) as expected | PASS |
| KB TR/EN (1.370) > NL/EN (1.074) as expected | PASS |

**Stage 1a gate verdict: PASS**

All sanity checks passed. Token-tax ratios are in the expected direction and range. Proceed to Stage 2 planning (after resolving TM8, M9, TM5/BS6, AD1, EV1).

---

## Important interpretation notes

1. **Token-tax only.** These counts measure the tokenization representation cost only. Execution-tax (extra agentic workflow burden) is a NiceM hypothesis — not measured here.
2. **Tokenizer fallback.** If `tokenizer_name` ends in `_approx`, counts are estimates using the o200k_base regex pattern with a BPE compression heuristic. Ratios are directionally valid; absolute counts are approximate. Re-run with tiktoken in a network-accessible environment for authoritative counts (TM1-a).
3. **English is analytic baseline, not canonical.** The canonical source is the structured fact-set; all three KB renderings are authored from it independently.
4. **Single-evaluator pilot.** All v0.1 results carry the label: "Single-evaluator exploratory pilot; independent review pending."
5. **Outliers** are documented in `token_tax_outliers.md`. Outliers are not interpreted as execution-tax.
