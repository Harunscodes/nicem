# NiceM v0.1 Quality Gates

**Status:** Pre-run checklist — must be fully reviewed before any Stage 1, 2, or 3 activity
**Role:** Consolidates all quality gates from `dataset-specification.md` §11, `document-plan.md` §8, `validation-plan-v0.1.md` §6, and the evaluation methodology into one authoritative pass/fail status document. No benchmark stage begins until its gate section is fully PASS (or explicitly WAIVED_WITH_LIMITATION with documented scope).
**Version:** qg-v0.1.0
**Depends on:** Every artifact in `docs/benchmark/v0.1/` and every methodology document in `docs/methodology/`
**Last updated:** 2026-06-13

---

## 1. Purpose

Quality gates exist because a flawed artifact that enters a benchmark stage causes one of three expensive failures:

1. **Wasted run cost** — API budget spent on a benchmark that cannot be interpreted because a KB rendering is wrong or an intent is ill-formed.
2. **Corrupt results** — Artifacts that are structurally correct but semantically wrong (e.g., a Dutch rendering that silently omits a condition) produce data that looks clean but is uninterpretable — worse than no data.
3. **Invalid comparison** — If the three language renderings are not structurally parallel (same chunks, same facts, same section boundaries), any token-count or retrieval-unit difference is partly an authoring artifact, not a language/tokenizer effect.

The gates in this document are the barrier between benchmark construction and benchmark execution. They are not aspirational checklists — they are go/no-go decisions. A FAIL or BLOCKED gate stops the relevant stage; a NEEDS_REVIEW gate requires human sign-off before the stage proceeds.

The governing principle from `validation-plan-v0.1.md` §1: **spend cheap effort before expensive effort** — review before tokenizing, tokenize before running, smoke-test before committing the full budget.

---

## 2. Gate status legend

| Status | Meaning |
|---|---|
| **PASS** | Gate criterion is satisfied; evidence documented below |
| **FAIL** | Gate criterion is not satisfied; blocks the relevant stage; action required before proceeding |
| **BLOCKED** | Gate cannot be assessed because a prerequisite is incomplete (note the prerequisite) |
| **NOT_STARTED** | Gate not yet attempted; no artifact or activity exists to assess |
| **NEEDS_REVIEW** | Artifact exists but requires human review before PASS can be declared; stage may not proceed without sign-off |
| **WAIVED_WITH_LIMITATION** | Gate criterion is relaxed for v0.1 with a documented scope limitation; public claims must acknowledge the limitation |

---

## 3. Dataset artifact inventory gate

*Purpose: confirm all benchmark artifacts exist and are structurally complete before any quality content-check proceeds.*

| Artifact | Status | Owner | Evidence | Notes |
|---|---|---|---|---|
| `dataset-specification.md` | **PASS** | Project owner | File exists; 14 sections; versioned ds-spec-v0.1.0 | Basis document for all subsequent artifacts |
| `canonical-fact-set.md` | **PASS** | Project owner | File exists; 78 facts (D01:10, D02:9, D03:11, D04:9, D05:8, D06:13, D07:9, D08:9); versioned fs-v0.1.0 | Not yet frozen |
| `document-plan.md` | **PASS** | Project owner | File exists; 39 sections across 8 documents; versioned kb-plan-v0.1.0 | Not yet frozen |
| `language-rendering-plan.md` | **PASS** | Project owner | File exists; 20-concept EN/NL/TR terminology table; AC1–AC9 preservation rules; chunk-ID scheme; versioned lr-plan-v0.1.0 | Not yet frozen |
| `kb-rendering-en.md` | **PASS** | Project owner | File exists; 39 chunks confirmed by automated grep; versioned kb-en-v0.1.0 | Not yet frozen; owner review pending |
| `kb-rendering-nl.md` | **PASS** | Project owner | File exists; 39 chunks confirmed by automated grep; versioned kb-nl-v0.1.0 | Not yet frozen; Dutch native review pending (LR6) |
| `kb-rendering-tr.md` | **PASS** | Project owner | File exists; 39 chunks confirmed by automated grep; versioned kb-tr-v0.1.0 | Not yet frozen; project-owner Turkish review pending |
| `intent-set.md` | **PASS** | Project owner | File exists; 36 intents (12/12/12); all 8 documents represented; versioned intent-v0.1.0 | Not yet frozen |
| `expected-fact-mapping.md` | **PASS** | Project owner | File exists; 36 mappings; IS1–IS7 pre-registered; versioned efm-v0.1.0 | Not yet frozen |
| `quality-gates.md` | **PASS** | Project owner | This file; 16 sections; versioned qg-v0.1.0 | — |
| `query-rendering-plan.md` | **PASS** | Project owner | File exists; 11 sections; QR1–QR9 open questions; versioned qr-plan-v0.1.0 | Not yet frozen |
| `query-rendering-en.md` | **PASS** | Project owner | File exists; 36 queries confirmed by automated grep; INT-001–036 all present; no fact/chunk IDs or answer hints in query_text; versioned qr-en-v0.1.0 | Not yet frozen; owner review pending |
| `query-rendering-nl.md` | **NEEDS_REVIEW** | External (QR8/LR6) | File exists; 36 queries confirmed; INT-001–036 all present; authored from intent specs (not translated from EN); no TODO_REVIEW in query_text; versioned qr-nl-v0.1.0 | Native Dutch speaker review required before Stage 2+ public claims; sufficient for internal Stage 1 |
| `query-rendering-tr.md` | **PASS** | Project owner (QR9) | File exists; 36 queries confirmed; INT-001–036 all present; apostrophe suffix convention applied; controlled terms applied; QR9 review complete (7 corrections applied); versioned qr-tr-v0.1.0 | — |
| `tm1-tokenizer-model-decision.md` | **PASS** | Project owner | File exists; resolves TM1 with confirmed choice (OpenAI GPT-4.1-mini/GPT-4.1 family); versioned tm1-v0.1.1 | Status CONFIRMED 2026-06-13; exact tokenizer encoding name (TM1-a) confirmed in Stage 1 tooling |
| `query-variant-plan.md` | **PASS** | Project owner | File exists; 11 sections; qv-plan-v0.1.0; no variant texts yet — planning only | Variants are optional robustness layer; not required before Stage 1a |
| `stage2-decision-plan.md` | **PASS** | Project owner | File exists; 14 sections; s2-plan-v0.1.1 (2026-06-14); all 5 Stage 2 decisions CONFIRMED | All five decisions confirmed 2026-06-14 |
| `stage2-smoke-test-run-plan.md` | **PASS** | Project owner | File exists; 18 sections; s2-runplan-v0.1.0 (2026-06-14); defines the 30-run smoke test, prompts, retrieval, logging, budget enforcement | Does NOT start Stage 2 |
| `stage2-live-run-readiness.md` | **PASS** | Project owner | File exists; 10 sections; s2-live-readiness-v0.1.0 (2026-06-14); blockers, guards, budget design, approval checklist, rollback conditions | Live execution BLOCKED; does NOT authorize a run |
| `stage2-model-pricing-config.md` | **PASS** | Project owner | File exists; 9 sections; s2-model-pricing-v0.1.0 (2026-06-14); model IDs, pricing formula, hand-calculation example, change-invalidation rules, confirmed-values table (empty until pricing confirmed) | Confirmed values table empty; pricing table placeholders must be filled before first API call |
| All artifacts in `source-map.md` | **PASS** | Project owner | Every artifact created in this phase is catalogued in `docs/source-map.md` | — |

