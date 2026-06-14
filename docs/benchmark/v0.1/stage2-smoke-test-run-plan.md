# Stage 2 Smoke-Test Run Plan v0.1

**Version:** s2-runplan-v0.1.0
**Date:** 2026-06-14
**Status:** DRAFT — defines the first API-backed smoke test; does NOT start it. Stage 2 remains BLOCKED until the logging runner exists and is reviewed.
**Depends on:** `stage2-decision-plan.md` (s2-plan-v0.1.1, all five decisions CONFIRMED), `quality-gates.md`, `logging-schema-v0.1.md`, `expected-fact-mapping.md`, `intent-set.md`, `kb-rendering-{en,nl,tr}.md`, `query-rendering-{en,nl,tr}.md`, `evaluation-method-v0.1.md`
**Feeds into:** the minimal logging runner implementation, then the Stage 2 smoke-test execution

---

## 1. Purpose

This plan defines the first API-backed smoke test for NiceM v0.1 in full operational detail — the intents, the run matrix, the prompts, the retrieval procedure, the logging fields, the budget enforcement, and the pass/fail criteria. **It does not start the smoke test.** No API call, no embedding, and no run is triggered by this document.

What Stage 2 is:
- A test of the **pipeline**: that a query can be sent, a response received, retrieval performed (Agent B), and a complete log record written.
- A test of **logging**: that every required field is captured correctly for every run.
- A test of **retrieval**: that Agent B retrieves the correct language-matched KB chunks for each intent.
- A test of **prompting**: that Agent A (full-KB-in-context) and Agent B (retrieval) are comparable and that neither leaks hidden model knowledge.
- A test of the **evaluation flow**: that the project owner can classify every output as PASS / FAIL / UNCERTAIN against `expected-fact-mapping.md`.

What Stage 2 is **not**:
- It does **not** prove execution-tax. Execution-tax remains a hypothesis. A 5-intent smoke test with one run per condition cannot support any execution-tax finding.
- It does **not** produce public claims. All Stage 2 results are internal and exploratory.
- It is a check of whether the benchmark **can be executed safely and reproducibly** — nothing more.

---

## 2. Current readiness

| Item | Status |
|---|---|
| Stage 1a tokenizer-only sanity gate | **PASS** (2026-06-13; results in `results/stage1a/`) |
| M9 — instrumentation | **CONFIRMED** — lightweight local JSONL/CSV logging |
| AD1 — Agent A context | **CONFIRMED** — A1 (full relevant-language KB rendering in prompt) |
| TM8 — embedding model | **CONFIRMED** — OpenAI `text-embedding-3-small` |
| EV1 — audit fraction | **CONFIRMED** — audit all Stage 2 outputs manually |
| TM5/BS6 — budget | **CONFIRMED** — $25 hard cap; stop-and-review at $20 |
| Minimal logging runner | **NOT IMPLEMENTED** — blocks first API call |
| Runner review | **NOT DONE** — blocks first API call |
| Version-pinned model IDs (TM1-b/c) | **NOT SET** — must be recorded before first API call |
| `pricing_version` | **NOT SET** — must be recorded before first API call |

**Stage 2 is still BLOCKED.** The five decisions are confirmed, but no API call may run until: (1) the minimal logging runner is implemented and reviewed; (2) the exact response model ID and `pricing_version` are recorded; and (3) the budget cap is implemented or manually enforced. No API calls yet. No embeddings yet.

---

## 3. Scope

| Dimension | Value |
|---|---|
| Selected intents | 5 (INT-004, INT-015, INT-017, INT-026, INT-031) |
| Languages | 3 (en, nl, tr) |
| Agent designs | 2 (Agent A = Direct LLM with full KB in context; Agent B = Simple RAG) |
| Runs per condition (initial) | 1 |
| **Total planned base runs** | **5 × 3 × 2 = 30** |
| Repeats | None, unless a pipeline/logging failure occurs (re-run only the failed condition) |
| Output audit | All 30 outputs manually audited (EV1) |

