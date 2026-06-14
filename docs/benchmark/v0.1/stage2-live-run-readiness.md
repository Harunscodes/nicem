# Stage 2 Live-Run Readiness v0.1

**Version:** s2-live-readiness-v0.1.2
**Date:** 2026-06-14
**Status:** Dry-run PASS; model IDs + pricing **CONFIRMED**; live completion + embedding paths **IMPLEMENTED** (review pending); **live execution still BLOCKED** (`allow_api_calls=False`). This document defines the conditions, guards, and approval steps required before the first Stage 2 API call. It does not authorize a live run.
**Depends on:** `stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0), `stage2-decision-plan.md` (s2-plan-v0.1.1), `stage2-model-pricing-config.md` (s2-model-pricing-v0.1.1), `scripts/stage2_smoke_runner.py`, `logging-schema-v0.1.md`
**Feeds into:** the final manual approval step before live Stage 2 execution

---

## 1. Current status

| Item | Status |
|---|---|
| Stage 2 decisions (M9, AD1, TM8, EV1, TM5/BS6) | **CONFIRMED** (2026-06-14) |
| Stage 2 smoke-test run plan | **COMPLETE** (s2-runplan-v0.1.0) |
| Model IDs + pricing config | **CONFIRMED** (2026-06-14) — `stage2-model-pricing-config.md` (s2-model-pricing-v0.1.1) |
| Logging runner — dry-run skeleton | **PASS** — `scripts/stage2_smoke_runner.py`; 30 runs, all required fields, $0 cost, no API key |
| Live-mode scaffolding (guards, pricing, budget) | **IMPLEMENTED** — refuses to run by default |
| Live completion + embedding paths | **IMPLEMENTED, REVIEW PENDING** — `_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, `run_live`; lazily import `openai`; unreachable while `allow_api_calls=False` |
| Budget enforcement wired into live loop | **IMPLEMENTED** — `run_live` prechecks `BudgetGuard` before each call; pauses at $20, halts at $25; no auto-retry |
| Safety-guard tests (6) | **PASS** — in `dry_run_validation.md` (no API, no key) |
| Live execution | **BLOCKED** (`allow_api_calls=False`) |

The live call paths are now implemented and ready for review, but they are unreachable while `allow_api_calls=False`: `run_live` is only invoked after `can_run_api_mode()` returns `allowed=True`, which requires the config flag, confirmed model/pricing, `OPENAI_API_KEY`, and both `--live --confirm-spend`. The `openai` package is imported lazily (live only); dry-run, the validation checks, and the guard tests never import it, read a key, or touch the network.

---

## 2. Exact blockers before the first API call

**RESOLVED (2026-06-14)** — confirmed in `stage2-model-pricing-config.md` (s2-model-pricing-v0.1.1) and set in the runner `CONFIG`:

1. ~~**`response_model_id`** placeholder~~ → **RESOLVED**: `gpt-4.1-mini-2025-04-14` (version-pinned snapshot). Reconfirm against the live `/v1/models` listing immediately before the run.
2. ~~**`pricing_version`** placeholder~~ → **RESOLVED**: `openai-2026-06-14`.
3. ~~**Pricing table** unset~~ → **RESOLVED**: input `0.00040`, output `0.00160`, embedding `0.00002` (USD/1K). `pricing_configured()` now returns `True`.

**RESOLVED (implementation) — review pending:**

