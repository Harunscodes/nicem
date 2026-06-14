# Stage 2 Decision Plan v0.1

**Version:** s2-plan-v0.1.1
**Date:** 2026-06-14
**Status:** CONFIRMED — all five decisions confirmed by project owner 2026-06-14; Stage 2 remains blocked on the smoke-test run plan and logging runner (see §2)
**Depends on:** `validation-plan-v0.1.md`, `quality-gates.md` §13, `logging-schema-v0.1.md`, `agent-design-selection-v0.1.md`, `evaluation-method-v0.1.md`
**Feeds into:** Stage 2 smoke-test run plan, minimal logging runner implementation

---

## 1. Purpose

Stage 1a (tokenizer-only sanity gate) is complete. All 108 query renderings and 117 KB chunks have been tokenized; token-tax ratios are in the expected direction and range; all structural quality gates PASS. The next step is Stage 2: a small instrumented smoke test that runs Agent A and Agent B on a subset of intents across all three languages and verifies that the full measurement pipeline works end to end.

Stage 2 requires five decisions that do not exist yet. These are not methodology gaps — the methodology is complete. They are practical design choices whose answers determine what gets built for Stage 2, in what order, and at what cost.

This document resolves those five decisions by providing a recommended default for each, explaining the reasoning, and identifying which decisions still require project-owner confirmation before any API budget is spent.

The governing principle from `validation-plan-v0.1.md` §1 applies: **spend cheap effort before expensive effort.** The purpose of Stage 2 is to validate the pipeline, not to prove execution-tax. No claims about execution-tax will be made from Stage 2 results. A smoke test that runs cleanly, logs all required fields, and produces classifiable PASS/FAIL/UNCERTAIN outcomes is a fully successful Stage 2.

---

## 2. Current status

| Item | Status | Notes |
|---|---|---|
| Stage 1a (tokenizer-only sanity gate) | **COMPLETE** | Run 2026-06-13; all sanity checks PASS; results in `results/stage1a/` |
| Token-tax baseline | **MEASURED (APPROXIMATE)** | `o200k_base_approx` fallback used; network policy blocked tiktoken BPE data download; directionally valid for sanity gate; not publication-grade absolute counts |
| All benchmark artifacts | **STRUCTURALLY COMPLETE** | Inventory gate PASS; content freeze pending language reviews |
| Execution-tax | **NOT MEASURED** | Stage 2 is not an execution-tax proof; it is a pipeline validation smoke test |
| Five Stage 2 decisions (M9, AD1, TM8, EV1, TM5/BS6) | **CONFIRMED 2026-06-14** | All five confirmed by project owner; see §13 table and per-decision confirmation notes |
| Stage 2 | **BLOCKED** | Two artifacts remain before the first API call: the smoke-test run plan (`stage2-smoke-test-run-plan.md`) and the minimal logging runner; both must be created and reviewed |

**What Stage 2 is not:** a proof of execution-tax, a full benchmark, or a basis for public claims. It is a controlled exercise to confirm that the measurement instrument works before committing Stage 3 budget.

**What still blocks the first API call (as of 2026-06-14):** the five decisions are confirmed, but Stage 2 is *not* yet runnable. Two things remain: (1) `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` — the run plan specifying prompt templates, KB indexing procedure, run order, and budget-enforcement mechanism; and (2) the minimal logging runner script. Neither may trigger an API call until both exist and are reviewed, and until the budget cap is implemented or manually enforced.

---

## 3. Recommended decision order

The five blocking decisions should be resolved in this order:

1. **M9 — instrumentation platform**
2. **AD1 — Agent A context condition**
3. **TM8 — embedding model for Agent B**
4. **EV1 — human audit fraction**
5. **TM5/BS6 — pilot budget**

**Rationale for this order:**

M9 (instrumentation) comes first because it determines what the logging runner looks like. Every other decision generates fields that must be logged — so knowing how logging works before deciding what to log avoids rework. If M9 selects lightweight local JSONL logging, the runner is a simple script; if M9 selects Langfuse or another platform, the runner is a different kind of integration.

AD1 (Agent A context condition) comes second because it determines the structure of the smoke-test runs: how many run types, how the prompt is constructed for Agent A, and whether an A0/A1 split is needed. This affects the Stage 2 cost estimate (§8) and therefore the TM5/BS6 budget conversation.