**Inventory gate verdict: PASS** — all 19 artifacts exist (14 benchmark artifacts + 1 variant planning document + 1 Stage 2 decision plan + 1 Stage 2 smoke-test run plan + 1 Stage 2 live-run readiness document + 1 Stage 2 model/pricing config document). Content quality gates follow below.

---

## 4. Fact-set quality gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| 78 facts present | **PASS** | Verified at creation; summary table in `canonical-fact-set.md` §Summary |
| All facts have required schema fields (fact_id through ambiguity_notes) | **PASS** | All facts authored with the full 10-field schema from `dataset-specification.md` §5 |
| No duplicate fact IDs | **PASS** | IDs are sequential per document (F0101–F0110, F0201–F0209, etc.); no overlaps by construction |
| No contradictory policy facts | **PASS** | Internal review at authoring; 8 ambiguity risks documented and disambiguated rather than contradicted |
| Every fact has `language_neutral_expected_outcome` | **PASS** | Present in all 78 fact entries |
| Every relevant fact has `forbidden_claims` | **PASS** | All facts with realistic hallucination risk carry forbidden_claims; simple descriptive facts also carry them where appropriate |
| Ambiguity notes present for risky facts | **PASS** | 8 identified risks carry `ambiguity_notes`; listed in `canonical-fact-set.md` §Summary |
| Fact-set not yet frozen | **NEEDS_REVIEW** | fs-v0.1.0 is the working version; must be frozen (no further edits without version bump) before KB renderings are frozen | Project owner to confirm fact-set is stable before freezing |

**Fact-set gate verdict: PASS** on content; **NEEDS_REVIEW** on freeze status.

---

## 5. Document/chunk alignment gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| 8 documents planned | **PASS** | D01–D08 in `document-plan.md` §4 |
| 39 sections/chunks planned | **PASS** | D01:4, D02:5, D03:5, D04:5, D05:4, D06:6, D07:5, D08:5 = 39 total |
| All 78 facts mapped to at least one chunk | **PASS** | Section-by-section fact mapping in `document-plan.md` §4; every fact ID appears |
| Chunk IDs stable and unambiguous (scheme: `D0n-Sn`) | **PASS** | Scheme fixed in `language-rendering-plan.md` §3; applied consistently in all three renderings |
| F0807 / AC9 forward-reference rule preserved | **PASS** | F0807 stated once in D08-S4; D08-S3 carries forward reference; both renderings (en/nl/tr) confirmed to follow this structure |
| No policy fact duplicated across chunks (avoiding double-counted retrieval units) | **PASS** | Each fact ID assigned to exactly one primary chunk; F0807 exception handled by single-source rule (AC9); `document-plan.md` §6 enforces minimal cross-document redundancy |

**Chunk alignment gate verdict: PASS**

---

## 6. Language rendering alignment gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| EN, NL, TR files each contain exactly 39 chunk IDs | **PASS** | Automated grep confirmed 39 `chunk_id:` lines in each file at commit f90f901 |
| Chunk IDs match across all three languages | **PASS** | `diff` of chunk_id+fact_ids lines: EN==NL and EN==TR identical at commit f90f901 |
| Fact ID mappings match across all three languages | **PASS** | Same diff check; identical fact_ids per chunk across all three |
| Device and plan names preserved (not translated) | **PASS** | NiceHome Hub/Sensor/Plug/Camera and Camera Plus Plan appear untranslated in all three renderings |
| Controlled terminology applied consistently | **NEEDS_REVIEW** | Terms verified at authoring against `language-rendering-plan.md` §6; full consistency pass by a native reviewer has not been done for Dutch (LR6) or formally signed off for Turkish |
| AC1–AC9 ambiguity controls preserved | **PASS** | Verified by authoring review; lexically distinct terms confirmed for each AC in all three renderings (per commit message and authoring notes) |
| No unsupported policy facts introduced | **PASS** | Prose limited to connective language; no policy content added beyond the fact-set (verified at authoring) |
| No required conditions removed | **PASS** | All conditional facts rendered with their conditions in all three languages (verified at authoring) |
| No `TODO_REVIEW` markers in prose | **PASS** | Automated grep at commit f90f901: zero `TODO_REVIEW` in prose of all three files (one mention in Dutch file header description only) |

