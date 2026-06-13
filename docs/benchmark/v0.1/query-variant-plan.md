# NiceM Query Variant Plan — v0.1

**Status:** Planning artifact — variant texts not yet created
**Role:** Defines the design, naming, authoring rules, and quality gates for an optional robustness layer of query variants on top of the primary 108-query set
**Version:** qv-plan-v0.1.0
**Depends on:** `query-rendering-plan.md` (qr-plan-v0.1.0), `intent-set.md` (intent-v0.1.0), `query-rendering-en.md`, `query-rendering-nl.md`, `query-rendering-tr.md` (all qr-*-v0.1.0)
**Last updated:** 2026-06-13

---

## 1. Purpose

The primary query set (108 queries, 36 × 3 languages) uses one controlled query per intent per language. This is a deliberate methodological choice: a single controlled phrasing minimises authoring variation as a confound when comparing token counts and retrieval outcomes across languages.

However, a single query per intent is also narrow. Real users ask the same question in many ways — terse, verbose, formal, informal, contextualised, problem-description style. If NiceM's token-tax and execution-tax measurements are sensitive to phrasing choices, that sensitivity is a result worth knowing.

The query variant plan adds up to four additional phrasing variants per intent per language (V2–V5), keeping the primary rendering as V1. Together, the five variants per intent allow:

- robustness testing: does the system succeed across natural phrasing variation?
- phrasing-sensitivity analysis: do different phrasings produce different token counts, retrieval outcomes, or answer quality within a language?
- cross-language phrasing-controlled comparisons: do V2 variants in Turkish cost proportionally more than V2 variants in Dutch?

Variants are an **optional robustness layer**. The benchmark can run and produce valid results without them. They are not required before Stage 1.

---

## 2. Relationship to primary query renderings

The three primary query rendering files (`query-rendering-en.md`, `query-rendering-nl.md`, `query-rendering-tr.md`) are unchanged by this plan.

- Primary files remain the authoritative Stage 1a input
- Variants live in separate files (see §8)
- Stage 1a = 108 primary queries only
- Stage 1b = optional 540-query variant set (if created before Stage 1b is scheduled)
- Primary renderings and variants are never mixed in the same analysis pass without explicit labelling
- If variants are created later than the primary set, they are treated as a separate benchmark iteration, not as a correction to the primary set

The V1 slot in the variant naming scheme is occupied by the existing primary query. No V1 variant text is authored; V1 is always a pointer to the primary rendering.

---

## 3. Variant count and naming

**Variants per intent per language:** 5 (V1–V5)
**Total variant texts (V2–V5 only):** 4 variants × 36 intents × 3 languages = 432 new texts
**Total queries including primaries (V1–V5):** 5 × 36 × 3 = 540

**Naming scheme:**

| Field | Format | Example |
|---|---|---|
| `intent_id` | INT-NNN | INT-012 |
| `variant_id` | INT-NNN-VN | INT-012-V3 |
| `variant_type` | V1–V5 (see §4) | V3 |
| `language` | en / nl / tr | tr |

V1 entries in variant files are stubs that reference the primary rendering; they do not repeat the query_text.

---

## 4. Variant types

| Code | Name | Description |
|---|---|---|
| **V1** | Primary controlled | The existing primary rendering from `query-rendering-*.md`. No new text authored; variant file entry references the primary file. Establishes the controlled baseline for within-intent comparison. |
| **V2** | Concise natural | A short, direct phrasing — what a user might type when confident and in a hurry. Shorter than V1 but must preserve all required conditions. No telegraphic compression that drops conditions. |
| **V3** | Context-rich | A longer phrasing that adds situational context — user describes their setup, what they've already tried, or why they are asking. Still asks the same question; added context must not introduce new facts or conditions not in the intent spec. |
| **V4** | Indirect support-style | Phrased as a support interaction opener — describing a situation or problem rather than asking a direct question. Example: "I bought a NiceHome Hub last month and I'm wondering about the warranty." Tests whether the system correctly identifies the intent when it is expressed as context rather than a direct question. |
| **V5** | Alternate natural phrasing | A second natural phrasing that is neither concise (V2) nor context-rich (V3) — a genuinely different sentence structure or vocabulary choice. For troubleshooting intents, V5 may be problem-description style ("My Camera won't connect after a firmware update — what should I do?"). For simple factual intents, V5 is an alternate question form. |

