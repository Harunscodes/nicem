# NiceM Methodology Framework v0.1

**Status:** Internal research/startup document. Not public. Not a benchmark specification. Not experiment design.
**Version:** 0.1 — first structured measurement framework
**Scope:** This document turns the methodology questions M1–M9 (`docs/open-questions.md`) into a structured way of thinking about how to measure execution-tax — *before* any benchmark is implemented.
**Source boundary:** Token-tax is established (Petrov, Ahia, Lundin). Execution-tax is a NiceM hypothesis. Nothing in this document proves execution-tax; it defines how NiceM would attempt to measure it rigorously enough to validate or falsify the hypothesis.
**M1 follow-up:** The working success definition in §4 is operationalized in `docs/methodology/success-rubric-v0.1.md`, which defines the binary success gate, minimum criteria, quality bands, multilingual equivalence requirements, failure taxonomy, and evaluation method comparison.
**Task family follow-up:** The §12 task-family prerequisite is addressed in `docs/methodology/task-family-selection-v0.1.md`, which compares six candidate families and recommends Product FAQ / policy QA (fictional synthetic knowledge base) as the primary v0.1 task family.
**Retrieval design follow-up:** The TF5 retrieval-design question is analyzed in `docs/methodology/retrieval-design-decision-v0.1.md`: v0.1 uses language-matched retrieval with KB quality control as a hard prerequisite; language-neutral (canonical) retrieval is pre-registered as the v0.2 contrast condition that tests whether execution-tax is architecture-dependent.
**Language selection follow-up:** TF3 is resolved in `docs/methodology/language-selection-v0.1.md`: English (analytic baseline; the structured fact-set is canonical, not English), Dutch, and Turkish for v0.1.
**Sizing follow-up:** TF1/TF2 are given an exploratory resolution in `docs/methodology/benchmark-sizing-v0.1.md`: Small KB (6–10 documents, 50–100 canonical facts) and 30–50 intents × 3 languages; minimum viable proposal 8 documents / ~75 facts / 36 intents / 108 task instances. The pilot's primary statistical deliverable is the variance estimates that the M8 power calculation requires.
**Logging schema follow-up:** The §12 logging-schema item is specified in `docs/methodology/logging-schema-v0.1.md`: one row per run, full field set for the §6 trajectory metrics and the §7 decomposition, dual token/semantic-unit retrieval reporting, and a minimal required field set for v0.1.
**Agent design follow-up:** The §12 agent-designs item is resolved in `docs/methodology/agent-design-selection-v0.1.md`: Agent A (Direct LLM baseline) vs. Agent B (Simple RAG), one model held constant; the A-vs-B delta compared across languages is the pilot's key contrast for whether workflow design amplifies or suppresses language-related cost.
**Falsification follow-up:** M7 and the §12 falsification-threshold item are pre-registered in `docs/methodology/falsification-and-decision-rules-v0.1.md`: H0/H1/H2 hypotheses, eight candidate-signal patterns, provisional thresholds, the A-vs-B interpretation matrix, nine reporting rules. These are locked before any benchmark run.
**Token-tax baseline follow-up:** The §12 baseline-token-tax item is defined in `docs/methodology/baseline-token-tax-calculation-v0.1.md`: per-intent token-tax ratios relative to the English analytic baseline (the structured fact-set remains canonical), semantic-normalized retrieval comparison, the Agent A/B measurement roles, and the residual-overhead-after-token-count-control method. Grounded in Petrov, Ahia, and Lundin; pending the tokenizer/model choice (LS4/LG2).

---

## 1. Purpose

NiceM's central claim — that different languages, task types, prompts, retrieval strategies, tools, and agent designs may require different total workloads to complete the same human intent — is a measurement claim. It can only be supported or refuted by measurement.

A premature benchmark would produce numbers, but not trustworthy ones. If NiceM builds an experiment before resolving how it defines success, how it scores trajectories, how it separates token-tax from execution-tax, and what would falsify its own hypothesis, then any result it produces will be uninterpretable. A measured cost difference between two languages could reflect execution-tax, or token-tax, or evaluator bias, or task inequivalence, or sampling noise — and without a methodology layer, NiceM could not tell which.

This framework exists to make the measurement honest before it is made. It is the discipline layer between the thesis (v0.1) and any future proof-of-concept. Its job is to ensure that when NiceM eventually measures something, the measurement means what NiceM claims it means.

---

## 2. The core measurement problem

NiceM's primary metric is **cost per successful completion**. This metric has two terms, and the denominator is the harder one.