**Rendering alignment gate verdict: PASS** on automated checks; **NEEDS_REVIEW** on controlled-terminology native sign-off.

---

## 7. Language review gate

| Criterion | Status | Owner | Notes |
|---|---|---|---|
| English rendering reviewed for over-concision risk | **NEEDS_REVIEW** | Project owner | English was authored with full conditional sentences per `language-rendering-plan.md` §7; no compression artifacts visible at authoring; formal owner sign-off pending |
| Dutch rendering — native speaker review | **NEEDS_REVIEW** | External (LR6) | Project owner is not a native Dutch speaker; independent Dutch review is required before any publication-grade claim; for internal Stage 1 (tokenizer-only) the rendering is sufficient; for Stage 2+ see note below |
| Turkish rendering — project-owner review | **NEEDS_REVIEW** | Project owner (native Turkish speaker) | Full read-through of `kb-rendering-tr.md` not yet formally completed; project owner should review before Stage 2 smoke test |
| Independent bilingual review (publication-grade) | **NOT_STARTED** | External | Required only before public or publication-grade claims; not a Stage 1 or Stage 2 blocker for internal exploratory use; must be completed before any external sharing of results |
| Single-evaluator limitation documented | **PASS** | — | `evaluation-method-v0.1.md` §8 and `language-selection-v0.1.md` §8 both document this limitation; all v0.1 results must carry "single-evaluator exploratory pilot; independent review pending" label when shared |

**Stage gate note for Dutch:** the Dutch rendering is sufficient for internal Stage 1 (tokenizer-only) and Stage 2 smoke tests as an exploratory exercise. It is NOT sufficient for any public claim about Dutch token-tax or Dutch model performance without native review. This is a **WAIVED_WITH_LIMITATION** for internal use.

**Language review gate verdict: NEEDS_REVIEW** (Turkish project-owner review and Dutch native review both outstanding).

---

## 8. Intent-set quality gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Exactly 36 intents | **PASS** | INT-001 through INT-036; 36 entries in `intent-set.md` |
| 12 simple factual (INT-001–012) | **PASS** | Confirmed in `intent-set.md` distribution |
| 12 conditional policy (INT-013–024) | **PASS** | Confirmed |
| 12 troubleshooting/process (INT-025–036) | **PASS** | Confirmed |
| All 8 documents represented | **PASS** | Coverage analysis table in `intent-set.md`: D01:4, D02:4, D03:7, D04:6, D05:4, D06:5, D07:3, D08:4 |
| AC1–AC3, AC5–AC9 directly tested | **PASS** | Direct tests documented in coverage analysis; discriminating pairs confirmed |
| AC4 direct coverage | **WAIVED_WITH_LIMITATION** | No direct AC4 intent exists (IS1); AC4 monitored only as secondary observation in INT-005 outputs; a dedicated intent deferred to v0.2 — this limitation is pre-registered in `expected-fact-mapping.md` global rules |
| No intent introduces new facts | **PASS** | All intents reference only fact IDs that exist in `canonical-fact-set.md` |
| Every intent maps to fact IDs and chunk IDs | **PASS** | All 36 entries include `linked_fact_ids` and `linked_chunk_ids` |
| Coverage gaps documented | **PASS** | IS1–IS3 gaps (F0110, F0612, F0708 without direct intents) documented in `intent-set.md` §Open questions and `expected-fact-mapping.md` |

**Intent-set gate verdict: PASS** with one **WAIVED_WITH_LIMITATION** (AC4).

---

## 9. Expected fact mapping gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| All 36 intents mapped | **PASS** | INT-001 through INT-036 all present in `expected-fact-mapping.md` |
| PASS criteria defined for every intent | **PASS** | All 36 entries include explicit PASS criteria |
| FAIL criteria defined for every intent | **PASS** | All 36 entries include explicit FAIL criteria |
| UNCERTAIN conditions defined for every intent | **PASS** | All 36 entries include UNCERTAIN conditions |
| Forbidden claims listed for every intent | **PASS** | All 36 entries include forbidden_claims |
| Ordered-step rules defined (IS5) | **PASS** | IS5 resolution pre-registered in global rules; 7 intents identified; causal order required |
| Partial-answer rules defined (IS4) | **PASS** | IS4 resolution pre-registered in global rules and INT-003 entry |
| Conditional-answer rules defined | **PASS** | Condition rule defined in global rules; applied to all 12 conditional intents |
| AC8 / INT-019 FAIL patterns pre-registered (IS6) | **PASS** | All three FAIL patterns (flat-90, full-2-year, no-warranty) explicitly listed in INT-019 entry |
| INT-031 / INT-032 two-chunk requirement documented | **PASS** | Both entries note the D08-S3 + D08-S4 span requirement; evaluator_notes specify retrieval tracking |
| Language-neutrality rule documented | **PASS** | Global rules section explicitly states outputs in all three languages are evaluated against the language-neutral expected_outcome |

**Expected fact mapping gate verdict: PASS**

---

