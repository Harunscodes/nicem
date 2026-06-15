# Stage 2 Smoke Runner — Dry-Run Validation

**Generated:** 2026-06-15T19:41:03.946803+00:00
**Mode:** dry-run (no API calls, no embeddings, no API key)
**Runner:** `scripts/stage2_smoke_runner.py`

## Summary

- Planned runs: **30** (expected 30)
- Total dry-run estimated cost: **$0**
- All validations passed: **YES**

## Configuration (placeholders must be confirmed before API run)

| Key | Value |
|---|---|
| `response_model_id` | `gpt-4.1-mini-2025-04-14` |
| `embedding_model_id` | `text-embedding-3-small` |
| `embedding_model_version` | `not-exposed-by-provider` |
| `tokenizer_name` | `o200k_base` |
| `pricing_version` | `openai-2026-06-14` |
| `top_k` | `3` |
| `budget_hard_cap_usd` | `25.0` |
| `budget_stop_review_usd` | `20.0` |
| `allow_api_calls` | `False` |
| `allow_local_calls` | `False` |
| `first_run_only` | `True` |
| `first_run_intent_id` | `INT-004` |
| `first_run_language` | `en` |
| `first_run_agent` | `agent_a_direct_full_kb` |
| `pricing.completion_input_usd_per_1k` | `0.0004` |
| `pricing.completion_output_usd_per_1k` | `0.0016` |
| `pricing.embedding_usd_per_1k` | `2e-05` |
| `pricing_configured` | `True` |

## Artifact versions parsed

| Language | Query version | KB version | KB chunks |
|---|---|---|---|
| en | `qr-en-v0.1.0` | `kb-en-v0.1.0` | 39 |
| nl | `qr-nl-v0.1.0` | `kb-nl-v0.1.0` | 39 |
| tr | `qr-tr-v0.1.0` | `kb-tr-v0.1.0` | 39 |

## Validation checks

| Check | Result | Detail |
|---|---|---|
| run_count_is_30 | PASS | 30 runs (expected 30) |
| run_ids_unique | PASS | 30 unique of 30 |
| all_required_log_fields_present | PASS | all present |
| required_nonempty_fields_populated | PASS | all populated |
| selected_intents_in_all_query_files | PASS | all 5 intents present in en/nl/tr |
| query_text_nonempty_for_all | PASS | all query_text present |
| kb_renderings_exist_all_languages | PASS | en/nl/tr present, 39 chunks each |
| budget_cap_fields_present | PASS | hard_cap=$25.0, stop_review=$20.0 |
| dry_run_sentinels_correct | PASS | endpoint=NOT_RUN, cost=0, raw_output_path=null on all runs |
| total_dry_run_cost_zero | PASS | total=$0 |
| pricing_selftest_pass | PASS | estimate_cost_usd(1000, 500, 200) = 0.00202; expected 0.00202 |

## Required-field validation (run plan §12/§13)

- Required log fields per record: 28
- Required non-empty fields: intent_id, language, query_text, agent_design_id, kb_version, response_model_id, tokenizer_name, prompt_version

## API execution status

**API execution remains BLOCKED.** The following preconditions are not satisfied:

- CONFIG['allow_api_calls'] is False
- OPENAI_API_KEY is not present in the environment

Additionally, the live completion + embedding code paths are now implemented (`_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, `run_live`) but are unreachable while `allow_api_calls` is False — they are never exercised by dry-run, the validation checks, or the guard tests. The `openai` package is imported lazily (live only); dry-run needs no dependency and no key.

## Pricing self-test

| Item | Result |
|---|---|
| Pricing formula self-test | PASS |
| Detail | `estimate_cost_usd(1000, 500, 200) = 0.00202; expected 0.00202` |

The self-test uses synthetic rates (not real pricing) and requires no API key. It verifies the `estimate_cost_usd` formula implementation. See `docs/benchmark/v0.1/stage2-model-pricing-config.md` §6.

## Safety-guard tests (no API calls, no embeddings, no API key)

### OpenAI live guard tests

| Guard test | Result | Detail |
|---|---|---|
| dry_run_default | PASS | no flags → dry-run (live=False, local=False) |
| no_api_key_required_for_dry_run | PASS | dry-run code path does not read OPENAI_API_KEY |
| live_without_confirm_refuses | PASS | refused; 4 blockers |
| live_with_confirm_refuses_when_allow_api_calls_false | PASS | refused: allow_api_calls is False |
| pricing_selftest | PASS | estimate_cost_usd(1000, 500, 200) = 0.00202; expected 0.00202 |
| budget_guard_synthetic_test | PASS | within=True, pause@$20=True, halt@$25=True; no state written (precheck only) |

### Local rehearsal guard tests

| Guard test | Result | Detail |
|---|---|---|
| local_without_confirm_refuses | PASS | refused; 3 blockers |
| local_with_confirm_refuses_when_allow_local_calls_false | PASS | refused: allow_local_calls is False |
| local_requires_max_runs | PASS | refused: max_runs=None → 3 blockers |
| local_base_url_must_be_localhost | PASS | non-localhost URL refused; original URL restored |
| live_and_local_mutually_exclusive | PASS | --live and --local cannot both be passed (argparse mutually exclusive group) |
| openai_live_still_blocked | PASS | OpenAI live refused: 3 blockers (allow_api_calls=False) |

### First-run selector guard tests

(`first_run_only=True`, approved run: `S2-INT-004-en-A`)

| Guard test | Result | Detail |
|---|---|---|
| local_requires_explicit_first_run_selector | PASS | refused: no selector supplied when first_run_only=True (2 blockers) |
| live_requires_explicit_first_run_selector | PASS | refused: no selector supplied when first_run_only=True (3 blockers) |
| local_rejects_wrong_first_run_selector | PASS | refused: intent INT-999 ≠ INT-004 (2 blockers) |
| live_rejects_wrong_first_run_selector | PASS | refused: language 'tr' ≠ 'en' (3 blockers) |
| selected_first_run_resolves_to_S2_INT_004_en_A | PASS | _resolve_run_id → 'S2-INT-004-en-A' (expected 'S2-INT-004-en-A') |

All guard tests: **ALL PASS** (17/17). No network access required. OpenAI live mode and local rehearsal mode are independently blocked (`allow_api_calls=False`, `allow_local_calls=False`). `--live` and `--local` are mutually exclusive. First-run selector enforced when `first_run_only=True`.

## Remaining steps before the first local rehearsal call

Local guard is implemented. The remaining steps for Stage 2-local are:

1. Install Ollama outside the repository and pull a local model (`ollama pull llama3.2:3b-instruct`).
2. Confirm the local server is reachable at `http://localhost:11434/v1`.
3. Set `allow_local_calls = True` (after confirming the above).
4. Run: `--local --confirm-local --max-runs 1 --intent-id INT-004 --language en --agent agent_a_direct_full_kb`
5. Inspect `results/stage2-local/raw_outputs/S2-INT-004-en-A.json`.
6. Set `allow_local_calls = False` again.

## Remaining steps before the first OpenAI live API call

Model IDs and pricing are CONFIRMED; the live paths are implemented. The remaining steps are:

1. Complete Stage 2-local rehearsal (above) to validate the pipeline.
2. Code-review the live paths (`_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, `run_live`).
3. Reconfirm `response_model_id` is non-deprecated and rates are current against the live API.
4. Set `allow_api_calls = True` (after review) — the single config flip that unblocks live mode.
5. Export `OPENAI_API_KEY` in the run environment (never committed, never logged).
6. Run `--live --confirm-spend --max-runs 1`, starting with one English Agent A run, watching `budget_state.json`.