Cost — tokens, calls, latency, dollars — is mechanically measurable. Modern observability tooling (Langfuse, Arize Phoenix, NeMo Agent Toolkit) already captures it at the per-step level.

**Successful completion is not mechanically measurable.** It is a judgment. And until NiceM defines that judgment precisely, language-independently, and reproducibly, it cannot compute its own primary metric.

This is the bottleneck. A cheap failed run is not efficient — so cost is meaningless without success. But "success" for an agentic task in an arbitrary language is exactly the thing that is hard to define without smuggling in bias toward high-resource languages, hidden assumptions about output format, or evaluator preferences that do not generalize.

Therefore: **NiceM cannot measure cost per successful completion until it defines successful completion.** Everything else in this framework follows from that constraint.

---

## 3. Endpoint vs. trajectory

There are two distinct things one can evaluate about an agent run.

**Endpoint evaluation** asks: is the final answer or action correct? Did the agent resolve the intent? This is a property of the output.

**Trajectory evaluation** asks: how did the agent get there? How many steps, model calls, retrievals, tool calls, and retries did it take? How much context did it accumulate? This is a property of the path.

These are orthogonal. Two runs can reach the same correct endpoint via very different trajectories — one direct, one circuitous and expensive. Conversely, two runs can take similar trajectories and reach different endpoints.

**Execution-tax is primarily a trajectory property.** The hypothesis is not that some languages produce wrong answers (that is closer to a token-tax-and-accuracy finding, à la Lundin). The hypothesis is that some languages, for the *same successful endpoint*, require a *more expensive trajectory*. NiceM's distinctive measurement is therefore: hold the endpoint fixed (only count successful runs), then compare trajectory cost across conditions.

This is why endpoint evaluation and trajectory evaluation must be kept methodologically separate. Endpoint evaluation gates which runs count (success filter). Trajectory evaluation measures what those successful runs cost. Conflating them — for example, by letting a quality score absorb both correctness and efficiency — would make execution-tax unmeasurable.

---

## 4. Definition of successful completion

**Working definition (v0.1, provisional):**

> A run is *successful* if it completes the intended task according to a pre-defined, language-independent rubric, without relying on hidden assumptions, and within acceptable quality constraints.

Each clause carries weight:

- **"completes the intended task"** — success is defined relative to the intent, not relative to producing fluent output. An eloquent answer to the wrong question is a failure.
- **"according to a pre-defined rubric"** — the criterion is fixed before runs are scored, not adjusted to fit results. This prevents post-hoc rationalization.
- **"language-independent rubric"** — the same standard of success applies regardless of the language the task was expressed in. The rubric must not implicitly reward English-shaped outputs.
- **"without relying on hidden assumptions"** — the rubric must not assume a particular output format, length, or style that happens to be natural in one language and unnatural in another.
- **"within acceptable quality constraints"** — there is a quality floor below which a run does not count as successful even if it nominally addresses the task.

**This definition is not yet validated.** It is a starting point. It has known soft spots: "acceptable quality constraints" is underspecified, "hidden assumptions" is hard to enforce operationally, and "language-independent" is an aspiration that must be tested rather than asserted. Validating this definition — confirming that it can be applied consistently across languages by different evaluators — is itself a prerequisite research task (see M1, M3).

---

## 5. Success evaluation options

Five approaches to operationalizing the success definition. None is sufficient alone; the right answer is likely a hybrid keyed to task type.

### 5.1 Deterministic checks

Programmatic assertions about the output (exact match, structured-field validation, constraint satisfaction, executable test passes).

- **Strengths:** Fully reproducible, zero evaluator cost per run, no model bias, fast.
- **Weaknesses:** Only applicable to tasks with verifiable or structured outputs. Cannot judge open-ended quality.
- **Multilingual risks:** Low — *if* the check operates on language-neutral artifacts (a booked flight, a returned JSON object, a passed test). High if the check secretly assumes English string matching or Latin-script formatting.
- **Relevance to NiceM:** The gold standard where applicable. NiceM should prefer task families that admit deterministic success checks precisely because they remove evaluator bias from the success filter. This is the cleanest way to gate trajectory measurement.

### 5.2 Rubric-based human evaluation

Trained annotators score outputs against the pre-defined rubric.

- **Strengths:** Can judge open-ended and nuanced quality. The benchmark for what "correct" means.
- **Weaknesses:** Expensive, slow, does not scale to large run counts; inter-annotator variance.
- **Multilingual risks:** Requires fluent annotators per language. Annotator standards may drift across languages even with a shared rubric. Recruiting balanced annotator pools for low-resource languages is hard.
- **Relevance to NiceM:** The validation anchor. Even if NiceM cannot afford human evaluation at scale, a human-scored subset is needed to validate whatever automated method is used — especially to check for cross-language bias.