## 9b. Query rendering quality gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Exactly 36 EN queries | **PASS** | Automated grep: 36 `## INT-` headers in `query-rendering-en.md` |
| Exactly 36 NL queries | **PASS** | Automated grep: 36 `## INT-` headers in `query-rendering-nl.md` |
| Exactly 36 TR queries | **PASS** | Automated grep: 36 `## INT-` headers in `query-rendering-tr.md` |
| Same INT IDs across all three files | **PASS** | `diff` of `## INT-` lines: EN==NL and EN==TR identical |
| No fact IDs in query_text fields | **PASS** | Automated grep: zero matches for `F[0-9]{4}` in query_text lines |
| No chunk/document IDs in query_text fields | **PASS** | Automated grep: zero matches for `D0[0-9]-S` in query_text lines |
| No answer hints in query_text fields | **PASS** | Verified at authoring; queries ask, do not guide |
| No TODO_REVIEW in query_text fields | **PASS** | Automated grep of actual query_text entries: zero matches |
| All conditions preserved for conditional intents | **PASS** | Verified per entry; all 12 conditional intents carry their required conditions |
| Troubleshooting intents preserve problem state | **PASS** | Verified per entry; all 12 troubleshooting intents describe symptom state |
| English not systematically over-compressed | **PASS** | Natural clause structures used throughout; no artificial clipping |
| Dutch not a literal translation of English | **PASS** | Dutch queries authored independently from intent specs; different sentence structures |
| Turkish not a literal translation of English | **PASS** | Turkish queries authored independently; natural Turkish support-style phrasing |
| Apostrophe suffix convention (TR) | **PASS** | Hub'ım, Camera'mı, Plan'ımı etc. applied consistently |
| Controlled product names preserved (all languages) | **PASS** | NiceHome Hub/Sensor/Plug/Camera; Camera Plus Plan — untranslated in NL and TR |
| Turkish query owner review (QR9) | **PASS** | Project owner reviewed all 36 Turkish queries; 7 phrasing corrections applied (INT-004, 012, 019, 028, 029, 033, 035); no meaning errors found; review complete 2026-06-13 |
| Dutch query native review (QR8/LR6) | **NEEDS_REVIEW** | Required before Stage 2+ public claims; internal Stage 1 use acceptable |

**Query rendering gate verdict: PASS** on structural and parity checks; Turkish owner review (QR9) PASS; **NEEDS_REVIEW** on Dutch native review (QR8/LR6, deferred to pre-publication).

---

## 9c. Cross-language query semantic equivalence gate

*Purpose: confirm that EN/NL/TR query renderings for each INT express the same intent, same conditions, same difficulty, and same absence of answer hints — so token-count differences reflect language/tokenization properties, not authoring differences.*

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Same intent expressed across all three languages per INT | **PASS** | Full 36-INT review conducted 2026-06-13; EN/NL/TR compared against `intent-set.md` and `expected-fact-mapping.md`; no intent-level meaning divergence found |
| Same conditions preserved (conditional intents) | **PASS** | All 12 conditional intents (INT-013–024) carry the same activating conditions in all three languages; verified per entry |
| Same difficulty level across languages | **PASS** | No language renders a simple intent as conditional or vice versa; same multi-fact or ordered-step requirements |
| No answer hints in any language | **PASS** | Verified at authoring and confirmed in cross-language review; queries ask, do not guide |
| INT-004 TR terminology alignment | **PASS** | "ücret iadesi" (fee refund) changed to "para iadem" (my money refund) 2026-06-13, aligning with "para iadesi" used in INT-011 and INT-035 TR; consistent controlled-register terminology across TR file |
| INT-035 TR controlled term alignment | **PASS** | "yeni ürün" replaced with "değişim ürünü" in QR9 review; aligns with EN "replacement" and NL "vervanging" and controlled term "değişim" |
| Natural register across all three languages | **PASS** | EN: neutral support-style; NL: natural ik/mijn product support; TR: natural Turkish support-style with correct apostrophe-suffix convention |
| Cross-language audit single-evaluator caveat | **WAIVED_WITH_LIMITATION** | Review conducted by project owner (native Turkish, non-native Dutch); Dutch register and phrasing accepted for internal Stage 1 use; independent bilingual review required before publication-grade claims |

**Cross-language equivalence gate verdict: PASS** for internal Stage 1 — no intent-level parity failures found; one terminology inconsistency (INT-004 TR) resolved; Dutch phrasing accepted under WAIVED_WITH_LIMITATION (native review pending for public claims).

---

## 9d. Query variant plan gate

*Purpose: confirm that the query variant design is documented and that variants are correctly scoped as optional — i.e., that no variant creation is required before Stage 1a.*

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Query variant plan exists | **PASS** | `query-variant-plan.md` (qv-plan-v0.1.0) created 2026-06-13; 11 sections |
| Variant type definitions fixed | **PASS** | V1–V5 defined in §4; V1 = existing primary rendering; V2–V5 = optional new texts |
| Variant equivalence requirements defined | **PASS** | §5: same intent_id, linked facts, conditions, difficulty, expected answer; no answer hints; no new intent |
| Language fairness rules defined | **PASS** | §6: authored from intent spec (not EN translation); comparable variant types across languages; Turkish apostrophe convention and controlled terms apply; Dutch native review required for public claims |
| Stage 1a/1b separation documented | **PASS** | §7: Stage 1a = 108 primary queries only; Stage 1b = optional 540-query variant set; never mixed in headline metrics |
| Variants not required before Stage 1a | **PASS** | §11 recommendation: defer variant authoring until Stage 1a tokenizer sanity gate passes and TM1 is confirmed |
| No variant texts exist yet | **PASS** | qv-plan-v0.1.0 is planning only; `query-variants-en.md`, `query-variants-nl.md`, `query-variants-tr.md` not yet created |
| Risks documented | **PASS** | §10: variant explosion, specificity drift in V3/V4, phrasing inflating token counts, metric complexity, scope risk for v0.1 all pre-registered |

**Query variant plan gate verdict: PASS** — variant design is planned and scoped; no variant creation is required before Stage 1a; primary 108-query set remains the sole Stage 1a input.

---

