# Stage 2 Smoke Runner — Dry-Run Validation

**Generated:** 2026-06-14T05:49:10.208663+00:00
**Mode:** dry-run (no API calls, no embeddings, no API key)
**Runner:** `scripts/stage2_smoke_runner.py`

## Summary

- Planned runs: **30** (expected 30)
- Total dry-run estimated cost: **$0**
- All validations passed: **YES**

## Configuration (placeholders must be confirmed before API run)

| Key | Value |
|---|---|
| `response_model_id` | `TO_CONFIRM_EXACT_MODEL_ID` |
| `embedding_model_id` | `text-embedding-3-small` |
| `embedding_model_version` | `TO_CONFIRM` |
| `tokenizer_name` | `o200k_base` |
| `pricing_version` | `TO_CONFIRM_BEFORE_API_RUN` |
| `top_k` | `3` |
| `budget_hard_cap_usd` | `25.0` |
| `budget_stop_review_usd` | `20.0` |
| `allow_api_calls` | `False` |

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

## Required-field validation (run plan §12/§13)

- Required log fields per record: 28
- Required non-empty fields: intent_id, language, query_text, agent_design_id, kb_version, response_model_id, tokenizer_name, prompt_version

## API execution status

**API execution remains BLOCKED.** The following preconditions are not satisfied:

- CONFIG['allow_api_calls'] is False
- response_model_id is still a placeholder
- pricing_version is still a placeholder
- OPENAI_API_KEY is not present in the environment

Additionally, no real completion or embedding code is implemented: `_call_completion_api` and `_create_embeddings` are unreachable stubs that raise `NotImplementedError`. Stage 2 live execution cannot occur from this skeleton.

## Remaining blockers before the first live API call

1. Confirm `response_model_id` (TM1-b/c) — replace placeholder.
2. Confirm `pricing_version` — replace placeholder.
3. Implement and review the live completion + embedding paths (currently stubs).
4. Implement programmatic budget-cap enforcement (or document manual enforcement).
5. Set `allow_api_calls = True` only after review.
6. Provide `OPENAI_API_KEY` in the environment at run time.

