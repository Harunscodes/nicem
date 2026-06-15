# NiceM — AI Execution Intelligence

> Human language is the new code.
> Token-tax is the representation cost.
> Execution-tax is the workflow cost.
> Tokens-per-watt is the infrastructure efficiency question.
> NiceM measures and optimizes how AI systems execute human intent.

---

## What is NiceM?

NiceM is an independent research/startup project exploring how language, tokenization, agent design, retrieval, tool use, latency, cost, quality, and human correction affect the **total workload** required for AI systems to complete human intent.

The project starts from an observation in the academic literature — that different languages are treated unequally by AI tokenization systems — and extends it into a broader hypothesis: that all kinds of AI workflow overhead can be measured, diagnosed, and reduced.

---

## What is token-tax?

Token-tax is the extra representation burden caused by how a language, script, morphology, or tokenizer represents equivalent meaning. The same sentence in different languages can require very different numbers of tokens — and because most AI APIs charge per token, this creates a direct cost and quality inequality.

**This is established in the academic literature:**

- Petrov et al. (NeurIPS 2023) — tokenization parity across 200 languages; Shan requires up to 15× more tokens than English on the same tokenizer
- Ahia et al. (arXiv 2023) — API cost inequality by language; Telugu users pay ~4× more than English users for the same task
- Lundin et al. (arXiv 2025) — fertility (tokens/word) reliably predicts accuracy; higher fertility → lower accuracy; African languages trail English by ~25 accuracy points on average

Token-tax affects not just cost, but also latency, effective context window size, and model accuracy.

---

## What is execution-tax?

Execution-tax is the **extra total AI workflow burden** required to complete the same human intent successfully. It includes not only tokens, but also:

- retrieval calls and retrieval tokens
- tool calls and agent steps
- retries and context expansion
- latency, cost, quality score
- human correction

**This is a NiceM hypothesis.** It extends the token-tax concept from the tokenization layer into the full execution layer of agentic AI workflows. It is not yet proven by existing research — it is the core question NiceM is investigating.

The key research question:

> For the same human intent, do different languages, task types, models, prompts, retrieval strategies, tools, or agent designs create different total AI execution workloads?

---

## Why does this project exist?

The AI industry is moving from discrete model deployments to continuous **AI factories** — infrastructure designed to produce tokens at scale, continuously, efficiently (Jensen Huang, NVIDIA). The primary efficiency metric in this framing is **tokens per watt**.

NiceM's hypothesis is that the meaningful long-term metric is not just tokens per watt, but **successful human intent per watt** — and that execution-tax is the gap between these two numbers.

If execution-tax exists and is measurable, it has consequences for:
- AI infrastructure economics
- Language and accessibility equity
- Agentic AI system design
- Cost attribution and optimization

---

## What is the current stage?

This repository is in the **research and startup-foundation phase.**

The current work is:
- Structuring the thesis
- Mapping the academic literature
- Defining open questions
- Planning validation methodology

**Status:** the v0.1 methodology layer is complete and the full benchmark artifact construction phase is complete. `docs/methodology/` covers the full methodology stack. `docs/benchmark/v0.1/` contains all 14 benchmark artifacts plus a query variant plan: canonical fact-set (78 facts), document plan (39 chunks), language rendering plan, three aligned KB renderings (EN/NL/TR, 39 chunks each), 36-intent set, expected-fact mapping, quality gates, query rendering plan, three query rendering files (EN/NL/TR, 36 queries each, 108 total), a TM1 tokenizer/model decision note, and a query variant plan (optional robustness layer, not required before Stage 1). The consolidated roadmap is `docs/methodology/validation-plan-v0.1.md`.