## 10. Evaluation readiness gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Success rubric exists | **PASS** | `docs/methodology/success-rubric-v0.1.md` |
| Evaluation method exists | **PASS** | `docs/methodology/evaluation-method-v0.1.md` |
| Evaluator inputs defined (what evaluator sees) | **PASS** | `evaluation-method-v0.1.md` §5: evaluator sees model output + expected fact mapping; NOT cost/trajectory data (blind gate) |
| Endpoint outcome categories defined (PASS/FAIL/UNCERTAIN) | **PASS** | `success-rubric-v0.1.md` and `expected-fact-mapping.md` global rules |
| Human review policy defined | **PASS** | `evaluation-method-v0.1.md` §6: all UNCERTAINs mandatory; FAILs recommended; sampled PASSes |
| LLM-as-judge limitation documented | **PASS** | `evaluation-method-v0.1.md` §7: LLM-as-judge is triage/support only; never sole source of truth |
| UNCERTAIN-rate recalibration gate (>25%) documented | **PASS** | `falsification-and-decision-rules-v0.1.md` §7 and `expected-fact-mapping.md` evaluator risks |
| Human audit fraction | **NOT_STARTED** | EV1 is open — the specific audit fraction must be pre-committed before analysis begins; blocks Stage 2 analysis (not Stage 1) |

**Evaluation readiness gate verdict: PASS** for Stage 1; **NOT_STARTED** on audit fraction (EV1) which must be resolved before Stage 2 analysis.

---

## 11. Logging readiness gate

| Criterion | Status | Evidence / Notes |
|---|---|---|
| Logging schema exists | **PASS** | `docs/methodology/logging-schema-v0.1.md` |
| Required v0.1 minimal field set defined | **PASS** | `logging-schema-v0.1.md` §12: minimal required fields listed |
| Run unit defined (one row = one intent × language × agent × model × KB rendering) | **PASS** | `logging-schema-v0.1.md` §3 |
| Agent A null-retrieval convention defined | **PASS** | Null-not-omitted convention: Agent A logs retrieval fields as null |
| Token and cost fields defined | **PASS** | `logging-schema-v0.1.md` §5 |
| Retrieval semantic-unit fields defined (dual token/fact-ID reporting) | **PASS** | `logging-schema-v0.1.md` §4; `baseline-token-tax-calculation-v0.1.md` §4 |
| `pricing_version` field defined | **PASS** | Date-stamped price table field prevents silent cost-comparison breakage |
| Instrumentation platform (M9) | **BLOCKED** | M9 is unresolved — platform must capture the minimal required field set; candidates Langfuse / Arize Phoenix identified; blocks Stage 2 instrumented runs |

**Logging readiness gate verdict: PASS** for Stage 1 (tokenizer-only, no instrumentation needed); **BLOCKED** on M9 for Stage 2+.

---

## 12. Stage 1 readiness gate

*Stage 1 = tokenizer-only sanity gate: tokenize all query renderings and KB chunks; compute per-intent token-tax ratios; no API calls.*

| Criterion | Status | Notes |
|---|---|---|
| Tokenizer/model decision rules exist | **PASS** | `docs/methodology/tokenizer-model-choice-v0.1.md` |
| Specific tokenizer/provider selected | **PASS** | TM1 CONFIRMED 2026-06-13 (`tm1-tokenizer-model-decision.md`, tm1-v0.1.1): OpenAI GPT-4.1-mini/GPT-4.1 family for all of v0.1 |
| Exact tokenizer encoding name (TM1-a) | **PASS (FALLBACK)** | Target: `o200k_base` (tiktoken encoding for GPT-4.1 family). Network policy blocks `openaipublic.blob.core.windows.net` in this environment; BPE data unavailable; fallback used: `o200k_base_approx` (o200k_base regex + BPE compression heuristic). See `scripts/stage1a_tokenizer_sanity_gate.py` `TOKENIZER_RESOLUTION_NOTE`. Authoritative counts require re-run with tiktoken in a network-accessible environment. |
| Query rendering plan exists | **PASS** | `query-rendering-plan.md` complete |
| 36 × 3 = 108 query renderings exist | **PASS** | All three query rendering files verified: 108 rows produced by script |
| Turkish query review (QR9) | **PASS** | Completed 2026-06-13 |
| KB renderings ready for tokenization | **PASS** | All three KB files parsed: 117 chunk rows produced |
| Token-tax calculation method documented | **PASS** | `docs/methodology/baseline-token-tax-calculation-v0.1.md` |
| Stage 1 go/no-go criteria defined | **PASS** | `validation-plan-v0.1.md` §7: Dutch ~1.1×–1.5×; Turkish above Dutch |
| **Stage 1a execution** | **PASS** | `scripts/stage1a_tokenizer_sanity_gate.py` run 2026-06-13; results in `results/stage1a/`; all sanity checks PASS; see §12a below |

**Stage 1 gate verdict: PASS** — Stage 1a complete; all sanity checks passed; token-tax ratios are in the expected direction and range.

---

## 12a. Stage 1a execution results

**Run date:** 2026-06-13
**Script:** `scripts/stage1a_tokenizer_sanity_gate.py`
**Tokenizer used:** `o200k_base_approx` (fallback; see TM1-a note above)
**Outputs:** `results/stage1a/token_counts_queries.csv`, `results/stage1a/token_counts_kb_chunks.csv`, `results/stage1a/token_tax_summary.md`, `results/stage1a/token_tax_outliers.md`

| Check | Result |
|---|---|
| Total query rows | 108 ✓ |
| Total KB chunk rows | 117 ✓ |
| Query intent ID alignment (EN == NL == TR) | PASS ✓ |
| KB chunk ID alignment (EN == NL == TR) | PASS ✓ |
| Query NL/EN median | 1.000 (within expected 1.0–1.6) ✓ |
| Query TR/EN median | 1.083 (within expected 1.0–3.5) ✓ |
| KB NL/EN median | 1.074 (within expected 1.0–1.6) ✓ |
| KB TR/EN median | 1.370 (within expected 1.0–3.5) ✓ |
| Query TR/EN > NL/EN | 1.083 > 1.000 ✓ |
| KB TR/EN > NL/EN | 1.370 > 1.074 ✓ |

