# NiceM Baseline Token-Tax Calculation v0.1

**Status:** Calculation convention defined — pending tokenizer/model choice (LS4/LG2)
**Addresses:** Framework §12 baseline-token-tax-calculation prerequisite; operationalizes the token-tax side of the framework §7 decomposition
**Depends on:** `docs/methodology/logging-schema-v0.1.md`, `docs/methodology/falsification-and-decision-rules-v0.1.md`, `docs/methodology/agent-design-selection-v0.1.md`, `docs/methodology/language-selection-v0.1.md`
**Grounded in:** `docs/sources/papers/petrov-tokenization-parity.md`, `docs/sources/papers/ahia-tokenization-fairness-api-pricing.md`, `docs/sources/papers/lundin-token-tax.md`
**Feeds into:** Pilot analysis, residual-overhead computation (falsification §7), v0.1 reporting

**Fixed context for this convention:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 synthetic documents, ~75 canonical facts (structured fact-set canonical)
- Intents: 36 unique intents × English, Dutch, Turkish
- Agent A: Direct LLM baseline; Agent B: Simple RAG
- Retrieval: language-matched
- Execution-tax remains a hypothesis

---

## 1. Purpose

Token-tax must be calculated **before** any residual workflow overhead can be interpreted as candidate execution-tax, for one structural reason:

> Every cost, latency, and context metric in this benchmark is downstream of token counts. If Turkish queries, contexts, and answers simply contain more tokens than English ones for the same meaning, then higher Turkish cost is expected from tokenization alone — and attributing it to workflow overhead would be a false positive for the execution-tax hypothesis.

The falsification rules (falsification-and-decision-rules §4) explicitly list "language cost differences are proportional to token count only" as a falsifying observation for H1. That test can only be run if a token-tax baseline exists per language, per intent, computed by a fixed convention. This document defines that convention.

Without this baseline, the pilot cannot distinguish its two layers: token-tax (established in the literature) and candidate execution-tax (the NiceM hypothesis).

---

## 2. Scientific grounding for token-tax

Token-tax is not introduced by NiceM as an unsupported assumption. The repository's academic sources document multilingual tokenization disparities and their consequences:

- **Petrov et al. (NeurIPS 2023)** — `docs/sources/papers/petrov-tokenization-parity.md` — establishes tokenization disparity across 200 languages on parallel text (FLORES-200): equivalent content tokenizes to systematically different lengths by language and script, with premiums from ~1.5× for the cheapest non-English languages to over 15× at the extreme, and shows that byte-level models do not eliminate the disparity. This grounds the *tokenization parity ratio* — the core measurement NiceM adapts in §6 below.
- **Ahia et al. (arXiv 2023)** — `docs/sources/papers/ahia-tokenization-fairness-api-pricing.md` — connects tokenization disparity to API pricing: because providers bill per token, users of underrepresented languages pay more for equivalent content (up to ~4× for Telugu/Amharic), and lose effective context window (unable to fit even one in-context example for the majority of test cases in some languages). This grounds NiceM's cost and context-pressure framing.
- **Lundin et al. (arXiv 2025)** — `docs/sources/papers/lundin-token-tax.md` — names the "token tax" concept, defines the fertility metric (F = tokens/word), and shows that fertility correlates with accuracy degradation (slopes −0.08 to −0.18 per unit fertility on AfriMMLU; fertility explaining 20–50% of accuracy variance) and with training/inference cost. This grounds NiceM's use of fertility as a supporting metric and its expectation that token-tax may also affect success rates, not only cost.

**Together, these papers support token-tax as a representation, cost, latency, context, and sometimes performance issue.**

**What they do not prove:** none of these papers measure agentic workflows. They do not show that languages with higher token-tax also incur more retrieval calls, retries, failures, or correction burden in multi-step systems. That is execution-tax — a NiceM hypothesis to validate, not a finding to import.

The baseline token-tax calculation is therefore required for two reasons at once: to align NiceM's measurement with the established literature, and to avoid mislabeling token-count effects — which the literature predicts — as execution-tax, which it does not.

---

## 3. Definitions

