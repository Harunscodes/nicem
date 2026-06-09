# Langfuse — Agent Evaluation

## Type

Agent evaluation / methodology source — product documentation and observability platform.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| Langfuse agent evaluation documentation | Product docs / blog | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

Langfuse is an open-source LLM observability and evaluation platform. It captures traces across multi-step agent runs — including token counts per step, latency per step, and cost per step. This instrumentation approach is directly relevant to how NiceM might measure execution-tax: by tracing the full token and cost overhead of an agentic workflow, not just the final output.

---

## What this supports

TODO: Add once source is read and verified.

---

## What this does not prove

- That execution-tax exists or compounds with token-tax
- That Langfuse's instrumentation approach is the right methodology for NiceM
- Any NiceM-specific claim
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: Langfuse likely addresses per-step tracing, token attribution, and cost breakdown across agent runs — the instrumentation layer that makes execution-tax visible.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: If Langfuse can attribute tokens and cost to individual agent steps (retrieval, tool call, orchestration, retry), it provides a measurement framework that could be adapted for execution-tax attribution in NiceM.

---

## Connection to successful completion

Langfuse captures traces of full agent runs including final outputs, intermediate steps, and scores. If a success scorer is attached to a trace, Langfuse can record whether a run succeeded — making it a candidate instrumentation substrate for NiceM's cost-per-successful-completion metric, where cost and success are captured in the same trace.

TODO: Confirm whether Langfuse supports attaching custom success scorers to traces, and whether scores can be disaggregated by language or task condition.

---

## Connection to agent trajectory evaluation

Langfuse's trace structure captures the full agent trajectory as a sequence of spans — each span corresponding to a model call, tool call, or retrieval step. This is the instrumentation layer for trajectory evaluation: each step in the execution path is recorded with its own token counts, latency, and cost.

For NiceM, this means execution overhead can potentially be attributed at the span level: how many tokens did the retrieval step consume? How many model calls occurred before a successful answer? How did this differ across language conditions?

---

## Risks or limitations for multilingual evaluation

- Langfuse is instrumentation — it records what happens but does not interpret whether a run succeeded or whether the path was optimal. A language-fair success scorer must be added externally.
- Token count attribution in Langfuse reflects raw token consumption. Interpreting whether higher token counts in one language represent execution-tax requires a controlled experimental design outside Langfuse's scope.

---

## Notes for NiceM methodology

Langfuse is a strong candidate for NiceM's instrumentation layer. Its open-source nature, span-level attribution, and cost tracking make it compatible with a controlled execution-tax measurement experiment. The primary gap is the success criterion — Langfuse records cost, but whether a run was "successful" must be determined by a separate evaluator that must be validated for cross-language reliability.
