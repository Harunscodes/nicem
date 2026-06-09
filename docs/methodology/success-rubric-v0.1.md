# NiceM Success Rubric v0.1

**Status:** Internal working document. Not public. Not a benchmark specification.
**Version:** 0.1 — first draft success rubric, addresses methodology question M1
**Scope:** Defines when a run counts as a successful completion, before any execution-cost or execution-tax metric is calculated. Does not define the full benchmark, choose languages, select models, or prove execution-tax.
**Relationship to framework:** This document resolves the working definition introduced in `docs/methodology/nicem-methodology-framework-v0.1.md` §4, and operationalizes the success-gate principle from §3 of that document.

---

## 1. Purpose

NiceM's primary metric is cost per successful completion. That metric has two terms. The cost term — tokens, steps, latency, dollars — is measurable once an instrumentation layer is in place. The *successful completion* term is not mechanically measurable; it is a judgment, and the judgment must be defined before any run is scored.

Without a rubric:
- There is no consistent way to decide whether a run passed or failed.
- Cost comparisons between languages or architectures may include failed runs, making them meaningless or misleading.
- A cheap run that failed is not evidence of efficiency — but without a rubric, it enters the cost calculation as if it were.
- Different evaluators or automated judges will apply different implicit standards, introducing noise or bias into the most important binary in the measurement.

The success rubric is therefore the first methodological requirement before any benchmark runs. It is not the most exciting part of NiceM's research — but it is the foundation on which every execution-tax measurement rests. A rubric that is inconsistently applied, language-biased, or too lenient will corrupt every metric downstream.

This rubric is deliberately conservative. It favors precision over coverage: it is better to classify fewer runs confidently than to classify more runs ambiguously.

---

## 2. Working definition

**A run is successful if it completes the intended task according to a pre-defined language-independent rubric, preserves the required meaning, avoids critical errors, and produces an output or action that would be acceptable to a neutral evaluator.**

Each clause is load-bearing:

- **"completes the intended task"** — the run must resolve the human intent that initiated it. A fluent, well-formed, on-topic response that does not answer the question is a failure.
- **"according to a pre-defined language-independent rubric"** — the standard is set before runs are scored, and the same standard applies regardless of language. The rubric cannot reward English-style outputs or penalize valid linguistic variation in other languages.
- **"preserves the required meaning"** — facts, constraints, and required actions must be communicated accurately. Paraphrasing is acceptable; omission or distortion of required content is not.
- **"avoids critical errors"** — factual errors, missing required steps, unsafe outputs, and irrelevant actions each constitute failure. Minor stylistic imperfections do not.
- **"acceptable to a neutral evaluator"** — the output or action must meet the needs of the intended user in the intended context, as judged by a rater without a stake in any particular language or output style.

**This definition is provisional.** It has known soft spots: "neutral evaluator" is an aspiration, not a guarantee; "critical" versus "minor" error requires case-by-case calibration; "required meaning" must be specified per task type before scoring begins. These soft spots are tracked as open questions in Section 13 and are not resolved by naming them here.

---

## 3. The success gate

**Success is a gate, not the final metric.**

Every run receives one of two gate outcomes:

| Gate outcome | Meaning | Effect on cost-per-successful-completion |
|---|---|---|
| **PASS** | The run completed the intended task according to the rubric | Eligible for execution-cost comparison across languages and architectures |
| **FAIL** | The run did not complete the intended task according to the rubric | Excluded from the cost-per-successful-completion numerator; logged separately as failure cost |

**Why failed runs are still recorded, not discarded:**

A cheap failed run is not efficient. If Language B requires half the tokens of Language A per run, but fails twice as often, its cost-per-successful-completion may be higher than Language A's — not lower. Discarding failures would systematically undercount the true cost of operating in Language B.

Failed runs therefore contribute to two metrics that NiceM must track:
- **Failure rate** (per language condition and architecture) — a component of total execution cost
- **Failure cost** (tokens, steps, latency of failed runs) — contributes to the denominator of a full cost-accounting that includes retries and abandoned attempts

The gate determines *eligibility for the primary metric*; it does not determine whether the run's cost data is recorded. All runs are logged; only passing runs enter the cost-per-successful-completion comparison.

