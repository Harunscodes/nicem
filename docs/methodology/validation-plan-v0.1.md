# NiceM Validation Plan v0.1

**Status:** Consolidated roadmap — sequences the completed methodology layer into an executable plan
**Role:** This document introduces no new methodology. It integrates the twelve existing methodology documents into one step-by-step path from where the project stands (methodology complete, no artifacts built) to a completed exploratory pilot with interpreted results.
**Depends on:** every document listed in §2
**Feeds into:** Dataset specification, Stage 1–3 execution, v0.1 reporting, v0.2 planning

---

## 1. Purpose

The v0.1 methodology layer is complete: every prerequisite on the framework §12 checklist has a working answer. What does not yet exist is anything executable — no dataset, no fact-set, no runs, no results.

This document connects the two. It sequences the existing decisions into a roadmap with explicit quality gates and go/no-go decisions, so that benchmark construction can proceed without re-deriving methodology, and so that no stage spends budget before the previous stage has validated its prerequisites.

The governing principle, inherited from the tokenizer/model decision: **spend cheap effort before expensive effort** — review before tokenizing, tokenize before running, smoke-test before committing the full budget, validate the evaluator before interpreting costs.

---

## 2. Current methodology status

| Decision | Resolution | Document |
|---|---|---|
| Success definition (M1) | Binary PASS/FAIL gate with UNCERTAIN first-class; seven minimum criteria; nine failure types | `success-rubric-v0.1.md` |
| Task family | Product FAQ / Policy QA on a fictional synthetic KB; five task skeletons T1–T5 | `task-family-selection-v0.1.md` |
| Retrieval design (TF5) | Language-matched retrieval; KB quality control as hard prerequisite; language-neutral retrieval pre-registered for v0.2 | `retrieval-design-decision-v0.1.md` |
| Language set (TF3) | English (analytic baseline; fact-set canonical), Dutch, Turkish; English+Dutch fallback if Turkish review infeasible | `language-selection-v0.1.md` |
| Benchmark size (TF1/TF2) | 8 documents, ~75 canonical facts, 36 intents × 3 languages = 108 task instances; 2–3 repetitions if budget allows; exploratory | `benchmark-sizing-v0.1.md` |
| Logging schema | One row per run; full field set; dual token/semantic-unit retrieval reporting; minimal required v0.1 field set | `logging-schema-v0.1.md` |
| Agent designs | Agent A (Direct LLM baseline) vs. Agent B (Simple RAG); one model held constant; one architectural dimension of difference | `agent-design-selection-v0.1.md` |
| Falsification rules (M7) | Pre-registered H0/H1/H2; eight candidate-signal patterns; provisional thresholds; A-vs-B interpretation matrix; reporting rules | `falsification-and-decision-rules-v0.1.md` |
| Token-tax calculation | Per-intent ratios vs. English baseline; semantic normalization; residual-overhead method; grounded in Petrov/Ahia/Lundin | `baseline-token-tax-calculation-v0.1.md` |
| Tokenizer/model rules (BT1/LS4/LG2) | One model, one tokenizer; staged approach (tokenizer-only → smoke test → full run); selection criteria defined, provider TBD | `tokenizer-model-choice-v0.1.md` |
| Evaluation method (M2) | Deterministic fact-set checks primary; project-owner human audit layer; LLM-as-judge optional support only; recalibration gate | `evaluation-method-v0.1.md` |
| Framework | Endpoint-vs-trajectory split; six-component decomposition; §12 checklist now fully addressed | `nicem-methodology-framework-v0.1.md` |

---

## 3. Validation objective

> **NiceM v0.1 does not aim to prove execution-tax universally. It aims to test whether candidate execution-tax signals can be measured in a controlled synthetic Product FAQ / Policy QA benchmark across English, Dutch, and Turkish, under Direct LLM and Simple RAG agent designs.**

