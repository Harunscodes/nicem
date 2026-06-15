# NiceM — Open Questions

This document tracks what is not yet known, not yet proven, and not yet decided. It is a living document. Questions should be moved to resolved when answered with evidence or closed when determined to be out of scope.

---

## Research questions

### On token-tax

- **Q1:** What is the token-tax multiplier for the languages/scripts most relevant to NiceM's target context? (i.e., how many more tokens does an equivalent sentence require in each language compared to English?)
  - *Partially addressed by: Petrov et al., Ahia et al. — figures extracted in the paper notes. For the v0.1 languages (English/Dutch/Turkish), NiceM will measure multipliers directly: `docs/methodology/baseline-token-tax-calculation-v0.1.md` defines the per-intent ratio convention, and §13 step 1 front-loads a query-level token-tax table as a dataset sanity gate before any agent runs.*

- **Q2:** Does token-tax vary across different model providers' tokenizers, or is it consistent across the field?
  - *Status: Open*

- **Q3:** Has token-tax improved over time as newer tokenizers have been released? Is the trend improving or stable?
  - *Status: Open*

---

### On execution-tax (NiceM hypothesis)

- **Q4:** Can execution-tax be measured empirically? What is the methodology?
  - *Status: Open — core hypothesis validation question*

- **Q5:** What share of total tokens in a typical agentic workflow are overhead (orchestration, scaffolding, repeated context) vs. task content?
  - *Status: Open — requires measurement*

- **Q6:** Does execution-tax vary significantly by workload architecture (e.g., single-agent vs. multi-agent, tool-heavy vs. reasoning-heavy)?
  - *Status: Open*

- **Q7:** Is execution-tax reducible without degrading task quality? What architectural changes reduce it?
  - *Status: Open — requires experimentation*

- **Q8:** Do token-tax and execution-tax compound in real workloads? By how much?
  - *Status: Open*

---

### On industry context

- **Q9:** Is tokens-per-watt used as an internal efficiency metric by AI infrastructure operators, or is it primarily a public-facing narrative?
  - *Status: Partially addressed — NVIDIA uses tokens-per-watt and cost-per-token as product comparison metrics across hardware generations (Vera Rubin vs. Blackwell). This is more than a narrative framing; it appears in product specifications and technical blogs. Whether it is used as an internal engineering KPI is not confirmed. See `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md`, S2–S4.*

- **Q10:** Are there existing tools or benchmarks that measure execution overhead in agentic pipelines?
  - *Status: Partially addressed — NVIDIA NeMo Agent Toolkit supports per-step token and timing tracking and bottleneck identification. Langfuse, LangSmith, and Arize Phoenix offer observability at the workflow level. None of these define or measure execution-tax in NiceM's sense — they provide the instrumentation substrate that controlled execution-tax measurement would require. See `docs/sources/industry/nvidia-agents-infrastructure-notes.md` and `docs/sources/agent-evals/`.*

- **Q15:** What are the original NVIDIA / Jensen Huang sources for the following claims that currently appear in chat-derived notes?
  - "Human language is the new programming language" (exact source and quote)
  - "Electrons to tokens" or equivalent AI factory framing (exact source)
  - Performance improvement vs. demand growth argument (exact source and quote)
  - Open-source AI ecosystem framing (exact source)
  - *Status: Open — all four need source verification before citation. See `docs/sources/notes/nvidia-jensen-chat-context.md`.*

---

## Methodology questions before validation

These questions must be answered — or at minimum scoped — before NiceM can run a valid execution-tax measurement experiment. They are not research hypotheses; they are design decisions whose answers determine whether the experiment is sound.

> **Now structured by:** `docs/methodology/nicem-methodology-framework-v0.1.md`. The framework provides working positions on most of these (success definition in §4, evaluation options in §5, trajectory metrics in §6, token-tax/execution-tax decomposition in §7, falsification criteria in §8). The framework *structures* these questions; it does not yet *close* them — each still requires the validation work listed in framework §12 before it is resolved. Status notes below reflect this.
>
> **Roadmap:** the complete methodology layer is sequenced into an executable plan in `docs/methodology/validation-plan-v0.1.md`: remaining practical decisions → dataset construction → quality gates → Stage 1 (tokenizer-only) → Stage 2 (smoke test) → Stage 3 (full exploratory benchmark) → nine-step analysis → pre-registered interpretation.

- **M1:** How should NiceM define successful completion?
  - What counts as success: a correct final answer, a completed workflow, a user-approved outcome, or all three? Does partial completion count? The definition must be precise enough to apply consistently across languages and task types.
  - *Status: First draft resolved — `docs/methodology/success-rubric-v0.1.md` defines the binary success gate (PASS/FAIL), seven minimum criteria, quality bands (Pass-high / Pass-minimal / Fail-recoverable / Fail-critical), multilingual equivalence requirements, failure taxonomy (nine types), and evaluator uncertainty protocol. Still requires empirical calibration (how many human reviews, what quality threshold on real outputs) before use in any benchmark run. Open sub-questions tracked in rubric §13.*

