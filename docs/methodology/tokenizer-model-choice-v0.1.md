# NiceM Tokenizer and Model Choice v0.1

**Status:** Decision rules defined — specific provider/model not yet chosen (pending budget and smoke-test; see §12)
**Addresses:** BT1 / LS4 / LG2 open questions; framework §12 baseline-token-tax prerequisite (unblocking the final step)
**Depends on:** `docs/methodology/baseline-token-tax-calculation-v0.1.md`, `docs/methodology/logging-schema-v0.1.md`, `docs/methodology/falsification-and-decision-rules-v0.1.md`
**Feeds into:** Dataset construction (query tokenization sanity gate, §5 step 1), pilot implementation, M9 instrumentation choice

**Fixed context:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 documents, ~75 canonical facts; intents: 36 × English/Dutch/Turkish
- Agent A: Direct LLM baseline; Agent B: Simple RAG
- Execution-tax remains a hypothesis

---

## 1. Purpose

The tokenizer and model choice is load-bearing for every quantitative claim NiceM v0.1 makes:

- **Token-tax ratios are tokenizer-dependent.** A 1.8× Turkish/English ratio under one tokenizer may be 1.3× under another. NiceM's token-tax measurements are only comparable to the literature (Petrov, Ahia, Lundin) and internally consistent if the tokenizer is fixed and named (baseline-token-tax-calculation §2 and §10).
- **Residual overhead can only be computed against the same tokenizer that drove run costs.** The residual-overhead method (baseline-token-tax §9) subtracts a token-scaled expectation from observed costs. If the tokenizer used for counting and the model used for running differ, the expectation is computed in the wrong unit and the residual is meaningless.
- **PASS/FAIL rates are model-dependent.** If the chosen model cannot reliably answer Product FAQ intents in Turkish, failures may reflect model capability rather than language overhead — a confound that would corrupt both token-tax and candidate execution-tax measurements. This is why model choice must be accompanied by a smoke test (§5) before the full benchmark runs.

This document defines the decision rules and staged approach for making this choice without premature commitment.

---

## 2. Core principle

> **For v0.1, NiceM uses one model family and one tokenizer, consistently, across all language conditions and both agent designs.**

- The tokenizer used for token-tax calculation (query rendering sanity gate, per-intent ratios) **must match** the tokenizer that the execution model uses for billing and context management.
- Both Agent A and Agent B use the same model. The only variable between them is whether retrieval is used — if models differed, design differences would be confounded with model differences.
- Do not compare multiple model families in v0.1. That is a separate experiment, requiring a separate run design.

Violation of this principle does not just weaken results — it invalidates the residual-overhead calculation entirely.

---

## 3. Why not compare multiple models in v0.1

The reasons compound, not just add:

| Problem | Consequence |
|---|---|
| Different tokenizers → different token-tax ratios | The token-tax baseline would need to be calculated separately per model; ratios would not be comparable across model conditions at n=36 |
| Different model capability → different PASS/FAIL rates | A cross-language success-rate gap could reflect one model's Turkish ability rather than the task's execution overhead |
| Different pricing → different cost-per-successful-completion | Even if PASS rates were equal, cost comparisons would require normalization that introduces its own assumptions |
| Different context limits → different retrieval context sizes | Agent B's retrieved context might be constrained differently per model, changing retrieval behavior |
| Too many variables → attribution impossible | At 36 intents, a significant model × language interaction has no chance of being separated from a design × language interaction |

Multi-model comparison is a legitimate v0.2 or later study — once the measurement instrument is validated on a single model, adding a second model tests whether token-tax and execution-tax ratios are model-dependent (Q2 in open-questions). It should not be v0.1's scope.

---

## 4. Candidate model/tokenizer options

### Option A — Commercial API model with provider token usage logs

Typical examples: a major hosted API that reports input tokens, output tokens, and (if applicable) cached tokens per call, with a published tokenizer or a deterministic provider-side count.