---

## 4. Minimum success criteria

For a run to receive a PASS, it must satisfy all of the following. These are necessary conditions, not a scoring rubric — any single failure disqualifies the run.

| Criterion | Pass condition | Notes |
|---|---|---|
| **Intent satisfied** | The run directly addresses and resolves the stated human intent | The most fundamental criterion; evaluators should ask "would the user consider this task done?" |
| **Required facts/actions completed** | All facts, answers, or actions required by the task are present in the output | Assessed against the pre-defined expected outcome for the task |
| **No critical factual error** | The output contains no factually incorrect claim that would mislead the user or invalidate the response | Minor imprecision tolerated; incorrect core facts disqualify |
| **No missing required step** | All steps in a multi-step task have been completed | Partial completion counts as failure unless partial completion is explicitly defined as acceptable in the task spec |
| **No unsafe or irrelevant output** | The output contains nothing harmful, dangerous, or clearly off-task | Hard failure; safety failures are never borderline |
| **Language meaning preserved** | The semantic content required for the task is communicated in the output language, regardless of stylistic variation | Evaluators must not penalize grammatical or stylistic differences between languages; only meaning loss counts |
| **Output/action usable by target user** | A typical user in the intended context could act on or use the output without correction | Accounts for outputs that are technically correct but practically unusable in context |

These criteria apply identically across all language conditions. An evaluator may not apply stricter standards to one language than another.

---

## 5. Quality bands

Binary PASS/FAIL is sufficient for the primary metric. For richer analysis, runs may optionally be assigned to quality bands.

| Band | Meaning |
|---|---|
| **Pass-high** | Fully satisfies all minimum criteria with high confidence; output is clear, complete, and directly usable |
| **Pass-minimal** | Satisfies all minimum criteria but only marginally; output is usable but may require user effort to apply |
| **Fail-recoverable** | Does not meet minimum criteria, but the failure is shallow — a minor missing step or recoverable factual gap that a follow-up turn might resolve |
| **Fail-critical** | Does not meet minimum criteria due to a fundamental failure — wrong intent, major factual error, missing core action, safety issue |

**For the first benchmark (v0.1):** collapse these into binary PASS/FAIL. Pass-high and Pass-minimal both count as PASS; Fail-recoverable and Fail-critical both count as FAIL. Quality bands are recorded but not used in the cost-per-successful-completion calculation in v0.1.

**Rationale:** Adding quality bands to the v0.1 success gate introduces scoring complexity before the basic binary judgment has been validated for cross-language reliability. The bands are defined now so the logging schema captures them, but they are not used as a gate until the simpler binary judgment is confirmed to work consistently.

---

## 6. Multilingual equivalence

The most important property of this rubric is that it must apply identically across all language conditions. This section makes that concrete.

**Same underlying intent:** Before any run, the intended outcome must be specified in language-neutral terms — not as an English sentence, but as a description of what the agent should accomplish. Example: "The agent correctly identifies the cheapest available option satisfying all stated constraints and communicates it clearly to the user" — not "The agent says 'The cheapest option is…'".

**Same required facts and actions:** The expected outcome is defined as a set of facts or actions that must be present, not as a specific wording. A Turkish-language output that communicates the correct fact in Turkish is a pass; an English-language output that communicates it in English is equally a pass. The evaluator is assessing the *content*, not the form.

**Same acceptance criteria:** The quality floor is the same regardless of language. An output that would barely pass in English should barely pass in Turkish and vice versa. The evaluator must not implicitly apply stricter standards to less familiar languages.

**No advantage for English wording:** The rubric must not contain implicit assumptions that produce higher scores for English-shaped output — e.g., preference for direct sentence structure, particular date formats, or response length conventions that are natural in English but not in morphologically complex languages.

**No penalty for valid linguistic variation:** An agent that produces a grammatically correct, semantically accurate, appropriately polite response in Turkish is not penalized because the response is longer, more formal, or structured differently than an English equivalent. Length, formality, and discourse structure vary across languages; only meaning accuracy is assessed.

