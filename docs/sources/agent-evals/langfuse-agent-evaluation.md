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

## Notes for NiceM positioning

TODO: Add once source is read and verified.