| Dimension | Assessment |
|---|---|
| Realistic cost measurement | Yes — provider-reported token usage and a published price table give the most realistic cost-per-successful-completion estimate for anyone running AI workflows in production |
| Token count reliability | High if provider-reported; provider counts are what billing is based on, which is what NiceM's cost metric should reflect |
| Tokenizer inspectability | Variable — some providers publish their tokenizer or an open equivalent (e.g., tiktoken for OpenAI-family models); others do not. This matters for the query-tokenization sanity gate (§5 step 1), which runs before API calls |
| Multilingual coverage | Generally strong for Dutch; Turkish coverage is adequate but varies by model family — must be confirmed in a smoke test |
| Cost to run the pilot | Real; at 108 base task instances (benchmark-sizing §10) with a mid-tier model, total cost is likely in the low tens of USD, which is acceptable for a pilot (subject to BS6) |
| Version drift | Real risk — providers update models; pinning to a specific version identifier is required (§9) |
| Hidden provider behavior | Possible — prompt caching, safety filtering, or prompt injection guards may affect completion behavior in ways not fully transparent |
| Suitability for v0.1 | **Suitable** — the realistic cost measurement is directly relevant to NiceM's core metric; the inspectability tradeoff is manageable with a published tokenizer |

### Option B — Open-source/local model with fully inspectable tokenizer

Typical examples: a locally-run model from a major open-weights family, with full tokenizer access via a library like Hugging Face Tokenizers.

| Dimension | Assessment |
|---|---|
| Tokenizer inspectability | Maximum — the tokenizer is the exact object used for both pre-run counting and in-model tokenization; no discrepancy between local estimates and actual token use |
| Reproducibility | High — given version pins and a fixed runtime environment, exact token counts are reproducible |
| No API pricing ambiguity | True — but this is partly a disadvantage: there is no market price to report, so cost-per-successful-completion must be expressed in tokens or compute-time units, which are less directly useful for NiceM's business framing |
| Multilingual competence | Varies widely by model family and size; smaller local models may underperform multilingual tasks and produce inflated failure rates in Turkish — which would corrupt the PASS/FAIL comparison |
| Setup complexity | Non-trivial; requires hardware or cloud instance with enough VRAM; reproducing the setup adds a barrier for later collaborators |
| Suitability for v0.1 | **Suitable as an alternative** — best choice if inspectability and budget control are the priority; requires verifying Turkish competence before committing |

### Option C — Tokenizer-only baseline first, model execution deferred

Run only the query/KB tokenization step (§5 step 1) initially, without any model execution.

| Dimension | Assessment |
|---|---|
| Cost | Essentially zero — tokenizer libraries are free to run locally |
| Value | High as a gate: confirms that the 108 query renderings produce token-tax ratios in the expected range (Dutch ~1.1×–1.4×, Turkish in the literature-expected range) before spending budget; surfaces KB rendering issues early |
| Execution-tax measurement | None — no trajectory metrics, no PASS/FAIL, no cost per successful completion |
| Suitability for v0.1 | **Not standalone** — but **mandatory as the first phase** regardless of which execution option is chosen (see §5) |

---

## 5. Recommended v0.1 staged approach

The core principle is: **spend cheap tokens before expensive ones**.

### Stage 1 — Tokenizer-only baseline (before any model runs)

1. Choose a tokenizer (see §7 requirements). For Option A providers with a published open tokenizer (e.g., tiktoken for OpenAI-family), this can be done locally at zero API cost.
2. Tokenize all 36 × 3 = 108 user query renderings.
3. Tokenize all 8 × 3 = 24 KB document renderings (or their chunked equivalents).
4. Compute per-intent token-tax ratios (Dutch/English, Turkish/English) per the baseline-token-tax §6 conventions.
5. **Sanity check against the literature:** Dutch ratios should fall in the expected European-language range (~1.1×–1.5×, Petrov §3); Turkish ratios should reflect the agglutinative morphological load (no strong Petrov/Ahia headline figure for Turkish, but clearly above Dutch; exact number is a NiceM v0.1 empirical contribution). If either language comes out at 0.9× or 3×, the KB rendering or tokenizer assumption is likely wrong — fix before running the model.
6. Record the token-tax table in the benchmark log before any run begins.

### Stage 2 — Smoke test (3–5 intents, one language condition)

Before the full 36-intent run:
1. Run 3–5 intents in Turkish (the highest-risk condition) under both Agent A and Agent B.
2. Check: does the model produce answers in Turkish? Does Agent B retrieve from the Turkish KB rendering? Are PASS rates non-zero?
3. If Turkish PASS rates are near zero under Agent A (hallucination — expected since the product is fictional) but reasonable under Agent B (retrieval works): proceed.
4. If Turkish PASS rates are near zero under both designs: diagnose (prompt failure, KB quality gap, model Turkish capability) before committing the full budget.
5. Confirm that `translation_used` detection is working and that the model is not silently responding in English on Turkish inputs.

### Stage 3 — Full benchmark execution