TM8 (embedding model) comes third because it is the most technically constrained decision: multilingual coverage must be confirmed, and the model must be the same across all three language conditions. Once M9 is selected, the embedding model choice can be evaluated in the context of the instrumentation tooling.

EV1 (human audit fraction) comes fourth because it is a policy decision, not a technical one. At Stage 2 smoke-test scale (18–30 runs), the answer is almost certainly "audit all outputs" — but this must be pre-committed, not decided after seeing results.

TM5/BS6 (pilot budget) comes last in the decision sequence because it is the constraint that bounds the scope of Stage 2. The intent subset (§9) and repetition count follow from the approved budget, not the other way around. However, budget confirmation should happen *before any API call* — the recommended approach is to fix the budget cap, then size the smoke test to fit within it.

---

## 4. M9 — instrumentation platform decision

### Problem

Stage 2 requires per-run logging of input tokens, output tokens, retrieval chunks, latency, cost, and endpoint outcome. The instrumentation platform is the mechanism by which these fields are captured reliably and reproducibly.

### Options

| Option | Description | Pro | Con |
|---|---|---|---|
| **Lightweight local JSONL/CSV logging** | A simple Python runner writes one JSONL record per run; a summary CSV is generated at the end | Transparent, fully controllable, no external dependency, easy to inspect and audit | No span-level per-step breakdown; must implement all counting manually |
| **Langfuse** | Open-source, self-hostable, span-level observability; strong OpenAI integration | Span-level per-call attribution; UI for trace inspection; free for self-hosted; production-ready | Requires a Langfuse server (local or cloud); extra setup overhead; not needed at smoke-test scale |
| **LangSmith** | LangChain-native observability and dataset management | Good if Agent B uses LangChain; dataset tracking built in | LangChain coupling; not ideal if agents are built with a different framework; paid tiers |
| **Braintrust** | Scorer-first evaluation and experiment tracking | Good for longitudinal tracking; score-centric design | More overhead than needed for a smoke test |
| **Arize Phoenix** | Open-source, OpenTelemetry-compatible; strong span-level attribution | Vendor-neutral; works with any agent framework | Setup overhead; adds an external dependency for what is currently a simple script-based pipeline |
| **Custom notebook only** | Run calls from a Jupyter notebook with manual logging | Zero setup | Not reproducible; not suitable for a benchmark with repeatable runs |

### Decision: CONFIRMED — lightweight local JSONL/CSV logging (2026-06-14)

**Project-owner confirmation (2026-06-14):** Use lightweight local JSONL/CSV logging for Stage 2. One record per run. The minimum required fields from `logging-schema-v0.1.md` must be captured. No external observability platform in Stage 2.

For the Stage 2 smoke test, lightweight local JSONL/CSV logging is the correct choice. The reasons are:

- **Transparency:** every logged field is written by code the project owner controls and can inspect directly. There is no intermediate abstraction that might silently miscategorize a field.
- **No external dependency:** the smoke test does not require a Langfuse server, a LangSmith account, or any cloud service. The only external dependency is the OpenAI API itself.
- **Auditability:** a JSONL file with one record per run is the simplest possible audit trail. Each record maps directly to the logging schema field set.
- **Portability:** the same logging format can be ingested by Langfuse or Arize Phoenix in Stage 3 if a platform is added later — starting with structured JSONL does not lock out platform adoption.

Stage 3 may benefit from a span-level platform (Langfuse or Arize Phoenix) once per-step attribution is needed. Stage 2 does not require that level of granularity.

### Required minimal log fields

Each run record must include all fields in the `logging-schema-v0.1.md` §12 minimal required set. For Stage 2, this is:

| Field | Type | Notes |
|---|---|---|
| `run_id` | string | Unique identifier per run (e.g., `RUN-001`); deterministic from intent+language+agent+repetition |
| `intent_id` | string | e.g., `INT-004` |
| `language` | string | `EN`, `NL`, or `TR` |
| `agent_design_id` | string | `A` (Direct LLM baseline) or `B` (Simple RAG) |
| `model_id` | string | Version-pinned completion-model identifier (e.g., `gpt-4.1-mini-2025-04-14`); never a "latest" alias |
| `embedding_model_id` | string\|null | Embedding model used by Agent B (confirmed: `text-embedding-3-small`); `null` for Agent A |
| `embedding_model_version` | string\|null | Version/snapshot identifier for the embedding model; `null` for Agent A |
| `prompt_version` | string | Version of the prompt template used; allows rerunning with identical prompts |
| `query_text` | string | The exact query sent to the model (from query-rendering files) |
| `retrieved_chunk_ids` | list\|null | Chunk IDs retrieved by Agent B; `null` for Agent A |
| `retrieved_fact_ids` | list\|null | Fact IDs covered by retrieved chunks; `null` for Agent A; derived from chunk metadata |
| `input_tokens` | integer | As reported by the provider API |
| `output_tokens` | integer | As reported by the provider API |
| `total_tokens` | integer | `input_tokens + output_tokens` |
| `model_calls` | integer | Number of API calls made (≥1; >1 if retries or multi-step) |
| `retrieval_calls` | integer | Number of retrieval/embedding calls made; `0` for Agent A |
| `retry_count` | integer | Number of retries triggered; `0` for a clean first-pass run |
| `latency_ms` | integer | Wall-clock time from query submission to final response, in milliseconds |
| `estimated_cost_usd` | float | Computed from `pricing_version` token rates; not provider-reported billing |
| `pricing_version` | string | Date-stamped price table used for cost computation (e.g., `openai-2026-06-14`) |
| `raw_model_output` | string | The full model output text; required for evaluation |
| `endpoint_outcome` | string | `PASS`, `FAIL`, or `UNCERTAIN`; assigned by evaluator *after* the run, blind to cost/trajectory |
| `failure_type` | string\|null | From the nine failure types in `success-rubric-v0.1.md`; `null` if PASS |
| `evaluator_notes` | string\|null | Free-text evaluator notes; especially required for UNCERTAIN outcomes |

Fields from `logging-schema-v0.1.md` that are deferred to Stage 3 or later: `human_correction_count`, `correction_tokens`, `quality_band`, `retrieval_score` (if not captured by the embedding library), `agent_trace` (full step-by-step trace; capture if logging makes it easy, otherwise defer).

---

## 5. AD1 — Agent A context condition

### Problem

Agent A is the Direct LLM baseline. The agent-design decision (`agent-design-selection-v0.1.md`) established that Agent A differs from Agent B in exactly one dimension: Agent A does not use retrieval. But the NiceHome policy domain is entirely fictional — no model can know NiceHome's return window or Hub factory-reset sequence from training data. This means a no-context Agent A will produce mostly FAIL runs, which limits the cost-per-successful-completion comparison.

### Options

| Option | Description | Implication |
|---|---|---|
| **A0: Direct LLM, no KB context** | Agent A receives only the user query; no policy document is in the prompt | Most runs will FAIL on fictional policy facts; few PASS runs available for cost comparison; measures model knowledge baseline |
| **A1: Direct LLM, full KB-in-context** | Agent A receives the complete KB (all three language renderings concatenated or the relevant-language rendering only) in the prompt alongside the user query | Agent A can answer correctly; measures cost of long-context prompting vs. retrieval; eliminates retrieval but does not eliminate KB context |
| **A1b: Direct LLM, single-document context** | Agent A receives only the document most likely to contain the answer (project owner identifies document per intent) | A compromise; reduces context size vs. A1; but document selection is a form of retrieval decision made by the evaluator, not the agent |

### Decision: CONFIRMED — A1 (2026-06-14)

**Project-owner confirmation (2026-06-14):** Use A1. Agent A is the Direct LLM baseline with the full relevant-language KB rendering in the prompt. Reason: A0 would likely fail the fictional-domain benchmark because the model should not know NiceHome policies.

### Decision rule and recommendation

**Agent A should be a direct-answer baseline with the minimum controlled context needed to make the task answerable, without using retrieval.**

The key constraint from `agent-design-selection-v0.1.md`: Agent A and Agent B must differ in exactly one architectural dimension. That dimension is retrieval: Agent B retrieves relevant chunks; Agent A does not. Both must have access to equivalent information in principle — otherwise the comparison measures "access to information" not "cost of retrieval."

**Recommendation: A1 — Direct LLM with the relevant-language full KB rendering in context.**

