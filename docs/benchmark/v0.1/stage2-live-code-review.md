# Stage 2 Live Code Review

**Document ID:** s2-code-review-v0.1.0  
**Date:** 2026-06-14  
**Reviewer:** project owner (self-review)  
**Status:** BLOCKED_PENDING_PROJECT_OWNER_APPROVAL  

---

## 1. Purpose

This document is the final safety gate before any live OpenAI API call is made as part of Stage 2. Its purpose is to confirm that the live code paths in `scripts/stage2_smoke_runner.py` are correct, safe, and consistent with the run plan, pricing config, and logging schema — before `allow_api_calls` is set to `True`.

No API call may be made until the project owner has reviewed this document, verified each section, and checked all items in the approval checklist (§12).

---

## 2. Current Status

| Item | Status |
|---|---|
| Dry-run validation | PASS (11/11 checks) |
| Safety-guard tests | PASS (6/6) |
| Live paths implemented | YES (`_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, `_build_agent_a_prompt`, `_build_agent_b_prompt`, `run_live`, `BudgetGuard`) |
| Live mode default | BLOCKED (`allow_api_calls = False`) |
| API calls made so far | NONE |
| Embeddings created so far | NONE |
| Live artifacts created | NONE |
| `openai` package imported | NEVER (lazy import; dry-run does not trigger it) |
| `OPENAI_API_KEY` read | NEVER (only read inside `_get_openai_client()`, unreachable in current state) |

---

## 3. Review Scope

The following components are reviewed in this document:

- Live-mode guard logic (`can_run_api_mode`, `_dry_run_codepath_env_reads`)
- API key handling (`_get_openai_client`)
- Completion call (`_call_completion_api`)
- Embedding call (`_create_embeddings`)
- Cosine similarity (`_cosine_similarity`)
- Retrieval logic (`_retrieve_top_k`)
- Agent A prompt construction (`_build_agent_a_prompt`)
- Agent B prompt construction (`_build_agent_b_prompt`)
- Pre-call token estimation (`_estimate_chars_tokens`)
- BudgetGuard (`BudgetGuard.precheck`, `BudgetGuard.record`, `BudgetGuard.write_state`)
- Cost estimation (`estimate_cost_usd`, pricing constants)
- Run ordering (`_live_run_sequence`)
- Logging schema (`build_runs`, `REQUIRED_LOG_FIELDS`)
- Raw output storage (`run_live` raw payload)
- Failure handling (retrieval error, budget stop, completion error)

---

## 4. Safety Guard Checklist

Each item was verified against the implemented runner source.

| Guard | Status | Evidence |
|---|---|---|
| Dry-run is the default (no flags needed) | PASS | `mode_group` default: `--dry-run` default=True; `dry_run = not args.live` |
| Dry-run requires no API key | PASS | `_dry_run_codepath_env_reads()` returns `set()`; guard test `no_api_key_required_for_dry_run` PASS |
| `openai` package is imported lazily (live only) | PASS | `from openai import OpenAI` at line 666, inside `_get_openai_client()` body only; no top-level import |
| `OPENAI_API_KEY` read only at live runtime | PASS | Read only in `_get_openai_client()` via `os.environ.get("OPENAI_API_KEY")`; never read on dry-run path |
| API key never logged or written to any file | PASS | Key is passed only to `OpenAI(api_key=...)` constructor; not included in any log record, raw payload, or console output |
| `--live` requires `--confirm-spend` | PASS | `can_run_api_mode` checks `getattr(args, "confirm_spend", False)`; guard test `live_without_confirm_refuses` PASS |
| `allow_api_calls=False` blocks all live paths | PASS | `can_run_api_mode` checks `CONFIG.get("allow_api_calls")` first; ships as `False`; guard test `live_with_confirm_refuses_when_allow_api_calls_false` PASS |
| Model IDs are non-placeholder | PASS | `response_model_id = "gpt-4.1-mini-2025-04-14"` (CONFIRMED TM1-b/c); `embedding_model_id = "text-embedding-3-small"` (CONFIRMED TM8); `PLACEHOLDER_TOKENS` check in `can_run_api_mode` |
| All pricing fields are real numbers | PASS | `GPT_4_1_MINI_INPUT_USD_PER_1K = 0.00040`, output `0.00160`, embedding `0.00002`; `pricing_configured()` check in `can_run_api_mode` |
| Pricing self-test PASS | PASS | `estimate_cost_usd(1000, 500, 200) = 0.00202` with synthetic rates; guard test `pricing_selftest` PASS |
| BudgetGuard synthetic test PASS | PASS | `$0.50` proceeds; `$19.50+$1.00` pauses at stop-review; `$24.50+$1.00` halts at hard cap; guard test `budget_guard_synthetic_test` PASS |
| BudgetGuard `precheck` called before every API call | PASS | In `run_live`: `guard.precheck(est_cost)` called before `_call_completion_api`; retrieval errors halt before reaching completion |
| Hard cap is $25 USD | PASS | `CONFIG["budget_hard_cap_usd"] = 25.00`; `BudgetGuard.precheck` enforces `projected > self.hard_cap` |
| Stop-review threshold is $20 USD | PASS | `CONFIG["budget_stop_review_usd"] = 20.00`; `BudgetGuard.precheck` enforces `projected >= self.stop_review` |
| No auto-retry on API failure | PASS | Both `_call_completion_api` and `_create_embeddings` raise on error; `run_live` catches, sets `halted = True`, continues to mark remaining runs `NOT_RUN` |
| API error halts loop (no continuation) | PASS | Both retrieval error and completion error set `halted = True`; subsequent records get `endpoint_outcome = "NOT_RUN"` |
| Raw outputs written to `results/stage2/raw_outputs/` | PASS | `raw_dir = RESULTS_DIR / "raw_outputs"` in `run_live`; each run writes `{run_id}.json` |
| No live artifacts created in dry-run | PASS | `raw_outputs/`, `live_runs.*`, `budget_state.json` do not exist after dry-run; guard test `dry_run_default` PASS |

---

## 5. Agent A Review

Agent A design: `agent_a_direct_full_kb` (A1 — full relevant-language KB in prompt).

| Item | Status | Notes |
|---|---|---|
| Agent A uses no embeddings | PASS | `uses_retrieval = False`; `embedding_model_id` logged as `None` |
| `embedding_model_id` set to `null` in log record | PASS | `build_runs`: `embedding_model_id = None if not uses_retrieval` |
| Full KB rendered in user prompt | PASS | `_build_agent_a_prompt` joins all 39 chunks as `[chunk_id] <text>` |
| KB language matches query language | PASS | `kb_chunks = kb_chunk_data[lang]["chunks"]` using same `lang` as `record["language"]` |
| System prompt applied | PASS | `SYSTEM_PROMPT` passed as first argument to `_call_completion_api` |
| All 28 required log fields present | PASS | `REQUIRED_LOG_FIELDS` (28 items) verified by `validate()`; Agent A records satisfy all |
| `retrieval_calls` logged as 0 | PASS | Dry-run sets 0; live Agent A path does not call `_retrieve_top_k` |
| `retrieved_chunk_ids/fact_ids/scores` null | PASS | Not set on Agent A path; remain `None` from `build_runs` skeleton |

---

## 6. Agent B Review

Agent B design: `agent_b_simple_rag` (Simple RAG — language-matched top-k retrieval).

| Item | Status | Notes |
|---|---|---|
| Retrieval is language-matched | PASS | `_retrieve_top_k(client, query_text, kb_chunk_data[lang]["chunks"], top_k)` — same `lang` as query |
| Embedding model is `text-embedding-3-small` | PASS | `CONFIG["embedding_model_id"] = "text-embedding-3-small"` passed to `_create_embeddings` |
| top_k = 3 | PASS | `CONFIG["top_k"] = 3`; passed to `_retrieve_top_k` |
| Retrieved chunk IDs logged | PASS | `record["retrieved_chunk_ids"] = [c["chunk_id"] for c in retr["retrieved"]]` |
| Retrieval scores logged | PASS | `record["retrieval_scores"] = [c["score"] for c in retr["retrieved"]]` |
| Retrieved fact IDs logged | PASS | `record["retrieved_fact_ids"]` collects `fact_ids` from each retrieved chunk |
| Embedding token usage logged | PASS | `embedding_tokens_actual = retr["embedding_tokens"]` fed into `estimate_cost_usd` |
| `retrieval_calls` logged as 1 | PASS | `retr["retrieval_calls"] = 1` from `_retrieve_top_k` |
| Agent B prompt uses retrieved chunks only | PASS | `_build_agent_b_prompt(query_text, retr["retrieved"])` — not full KB |
| All 28 required log fields present | PASS | Same schema as Agent A; retrieval fields populated with real values in live mode |

---

## 7. Cost and Budget Review

| Item | Status | Notes |
|---|---|---|
| Pricing formula matches documentation | PASS | `estimate_cost_usd`: `(input/1000)*input_rate + (output/1000)*output_rate + (embedding/1000)*emb_rate` — matches `stage2-model-pricing-config.md` §5 |
| Standard (non-cached) input price used | PASS | `GPT_4_1_MINI_INPUT_USD_PER_1K = 0.00040`; cached rate (`0.00010`) is informational only, not used in formula |
| Embedding cost included for Agent B | PASS | `embedding_tokens_actual` included in `estimate_cost_usd(in_tok, out_tok, emb_tok)` |
| Embedding cost is 0 for Agent A | PASS | `emb_tok = embedding_tokens_actual or 0`; Agent A never calls `_retrieve_top_k` so `embedding_tokens_actual = None` |
| BudgetGuard records cumulative spend | PASS | `guard.record(actual_cost)` called after each successful run; `cumulative_cost` accumulates |
| BudgetGuard pauses at $20 | PASS | `precheck`: `projected >= self.stop_review` → `pause_stop_review`; sets `halted = True` |
| BudgetGuard halts at $25 | PASS | `precheck`: `projected > self.hard_cap` → `halt_hard_cap`; sets `halted = True` |
| Manual review required after first run | NOTE | Not enforced in code; must be observed by project owner — see §12 approval checklist item 7 |
| Pre-call estimate uses conservative (600 token) output estimate | PASS | `CONFIG["output_token_estimate"] = 600`; used in `est_output` before actual call |
| Budget state written to `results/stage2/budget_state.json` | PASS | `BudgetGuard.write_state()` called from `record()` and on error/halt |

---

## 8. Run-Order Review

| Item | Status | Notes |
|---|---|---|
| First live run must be INT-004 / en / Agent A | PASS | `_live_run_sequence` first entry: `f"S2-{first}-en-A"` where `first = SELECTED_INTENTS[0] = "INT-004"` |
| Second run is INT-004 / en / Agent B | PASS | Second entry: `f"S2-{first}-en-B"` |
| Remaining first-intent runs follow (NL-A, NL-B, TR-A, TR-B) | PASS | Loop over `[l for l in LANGUAGES if l != "en"]` → nl, tr |
| Remaining intents follow in order (INT-015, INT-017, INT-026, INT-031) | PASS | Loop over `SELECTED_INTENTS[1:]` |
| Defensive tail handles any unordered residuals | PASS | `tail` appended for any run_id not in `ordered_ids` |
| Project owner must stop after first run for manual inspection | NOTE | Not enforced in code; enforced by project owner — see §12 item 7 |

---

## 9. Logging Review

All 28 required log fields from `REQUIRED_LOG_FIELDS`:

| Field | Populated in dry-run | Populated in live (Agent A) | Populated in live (Agent B) |
|---|---|---|---|
| `run_id` | ✓ | ✓ | ✓ |
| `timestamp` | ✓ | ✓ | ✓ |
| `benchmark_version` | ✓ | ✓ | ✓ |
| `stage` | ✓ | ✓ | ✓ |
| `intent_id` | ✓ | ✓ | ✓ |
| `language` | ✓ | ✓ | ✓ |
| `query_text` | ✓ | ✓ | ✓ |
| `agent_design_id` | ✓ | ✓ | ✓ |
| `response_model_id` | ✓ | ✓ | ✓ |
| `embedding_model_id` | null (Agent A), value (Agent B) | null | ✓ `text-embedding-3-small` |
| `tokenizer_name` | ✓ | ✓ | ✓ |
| `prompt_version` | ✓ | ✓ | ✓ |
| `kb_version` | ✓ | ✓ | ✓ |
| `retrieved_chunk_ids` | null | null | ✓ list of 3 chunk IDs |
| `retrieved_fact_ids` | null | null | ✓ list of fact IDs |
| `retrieval_scores` | null | null | ✓ list of 3 scores |
| `input_tokens` | null | ✓ from API usage | ✓ from API usage |
| `output_tokens` | null | ✓ from API usage | ✓ from API usage |
| `total_tokens` | null | ✓ from API usage | ✓ from API usage |
| `model_calls` | 0 | 1 | 1 |
| `retrieval_calls` | 0 | 0 | 1 |
| `retry_count` | 0 | 0 | 0 |
| `latency_ms` | null | ✓ wall-clock ms | ✓ wall-clock ms |
| `estimated_cost_usd` | 0 | ✓ from formula | ✓ includes embedding |
| `endpoint_outcome` | `NOT_RUN` | `OK` / `ERROR` / `HALTED_BUDGET` / `PAUSED_BUDGET` | same |
| `failure_type` | null | null (OK) or error string | same |
| `evaluator_notes` | `"dry-run skeleton; not executed"` | null (OK) or error note | same |
| `raw_output_path` | null | ✓ relative path to `results/stage2/raw_outputs/{run_id}.json` | ✓ |

---

## 10. Failure Handling Review

| Failure scenario | Handling | Status |
|---|---|---|
| Embedding/retrieval API error (Agent B) | Caught in `run_live`; `endpoint_outcome = "ERROR"`, `failure_type = "retrieval_error: <ExcType>"`, `halted = True`; `guard.write_state()` called | PASS |
| Budget precheck stop (pause or halt) | `endpoint_outcome = "PAUSED_BUDGET"` or `"HALTED_BUDGET"`, `failure_type = guard.status`, `halted = True`; `guard.write_state()` called | PASS |
| Completion API error | Caught in `run_live`; `endpoint_outcome = "ERROR"`, `failure_type = "completion_error: <ExcType>"`, `evaluator_notes` set, `halted = True`; `guard.write_state()` called | PASS |
| Remaining runs after halt | All get `endpoint_outcome = "NOT_RUN"`, `evaluator_notes = "skipped: loop halted before this run"` | PASS |
| Missing `OPENAI_API_KEY` | `can_run_api_mode` refuses before any run begins; also `_get_openai_client()` raises `RuntimeError` if key absent | PASS |
| `openai` package not installed | `_get_openai_client()` raises descriptive `RuntimeError`; caught by live entry guard | PASS |
| Placeholder model ID / pricing | `can_run_api_mode` refuses before live mode begins | PASS |
| No auto-retry in any path | Verified: no retry loop anywhere in `_call_completion_api`, `_create_embeddings`, `_retrieve_top_k`, or `run_live` | PASS |

---

## 11. Known Remaining Risks

The following risks are noted but do not block approval; they must be managed at run time:

1. **Model snapshot availability.** `gpt-4.1-mini-2025-04-14` must be confirmed as non-deprecated against the live `/v1/models` endpoint immediately before the first run. If deprecated, update `response_model_id` in CONFIG and re-review.

2. **Pricing currency.** Rates were verified 2026-06-14. If OpenAI changes pricing before the run date, update pricing constants, regenerate the pricing document (s2-model-pricing-config.md), and re-run dry-run validation before enabling live mode.

3. **OpenAI SDK version behavior.** The code uses `resp.model_dump()` and `resp.usage.prompt_tokens`. These field names are stable as of the `openai` Python SDK v1.x. Confirm the installed version before the first run (`pip show openai`).

4. **`usage` field shape.** If OpenAI returns `None` for `usage` or changes field names, the fallback (`result["input_tokens"] or est_input`) will use the pre-call estimate rather than actual counts. The first run output must be manually inspected to confirm usage fields are populated correctly.

5. **Single-evaluator limitation.** All Stage 2 quality evaluation (EV1: audit all outputs) is by the project owner alone. Results must carry the label "single-evaluator exploratory pilot; independent review pending" before any external sharing. Turkish and Dutch outputs require independent bilingual review before any publication-grade claim.

6. **No public claims before review.** v0.1 Stage 2 results are internal exploratory data. No public or publication-grade claims may be made from Stage 2 outputs alone.

7. **First-run selector added post-review.** After this document was written, a first-run selector was implemented (2026-06-15): `first_run_only=True` in CONFIG, `--intent-id`/`--language`/`--agent` CLI flags, `_check_first_run_selector()` guard called from `can_run_api_mode()`. The live command now requires explicit selector flags and will refuse if they do not match `first_run_intent_id="INT-004"`, `first_run_language="en"`, `first_run_agent="agent_a_direct_full_kb"`. This is an additional safety control; it does not introduce new risk. The 9-item approval checklist below is extended accordingly.

---

## 12. Approval Checklist

The project owner must verify and manually check each item before setting `allow_api_calls = True`.

- [ ] I have read the full live code review document (§1–§11 above).
- [ ] I have confirmed `response_model_id = "gpt-4.1-mini-2025-04-14"` is current and non-deprecated against the live `/v1/models` API listing.
- [ ] I have confirmed pricing rates in `PRICING_VERSION = "openai-2026-06-14"` are still current from official OpenAI sources on the run date.
- [ ] I have confirmed the `openai` Python package is installed and the SDK version is v1.x compatible with `resp.model_dump()` and `resp.usage.prompt_tokens`.
- [ ] I have the `OPENAI_API_KEY` ready to export into the run environment and will not commit it to the repository.
- [ ] I have read and accept the $25 hard cap and $20 stop-review thresholds. I understand the runner will halt automatically at these limits.
- [ ] I will stop after the first run (`S2-INT-004-en-A`) to manually inspect `results/stage2/raw_outputs/S2-INT-004-en-A.json` and `results/stage2/budget_state.json` before allowing the loop to continue.
- [ ] I understand that all Stage 2 outputs are internal exploratory data and will not be shared publicly or cited as publication-grade findings without independent bilingual review of Turkish and Dutch outputs.
- [ ] I understand the first-run selector (`first_run_only=True`): the live call requires `--intent-id INT-004 --language en --agent agent_a_direct_full_kb` to be passed explicitly, and the runner will refuse if they are missing or don't match.
- [ ] I am ready to set `CONFIG["allow_api_calls"] = True` in `scripts/stage2_smoke_runner.py` and run `python scripts/stage2_smoke_runner.py --live --confirm-spend --max-runs 1 --intent-id INT-004 --language en --agent agent_a_direct_full_kb`.

---

## 13. Verdict

```
BLOCKED_PENDING_PROJECT_OWNER_APPROVAL
```

The live code paths are implemented and all automated safety checks pass. The single action that unblocks live mode is:

1. The project owner reviews this document and checks all 9 items in §12.
2. Set `CONFIG["allow_api_calls"] = True` in `scripts/stage2_smoke_runner.py`.
3. Export `OPENAI_API_KEY` in the run environment.
4. Run: `python scripts/stage2_smoke_runner.py --live --confirm-spend --max-runs 1 --intent-id INT-004 --language en --agent agent_a_direct_full_kb`

No API call may be made before these steps are complete.
