# Stage 2 Local LLM Rehearsal Plan v0.1

**Document ID:** s2-local-rehearsal-v0.1.0  
**Date:** 2026-06-15  
**Status:** PLANNING — not yet implemented  

---

## 1. Purpose

Stage 2-local is a zero-API-cost rehearsal phase that runs before any paid OpenAI Stage 2-live call. It uses a locally running LLM instead of the OpenAI API, so the full runner pipeline can be exercised at no cost and without an API key.

Stage 2-local tests:

- prompt formatting and system/user message structure
- run order and the staged execution sequence
- logging completeness — whether all 28 required fields are populated
- raw output capture to `results/stage2-local/raw_outputs/{run_id}.json`
- manual audit workflow — whether a human evaluator can open outputs and apply PASS/FAIL/UNCERTAIN
- failure handling — what happens when the local server is unavailable or returns an error

Stage 2-local does **not**:

- prove or estimate execution-tax
- replace the OpenAI Stage 2 smoke test
- produce results comparable to Stage 2-live outputs
- contribute to any NiceM claim about token-tax or model performance

All Stage 2-local results must be labeled `LOCAL_REHEARSAL_ONLY` and stored under `results/stage2-local/`, separate from `results/stage2/` (the OpenAI output directory).

---

## 2. Why local first

Running a local provider before the first paid OpenAI call offers several concrete benefits:

- **Zero spend risk.** Local inference costs nothing. Mistakes in prompt construction, log field population, or output storage have no financial consequence.
- **No API key required.** `OPENAI_API_KEY` is never read or needed. The OpenAI live guard remains blocked.
- **Runner debugging.** The live code paths (`_call_completion_api` shape, `run_live` loop, BudgetGuard interaction, raw output writing) can be exercised against a real HTTP response rather than a dry-run stub.
- **Prompt inspection.** The system prompt and the full-KB Agent A user prompt (39 chunks) can be seen as actually sent over the wire — format, whitespace, chunk ordering — before they are sent to a paid model.
- **Raw output validation.** The raw JSON response structure from a local model can be checked to confirm that the `resp.usage.prompt_tokens` / `resp.choices[0].message.content` / `resp.model_dump()` fields are present in the expected shape.
- **Audit workflow rehearsal.** The project owner can practice the EV1 manual evaluation (PASS/FAIL/UNCERTAIN against `expected-fact-mapping.md`) before the first paid result arrives.
- **Safe iteration.** Prompt wording can be adjusted, field names verified, and edge cases triggered — all before a single token of OpenAI budget is spent.

---

## 3. Provider options

Three local provider options are suitable for this rehearsal:

### Ollama

Runs a local HTTP server (`http://localhost:11434`) with an OpenAI-compatible `/v1/chat/completions` API. Models are downloaded via `ollama pull <model>`. No configuration files beyond the model name. Supports a wide range of instruction models (Mistral, Llama, Qwen, Gemma, and others). The OpenAI Python SDK can point to it with `base_url="http://localhost:11434/v1"` and a dummy `api_key="ollama"`.

**Recommended default.** Easiest local setup; directly compatible with the runner's existing `_call_completion_api` and `_create_embeddings` call shapes.

### llama.cpp local server

`llama-server` (from the llama.cpp project) also exposes an OpenAI-compatible API. Requires manually downloading a GGUF model file and launching the server with the correct context-length flags. More control over quantization and context size than Ollama, but more setup steps. A good fallback if Ollama is unavailable.

### LM Studio

A GUI wrapper around llama.cpp that also exposes a local OpenAI-compatible server. Useful if the project owner prefers a graphical model browser for downloading and selecting models. The local server endpoint is typically `http://localhost:1234/v1`. Works with the same runner integration pattern as Ollama.

**Provider decision:** select before adding the local provider guard to the runner (§7 / next action 1).

---

## 4. Candidate local models

The exact local model is a **rehearsal parameter** — it is not the benchmark model and its outputs are not comparable to GPT-4.1-mini. The purpose of the model choice is only to produce a structured JSON-shaped response that the runner can parse and store.

Candidate instruction-tuned model families, all available on Ollama:

| Family | Example pull name | Notes |
|---|---|---|
| Mistral | `mistral:7b-instruct` | Strong instruction following; widely tested |
| Qwen | `qwen2.5:7b-instruct` | Good multilingual coverage; relevant for NL/TR rehearsal |
| Llama | `llama3.2:3b-instruct` | Smallest capable Llama; fast on laptop |
| Gemma | `gemma2:9b-instruct` | Google family; good instruction tuning |