### 5.3 LLM-as-judge

A single LLM scores the output against the rubric.

- **Strengths:** Scalable, cheap relative to humans, can handle open-ended outputs.
- **Weaknesses:** Inherits the judge model's biases; may be inconsistent; can be gamed by fluent-but-wrong outputs.
- **Multilingual risks:** **High and central.** LLM judges typically perform best in high-resource languages. If the judge is more lenient or more reliable in English than in Turkish or Amharic, it injects a systematic bias directly into the success filter — which would masquerade as execution-tax. This is the single most dangerous confound in NiceM's design.
- **Relevance to NiceM:** Usable only if its cross-language reliability is independently characterized against a human-scored subset. Cannot be trusted blind.

### 5.4 Agent-as-a-judge

An evaluating agent (with tools, retrieval, or multi-step reasoning) assesses the run, potentially including intermediate steps, not just the final output.

- **Strengths:** Can evaluate trajectory correctness, not only endpoint; can verify intermediate claims against sources.
- **Weaknesses:** More complex, more expensive, harder to validate; the judge's own trajectory adds meta-level cost and its own potential errors.
- **Multilingual risks:** All the LLM-as-judge risks, compounded by the judge's own multi-step behavior potentially varying across languages.
- **Relevance to NiceM:** Promising for trajectory-level success judgments, but its reliability must be validated even more carefully than a single-shot judge. Its own token cost must be tracked separately and never folded into the measured run's cost.

### 5.5 Hybrid evaluation

Deterministic checks where outputs are verifiable; LLM- or agent-judge for open-ended portions; human evaluation on a sampled subset to validate the automated layers.

- **Strengths:** Combines reproducibility, scale, and a validation anchor. Most robust overall.
- **Weaknesses:** More complex to design and maintain; requires defining which evaluation method applies to which task component.
- **Multilingual risks:** Reduced, because the human-scored subset can detect cross-language bias in the automated layers — *if* the subset spans all languages.
- **Relevance to NiceM:** The likely default. NiceM should anchor success on deterministic checks where possible, use automated judging where necessary, and reserve human scoring for validation of the automated layers' cross-language fairness.

---

## 6. Trajectory metrics

For each run that passes the success filter, NiceM should record the following. These are the raw materials of execution-tax measurement; they are *descriptive*, and recording them does not assume execution-tax exists.

| Metric | What it captures |
|---|---|
| Input tokens | Tokens consumed across all model calls as input |
| Output tokens | Tokens generated across all model calls |
| Retrieval tokens | Tokens added to context from retrieval |
| Total tokens | Sum of all tokens consumed across the full run |
| Model calls | Number of distinct LLM invocations |
| Retrieval calls | Number of retrieval/search operations |
| Tool calls | Number of external tool/API invocations |
| Agent steps | Number of discrete reasoning/action steps |
| Retries | Number of repeated attempts after a failed or low-confidence step |
| Latency | End-to-end wall-clock time for the run |
| Cost | Total monetary cost (API + infrastructure where attributable) |
| Context expansion | Growth of context-window occupancy across steps |
| Human correction estimate | Estimated or recorded human intervention needed |
| Success/failure | Outcome from the success filter (Section 4–5) |
| Quality score | Graded quality of the successful output (separate from binary success) |

Two design notes:

- **Success/failure is a gate, not a trajectory cost.** It determines whether the run's trajectory metrics enter the cost-per-successful-completion calculation.
- **Quality score is kept separate from success** so that NiceM can distinguish "did it succeed" from "how well" without letting quality silently absorb efficiency differences.

---

## 7. Separating token-tax from execution-tax

This is the methodological crux. The danger is straightforward:

> If Language B's runs cost more than Language A's runs, NiceM must determine whether the difference is explained *only* by token count (token-tax — already established in the literature), or by *additional workflow overhead* (execution-tax — the NiceM hypothesis).

If NiceM measures a total-cost difference and attributes it to execution-tax without controlling for token-tax, it will have proven nothing new — it will have rediscovered token-tax and mislabeled it.

**Proposed decomposition (hypothesis — must be validated):**

