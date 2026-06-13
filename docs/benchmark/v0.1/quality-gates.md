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
| `query-rendering-tr.md` | **NEEDS_REVIEW** | Project owner (QR9) | File exists; 36 queries confirmed; INT-001–036 all present; apostrophe suffix convention applied; controlled terms applied; versioned qr-tr-v0.1.0 | Project-owner Turkish review required BEFORE Stage 1; QR9 is an active gate |
| All artifacts in `source-map.md` | **PASS** | Project owner | Every artifact created in this phase is catalogued in `docs/source-map.md` | — |

**Inventory gate verdict: PASS** — all 13 artifacts exist. Content quality gates follow below.

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
| Specific tokenizer/provider selected | **BLOCKED** | TM1 is unresolved — specific provider/model not yet chosen; tokenizer identity is required to run Stage 1 |
| Query rendering plan exists | **PASS** | `query-rendering-plan.md` created; defines register, style, difficulty-preservation, AC controls, and QR1–QR9 open questions |
| 36 × 3 = 108 query renderings exist | **PASS** | `query-rendering-en.md` (36), `query-rendering-nl.md` (36), `query-rendering-tr.md` (36) all created; INT-001–036 present in each; parity confirmed by automated diff |
| Turkish query review (QR9) | **NEEDS_REVIEW** | Active gate — project owner must review `query-rendering-tr.md` before Stage 1; QR9 pre-registered in query-rendering-plan.md |
| KB renderings ready for tokenization | **PASS** | `kb-rendering-en.md`, `kb-rendering-nl.md`, `kb-rendering-tr.md` all exist and are structurally verified |
| Token-tax calculation method documented | **PASS** | `docs/methodology/baseline-token-tax-calculation-v0.1.md` defines per-intent ratios and the five-step residual method |
| Stage 1 go/no-go criteria defined | **PASS** | `validation-plan-v0.1.md` §7 defines the sanity check against literature expectations (Dutch ~1.1×–1.5×; Turkish above Dutch) |

**Stage 1 gate verdict: BLOCKED** — one prerequisite remaining: tokenizer/provider not selected (TM1). All 108 query renderings exist and Turkish query review (QR9) is complete.

---

## 13. Stage 2 readiness gate

*Stage 2 = smoke test: 3–5 intents, both agent designs, all three languages, small instrumented run.*

| Criterion | Status | Notes |
|---|---|---|
| Specific model/provider selected (TM1) | **BLOCKED** | — |
| Embedding model for Agent B selected (TM8/AD2) | **BLOCKED** | Multilingual coverage must be confirmed; same model across all languages |
| Instrumentation platform (M9) | **BLOCKED** | Must capture minimal logging fields |
| Smoke-test intent subset selected | **NOT_STARTED** | Should be chosen after Stage 1; recommend 1 simple + 1 conditional + 1 troubleshooting-process covering different documents |
| Pilot budget approved (TM5/BS6) | **NOT_STARTED** | Budget must be confirmed before any API spend |
| Evaluation procedure ready | **PASS** | `evaluation-method-v0.1.md` and `expected-fact-mapping.md` are complete |
| Logging pipeline ready | **BLOCKED** | Depends on M9 |
| Human audit fraction pre-committed (EV1) | **NOT_STARTED** | Must be set before Stage 2 analysis begins |
| Direct LLM context condition (AD1: A0 vs. A1) | **NOT_STARTED** | Choice of no-context vs. full-KB-in-context for Agent A must be made; affects Stage 2 design and cost |

**Stage 2 gate verdict: BLOCKED** — five open decisions (TM1, TM8, M9, TM5, AD1) and two pending starts (EV1, smoke-test subset).

---

## 14. Known limitations and waivers

All v0.1 results must carry the label: **"Single-evaluator exploratory pilot; independent review pending."** This applies to any external communication.