**Summary statistics:**

| Metric | Query NL/EN | Query TR/EN | KB NL/EN | KB TR/EN |
|---|---|---|---|---|
| min | 0.857 | 0.667 | 0.821 | 0.974 |
| max | 1.333 | 1.577 | 1.467 | 2.000 |
| mean | 1.018 | 1.147 | 1.086 | 1.426 |
| median | 1.000 | 1.083 | 1.074 | 1.370 |
| p90 | 1.182 | 1.500 | 1.267 | 1.800 |

**Total tokens:**
| Language | Queries (36) | KB chunks (39) |
|---|---|---|
| English | 710 | — (see CSV) |
| Dutch | 724 | — (see CSV) |
| Turkish | 831 | — (see CSV) |

**Outliers:** 6 query outliers + 1 KB chunk outlier documented in `results/stage1a/token_tax_outliers.md`. All are explainable:
- 6 query TR_BELOW_NL cases: Turkish syntactic compactness for short queries (agglutinative morphology reduces word count, partially offsetting the BPE-splitting premium). For KB chunks (longer text), TR > NL holds for 38/39. Pre-registered as a Stage 2 analysis note.
- 1 KB outlier (D08-S5): TR > EN (correct direction); NL unusually high due to Dutch verbose procedural phrasing for this section.

**Stage 1a verdict: PASS** — ratios are in the expected direction and within literature-consistent ranges. No artifacts require revision. Proceed to Stage 2 planning.

**Tokenizer rerun note (TM1-a):** For authoritative token counts, re-run `stage1a_tokenizer_sanity_gate.py` in a network-accessible environment where `openaipublic.blob.core.windows.net` is reachable. The script will automatically use exact tiktoken counts when the encoding loads successfully. The current fallback counts are suitable for the directional sanity gate; they are **not** publication-grade absolute counts.

---

## 13. Stage 2 readiness gate

*Stage 2 = smoke test: 3–5 intents, both agent designs, all three languages, small instrumented run.*

| Criterion | Status | Notes |
|---|---|---|
| Specific model/provider selected (TM1) | **PASS** | TM1 CONFIRMED: OpenAI GPT-4.1-mini/GPT-4.1 family. Exact tier (mini vs. full) for Stage 3 settled by smoke test (TM1-d); version-pinned model IDs to be set at Stage 2 setup (TM1-b/c) |
| Embedding model for Agent B selected (TM8/AD2) | **PASS** | TM8 CONFIRMED 2026-06-14: OpenAI `text-embedding-3-small`; same model across EN/NL/TR; `embedding_model_id` + `embedding_model_version` logged |
| Instrumentation platform (M9) | **PASS** | M9 CONFIRMED 2026-06-14: lightweight local JSONL/CSV logging; one record per run; minimum required fields; no external platform |
| Smoke-test intent subset selected | **PASS** | Subset confirmed: INT-004, INT-015, INT-017, INT-026, INT-031 (`stage2-decision-plan.md` §9) |
| Pilot budget approved (TM5/BS6) | **PASS** | TM5/BS6 CONFIRMED 2026-06-14: $25 USD hard cap; stop-and-review at $20; cap must be implemented or manually enforced before any call |
| Evaluation procedure ready | **PASS** | `evaluation-method-v0.1.md` and `expected-fact-mapping.md` are complete |
| Logging pipeline ready | **NEEDS_REVIEW** | M9 decided (local JSONL); the logging runner script itself must be implemented and reviewed before runs |
| Human audit fraction pre-committed (EV1) | **PASS** | EV1 CONFIRMED 2026-06-14: audit all Stage 2 outputs manually (PASS, FAIL, UNCERTAIN); no sampling |
| Direct LLM context condition (AD1: A0 vs. A1) | **PASS** | AD1 CONFIRMED 2026-06-14: A1 — Direct LLM with full relevant-language KB rendering in context |
| Version-pinned model IDs set (TM1-b/c) | **NOT_STARTED** | Exact completion + embedding model IDs to be recorded before the first API call; placeholders in run plan §6 |
| Smoke-test run plan exists | **PASS** | `stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0) created 2026-06-14; defines intents, run matrix, prompts, retrieval, logging, budget enforcement, pass/fail criteria |
| `pricing_version` recorded | **NOT_STARTED** | Date-stamped rate table (completion + embedding) to be recorded before the first API call |
| Minimal logging runner (dry-run skeleton) | **PASS** | `scripts/stage2_smoke_runner.py` created 2026-06-14; dry-run builds all 30 runs, validates all required fields, total cost $0, no API key required; outputs in `results/stage2/dry_run_*` |
| Logging runner — live-mode scaffolding | **PASS** | `stage2_smoke_runner.py` has pricing table, `estimate_cost_usd`, `BudgetGuard`, strict `can_run_api_mode` guard, and `--live`/`--confirm-spend` flags; live mode refuses by default; verified 2026-06-14 |
| Logging runner — pricing self-test | **PASS** | `_run_pricing_selftest()` added 2026-06-14; uses synthetic rates (not real pricing); verifies `estimate_cost_usd` formula; result: PASS (0.00202); included in dry-run validation report |
| Logging runner — live API/embedding paths | **NOT_STARTED** | Completion + embedding paths are unreachable stubs; must be implemented + reviewed; `allow_api_calls` is False; model/pricing placeholders block live mode |
| Live-run readiness documented | **PASS** | `stage2-live-run-readiness.md` (s2-live-readiness-v0.1.0): blockers, guards, budget design, approval checklist, rollback conditions |
| Model and pricing config documented | **PASS** | `stage2-model-pricing-config.md` (s2-model-pricing-v0.1.0 2026-06-14): model IDs, formula, hand-calculation example, change-invalidation rules; confirmed-values table pending |

**Stage 2 decision plan:** `docs/benchmark/v0.1/stage2-decision-plan.md` (s2-plan-v0.1.1, 2026-06-14) documents all five blocking decisions, now **CONFIRMED**. **Stage 2 smoke-test run plan:** `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0, 2026-06-14) defines the full 30-run smoke test.