No product code has been built. No model inference has been run. **Stage 1a (tokenizer-only sanity gate) is complete as of 2026-06-13** — all sanity checks PASS. The Turkish query review (QR9) is complete. Cross-language semantic equivalence audit is PASS. TM1 is confirmed: v0.1 uses the OpenAI GPT-4.1-mini/GPT-4.1 family (one family, one tokenizer, encoding `o200k_base`). Key Stage 1a findings: KB TR/EN median 1.37×, KB NL/EN median 1.07×; query TR/EN median 1.08× (compressed for short queries by Turkish syntactic compactness — pre-registered finding). Results in `results/stage1a/`. A tokenizer fallback was used (network policy blocked tiktoken BPE data download); re-run in a network-accessible environment for exact counts. Stage 2 decision plan is complete and all five blocking decisions are **CONFIRMED (2026-06-14)**: `docs/benchmark/v0.1/stage2-decision-plan.md` (s2-plan-v0.1.1). M9 = lightweight local JSONL/CSV logging (no external platform); AD1 = A1 (full relevant-language KB in Agent A prompt); TM8 = OpenAI `text-embedding-3-small` (same model across EN/NL/TR); EV1 = audit all Stage 2 outputs manually; TM5/BS6 = $25 USD hard cap (stop-and-review at $20). Smoke-test intent subset: INT-004, INT-015, INT-017, INT-026, INT-031. Estimated Stage 2 cost under $10 USD at GPT-4.1-mini rates. The Stage 2 smoke-test run plan is complete: `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` (s2-runplan-v0.1.0) defines the 30-run smoke test (5 intents × 3 languages × 2 agents), prompt plans, retrieval (top-k=3, language-matched), logging fields, and budget enforcement. The minimal logging runner (`scripts/stage2_smoke_runner.py`) is implemented with dry-run validation (30 runs built, all required fields, $0 cost, no API key required; outputs in `results/stage2/dry_run_*`) and live-mode scaffolding behind a strict guard (pricing table, cost estimation, a `BudgetGuard` enforcing the $25 hard cap / $20 stop-review, and `--live`/`--confirm-spend` flags). The live completion + embedding code paths are now **implemented** (review pending): `_call_completion_api`, `_create_embeddings`, a language-matched top-k retrieval (`_retrieve_top_k`), and the `BudgetGuard`-driven `run_live` loop (single attempt, no auto-retry, raw outputs to `results/stage2/raw_outputs/`). The `openai` package is imported lazily — dry-run never imports it or reads a key. Six safety-guard tests (default-is-dry-run, no-key-for-dry-run, live-refuses-without-confirm, live-refuses-while-`allow_api_calls=False`, pricing self-test, budget synthetic test) all PASS in `results/stage2/dry_run_validation.md`. Live mode is refused by default. The live-run readiness layer is documented in `docs/benchmark/v0.1/stage2-live-run-readiness.md` (s2-live-readiness-v0.1.2: blockers, guards, budget design, manual approval checklist, rollback conditions). The model and pricing configuration is CONFIRMED in `docs/benchmark/v0.1/stage2-model-pricing-config.md` (s2-model-pricing-v0.1.1): `response_model_id = gpt-4.1-mini-2025-04-14`, `pricing_version = openai-2026-06-14`, rates verified from official OpenAI sources, with the `estimated_cost_usd` formula, a hand-calculation, change-invalidation rules, and a filled confirmed-values table. A **Stage 2 local LLM rehearsal plan** has been added: `docs/benchmark/v0.1/stage2-local-llm-rehearsal-plan.md` (s2-local-rehearsal-v0.1.0, 2026-06-15) defines a zero-API-cost rehearsal phase using a local model (Ollama recommended; candidate: `llama3.2:3b-instruct`) before any paid OpenAI call. Local outputs go under `results/stage2-local/` and are labeled `LOCAL_REHEARSAL_ONLY` — separate from and not comparable to Stage 2-live OpenAI outputs. `allow_api_calls` remains `False` throughout. The local provider guard is now **implemented** in `scripts/stage2_smoke_runner.py` (2026-06-15): `can_run_local_mode()`, `allow_local_calls=False`, `--local`/`--confirm-local`/`--max-runs` CLI flags, `run_local()` (Agent A only; Agent B blocked), and 6 new local guard tests (12/12 total PASS). No localhost call has been made; `results/stage2-local/` does not yet exist. The rehearsal tests the runner pipeline, prompt formatting, logging, and audit workflow before money is spent. The Stage 2 live code review is complete: `docs/benchmark/v0.1/stage2-live-code-review.md` (s2-code-review-v0.1.0, 2026-06-14) is a 13-section self-review covering all live paths (safety-guard checklist 18 items all PASS, Agent A/B review, cost/budget review, run-order review, 28-field logging review, failure-handling review, 6 known risks, 9-item approval checklist). Verdict: **BLOCKED_PENDING_PROJECT_OWNER_APPROVAL**. The single sequence that unblocks Stage 2: project owner reviews the code review document, checks all 9 approval items, sets `allow_api_calls=True`, exports `OPENAI_API_KEY`, and runs `--live --confirm-spend`. No API call until the project owner completes that checklist.