Run all 108 (or 216–324 with repetitions) task instances with the chosen model, consistent tokenizer, and full logging schema.

**If no provider/model is chosen yet:** define the selection criteria in §6 and treat Stage 1 (tokenizer-only) as the immediate next step, which is executable now. The model does not need to be chosen to run Stage 1 if a tokenizer equivalent is available locally.

---

## 6. Selection criteria for execution model

A model is suitable for v0.1 if it meets all of the following:

| Criterion | Requirement |
|---|---|
| Multilingual competence | Adequate performance in English, Dutch, and Turkish on short-answer retrieval tasks; confirmed via the §5 smoke test |
| API stability or local runtime | No major version changes anticipated during the benchmark run; version pinning possible |
| Token usage visibility | Provider-reported per-call token counts (input/output) available, or a matching open tokenizer exists for local counting |
| Cost | Pilot estimated at ≤108 base runs + repetitions; total API cost within the project's BS6 budget |
| RAG-compatible prompting | Supports system/user message separation and a context injection pattern adequate for Agent B |
| Low-temperature or deterministic mode | Temperature ≤ 0.2 recommended; full determinism preferred if available (reduces run-to-run nondeterminism in PASS/FAIL) |
| Tokenizer association | A specific tokenizer name and version can be associated with the model version used |
| Version pinning | The specific model version used can be locked in API calls (e.g., via a version-specific model ID, not a "latest" alias) |
| Latency | Consistent enough that `total_latency_ms` per run is meaningful, not dominated by API queue time |
| Independence | No employer, customer, or confidential data is transmitted; synthetic benchmark inputs only (§14, logging-schema) |

---

## 7. Tokenizer requirements

The following must be logged per run and confirmed at setup:

| Field | Requirement |
|---|---|
| `tokenizer_name` | Named tokenizer or the model's associated encoding (e.g., "cl100k_base" for OpenAI GPT-4 family, or the Hugging Face tokenizer config for open-source models) |
| `tokenizer_version` | Explicit version; for open tokenizers, a commit hash or release version; for provider-reported counts, a date-stamped note that counts are provider-side |
| Model association | The tokenizer corresponds to the specific model version used in the run |
| Input counting | Includes system prompt, user message, retrieved context, and any tool-call payloads injected into the model's context |
| Output counting | Completion tokens only (not a re-encoding of input) |
| Retrieval-context counting | Retrieved context is counted as part of the model input, ensuring `retrieved_context_token_count` and the `input_tokens` total are consistent |
| Cached-token handling | If caching applies: log whether it is active, use `billable_tokens` to separate billed from total, and report both (BT4 guidance) |
| Local vs. provider counts | If both local tokenizer and provider-reported counts exist: log both; use provider-reported for cost calculations, local for token-tax ratio calculations, report if they diverge by more than 2% |

---

## 8. Pricing requirements

| Field | Requirement |
|---|---|
| `pricing_version` | A dated identifier for the price table used (e.g., "openai-gpt4o-2025-06-01"); must be logged per run since prices change |
| Input token price | USD per 1K (or 1M) input tokens at the pricing version date |
| Output token price | USD per 1K (or 1M) output tokens (typically higher than input) |
| Cached-token price | If applicable: the discounted rate for cached/repeated prompt segments |
| Retrieval cost | Embedding API calls and vector store queries, if billed separately; log `estimated_retrieval_cost` per run or as a session-level note |
| Tool cost | Negligible in v0.1 (no non-retrieval tools), but log the field as zero |
| Currency | USD; all cost fields and ratios in the same currency |
| Normalization | Cost-per-run in nominal USD; cost ratios across languages always computed at the same pricing version |

---

## 9. Version drift

Model behavior and tokenizer encodings may change between the date a benchmark is designed and the date it is run, and again between runs if the benchmark spans multiple sessions. Version drift invalidates cross-session comparisons silently.

The following fields in the logging schema already address this (logging-schema §3):

- `model_id` — exact model version identifier, not a "latest" alias
- `tokenizer_name` and `tokenizer_version` (logging-schema §4)
- `pricing_version` (logging-schema §7)
- `timestamp` (logging-schema §3)
- `benchmark_version` (logging-schema §3)

**Operational rule:** if the provider updates the model or tokenizer between Stage 2 (smoke test) and Stage 3 (full run), Stage 2 must be re-run on the new version before Stage 3 proceeds. Token-tax ratios computed in Stage 1 carry the tokenizer version; if the tokenizer changed, Stage 1 must be repeated.