Rationale:
- A0 produces near-zero PASS rates on fictional policy facts, making CPS undefined or unmeasurable for Agent A. The comparison collapses.
- A1 puts the full KB in the prompt. Agent A and Agent B both have access to the same factual content; the difference is *how* they access it (full context vs. retrieved chunks). This makes the cost comparison interpretable.
- A1 provides the most direct measurement of the architectural trade-off: long-context prompting cost vs. retrieval cost. This is a genuine execution-overhead signal, not an information-access confound.
- For the NiceHome domain, the relevant-language KB rendering is approximately 39 chunks × ~100–200 tokens each = ~4,000–8,000 tokens per language. This is well within the GPT-4.1-mini context window and keeps costs manageable.

**Alternative worth pre-registering for Stage 3:** run A0 as an additional condition in Stage 3 to measure the failure-rate floor. If A0 produces near-zero PASS, this establishes that the fictional domain is not learnable from pretraining — a validity check on the benchmark, not a main analysis condition.

**What Agent A must not do:** rely on model-internal knowledge about NiceHome. If the project owner suspects a model is "guessing correctly" on fictional policy facts at rates higher than chance, this must be logged in `evaluator_notes` and treated as a confound.

---

## 6. TM8 — embedding model decision

### Problem

Agent B (Simple RAG) requires an embedding model to encode KB chunks and queries for semantic retrieval. The embedding model choice affects: multilingual retrieval quality, retrieval fairness across EN/NL/TR, cost, repeatability, and the `retrieval_calls` field in the logging schema.

### Requirements (non-negotiable)

- **Multilingual:** the same embedding model must be used for all three language conditions. Using a different embedding model for Turkish than for English would introduce a confound into retrieval quality comparisons.
- **Same model across all KB renderings:** the EN, NL, and TR KB chunks must all be embedded with the same model, version-pinned.
- **Retrieval score accessible:** the embedding library or API must return per-chunk similarity scores so they can be logged.
- **Deterministic enough for repeatability:** the same query embedded twice should return the same top-k chunks (or near-identical rankings); this is important for reproducibility across repetitions.

### Candidate options

| Model | Provider | Notes |
|---|---|---|
| `text-embedding-3-small` | OpenAI | Strong multilingual coverage; 1536 dimensions; low cost (~$0.02/1M tokens); same provider as TM1 completion model — simplifies accounting |
| `text-embedding-3-large` | OpenAI | Better quality; higher cost; same provider advantage |
| `multilingual-e5-large` | Open-source (HuggingFace) | Strong multilingual model; free to run locally; avoids additional API dependency; requires local inference setup |
| `paraphrase-multilingual-mpnet-base-v2` | Open-source (HuggingFace) | Lighter; good multilingual baseline; can run on CPU |

### Decision: CONFIRMED — `text-embedding-3-small` (2026-06-14)

**Project-owner confirmation (2026-06-14):** Use OpenAI `text-embedding-3-small` for Agent B Simple RAG. Use the same embedding model for English, Dutch, and Turkish. Record `embedding_model_id` and `embedding_model_version` in the logs.

For the Stage 2 smoke test, `text-embedding-3-small` is the recommended default:
- Same provider as the TM1 completion model; one API key, one billing account, one `pricing_version` table.
- Confirmed multilingual coverage including Turkish.
- Retrieval scores (cosine similarity) available from the OpenAI embeddings response.
- Low enough cost that embedding 39 chunks × 3 languages + 5 intents × 3 languages for Stage 2 is negligible.
- If Stage 3 requires a different embedding model (e.g., for cost reasons or quality concerns), this must be noted as a configuration change — Stage 3 results would not be directly comparable to Stage 2 results if the embedding model changes.

**Final selection (CONFIRMED 2026-06-14): `text-embedding-3-small`.** The local open-source alternatives (`multilingual-e5-large`, `paraphrase-multilingual-mpnet-base-v2`) are not used in Stage 2. The selection is logged as `embedding_model_id` and `embedding_model_version` in every Agent B run record and is fixed for all of Stage 2.

**Pre-registration note:** the embedding model is itself a potential execution-tax variable. If the model has uneven quality across EN/NL/TR, retrieval precision will differ by language — confounding the execution-tax signal. This must be acknowledged in Stage 2 and Stage 3 reporting. A retrieval quality check (do the top-k chunks for each intent contain the required fact IDs?) should be performed at Stage 2 setup and logged.