---

## 5. Equivalence requirements

All five variants for a given intent must be equivalent on the following dimensions:

| Requirement | Rule |
|---|---|
| Same `intent_id` | All variants for INT-NNN carry `intent_id: INT-NNN` |
| Same linked fact IDs | All variants link to the same `linked_fact_ids` as the primary |
| Same conditions | All activating conditions in the intent spec are preserved in every variant; no condition may be added or dropped |
| Same difficulty level | A simple intent is simple in all variants; a conditional intent is conditional in all variants; no variant may change the cognitive demand of answering correctly |
| Same expected answer | The correct answer to every variant is the same set of facts; the expected_fact_set_id is unchanged |
| No answer hints | No variant may include phrasing that implies or reveals the answer (e.g., mentioning a specific number of years when asking about warranty length) |
| No new intent | A V3 context-rich variant that adds so much context that it effectively asks a different or more specific question than the primary is not a valid variant — it is a new intent and must be treated as such |

---

## 6. Language fairness rules

The same authoring discipline applied to the primary renderings applies to all variants:

- **Author from the intent specification, not from the English variant.** A V2 Turkish variant is written from what V2 (concise natural) means for that intent in Turkish — not by compressing or adapting the English V2 text.
- **Comparable variant types across languages.** V3 in Turkish and V3 in Dutch should both be context-rich in the sense defined in §4 — not one being a slight extension of V1 and the other being a paragraph of background.
- **No systematic English compression.** The English V2 must not be systematically shorter than the Turkish or Dutch V2 simply because English is more concise morphologically. If English V2 naturally compresses more, this may be a legitimate token-tax signal — but the authoring intent (concise natural) must be the same.
- **Turkish morphology is accepted as-is.** Agglutinative forms that are morphologically longer than English equivalents are not errors; they are the signal being measured.
- **Apostrophe suffix convention (TR) applies to all variants.** Hub'ım, Camera'mı, Plan'ımı, Sensor'u — consistent in all V1–V5 Turkish entries.
- **Controlled terminology applies to all variants.** Terms from `language-rendering-plan.md` §6 (e.g., TR: canlı görüntü, değişim, yenilenmiş değişim cihazı, para iadesi) must be used consistently across all variants in all languages.
- **Dutch native review required for public claims.** Dutch variants, like the primary Dutch rendering, require independent native review before any publication-grade claim about Dutch token-tax or Dutch model performance.

---

## 7. Measurement design

| Stage | Query set | Count | Notes |
|---|---|---|---|
| Stage 1a | Primary renderings only | 108 queries | Tokenize EN/NL/TR; compute per-intent token-tax ratios; establish baseline. No variants required. |
| Stage 1b | Full variant set (if created) | 540 queries | Optional extension of Stage 1a. Tokenize all V1–V5 variants; compute phrasing-sensitivity distributions per intent per language. Only if variants are created before Stage 1b is scheduled. |
| Stage 2+ | Primary renderings for smoke test | 108 queries (subset) | Stage 2 smoke test uses primary renderings only. Variants are not introduced until Stage 3 or later. |

**Reporting rule:** Primary and variant results are always reported separately. Variant token counts and execution results are never averaged into the same headline metric as primary counts without explicit labelling.

**Labelling rule:** Any result derived from V2–V5 variant queries carries the label "query-variant robustness analysis (V2–V5); not part of primary benchmark metric."

---

## 8. Future files

When variants are created, they will be stored in three new files in `docs/benchmark/v0.1/`:

| File | Language | Entries |
|---|---|---|
| `query-variants-en.md` | English | 36 intents × 5 variants = 180 entries (V1 stubs + 144 new texts) |
| `query-variants-nl.md` | Dutch | 180 entries |
| `query-variants-tr.md` | Turkish | 180 entries |

**Schema for each entry:**

```
## INT-NNN-VN

- intent_id: INT-NNN
- variant_id: INT-NNN-VN
- variant_type: V1 | V2 | V3 | V4 | V5
- language: en | nl | tr
- query_text: "..."   (empty for V1 stubs; "see query-rendering-*.md" pointer instead)
- linked_fact_ids: [F0NNN, ...]
- expected_fact_set_id: INT-NNN
- review_status: draft | owner_reviewed | native_reviewed | frozen
- notes: ...
```

V1 stub entries use:
```
- query_text: (primary — see query-rendering-[language].md INT-NNN)
```

