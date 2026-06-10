# NiceM Falsification and Decision Rules v0.1

**Status:** Pre-registered — these rules must be fixed before any benchmark run begins
**Addresses:** M7 (falsification criteria) from `docs/open-questions.md`; framework §8 and §12
**Depends on:** `docs/methodology/success-rubric-v0.1.md`, `docs/methodology/logging-schema-v0.1.md`, `docs/methodology/agent-design-selection-v0.1.md`, `docs/methodology/benchmark-sizing-v0.1.md`
**Feeds into:** Pilot analysis, v0.1 reporting, v0.2 planning

**Fixed context for this pre-registration:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 synthetic documents, ~75 canonical facts
- Intents: 36 unique intents × English, Dutch, Turkish
- Agent A: Direct LLM baseline; Agent B: Simple RAG
- Retrieval: language-matched
- Success rubric: PASS / FAIL / UNCERTAIN
- Logging schema: one row per run (logging-schema-v0.1)
- Execution-tax remains a hypothesis

---

## 1. Purpose

Falsification criteria must be defined **before** implementation and analysis, not after. This is the guard against the most common failure mode in exploratory research: choosing the interpretation that fits the result after seeing it.

Without pre-registered decision rules, NiceM faces three specific risks:

1. **Confirmation bias in result interpretation.** If any combination of 36 intents × 3 languages × 2 agent designs can be sliced to show a "pattern," a positive-looking result can always be found in the noise. Pre-defined thresholds remove that freedom.
2. **Premature falsification.** Without stating in advance what would constitute a null result, any result could be reframed as "interesting." A null result is only informative if it was possible in principle to get one.
3. **Overclaiming to stakeholders.** The startup thesis depends on execution-tax being real. The temptation to present preliminary pilot data as proof is real. Pre-registered rules are the commitment mechanism.

This document does not predict what the pilot will find. It defines, before looking at any data, what patterns would be described as a candidate signal, what patterns would be described as a null result, and what conditions would make the results inconclusive or invalid.

---

## 2. Hypotheses

These are stated in advance and are the only hypotheses this pilot is designed to test. Any other question that emerges during analysis is exploratory and must be labeled as such.

### H0 — No distinct execution-tax signal

Observed cross-language differences in cost, latency, or trajectory metrics are fully or mostly explained by:
- representation and generation token-tax (input/output token count differences), or
- evaluator uncertainty (uneven UNCERTAIN rates across language conditions), or
- measurement noise (random variation within the sample size)

Under H0, after controlling for input/output token counts, trajectory metrics (retrieval calls, retries, failures, latency) are not meaningfully higher in any language condition. The workflow adds no language-sensitive overhead beyond what the tokenizer already charges.

### H1 — Candidate execution-tax signal

After accounting for representation/generation token-tax (token count differences between language conditions), at least one language condition shows additional workflow overhead in at least one of the following components:
- extra retrieval calls
- extra irrelevant retrievals (failing to retrieve required facts)
- missing required facts despite retrieval
- extra retries
- higher failure rate
- higher uncertainty rate
- higher latency not proportional to token count
- higher cost per successful completion after token-count control

H1 does not prove execution-tax. It constitutes a *candidate signal* warranting a properly powered v0.2 study.

### H2 — Agent-design amplification or reduction

The cross-language gap in cost, trajectory, or success metrics changes materially between Agent A (Direct LLM) and Agent B (Simple RAG) conditions. Specifically:
- A widening gap (B > A) would suggest that workflow design can amplify language-related cost — retrieval adds language-sensitive overhead.
- A narrowing gap (B < A) would suggest that structured retrieval partially compensates for language-related overhead — a practically important finding for NiceM's product direction.
- An unchanged gap would suggest that workflow design is neutral with respect to language cost in this setup.

H2 is independent of H1. A null H1 result with a strong H2 result (the gap changed between A and B even if both are small) is still informative.

---

## 3. What counts as evidence for a candidate execution-tax signal

A candidate signal requires **at least two of the following patterns**, consistent in direction across **at least two task categories or five intents**, before being described as a signal rather than noise:

| Pattern | Required measure | Condition |
|---|---|---|
| Extra retrieval calls | `retrieval_calls` median higher in one language than another | After excluding runs where `missing_required_fact_count` = 0 in all conditions (to avoid floor effects) |
| Failed retrieval | `missing_required_fact_count` > 0 rate higher in one language | Not explained by KB rendering gaps found in the quality-control check |
| Irrelevant retrieval | `irrelevant_retrieval_count` higher in one language | Normalized by `retrieved_context_semantic_units_count`, not raw tokens |
| Extra retries | `retry_count` > 0 rate higher in one language | If retries are enabled (AD4) |
| Higher failure rate | FAIL rate gap between language conditions | Not attributable to evaluator uncertainty (check `uncertainty_rate` first) |
| Elevated uncertainty | `uncertainty_rate` gap between language conditions | After rubric calibration confirms uniform application |
| Latency above token prediction | Residual latency unexplained by `total_tokens` regression | Per-language and per-design |
| Cost above token prediction | `residual_overhead_after_token_count_control` > 0 | Defined precisely in §7 |

A single metric showing a difference in a single category is **not** described as a candidate signal. It is described as an observation warranting investigation.

---

## 4. What weakens or falsifies the execution-tax hypothesis in this setup

The following patterns, if observed, weaken or refute H1 *in this specific setup* (this task family, these languages, these agent designs, this model):

- **Language cost differences are proportional to token count only.** Cross-language cost differences in Agent B are fully explained by `input_tokens` and `output_tokens` differences — no residual after token-count control.
- **Agent B does not widen or change language gaps relative to Agent A.** The cross-language cost gap is the same under B as under A — retrieval adds cost uniformly and does not interact with language.
- **Retrieval semantic units are equivalent; only raw tokens differ.** `retrieved_context_semantic_units_count` is equal across language conditions but `retrieved_context_token_count` differs — this is token-tax inside the retrieval component, not retrieval-side execution overhead.
- **Failures and uncertainty are evenly distributed across languages.** No language condition has a systematically higher FAIL or UNCERTAIN rate — success is language-neutral in this setup.
- **Translation or KB rendering quality explains the gap.** If the observed gap tracks `kb_rendering_version` differences or `translation_used` flags rather than language conditions, it is a quality-control artifact, not execution-tax.
- **Model behavior dominates language effects.** If the model responds differently to Dutch and Turkish in ways unrelated to retrieval (e.g., shorter answers, different formatting), and these differences explain cost gaps, the effect is model-behavior, not execution-tax.
- **Evaluator uncertainty explains apparent success-rate differences.** If `uncertainty_rate` is higher in one language condition and uncertainty is resolved randomly as PASS or FAIL, apparent failure-rate differences may be rubric artifacts.

**Important:** falsification here is specific. Observing H0 does not prove execution-tax does not exist; it proves execution-tax is not detectable in *this setup*. The right conclusion is that v0.1 found no signal in this task family, these languages, this model, and these agent designs — not that execution-tax as a concept is false.

---

## 5. Inconclusive outcomes

Results must be treated as **inconclusive** — neither supporting H1 nor falsifying it — under these conditions:

| Condition | Reason |
|---|---|
| Fewer than 10 PASS runs in any language condition | Cost-per-successful-completion from fewer than 10 PASS runs is too unstable for comparison |
| `uncertainty_rate` above 25% in any condition | The success gate is not being applied consistently; rubric must be recalibrated before any between-condition comparison |
| Direction of effects is inconsistent across task categories | Some categories show higher Turkish overhead, others show lower; no coherent pattern exists |
| KB quality-control gate was not completed before the run | KB rendering differences are an uncontrolled confound; data is not interpretable |
| Required logging fields are missing for more than 5% of runs | The logging schema was not implemented correctly |
| Provider/model instability during the run | Output quality or behavior changed mid-run in ways not attributable to input language |
| One language condition has too few runs due to failures or abandonment | Comparison across unequal cell sizes at this sample size is unreliable |

Inconclusive results are not failures. They provide information about what must be fixed before v0.2: rubric calibration, KB quality control, logging coverage, or sample-size scaling. Report them as such.

---

## 6. Measurement failure conditions

The following conditions require **stopping analysis and fixing the underlying problem** before any results are examined:

1. **KB rendering quality fails the pre-run completeness check.** If any language rendering cannot answer all five task skeletons from the KB, the language condition is invalid. Do not run it; fix the KB first.
2. **Expected fact-sets are inconsistent across languages.** If the English and Turkish expected fact-sets for the same intent differ in required facts (not just expression), the success gate will give unequal decisions for identical agent behavior. Stop and fix.
3. **The evaluator cannot apply the success rubric reliably.** If a calibration trial (apply the rubric to a small held-out set before the full run) produces >25% UNCERTAIN or obvious inconsistencies, recalibrate the rubric.
4. **Required logging fields are absent.** If the instrumentation platform cannot capture the minimal v0.1 field set (logging-schema §12), the run produces data that cannot answer the pilot's questions. Do not run; fix logging.
5. **Hidden translation cannot be ruled out or flagged for a critical condition.** If there is reason to believe the model is translating Turkish queries to English internally and the `translation_used` flag cannot detect it, the Turkish condition conflates two designs. This is a stated limitation (AD6) — if it becomes a material concern, the run can still proceed with that limitation stated prominently. If it affects more than a small fraction of runs, the Turkish condition results are unreliable.
6. **One language condition has zero or near-zero PASS runs before the full benchmark.** If a smoke test on a small subset shows near-zero success for one language, stop and diagnose (KB gap, prompt failure, retrieval failure) before running the full 36 intents.