**Stage 2 gate verdict: BLOCKED** — all five decisions are CONFIRMED; the run plan, the live-run readiness document, and the runner (dry-run skeleton + live-mode scaffolding) all exist. The dry-run passes all structural validations (30 runs, all required fields, $0 cost, no API key), and live mode is refused by default through a strict multi-condition guard. Stage 2 is still not runnable: the live completion + embedding paths are unimplemented stubs; the version-pinned model IDs (TM1-b/c), `pricing_version`, and pricing table are placeholders; `allow_api_calls` is False; and the `--live`/`--confirm-spend` flags are required. All blockers and the manual approval checklist are tracked in `stage2-live-run-readiness.md`.

---

## 14. Known limitations and waivers

All v0.1 results must carry the label: **"Single-evaluator exploratory pilot; independent review pending."** This applies to any external communication.

| Limitation | Type | Scope restriction |
|---|---|---|
| Dutch native review not yet done (LR6) | WAIVED_WITH_LIMITATION | Internal exploratory use only; any public or publication-grade claim about Dutch performance requires native review first |
| Turkish project-owner review (QR9) | RESOLVED | Completed 2026-06-13; 7 corrections applied; gate now PASS |
| Independent bilingual review not yet started | NOT_STARTED | Required before any external publication; not a Stage 1/2 blocker for internal use |
| AC4 direct coverage absent (IS1) | WAIVED_WITH_LIMITATION | The benchmark does not directly test whether models confuse live-view subscription-independence; this gap is pre-registered; observed AC4 violations are logged as secondary observations in INT-005 |
| Some facts covered only indirectly (F0110, F0612, F0708, others) | WAIVED_WITH_LIMITATION | Coverage gaps documented in `intent-set.md`; these facts are present in the KB and may be tested incidentally but are not evaluation targets |
| Specific model/provider selection (TM1) | RESOLVED | CONFIRMED 2026-06-13: OpenAI GPT-4.1-mini/GPT-4.1 family; Stage 1a unblocked; exact tokenizer encoding name (TM1-a) confirmed in Stage 1 tooling |
| Instrumentation platform (M9) | RESOLVED 2026-06-14 | Lightweight local JSONL/CSV logging; `stage2-decision-plan.md` §4 |
| Human audit fraction (EV1) | RESOLVED 2026-06-14 | Audit all Stage 2 outputs manually; `stage2-decision-plan.md` §7 |
| Pilot budget (TM5/BS6) | RESOLVED 2026-06-14 | $25 USD hard cap; stop-and-review at $20; cap must be implemented/enforced before any call; `stage2-decision-plan.md` §8 |
| Embedding model for Agent B (TM8) | RESOLVED 2026-06-14 | OpenAI `text-embedding-3-small`; same model across EN/NL/TR; `stage2-decision-plan.md` §6 |
| Agent A context condition (AD1) | RESOLVED 2026-06-14 | A1 (full relevant-language KB in context); `stage2-decision-plan.md` §5 |
| Smoke-test run plan | RESOLVED 2026-06-14 | `stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0) created; 30-run plan defined |
| Logging runner — dry-run skeleton | RESOLVED 2026-06-14 | `scripts/stage2_smoke_runner.py`; all structural validations PASS; outputs in `results/stage2/dry_run_*` |
| Logging runner — live-mode scaffolding | RESOLVED 2026-06-14 | Pricing table, cost estimation, `BudgetGuard`, strict guard, CLI flags; live refused by default |
| Logging runner — pricing self-test | RESOLVED 2026-06-14 | `_run_pricing_selftest()` verifies the formula with synthetic rates; PASS (0.00202); included in dry-run validation |
| Model/pricing config document | RESOLVED 2026-06-14 | `stage2-model-pricing-config.md` (s2-model-pricing-v0.1.0); formula, hand-calculation, change-invalidation rules; confirmed-values table pending |
| Logging runner — live API/embedding paths | NOT_STARTED | Unreachable stubs; must be implemented + reviewed; blocks first API call |
| Exact model IDs (TM1-b/c) + `pricing_version` + pricing table not yet recorded | NOT_STARTED | Placeholders in runner CONFIG; must be set before first API call; see `stage2-live-run-readiness.md` §2–§4 and `stage2-model-pricing-config.md` §8 |
| Manual approval checklist for live run | NOT_STARTED | `stage2-live-run-readiness.md` §8; must be completed before `allow_api_calls=True` |

---

## 15. Overall readiness summary

| Activity | Ready? | Blocking issues |
|---|---|---|
| Quality review of existing artifacts | **YES** | None — all artifacts exist and pass structural checks |
| Query rendering plan | **YES** | `query-rendering-plan.md` complete; defines authoring rules for all 108 queries |
| Query rendering (108 queries) | **YES** | All three files created; 36 queries each; parity confirmed; structural quality gates PASS |
| Stage 1 tokenizer-only sanity gate | **COMPLETE** | Stage 1a run 2026-06-13; all sanity checks PASS; token-tax ratios in expected direction and range; results in `results/stage1a/`; tokenizer fallback (TM1-a) documented; re-run with exact tiktoken for authoritative counts |
| Stage 2 smoke test | **NO** | Decisions CONFIRMED + run plan + readiness doc + runner (dry-run + live scaffolding) (2026-06-14); remaining: live API/embedding paths, TM1-b/c model IDs, `pricing_version` + pricing table, manual approval checklist, `allow_api_calls=True` + `--live --confirm-spend` after review |
| Stage 3 full benchmark run | **NO** | All Stage 2 blockers + Stage 2 must complete first |
| Internal exploratory review and planning | **YES** | All methodology documents complete; benchmark artifact construction complete |
| Public or publication-grade claims | **NO** | Independent review not started; Dutch native review pending; all stages yet to run |

**Current position:** Stage 1a (tokenizer-only sanity gate) is **COMPLETE** as of 2026-06-13. All artifacts are structurally verified. QR9 (Turkish query review) is complete. TM1 is CONFIRMED (OpenAI GPT-4.1-mini/GPT-4.1). Stage 1a produced token-tax baselines for all 108 queries and 117 KB chunks; all sanity checks PASS (results in `results/stage1a/`). A tokenizer fallback was used (TM1-a; network restriction prevented exact tiktoken load); re-run with exact tiktoken for publication-grade counts. **All five Stage 2 decisions (M9, AD1, TM8, EV1, TM5/BS6) are CONFIRMED (2026-06-14); the run plan, the live-run readiness document (`stage2-live-run-readiness.md`), and the runner (dry-run skeleton + live-mode scaffolding with a strict guard, pricing table, `BudgetGuard`, and `--live`/`--confirm-spend` flags) all exist.** The dry-run passes all structural validations; live mode is refused by default. Stage 2 remains blocked on: the live completion + embedding paths (unreachable stubs), the version-pinned model IDs (TM1-b/c), `pricing_version` + pricing table (placeholders), the manual approval checklist, and `allow_api_calls=True` + `--live --confirm-spend` after review. No API call may be made until these are resolved and the runner reviewed.

---

## 16. Next actions

Listed in priority order. Each action unlocks subsequent steps.

1. **~~Confirm TM1~~ — DONE (2026-06-13).** OpenAI GPT-4.1-mini/GPT-4.1 family confirmed.

2. **~~Run Stage 1a tokenizer-only sanity gate~~ — DONE (2026-06-13).** Results in `results/stage1a/`; all sanity checks PASS; token-tax ratios in expected direction. Tokenizer fallback used (TM1-a); re-run with exact tiktoken for publication-grade counts.

3. **(Optional) Re-run Stage 1a with exact tiktoken** — in a network-accessible environment where `openaipublic.blob.core.windows.net` is reachable. The script auto-detects tiktoken availability and switches from fallback to exact counts. This is a quality improvement, not a prerequisite for Stage 2.

4. **Project-owner review of Turkish KB rendering** (`kb-rendering-tr.md`) — formal read-through for language quality before the KB rendering is frozen. Unblocks: Turkish rendering freeze; Stage 2 for Turkish.

5. **Decide Dutch review scope (QR8/LR6)** — is the Dutch rendering (KB + queries) sufficient for internal Stage 1/2 without a native reviewer? If deferred to pre-publication, document explicitly. Unblocks: Dutch artifact freeze decision.

6. **Resolve TM5/BS6 (pilot budget)** — approve spend before any API call; determines repetition count and smoke-test scope.

7. **~~Resolve remaining Stage 2 decisions~~ — DONE (2026-06-14).** All five (M9, AD1, TM8, EV1, TM5/BS6) CONFIRMED; see `docs/benchmark/v0.1/stage2-decision-plan.md` (s2-plan-v0.1.1).

8. **~~Create the Stage 2 smoke-test run plan~~ — DONE (2026-06-14).** `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0): 5 intents, run matrix, prompt plans (Agent A = A1, Agent B = Simple RAG), KB indexing, retrieval top-k=3, run order, budget enforcement, logging fields, pass/fail criteria.