**Avoid judging style as correctness:** An output that achieves the task in a culturally or stylistically different way is not a failure. Evaluators should be instructed that style is irrelevant; task completion and factual correctness are the only criteria.

**Validation requirement:** Before using the rubric at scale, NiceM should validate that independent evaluators applying this rubric to the same set of runs across multiple languages produce consistent PASS/FAIL judgments. Systematic disagreement between evaluators on the same language condition is a signal that the rubric is being applied inconsistently.

---

## 7. Evaluation methods

### 7.1 Deterministic checks

Programmatic assertions: exact match on a required value, structured output validation, constraint-satisfaction check, executable test.

- **When useful:** Tasks with verifiable or structured outputs — e.g., "return the cheapest flight under €300" (check: price field ≤ 300, flight field non-null). Any task where the required outcome can be expressed as a predicate on the output.
- **Risk:** Only applicable to tasks with checkable outputs. Cannot assess open-ended quality.
- **Multilingual concern:** Low *if* the check is language-neutral (operates on extracted data, not on strings). High if the check pattern-matches on English text or assumes Latin-script formatting.
- **Relevance to NiceM:** The most reliable success gate available. NiceM should design the v0.1 task family specifically to support deterministic checks wherever possible — this removes evaluator bias from the success gate entirely.

### 7.2 Human evaluation

Trained human annotators score outputs against the rubric defined in Sections 4–6.

- **When useful:** Tasks where output quality cannot be reduced to a predicate — open-ended questions, multi-part responses, actions requiring contextual judgment.
- **Risk:** Expensive and slow; inter-annotator variance; cultural assumptions may leak into judgments.
- **Multilingual concern:** Requires fluent, calibrated annotators per language. Recruiting balanced pools for low-resource languages is hard. Annotator standards may drift across languages even with a shared rubric; periodic cross-annotator calibration is required.
- **Relevance to NiceM:** The validation anchor. Even at small scale, a human-reviewed subset is essential for validating whatever automated evaluation is used — especially to detect cross-language bias in automated judgments. Cannot be replaced entirely by automation in v0.1.

### 7.3 LLM-as-judge

A language model prompted with the rubric scores the output.

- **When useful:** Scalable evaluation of open-ended outputs where human annotation is too expensive for full coverage.
- **Risk:** Inherits the judge model's biases; may be inconsistent across prompt variants; can be misled by fluent but wrong outputs; judges typically perform better on training-distribution inputs.
- **Multilingual concern:** **High and central.** LLM judges perform less reliably on low-resource languages. If the judge is more lenient or more consistent in English than in Turkish or Amharic, it injects a systematic bias into the success gate — failures in one language are classified as passes, inflating apparent success rates and deflating apparent execution cost. This is the most dangerous confound in NiceM's design and must be characterized before any results are trusted.
- **Relevance to NiceM:** Usable only after its cross-language reliability is validated against a human-scored subset. The reliability check must span all language conditions used in the benchmark, not only the high-resource ones.

### 7.4 Agent-as-a-judge

An evaluating agent (with tools, retrieval access, or multi-step reasoning) assesses the run, potentially including intermediate steps.

- **When useful:** Trajectory-level evaluation — assessing whether the agent used the right tools, retrieved relevant information, or reasoned correctly across steps. Also useful for verifying factual claims against a source.
- **Risk:** All LLM-as-judge risks, compounded. The judge agent's own trajectory may vary across languages, introducing additional language-driven variance. Harder to validate and calibrate than a single-shot judge. Its own token cost must be tracked separately and never mixed into the measured run's cost.
- **Multilingual concern:** Same as LLM-as-judge, with additional risk from the judge's retrieval and reasoning steps potentially being language-sensitive.
- **Relevance to NiceM:** Promising for v0.2 trajectory-level success evaluation, but not recommended for v0.1 — too complex to validate reliably before the basic binary judgment is confirmed.

### 7.5 Hybrid evaluation

Deterministic checks where outputs are verifiable; LLM- or agent-judge for open-ended portions; human review on a sampled subset to validate the automated layers.