A **mathematical foundations layer** has been added: `docs/theory/nicem-mathematical-foundations-roadmap-v0.1.md` (mf-roadmap-v0.1.0, 2026-06-14) provides formal definitions and conditional theorems grounding token-tax and execution-tax in Shannon information theory, Kolmogorov complexity, rate-distortion theory, and queueing theory. The roadmap explicitly separates mathematical existence (theorems) from empirical measurement (to be done in Stage 2/3). Seven future theory documents are planned; the rate-distortion model is the recommended next formalization.

---

## What should not be done yet

- No product code
- No experiments
- No SaaS architecture
- No customer-facing features

The next steps are: canonical fact-set, document plan, intent set, language rendering plan — in that order.

---

## Repository structure

```
CLAUDE.md                        — Global working instructions for Claude Code
README.md                        — This file

docs/
  nicem-thesis.md                — Core thesis and argument structure
  token-tax-vs-execution-tax.md  — Canonical definitions and distinction
  research-foundation.md         — Literature base, what is/isn't proven
  source-map.md                  — Which sources support which claims
  industry-context.md            — Jensen Huang / NVIDIA framing (industry context only)
  open-questions.md              — Tracked open and resolved questions

  sources/
    papers/
      petrov-tokenization-parity.md
      ahia-tokenization-fairness-api-pricing.md
      lundin-token-tax.md
      pdf/                       — Original PDF source files
    industry/                    — Industry source notes (in progress)
    notes/                       — Working notes and terminology (in progress)

  benchmark/
    v0.1/
      dataset-specification.md   — Structure, constraints, and authoring rules for all v0.1 artifacts
      canonical-fact-set.md      — 78 language-neutral canonical facts
      document-plan.md           — Content plan for 8 synthetic documents (39 chunks)
      intent-set.md              — 36 intent specifications (12/12/12 difficulty split)
      language-rendering-plan.md — Terminology and register rules per language
      expected-fact-mapping.md   — Evaluator reference: intent → required facts
      quality-gates.md           — Pre-run checklist with pass/fail status
      kb-rendering-en/nl/tr.md   — Three aligned KB renderings (39 chunks each)
      query-rendering-en/nl/tr.md — 108 user queries (36 intents × 3 languages)
      tm1-tokenizer-model-decision.md — TM1 confirmed: GPT-4.1-mini/GPT-4.1, o200k_base
      query-variant-plan.md      — Optional robustness layer (deferred to Stage 1b)
      stage2-decision-plan.md    — All 5 Stage 2 decisions (CONFIRMED 2026-06-14)
      stage2-smoke-test-run-plan.md — 30-run smoke-test plan (does not start Stage 2)
      stage2-live-run-readiness.md — Live-run blockers, guards, approval checklist (BLOCKED)
      stage2-model-pricing-config.md — Model IDs, pricing formula, hand-calc, change rules (CONFIRMED 2026-06-14)
      stage2-live-code-review.md — 13-section live path code review; approval checklist (BLOCKED_PENDING_PROJECT_OWNER_APPROVAL)
      stage2-local-llm-rehearsal-plan.md — Zero-cost local LLM rehearsal plan before Stage 2-live (Ollama recommended)

  theory/
    nicem-mathematical-foundations-roadmap-v0.1.md — Formal grounding: Shannon,
                                   Kolmogorov, rate-distortion, queueing; conditional
                                   theorems; 7 planned theory documents; TH1–TH8

scripts/
  stage1a_tokenizer_sanity_gate.py — Stage 1a execution script (o200k_base / fallback)
  stage2_smoke_runner.py      — Stage 2 logging runner (dry-run default; live paths implemented but blocked by allow_api_calls=False)

results/
  stage1a/
    token_counts_queries.csv    — 108 rows: per-intent, per-language query token counts
    token_counts_kb_chunks.csv  — 117 rows: per-chunk, per-language KB token counts
    token_tax_summary.md        — Stage 1a summary, ratio tables, gate verdict (PASS)
    token_tax_outliers.md       — 7 outlier cases with analysis
  stage2/
    dry_run_runs.jsonl          — 30 dry-run run records (no API calls)
    dry_run_runs.csv            — tabular export of the 30 dry-run records
    dry_run_run_matrix.csv      — compact run matrix
    dry_run_validation.md       — dry-run validation report (API execution BLOCKED)
```

---

## Independence note

NiceM is an independent personal research/startup project. It does not use employer data, customer data, or confidential information. All examples in this project use neutral synthetic scenarios.