---

## 7. EV1 — human audit fraction

### Problem

`evaluation-method-v0.1.md` §6 defines the human audit policy: all UNCERTAINs are mandatory review; all FAILs are strongly recommended; a sample of PASSes is reviewed for calibration. The specific sampling fraction for PASSes (EV1) must be pre-committed before any run — it cannot be decided after seeing results without introducing selection bias.

### Decision: CONFIRMED — audit all Stage 2 outputs (2026-06-14)

**Project-owner confirmation (2026-06-14):** Audit all Stage 2 outputs manually. This includes PASS, FAIL, and UNCERTAIN outputs. No sampling at Stage 2.

At Stage 2 smoke-test scale (18–30 runs across 5 intents × 3 languages × 2 agents), the total number of outputs is small enough that full manual review is the correct approach:

- Reviewing all 18–30 outputs takes less time than building a sampling protocol for this scale.
- Full review at Stage 2 calibrates the evaluator's fact-checking procedure against the expected-fact-mapping entries before Stage 3 scales up.
- Full review at Stage 2 catches any systematic evaluation errors (e.g., UNCERTAIN for conditions that should be FAIL) before they propagate to Stage 3 analysis.
- The UNCERTAIN recalibration gate (>25% UNCERTAIN rate in any condition triggers a stop) can only be assessed reliably with full review at small scale.

**Pre-commit the following EV1 rule for Stage 2:**
> All Stage 2 outputs receive human evaluation by the project owner. No sampling. Evaluation is blind to cost and trajectory data (evaluator sees model output + expected fact mapping only). Turkish outputs: project owner (native speaker). Dutch outputs: project owner (non-native, reviewing for factual accuracy against the language-neutral expected fact mapping; phrasing review deferred to LR6 independent reviewer).

**Stage 3 EV1 rule** (to be confirmed before Stage 3): audit all FAILs + all UNCERTAINs + ≥20% of PASSes per condition (EN/NL/TR × A/B), randomly selected and pre-committed before analysis.

---

## 8. TM5/BS6 — pilot budget

### Problem

No API call should be made before a hard budget cap is confirmed. Budget determines: the repetition count (one pass through 5 intents × 3 languages × 2 agents = 30 runs before any repeats), whether a rerun of failed logging is affordable, and whether the optional exact tiktoken rerun is included in Stage 2 scope.

### Stage 2 cost estimate

| Item | Count | Estimated tokens per run | Estimated cost |
|---|---|---|---|
| Agent A (A1 full-KB-in-context): completion calls | 15 runs (5 intents × 3 languages) | ~5,000–9,000 input + ~100–300 output = ~9,300 tokens/run | ~$0.03–0.09/run × 15 = ~$0.45–1.35 |
| Agent B (Simple RAG): completion calls | 15 runs (5 intents × 3 languages) | ~500–1,500 input (retrieved chunks + query) + ~100–300 output = ~1,800 tokens/run | ~$0.006–0.018/run × 15 = ~$0.09–0.27 |
| Agent B: embedding calls (KB chunks) | 39 chunks × 3 languages = 117 embeddings; one-time at KB index build | ~100 tokens/chunk × 117 = ~11,700 tokens | ~$0.0002 at text-embedding-3-small rates |
| Agent B: embedding calls (queries, per run) | 15 query embeddings | ~20 tokens/query × 15 = 300 tokens | negligible |
| Buffer for reruns and debugging | — | — | 2× the above |

**Total estimated Stage 2 cost: under $10 USD** at GPT-4.1-mini pricing and one pass through 5 intents × 3 languages × 2 agents, even with a 2× rerun buffer. The dominant cost is Agent A long-context prompting.

**Decision: CONFIRMED — $25 USD hard cap (2026-06-14).**

**Project-owner confirmation (2026-06-14):** Approve a $25 USD hard cap for Stage 2. Stop and review at $20 USD. Estimated actual spend is around $5–10, but the hard cap is $25. **No API call may run unless the budget cap is implemented (programmatic cost ceiling in the runner) or manually enforced (operator monitors running cost and halts at the threshold).**

This covers one full pass, a rerun buffer, and a second repetition of any intent where logging failed. Any spend approaching $20 triggers a stop-and-review before further calls. The budget-enforcement mechanism (programmatic vs. manual) must be specified in the smoke-test run plan before the first API call.

