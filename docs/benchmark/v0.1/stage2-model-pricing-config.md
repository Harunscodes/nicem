# Stage 2 Model and Pricing Configuration v0.1

**Version:** s2-model-pricing-v0.1.0
**Date:** 2026-06-14
**Status:** Configuration PENDING — all placeholders must be confirmed before the first live API call. This document does not authorize a live run.
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

| Field | Required value | Status |
|---|---|---|
| `response_model_id` | Version-pinned completion snapshot, e.g. `gpt-4.1-mini-2025-04-14` (never a "latest" alias) | **PLACEHOLDER** — `TO_CONFIRM_EXACT_MODEL_ID` |
| `embedding_model_id` | `text-embedding-3-small` | **CONFIRMED** (TM8, s2-plan-v0.1.1) |
| `embedding_model_version` | Exact embedding snapshot if provider exposes one | **PLACEHOLDER** — `TO_CONFIRM` |
| `tokenizer_name` | `o200k_base` | **CONFIRMED** (TM1, Stage 1a) |

### Notes on model ID requirements

- `response_model_id` must be a **version-pinned snapshot**, not a rolling alias. Example: `gpt-4.1-mini-2025-04-14`, not `gpt-4.1-mini`.
- A change to `response_model_id` between runs requires re-labeling all results that used the previous ID.
- `embedding_model_version` should be recorded if the provider exposes a snapshot identifier. If not exposed, record `"not-exposed-by-provider"` (not a placeholder).
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

**Current value:** `TO_CONFIRM_BEFORE_API_RUN` (placeholder)

Before the first API call, replace with the actual date the rates were verified from the provider's published pricing page, e.g. `openai-2026-06-14`.

### 3.2 Rate fields

All three of the following must be set (USD per 1,000 tokens) before live mode is permitted:

| Field | Units | Source | Current value |
|---|---|---|---|
| `pricing.completion_input_usd_per_1k` | USD / 1,000 input tokens | OpenAI published rates as of `pricing_version` | **None** (placeholder) |
| `pricing.completion_output_usd_per_1k` | USD / 1,000 output tokens | OpenAI published rates as of `pricing_version` | **None** (placeholder) |
| `pricing.embedding_usd_per_1k` | USD / 1,000 tokens embedded | OpenAI published rates as of `pricing_version` | **None** (placeholder) |

### 3.3 How to populate the pricing table

1. Go to the provider's published pricing page for GPT-4.1-mini and text-embedding-3-small.
2. Record the input, output, and embedding rates (USD per 1,000 tokens).
3. Set `pricing_version` to `openai-YYYY-MM-DD` where YYYY-MM-DD is today's date.
4. Update the three pricing fields in `CONFIG["pricing"]` in the runner.
5. Verify using the hand-calculation in §4.
6. Update this document to record the confirmed values and date.

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

### 4.3 Hand-calculation example (illustrative only — uses placeholder rates)

This example uses **illustrative rates** to verify the formula. These are NOT the confirmed rates. Replace with real rates when `pricing_version` is confirmed.

Illustrative rates (hypothetical):
- Input: $0.40 / 1M tokens = $0.0004 / 1K tokens
- Output: $1.60 / 1M tokens = $0.0016 / 1K tokens
- Embedding: $0.02 / 1M tokens = $0.000020 / 1K tokens

Scenario: Agent B run, INT-031-tr-B (highest complexity case)
- Estimated input tokens: 2,500 (system + full-KB context + query)
- Estimated output tokens: 300 (answer text)
- Estimated embedding tokens: 25 (query text for retrieval)

Calculation:
```
completion input:  (2500 / 1000) × 0.0004 = $0.001000
completion output: (300  / 1000) × 0.0016 = $0.000480
embedding:         (25   / 1000) × 0.00002 = $0.000001 (rounded)
------------------------------------------------------------
total:                                       $0.001481
```

Agent A run equivalent (no embedding, same input/output tokens):
```
completion input:  (2500 / 1000) × 0.0004 = $0.001000
completion output: (300  / 1000) × 0.0016 = $0.000480
------------------------------------------------------------
total:                                       $0.001480
```

30-run total (rough upper bound at these illustrative rates):
```
30 × $0.0015 ≈ $0.045 — well within the $25 hard cap.
```

The actual rates at confirmed `pricing_version` may differ. The hand-calculation must be redone with real rates before the first live run (manual approval checklist §8 item 5 in s2-live-readiness-v0.1.0).

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

In dry-run, `estimated_cost_usd = 0` and `pricing_version` remains the placeholder. This is correct and expected.

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

## 8. Confirmed values (to be filled before live run)

This table is empty until the project owner confirms values and updates this document:

| Field | Confirmed value | Confirmed date | Source |
|---|---|---|---|
| `response_model_id` | — | — | — |
| `embedding_model_version` | — | — | — |
| `pricing_version` | — | — | — |
| `completion_input_usd_per_1k` | — | — | — |
| `completion_output_usd_per_1k` | — | — | — |
| `embedding_usd_per_1k` | — | — | — |

---

## 9. Relation to live-run readiness

Blockers 1–3 in `stage2-live-run-readiness.md` (s2-live-readiness-v0.1.0 §2) are directly addressed by this document:

- **Blocker 1** (`response_model_id` is a placeholder) → resolved by confirming the value in §8 of this document and updating `CONFIG["response_model_id"]`.
- **Blocker 2** (`pricing_version` is a placeholder) → resolved by confirming the date-stamped identifier in §8.
- **Blocker 3** (pricing table is unset) → resolved by confirming all three rate fields in §8 and `CONFIG["pricing"]`.

Manual approval checklist items 1–5 (s2-live-readiness-v0.1.0 §8) map to this document:

| Checklist item | Reference |
|---|---|
| `response_model_id` set to version-pinned snapshot | §2 |
| `embedding_model_version` recorded | §2 |
| `pricing_version` set to date-stamped identifier | §3.1 |
| All three pricing fields populated | §3.2 |
| `estimate_cost_usd` verified against hand-calculation | §4.3 |

---

*This document records the model and pricing configuration for Stage 2. It does not authorize a live run. Live execution remains BLOCKED until all placeholders in §8 are confirmed and the full manual approval checklist in s2-live-readiness-v0.1.0 §8 is complete. Version: s2-model-pricing-v0.1.0.*