- **When useful:** The general case — most real tasks have both checkable and non-checkable components.
- **Risk:** More complex to design and maintain than any single-method approach.
- **Multilingual concern:** Reduced relative to automated-only — the human-reviewed subset catches cross-language bias in the automated layers, *provided* the subset is balanced across all language conditions.
- **Relevance to NiceM:** The recommended default. Anchor success on deterministic checks where the task permits; use automated judging where necessary for scale; reserve human scoring for validating the automated layers' cross-language fairness.

---

## 8. Recommended approach for first benchmark

The v0.1 benchmark should be deliberately conservative on evaluation method to avoid confounding evaluation reliability with execution-tax measurement.

**Design principle:** Prefer tasks where success can be determined without a language-sensitive judge. The goal is to make the success gate as language-neutral as possible, so that any cost difference measured between language conditions is attributable to the execution path — not to a biased evaluator.

**Specific recommendations:**

- **Use tasks with deterministic or semi-deterministic success conditions.** Examples: product FAQ retrieval (did the agent return the correct fact?), travel constraint satisfaction (did the agent find an option meeting all stated criteria?), structured data extraction (did the agent extract the required fields?). Avoid open-ended creative or argumentative tasks in v0.1.
- **Define expected outcomes in language-neutral terms** before any run — as a set of required facts, actions, or fields, not as a target string.
- **Use a small human-reviewed sample to audit automated judgments.** A minimum of 10–20% of runs per language condition should be scored by a bilingual human reviewer and compared against the automated judgment. Systematic disagreement indicates evaluator bias.
- **Do not use LLM-as-judge as the primary success gate in v0.1** without first validating its cross-language reliability on the specific task family chosen.
- **Log quality bands** (Section 5) but do not use them in the primary metric calculation in v0.1. Add them to the analysis only after the binary gate is validated.

---

## 9. Failure taxonomy

Not all failures are equivalent. Recording failure type serves two purposes: it enables recovery analysis (could a retry have recovered this?), and it makes the failure rate comparable across language conditions (does one language fail more often for a particular reason?).

| Failure type | Definition |
|---|---|
| **Intent failure** | The run addressed the wrong intent or a different task than the one stated |
| **Factual failure** | The run returned incorrect information that would mislead or harm the user |
| **Missing-step failure** | The run completed part of the task but omitted a required action or fact |
| **Tool-use failure** | The agent called the wrong tool, called it incorrectly, or failed to call a required tool |
| **Retrieval failure** | The agent retrieved irrelevant or insufficient content to support the task |
| **Language/translation failure** | Meaning was lost, distorted, or made ambiguous in the output language (distinct from stylistic variation) |
| **Formatting failure** | The output was structured in a way that makes it unusable in context (e.g., wrong field names, encoding failure, truncation) — logged separately from factual failure |
| **Safety failure** | The output contained unsafe, harmful, or policy-violating content — always a hard FAIL regardless of other content |
| **Evaluator uncertainty** | The evaluator could not confidently apply the rubric; the run is flagged for review rather than assigned PASS or FAIL |

Failure type is recorded for all failed runs. In v0.1, failure type informs analysis but does not affect the primary success gate. If certain failure types cluster in particular language conditions, that is a signal worth investigating — but causality should not be assumed from frequency alone.

---

## 10. Evaluator uncertainty

Evaluators will encounter runs that do not clearly pass or clearly fail. Forcing a binary judgment on an uncertain case introduces noise — a coin-flip disguised as a rubric application.

**Protocol for uncertain cases:**

- Mark the run as **UNCERTAIN** rather than forcing PASS or FAIL.
- Record the specific source of uncertainty (ambiguous intent, borderline factual accuracy, unclear whether a step was completed, etc.).
- Do not include UNCERTAIN runs in the cost-per-successful-completion calculation unless a policy is explicitly set.
- Review UNCERTAIN runs manually before a study is finalized. If a systematic pattern of uncertainty appears in a particular language condition, treat this as a signal of rubric gap or evaluator calibration failure — not as a property of the language.
- Track **uncertainty rate** as its own metric per language condition. A higher uncertainty rate in one language may indicate that the rubric is less well-specified for that language, or that the evaluator is less calibrated for it. Either requires investigation before results are trusted.

