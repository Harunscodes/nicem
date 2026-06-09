# Braintrust — Evals

## Type

Agent evaluation / methodology source — evaluation platform and methodology.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| Braintrust evaluation documentation / blog | Product docs / blog | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

Braintrust is an evaluation platform focused on LLM and agent quality measurement. It emphasizes experiment tracking, scoring, and regression detection across runs. Its approach to defining what "good" looks like for an agent task — and measuring whether a run achieved it — is relevant to NiceM's concept of cost per successful completion: a run should only count as efficient if it actually succeeded.

---

## What this supports

TODO: Add once source is read and verified.

---

## What this does not prove

- That execution-tax exists or is measurable in the way NiceM hypothesizes
- That Braintrust's evaluation approach is the right methodology for NiceM
- Any NiceM-specific claim
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: Braintrust likely addresses scoring methodology, dataset construction, and run-to-run comparison — relevant to how NiceM would define a controlled execution-tax experiment with a fixed intent and variable workload conditions.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: Braintrust's focus on task success and quality scoring maps directly to NiceM's "cost per successful completion" metric — a run that fails cheaply is not efficient, and the evaluation framework must capture success as a prerequisite for cost comparison.

---

## Connection to successful completion

Braintrust's scoring and experiment-tracking approach is directly relevant to NiceM's cost-per-successful-completion metric. Braintrust requires an explicit scorer — a function that determines whether a run met its quality criterion — before cost comparisons across runs are meaningful. This scorer-first design disciplines the NiceM question: you must define successful before you can measure cost-per-successful.

TODO: Confirm whether Braintrust supports custom scorers that can evaluate agent outputs in non-English languages, and whether scorer reliability can be tracked separately per language.

---

## Connection to agent trajectory evaluation

TODO: Confirm whether Braintrust supports step-level evaluation of agent trajectories, or whether it primarily scores final outputs. Trajectory evaluation requires scoring intermediate steps — tool calls, retrieval results, reasoning chains — not only the endpoint.

---

## Risks or limitations for multilingual evaluation

- Braintrust's built-in LLM-based scorers may perform inconsistently across languages. Custom scorers would be required for multilingual evaluation.
- Experiment tracking across language conditions requires careful dataset design — test cases must be genuinely equivalent across languages, not just translated.
- Regression detection may be confounded if model updates affect different languages differently — an improvement in English accuracy might coincide with degradation in Turkish, which a single aggregate score would not reveal.

---

## Notes for NiceM methodology

Braintrust's experiment-tracking and regression-detection approach is useful for NiceM's longitudinal question: does execution-tax change as models, tokenizers, and agent frameworks improve over time? If NiceM establishes a baseline execution-tax measurement, Braintrust-style tracking could monitor whether the gap narrows or widens across model generations.