**Recommendation:** start with `llama3.2:3b-instruct` (or `mistral:7b-instruct` if RAM allows). Both run comfortably on a modern laptop (16 GB RAM), complete a prompt in seconds, and produce well-formed chat responses. For the 39-chunk Agent A full-KB prompt (~4,000–6,000 tokens), a model with at least 8 K context is required; confirm context window before pulling.

The specific model chosen must be recorded in the runner's `local_response_model_id` config field before the first local run.

---

## 5. Scope

Stage 2-local follows the same first-run discipline as Stage 2-live:

**Step 1 (required):** run only `S2-INT-004-en-A` (INT-004, English, Agent A). Stop immediately afterward. Inspect:
- `results/stage2-local/raw_outputs/S2-INT-004-en-A.json`
- the JSONL log record
- whether all 28 required fields are populated
- whether the model response is usable for manual evaluation

**Step 2 (optional, only after step 1 passes):** run the full 30-run local rehearsal matrix:

```
5 intents × 3 languages × 2 agents = 30 local runs
```

Using the same intents, languages, and agents as Stage 2-live (INT-004, INT-015, INT-017, INT-026, INT-031; en/nl/tr; Agent A and Agent B).

The optional matrix is not a prerequisite for Stage 2-live. If step 1 passes (pipeline works, logs are clean, audit is feasible), that is sufficient rehearsal evidence to proceed to Stage 2-live.

---

## 6. Separation from Stage 2-live

Local and OpenAI results must never be mixed.

| Dimension | Stage 2-local | Stage 2-live |
|---|---|---|
| Output directory | `results/stage2-local/` | `results/stage2/` |
| Raw outputs | `results/stage2-local/raw_outputs/` | `results/stage2/raw_outputs/` |
| Provider | local (Ollama / llama.cpp / LM Studio) | OpenAI API |
| Model | local instruction model (rehearsal parameter) | `gpt-4.1-mini-2025-04-14` |
| `estimated_cost_usd` | 0 (local inference is free) | real cost at confirmed OpenAI rates |
| Tokenizer | local model tokenizer (varies) | `o200k_base` |
| Token counts | local model token counts (not comparable) | OpenAI token counts |
| Result label | `LOCAL_REHEARSAL_ONLY` | Stage 2-live smoke-test output |
| Evidence value | pipeline / engineering evidence | first OpenAI-backed benchmark data |

Local model outputs cannot be mixed with OpenAI outputs because:
- the model family, size, and instruction-following behavior differ substantially
- local tokenizer token counts are not comparable to `o200k_base`
- local cost fields are always 0, which would corrupt cost-analysis aggregations

Any document or communication that references NiceM Stage 2 results must clearly state which provider produced the outputs.

---

## 7. Runner changes required

The current runner has a single provider path (dry-run or OpenAI live). Local rehearsal requires a second provider path with its own guard flags, config values, and output directory. The following changes are proposed but not yet implemented.

### Config additions

```python
CONFIG = {
    ...
    # Local provider (Stage 2-local rehearsal — separate from OpenAI live).
    "provider": "dry_run",              # "dry_run" | "local_ollama" | "openai"
    "local_base_url": "http://localhost:11434/v1",
    "local_response_model_id": "TO_CONFIRM_LOCAL_MODEL",
    "local_embedding_model_id": "TO_CONFIRM_LOCAL_EMBEDDING_MODEL_OR_DISABLED",

    # Guard flags — both default to False.
    "allow_local_calls": False,         # flip for local rehearsal
    "allow_api_calls": False,           # flip only for OpenAI live (reviewed separately)
    ...
}
```

### CLI additions

```
--local           request local rehearsal mode (requires --confirm-local)
--confirm-local   explicit confirmation of local provider use
```

These flags are separate from `--live` / `--confirm-spend`. OpenAI and local providers must have independent guard paths so enabling one cannot accidentally enable the other.

### Guard logic

A new `can_run_local_mode(args)` function (parallel to `can_run_api_mode`) should check:

- `CONFIG["allow_local_calls"] is True`
- `CONFIG["provider"]` is a non-placeholder local provider string
- `CONFIG["local_response_model_id"]` is not `TO_CONFIRM_LOCAL_MODEL`
- `CONFIG["local_base_url"]` resolves to a live local server
- `args.local is True` and `args.confirm_local is True`
- `OPENAI_API_KEY` is **not** checked (local mode must not require it)
- `allow_api_calls` is **not** checked (OpenAI remains independently blocked)

### Output path routing

When `provider == "local_ollama"`, the runner must write to `results/stage2-local/` (not `results/stage2/`). The `RESULTS_DIR` path should be selected at runtime based on the active provider, not hardcoded.