| Overhead component | Definition |
|---|---|
| Representation overhead | Extra *input* tokens required to express the equivalent input in this language |
| Generation overhead | Extra *output* tokens required to express the equivalent answer |
| Retrieval overhead | Extra retrieval calls or retrieval tokens triggered by this language condition |
| Tool overhead | Extra tool calls triggered by this language condition |
| Retry overhead | Extra failed or repeated attempts before success |
| Evaluation/correction overhead | Extra human or judge correction burden to reach an acceptable result |

The first two components (representation, generation) are essentially **token-tax** expressed in the agentic setting — they are the known effect, and Petrov/Ahia/Lundin already establish that they vary by language. The last four (retrieval, tool, retry, correction) are the candidate **execution-tax** — the part of the cost difference that is *not* explained by raw token counts on the input/output of a single conceptual call.

NiceM's empirical question becomes precise: **after controlling for representation and generation overhead (token-tax), is there residual cost variation across languages in the retrieval/tool/retry/correction components?** If yes, that residual is the candidate execution-tax signal. If the residual is statistically zero, execution-tax — at least in this decomposition and architecture — does not exist.

This decomposition is itself a hypothesis. It may be that the categories are not cleanly separable (e.g., longer input causes more retries through context exhaustion, blurring representation and retry overhead). Validating that the decomposition is coherent and measurable is a prerequisite, not an assumption.

---

## 8. Falsification criteria

A hypothesis that cannot be falsified is not a research claim. NiceM must state, in advance, what results would weaken or refute execution-tax. The following would each count as evidence against the hypothesis:

- **Cost differences fully explained by token count alone.** If, after controlling for representation and generation overhead (Section 7), the residual cost variation across languages is statistically indistinguishable from zero, then there is no execution-tax beyond token-tax.
- **Trajectories remain equivalent across languages.** If successful runs take the same number of steps, retrievals, tool calls, and retries regardless of language, the trajectory — and thus execution-tax — does not vary.
- **Translation normalization eliminates most measured differences.** If translating all inputs to a common language before execution removes the cost gap, the effect is a representation artifact, not a structural execution property. (This must be weighed against translation introducing its own overhead.)
- **Model choice dominates language effects.** If switching models changes the cross-language cost pattern more than the language itself does, then execution-tax is a transient model limitation rather than a structural property of agentic AI.
- **Evaluator bias explains apparent differences.** If the measured success-rate or quality differences across languages disappear when the success filter is validated against balanced human scoring, the apparent execution-tax was an evaluation artifact.

NiceM should pre-register at least one quantitative falsification threshold (e.g., "residual cross-language cost variation below X% after token-tax control refutes execution-tax in this architecture") before running any experiment. See M7.

---

## 9. Benchmark design implications

This framework constrains any future benchmark, without designing it here:

- **Use neutral synthetic tasks** — fictional smart-home FAQ, travel assistant, research assistant, public document Q&A. No employer, customer, or internal data.
- **Use fixed human intents** — the same intent expressed across all language conditions, so the endpoint is held constant and only the trajectory varies.
- **Use language-independent rubrics** — success criteria that do not implicitly reward English-shaped outputs.
- **Compare multiple languages** — spanning the token-tax spectrum (a low-premium language, English baseline, and at least one high-premium language from the Petrov/Ahia studies).
- **Compare multiple agent designs** — so execution-tax can be attributed to architecture as well as language.
- **Separate endpoint success from trajectory cost** — success gates inclusion; trajectory metrics measure cost.
- **Prefer deterministic-checkable task families** — to remove evaluator bias from the success filter wherever possible.
- **Avoid employer/customer/internal data** — independence and safety constraint (see `CLAUDE.md`).

---

## 10. Relationship to existing agent-evaluation sources

The agent-evaluation sources in `docs/sources/agent-evals/` provide methodology *components*. None of them answers NiceM's execution-tax question; each contributes a piece NiceM can borrow.

- **Biscuit** — the scenario/capability/automated-check structure is the organizing template for NiceM's experiment design. Provides: how to structure fixed-intent scenarios and uncertainty handling.
- **τ-bench** — a rigorous multi-step, tool-using benchmark with multi-turn success criteria. Provides: a model for endpoint-success definition over realistic trajectories.
- **LangSmith** — dataset-based evaluation and run comparison. Provides: a controlled-comparison and regression-tracking pattern.
- **Langfuse** — open-source, span-level tracing. Provides: a candidate instrumentation layer for the Section 6 trajectory metrics.
- **Braintrust** — scorer-first evaluation and experiment tracking. Provides: the discipline of defining the scorer before measuring, and longitudinal tracking across model versions.
- **Arize Phoenix** — open-source, OpenTelemetry span attribution. Provides: a candidate instrumentation layer with step-type decomposition for Section 7.
- **Agent-as-a-Judge** — automated, potentially trajectory-level scoring. Provides: a candidate (but bias-risky) success-evaluation method for Section 5.
- **NVIDIA agent evaluation / NeMo Agent Toolkit** — infrastructure-level workflow profiling. Provides: industry context that per-step token/timing instrumentation exists; not a methodology for cross-language comparison.

