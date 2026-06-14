# Stage 2 Live-Run Readiness v0.1

**Version:** s2-live-readiness-v0.1.0
**Date:** 2026-06-14
**Status:** Dry-run PASS; **live execution BLOCKED.** This document defines the conditions, guards, and approval steps required before the first Stage 2 API call. It does not authorize a live run.
**Depends on:** `stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0), `stage2-decision-plan.md` (s2-plan-v0.1.1), `scripts/stage2_smoke_runner.py`, `logging-schema-v0.1.md`
**Feeds into:** the final manual approval step before live Stage 2 execution

---

## 1. Current status

| Item | Status |
|---|---|
| Stage 2 decisions (M9, AD1, TM8, EV1, TM5/BS6) | **CONFIRMED** (2026-06-14) |
| Stage 2 smoke-test run plan | **COMPLETE** (s2-runplan-v0.1.0) |
| Logging runner — dry-run skeleton | **PASS** — `scripts/stage2_smoke_runner.py`; 30 runs, all required fields, $0 cost, no API key |
| Live-mode scaffolding (guards, pricing, budget) | **IMPLEMENTED** — refuses to run by default |
| Live completion + embedding paths | **NOT IMPLEMENTED** — unreachable stubs |
| Live execution | **BLOCKED** |

Stage 2 cannot run live from the current runner. The live call paths are unreachable stubs (`_call_completion_api`, `_create_embeddings`) that raise `NotImplementedError`, and the strict live-mode guard refuses to proceed until every precondition in §6 is satisfied.

---

## 2. Exact blockers before the first API call

All of the following must be resolved (and reviewed) before any live run:

1. **`response_model_id`** is still the placeholder `TO_CONFIRM_EXACT_MODEL_ID` (TM1-b/c). Must be a version-pinned snapshot.
2. **`pricing_version`** is still the placeholder `TO_CONFIRM_BEFORE_API_RUN`. Must be a date-stamped rate-table identifier.
3. **Pricing table** (`completion_input_usd_per_1k`, `completion_output_usd_per_1k`, `embedding_usd_per_1k`) is unset (all `None`). Must be configured with real rates.
4. **Live call paths** are unimplemented stubs. The completion and embedding functions must be implemented and reviewed.
5. **Programmatic budget enforcement** must be wired into the run loop (the `BudgetGuard` class exists but is not yet exercised by a live loop).
6. **`allow_api_calls`** is `False`. Must be explicitly set to `True` — only after review.
7. **`OPENAI_API_KEY`** must be present in the environment at run time (never required for dry-run/review).
8. **CLI confirmation flags** `--live` and `--confirm-spend` must both be passed.

---

## 3. Required model IDs

| Field | Required value | Current |
|---|---|---|
| `response_model_id` | Version-pinned completion model, e.g. `gpt-4.1-mini-YYYY-MM-DD` (never a "latest" alias) | `TO_CONFIRM_EXACT_MODEL_ID` |
| `embedding_model_id` | `text-embedding-3-small` (CONFIRMED, TM8) | `text-embedding-3-small` |
| `embedding_model_version` | Exact embedding snapshot if the provider exposes one | `TO_CONFIRM` |
| `tokenizer_name` | `o200k_base` (encoding family, for traceability) | `o200k_base` |

The exact model IDs must be recorded in the runner `CONFIG` and in `stage2-smoke-test-run-plan.md` §6 before the run.

---

## 4. Required pricing_version

- **`pricing_version`** must be a date-stamped identifier covering both the completion and embedding model rates, e.g. `openai-2026-06-14`.
- The pricing table fields below must all be set (USD per 1,000 tokens), sourced from the provider's published rates as of `pricing_version`:
  - `pricing.completion_input_usd_per_1k`
  - `pricing.completion_output_usd_per_1k`
  - `pricing.embedding_usd_per_1k`
- The runner's `pricing_configured()` helper returns `True` only when all three are real numbers. Live mode is refused while any is `None`.

---

## 5. Budget enforcement design

| Parameter | Value |
|---|---|
| Hard cap | **$25.00** (CONFIRMED, TM5/BS6) |
| Stop-and-review threshold | **$20.00** |
| Estimated total spend | $5–10 |

Mechanism (implemented as `BudgetGuard` in the runner; exercised only in a live loop):
- **Pre-run estimate:** before each run, the projected cumulative cost (`cumulative_cost + next_cost`) is computed via `estimate_cost_usd(...)`.
- **Hard-cap halt:** if the projected cost would exceed **$25**, the run is refused and the loop halts (`status = halt_hard_cap`).
- **Stop-review pause:** if the projected cost reaches **$20**, the loop pauses and requires explicit manual approval before continuing (`status = pause_stop_review`).
- **State persistence:** cumulative cost, run count, thresholds, status, and timestamp are written to `results/stage2/budget_state.json` after each recorded run.
- **No auto-retry:** a failed API call is never automatically retried. Any retry requires explicit human approval and is logged with an incremented `retry_count`.

`budget_state.json` is a **live-run artifact only** — it is not created in dry-run mode (dry-run performs no spend).

---

## 6. API safety guards (strict live-mode refusal)

`can_run_api_mode(args)` returns `allowed = True` **only** when every one of these holds:

1. `CONFIG['allow_api_calls']` is `True`
2. `response_model_id` is not a placeholder
3. `pricing_version` is not a placeholder
4. `pricing.completion_input_usd_per_1k` is configured
5. `pricing.completion_output_usd_per_1k` is configured
6. `pricing.embedding_usd_per_1k` is configured
7. `budget_hard_cap_usd` is set
8. `budget_stop_review_usd` is set
9. `OPENAI_API_KEY` is present in the environment
10. `--live` flag passed
11. `--confirm-spend` flag passed

If any condition fails, the runner prints the unsatisfied preconditions and exits **without making any API call**. Even when all conditions pass, the live call paths remain unreachable stubs in this version — so no API call can occur from the current skeleton. Implementing those paths is itself a reviewed step (§2 item 4).

Dry-run mode (the default, and `--dry-run`) bypasses all of this: it requires no API key, makes no external request, and is the mode used for review.

---

## 7. Live run order

Once every blocker in §2 is resolved and reviewed, the live run follows the staged order from the run plan (§11), with budget checks at each step:

1. **Dry-run once more** — confirm 30 records, $0 cost, schema intact (no API).
2. **One English Agent A run** — confirm a real completion logs all fields, cost is plausible, `budget_state.json` updates.
3. **One English Agent B run** — confirm retrieval works, `retrieved_chunk_ids` + scores captured.
4. **One full intent across all languages and both agents** (6 runs) — confirm language-matched retrieval and per-language logging.
5. **Remaining four intents** (24 runs) — only if steps 1–4 are clean and the budget is on track.

At every step the `BudgetGuard` pre-checks projected cost; the loop pauses at $20 and halts at $25.

---

## 8. Manual approval checklist

Before flipping `allow_api_calls = True` and launching a live run, the project owner confirms each item:

- [ ] `response_model_id` set to a version-pinned snapshot (no "latest" alias)
- [ ] `embedding_model_version` recorded
- [ ] `pricing_version` set to a date-stamped identifier
- [ ] All three pricing fields populated from the provider's published rates
- [ ] `estimate_cost_usd` verified against a hand-calculated example
- [ ] `BudgetGuard` wired into the live run loop and tested with synthetic costs
- [ ] Live completion + embedding paths implemented and code-reviewed
- [ ] Dry-run re-run: 30 records, $0 cost, all validations PASS
- [ ] `OPENAI_API_KEY` available in the run environment (not committed, not logged)
- [ ] Budget cap ($25) and stop-review ($20) confirmed
- [ ] Evaluation plan ready (`expected-fact-mapping.md`; all outputs audited)
- [ ] Single-evaluator exploratory label acknowledged for any shared result

Only after every box is checked may `allow_api_calls = True` be set and `--live --confirm-spend` be used.

---

## 9. Rollback / stop conditions

The live run is stopped (and, if needed, rolled back) if any of these occur:

- Cumulative estimated cost reaches **$20** (pause for review) or would exceed **$25** (hard halt).
- Logging is incomplete (a required field is missing or null where a value is expected).
- Agent B retrieval metadata is missing.
- A model output uses facts not present in the KB / retrieved chunks (possible hidden-context leak).
- Agent A and Agent B prompts are found not to be comparable.
- A language rendering or query defect surfaces during runs.
- An API/auth error or rate-limit error occurs that is not cleanly handled.

On a stop: do not auto-retry. Preserve `results/stage2/budget_state.json` and all partial logs, record the stop reason, and review before any continuation. Continuation requires re-running the manual approval checklist for the remaining runs.

---

## 10. Stage 2 scope statement

**Stage 2 is a smoke test, not a proof of execution-tax.** Its purpose is to verify that the pipeline, logging, retrieval, prompting, and evaluation flow work safely and reproducibly. A 5-intent, single-repetition smoke test cannot support any execution-tax finding. Execution-tax remains a NiceM hypothesis. No public or publication-grade claim may be made from Stage 2 results; all shared results carry the label "single-evaluator exploratory pilot; independent review pending."

---

*This document defines live-run readiness. It does not authorize a live run. Live execution remains BLOCKED until every blocker in §2 is resolved, the manual approval checklist in §8 is complete, and the runner is reviewed. Version: s2-live-readiness-v0.1.0.*
