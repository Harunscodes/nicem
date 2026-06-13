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
  - *Status: Structured, not closed — framework §6 defines the trajectory metrics any platform must capture and §10 notes Langfuse/Phoenix as strong span-level candidates; final choice depends on agent framework. `docs/methodology/logging-schema-v0.1.md` §12 now defines the minimal field set the chosen platform must capture — any platform that cannot capture those fields is disqualified. See `docs/sources/agent-evals/` for platform notes.*

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
  - *Status: Open — token-tax component of the execution-tax decomposition depends on this; must be decided before dataset construction*

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
  - *Status: Open — determines repetition count (BS2) and model choice (LS4)*

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
  - *Status: Open — no-context measures retrieval dependence (mostly FAILs expected); full-KB-in-context yields PASS runs for cost comparison; possibly both as A0/A1 sub-conditions, budget permitting (BS6)*

- **AD2:** Should Simple RAG use the same embedding model across languages?
  - *Status: Open, leaning yes — one multilingual embedding model keeps the design constant; uneven per-language quality then becomes a measured property, not an experimenter-introduced confound*

- **AD3:** How many chunks should Simple RAG retrieve (top-k)?
  - *Status: Open — fixed k across languages required; interacts with chunk size and BS4*

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
  - *Status: Partially resolved — `docs/methodology/tokenizer-model-choice-v0.1.md` defines the staged approach (Stage 1 tokenizer-only sanity gate → Stage 2 smoke test → Stage 3 full run), selection criteria (§6), tokenizer requirements (§7), pricing requirements (§8), and version-drift rules. Stage 1 is executable now if a tokenizer equivalent is available locally. Specific provider/model not yet chosen (TM1). Seven open sub-questions TM1–TM8.*

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
  - *Status: Open — selection criteria defined in §6; the actual choice; blocks Stages 2 and 3 but not Stage 1*

- **TM2:** Is provider-reported token usage sufficient, or should local counting serve as a cross-check?
  - *Status: Open, leaning both — log both; provider counts for cost, local for token-tax ratios; report divergences*

- **TM3:** What temperature setting should be used?
  - *Status: Open, recommendation ≤ 0.2 — lower temperature reduces run-to-run nondeterminism*

- **TM4:** How should model version pinning be handled in API calls?
  - *Status: Open — use version-specific model ID, never a "latest" alias; confirm provider's version-pinning mechanism before Stage 3*

- **TM5:** How much budget is acceptable for pilot runs?
  - *Status: Open — same as BS6; ~108 runs × mid-tier model ≈ low tens of USD; decide before Stage 3*

- **TM6:** What happens if the model performs poorly in Turkish?
  - *Status: Open — smoke test gate; if Stage 2 shows near-zero Turkish PASS under both designs, diagnose before Stage 3: choose a more capable multilingual model, adjust prompts, or defer Turkish to v0.2*

- **TM7:** Should a cheaper model be used for pilot smoke tests?
  - *Status: Open — reasonable for budget, but only if Stage 1 tokenizer matches Stage 3 model tokenizer and Stage 2 is re-run on the Stage 3 model*

- **TM8:** How should embedding model choice be handled for Agent B?
  - *Status: Open — embedding model is separate from completion model; its multilingual coverage must be confirmed; relates to AD2*

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

### Evaluation method sub-questions (from evaluation-method-v0.1.md §15)

- **EV1:** What percentage of outputs should receive human review?
  - *Status: Open — audit fraction must be fixed before analysis; all FAILs + all UNCERTAINs + ~20% of PASSes per condition looks feasible at v0.1 scale; confirm against BS5*

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

---

## Resolved questions

*(Move questions here when answered, with a brief note on the resolution and the source.)*

| Question | Resolution | Source |
|---|---|---|
| Does token-tax exist? | Yes — established in literature | Petrov et al., Ahia et al., Lundin |
| Is token-tax an API cost problem, not just a tokenization problem? | Yes — pricing is per-token | Ahia et al. |
| Is agentic infrastructure a real and growing industry direction? | Yes — confirmed by NVIDIA and Jensen Huang | Industry sources |