**What they do not replace:** none of these defines success language-independently, none decomposes token-tax from execution-tax, and none asks whether trajectory cost varies by language for a fixed intent. That question — and that decomposition — is NiceM's contribution. The existing sources are the toolbox; the execution-tax question is the experiment NiceM builds with them.

---

## 11. Open methodology risks

- **Evaluator language bias** — automated judges may score high-resource languages more reliably, injecting bias into the success filter. The most dangerous confound (Section 5.3).
- **Translation artifacts** — translating tasks across languages may introduce inequivalence in difficulty, ambiguity, or retrieval tractability that is not the language effect NiceM intends to measure.
- **Task equivalence across languages** — a task described "identically" in two languages may not be genuinely equivalent. Hard to guarantee, easy to assume.
- **Small sample sizes** — agent behavior is non-deterministic; too few runs per cell will not distinguish an execution-tax signal from noise.
- **Model/version drift** — model updates during a study can change cross-language patterns, confounding longitudinal comparison.
- **Prompt sensitivity** — small prompt changes can swing agent behavior; results may be artifacts of a particular prompt rather than the language.
- **Unclear human-correction estimates** — "human correction burden" is conceptually important but operationally fuzzy; quantifying it consistently is unsolved.
- **Difficulty attributing causality** — even a clean residual cost difference does not by itself prove *why* it occurs; causal attribution requires careful controlled variation, not just observation.

---

## 12. Next steps before implementation

Before any proof-of-concept benchmark is built, the following must be resolved. None of these is code; all are design decisions.

- [ ] **Finalize success rubric** — operationalize the Section 4 definition into an applicable, language-independent scoring rubric (resolves M1).
- [ ] **Choose neutral task family** — select synthetic tasks, preferring those with deterministic success checks (Section 9).
- [x] **Choose initial languages** — resolved: English, Dutch, Turkish (`docs/methodology/language-selection-v0.1.md`); Turkish bilingual review is a prerequisite, with an English+Dutch fallback.
- [x] **Size the KB and task set** — exploratory resolution: Small KB + 30–50 intents × 3 languages (`docs/methodology/benchmark-sizing-v0.1.md`); pending dataset construction.
- [x] **Choose initial agent designs** — resolved: Agent A (Direct LLM baseline) and Agent B (Simple RAG), differing in exactly one architectural dimension so the A-vs-B delta per language is attributable (`docs/methodology/agent-design-selection-v0.1.md`); Agents C–F (translation-first, language-aware, prompt-compressed, model-router) deferred to v0.2 as intervention arms.
- [x] **Define logging schema** — resolved: `docs/methodology/logging-schema-v0.1.md` specifies identifiers, input/retrieval/trajectory/token-cost/output/success fields, derived metrics, the field-to-decomposition mapping, and the minimal v0.1 field set; pending implementation against the chosen instrumentation platform (M9).
- [x] **Define baseline token-tax calculation** — resolved: `docs/methodology/baseline-token-tax-calculation-v0.1.md` defines the text units to tokenize, the per-intent ratio metrics (grounded in Petrov/Ahia/Lundin), the semantic-normalization rule, the Agent A/B roles, and the residual-overhead method; pending the LS4/LG2 tokenizer/model choice.
- [ ] **Decide human vs. automated evaluation** — choose the Section 5 approach (likely hybrid) and define the human-scored validation subset.
- [x] **Define falsification threshold** — resolved: `docs/methodology/falsification-and-decision-rules-v0.1.md` pre-registers H0/H1/H2, eight evidence patterns, falsifying observations, inconclusiveness conditions, measurement-failure stoppers, provisional quantitative thresholds, the A-vs-B interpretation matrix, and nine reporting rules. Must be confirmed before benchmark runs.

Only once these are settled should NiceM consider a minimal proof-of-concept. The PoC's purpose will be to validate or falsify execution-tax — not to assume it.

---

*This document is v0.1. It defines how NiceM should think about measurement. It does not measure anything, does not implement anything, and does not claim execution-tax is proven. Next: resolve the Section 12 checklist, then design a minimal PoC.*