These changes must be implemented and code-reviewed before `allow_local_calls` is set to `True`. The dry-run path must remain unaffected.

---

## 8. Embedding strategy for local rehearsal

Agent B requires retrieval (embedding the query + KB chunks, cosine ranking, top-k selection). Local embedding models exist (e.g., `nomic-embed-text` on Ollama) but add setup complexity. Three options:

**Option A — Agent A only first, no embeddings (recommended for first local run).**
Run only `S2-INT-004-en-A` (Agent A). No embeddings needed. The full KB is placed directly in the user prompt. This is the minimal-complexity first rehearsal.

**Option B — Local embeddings via Ollama.**
Pull an embedding model (`ollama pull nomic-embed-text` or similar). The `_create_embeddings` call pointed to `local_base_url` should work without code changes if the model is running. Use this for Agent B local rehearsal once Agent A passes. Local embedding counts are not comparable to `text-embedding-3-small`.

**Option C — Lexical retrieval fallback for Agent B local rehearsal.**
Replace `_retrieve_top_k` with a BM25-style lexical ranker (e.g., simple TF-IDF or keyword overlap) for local mode only, avoiding any embedding call entirely. This tests the Agent B logging and prompt structure without needing a local embedding model.

**Recommendation:** Option A first (Agent A only), then Option B if a local embedding model is available. Fall back to Option C if local embedding setup is too complex. Option C is lower fidelity for retrieval rehearsal but still validates the logging schema for Agent B runs.

---

## 9. Logging requirements

Local rehearsal runs must still populate all 28 Stage 2 required fields wherever possible, so the logs are structurally identical to Stage 2-live logs and can be audited with the same tooling.

**Additional local-only fields** (appended to each local run record):

| Field | Type | Value |
|---|---|---|
| `provider` | string | `"local_ollama"` (or chosen provider name) |
| `local_base_url` | string | `"http://localhost:11434/v1"` |
| `local_model_id` | string | confirmed model name (e.g. `"llama3.2:3b-instruct"`) |
| `local_embedding_model_id` | string or null | local embedding model name, or null if not used |
| `local_cost_usd` | float | `0` (local inference has no token cost) |
| `local_runtime_seconds` | float or null | wall-clock seconds for the local call, if measurable |

**Cost field behavior for local runs:**
- `estimated_cost_usd` must be set to `0` (no spend).
- `local_cost_usd` carries the same `0` value explicitly.
- Token count fields (`input_tokens`, `output_tokens`, `total_tokens`) should be populated from the local API response's `usage` field where available; if unavailable, set to `null` with a note in `evaluator_notes`.
- Local token counts are **not** comparable to `o200k_base` counts and must not be used in token-tax analysis.

---

## 10. Safety guards

The following constraints must hold throughout Stage 2-local:

- **Local mode must not read `OPENAI_API_KEY`.** The `can_run_local_mode` guard must not check for it. If the key happens to be present in the environment, it must be ignored on the local code path.
- **Local mode must not call `api.openai.com`.** The `local_base_url` must point to localhost. A test that verifies the URL is not an OpenAI domain must be part of the local guard.
- **OpenAI live mode must remain blocked.** `allow_api_calls` stays `False` throughout Stage 2-local. The local guard and the OpenAI guard are independent; flipping `allow_local_calls` must not affect `allow_api_calls`.
- **Local calls require `allow_local_calls=True`.** Default is `False`; must be flipped manually after the local runner code is reviewed.
- **Local calls require `--local --confirm-local`.** Both flags must be passed; neither alone is sufficient.
- **Localhost unavailability must fail safely.** If `http://localhost:11434` is unreachable, the runner must catch the connection error, log `endpoint_outcome=ERROR`, set `failure_type="local_connection_error"`, and halt. No hang, no retry.
- **No secrets logged.** The `local_base_url` is safe to log (it is a localhost address). No API keys or credentials of any kind appear in any log record or raw output file.

---

## 11. Evaluation plan

Local rehearsal outputs are evaluated using the same PASS / FAIL / UNCERTAIN manual audit defined in `docs/methodology/evaluation-method-v0.1.md` and `docs/benchmark/v0.1/expected-fact-mapping.md`.

All local evaluation records must carry the label:

```
LOCAL_REHEARSAL_ONLY
```

This label must appear in:
- the `evaluator_notes` field of every local run record
- any document or summary that references local results
- the header of any local results file

Local results must not be used to make claims about:
- token-tax magnitude or direction
- execution-tax magnitude or direction
- model performance on the NiceM benchmark
- cross-language performance differences

A PASS on a local evaluation means: "the pipeline produced a usable answer that can be audited." It does not mean: "the local model performs equivalently to GPT-4.1-mini."

