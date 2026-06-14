# Stage 2 Model and Pricing Configuration v0.1

**Version:** s2-model-pricing-v0.1.1
**Date:** 2026-06-14
**Status:** Model IDs and pricing **CONFIRMED** from official OpenAI sources (2026-06-14). Live execution still BLOCKED (`allow_api_calls=False`; live call paths are unreachable stubs). This document does not authorize a live run.
**Depends on:** `stage2-decision-plan.md` (s2-plan-v0.1.1), `stage2-live-run-readiness.md` (s2-live-readiness-v0.1.0), `scripts/stage2_smoke_runner.py`
**Feeds into:** Manual approval checklist (s2-live-readiness-v0.1.0 §8) — items 1–5

---

## 1. Purpose

This document records the model IDs, tokenizer, pricing table, and cost estimation rules for the Stage 2 smoke test. It provides:

- The exact identifiers to be placed in `CONFIG` before a live run
- The `estimated_cost_usd` formula (for transparency and auditing)
- A hand-calculation example verifying the formula
- Rules for what changes invalidate a run or require re-labeling
- The relationship between estimated cost, budget guards, and logged cost

This document is a **configuration reference**. It does not contain live pricing values until those values are confirmed from the provider's published rates.

---

## 2. Model identifiers

| Field | Confirmed value | Status |
|---|---|---|
| `response_model_id` | `gpt-4.1-mini-2025-04-14` (version-pinned snapshot) | **CONFIRMED** (TM1-b/c, 2026-06-14) — reconfirm against live `/v1/models` at run time |
| `embedding_model_id` | `text-embedding-3-small` | **CONFIRMED** (TM8, s2-plan-v0.1.1) |
| `embedding_model_version` | `not-exposed-by-provider` (no dated snapshot for this embedding model) | **CONFIRMED** (recorded 2026-06-14) |
| `tokenizer_name` | `o200k_base` | **CONFIRMED** (TM1, Stage 1a) |

### Notes on model ID requirements

- `response_model_id` must be a **version-pinned snapshot**, not a rolling alias. The confirmed value `gpt-4.1-mini-2025-04-14` is the dated snapshot (not the `gpt-4.1-mini` rolling alias). It must be reconfirmed against the live `/v1/models` listing immediately before the first run (live-readiness item).
- A change to `response_model_id` between runs requires re-labeling all results that used the previous ID.
- `embedding_model_version` is recorded as `not-exposed-by-provider` because `text-embedding-3-small` does not publish a dated snapshot identifier. This is a confirmed value, not a placeholder.
- The tokenizer `o200k_base` is the encoding family for all GPT-4.1-mini/GPT-4.1 variants (confirmed in Stage 1a). This does not change with the completion model snapshot.

### Where these values appear in the runner

```
CONFIG["response_model_id"]       → logged in every run record
CONFIG["embedding_model_id"]      → logged in Agent B run records (None for Agent A)
CONFIG["embedding_model_version"] → referenced in the pricing_version confirmation
CONFIG["tokenizer_name"]          → logged in every run record
```

---

## 3. Pricing table

### 3.1 Pricing version

`pricing_version` is a date-stamped identifier recording which published rate table was used. Format: `openai-YYYY-MM-DD`.

**Confirmed value:** `openai-2026-06-14`

Verified on 2026-06-14 against OpenAI's official API pricing (developers.openai.com / openai.com/api/pricing). If the published rates change, bump `pricing_version` and re-record the table.

### 3.2 Rate fields

All three are CONFIRMED (USD per 1,000 tokens), converted from OpenAI's published USD-per-1M rates:

| Field | Confirmed value (USD/1K) | Published rate (USD/1M) | Source |
|---|---|---|---|
| `pricing.completion_input_usd_per_1k` | **0.00040** | $0.40 / 1M input | OpenAI API pricing, gpt-4.1-mini, 2026-06-14 |
| `pricing.completion_output_usd_per_1k` | **0.00160** | $1.60 / 1M output | OpenAI API pricing, gpt-4.1-mini, 2026-06-14 |
| `pricing.embedding_usd_per_1k` | **0.00002** | $0.02 / 1M | OpenAI API pricing, text-embedding-3-small, 2026-06-14 |

**Informational (not used in `estimate_cost_usd`):** gpt-4.1-mini cached input is **$0.10 / 1M = $0.00010 / 1K**. The Stage 2 estimator uses the standard (non-cached) input rate, which is conservative (higher) for budget purposes. If prompt caching is enabled in a future stage, add a `completion_cached_input_usd_per_1k` field and adjust the formula.

### 3.3 How the pricing table was populated (completed 2026-06-14)

