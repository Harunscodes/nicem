# LangSmith — Agent Evaluation

## Type

Agent evaluation / methodology source — product documentation and evaluation platform (LangChain ecosystem).
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| LangSmith agent evaluation documentation | Product docs / blog | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

LangSmith is LangChain's evaluation and observability platform for LLM applications. It supports tracing of multi-step agent runs, dataset-based evaluation, and comparison across runs. The evaluation primitives it exposes — correctness scoring, step-level tracing, latency, token cost — are relevant to the NiceM question of whether equivalent human intent requires different total workloads depending on language, task type, or agent design.

---

## What this supports

TODO: Add once source is read and verified.

---

## What this does not prove

- That execution-tax exists or is measurable in the way NiceM hypothesizes
- That LangSmith's evaluation approach is the right methodology for NiceM
- Any NiceM-specific claim
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: LangSmith likely describes evaluation datasets, scoring approaches, and run comparison methodologies — relevant to how NiceM would design a controlled execution-tax measurement experiment.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: LangSmith's per-run token and cost tracing could serve as the instrumentation substrate for NiceM's execution-tax measurement methodology, particularly if it can attribute overhead to specific orchestration components (retrieval vs. tool call vs. retry).

---

## Connection to successful completion

LangSmith's dataset-based evaluation approach requires defining expected outputs or success criteria for each test case. This explicit success definition is directly relevant to NiceM — it forces the question of what correct completion looks like for each task, in each language, before any metric is computed.

TODO: Confirm whether LangSmith supports per-language evaluation datasets and whether success criteria can be defined independently per language.

---

## Connection to agent trajectory evaluation

LangSmith traces multi-step agent runs and allows evaluation of individual steps, not only final outputs. This supports trajectory evaluation: scoring whether the agent took the right path, not just whether it arrived at the right answer.

TODO: Confirm the granularity of step-level evaluation in LangSmith — specifically whether individual tool calls and retrieval steps can be scored independently.

---

## Risks or limitations for multilingual evaluation

- LangSmith's built-in evaluators are primarily designed for English. Custom evaluators would be needed for non-English languages.
- Dataset construction across languages requires translation and validation — translated test cases may introduce inequivalence if not carefully designed.
- Run comparison across language conditions requires that the underlying tasks are genuinely equivalent, which is a design constraint outside LangSmith's control.

---

## Notes for NiceM methodology

TODO: Add once source is read and verified.