This is a smoke test, not a full benchmark. No repetitions for variance estimation are included; variance estimation is a Stage 3 deliverable (M8). If a run fails for a pipeline or logging reason (not a model-quality reason), that single condition is re-run; the re-run is logged with an incremented `retry_count` or a distinct `run_id`, and the failure is documented.

---

## 4. Selected intents

The five intents below are confirmed in `stage2-decision-plan.md` §9. Linked facts and chunks are taken from `intent-set.md` and `expected-fact-mapping.md`.

### INT-004 — Refund payment method (simple factual)
- **Reason selected:** Simplest possible evaluation target; validates the pipeline on a clean, single-fact, zero-condition intent before harder cases. Also exercises the INT-004 TR terminology fix from QR9 ("para iadem").
- **Linked facts:** F0307 (required)
- **Linked chunks:** D03-S4
- **Risk tested:** Baseline pipeline correctness; does the model answer "original payment method" without inventing store-credit or alternative-account claims?
- **Evaluation notes:** Binary — "original payment method" = PASS. Store credit / arbitrary bank account / cash = FAIL.

### INT-015 — Warranty coverage: accidental damage (conditional)
- **Reason selected:** Tests a rule + exception pattern (F0202 general coverage vs. F0203 accidental-damage exclusion); a common failure mode is applying the general rule without the exception.
- **Linked facts:** F0202, F0203 (F0203 required)
- **Linked chunks:** D02-S2, D02-S3
- **Risk tested:** Does the model correctly apply the exclusion (accidental damage NOT covered) rather than the general coverage rule? Tests condition handling.
- **Evaluation notes:** Must state accidental damage is excluded = PASS. Mentioning the out-of-warranty service quote (D07/F0708) is acceptable additional info. Claiming coverage = FAIL.

### INT-017 — Subscription mid-period cancellation (conditional, two-part output)
- **Reason selected:** Tests a two-part answer where both components matter; a partial answer is first-class UNCERTAIN. Exercises the evaluator's partial-answer rule.
- **Linked facts:** F0407, F0408 (both required)
- **Linked chunks:** D04-S5
- **Risk tested:** Does the model give BOTH (1) access continues to end of billing period AND (2) no pro-rated refund? Tests multi-fact completeness and the UNCERTAIN path.
- **Evaluation notes:** Both components required for PASS. Missing one = UNCERTAIN. "Access ends immediately" or "partial refund issued" = FAIL.

### INT-026 — Add new Sensor / pairing sequence (troubleshooting-process)
- **Reason selected:** Tests an ordered multi-step procedure and the AC2 ambiguity control (5-second pairing hold vs. 10-second factory-reset hold).
- **Linked facts:** F0606, F0607, F0608 (all required)
- **Linked chunks:** D06-S3
- **Risk tested:** Does the model give all three steps in causal order, and specifically "5 seconds" (not 10)? Tests ordered-step handling and AC2 discrimination.
- **Evaluation notes:** Three ordered steps required; "5 seconds" specifically required; 10 seconds = FAIL (AC2 violation).

### INT-031 — Hub factory reset + post-reset step (troubleshooting-process, AC9 two-chunk)
- **Reason selected:** The highest retrieval complexity in the benchmark — the answer spans two chunks (D08-S3 + D08-S4). Tests whether Agent B retrieves both required chunks. Also tests AC2 (10-second factory reset vs. 5-second pairing) and the AC9 forward-reference rule for F0807.
- **Linked facts:** F0806, F0807 (both required)
- **Linked chunks:** D08-S3, D08-S4
- **Risk tested:** Does Agent B retrieve **both** chunks? If only D08-S3 is retrieved, the re-pair requirement (F0807, in D08-S4) is missing and the answer is incomplete. Tests two-chunk retrieval, AC2 (10 seconds), and re-pair requirement.
- **Evaluation notes:** "10 seconds" specifically required; re-pair requirement must be mentioned = PASS. 5 seconds = FAIL. Missing re-pair = FAIL or UNCERTAIN depending on completeness. For Agent B, log whether both chunks were retrieved (key diagnostic).