1. Consulted OpenAI's official API pricing (developers.openai.com / openai.com/api/pricing) for gpt-4.1-mini and text-embedding-3-small.
2. Recorded input ($0.40/1M), output ($1.60/1M), and embedding ($0.02/1M) rates; converted to USD-per-1K.
3. Set `pricing_version = openai-2026-06-14` (verification date).
4. Updated the three pricing fields in `CONFIG["pricing"]` (via named constants — see §6 and the runner).
5. Verified with the hand-calculation in §4 and the runner self-test (§6).
6. Recorded the confirmed values in §8.

To refresh in the future (rates change, new model snapshot), repeat steps 1–6 and bump `pricing_version`.

---

## 4. Cost estimation formula

### 4.1 Formula

```
estimated_cost_usd =
    (input_tokens  / 1000.0) × completion_input_usd_per_1k
  + (output_tokens / 1000.0) × completion_output_usd_per_1k
  + (embedding_tokens / 1000.0) × embedding_usd_per_1k
```

For Agent A runs (no retrieval), `embedding_tokens = 0`.
For Agent B runs (RAG, uses retrieval), `embedding_tokens` = total tokens in the query text passed to the embedding API.

`estimated_cost_usd` is rounded to 6 decimal places. It is a **pre-run estimate** based on expected token counts, not a post-run billed amount. The billed amount will differ slightly; the estimate is for budget enforcement and logging only.

### 4.2 Where this is implemented

```python
# scripts/stage2_smoke_runner.py
def estimate_cost_usd(input_tokens, output_tokens, embedding_tokens=0):
    p = CONFIG["pricing"]
    cost  = (input_tokens  / 1000.0) * p["completion_input_usd_per_1k"]
    cost += (output_tokens / 1000.0) * p["completion_output_usd_per_1k"]
    cost += (embedding_tokens / 1000.0) * p["embedding_usd_per_1k"]
    return round(cost, 6)
```

The function raises `ValueError` if the pricing table is not configured. `pricing_configured()` returns `True` only when all three fields are real numbers.

### 4.3 Hand-calculation example (confirmed rates, `openai-2026-06-14`)

This example uses the **confirmed rates** from §3.2.

Confirmed rates (USD per 1K tokens):
- Input: $0.00040 (gpt-4.1-mini, $0.40/1M)
- Output: $0.00160 (gpt-4.1-mini, $1.60/1M)
- Embedding: $0.00002 (text-embedding-3-small, $0.02/1M)

Scenario: Agent B run, INT-031-tr-B (highest complexity case)
- Estimated input tokens: 2,500 (system + full-KB context + query)
- Estimated output tokens: 300 (answer text)
- Estimated embedding tokens: 25 (query text for retrieval)

Calculation:
```
completion input:  (2500 / 1000) × 0.00040 = $0.001000
completion output: (300  / 1000) × 0.00160 = $0.000480
embedding:         (25   / 1000) × 0.00002 = $0.0000005 → $0.000001 (round 6dp)
---------------------------------------------------------------
total:                                        ≈ $0.001481
```

Agent A run equivalent (no embedding, same input/output tokens):
```
completion input:  (2500 / 1000) × 0.00040 = $0.001000
completion output: (300  / 1000) × 0.00160 = $0.000480
---------------------------------------------------------------
total:                                        = $0.001480
```

30-run rough upper bound at confirmed rates (assuming ~$0.0015/run):
```
30 × $0.0015 ≈ $0.045 — far below the $25 hard cap and the $20 stop-review.
```

Actual token counts (and therefore cost) are measured per run at execution time. This estimate confirms the smoke test is comfortably within budget. The `estimate_cost_usd` implementation is independently verified by the runner self-test (§6).

---

## 5. How estimated cost is logged and enforced

### 5.1 In the run log

Each run record includes:
```json
{
  "estimated_cost_usd": 0.001481,
  "pricing_version": "openai-2026-06-14"
}
```

In dry-run, `estimated_cost_usd = 0` regardless of the (now confirmed) pricing table, because dry-run performs no API call and logs no token counts. `pricing_version` is `openai-2026-06-14`. This is correct and expected.

### 5.2 Budget enforcement (BudgetGuard)

The `BudgetGuard` class uses `estimated_cost_usd` for pre-run cost projection:

1. Before each run, compute `next_cost = estimate_cost_usd(input_tokens, output_tokens, embedding_tokens)`.
2. If `cumulative_cost + next_cost > $25.00` → **halt** (hard cap).
3. If `cumulative_cost + next_cost >= $20.00` → **pause** (stop-review; manual approval required).
4. Otherwise → proceed; after the run, call `guard.record(actual_cost)`.

State is written to `results/stage2/budget_state.json` after each run (live-only; not created in dry-run).

---

## 6. Pricing self-test

The runner includes a unit-style self-test for `estimate_cost_usd` using **synthetic pricing values** (not real rates, not requiring an API key). The test is run as part of the dry-run validation.