Secondary objectives, in priority order:
1. Validate the measurement instrument itself (logging, evaluation, decomposition) end to end.
2. Produce per-intent and between-intent variance estimates for the M8 power calculation.
3. Produce the first NiceM-specific token-tax table for English/Dutch/Turkish on this task family.
4. Surface failure patterns that inform v0.2 design (richer agents, more languages, contrast retrieval condition).

---

## 4. Remaining practical decisions before construction

These are decisions, not methodology gaps. Each blocks a specific step below.

| ID | Decision | Why it matters | Blocks |
|---|---|---|---|
| TM1 | Specific provider/model | Determines the tokenizer (and thus Stage 1 validity), pricing, multilingual competence, and version pinning | Stage 2 onward; Stage 1 only needs the matching tokenizer |
| TM5 / BS6 | Pilot budget | Determines repetition count (2–3× or none), smoke-test scope, and whether both AD1 sub-conditions are affordable | Stage 2 sizing, Stage 3 sizing |
| LS1 | Turkish KB review arrangement | The KB quality gate requires bilingual review of the Turkish rendering; evaluation-method permits owner self-review at run level, but the KB gate is stricter — if no arrangement is possible, the English+Dutch fallback activates | Step 7 of §5 |
| M9 | Instrumentation platform | Must capture the minimal field set of logging-schema §12; candidates Langfuse / Arize Phoenix (span-level, open-source); choice depends on agent framework | Stage 2 onward |
| EV1 | Human audit fraction | Must be fixed before analysis (pre-committed sampling, not post-hoc); determines review workload | §6 evaluation gate; analysis step 1 |
| TM8 / AD2 | Embedding model for Agent B | Multilingual coverage must be confirmed; same model across all three language conditions; it has its own tokenizer and cost accounting | Step 8 of §5; Stage 2 |
| AD1 | Direct LLM context condition (A0 no-context / A1 full-KB-in-context) | A0 mostly fails by design (fictional product) → few PASS runs for cost comparison; A1 yields PASS runs but measures long-context cost instead; running both doubles Agent A cost | Stage 2 design, Stage 3 design |

Recommended order: TM5/BS6 (budget) first — it constrains everything else; then TM1 (model), which fixes the tokenizer and unblocks Stage 1 fully; LS1, M9, TM8, EV1, AD1 can be settled in parallel during dataset construction.

---

## 5. Benchmark artifact construction sequence

The order matters: the fact-set precedes everything, and no language rendering precedes the language-neutral specification it renders.

1. **Create the canonical structured fact-set** (~75 facts across the seven categories of benchmark-sizing §6 plus general terms). This is the canonical artifact — every later artifact derives from it. **Complete:** `canonical-fact-set.md` (fs-v0.1.0) — 78 facts.
1b. **Create the document plan** — a section-level structural plan mapping every fact to a document section before any prose is written, so the three renderings can be parallel. **Complete:** `document-plan.md` (kb-plan-v0.1.0) — 39 sections, section-as-chunk convention, ambiguity controls AC1–AC9.
2. **Create the synthetic KB renderings** — 8 documents in English, Dutch, and Turkish, each authored *from the fact-set and document plan*, never translated from another rendering (TF4, TF7). Preceded by `language-rendering-plan.md` (per-language terminology, register, chunk-ID scheme).
3. **Create 36 language-neutral intent specifications** — each defined at the fact level (which facts, which conditions), per the intent design principles (benchmark-sizing §7). **Complete:** `intent-set.md` (intent-v0.1.0) — 36 intents (12 simple / 12 conditional / 12 troubleshooting-process); all 8 documents represented; AC1–AC9 covered; 7 open questions IS1–IS7.
4. **Render each intent in English, Dutch, and Turkish** — from the intent specification, not from the English rendering (LS3). To be done in `intent-set-rendering.md`.
5. **Create expected fact-set mappings** — one language-neutral expected fact-set per intent (`expected_fact_set_id`), stored separately from the prose KB (benchmark-sizing §8).
6. **Create forbidden claims / failure conditions per intent** — the hallucination-check targets and any format requirements (evaluation-method §4).
7. **Review all renderings** — KB completeness check per language (all five task skeletons answerable), bilingual review of the Turkish KB (LS1), intent-rendering review, register consistency (LS2).
8. **Freeze the dataset version** — assign `kb_version`, `kb_rendering_version` per language, and `benchmark_version`; no edits after freeze without a version bump.