---

## 12. Pass/fail criteria

### Local rehearsal passes if

- the local provider is reachable and returns a valid chat completion response
- the raw output is written to `results/stage2-local/raw_outputs/S2-INT-004-en-A.json`
- all 28 required log fields are populated (or null with documented reason)
- the additional local fields (`provider`, `local_model_id`, `local_cost_usd`) are present
- the model response is a readable English text that can be manually evaluated
- the run halts after the one approved local run (first-run discipline enforced)
- `allow_api_calls` remains `False` throughout
- no call was made to any OpenAI endpoint

### Local rehearsal fails or pauses if

- the local provider accidentally routes to an OpenAI endpoint (hard fail; abort)
- any log record is missing required fields without a documented reason
- the raw output file cannot be written or is not valid JSON
- the local model returns an empty or unparseable response in a way that breaks the audit workflow
- the run continues past the first approved local run without explicit re-approval
- the runner reads or requires `OPENAI_API_KEY` during local mode

---

## 13. First local run approval

The first local run approved under this plan is:

| Field | Value |
|---|---|
| `intent_id` | INT-004 |
| `language` | en |
| `agent_design_id` | agent_a_direct_full_kb |
| `provider` | local_ollama (or chosen local provider) |
| `run_id` | S2-INT-004-en-A (local prefix or run_id suffix TBD by implementation) |
| Stop condition | immediately after this one call |

This approval is conditional on:
1. The runner having a reviewed local provider guard (`can_run_local_mode`).
2. `allow_local_calls = True` set after that review.
3. The local provider being running and reachable at `local_base_url`.
4. `allow_api_calls` confirmed as `False` immediately before the run.

This approval covers only the one call above. Any additional local run requires a separate decision.

---

## 14. Relationship to NiceM evidence

Stage 2-local produces **engineering evidence** only. It tells the project owner whether the pipeline works as designed. It does not produce research evidence.

| Phase | Evidence type | What it shows |
|---|---|---|
| Dry-run | Structural evidence | 30 run records are well-formed; logging schema is correct |
| Stage 2-local | Engineering evidence | Live code paths work; prompts are sent and received; logs are complete; audit is feasible |
| Stage 2-live | First benchmark data | First real OpenAI-backed outputs; first cost-and-token measurements with `o200k_base` |
| Stage 3 / full benchmark | Research evidence | Sufficient runs to observe token-tax and execution-tax patterns |

No claim about token-tax, execution-tax, cost inequality, or model performance can be drawn from Stage 2-local alone. The first meaningful benchmark data comes from Stage 2-live. Even Stage 2-live (30 runs) is a smoke test — Stage 3 or a larger benchmark run is required before any quantitative execution-tax claim.

---

## 15. Next actions

In priority order:

1. **Choose local provider** — confirm Ollama, llama.cpp, or LM Studio. Default recommendation: Ollama. Install and start outside the repository.
2. **Choose local model** — pull a small instruction model (e.g. `ollama pull llama3.2:3b-instruct`). Confirm context window ≥ 8 K tokens for the 39-chunk full-KB Agent A prompt.
3. **Install/start local provider** — verify the local server is reachable at `http://localhost:11434/v1` (Ollama) before touching the runner.
4. **Add local provider guards to runner** — implement `can_run_local_mode`, `--local` / `--confirm-local` flags, provider-aware `RESULTS_DIR` routing, and additional local log fields. Keep `allow_local_calls = False` until implementation is reviewed.
5. **Code-review local runner additions** — parallel to the existing `stage2-live-code-review.md` process; confirm OpenAI live mode remains blocked.
6. **Dry-run validation** — re-run `--dry-run` and confirm all 11 checks still PASS after the local provider additions.
7. **Run one local Agent A call** — set `allow_local_calls = True`, run `--local --confirm-local`, execute `S2-INT-004-en-A`, set `allow_local_calls = False` immediately after.
8. **Inspect logs** — review `results/stage2-local/raw_outputs/S2-INT-004-en-A.json`, the JSONL record, and manually evaluate the response against `expected-fact-mapping.md` for INT-004.
9. **Decide whether to run the 30-run local rehearsal** — only proceed if step 7–8 pass and the additional rehearsal scope is worth the setup time.
10. **Proceed to Stage 2-live** — after local rehearsal confirms the pipeline works, follow the Stage 2-live approval process (`stage2-live-code-review.md` §12).

---

*Stage 2-local is a rehearsal, not a result. OpenAI Stage 2-live remains the first paid benchmark phase. This plan does not authorize any paid call. Version: s2-local-rehearsal-v0.1.0.*