Self-test logic (see `_run_pricing_selftest()` in the runner):
- Temporarily configure synthetic rates: input=$0.001/1K, output=$0.002/1K, embedding=$0.0001/1K.
- Compute `estimate_cost_usd(1000, 500, 200)`.
- Expected: `(1.0 × 0.001) + (0.5 × 0.002) + (0.2 × 0.0001) = 0.001 + 0.001 + 0.00002 = 0.00202`.
- Assert result == `0.00202` (to 5 decimal places).
- Restore the original pricing table (None values) after the test.

The self-test PASS/FAIL appears in the dry-run validation report. It verifies the formula implementation, not the pricing values.

---

## 7. What changes require re-running or re-labeling

| Change | Effect |
|---|---|
| `response_model_id` changes | All runs using the old model ID must be re-labeled with the new ID. Re-run if cross-model comparison is needed. |
| `pricing_version` changes | Update `pricing_version` in CONFIG and in this document. Past cost estimates do not change (they are logged per-run). |
| Any pricing rate changes | Update `pricing_version`. Past records retain their original estimates. |
| `embedding_model_id` changes | Re-run all Agent B runs (retrieval results may differ). Re-label. |
| Tokenizer changes | Stage 1a results are invalidated; full re-run required. |
| KB rendering changes | All runs against that language are invalidated. Re-run with the new KB version. |

A change that invalidates past results must be documented in the run log (`evaluator_notes`) and in `stage2-smoke-test-run-plan.md`.

---

## 8. Confirmed values (verified 2026-06-14)

| Field | Confirmed value | Confirmed date | Source |
|---|---|---|---|
| `response_model_id` | `gpt-4.1-mini-2025-04-14` | 2026-06-14 | OpenAI API docs (model snapshot listing) — reconfirm against live `/v1/models` at run time |
| `embedding_model_version` | `not-exposed-by-provider` | 2026-06-14 | text-embedding-3-small publishes no dated snapshot |
| `pricing_version` | `openai-2026-06-14` | 2026-06-14 | OpenAI API pricing (developers.openai.com / openai.com/api/pricing) |
| `completion_input_usd_per_1k` | `0.00040` ($0.40/1M) | 2026-06-14 | OpenAI API pricing, gpt-4.1-mini |
| `completion_output_usd_per_1k` | `0.00160` ($1.60/1M) | 2026-06-14 | OpenAI API pricing, gpt-4.1-mini |
| `embedding_usd_per_1k` | `0.00002` ($0.02/1M) | 2026-06-14 | OpenAI API pricing, text-embedding-3-small |

**Informational:** gpt-4.1-mini cached input = `0.00010` ($0.10/1M), 2026-06-14. Not used by `estimate_cost_usd` (the estimator uses the standard input rate, which is conservative for budgeting).

**Remaining live-readiness item:** reconfirm `gpt-4.1-mini-2025-04-14` is still an available, non-deprecated snapshot against the live `/v1/models` endpoint immediately before the first run, and re-verify the published rates have not changed (bump `pricing_version` if they have).

---

## 9. Relation to live-run readiness

Blockers 1–3 in `stage2-live-run-readiness.md` (s2-live-readiness-v0.1.0 §2) are now **RESOLVED** by this document:

- **Blocker 1** (`response_model_id` placeholder) → **RESOLVED**: `gpt-4.1-mini-2025-04-14` confirmed in §8 and set in `CONFIG["response_model_id"]`. (Reconfirm against live `/v1/models` at run time.)
- **Blocker 2** (`pricing_version` placeholder) → **RESOLVED**: `openai-2026-06-14` confirmed in §8.
- **Blocker 3** (pricing table unset) → **RESOLVED**: all three rate fields confirmed in §8 and set in `CONFIG["pricing"]`.

Manual approval checklist items 1–5 (s2-live-readiness-v0.1.0 §8) — status:

| Checklist item | Reference | Status |
|---|---|---|
| `response_model_id` set to version-pinned snapshot | §2 | DONE (reconfirm at run time) |
| `embedding_model_version` recorded | §2 | DONE (`not-exposed-by-provider`) |
| `pricing_version` set to date-stamped identifier | §3.1 | DONE |
| All three pricing fields populated | §3.2 | DONE |
| `estimate_cost_usd` verified against hand-calculation | §4.3, §6 | DONE (hand-calc + runner self-test PASS) |

Remaining live-readiness blockers (still open): live completion + embedding paths (stubs), `BudgetGuard` wired into the live loop, `allow_api_calls=True` after review, `OPENAI_API_KEY` in the environment, and `--live --confirm-spend` flags.

---

*This document records the confirmed model and pricing configuration for Stage 2. It does not authorize a live run. Live execution remains BLOCKED until the remaining live-readiness blockers in s2-live-readiness-v0.1.0 §2 are resolved, the manual approval checklist in §8 is complete, and `allow_api_calls=True` is set after review. Version: s2-model-pricing-v0.1.1.*