**Full benchmark artifact construction phase is now complete.** All 14 benchmark artifacts exist: dataset-specification, canonical-fact-set, document-plan, language-rendering-plan, three KB renderings (EN/NL/TR), intent-set, expected-fact-mapping, quality-gates, query-rendering-plan, three query rendering files (EN/NL/TR), and the TM1 tokenizer/model decision note. The 108 user query renderings (36 × 3 languages) have been authored, structurally verified (36 entries each; same INT IDs across languages; no fact/chunk IDs or answer hints in query_text), and committed. A cross-language semantic equivalence audit was completed (2026-06-13); all 36 intents PASS for internal Stage 1 use. A query variant plan (`query-variant-plan.md`, qv-plan-v0.1.0) has been created, defining an optional Stage 1b robustness layer; variants are not required before Stage 1a.

Both prerequisites for Stage 1 are now resolved:
1. ~~Project-owner Turkish review of `query-rendering-tr.md` (QR9)~~ — **RESOLVED 2026-06-13**
2. ~~Tokenizer/model selection (TM1)~~ — **CONFIRMED 2026-06-13**: `tm1-tokenizer-model-decision.md` (tm1-v0.1.1) fixes the OpenAI GPT-4.1-mini/GPT-4.1 family for all of v0.1. **Stage 1a is unblocked**; the remaining step is the tooling task of confirming the exact `tiktoken` encoding name (TM1-a) and writing the counting script. No API calls.

The consolidated pre-run gate status is in `docs/benchmark/v0.1/quality-gates.md` (qg-v0.1.0).

---

## 6. Quality gates before any model run

All gates must pass before Stage 2 begins. Each gate has an owner action and a fail consequence.

| Gate | Check | If it fails |
|---|---|---|
| Fact-set completeness | Every intent's required facts exist in the canonical fact-set; no orphan facts, no orphan intents | Fix fact-set before any rendering work proceeds |
| KB rendering completeness | Each language rendering answers all five task skeletons; every canonical fact is expressed in every rendering | Fix rendering; re-review |
| Language rendering review | Turkish bilingual review done (LS1); Dutch/English owner review done; register consistent (LS2) | Fix or activate English+Dutch fallback |
| Expected fact-set consistency | Same required facts per intent across languages — only expression differs (falsification §6.2) | Fix before evaluation can be trusted |
| Tokenizer-only sanity gate | Stage 1 (§7) passed | Investigate renderings/tokenizer before spending API budget |
| Evaluation checker dry run | Deterministic checker runs against hand-written sample answers (correct, wrong, ambiguous) in all three languages and classifies them as expected | Fix matching rules; re-run dry run |
| Logging schema readiness | The M9 platform captures every minimal required field (logging-schema §12) in a test trace | Fix instrumentation or change platform — never drop fields |

---

## 7. Stage 1 — Tokenizer-only sanity gate

**Status: COMPLETE — 2026-06-13.** Results in `results/stage1a/`. All sanity checks PASS.

(Per tokenizer-model-choice §5 Stage 1; executable at near-zero cost once the tokenizer is fixed.)

- Tokenize all 108 query renderings (36 intents × 3 languages). ✓ Done.
- Tokenize all 117 KB chunks (39 × 3 languages). ✓ Done.
- Compute per-intent token-tax ratios (Dutch/English, Turkish/English) per baseline-token-tax §6. ✓ Done.
- Compare against rough literature expectations: Dutch ~1.1×–1.5×; Turkish above Dutch. ✓ PASS.
- Flag suspicious renderings. ✓ 7 outliers documented and explained (see `results/stage1a/token_tax_outliers.md`).
- Record the full token-tax table with `tokenizer_name`/`tokenizer_version`. ✓ Done (`o200k_base_approx`; see tokenizer resolution note).