---

## 9. Stage 2 smoke-test intent subset

Stage 2 should run on exactly 5 intents selected to cover the main risk dimensions of the benchmark. The 5 intents below are recommended:

| Intent | Category | Why this intent |
|---|---|---|
| **INT-004** Simple factual — refund destination | Simple (T1) | Directly tests the INT-004 TR terminology fix (QR9); covers D03 returns; simplest possible evaluation target; AC3 |
| **INT-015** Conditional — accidental-damage warranty exclusion | Conditional (T2) | Tests a condition-rule intent; covers D02 warranty + D07 repair cross-reference; INT-019 FAIL pattern risk |
| **INT-017** Conditional — subscription mid-period cancellation | Conditional (T3) | Tests subscription policy; covers D04; cancellation-window condition that is easy to get wrong |
| **INT-026** Process — add new Sensor (pairing sequence) | Process/troubleshooting (T4) | Tests an ordered multi-step sequence; covers D06; step-order requirement (IS5); moderate length |
| **INT-031** Process — Hub factory reset | Process/two-chunk (T5) | Tests the two-chunk retrieval requirement (D08-S3 + D08-S4); AC9 forward-reference test; highest retrieval complexity in the benchmark |

**Risk coverage:**
- INT-004: simple factual, lowest complexity, fastest to evaluate — validates the pipeline works before running harder cases
- INT-015: condition-rule failure mode — tests whether models fabricate warranty coverage for excluded damage types
- INT-017: subscription mid-period window — tests whether models confuse cancellation timing conditions
- INT-026: ordered pairing procedure — tests whether models omit or reorder steps
- INT-031: two-chunk span — tests whether Agent B retrieves both required chunks; if D08-S4 (containing F0807) is not retrieved, the answer is incomplete; also tests AC9 (single-source rule for F0807)

Together these five cover: all three intent difficulty levels; four different NiceHome documents (D03, D02/D07, D04, D06, D08); three of the five task skeletons (T1–T5); the AC3, AC7, and AC9 ambiguity controls; and the most challenging retrieval case in the benchmark.

---

## 10. Stage 2 success criteria

Stage 2 passes if all of the following hold:

| Criterion | Pass condition |
|---|---|
| Logging works | Every run produces a valid JSONL record with all required fields populated; no silent field-drop failures |
| Both agents run without pipeline failure | Agent A and Agent B both complete all 15 runs (5 intents × 3 languages) without exceptions or API errors; any pipeline failure is diagnosed and documented |
| Evaluator can classify all outputs | Project owner can assign PASS/FAIL/UNCERTAIN to every run output within reasonable time; no systematic "cannot evaluate" cases |
| Retrieval chunks captured for Agent B | `retrieved_chunk_ids` is populated for all 15 Agent B runs; at least the primary chunk for each intent is retrieved |
| Token/cost/latency fields captured | `input_tokens`, `output_tokens`, `total_tokens`, `estimated_cost_usd`, and `latency_ms` are present and plausible for all runs |
| No obvious language rendering defect | No run in any language condition produces an output that is clearly responding to a different intent or a garbled query — this would indicate a query or KB rendering error |
| No uncontrolled hidden context | No evidence that Agent A is producing correct answers from model knowledge rather than from the KB-in-context (evaluator watches for this; logs in `evaluator_notes`) |
| UNCERTAIN rate ≤ 25% in any single condition | If UNCERTAIN rate exceeds 25% in any language × agent condition, the evaluation instrument must be recalibrated before Stage 3 |

**Stage 2 does not need to show an execution-tax signal.** It is a pipeline validation exercise. A Stage 2 where all costs and token counts are logged correctly, all 30 outputs are classifiable, and Agent B correctly retrieves the right chunks is a fully successful Stage 2 — regardless of whether TR costs more than EN.

---

## 11. Stage 2 non-goals

Stage 2 explicitly does not aim to:

- **Prove execution-tax.** A 5-intent smoke test with no repetitions cannot support an execution-tax finding. Any observed pattern is exploratory only.
- **Run the full benchmark.** Stage 3 runs all 36 intents × 3 languages × 2 agents (108 instances, with repetitions if budget allows). Stage 2 runs 5 intents only.
- **Make public claims.** All Stage 2 results are internal exploratory. The Dutch rendering has not received native review; the tokenizer has not been re-run with exact tiktoken; Stage 2 results are not publication-grade.
- **Compare models.** Stage 2 uses exactly one model family (TM1 confirmed: GPT-4.1-mini/GPT-4.1). No model comparison is in scope.
- **Compare tokenizers.** v0.1 uses one tokenizer family (o200k_base). No tokenizer comparison is in scope.
- **Make optimization recommendations.** Stage 2 produces candidate pipeline validation data, not a basis for architectural recommendations.
- **Produce statistical power estimates.** Those are a Stage 3 deliverable (M8). Stage 2 is too small.

---

## 12. Optional exact-tokenizer rerun

Stage 1a used the `o200k_base_approx` fallback tokenizer because the network policy in the execution environment blocked access to `openaipublic.blob.core.windows.net`, where tiktoken downloads BPE data. The `stage1a_tokenizer_sanity_gate.py` script auto-detects tiktoken availability and switches to exact counts when the encoding loads successfully.

**This rerun does not block internal Stage 2 smoke testing.** The Stage 1a sanity gate is directional — it checks that token-tax ratios are in the expected range and direction. The approximate counts are sufficient for this purpose, and all sanity checks PASS.

**The exact-tokenizer rerun is required before:**
- Any public communication of absolute token counts
- Any publication-grade claim about token-tax multipliers for NL/EN or TR/EN
- Any Stage 3 final reporting where token-tax numbers appear as quantitative findings

**How to rerun:** run `python scripts/stage1a_tokenizer_sanity_gate.py` in a network-accessible environment (or a machine where tiktoken is already installed and cached). The script will log `TOKENIZER_RESOLUTION_NOTE` with "exact" rather than "FALLBACK" and produce authoritative counts in `results/stage1a/`. Results should be stored as `results/stage1a_exact/` to distinguish from the approximate run.

---

## 13. Open decisions table

| Decision ID | Decision | Confirmed value | Status | Owner | Blocks Stage 2? | Notes |
|---|---|---|---|---|---|---|
| **M9** | Instrumentation platform | Lightweight local JSONL/CSV logging; one record per run; minimum required fields from logging-schema; no external platform | **CONFIRMED 2026-06-14** | Project owner | No longer blocking | Langfuse / Arize Phoenix deferred to Stage 3 |
| **AD1** | Agent A context condition | A1 — Direct LLM with full relevant-language KB rendering in context | **CONFIRMED 2026-06-14** | Project owner | No longer blocking | A0 (no context) would fail fictional domain; A1 enables interpretable cost comparison; A0 deferred as optional Stage 3 floor check |
| **TM8** | Embedding model for Agent B | OpenAI `text-embedding-3-small`; same model across EN/NL/TR; log `embedding_model_id` + `embedding_model_version` | **CONFIRMED 2026-06-14** | Project owner | No longer blocking | Version-pinned; multilingual coverage confirmed |
| **EV1** | Human audit fraction | Audit all Stage 2 outputs manually (PASS, FAIL, UNCERTAIN); no sampling | **CONFIRMED 2026-06-14** | Project owner | No longer blocking | Stage 3 rule: all FAILs + all UNCERTAINs + ≥20% PASSes per condition |
| **TM5/BS6** | Pilot budget | $25 USD hard cap for Stage 2; stop-and-review at $20; cap must be implemented or manually enforced before any call | **CONFIRMED 2026-06-14** | Project owner | No longer blocking the decision; enforcement mechanism still required before first call | Estimated actual spend ~$5–10 at GPT-4.1-mini rates |
| TM1-a (optional) | Exact tiktoken rerun | Rerun in network-accessible environment before public claims | Optional for Stage 2; required before Stage 3 reporting | Project owner | NO | Script auto-detects tiktoken; results to `results/stage1a_exact/` |
| LR6 | Dutch native review | Deferred to pre-publication | Deferred | External reviewer | NO for internal Stage 2 | Dutch results carry WAIVED_WITH_LIMITATION label for public claims |
| TM1-b/c | Version-pinned model IDs for Agent A and B | Set at Stage 2 setup (e.g., `gpt-4.1-mini-2025-04-14`) | NOT_STARTED | Project owner | YES (must be set before first API call) | Never use "latest" alias; pin version before run; record in smoke-test run plan |
| TM1-d | GPT-4.1-mini vs. GPT-4.1 for Stage 3 | GPT-4.1-mini for Stage 2 and Stage 3 exploratory; upgrade to GPT-4.1 only if Stage 2 smoke test shows inadequate quality | NOT_STARTED | Settled by Stage 2 results | NO for Stage 2 | GPT-4.1-mini is the Stage 2 default |
| RUNNER | Minimal logging runner script | Implements JSONL logging, embedding + completion calls, budget enforcement | NOT_STARTED | Project owner | **YES — blocks first API call** | Must exist and be reviewed before Stage 2 runs |
| RUNPLAN | Smoke-test run plan | `stage2-smoke-test-run-plan.md`: prompt templates, KB indexing, run order, budget enforcement | NOT_STARTED | Project owner | **YES — blocks first API call** | Next artifact to create |