4. ~~**Live call paths** are unimplemented stubs~~ → **IMPLEMENTED**: `_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, and the `run_live` loop are written (lazy `openai` import; single attempt; no auto-retry; raw outputs to `results/stage2/raw_outputs/`). **Code review is still required** before enabling.
5. ~~**Programmatic budget enforcement** not wired~~ → **IMPLEMENTED**: `run_live` calls `BudgetGuard.precheck()` before every call (pause at $20, halt at $25) and `record()` after each, persisting `budget_state.json`. Verified by the `budget_guard_synthetic_test` (synthetic costs; no spend).

**STILL OPEN** — must be resolved before any live run:

6. **`allow_api_calls`** is `False`. Must be explicitly set to `True` — only after the §8 review. This is the single config flip that unblocks live mode.
7. **`OPENAI_API_KEY`** must be present in the environment at run time (never required for dry-run/review).
8. **CLI confirmation flags** `--live` and `--confirm-spend` must both be passed.

---

## 3. Required model IDs

| Field | Required value | Current (CONFIRMED 2026-06-14) |
|---|---|---|
| `response_model_id` | Version-pinned completion model (never a "latest" alias) | `gpt-4.1-mini-2025-04-14` |
| `embedding_model_id` | `text-embedding-3-small` (CONFIRMED, TM8) | `text-embedding-3-small` |
| `embedding_model_version` | Exact embedding snapshot if the provider exposes one | `not-exposed-by-provider` |
| `tokenizer_name` | `o200k_base` (encoding family, for traceability) | `o200k_base` |

The model IDs are recorded in the runner `CONFIG`. Reconfirm `gpt-4.1-mini-2025-04-14` is available and non-deprecated against the live `/v1/models` listing immediately before the run. See `stage2-model-pricing-config.md` §2.

---

## 4. Required pricing_version

- **`pricing_version`** is **CONFIRMED**: `openai-2026-06-14` (date of verification against OpenAI's official API pricing).
- The pricing table fields are all set (USD per 1,000 tokens), sourced from OpenAI's published rates as of `pricing_version`:
  - `pricing.completion_input_usd_per_1k` = `0.00040` (gpt-4.1-mini, $0.40/1M)
  - `pricing.completion_output_usd_per_1k` = `0.00160` (gpt-4.1-mini, $1.60/1M)
  - `pricing.embedding_usd_per_1k` = `0.00002` (text-embedding-3-small, $0.02/1M)
- The runner's `pricing_configured()` helper now returns `True`. Live mode is nonetheless refused because `allow_api_calls=False` and the live call paths are stubs.
- Before the first run, re-verify the published rates have not changed; if they have, bump `pricing_version`. Full sourcing in `stage2-model-pricing-config.md` §3 / §8.

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

If any condition fails, the runner prints the unsatisfied preconditions and exits **without making any API call**. Because `allow_api_calls=False` ships in `CONFIG`, condition 1 fails by default and live mode is refused regardless of any other state. The live call paths are now implemented (§2 items 4–5) but are reached only after this guard returns `allowed=True`; setting `allow_api_calls=True` is itself the reviewed step (§8).

Six **safety-guard tests** in `dry_run_validation.md` assert this behavior with no network access: `dry_run_default`, `no_api_key_required_for_dry_run`, `live_without_confirm_refuses`, `live_with_confirm_refuses_when_allow_api_calls_false`, `pricing_selftest`, and `budget_guard_synthetic_test` — all PASS.

Dry-run mode (the default, and `--dry-run`) bypasses all of this: it requires no API key, makes no external request, never imports `openai`, and is the mode used for review.

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

- [x] `response_model_id` set to a version-pinned snapshot (no "latest" alias) — `gpt-4.1-mini-2025-04-14` (reconfirm against live `/v1/models` at run time)
- [x] `embedding_model_version` recorded — `not-exposed-by-provider`
- [x] `pricing_version` set to a date-stamped identifier — `openai-2026-06-14`
- [x] All three pricing fields populated from the provider's published rates — input 0.00040 / output 0.00160 / embedding 0.00002 (USD/1K)
- [x] `estimate_cost_usd` verified against a hand-calculated example — hand-calc (s2-model-pricing §4.3) + runner self-test PASS (0.00202)
- [x] `BudgetGuard` wired into the live run loop and tested with synthetic costs — `run_live` prechecks/records; `budget_guard_synthetic_test` PASS
- [ ] Live completion + embedding paths implemented and code-reviewed — **IMPLEMENTED 2026-06-14; code review still required** before enabling
- [x] Dry-run re-run: 30 records, $0 cost, all validations PASS (11/11) + 6 guard tests PASS (2026-06-14)
- [ ] `OPENAI_API_KEY` available in the run environment (not committed, not logged)
- [x] Budget cap ($25) and stop-review ($20) confirmed
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

*This document defines live-run readiness. It does not authorize a live run. The live paths are now implemented; live execution remains BLOCKED until the still-open blockers in §2 (items 6–8) are resolved, the manual approval checklist in §8 is complete, and the live paths are code-reviewed. The single config flip that unblocks live mode is `allow_api_calls=True`. Version: s2-live-readiness-v0.1.2.*
