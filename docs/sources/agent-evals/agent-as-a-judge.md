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

## Notes for NiceM positioning

TODO: Add once source is read and verified.

Anticipated positioning note: NiceM needs a scalable success criterion for its execution-tax benchmark. Agent-as-a-Judge is one approach; the choice between automated judging, rubric-based scoring, and human evaluation is an open methodological question for NiceM's validation plan.