| Term | Definition |
|---|---|
| **Baseline language** | The language whose values serve as the denominator in ratio calculations: English in v0.1. An analytic convention only (see §4). |
| **Language condition** | One of the three benchmark conditions (en/nl/tr): the language of the query, KB rendering, and expected output. |
| **Token count** | Number of tokens a specified text unit produces under the measurement tokenizer (`tokenizer_name`/`tokenizer_version` in the logging schema). |
| **Token-tax ratio** | Token count of a text unit in language X ÷ token count of the semantically equivalent unit in the baseline language, for the same intent. Adapts Petrov's tokenization parity ratio to this benchmark's text units. |
| **Representation overhead** | Extra input-side tokens a language condition requires to express the same intent and context (query + retrieved context + prompt). |
| **Generation overhead** | Extra output-side tokens a language condition requires to express the same answer facts. |
| **Retrieval token overhead** | Extra tokens in retrieved context for one language relative to the baseline, *for the same retrieved semantic units*. A sub-case of representation overhead, isolated because it is easy to misread as retrieval-side execution-tax. |
| **Semantic retrieval unit** | One canonical fact (by fact ID) contained in retrieved context, deduplicated — the tokenizer-independent measure of how much *meaning* was retrieved. |
| **Residual overhead after token-count control** | The portion of a cross-language cost/latency/trajectory difference that remains after the difference predicted by token counts alone is subtracted (provisional formula in falsification §7; method restated in §9 below). |

---

## 4. Baseline principle

**English is the analytic baseline, not the canonical source.**

Ratios need a denominator, and English is the practical choice: it is the literature's reference language (Petrov, Ahia, and Lundin all report premiums relative to English), which makes NiceM's numbers comparable to published findings.

But this is a reporting convention only. The canonical artifact remains the **structured fact-set**. The English KB rendering, English queries, and English expected answers are renderings of that fact-set, exactly like the Dutch and Turkish ones (TF7, language-selection §3). Nothing in the calculation treats English text as ground truth; if a dispute arises about what an intent "really asks," it is resolved against the fact-set, never against the English rendering.

If a future analysis wants a different denominator (e.g., Dutch, or the per-intent minimum), the per-language token counts are logged raw, so any baseline can be recomputed.

---

## 5. What should be tokenized

| Text unit | Logging field | v0.1 status |
|---|---|---|
| User query | `user_query_token_count` | **Required** — the cleanest per-intent token-tax measurement |
| Final answer | `final_answer_token_count` | **Required** — generation overhead |
| Retrieved context (Agent B) | `retrieved_context_token_count` | **Required** — retrieval token overhead, paired with semantic units |
| Full prompt as sent to the model | via `input_tokens` per call | **Required if accessible** — captures prompt-template and instruction overhead per language; if per-call prompt text is not retrievable from the platform, `input_tokens` totals are the fallback |
| System/developer prompt | within `input_tokens` | Nice-to-have as a separate count — needed only if prompt templates differ in token length across languages (they will, since instructions are rendered per language; AD7) |
| Tool call payloads | within `input_tokens`/`output_tokens` | Nice-to-have — Agent B has no non-retrieval tools in v0.1, so this is a v0.2 concern |

Rule: every required unit is tokenized with the **same tokenizer for all three languages** within a run set. Mixed-tokenizer comparisons are invalid (§10).

---

## 6. Token-tax metrics

Proposed measurement conventions. **These are conventions, not universal language properties** — a different tokenizer, task family, or text register would produce different numbers (Petrov's premiums vary widely by tokenizer; Lundin's fertility varies by domain).