**Default policy for v0.1:** UNCERTAIN runs are excluded from both PASS and FAIL counts in the primary metric calculation, but their costs are logged. The uncertainty rate is reported alongside the primary results.

---

## 11. Relationship to execution-tax

This rubric and execution-tax are related in a precise way that must not be conflated.

**The rubric defines which runs are eligible for cost comparison.** Only PASS runs enter the cost-per-successful-completion calculation. This is the gate.

**Execution-tax is measured on the trajectory of PASS runs.** Once a run is classified as successful, NiceM compares its trajectory cost (tokens, steps, retries, latency) across language conditions and architectures. If successful runs in Language B require systematically more trajectory cost than successful runs in Language A, that is the candidate execution-tax signal.

**Failed runs still contribute to total cost.** A language condition with a high failure rate forces more retries to achieve a given number of successful completions. Failure rate is therefore a component of total execution cost, even though failed runs are excluded from the per-successful-completion trajectory comparison.

**The rubric does not measure execution-tax.** It defines the population of runs over which execution-tax is measured. A rubric that incorrectly classifies more runs as failures in one language than another will artificially inflate that language's apparent failure rate and change which runs are eligible for the cost comparison — introducing measurement error without any actual difference in execution-tax.

This is why rubric language-neutrality (Section 6) is not a nicety but a measurement requirement.

---

## 12. What this rubric does not solve

Being precise about what a success rubric accomplishes is as important as what it defines.

- **It does not prove execution-tax.** A well-applied rubric enables measurement. Whether that measurement reveals a cross-language execution cost difference is an empirical question that the rubric does not answer.
- **It does not eliminate evaluator bias.** The rubric reduces bias by specifying criteria explicitly and requiring language-independence. It does not eliminate bias — automated evaluators still carry model biases, and human evaluators carry cultural assumptions. Bias can only be characterized and mitigated, not removed entirely.
- **It does not define the full benchmark.** Language selection, task family choice, agent architecture, run count, instrumentation platform, and statistical analysis method are outside the scope of this document.
- **It does not choose languages, tasks, or models.** Those are separate decisions (see `docs/methodology/nicem-methodology-framework-v0.1.md` §12).
- **It does not solve statistical power.** How many runs per language condition are needed to detect an execution-tax effect of a given size is a separate calculation (M8).

---

## 13. Open questions

These questions are not resolved by this rubric. They are the next layer of design work.

- **What is the minimum acceptable quality threshold?** Section 4 defines necessary conditions, but "critical error" versus "minor imprecision" requires calibration against real outputs. A set of example runs rated by multiple evaluators would establish this threshold empirically.
- **How many human reviews are needed?** The recommendation in Section 8 (10–20% of runs per language condition) is a starting estimate. The right number depends on the observed disagreement rate between human and automated scoring — higher disagreement requires a larger validation sample.
- **Should NiceM use bilingual reviewers?** A reviewer who is fluent in both the task language and English can directly compare the output content across languages, which is more reliable than monolingual evaluation. Whether the logistics of recruiting bilingual reviewers for all language conditions is feasible is an open question.
- **Can an LLM judge be trusted across languages?** This cannot be assumed; it must be tested on the specific task family and language set NiceM uses. The test requires a human-scored reference set spanning all language conditions.
- **Should uncertain cases be excluded or counted as failures?** Section 10 recommends exclusion from the primary metric in v0.1, but this means the PASS and FAIL counts do not account for all runs. An alternative is to count uncertain cases as failures. The right policy depends on the uncertainty rate; if it is high, exclusion may produce a skewed effective sample.
- **How should partial success be treated?** A run that completes 3 of 4 required steps is not a full success — but is it the same as a run that completes 0? The quality bands in Section 5 provide a vocabulary (Pass-minimal, Fail-recoverable), but the policy for how partial completions affect cost-per-successful-completion in v0.1 is not yet set.
- **How should the rubric handle tasks where the correct answer is not uniquely determined?** Some tasks (e.g., "summarize this document") have many acceptable answers. The rubric must either restrict v0.1 to tasks with more determinate answers or develop a principled approach for assessing open-ended outputs without introducing evaluator bias.