**Key results:**
- Query NL/EN: median 1.000, mean 1.018 (Dutch mild premium; small query texts reduce the signal)
- Query TR/EN: median 1.083, mean 1.147 (Turkish above English; partially compressed by Turkish syntactic compactness in short queries)
- KB NL/EN: median 1.074, mean 1.086 (Dutch mild premium; clearly visible in longer texts)
- KB TR/EN: median 1.370, mean 1.426 (Turkish clear premium; 38/39 chunks show TR > NL)

**Pre-registered Stage 2 note:** For short queries (10–20 tokens), Turkish token-tax premium is smaller than for KB chunks. This is a linguistic observation (Turkish syntactic compactness), not a dataset error. Stage 2 should not assume uniform per-intent query token-tax premium.

**Tokenizer note (TM1-a):** Network policy in the execution environment blocks `openaipublic.blob.core.windows.net` (tiktoken BPE data host). Fallback tokenizer `o200k_base_approx` was used (o200k_base regex + BPE heuristic). For publication-grade counts, re-run `scripts/stage1a_tokenizer_sanity_gate.py` in a network-accessible environment. The script auto-switches to exact tiktoken when available.

**Go/no-go:** ✓ PROCEED to Stage 2 planning. Ratios are plausible against the literature; no rendering looks defective.

---

## 8. Stage 2 — Smoke test

**Stage 2 decision plan:** All five blocking decisions (M9, AD1, TM8, EV1, TM5/BS6) are **CONFIRMED (2026-06-14)** in `docs/benchmark/v0.1/stage2-decision-plan.md` (s2-plan-v0.1.1): M9 = lightweight local JSONL/CSV logging; AD1 = A1 (full relevant-language KB in Agent A prompt); TM8 = OpenAI `text-embedding-3-small`; EV1 = audit all Stage 2 outputs manually; TM5/BS6 = $25 USD hard cap. Stage 2 now remains blocked only on execution prerequisites: the smoke-test run plan, the minimal logging runner, version-pinned model IDs (TM1-b/c), and budget-cap enforcement — no API call until these exist and are reviewed.

**Recommended intent subset (§9 of decision plan):** INT-004, INT-015, INT-017, INT-026, INT-031. These cover simple factual / conditional / process task categories, four different NiceHome documents, and the AC9 two-chunk retrieval case.

(Extends tokenizer-model-choice §5 Stage 2 from Turkish-only to all three languages, since the evaluation method and logging pipeline also need validation.)

**Scope:** 5 intents × 3 languages × both agent designs = 30 runs, on the confirmed TM1 model family (GPT-4.1-mini/GPT-4.1), with the full logging schema and the full evaluation method applied — the smoke test exercises the entire pipeline, not just the model. Full manual review of all 30 outputs (EV1 Stage 2 rule).

**Checks:**
- The model answers in the language of the query, in all three languages.
- Turkish PASS rate is non-zero under Agent B (under no-context Agent A, failures are expected and confirm retrieval-dependence).
- Agent B retrieves from the correct language-matched KB rendering.
- All minimal required logging fields populate correctly (no nulls where values are expected; nulls where the schema requires them for Agent A).
- The evaluation method produces PASS/FAIL/UNCERTAIN with the deterministic checker, and human review of *all* smoke-test outputs confirms the checker's decisions.
- Hidden translation or unexpected model behavior is flagged where visible (`translation_used`, output-language checks).
- Cost and latency per run are within the TM5/BS6 budget envelope when extrapolated to Stage 3 scale.

**Go/no-go:** proceed to Stage 3 only if the smoke test produces analyzable traces end to end and the evaluation method is reliable on the smoke-test sample. Per tokenizer-model-choice §9: if the provider updates the model or tokenizer after the smoke test, re-run the smoke test (and Stage 1 if the tokenizer changed) before Stage 3.

---

## 9. Stage 3 — Full exploratory benchmark