| Metric | Definition (per intent, language X vs. English) |
|---|---|
| `input_token_tax_ratio` | `user_query_token_count`(X) ÷ `user_query_token_count`(en) |
| `output_token_tax_ratio` | `final_answer_token_count`(X) ÷ `final_answer_token_count`(en), computed on PASS runs only (a failed answer's length is not a generation-overhead measurement) |
| `retrieval_context_token_tax_ratio` | `retrieved_context_token_count`(X) ÷ `retrieved_context_token_count`(en), **conditioned on equal `retrieved_context_semantic_units_count`** — where semantic units differ, the ratio is not computed (see §7) |
| `total_token_tax_ratio` | (`input_tokens` + `output_tokens`)(X) ÷ same(en), per intent per agent design |
| `billable_token_tax_ratio` | `billable_tokens`(X) ÷ `billable_tokens`(en) — diverges from total ratio when caching/pricing rules apply; v0.2 nice-to-have (logging-schema §13) |
| `token_tax_index` | Aggregate of `total_token_tax_ratio` across intents per language condition (median proposed; mean vs. median to be fixed before analysis — FD-adjacent, see BT5) |

Supporting metric: **fertility** (F = tokens/word, per Lundin) computed from `user_query_token_count` ÷ `input_word_count` where word counts are logged — with the stated caveat that whitespace word counts undercount morphological complexity in agglutinative Turkish, so fertility is reported as context, not as a primary metric.

---

## 7. Semantic-normalized comparisons

Raw token counts are not enough, because the same token count can carry different amounts of meaning across languages — that asymmetry *is* token-tax (Petrov's core finding restated at the level of this benchmark).

The semantic anchors that make cross-language comparison meaningful:

- `intent_id` — the same human intent across all three conditions
- `expected_fact_set_id` — the same required facts for success
- `retrieved_fact_ids` — which canonical facts were actually retrieved
- `retrieved_context_semantic_units_count` — how many distinct canonical facts the retrieved context contained

**The decision rule:** if two language conditions retrieve the **same semantic facts** but one consumes more retrieval tokens, that difference is **token-tax inside the retrieval channel** (representation overhead) — not retrieval-side execution-tax. Retrieval-side execution-tax candidates are differences in the *semantic* layer: more retrieval calls to obtain the same facts, more irrelevant facts retrieved, or required facts missed. This is the dual-reporting rule (retrieval-design-decision §8, logging-schema §5) expressed as a calculation rule.

## 8. Agent A vs Agent B token-tax roles

- **Agent A (Direct LLM)** captures representation and generation token-tax in near-pure form: one model call, no retrieval. Cross-language ratios from Agent A runs are the benchmark's cleanest token-tax estimates and the closest analogue to the literature's parallel-text measurements.
- **Agent B (Simple RAG)** captures representation + generation + retrieval-context token overhead, plus whatever workflow behavior retrieval induces.
- **The comparison is the test:** Agent A establishes the expected token-tax profile per language. If Agent B's cross-language differences exceed what Agent A's token-tax profile predicts — in cost, latency, or non-token trajectory fields — that excess is the candidate execution-tax signal. If Agent B's differences match the token-scaled expectation, H0 is supported (falsification §4).

## 9. Residual overhead after token-count control

Provisional v0.1 method, consistent with falsification §7:

1. **Compute per-language token-tax profile** from Agent A runs and Agent B token fields: input, output, retrieval-context ratios per intent (per §6).
2. **Compute token-scaled expectations.** For cost and latency, estimate the per-token relationship within the English condition (e.g., cost per 1K tokens from the price table; latency per token from English runs), then predict each language condition's cost/latency from its observed token counts.
3. **Compute residuals.** Observed cost/latency minus token-scaled expectation, per intent, per language, per design.
4. **Check non-token trajectory fields independently.** `retrieval_calls`, `irrelevant_retrieval_count`, `missing_required_fact_count`, `retry_count`, `failure_rate`, `uncertainty_rate` are counts and rates, not token quantities — token-tax does not mechanically inflate them. Cross-language differences in these fields are direct candidate-signal evidence (falsification §3).
5. **Apply the falsification thresholds.** A candidate execution-tax signal requires residual differences (step 3) and/or non-token trajectory differences (step 4) meeting the pre-registered §7 thresholds — never raw token expansion alone.

**This method is provisional and exploratory.** The token-cost and token-latency relationships estimated in step 2 are themselves noisy at pilot scale; residuals inherit that noise. v0.1 reports residuals as descriptive quantities with this caveat, not as significance-tested effects.

## 10. Tokenizer/model choice

- Token-tax is a property of a **tokenizer**, not of a language in the abstract. Petrov's premium table differs across the tokenizers it evaluates; NiceM's numbers will be specific to whichever tokenizer is chosen.
- **The measurement tokenizer should match the benchmark model's tokenizer** wherever possible, because that is the tokenizer that actually drives billed cost and context consumption in the runs.
- If multiple model providers are compared later (v0.2 model-router territory), token-tax must be **recalculated per tokenizer** — ratios do not transfer.
- v0.1 uses **one tokenizer and one model** for all conditions and both agent designs. Comparing tokenizers is a legitimate study (Q2 in open-questions) but a different one; mixing tokenizers inside v0.1 would confound every ratio.
- The specific choice is **not made here** — it is the open LS4/LG2 dependency. A secondary fixed reference tokenizer (logging both) remains an option under LG2 if cross-study comparability is wanted later.

## 11. Pricing and cost caveat

Token count is not identical to cost. Providers price input and output tokens differently, discount cached tokens, and may bill tools and retrieval infrastructure separately. Consequences:

- A language with a 1.5× total token ratio does not necessarily have a 1.5× cost ratio — output-heavy vs. input-heavy expansion changes the mix.
- **Token-tax and cost-tax are reported separately.** `total_token_tax_ratio` is the tokenizer-level fact; cost ratios (from `estimated_total_cost` with `pricing_version`) are the economic consequence under one provider's pricing at one point in time. Conflating them would make NiceM's numbers break silently whenever pricing changes.

## 12. Reporting rules

1. **Never report candidate execution-tax without reporting token-tax for the same conditions.** (Restates falsification reporting rule 2 at calculation level.)
2. **Never treat English as the canonical source.** English is the ratio denominator only; correctness disputes resolve against the structured fact-set.
3. **Never call a raw token difference execution-tax.** Token-count differences are token-tax — the literature-grounded layer. Only residuals and non-token trajectory differences are candidate execution-tax.
4. **Always report semantic retrieval units beside retrieval token counts.** Per the dual-reporting rule; a retrieval-token gap with equal semantic units is representation overhead.
5. **Always state scope:** this tokenizer (named and versioned), this model, this task family, this fictional KB, these three languages. Token-tax ratios are not portable claims about languages.

## 13. Minimal v0.1 calculation

The smallest calculation set that must be performed:

1. Tokenize each language version of every user query (36 intents × 3 languages) with the measurement tokenizer — this can be done **before any agent runs**, as a dataset-construction quality check and a first token-tax table.
2. Tokenize final answers from all runs (generation ratios on PASS runs).
3. Tokenize retrieved context for all Agent B runs, paired with semantic-unit counts.
4. Calculate per-intent ratios relative to the English analytic baseline (§6).
5. Aggregate ratios by language condition and task category (median, with spread).
6. Compare token ratios against cost, latency, and trajectory ratios per the §9 residual method, applying the falsification §7 thresholds.

Step 1 is deliberately front-loaded: if the query-level token-tax table shows unexpected values (e.g., Turkish at 1.0× or at 4×), that is checked against the literature's ranges *before* the benchmark runs, as a sanity gate on the dataset rendering.

## 14. Open questions (BT1–BT7)

| ID | Question | Status | Notes |
|---|---|---|---|
| BT1 | Which model/tokenizer will v0.1 use? | Partially resolved — `docs/methodology/tokenizer-model-choice-v0.1.md` defines the staged approach and selection criteria; specific provider/model still to be chosen (TM1) but Stage 1 (§13 step 1) is executable now if a tokenizer equivalent is available locally | |
| BT2 | How will full prompt tokens be captured? | Open | Depends on the M9 instrumentation platform; fallback is per-call `input_tokens` totals |
| BT3 | Should expected answers be generated in each language or evaluated language-neutrally? | Direction set — language-neutral | Expected outcomes are fact-sets (TF6); no expected answer *text* exists to tokenize; generation ratios use actual PASS answers instead |
| BT4 | How should cached tokens be handled? | Open | Caching distorts `billable_tokens`; v0.1 proposal: disable caching if possible, else log and report both total and billable ratios |
| BT5 | Should token-tax be calculated per intent before aggregation? | Direction set — yes, per intent, then aggregate by median | Aggregation choice (mean vs. median) must be fixed before analysis, alongside the FD thresholds |
| BT6 | Should output verbosity be constrained to avoid style-driven token differences? | Open | A max-length or answer-format instruction reduces style noise in output ratios but adds a prompt constraint that itself renders differently per language (AD7); decide at prompt design |
| BT7 | How should provider-specific pricing be normalized? | Open | Overlaps LG1; v0.1 single-provider design defers it; `pricing_version` preserves recomputability |

---

## Dependencies and update log

| Document | What changes with this convention |
|---|---|
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 baseline-token-tax-calculation item resolved (pending LS4/LG2 tokenizer choice) |
| `docs/methodology/falsification-and-decision-rules-v0.1.md` | §7 residual definition now has a step-by-step method here (§9); no change to thresholds |
| `docs/methodology/logging-schema-v0.1.md` | No schema change — all required fields already exist; `token_tax_index` computation now specified |
| `docs/open-questions.md` | BT1–BT7 added; Q1 status updated (figures extracted; NiceM-specific measurement defined) |
| `docs/source-map.md` | baseline-token-tax-calculation-v0.1.md added; Petrov/Ahia/Lundin entries note this document as their methodological application |

---

*v0.1 — 2026-06-10*