---

## 14. Next actions

Decisions 1–5 below are **CONFIRMED (2026-06-14)**. The remaining steps gate the first API call. **No API calls until the smoke-test run plan and logging runner exist, are reviewed, and the budget cap is implemented or manually enforced.**

1. **~~Confirm M9~~ — DONE (2026-06-14).** Lightweight local JSONL/CSV logging; one record per run; minimum required fields; no external platform.

2. **~~Confirm AD1~~ — DONE (2026-06-14).** A1 — Direct LLM with full relevant-language KB rendering in the Agent A prompt.

3. **~~Confirm TM8~~ — DONE (2026-06-14).** OpenAI `text-embedding-3-small`; same model across EN/NL/TR; log `embedding_model_id` + `embedding_model_version`.

4. **~~Confirm EV1~~ — DONE (2026-06-14).** Audit all Stage 2 outputs manually (PASS, FAIL, UNCERTAIN); no sampling.

5. **~~Confirm TM5/BS6~~ — DONE (2026-06-14).** $25 USD hard cap; stop-and-review at $20; cap must be implemented or manually enforced before any call.

6. **Create the Stage 2 smoke-test run plan** — **NEXT ARTIFACT.** `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` specifying: the 5 selected intents (INT-004, INT-015, INT-017, INT-026, INT-031), the prompt templates for Agent A (A1) and Agent B (Simple RAG), the KB indexing procedure for Agent B (embed 39 chunks × 3 languages with `text-embedding-3-small`), the retrieval top-k setting, the run order, the budget-enforcement mechanism, and the logging runner location.

7. **Set version-pinned model IDs (TM1-b/c)** — record exact completion and embedding model IDs (e.g., `gpt-4.1-mini-2025-04-14`, `text-embedding-3-small` snapshot) in the run plan and the `pricing_version` table before the first API call.

8. **Implement the minimal logging runner** — a Python script that: sends the query, calls the embedding model (Agent B), calls the completion model, enforces the budget cap, logs all required JSONL fields, and writes to `results/stage2/runs.jsonl`. The script should be deterministic (same query in = same API request; only the model response varies).

9. **Review the run plan and runner** — confirm both before any API call; verify the budget cap is enforced.

10. **Run Stage 2 smoke test** — execute 30 runs (5 intents × 3 languages × 2 agents, one pass); monitor cost against budget cap; stop if cost approaches $20.

11. **Evaluate all 30 outputs** — project owner reviews all outputs blind to cost/trajectory; assigns PASS/FAIL/UNCERTAIN + failure_type + evaluator_notes; checks UNCERTAIN rate per condition.

12. **Write Stage 2 results summary** — structured note covering: pipeline status (did logging work?), PASS/FAIL/UNCERTAIN distribution, retrieval quality (did Agent B retrieve the required chunks?), token/cost/latency ranges, any language rendering defects found, and go/no-go verdict for Stage 3.

13. **(Optional, not blocking Stage 2)** Re-run Stage 1a with exact tiktoken in a network-accessible environment; store results in `results/stage1a_exact/`.

---

*This document resolves the five decisions blocking Stage 2. All five are CONFIRMED by the project owner (2026-06-14). Stage 2 remains blocked on the smoke-test run plan and the logging runner; no API call may be made until both exist, are reviewed, and the budget cap is implemented or manually enforced. Version: s2-plan-v0.1.1.*