| Limitation | Type | Scope restriction |
|---|---|---|
| Dutch native review not yet done (LR6) | WAIVED_WITH_LIMITATION | Internal exploratory use only; any public or publication-grade claim about Dutch performance requires native review first |
| Turkish project-owner review not yet done | NEEDS_REVIEW | Formal review pass before Stage 2 smoke test; project owner may approve informally for Stage 1 tokenizer-only |
| Independent bilingual review not yet started | NOT_STARTED | Required before any external publication; not a Stage 1/2 blocker for internal use |
| AC4 direct coverage absent (IS1) | WAIVED_WITH_LIMITATION | The benchmark does not directly test whether models confuse live-view subscription-independence; this gap is pre-registered; observed AC4 violations are logged as secondary observations in INT-005 |
| Some facts covered only indirectly (F0110, F0612, F0708, others) | WAIVED_WITH_LIMITATION | Coverage gaps documented in `intent-set.md`; these facts are present in the KB and may be tested incidentally but are not evaluation targets |
| Specific model/provider not yet selected (TM1) | BLOCKED | Blocks Stage 1 and all later stages |
| Instrumentation platform not yet selected (M9) | BLOCKED | Blocks Stage 2 and later |
| Human audit fraction not yet decided (EV1) | NOT_STARTED | Must be decided and pre-committed before Stage 2 analysis |
| Pilot budget not yet approved (TM5/BS6) | NOT_STARTED | Must be approved before any API spend |
| Embedding model for Agent B not yet selected (TM8) | BLOCKED | Blocks Stage 2 and later |
| Agent A context condition not yet decided (AD1) | NOT_STARTED | Must be decided before Stage 2 design is finalized |

---

## 15. Overall readiness summary

| Activity | Ready? | Blocking issues |
|---|---|---|
| Quality review of existing artifacts | **YES** | None — all artifacts exist and pass structural checks |
| Query rendering plan | **YES** | `query-rendering-plan.md` complete; defines authoring rules for all 108 queries |
| Query rendering (108 queries) | **YES** | All three files created; 36 queries each; parity confirmed; structural quality gates PASS |
| Stage 1 tokenizer-only sanity gate | **NO** | TM1 (tokenizer/model not yet selected); Turkish query owner review (QR9) required before Stage 1 proceeds |
| Stage 2 smoke test | **NO** | TM1, TM8, M9, TM5/BS6, AD1, EV1, query renderings |
| Stage 3 full benchmark run | **NO** | All Stage 2 blockers + Stage 2 must complete first |
| Internal exploratory review and planning | **YES** | All methodology documents complete; benchmark artifact construction complete |
| Public or publication-grade claims | **NO** | Independent review not started; Dutch native review pending; all stages yet to run |

**Current position:** The full benchmark artifact construction phase is complete. All 13 artifacts exist and pass structural quality gates: dataset-specification, canonical-fact-set, document-plan, language-rendering-plan, three KB renderings, intent-set, expected-fact-mapping, quality-gates, query-rendering-plan, and three query rendering files (13 artifacts). The benchmark now has 108 user query renderings (36 × EN/NL/TR), all structurally verified. Two prerequisites remain before Stage 1: Turkish query owner review (QR9) and tokenizer/model selection (TM1).

---

## 16. Next actions

Listed in priority order. Each action unlocks subsequent steps.

1. **Project-owner review of Turkish query renderings (QR9)** — review `query-rendering-tr.md` for language quality, natural phrasing, controlled terminology consistency, and apostrophe suffix correctness. This is an active gate that blocks Stage 1. Can be done in parallel with TM1 resolution.

2. **Project-owner review of Turkish KB rendering** (`kb-rendering-tr.md`) — formal read-through for language quality before the KB rendering is frozen. Unblocks: Turkish rendering freeze; Stage 2 for Turkish.

3. **Decide Dutch review scope (QR8/LR6)** — is the Dutch rendering (KB + queries) sufficient for internal Stage 1/2 without a native reviewer? If deferred to pre-publication, document explicitly. Unblocks: Dutch artifact freeze decision.

4. **Resolve TM1 (specific tokenizer/model)** — select the provider/model and fix the tokenizer version. This is the highest-priority practical decision and the remaining structural blocker for Stage 1.

5. **Resolve TM5/BS6 (pilot budget)** — approve spend before any API call; determines repetition count and smoke-test scope.

6. **Resolve remaining practical decisions** — TM8 (embedding model), M9 (instrumentation platform), EV1 (audit fraction), AD1 (Agent A context condition). These can be resolved in parallel once budget is approved.

7. **Run Stage 1 tokenizer-only sanity gate** — tokenize all 108 queries + 39 × 3 KB chunks; compute per-intent token-tax ratios; compare against literature expectations. Cost: near-zero. Unblocks: Stage 2 if go/no-go criteria pass.

---

*This document is the pre-run gate authority. A gate that is FAIL or BLOCKED stops the relevant stage. NEEDS_REVIEW gates require human sign-off. WAIVED_WITH_LIMITATION gates must be acknowledged in any results communication. Version: qg-v0.1.0.*