**Coverage across the five:** all three difficulty levels (simple / conditional / process); five different documents (D03, D02, D04, D06, D08); AC2 (twice, in opposite directions) and AC9; the two-part-answer UNCERTAIN path; and the most demanding retrieval case in the benchmark.

---

## 5. Run matrix

- **Languages:** en, nl, tr
- **Agents:**
  - **Agent A** — Direct LLM with the full relevant-language KB rendering in the prompt (AD1 = A1). No retrieval.
  - **Agent B** — Simple RAG over the same-language KB chunks; retrieves top-k chunks; answers from retrieved chunks only.
- **Total runs:** 30

| Intent | en × A | en × B | nl × A | nl × B | tr × A | tr × B | Subtotal |
|---|---|---|---|---|---|---|---|
| INT-004 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| INT-015 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| INT-017 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| INT-026 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| INT-031 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| **Total** | 5 | 5 | 5 | 5 | 5 | 5 | **30** |

Each cell is one run = one `run_id`. The query text for each (intent × language) comes from `query-rendering-{en,nl,tr}.md`; both agents receive the same query for a given (intent × language) cell.

---

## 6. Model IDs and version pinning

Placeholders — **all must be replaced with exact values and recorded before the first API call:**

| Field | Value |
|---|---|
| `response_model_id` | `TO_CONFIRM_EXACT_OPENAI_MODEL_ID` — recommended default: `gpt-4.1-mini` with an exact dated snapshot if the provider exposes one (e.g., `gpt-4.1-mini-YYYY-MM-DD`); never a "latest" alias |
| `embedding_model_id` | `text-embedding-3-small` (CONFIRMED, TM8); record the exact snapshot/version if exposed |
| `embedding_model_version` | `TO_CONFIRM` — snapshot identifier if the provider exposes one |
| `tokenizer_name` | `o200k_base` (target encoding for the GPT-4.1 family); the Stage 1a fallback `o200k_base_approx` is noted separately and applies only to the Stage 1a counts, not to Stage 2 provider-reported token usage |
| `pricing_version` | `TO_CONFIRM_BEFORE_RUN` — date-stamped price table (e.g., `openai-2026-06-14`) covering both the completion and embedding model rates |

**Exact model IDs and `pricing_version` must be recorded in this plan (or the runner config) before the first API call.** Stage 2 token counts come from the provider API (`input_tokens` / `output_tokens`), not from the Stage 1a fallback tokenizer. The `tokenizer_name` field documents the encoding family for traceability.

---

## 7. Prompting plan for Agent A

Agent A is the Direct LLM baseline with full context (AD1 = A1). For each run, Agent A receives:

1. **System instruction** — defines the role: a product-support assistant answering strictly from a provided knowledge base.
2. **The full relevant-language KB rendering** — all 39 section chunks of `kb-rendering-{lang}.md`, in the same language as the query, with metadata blocks (chunk_id / fact_ids) **stripped** so only the prose is in context (per `language-rendering-plan.md` §3).
3. **The user query** — from `query-rendering-{lang}.md`, in the same language.
4. **Answer-only-from-KB instruction** — the model must answer using only the provided KB content.
5. **"Not in KB" instruction** — if the KB does not contain the answer, the model must say so explicitly rather than guess.
6. **No retrieval** — Agent A performs zero retrieval calls; `retrieval_calls = 0`; `retrieved_chunk_ids = null`.

**Agent A must not rely on hidden model knowledge.** Because the NiceHome domain is fictional, any correct answer must come from the in-context KB, not from pretraining. The evaluator watches for outputs that appear to use facts not present in the provided KB and logs them in `evaluator_notes` as a possible hidden-context leak.

The Agent A prompt is long (the full KB ≈ 4,000–8,000 tokens per language). The full assembled prompt token count is captured via `input_tokens`; the `prompt_version` field pins the template so the run is reproducible.

---

## 8. Prompting and retrieval plan for Agent B

Agent B is Simple RAG. For each run, Agent B:

1. **Indexes the same-language KB chunks** — the 39 section chunks from `kb-rendering-{lang}.md` (see §9).
2. **Embeds chunks** with `text-embedding-3-small` (one-time per language at index build; not per run).
3. **Embeds the user query** in the same language with the same embedding model.
4. **Retrieves top-k chunks** by cosine similarity. **Recommended `top_k`: 3.** The same `top_k` is used for all languages and all intents.
5. **Passes the retrieved chunks** (prose only; metadata stripped) to the response model alongside the query.
6. **Logs** `retrieved_chunk_ids`, `retrieved_fact_ids` (derived from chunk metadata), and `retrieval_scores` if the embedding response exposes them.
7. **Answers from retrieved chunks only** — same answer-only-from-context and "not in retrieved content" instructions as Agent A, scoped to the retrieved chunks rather than the full KB.

**Language-matched retrieval only in v0.1** — each language condition retrieves from its own same-language KB rendering. Cross-language / multilingual-neutral retrieval is the pre-registered v0.2 contrast condition (`retrieval-design-decision-v0.1.md`), not in Stage 2 scope.

Note on INT-031: with `top_k = 3`, Agent B must retrieve both D08-S3 and D08-S4 to answer completely. Whether it does is a key Stage 2 diagnostic recorded in `retrieval-diagnostics.md`.

---

## 9. KB indexing plan

- **Index structure:** one index per language, **or** one index with a `language` filter applied at query time — either is acceptable provided retrieval is strictly language-matched (a query never retrieves a chunk from a different language).
- **Chunks:** the 39 section chunks from `kb-rendering-{en,nl,tr}.md` (39 per language, 117 total).
- **Metadata per chunk:** `language`, `document_id`, `chunk_id`, `fact_ids`.
- **Metadata handling:** metadata is logged and used to derive `retrieved_fact_ids`, but it is **not** counted as user-facing KB prose and **not** included in the text sent to the response model (metadata blocks stripped before the prose is embedded or passed to the model), consistent with `language-rendering-plan.md` §3.
- **Determinism:** the index is built once and reused across all Agent B runs in a smoke-test session; the same query embedded twice should return the same top-k ranking.

---

## 10. Budget enforcement

| Parameter | Value |
|---|---|
| Hard cap | **$25 USD** |
| Stop-and-review threshold | **$20 USD** |
| Estimated spend | $5–10 USD (≈ $0.03–0.09/run Agent A long-context; ≈ $0.006–0.018/run Agent B; embeddings negligible) |
| Automatic retries | None, except a single re-run on a pipeline/logging failure (not a model-quality failure) |

- If cost tracking is approximate (estimated from token counts × `pricing_version` rates rather than provider-reported billing), a **manual cost review after each batch is required** before continuing.
- **The runner must enforce the cap** — either a programmatic running-cost ceiling that halts before exceeding $25, or a documented manual-enforcement procedure where the operator checks accumulated `estimated_cost_usd` after each batch and halts at $20.
- The run order (§11) is designed to allow an **early stop** after the first few multilingual rows if cost or logging behaves unexpectedly, so the cap is never approached blindly.

---

## 11. Recommended run order

To reduce risk before the full 30-run smoke test:

1. **Dry-run the parser and logging with no API.** Confirm the runner reads the queries, assembles prompts, and writes a complete JSONL record using mock/stub responses — zero API calls. (This validates the log schema before any spend.)
2. **One English Agent A run** (e.g., INT-004 × en × A). Confirm a real completion call logs all required fields and `estimated_cost_usd` is plausible.
3. **One English Agent B run** (INT-004 × en × B). Confirm retrieval works, `retrieved_chunk_ids` and scores are captured, and the response uses retrieved content.
4. **One full intent across all languages and both agents** (e.g., INT-004 × {en,nl,tr} × {A,B} = 6 runs). Confirm language-matched retrieval and per-language logging.
5. **Remaining four intents** (INT-015, INT-017, INT-026, INT-031 × 3 languages × 2 agents = 24 runs) only if the logs from steps 1–4 are correct.