---

## 7. Candidate quantitative thresholds

These thresholds are **provisional**. They must be reviewed and confirmed before the benchmark runs. They may require adjustment based on actual pilot variance estimates (M8), but they must not be adjusted after data is examined.

| Threshold | Provisional value | Rationale |
|---|---|---|
| Minimum relative cost gap to report as candidate signal | ≥ 20% difference in `estimated_total_cost` per successful completion between the highest and lowest language condition, after token-count control | 20% is roughly the bottom of the cost-premium ranges in Ahia et al.; below this, sampling noise at n=36 makes interpretation unreliable |
| Minimum number of trajectory components showing a gap | ≥ 2 of the 8 patterns in §3 | One component could be noise; two in the same direction is harder to dismiss |
| Minimum intent consistency | ≥ 5 intents showing the same direction, or ≥ 2 task categories | Prevents a single outlier intent from driving the interpretation |
| UNCERTAIN rate threshold for rubric recalibration | > 25% in any condition | Rubric must be recalibrated before results are analyzed |
| Failure-rate gap threshold for failure analysis | > 20 percentage-point gap between language conditions on FAIL rate | Requires failure-type analysis (rubric §9) before cost interpretation proceeds; a large failure-rate gap may indicate KB or evaluator problems rather than execution-tax |
| Minimum PASS count per condition for cost comparison | ≥ 10 PASS runs | Below this, the cost-per-successful-completion estimate is unstable |

**"Residual overhead after token-count control"** is defined as:
> The difference in median `estimated_total_cost` per run between condition X and the English baseline, **minus** the predicted cost difference based on the observed `total_tokens` ratio between the same conditions.

This operationalizes `residual_overhead_after_token_count_control` from logging-schema §10. The exact formula (median vs. mean, how to estimate the token-cost relationship) must be fixed before data is examined.

---

## 8. Agent A vs Agent B interpretation matrix

| Agent A result | Agent B result | Interpretation |
|---|---|---|
| Language gap present | Language gap similar | Token-tax-dominated; workflow adds cost uniformly; limited evidence for retrieval-side execution-tax. Token-tax finding stands. |
| Language gap present | Language gap wider | Candidate retrieval-side execution-tax signal: workflow design amplifies language-related cost. Warrants H1 investigation. |
| Language gap present | Language gap narrower | RAG may partially compensate for language-related cost; structured retrieval may help lower-resource conditions. Practically important for NiceM product direction. |
| Small or no language gap | Language gap present | RAG introduces language-sensitive overhead that direct generation does not; candidate H1+H2 signal. |
| Small or no language gap | Small or no language gap | No execution-tax or token-tax signal at this scale; H0 supported. Report as null result in this setup. |
| Both designs fail often | Both designs fail often | Benchmark or task design problem. Investigate KB, prompts, evaluator before interpreting cost or language effects. |
| B improves success, increases cost | — | Cost-success tradeoff, not execution-tax. Report as a design-comparison finding. |
| B lowers cost per successful completion | — | Workflow design reduces execution burden in this setup. Positive product-direction signal regardless of language gap. |

Every cell in this matrix is a reportable, honest result. No cell is described as a failure of the project — only a failure of the hypothesis in this setup.

---

## 9. Reporting rules

The following rules govern all v0.1 reporting, regardless of what the pilot finds:

1. **Do not claim execution-tax is proven from v0.1.** The correct language is "candidate execution-tax signal observed" or "no candidate execution-tax signal observed in this setup."
2. **Report token-tax metrics beside all execution metrics.** Every execution-cost comparison must be accompanied by the `token_tax_index` (input/output token ratio vs. English baseline) for the same condition. Execution metrics without token context are uninterpretable.
3. **Report success, failure, and uncertainty rates for every condition.** A cost comparison without success rates is meaningless — a cheap design that fails most intents is not efficient.
4. **Separate raw token effects from semantic retrieval effects.** Every retrieval-volume comparison reports both `retrieved_context_token_count` and `retrieved_context_semantic_units_count`. Differences in the first that are not reflected in the second are token-tax inside retrieval, not retrieval overhead.
5. **State scope limits explicitly and prominently.** Results apply to this task family (Product FAQ / Policy QA), this fictional synthetic KB, these three languages, this model (TBD), these two agent designs, and language-matched retrieval. No broader generalization is supported by v0.1 alone.
6. **Inconclusive results are reported as inconclusive, not as null.** An inconclusive result and a null result are different — an inconclusive result means the measurement was insufficient; a null result means the measurement was adequate but the signal was not there.
7. **Threshold deviations must be declared.** If any pre-registered threshold from §7 must be adjusted before or during analysis, the change, its reason, and its direction must be documented — and results reported under both the original and revised threshold.

---

## 10. Relationship to the startup thesis

The startup thesis (docs/startup/nicem-startup-thesis-v0.1.md) is built on the hypothesis that execution-tax exists and is measurable. The falsification rules here are a commitment to honest evaluation of that hypothesis. Three possible v0.1 outcomes, and their relationship to the thesis:

**A positive signal (H1 or H2 observed):** Supports further validation. A properly powered v0.2 study becomes the credible next step. Appropriate for cautious sharing with advisors or collaborators as "early evidence requiring confirmation." Does not authorize the claim that execution-tax is proven.

**A null signal (H0 supported in this setup):** Does not kill NiceM. It answers: execution-tax is not detectable with this task family, these languages, these agent designs, and this model. The startup question shifts to: which setup does show a signal? That is itself a valuable finding — it narrows the search space and may reveal where execution-tax is most commercially relevant (e.g., it may appear in agentic workflows more complex than simple RAG but not in single-pass retrieval). Null results in preliminary studies are common and do not preclude a larger finding.

**An inconclusive result:** Improves the measurement framework. The pilot surfaces rubric calibration gaps, KB quality issues, logging holes, or variance levels that demand larger samples. These are engineering findings that make v0.2 better-designed. An inconclusive pilot that produces clean variance estimates is not a failure — it is a pilot doing its job.

The business question — can NiceM become a product that measures, explains, and reduces execution overhead — does not require a dramatic positive finding in v0.1. It requires that the measurement framework is sound and that the question is tractable. These rules are what makes the measurement sound.

---

## 11. Open questions (FD1–FD7)

| ID | Question | Status | Notes |
|---|---|---|---|
| FD1 | What exact threshold counts as "material" for v0.1? | Open — provisional values in §7 | Must be confirmed before the benchmark runs, after reviewing pilot-variance feasibility; may be informed by a small smoke-test on 3–5 intents |
| FD2 | Should thresholds be cost-based, latency-based, or trajectory-based? | Open, leaning cost-based primary | Cost per successful completion is the stated NiceM business metric; trajectory metrics are supporting evidence; final priority must be stated before analysis |
| FD3 | How many intents must show the same direction? | Provisional: 5 intents or 2 task categories | Depends on between-intent variance; may need adjustment after smoke test |
| FD4 | Should failure rate be part of candidate execution-tax or reported separately? | Open — currently reported separately | A high failure rate could indicate execution-tax (the workflow cannot complete the intent successfully) or evaluation problems; separating these is conservative |
| FD5 | Should UNCERTAIN count as failure for business metrics? | Open, leaning yes | A result NiceM can't classify is not a reliable delivered output; `cost_per_successful_completion` should exclude UNCERTAIN runs unless they are subsequently resolved by human review |
| FD6 | How should hidden model translation be handled in Turkish condition results? | Open — state as limitation | If `translation_used` cannot flag it, Turkish results carry an acknowledged confound; this must be in any reporting |
| FD7 | What minimum PASS count is needed per condition? | Provisional: 10 | A smoke test on Agent B × Turkish will indicate whether 10 PASSes is achievable at n=36; if not, AD1 (full-KB-in-context for Agent A, or KB quality revision) must be addressed first |

---

## Dependencies and update log

| Document | What changes with this pre-registration |
|---|---|
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 falsification-threshold item resolved; M7 header pointer added |
| `docs/methodology/agent-design-selection-v0.1.md` | §8 interpretation matrix is now in this document; AD cross-references noted |
| `docs/methodology/logging-schema-v0.1.md` | `residual_overhead_after_token_count_control` formula now given a provisional definition in §7 here |
| `docs/open-questions.md` | M7 resolved; FD1–FD7 added |
| `docs/source-map.md` | falsification-and-decision-rules-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10 — Pre-registered before any benchmark run.*
