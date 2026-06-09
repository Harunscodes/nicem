# Arize Phoenix — Agent Observability

## Type

Agent evaluation / methodology source — open-source observability platform for LLM and agent applications.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| Arize Phoenix documentation / agent observability | Product docs | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

Arize Phoenix is an open-source observability platform for LLM applications and agents. It captures traces, spans, and token-level data across agent runs. Its OpenTelemetry-based instrumentation approach is particularly relevant to NiceM because it provides a vendor-neutral method for capturing per-step overhead — which is the instrumentation layer NiceM would need to measure execution-tax in a controlled way.

---

## What this supports

TODO: Add once source is read and verified.

---

## What this does not prove

- That execution-tax exists or compounds with token-tax
- That Phoenix's observability approach is the right methodology for NiceM
- Any NiceM-specific claim
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: Phoenix likely describes trace-based observability, span attribution, and token/cost breakdown per agent step — the instrumentation primitives that would make execution-tax visible across different languages, task types, and architectures.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: Phoenix's span-level token attribution could be the instrumentation substrate for NiceM's execution-tax measurement. If retrieval calls, tool calls, and orchestration steps each produce their own spans with token counts, the total overhead per step type becomes calculable.

---

## Notes for NiceM positioning

TODO: Add once source is read and verified.