This staged order means an early defect (bad log schema, broken retrieval, cost surprise) is caught after 1–6 runs, not after 30.

---

## 12. Logging requirements

Each run writes one JSONL record (M9: local JSONL/CSV). Required Stage 2 fields:

| Field | Notes |
|---|---|
| `run_id` | Unique per run (e.g., `S2-INT004-en-A-001`) |
| `timestamp` | ISO-8601 UTC at run start |
| `benchmark_version` | The frozen/working benchmark version identifier |
| `stage` | `stage2_smoke_test` |
| `intent_id` | e.g., `INT-004` |
| `language` | `en` / `nl` / `tr` |
| `query_text` | Exact query sent (from query-rendering files) |
| `agent_design_id` | `A` or `B` |
| `response_model_id` | Version-pinned completion model ID |
| `embedding_model_id` | `text-embedding-3-small` for Agent B; `null` for Agent A |
| `tokenizer_name` | `o200k_base` (encoding family for traceability) |
| `prompt_version` | Prompt template version |
| `kb_version` | KB rendering version used |
| `retrieved_chunk_ids` | List for Agent B; `null` for Agent A |
| `retrieved_fact_ids` | Derived from retrieved chunk metadata; `null` for Agent A |
| `retrieval_scores` | Per-chunk similarity scores if available; else `null` |
| `input_tokens` | Provider-reported |
| `output_tokens` | Provider-reported |
| `total_tokens` | `input_tokens + output_tokens` |
| `model_calls` | ≥1 |
| `retrieval_calls` | Embedding/retrieval calls; `0` for Agent A |
| `retry_count` | `0` on a clean first pass |
| `latency_ms` | Wall-clock query→response |
| `estimated_cost_usd` | From `pricing_version` token rates |
| `endpoint_outcome` | `PASS` / `FAIL` / `UNCERTAIN` — assigned by evaluator after the run, blind to cost/trajectory |
| `failure_type` | From the nine failure types (`success-rubric-v0.1.md`); `null` if PASS |
| `evaluator_notes` | Free text; required for every UNCERTAIN |
| `raw_output_path` | Path to the stored full model output |

(`pricing_version` and `embedding_model_version` are also recorded — at the run-config level if constant across the session, or per record if they may vary.)

---

## 13. Evaluation plan

- **All 30 outputs are audited manually** (EV1). PASS / FAIL / UNCERTAIN only.
- **`expected-fact-mapping.md` is the evaluation reference** — the authoritative per-intent PASS/FAIL/UNCERTAIN criteria, forbidden claims, and ordered-step rules.
- **No LLM-as-judge as the final evaluator** in Stage 2. (LLM-as-judge may be used for triage only, never as the source of truth — `evaluation-method-v0.1.md` §7.)
- **Blind to cost/trajectory:** the evaluator sees the model output and the expected fact mapping, not the token/cost/latency data.
- **Evaluator notes recorded for every run**, mandatory for every UNCERTAIN.
- **If the evaluator cannot classify reliably, mark UNCERTAIN and document why.** UNCERTAIN is first-class.
- **Language handling:** Turkish outputs reviewed by the project owner (native speaker); Dutch outputs reviewed by the project owner for factual accuracy against the language-neutral expected fact mapping (phrasing review deferred to the LR6 independent reviewer for any public claim).
- **Recalibration gate:** if UNCERTAIN rate exceeds 25% in any single condition (language × agent), the evaluation instrument must be recalibrated before Stage 3 (`falsification-and-decision-rules-v0.1.md` §7).

---

## 14. Stage 2 pass/fail criteria

**Stage 2 passes if all of the following hold:**
- All 30 runs complete, **or** a documented stop occurs (e.g., budget or logging halt with a clear record).
- Logs contain all required fields (§12) for every completed run.
- Agent B retrieval chunks are captured (`retrieved_chunk_ids` populated for all Agent B runs).
- The evaluator can classify every output (PASS / FAIL / UNCERTAIN).
- The budget cap is respected (no spend beyond $25; stop-and-review honored at $20).
- No hidden-context leak is observed (no Agent A output relies on facts absent from the provided KB).
- No query/KB artifact defect is discovered (no run reveals a broken rendering or mismatched query).