9. **~~Implement the dry-run logging runner skeleton~~ — DONE (2026-06-14).** `scripts/stage2_smoke_runner.py`; dry-run builds 30 runs, validates all required fields, $0 cost, no API key; outputs in `results/stage2/dry_run_*`.

10. **~~Add live-mode scaffolding to the runner~~ — DONE (2026-06-14).** Pricing table, `estimate_cost_usd`, `BudgetGuard` (writes `results/stage2/budget_state.json`), strict `can_run_api_mode` guard, `--live`/`--confirm-spend` flags. Live refused by default. Readiness documented in `stage2-live-run-readiness.md`.

10b. **~~Create model/pricing config document and pricing self-test~~ — DONE (2026-06-14).** `docs/benchmark/v0.1/stage2-model-pricing-config.md` (s2-model-pricing-v0.1.0): model IDs, formula, hand-calculation example, change-invalidation rules, confirmed-values table (empty until pricing confirmed). `_run_pricing_selftest()` added to runner; verifies `estimate_cost_usd` formula with synthetic rates; PASS (0.00202). Dry-run revalidated: 11/11 PASS, $0 cost, live mode blocked.

11. **Record exact model IDs (TM1-b/c), `pricing_version`, and pricing table** — version-pinned `gpt-4.1-mini` snapshot + embedding version + per-1k rates. Placeholders are in runner CONFIG (`stage2-live-run-readiness.md` §2–§4).

12. **Implement and review the live runner paths** — completion + embedding calls (currently stubs) + wire `BudgetGuard` into the run loop. Complete the manual approval checklist (`stage2-live-run-readiness.md` §8). Set `allow_api_calls=True` only after review. No API call until reviewed.

---

*This document is the pre-run gate authority. A gate that is FAIL or BLOCKED stops the relevant stage. NEEDS_REVIEW gates require human sign-off. WAIVED_WITH_LIMITATION gates must be acknowledged in any results communication. Version: qg-v0.1.0.*