---

## 9. Quality gates for variant creation

Before any variant file is frozen or used in a Stage 1b or Stage 2+ run, the following gates must pass:

| Gate | Requirement |
|---|---|
| **Count** | Exactly 5 variants per intent per language (V1–V5); exactly 36 intents per file; 180 entries per file |
| **ID consistency** | Same `intent_id` and `variant_id` naming across all three language files; INT-NNN-VN exists in EN, NL, and TR |
| **No condition changes** | No variant adds or removes a condition relative to the primary; verified by authoring review per entry |
| **No answer hints** | Automated grep + authoring review: no query_text reveals the answer |
| **No new intent** | No variant introduces a question that differs from the primary intent in what facts are required; if a candidate text activates different facts, it is a new intent candidate, not a variant |
| **Cross-language equivalence at variant-type level** | V2 in Turkish is concise natural in the same sense as V2 in Dutch and V2 in English; no systematic type-mismatch across languages |
| **Turkish owner review** | All Turkish variants reviewed by project owner (native Turkish speaker) before any tokenizer analysis using TR variants |
| **Dutch native review** | Required before any Stage 2+ public claims on Dutch variant data (same WAIVED_WITH_LIMITATION scope as primary Dutch rendering) |
| **Controlled terminology** | All controlled terms from `language-rendering-plan.md` §6 applied consistently across V1–V5 in each language |
| **Apostrophe suffix convention (TR)** | Applied in all TR variant texts |

---

## 10. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| **Variant explosion** | Medium | 432 new query texts (V2–V5 × 36 × 3) is a significant authoring and review burden. Each text requires the same authoring discipline as the primary. Do not underestimate the review cost. |
| **Uncontrolled specificity drift** | Medium | V3 (context-rich) and V4 (indirect support-style) variants are more vulnerable to accidentally introducing extra conditions or shifting the difficulty level. Per-entry review against the intent spec is essential. |
| **Phrasing choices inflate token counts** | Low-Medium | V2 variants may produce lower token counts and V3 variants higher token counts than V1, partly because of phrasing choice, not language properties. This is expected and is itself a measurement result — but it must be reported as within-language phrasing sensitivity, not as cross-language token-tax. |
| **Headline metric complexity** | Medium | Five variants per intent makes summary statistics more complex. Median vs. mean vs. min/max across variants adds analysis choices. The §7 reporting rule (always report primary and variant results separately) mitigates this, but the metrics story becomes harder to tell. |
| **540 queries may exceed v0.1 scope** | High | The primary goal of v0.1 is to establish baseline token-tax ratios with the 108-query set and run a smoke test. Adding 432 variant queries before Stage 1a is complete is premature. If the Stage 1a results are anomalous or the model choice changes, all variants must be reconsidered. |

---

## 11. Recommendation

**Keep the 108-query primary set as the exclusive Stage 1a input.**

Do not create variant texts before Stage 1a is complete. The reasons:

1. **TM1 must be confirmed first.** If the tokenizer or model family changes after variant creation, all token counts must be recomputed. Avoid committing authoring effort before the tokenizer is confirmed.
2. **Stage 1a may surface anomalies.** If Stage 1a shows unexpected token-tax ratios or structural problems in the KB renderings, the intent set or fact set may need revision. Variants built on a not-yet-validated primary set carry that uncertainty forward.
3. **Review burden is real.** 432 texts × full per-entry equivalence review is a substantial commitment. Deferring until Stage 1a provides a validated foundation reduces rework risk.
4. **Variants are optional for v0.1's core hypothesis.** The token-tax baseline (§7, Stage 1a) and the execution-tax smoke test (Stage 2) can both be completed with the 108-query primary set. Variants add robustness, not the core result.

**When to create variants:**

- After TM1 is confirmed and Stage 1a tokenizer sanity gate passes
- After the Stage 1a go/no-go criteria are met (see `validation-plan-v0.1.md` §7)
- Before Stage 1b is scheduled, if Stage 1b is included in the v0.1 scope decision

**If variants are created before Stage 1a completes:** freeze them (no further edits) and report them as a separate analysis pass with the labelling rule from §7. Do not merge them into the Stage 1a primary dataset.

---

*This file defines the variant design. No variant texts exist yet. The primary 108-query set remains the sole Stage 1a input. Version: qv-plan-v0.1.0.*