**Stage 2 fails or pauses if any of the following occur:**
- The budget cap cannot be enforced.
- Logs are incomplete (required fields missing or null where a value is expected).
- Retrieval metadata is missing for Agent B.
- The model uses unsupported facts (facts not in the KB / retrieved chunks).
- Agent A and Agent B prompts are not comparable (a confound is introduced).
- A language artifact defect appears (a rendering or query error surfaces during runs).
- Cost exceeds the stop-and-review threshold ($20) before completion.

Stage 2 passing means **the instrument works** — not that execution-tax exists. No execution-tax conclusion is drawn from Stage 2.

---

## 15. Outputs to create later

These are produced **after** the actual Stage 2 run (not by this plan):

- `results/stage2/runs.jsonl` — one record per run (primary log)
- `results/stage2/runs.csv` — tabular export of the JSONL for inspection
- `results/stage2/manual-audit.md` — per-run PASS/FAIL/UNCERTAIN with evaluator notes
- `results/stage2/stage2-smoke-test-summary.md` — pipeline status, outcome distribution, token/cost/latency ranges, defects found, go/no-go verdict for Stage 3
- `results/stage2/retrieval-diagnostics.md` — Agent B retrieval analysis (did the required chunks get retrieved? especially INT-031's two-chunk case)

---

## 16. Non-goals

Stage 2 explicitly does **not**:
- Run the full benchmark (Stage 3 = all 36 intents × 3 languages × 2 agents).
- Prove execution-tax.
- Produce public claims.
- Compare models (one model family only — TM1 confirmed).
- Add an optimizer or recommendation layer.
- Use query variants (Stage 1b / variant plan, deferred).
- Use cross-language / multilingual-neutral retrieval (pre-registered v0.2 contrast).

---

## 17. Open risks

- **Exact response model ID** still needs confirmation before the run (TM1-b/c).
- **`pricing_version`** must be recorded before the run, covering both completion and embedding rates.
- **Exact tokenizer fallback** (Stage 1a used `o200k_base_approx`) should be re-run eventually for publication-grade counts; not a Stage 2 blocker.
- **Embedding retrieval quality is unknown** before the test — `text-embedding-3-small` multilingual retrieval precision for NL/TR is unverified on this KB; the INT-031 two-chunk case is the stress test.
- **Agent A full-KB prompt may be long** (≈4,000–8,000 tokens/language) and dominates cost; `input_tokens` must be logged so this is visible.
- **Agent B `top_k` may be too small or too large** — `top_k = 3` is a starting value; if INT-031 fails to retrieve both required chunks, `top_k` may need adjustment (and that change must be logged and applied uniformly across languages).
- **Manual audit consistency is single-evaluator only** — all Stage 2 results carry the "single-evaluator exploratory pilot; independent review pending" label.

---

## 18. Next actions

1. **Confirm the exact response model ID** (TM1-b/c) — record the version-pinned `gpt-4.1-mini` snapshot.
2. **Confirm the `pricing_version`** — date-stamped rate table for completion + embedding models.
3. **Implement the minimal local logging runner** — assembles prompts, calls the embedding + completion models, enforces the budget cap, writes the §12 JSONL record.
4. **Dry-run the parser and log schema without API** (run-order step 1) — validate the schema using stub responses, zero API calls.
5. **Review the runner before the first API call** — confirm budget enforcement, field completeness, prompt comparability.
6. **Run the first two API calls only after review** (run-order steps 2–3), then proceed through the staged order if logs are correct.

---

*This document defines the Stage 2 smoke-test run plan. It does not start Stage 2. The smoke test may begin only after the minimal logging runner is implemented and reviewed, the exact model ID and `pricing_version` are recorded, and the budget cap is implemented or manually enforced. Version: s2-runplan-v0.1.0.*