- 36 intents × 3 languages = 108 language-condition task instances, executed under **both** Agent A and Agent B → 216 base runs (108 per agent design), subject to the AD1 decision on Agent A's context condition.
- Repetitions (2–3 per condition) only if budget permits; if budget forces a choice, prefer breadth of intents over repetitions (benchmark-sizing §10).
- Full logging schema on every run; evaluation per evaluation-method §14, with uncertainty and overturn rates tracked by language *during* the run, not only at the end.
- If the Turkish KB gate failed and the fallback is active: same plan at 2 languages (144 base runs).

**v0.1 remains exploratory.** Whatever Stage 3 produces, it does not support universal claims about languages, models, or execution-tax (benchmark-sizing §11; falsification §9).

---

## 10. Analysis sequence

Order is mandatory — later steps are only interpretable over earlier ones.

1. **Endpoint success analysis** — PASS/FAIL/UNCERTAIN rates per condition (language × design). Apply the evaluation gate first: if uncertainty >25% in any condition or overturn rates differ materially by language, stop and recalibrate before everything else (evaluation-method §14.5).
2. **Failure and uncertainty analysis** — failure-type distributions per condition; check the falsification §7 failure-rate threshold (>20pp gap triggers failure analysis before cost interpretation).
3. **Baseline token-tax calculation** — finalize the per-intent ratio table from Stage 1 plus run-level output/retrieval ratios (PASS runs only for output ratios).
4. **Cost/latency/token analysis** — per-condition distributions; cost per successful completion where the ≥10 PASS minimum (FD7) is met.
5. **Retrieval semantic-unit analysis** — Agent B only: retrieved facts vs. retrieved tokens; missing-fact and irrelevant-retrieval rates per language; apply the semantic-normalization rule (token gap with equal facts = token-tax, not retrieval overhead).
6. **Agent A vs. Agent B contrast** — the pilot's key comparison: does the cross-language gap change between designs?
7. **Residual overhead analysis** — the five-step method of baseline-token-tax §9; residuals reported as descriptive quantities with noise caveats.
8. **Falsification/decision-rule interpretation** — apply the pre-registered thresholds and the A-vs-B interpretation matrix; classify the outcome per §11 below. Thresholds are applied as registered; any deviation is declared and dual-reported (falsification §9.7).
9. **Reporting boundaries** — attach the mandatory scope statement to every reported number.

---

## 11. Interpretation outcomes

Exactly one primary outcome classification, from the pre-registered set:

| Outcome | Meaning |
|---|---|
| **Candidate execution-tax signal** | ≥2 trajectory components differ by language beyond token-count control, consistently across ≥5 intents or ≥2 categories, meeting the falsification §7 thresholds |
| **No observed candidate signal** | Measurement was adequate; cross-language differences are explained by token counts, or absent — H0 supported *in this setup* |
| **Agent-design amplification** | The cross-language gap widens from A to B — workflow design amplifies language cost (H2) |
| **Agent-design reduction** | The gap narrows from A to B — retrieval partially compensates; product-direction relevant (H2) |
| **Inconclusive — measurement failure** | One or more falsification §5/§6 conditions hit (too few PASS runs, high uncertainty, logging gaps, KB gate failure); neither H0 nor H1 is supported |
| **Recalibration needed** | The instrument (rubric, checker, fact-sets, KB renderings, or logging) needs revision before results can be classified; revise and re-run affected parts |

Amplification/reduction can co-occur with either of the first two outcomes; inconclusive and recalibration outcomes preempt all others.

---

## 12. Reporting rules

Consolidated from falsification §9, baseline-token-tax §12, and evaluation-method:

1. **Do not claim execution-tax is proven** — under any outcome. The strongest permissible claim is "candidate execution-tax signal observed in this setup."
2. **Report scope limits with every result:** this task family, this fictional KB, these three languages, this model and tokenizer (named, versioned), these two agent designs, language-matched retrieval.
3. **Report token-tax beside candidate execution-tax** — never an execution metric without its token context.
4. **Report PASS/FAIL/UNCERTAIN rates** for every condition alongside any cost figure.
5. **Report raw tokens and semantic units** for every retrieval comparison.
6. **Label all results as exploratory** — pilot-scale, not confirmatory.
7. **Label the single-evaluator limitation** — "single-evaluator exploratory pilot; independent review pending" on anything shared externally (EV7).
8. **No employer, customer, or internal data** appears anywhere in the benchmark, logs, or reports — synthetic artifacts only.