---

## 10. Relationship to token-tax

Token-tax ratios computed in this benchmark are **specific to the chosen tokenizer**. They are not universal claims about English, Dutch, or Turkish:

- A different tokenizer would produce different ratios.
- The literature (Petrov, Ahia, Lundin) used different tokenizers and different corpora; NiceM's numbers are expected to be broadly consistent in direction but not identical.
- Any publication or public sharing of v0.1 results must name the tokenizer and model used, as part of the mandatory scope statement (falsification §9, reporting rule 5; baseline-token-tax §12).
- If v0.2 tests a second model family, token-tax must be recomputed from scratch under that model's tokenizer — the v0.1 ratios do not transfer.

---

## 11. Relationship to candidate execution-tax

Candidate execution-tax cannot be interpreted unless token-tax is measured under the same tokenizer/model context as the benchmark run. Three specific failure modes this document prevents:

1. **Residual is not residual.** If the token-tax baseline uses Tokenizer A but the benchmark runs on Model B (with a different tokenizer), the "residual after token-count control" includes a systematic tokenizer bias — it is not a true residual.
2. **Model capability confounds language effects.** If the chosen model performs significantly worse in Turkish (lower PASS rate regardless of retrieval), the Turkish failure-rate gap would look like candidate execution-tax but would actually be model-level language bias. The smoke test (§5 Stage 2) is the gate: if Turkish PASS rates are near zero under both designs, a more capable multilingual model should be chosen before the full run.
3. **Output verbosity is model-style, not language.** Some models produce longer answers than others by default, inflating output token counts independently of language. The temperature setting (≤0.2 recommended), consistent prompt templates across languages (AD7), and possibly a max-length constraint (BT6) reduce this noise.

---

## 12. Open questions (TM1–TM8)

| ID | Question | Status | Notes |
|---|---|---|---|
| TM1 | Which provider/model will v0.1 use? | Open — selection criteria defined in §6 | The actual choice; blocks Stages 2 and 3; does not block Stage 1 if a tokenizer equivalent is available locally |
| TM2 | Is provider-reported token usage sufficient, or should local counting serve as cross-check? | Open, leaning both if feasible | Log both where possible; use provider counts for cost, local for token-tax ratios; report divergences |
| TM3 | What temperature setting should be used? | Open, recommendation ≤ 0.2 | Lower temperature reduces run-to-run nondeterminism; full determinism (temperature=0) is preferred if the provider supports it reliably |
| TM4 | How should model version pinning be handled in API calls? | Open | Use a version-specific model identifier, never a "latest" alias; confirm the provider's version-pinning mechanism before Stage 3 |
| TM5 | How much budget is acceptable for pilot runs (BS6)? | Open | Determines whether 2–3 repetitions per condition are feasible; low-end estimate: ~108 runs × a mid-tier model ≈ low tens of USD; exact budget must be decided before Stage 3 |
| TM6 | What happens if the model performs poorly in Turkish? | Open — mitigation: smoke test gate | If Stage 2 shows near-zero Turkish PASS rates under both designs, options: (a) choose a more capable multilingual model, (b) add a troubleshooting pass in the prompt, (c) defer Turkish to v0.2. Do not proceed to Stage 3 without diagnosing |
| TM7 | Should a cheaper model be used for pilot smoke tests? | Open | A smaller/cheaper model for Stages 1–2 and a better model for Stage 3 is reasonable for budget, but only if: the Stage 1 tokenizer matches the Stage 3 model's tokenizer, and Stage 2 is re-run on the Stage 3 model |
| TM8 | How should embedding model choice be handled for Agent B? | Open | The embedding model used for retrieval in Agent B is separate from the completion model; it has its own tokenizer and cost; its multilingual coverage must be confirmed (non-English queries retrieve from non-English KB renderings under language-matched design); relates to AD2 |

---

## Dependencies and update log

| Document | What changes with this decision |
|---|---|
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 tokenizer/model item noted (pending final provider choice; Stage 1 unblocked) |
| `docs/methodology/baseline-token-tax-calculation-v0.1.md` | BT1/LS4/LG2 now has a staged approach and selection criteria; §13 Stage 1 is executable before model is chosen |
| `docs/methodology/logging-schema-v0.1.md` | No schema change required — all version fields already exist |
| `docs/open-questions.md` | TM1–TM8 added; BT1/LS4/LG2 updated to point here |
| `docs/source-map.md` | tokenizer-model-choice-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10*