- **M2:** Should success be judged by humans, automated judges, deterministic checks, or a hybrid?
  - Each approach has different cost, scalability, and bias profiles. Human annotation is expensive but reliable. Automated LLM judges are scalable but may be biased toward high-resource languages. Deterministic checks are language-neutral where applicable but require tasks with verifiable outputs.
  - *Status: Resolved — `docs/methodology/evaluation-method-v0.1.md` defines the v0.1 method: deterministic/semi-deterministic fact-set checks as primary evaluator; project-owner human audit layer (all UNCERTAIN cases mandatory, all FAILs recommended at v0.1 scale, sampled PASSes per language); Turkish self-review permitted (project owner's mother tongue); LLM-as-judge optional support only, never sole source of truth; independent bilingual review required before public claims. Calibration sub-questions tracked as EV1–EV7.*

- **M3:** How can NiceM avoid evaluator bias toward English or high-resource languages?
  - An automated judge that rates Turkish agent outputs less reliably than English outputs will produce biased success classifications, making any execution-tax signal untrustworthy. The evaluator's cross-language reliability must be characterized before results are valid.
  - *Status: Mechanism defined, validation pending — framework §5.3 and §11 identify this as the single most dangerous confound. `docs/methodology/evaluation-method-v0.1.md` §9 now defines the operational defenses: language-neutral fact-set checks (no English wording as hidden target), no style penalties, per-language uncertainty and checker-overturn tracking, and a mandatory recalibration gate (falsification §7: >25% UNCERTAIN in any condition) before any cost interpretation. These defenses are designed but not yet empirically validated — that happens during the smoke test and pilot.*

- **M4:** How can NiceM distinguish execution-tax from token-tax in a measurement?
  - If a Turkish-language run uses more total tokens than an English run, is that token-tax (the input was longer), execution-tax (the agent took more steps), or both? NiceM needs a decomposition method to attribute overhead to its source — otherwise token-tax and execution-tax cannot be separately quantified.
  - *Status: Structured, not closed — framework §7 proposes a six-component decomposition (representation/generation = token-tax; retrieval/tool/retry/correction = candidate execution-tax). Task family §9 shows how this decomposition applies concretely to the Product FAQ task family: representation/generation overhead is the known token-tax baseline; retrieval call count, reasoning step count, and retry count are the candidate execution-tax signals. The decomposition is itself a hypothesis.*

- **M5:** Which metrics belong to agent trajectory evaluation, and which to output evaluation?
  - Trajectory metrics (steps taken, tool calls made, retries, tokens per step) measure the execution path. Output metrics (answer correctness, task completion, quality score) measure the endpoint. NiceM needs both, but they require different evaluation methods and must not be conflated.
  - *Status: Structured — framework §3 (endpoint vs. trajectory) and §6 (trajectory metric set) resolve the conceptual split: success/quality gate inclusion; trajectory metrics measure cost. See `docs/sources/agent-evals/tau-bench.md` and `biscuit-agent-evaluation.md`.*

- **M6:** How should retries, tool calls, retrieval calls, and human correction be counted toward execution-tax?
  - A retry that succeeds on the second attempt is more expensive than one that succeeds on the first — but by how much? Should failed intermediate steps count at full weight, half weight, or be excluded from cost-per-successful-completion? The counting rule must be defined before the metric is computed.
  - *Status: Partially structured — framework §6 enumerates the metrics and §7 places retry/tool/correction in the candidate execution-tax bucket, but the explicit weighting/counting rule is still open. `docs/methodology/logging-schema-v0.1.md` resolves the logging side: raw events (retries, error_events, all costs for all runs including failures) are logged per run so that any counting/weighting rule can be applied uniformly at analysis time. The rule itself (e.g., whether failed-run cost enters the cost-per-successful-completion numerator) remains open — see LG5 and LG7.*

- **M7:** What would falsify the execution-tax hypothesis?
  - A well-formed hypothesis must be falsifiable. A candidate falsification condition: if cost-per-successful-completion is statistically equivalent across language conditions after controlling for input token count, execution-tax in the agentic sense does not exist in that architecture. NiceM should specify this condition precisely before running any experiment.
  - *Status: Resolved — `docs/methodology/falsification-and-decision-rules-v0.1.md` pre-registers three hypotheses (H0 no signal, H1 candidate signal, H2 agent-design amplification/reduction), eight evidence patterns constituting a candidate signal, a list of falsifying observations, inconclusive-outcome conditions, measurement-failure stoppers, provisional quantitative thresholds (≥20% residual cost gap, ≥2 trajectory components, ≥5 intents or ≥2 categories, ≥10 PASS runs per condition), a full A-vs-B interpretation matrix, and nine reporting rules. Open calibration sub-questions tracked as FD1–FD7.*

- **M8:** What is the minimum number of languages, tasks, and runs needed for a statistically meaningful execution-tax measurement?
  - Agent behavior is non-deterministic. A single run per language condition is not sufficient. How many runs per cell, how many task types, and how many language conditions are needed to detect an execution-tax effect of a given size?
  - *Status: Open — framework §11 flags small-sample risk and §9 requires multiple languages/designs, but the statistical power calculation (runs per cell for a given effect size) is not yet done. `docs/methodology/benchmark-sizing-v0.1.md` §9 establishes that the formal power calculation requires variance estimates that do not yet exist; the v0.1 pilot (36 intents × 3 languages, exploratory) is designed to produce those estimates as a primary deliverable. M8 stays open until after the pilot.*

- **M9:** Which instrumentation platform should NiceM use for the proof-of-concept measurement?
  - Candidates: Langfuse (open-source, span-level), Arize Phoenix (open-source, OpenTelemetry), LangSmith (LangChain-native), NeMo Agent Toolkit (NVIDIA). The choice depends on the agent framework used and the granularity of per-step attribution needed.
  - *Status: RESOLVED (CONFIRMED 2026-06-14) — lightweight local JSONL/CSV logging for Stage 2: one record per run; minimum required fields from `logging-schema-v0.1.md`; no external observability platform in Stage 2. See `docs/benchmark/v0.1/stage2-decision-plan.md` §4. Langfuse or Arize Phoenix remain candidates for Stage 3 span-level attribution.*

### Task family sub-questions (from task-family-selection-v0.1.md §11)

These questions emerge from the Product FAQ / policy QA recommendation and must be resolved before a dataset can be constructed.

- **TF1:** How many synthetic documents and policy sections are needed for a valid pilot?
  - *Status: Decision made (exploratory) — `docs/methodology/benchmark-sizing-v0.1.md` recommends a Small KB: 6–10 synthetic policy/FAQ documents, 50–100 canonical facts in the structured fact-set; minimum viable proposal is 8 documents / ~75 facts. The binding constraint is the KB quality-control gate (bilingual review + completeness check across three languages), not retrieval realism. Tiny KB rejected (trivial retrieval); Medium KB deferred to v0.2 (review burden infeasible).*

- **TF2:** How many task instances per language condition?
  - *Status: Decision made (exploratory) — benchmark-sizing-v0.1 recommends 30–50 unique intents, each rendered in English, Dutch, and Turkish; minimum viable proposal is 36 intents × 3 languages = 108 task instances, with 2–3 repetitions only if budget allows. This is explicitly exploratory: it produces the variance estimates M8 needs but cannot confirm or refute the execution-tax hypothesis. Open sub-questions tracked as BS1–BS7.*

- **TF3:** How many languages and which ones?
  - *Status: Decision made — `docs/methodology/language-selection-v0.1.md` recommends English, Dutch, Turkish for v0.1. English = high-resource analytic baseline (NOT canonical source — canonical artifact is the structured fact-set). Dutch = near-baseline Latin-script comparison (mild premium, project owner evaluable). Turkish = agglutinative Latin-script condition (moderate-to-high premium, morphological variation probe). Six candidate v0.2 expansion languages ranked: Arabic (1), Hindi (2), Swahili (3), Korean (4), Japanese (5), Finnish (6). Fallback: if Turkish bilingual review is infeasible, v0.1 runs English + Dutch only. Open sub-questions: LS1 (Turkish bilingual reviewer identity), LS2 (Turkish formality register), LS4 (tokenizer/model for baseline measurement).*

- **TF4:** Should knowledge base documents be translated from canonical English or constructed language-specifically from a shared fact-set?
  - *Status: Direction set — retrieval-design-decision §6 and §9 recommend authoring each language KB from the canonical structured fact-set (not translating English prose), with bilingual review and a pre-run KB completeness check. Whether rendering is human-authored or machine-translated-then-reviewed remains open (depends on language selection and reviewer availability).*

- **TF5:** Should retrieval be language-aware (language-matched) or language-neutral (multilingual embeddings)?
  - *Status: Decided (with contingency) — `docs/methodology/retrieval-design-decision-v0.1.md` analyzes three options and recommends: v0.1 uses language-matched retrieval (each language condition retrieves from its own rendering of the canonical fact-set), with KB quality control (author-from-facts, bilingual review, pre-run completeness check) as a hard prerequisite. Language-neutral retrieval is pre-registered as the v0.2 contrast condition. Fallback: if KB quality control proves infeasible, switch v0.1 to a structured-fact-store canonical KB. Results must always be reported per retrieval configuration, never pooled.*

- **TF6:** Should expected answers be expressed as language-neutral structured fact-triples?
  - *Status: Recommended yes — see task family §11 and rubric §6. Structured expected outcomes (JSON-like fact sets) are the mechanism that makes the success check language-neutral.*

- **TF7:** How to prevent English from becoming the hidden canonical version of the knowledge base?
  - *Status: Working answer adopted — the canonical artifact is the structured fact-set; every language KB, including English, is a rendering of it (retrieval-design-decision §9, §10). The English KB has no privileged status. The concrete authoring protocol (who renders, in what order, with what review) is still to be written.*

### Language selection sub-questions (from language-selection-v0.1.md §10)

- **LS1:** Who will perform the bilingual review of the Turkish KB?
  - *Status: Open — must be identified before Turkish KB construction begins; if unavailable, Turkish defers to v0.2*

- **LS2:** What formality register should KB and task prompts use in Turkish?
  - *Status: Open — formal vs. informal affects morphology and tokenization; must be standardized before authoring begins*

- **LS3:** Should Dutch and Turkish task prompts be authored independently or adapted from English prompts?
  - *Status: Direction set — author from fact-set (not translated from English task prompts)*

- **LS4:** Which tokenizer and model will be used as the primary measurement baseline?
  - *Status: RESOLVED — same as TM1: OpenAI GPT-4.1-mini/GPT-4.1 family, confirmed 2026-06-13. See `docs/benchmark/v0.1/tm1-tokenizer-model-decision.md` (tm1-v0.1.1).*

- **LS5:** Should v0.1 include a fourth language (e.g., Spanish) as a near-English control to isolate Dutch-specific effects?
  - *Status: Open — only needed if Dutch-English comparison shows unexpected results; increases KB burden*

- **LS6:** At what fertility threshold does the Turkish condition become a high-token-tax condition vs. a mild-premium condition?
  - *Status: Answered empirically in v0.1 benchmark — no pre-specification needed*

### Benchmark sizing sub-questions (from benchmark-sizing-v0.1.md §12)

- **BS1:** Is 36 intents enough to observe trajectory differences?
  - *Status: Open — answered empirically by the pilot itself*

- **BS2:** How many repetitions are needed per intent/language condition?
  - *Status: Open — depends on run-to-run nondeterminism; 2–3 is a budget-bounded starting point*

- **BS3:** Should simple and conditional tasks be balanced 50/50, or weighted?
  - *Status: Open — affects difficulty-stratified analysis at n=36*

- **BS4:** How many facts per document are ideal?
  - *Status: Open — ~8–12 assumed; too few makes per-document retrieval trivial, too many makes chunks noisy*

- **BS5:** How much manual review is feasible for the project owner plus one Turkish reviewer?
  - *Status: Open — bounds the real upper limit of KB and intent counts; relates to LS1*

- **BS6:** What budget is acceptable for pilot runs?
  - *Status: RESOLVED for Stage 2 (CONFIRMED 2026-06-14, same as TM5) — $25 USD hard cap for the Stage 2 smoke test; stop-and-review at $20. Stage 3 (full-benchmark) budget remains open and depends on Stage 2 per-run cost observations. See `docs/benchmark/v0.1/stage2-decision-plan.md` §8.*

- **BS7:** What variance estimate does M8 need, and does this pilot produce it?
  - *Status: Open — the pilot is designed to produce per-intent and between-intent variance estimates; sufficiency checked after the pilot*

### Logging schema sub-questions (from logging-schema-v0.1.md §15)

- **LG1:** How precise can cost estimates be across model providers?
  - *Status: Open — pricing models differ (caching, batch pricing); `pricing_version` field mitigates but does not solve cross-provider comparability*

- **LG2:** Which tokenizer should define baseline token-tax?
  - *Status: Open — same decision as LS4; model-native vs. fixed reference tokenizer give different token-tax numbers; possibly log both*

- **LG3:** How should retrieval semantic units be counted?
  - *Status: Open — working answer is deduplicated canonical fact IDs; edge cases (partial/paraphrased facts in a chunk) need a counting rule before implementation*

- **LG4:** Should human correction be manually assigned or inferred from traces?
  - *Status: Open — v0.1 leans manual assignment; trace inference is a v0.2 question*

- **LG5:** How should retry events be normalized across agent designs?
  - *Status: Open — overlaps M6; raw error_events are logged so counting rules can be applied uniformly at analysis time*

- **LG6:** Should latency include network time?
  - *Status: Open — proposal: wall-clock latency in v0.1, per-component latency split deferred to v0.2 span-level instrumentation*

- **LG7:** How should failed runs affect cost-per-successful-completion?
  - *Status: Open — overlaps M6 weighting question; schema logs all costs for all runs so both conventions (failed-run cost included vs. excluded) can be computed and reported side by side*

### Agent design sub-questions (from agent-design-selection-v0.1.md §10)

- **AD1:** Should the Direct LLM baseline receive full KB context or no KB context?
  - *Status: RESOLVED (CONFIRMED 2026-06-14) — A1: Direct LLM with the full relevant-language KB rendering in the prompt. Reason: A0 would fail the fictional NiceHome domain because the model should not know NiceHome policies, leaving CPS undefined for Agent A; A1 enables an interpretable cost comparison (long-context prompting vs. retrieval). A0 pre-registered as an optional additional condition in Stage 3 (failure-rate floor check). See `docs/benchmark/v0.1/stage2-decision-plan.md` §5.*

- **AD2:** Should Simple RAG use the same embedding model across languages?
  - *Status: RESOLVED (CONFIRMED 2026-06-14, with TM8) — yes: one multilingual embedding model (`text-embedding-3-small`) is used for EN/NL/TR, keeping the design constant; uneven per-language retrieval quality becomes a measured property, not an experimenter-introduced confound. See `docs/benchmark/v0.1/stage2-decision-plan.md` §6.*

- **AD3:** How many chunks should Simple RAG retrieve (top-k)?
  - *Status: Provisional value set for Stage 2 — `docs/benchmark/v0.1/stage2-smoke-test-run-plan.md` §8 sets `top_k = 3`, fixed across all languages and intents. The INT-031 two-chunk case (D08-S3 + D08-S4) is the stress test: if Agent B fails to retrieve both required chunks at k=3, top_k may need adjustment (applied uniformly across languages, and logged). Confirmed for Stage 2; revisit after the smoke test before Stage 3.*

- **AD4:** Should retries be allowed in v0.1?
  - *Status: Open — single-pass is cleaner but empties the retry column; one bounded retry on retrieval failure would populate it; must be identical across languages either way*

- **AD5:** Should the RAG agent include a validation step?
  - *Status: Open, leaning no — validation belongs to the v0.2 multi-step validation agent; adding it to Agent B blurs the one-dimension A/B contrast*

- **AD6:** How can hidden translation by the model/provider be detected?
  - *Status: Open — output-language checks and trace inspection catch some cases; covert in-model translation may be undetectable and must be stated as a limitation in all v0.1 reporting*

- **AD7:** How are prompts kept equivalent across languages?
  - *Status: Open — render from a language-neutral prompt specification (the fact-set principle applied to prompts); review parallels the KB quality-control gate; relates to LS2*

### Falsification and decision-rule sub-questions (from falsification-and-decision-rules-v0.1.md §11)

- **FD1:** What exact threshold counts as "material" for v0.1?
  - *Status: Open — provisional values in §7 of falsification doc; must be confirmed before benchmark runs, possibly after a 3–5 intent smoke test*

- **FD2:** Should thresholds be cost-based, latency-based, or trajectory-based?
  - *Status: Open, leaning cost-based primary — cost per successful completion is the stated NiceM business metric; trajectory metrics are supporting evidence; priority must be stated before analysis*

- **FD3:** How many intents must show the same direction for a signal?
  - *Status: Provisional: ≥5 intents or ≥2 task categories — depends on between-intent variance; may need adjustment after smoke test*

- **FD4:** Should failure rate be part of candidate execution-tax or reported separately?
  - *Status: Open — currently separate; a high failure rate could indicate execution-tax or evaluation problems, and conflating them is risky*

- **FD5:** Should UNCERTAIN count as failure for business metrics?
  - *Status: Open, leaning yes — an unclassifiable result is not a reliably delivered output; cost_per_successful_completion should exclude UNCERTAIN runs unless resolved by human review*

- **FD6:** How should hidden model translation be handled in Turkish condition results?
  - *Status: Open — stated as a limitation; if translation_used cannot detect covert in-model translation, Turkish results carry an acknowledged confound and must be reported accordingly*

- **FD7:** What minimum PASS count is needed per condition?
  - *Status: Provisional: ≥10 — a smoke test on Agent B × Turkish will indicate whether this is achievable at n=36; if not, AD1 or KB revision must be addressed first*

### Baseline token-tax sub-questions (from baseline-token-tax-calculation-v0.1.md §14)

- **BT1 / LS4 / LG2:** Which model/tokenizer will v0.1 use?
  - *Status: RESOLVED — `docs/methodology/tokenizer-model-choice-v0.1.md` defines the staged approach and rules; TM1 is now CONFIRMED (2026-06-13): OpenAI GPT-4.1-mini/GPT-4.1 family, one family/one tokenizer, accessible locally via `tiktoken` for Stage 1a. See `docs/benchmark/v0.1/tm1-tokenizer-model-decision.md` (tm1-v0.1.1). Remaining TM sub-questions (TM1-a tokenizer encoding name, TM1-b/c model IDs, TM1-d tier, TM8 embedding, TM5 budget) gate Stage 2+, not Stage 1a.*

- **BT2:** How will full prompt tokens be captured?
  - *Status: Open — depends on the M9 instrumentation platform; fallback is per-call input_tokens totals*

- **BT3:** Should expected answers be generated per language or evaluated language-neutrally?
  - *Status: Direction set — language-neutral: expected outcomes are fact-sets (TF6); generation ratios use actual PASS answers*

- **BT4:** How should cached tokens be handled?
  - *Status: Open — proposal: disable caching if possible, else log and report both total and billable ratios*

- **BT5:** Should token-tax be calculated per intent before aggregation?
  - *Status: Direction set — yes, per intent, aggregated by median; mean-vs-median must be fixed before analysis alongside FD thresholds*

- **BT6:** Should output verbosity be constrained to avoid style-driven token differences?
  - *Status: Open — a length/format instruction reduces style noise but itself renders differently per language (AD7); decide at prompt design*

- **BT7:** How should provider-specific pricing be normalized?
  - *Status: Open — overlaps LG1; deferred by the v0.1 single-provider design; pricing_version preserves recomputability*

### Tokenizer and model choice sub-questions (from tokenizer-model-choice-v0.1.md §12)

- **TM1:** Which provider/model will v0.1 use?
  - *Status: RESOLVED — CONFIRMED by project owner 2026-06-13. Decision note `docs/benchmark/v0.1/tm1-tokenizer-model-decision.md` (tm1-v0.1.1): the OpenAI GPT-4.1-mini/GPT-4.1 family (one family, one tokenizer) is the v0.1 tokenizer/model family for both Stage 1 counting and Stage 2/3 execution. v0.1 will not compare multiple tokenizers or model families. Stage 1a is complete. Remaining sub-questions do not block Stage 2: exact tokenizer encoding name (TM1-a, see below), version-pinned model IDs for Agent A/B (TM1-b/c, set at Stage 2 setup), and whether GPT-4.1-mini suffices for Stage 3 or GPT-4.1 is needed (TM1-d, settled by the Stage 2 smoke test).*

- **TM1-a (Stage 1a finding):** Exact tiktoken encoding name for GPT-4.1 family.
  - *Status: PARTIALLY RESOLVED — target encoding is `o200k_base` (confirmed from tiktoken model registry: GPT-4.1-mini and GPT-4.1 both map to `o200k_base`). Network policy in the Stage 1a execution environment blocked `openaipublic.blob.core.windows.net` (tiktoken BPE data host); fallback tokenizer `o200k_base_approx` used (o200k_base regex + BPE heuristic). For authoritative token counts, re-run `scripts/stage1a_tokenizer_sanity_gate.py` in a network-accessible environment. Script auto-switches to exact tiktoken when available. Fallback counts are sufficient for the directional sanity gate and pre-registered Stage 2 planning. Exact encoding name to record in logging schema: `o200k_base`.*

- **TM1-b/c (Stage 2 setup):** Version-pinned model IDs for Agent A (completion) and Agent B (completion + embedding).
  - *Status: RESOLVED (CONFIRMED 2026-06-14) — `response_model_id = gpt-4.1-mini-2025-04-14` (version-pinned snapshot, both agents); `embedding_model_id = text-embedding-3-small` (TM8); `embedding_model_version = not-exposed-by-provider` (no dated embedding snapshot). Pricing CONFIRMED from official OpenAI sources: `pricing_version = openai-2026-06-14`; gpt-4.1-mini input $0.40/1M (0.00040/1K), output $1.60/1M (0.00160/1K); text-embedding-3-small $0.02/1M (0.00002/1K); cached input $0.10/1M recorded for reference. Set in `scripts/stage2_smoke_runner.py` CONFIG via named constants; dry-run revalidated 11/11 PASS, $0 cost, live mode still blocked. See `docs/benchmark/v0.1/stage2-model-pricing-config.md` (s2-model-pricing-v0.1.1). Remaining: reconfirm the snapshot is non-deprecated and rates are current against the live API immediately before the first run.*

- **TM2:** Is provider-reported token usage sufficient, or should local counting serve as a cross-check?
  - *Status: Open, leaning both — log both; provider counts for cost, local for token-tax ratios; report divergences*

- **TM3:** What temperature setting should be used?
  - *Status: Open, recommendation ≤ 0.2 — lower temperature reduces run-to-run nondeterminism*

- **TM4:** How should model version pinning be handled in API calls?
  - *Status: RESOLVED for Stage 2 (2026-06-14) — version-pinned snapshot `gpt-4.1-mini-2025-04-14` is used (not the `gpt-4.1-mini` rolling alias); to be reconfirmed against the live `/v1/models` listing immediately before the run. `pricing_version` (`openai-2026-06-14`) and `response_model_id` are logged per run; a change to either invalidates/relabels prior results (`stage2-model-pricing-config.md` §7). Stage 3 will reapply the same pinning discipline.*

- **TM5:** How much budget is acceptable for pilot runs?
  - *Status: RESOLVED for Stage 2 (CONFIRMED 2026-06-14) — $25 USD hard cap for Stage 2; stop-and-review at $20; estimated actual spend ~$5–10 at GPT-4.1-mini rates. No API call may run unless the budget cap is implemented (programmatic ceiling) or manually enforced. Stage 3 budget separate; same as BS6. See `docs/benchmark/v0.1/stage2-decision-plan.md` §8.*

- **TM6:** What happens if the model performs poorly in Turkish?
  - *Status: Open — smoke test gate; if Stage 2 shows near-zero Turkish PASS under both designs, diagnose before Stage 3: choose a more capable multilingual model, adjust prompts, or defer Turkish to v0.2*

- **TM7:** Should a cheaper model be used for pilot smoke tests?
  - *Status: Open — reasonable for budget, but only if Stage 1 tokenizer matches Stage 3 model tokenizer and Stage 2 is re-run on the Stage 3 model*

- **TM8:** How should embedding model choice be handled for Agent B?
  - *Status: RESOLVED (CONFIRMED 2026-06-14) — OpenAI `text-embedding-3-small` for Agent B Simple RAG; same model across EN/NL/TR; `embedding_model_id` and `embedding_model_version` recorded in logs. Confirmed multilingual coverage; same provider as TM1 completion model; low cost; retrieval scores accessible. See `docs/benchmark/v0.1/stage2-decision-plan.md` §6. Relates to AD2.*

### Dataset specification open questions (from dataset-specification.md §14)

- **DS1:** What should the fictional product brand name be?
  - *Status: Open — "NiceHome" is the working recommendation; alternatives (Velio, Lumio, Karu) keep it fully unrelated to the NiceM research project; decide before canonical-fact-set authoring*

- **DS2:** Should NiceM branding appear inside the fictional product world, or should they remain separate?
  - *Status: Direction set — keep entirely separate; NiceM does not appear inside KB documents; the two brands (NiceM the research project, NiceHome the fictional product) are distinct*

- **DS3:** How many facts should each document contain?
  - *Status: RESOLVED in canonical-fact-set.md (fs-v0.1.0) — 78 facts total: D01:10, D02:9, D03:11, D04:9, D05:8, D06:13, D07:9, D08:9. Supersedes the §4 estimates.*

- **DS4:** Which facts should be simple vs conditional?
  - *Status: Largely resolved at fact level — the fact-set contains ~18 simple, ~32 conditional, ~20 sequential, ~8 exception facts. The mapping of facts to the 12/12/12 intent difficulty tiers remains for intent-set.md authoring.*

- **DS5:** Should subscriptions/pricing be included or avoided to reduce arithmetic noise?
  - *Status: RESOLVED — pricing excluded entirely from the fact-set. Subscription facts (F0401–F0409) describe plans by features and rules (storage duration, trial length, cancellation/change timing), not by price. No arithmetic anywhere in the fact-set.*

- **DS6:** How formal should Turkish and Dutch renderings be?
  - *Status: Open — recommendation is Dutch informal (jij/je) and Turkish polite-informal (siz form without excessive honorifics); to be confirmed and documented as a global default in language-rendering-plan.md*

- **DS7:** Should troubleshooting tasks include ordered steps?
  - *Status: Direction set and reflected in the fact-set — D06 connectivity (F0601–F0604), pairing (F0606–F0608), and the Hub factory-reset (F0806–F0807) sequences are authored as ordered sequential facts with step conditions. Query forms remain a choice for intent-set.md (recommendation: implicit query, explicit expected steps).*

- **DS8:** Should any tasks require combining facts from two documents?
  - *Status: Direction set — include 2–4 cross-document (T5) intents within the 12 troubleshooting/process tier; not a separate category; confirm at intent-set authoring*

### Intent set open questions (from intent-set.md)

- **IS1:** Should a dedicated simple intent for F0110 (live view unavailable when Hub offline) be added to directly test AC4? Currently covered only indirectly.
  - *Status: WAIVED_WITH_LIMITATION for v0.1 — confirmed in quality-gates.md §8 and §14; pre-registered as secondary observation in expected-fact-mapping.md; dedicated intent deferred to v0.2*

- **IS2:** Should a dedicated simple intent for F0612 (Sensor recalibration) be added for D06 non-connectivity coverage?
  - *Status: Open — F0612 is the only D06 fact with no direct intent; low priority given D06 has 13 facts and 5 intents already*

- **IS3:** Should a troubleshooting intent for F0708 (accidental/liquid damage → out-of-warranty service quote) be added to cover D07's damage exclusion path?
  - *Status: Open — currently covered as secondary context in INT-015; may improve D07 depth*

- **IS4:** INT-003 requires all three Sensor measurements. Should "two out of three" be UNCERTAIN or FAIL?
  - *Status: RESOLVED in expected-fact-mapping.md — 2 of 3 = UNCERTAIN (partial, not wrong); ≤1 = FAIL (too incomplete); all 3 + fabricated 4th = FAIL (forbidden claim)*

- **IS5:** INT-025/INT-026 test full ordered sequences. Is exact step order required, or "all steps, substantially correct order"?
  - *Status: RESOLVED in expected-fact-mapping.md — causal order required for all 7 ordered-step intents (steps are causally ordered, not arbitrary lists); wrong order = FAIL; minor phrasing variation = PASS*

- **IS6:** INT-019 refurbished warranty floor — should all three misreadings be pre-registered as FAIL patterns?
  - *Status: RESOLVED in expected-fact-mapping.md — all three explicitly pre-registered: (a) flat 90-day reset, (b) full 2-year reset, (c) no warranty = all FAIL; "longer of remainder or 90 days" required for PASS*

- **IS7:** INT-035 delay vs. loss — is mentioning both remedies acceptable if delay remedy is correctly identified?
  - *Status: RESOLVED in expected-fact-mapping.md — acceptable (PASS) to mention both remedies correctly as long as delay-specific remedy (shipping-fee refund) is identified for the described scenario; stating replacement for delay = FAIL*

### Language rendering open questions (from language-rendering-plan.md §13)

- **LR1:** Should Dutch prose use "u" (formal direct address) or instructional impersonal phrasing?
  - *Status: Direction set — prefer impersonal instructional where natural; fall back to "u" for direct-address contexts; confirm with Dutch-language reviewer before Dutch rendering is frozen*

- **LR2:** Should Turkish prose use formal "siz" or impersonal imperatives?
  - *Status: Direction set — prefer impersonal imperative for procedural steps; "siz" constructions where impersonal reads awkwardly; project owner to confirm during Turkish rendering review*

- **LR3:** Are there cases where Turkish product-name suffix attachment with an apostrophe produces unnatural results?
  - *Status: Open — project owner to flag per-case during review; convention (apostrophe before suffix on foreign proper nouns) is standard Turkish orthography*

- **LR4:** Should section titles be natural translations or controlled literal labels?
  - *Status: Direction set — natural translations; section scope must match across languages but wording should be idiomatic*

- **LR5:** Should fact IDs and chunk IDs be visible in prose KB renderings or only in metadata?
  - *Status: RESOLVED — metadata only, not in prose. Resolves DP2. Chunk ID scheme: `<document_id>-S<section_number>` with metadata blocks stripped when served to agents.*

- **LR6:** Should the Dutch rendering be reviewed by a native Dutch speaker before public claims?
  - *Status: Open and now active — `kb-rendering-nl.md` (kb-nl-v0.1.0) is authored and awaiting independent native Dutch review before freezing or any publication-grade claim; project owner is not a native Dutch speaker. Analogous to LS1 (Turkish bilingual KB review).*

- **LR7:** Is the register guidance in §4 sufficient to prevent English from being systematically more compact than Dutch/Turkish?
  - *Status: Open — deferred to authoring stage; flag if English rendering is substantially shorter per section than Dutch without a clear structural reason*

### Document plan open questions (from document-plan.md §10)

- **DP1:** Should each document have the same number of sections across languages?
  - *Status: Direction set — yes within a document (cross-language parallelism required); no across different documents (section counts vary: D01:4, D02:5, D03:5, D04:5, D05:4, D06:6, D07:5, D08:5)*

- **DP2:** Should fact IDs appear visibly in prose KB renderings or only as metadata?
  - *Status: RESOLVED in language-rendering-plan.md §3 — metadata only, not in prose. Chunk ID scheme `<document_id>-S<section_number>`; metadata blocks stripped before serving content to agents. Resolves LR5.*

- **DP3:** How long should each retrieval chunk be?
  - *Status: Open — chunk boundary is the section (§6); resulting token length varies by section/language (a token-tax effect to measure, not engineer away); confirm no section is too long during rendering*

- **DP4:** Should troubleshooting steps be one chunk or multiple chunks?
  - *Status: Direction set — one chunk per ordered procedure so a full multi-step answer is retrievable together; confirm against DP3 length limits for the longest procedure (connectivity, four steps)*

- **DP5:** Should subscription (D04) and account (D08) documents cross-reference each other?
  - *Status: Direction set — yes, minimally: the cloud-video carve-out (F0809) references that cloud video is governed by the subscription (D04); cross-references are pointers, not duplicated policy facts*

- **DP6:** How much redundancy is allowed across documents?
  - *Status: Direction set — minimal; a policy fact lives in exactly one document/section; cross-document relationships are references, not repetition*

- **DP7:** How will chunk IDs map to fact IDs?
  - *Status: Direction set — each chunk = one document section; proposed scheme `<document_id>-S<section_number>` (e.g., D03-S2) with fact-ID list in rendering metadata; must be identical across languages so semantic_units_retrieved is comparable; finalize in language-rendering-plan.md*

### Query rendering open questions (from query-rendering-plan.md §9)

- **QR1:** Should conditional queries use one sentence or two?
  - *Status: Direction set — two sentences preferred (setup sentence + question); max two sentences; conditional-intent queries must not collapse the condition into the question in a way that answers the question by implication*

- **QR2:** Should troubleshooting queries describe only the symptom, or also what was already tried?
  - *Status: Direction set — symptom only at this stage; adding "already tried X" introduces a variable not in the intent specification; deferred to v0.2 if retry-scenario intents are added*

- **QR3:** Should queries include device names that activate ambiguity controls?
  - *Status: Direction set — yes, where the AC requires it; AC2 (button hold durations) requires the device context to be stated (Hub vs. Plug) so the model can give the correct duration*

- **QR4:** Is a single query sufficient, or should paraphrase variants be authored?
  - *Status: Direction set — one canonical query per intent per language for v0.1; paraphrase robustness addressed by the query variant plan (qv-plan-v0.1.0); variants are optional and designed to run as Stage 1b after Stage 1a is complete. See `docs/benchmark/v0.1/query-variant-plan.md`.*

- **ST1 (Stage 1a finding):** For short Turkish queries (10–20 tokens), is the Turkish token-tax premium near-zero or negative relative to English?
  - *Status: Observed in Stage 1a (2026-06-13) — 6 of 36 Turkish queries show TR/EN < 1.0 and TR < NL. Diagnosed as Turkish syntactic compactness: agglutinative morphology reduces the number of syntactic words in a sentence, partially offsetting the subword-splitting premium. For KB chunks (longer texts), TR > NL holds for 38/39 chunks (median KB TR/EN = 1.37). Pre-registered for Stage 2: do not assume uniform per-intent query token-tax premium for Turkish; short-form queries may have near-zero or negative Turkish query token-tax even when KB chunk token-tax is positive. This does not falsify the token-tax hypothesis; it establishes its scope (more pronounced in longer texts). See `results/stage1a/token_tax_outliers.md` for full analysis.*

- **ST2 (Stage 1a finding):** Does Dutch query token-tax match literature expectations for short query texts?
  - *Status: Observed in Stage 1a — query NL/EN median 1.000 (range 0.857–1.333), which is at the lower end of the Petrov et al. expected range (1.1–1.5). KB NL/EN median is 1.074, closer to expectations. Short queries reduce the signal because Dutch compounds and long forms appear less frequently in short questions than in policy text. Pre-registered for Stage 2 analysis.*

- **QR10:** Should query variants (V2–V5) be created before or after Stage 1a?
  - *Status: Direction set — after Stage 1a and after TM1 is confirmed. `query-variant-plan.md` §11 recommends deferring variant authoring until Stage 1a tokenizer sanity gate passes. Authoring 432 variant texts before the primary benchmark is validated risks rework if the tokenizer, model family, or intent set changes.*

- **QR11:** How many variant types are needed for a meaningful phrasing-sensitivity analysis?
  - *Status: Direction set (provisional) — five variant types (V1–V5) planned; V1=primary controlled, V2=concise natural, V3=context-rich, V4=indirect support-style, V5=alternate natural phrasing. Whether all five are necessary for v0.1 phrasing analysis or whether V2+V3 are sufficient is an open question to resolve before variant authoring begins.*

- **QR12:** Should variant token counts be reported per-variant-type or aggregated as a distribution?
  - *Status: Open — per-variant-type reporting is more interpretable (V2 is systematically shorter across languages; V3 is longer) but adds analysis complexity. `query-variant-plan.md` §7 requires variants to be reported separately from primary renderings and never mixed in headline metrics. Method for per-type vs. distribution reporting to be decided at Stage 1b analysis time.*

- **QR5:** How should queries be stored — one file per language, or one combined file?
  - *Status: RESOLVED — one file per language: `query-rendering-en.md`, `query-rendering-nl.md`, `query-rendering-tr.md`; each has 36 entries in the schema (intent_id, language, query_text, linked_fact_ids, expected_fact_set_id, notes, review_status); all three files now created.*

- **QR6:** Should query texts be versioned separately from the plan?
  - *Status: RESOLVED — yes; files versioned as qr-en-v0.1.0, qr-nl-v0.1.0, qr-tr-v0.1.0; a version bump on one does not force a bump on others unless chunk IDs or fact IDs change.*

- **QR7:** How does query length affect token-tax measurement?
  - *Status: Direction set — queries must be naturally equivalent across languages, not artificially equalized; observed query length differences are part of the token-tax signal; English queries authored with natural clause structures; Stage 1 will produce the first token-tax table.*

- **QR8:** Should Dutch query renderings be reviewed by a native speaker before Stage 1?
  - *Status: Direction set — `query-rendering-nl.md` is now created and structurally verified; for Stage 1 (tokenizer-only) the rendering is sufficient; for Stage 2+ public claims, native Dutch review is required before any publication-grade claim (QR8/LR6 dependency); project owner to decide timing.*

- **QR9:** Should Turkish query renderings be reviewed by the project owner before Stage 1?
  - *Status: RESOLVED — project owner reviewed all 36 Turkish queries on 2026-06-13. Seven phrasing corrections applied (INT-004, 012, 019, 028, 029, 033, 035): naturalness fixes, ownership suffix consistency, controlled term alignment ("değişim ürünü"), and one premise-framing improvement. No meaning errors found. Gate is now PASS in `quality-gates.md` §9b and §12.*

### Evaluation method sub-questions (from evaluation-method-v0.1.md §15)

- **EV1:** What percentage of outputs should receive human review?
  - *Status: RESOLVED for Stage 2 (CONFIRMED 2026-06-14) — audit all Stage 2 outputs manually (PASS, FAIL, UNCERTAIN); no sampling at smoke-test scale. Stage 3 rule (still to confirm before Stage 3): all FAILs + all UNCERTAINs + ≥20% of PASSes per condition, pre-committed before analysis. See `docs/benchmark/v0.1/stage2-decision-plan.md` §7.*

- **EV2:** Should all Turkish outputs be reviewed by the project owner in v0.1?
  - *Status: Open, leaning yes at base scale — full review of the highest-risk condition would also calibrate the checker's Turkish matching rules*

- **EV3:** Should all FAIL and UNCERTAIN cases be reviewed?
  - *Status: UNCERTAIN mandatory; FAIL leaning yes at v0.1 scale — becomes a sampling question only at v0.2 scale*

- **EV4:** Should LLM-as-judge be used at all in v0.1?
  - *Status: Open, leaning minimal — triage value modest at this scale; cross-language bias risk may outweigh it; decide at implementation*

- **EV5:** How should partial success be handled?
  - *Status: Direction set — no partial credit at the gate; partial information preserved in quality_band and failure_type for analysis*

- **EV6:** What evaluator agreement threshold is needed for v0.2?
  - *Status: Open — requires a second rater; define inter-rater agreement before v0.2 scales up or promotes an LLM judge*

- **EV7:** How should public claims be limited without independent review?
  - *Status: Interim rule — all externally shared results carry the label "single-evaluator exploratory pilot; independent review pending," plus standard scope limits*

---

## Definitional questions

- **Q11:** Is NiceM's definition of execution-tax consistent with any existing concept in the literature (e.g., inference overhead, KV cache cost, prompt engineering waste)?
  - *Status: Open — literature review needed*

- **Q12:** Should token-tax in NiceM's framing be restricted to language/script disparity, or expanded to include input modality (code vs. prose, structured vs. unstructured)?
  - *Status: Open — scoping decision*

---

## Strategic questions

- **Q13:** Who is the primary audience for NiceM — AI infrastructure operators, end users, policymakers, or model developers?
  - *Status: Open — affects thesis framing and product direction*

- **Q14:** Is NiceM's contribution primarily a measurement framework, a cost attribution tool, an architectural recommendation, or something else?
  - *Status: Open*

### Theory and mathematical foundations open questions (from nicem-mathematical-foundations-roadmap-v0.1.md §18)

These questions arise from the mathematical formalization layer and cannot be answered by empirical measurement alone. They are relevant to the research thesis, not the v0.1 benchmark execution.

- **TH1:** What is the best formal definition of intent? Intent should be language-neutral (the same intent expressed in Turkish and English should have the same theoretical object *I*), but how to formalize this invariance precisely — especially for intents with complex conditional structure — is non-trivial.
  - *Status: Open — relevant to rate-distortion and Kolmogorov theory branches*

- **TH2:** Should execution-tax include token-tax or remain residual beyond token-tax? The current definition separates them (residual execution-tax after token-tax baseline). But in infrastructure terms (e.g., cost per successful completion), they compound. The right accounting may depend on the specific question being asked.
  - *Status: Open — affects how CPS decomposition is reported; both conventions should be reported side by side in v0.1*

- **TH3:** What is the right unit for intent capacity: per token, per second, per euro, per watt? Different units are appropriate for different stakeholders (model researchers: per token; operators: per second or per euro; infrastructure designers: per watt).
  - *Status: Open — the SIPW (successful intents per watt) formulation is appropriate for infrastructure; per-euro or per-second framing may be clearer for cost attribution*

- **TH4:** How should semantic distortion be measured? The rate–distortion framing requires a distortion measure. For NiceM intents, distortion can be operationalized as the fraction of required conditions lost in compression. But measuring this requires evaluating each compressed rendering against the expected fact mapping, which is expensive.
  - *Status: Open — practical operationalization deferred to after v0.1 pilot; query variants (V2 concise) are the first empirical probe*

- **TH5:** Can a useful lower-bound theorem be stated without assuming too much about the model? A theorem of the form "for any model with context window *W*, if |T_L(I)| > W/2 then reliable execution requires retrieval" would be useful, but requires strong assumptions about model behavior.
  - *Status: Open — promising direction for execution-tax-capacity-theorem-sketch-v0.1.md*

- **TH6:** How should irreducible task complexity be estimated? If intent I₁ is inherently more complex than I₂ (e.g., a multi-condition policy query vs. a simple factual lookup), how do we separate the task-complexity component from the language-induced overhead component in the execution burden?
  - *Status: Open — the 12/12/12 difficulty stratification in the v0.1 intent set is a first attempt; full separation requires controlling for task complexity across conditions*

- **TH7:** How should redundancy be separated into necessary vs. avoidable? The Chaitin framing distinguishes necessary from avoidable overhead, but operationalizing this distinction requires knowing what the minimum-redundancy execution of an intent looks like. This is empirically inaccessible for complex tasks.
  - *Status: Open — lower-bounding avoidable overhead via agent design comparison (A vs. B) is the v0.1 empirical proxy; theory formalization in chaitin-irreducible-execution-complexity-v0.1.md*

- **TH8:** Which theory document should be formalized first? The most valuable next formalization is likely the rate–distortion analysis, because it directly connects to query variant design and the over-compression failure mode that Stage 2 may surface. Alternatively, the execution-tax capacity theorem sketch is highest leverage for the research claim.
  - *Status: Open — provisional recommendation is rate-distortion document first (most directly connected to benchmark design); capacity theorem sketch second (most relevant to the research paper)*

### Stage 2-local rehearsal open questions (from stage2-local-llm-rehearsal-plan.md)

- **LLM1:** Which local provider will be used for Stage 2-local rehearsal?
  - *Status: Open — recommended: Ollama. Decide before implementing `can_run_local_mode`. Install outside the repository.*

- **LLM2:** Which local model will be used for the first local rehearsal run?
  - *Status: Open — recommended: `llama3.2:3b-instruct` (fits 16 GB RAM) or `mistral:7b-instruct` if RAM allows. Must have ≥ 8 K context window for the 39-chunk Agent A prompt. Confirm before running.*

- **LLM3:** Should the 30-run local rehearsal matrix be run, or is one Agent A run sufficient rehearsal before Stage 2-live?
  - *Status: Open — decide after the first local Agent A call passes. If the pipeline works and the log is clean, one run is sufficient rehearsal evidence.*

- **LLM4:** How should local embedding be handled for Agent B local rehearsal?
  - *Status: Open — see plan §8. Options: local embedding via `nomic-embed-text` (Ollama), or lexical retrieval fallback. Decide at implementation time based on available GPU/RAM.*

- **LLM5:** Should a single-run limiter (`--max-live-runs 1` or `--only-run-id`) be added to the runner before any live call?
  - *Status: Open — recommended yes, as part of the local runner changes. A `--max-runs N` flag would enforce the first-run discipline for both local and OpenAI live modes without relying on project owner discipline alone.*

---

## Resolved questions

*(Move questions here when answered, with a brief note on the resolution and the source.)*

| Question | Resolution | Source |
|---|---|---|
| Does token-tax exist? | Yes — established in literature | Petrov et al., Ahia et al., Lundin |
| Is token-tax an API cost problem, not just a tokenization problem? | Yes — pricing is per-token | Ahia et al. |
| Is agentic infrastructure a real and growing industry direction? | Yes — confirmed by NVIDIA and Jensen Huang | Industry sources |