---

## 13. Startup relevance

Every outcome in §11 advances the startup question, which is **whether execution overhead is measurable, diagnosable, and reducible — not whether a universal theory is true**:

- **A positive candidate signal** justifies a properly powered v0.2 and gives NiceM its first own-data evidence — shareable (with labels) with advisors and collaborators.
- **A null signal** narrows the search: execution-tax does not appear in single-pass RAG on FAQ tasks for these languages — so v0.2 looks at richer agentic workflows, harder languages, or longer contexts. Knowing where the effect is *absent* sharpens both the research and the pitch.
- **An inconclusive result** hardens the instrument — and the instrument (observe → diagnose) is itself the first product layer. A validated multilingual execution-measurement pipeline has value independent of any particular finding.
- **Agent-design differences (either direction)** are the most commercially direct outcome: if design choice measurably changes cost per successful completion across languages, then "recommend → simulate → measure impact" has a demonstrated lever to operate on.

---

## 14. What comes after this plan

In order:

1. **Resolve the §4 practical decisions** — budget (TM5/BS6) and model (TM1) first.
2. **Create the dataset specification** — formats and authoring protocol for the fact-set, KB renderings, intent specifications, expected fact-sets, and forbidden claims (the §5 sequence made concrete). **Complete:** `docs/benchmark/v0.1/dataset-specification.md` defines the fictional product domain (NiceHome ecosystem), the 8-document structure and per-document fact estimates (~75 total), the canonical fact schema (§5), the intent schema (§6), language rendering rules (§7), expected answer design (§8), the 12/12/12 difficulty split (§9), retrieval implications (§10), quality gates (§11), and versioning scheme (§12). Eight open questions DS1–DS8.
3. **Create the canonical fact-set** — the first real benchmark artifact (§5 step 1).
4. **Build and run the Stage 1 tokenizer-only script** — the first and only code needed before any model run.
5. **Create the Stage 2 smoke-test plan** — intent selection, checklist, budget cap.
6. **Only then begin PoC implementation** — Agent A, Agent B, instrumentation, checker — consistent with the repository rule: minimal proof-of-concept, not a SaaS product.

---

## 15. Open risks

| Risk | Mitigation in this plan |
|---|---|
| Budget insufficient for repetitions or both AD1 sub-conditions | Decide TM5/BS6 first; prefer intent breadth over repetitions; smoke test extrapolates cost before commitment |
| Model/provider drift mid-pilot | Version pinning; re-run smoke test (and Stage 1 if tokenizer changed) on any version change |
| Evaluator bias | Language-neutral fact-set checks; per-language uncertainty/overturn tracking; recalibration gate before interpretation |
| Turkish self-review limitation | Acceptable for internal pilot; independent bilingual review required before public claims; stated on all shared results |
| Embedding model multilingual bias | Same embedding model across languages (its unevenness becomes a measured property); confirm coverage in smoke test (TM8) |
| Insufficient PASS runs (<10 per condition) | FD7 minimum enforced; AD1 full-context sub-condition and KB revision as remedies; smoke test catches this early |
| Hidden in-model translation | `translation_used` + output-language checks; residual undetectability stated as a limitation in all reporting (AD6/FD6) |
| Overinterpreting small samples | Pre-registered thresholds; exploratory labeling; no p-values presented as confirmatory (benchmark-sizing §9) |
| Confusing token-tax with execution-tax | The decomposition, dual-reporting rule, and residual method exist precisely to prevent this; reporting rule 3 enforces it |

---

*v0.1 — 2026-06-10 — This plan sequences existing decisions; it introduces no new methodology. Execution-tax remains a hypothesis to validate.*
