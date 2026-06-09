# Agent-as-a-Judge

## Type

Agent evaluation / methodology source — evaluation methodology using LLM agents to assess other agent outputs.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| "Agent-as-a-Judge" — paper or blog | Academic paper / blog | TODO: confirm source | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

Agent-as-a-Judge refers to the methodology of using an LLM or LLM agent to evaluate the output of another agent — assessing correctness, completeness, and quality without requiring human annotation for every run. This is relevant to NiceM because NiceM's cost-per-successful-completion metric requires a definition of "successful" — and at scale, human evaluation of every run is not feasible. Agent-as-a-Judge is one candidate methodology for automated success scoring.

---

## What this supports

TODO: Add once source is read and verified.

---

## What this does not prove

- That execution-tax exists or is measurable
- That automated judging is reliable enough for NiceM's purposes (this is an open question)
- That agent-judged success scores are equivalent to human-judged success scores
- Any NiceM-specific claim
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: Agent-as-a-Judge is relevant to the scalability of NiceM's execution-tax measurement. If NiceM runs the same intent across many language/architecture combinations, automated success scoring is necessary. The methodology's reliability and biases are directly relevant to the validity of NiceM's cost-per-successful-completion metric.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: Execution-tax measurement requires knowing whether a run succeeded. Agent-as-a-Judge is a candidate mechanism for making that determination at scale. However, if the judge itself introduces token overhead (it is an agent call), this adds to the measurement infrastructure cost — a meta-level execution-tax consideration.

---

## Connection to successful completion

Agent-as-a-Judge is a candidate methodology for NiceM's success criterion at scale. NiceM's cost-per-successful-completion metric requires a reliable, scalable way to determine whether a run succeeded — human annotation on every run is not feasible for a benchmark across multiple languages, tasks, and architectures.

The key risk: if the automated judge is itself an LLM, its reliability across languages must be validated. A judge trained predominantly on English may score non-English outputs inconsistently, introducing systematic bias into the success classifications that NiceM's metric depends on.

---

## Connection to agent trajectory evaluation

Agent-as-a-Judge can potentially evaluate not only the final output but also intermediate steps — whether the agent reasoned correctly, called the right tools, retrieved relevant content. This makes it relevant to trajectory evaluation, not only endpoint scoring.

However, trajectory-level judging is more complex than output-level judging, and reliability across step types and languages needs separate validation.

---

## Risks or limitations for multilingual evaluation

- LLM judges tend to perform better in high-resource languages. A judge evaluating Turkish or Arabic agent outputs may be less reliable than one evaluating English outputs, introducing bias into NiceM's success classifications.
- If the judge is more lenient in some languages than others, NiceM's execution-tax measurement will be confounded: apparent differences in success rates may reflect judge inconsistency, not genuine task completion differences.
- The judge itself is an agentic call with token cost — adding it to the measurement infrastructure introduces a meta-level overhead that should be tracked.
- There is no language-neutral, validated Agent-as-a-Judge benchmark for multilingual agent evaluation yet (as of the knowledge available here). NiceM may need to develop or adapt one.

---

## Notes for NiceM methodology

NiceM needs a scalable success criterion for its execution-tax benchmark. Agent-as-a-Judge is one candidate approach; alternatives include deterministic checks (for tasks with verifiable outputs), rubric-based human annotation (reliable but costly), and hybrid methods.

The choice of evaluator is not neutral — it directly affects what NiceM measures as "successful." The evaluator's cross-language reliability must be characterized before NiceM's results can be trusted as language-fair. This is an open methodological question that must be resolved before any execution-tax validation experiment is run.
