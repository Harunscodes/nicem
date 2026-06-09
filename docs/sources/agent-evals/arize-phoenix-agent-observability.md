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

## Connection to successful completion

Phoenix records traces but does not inherently define success. For NiceM's cost-per-successful-completion metric, a success label must be attached to each trace — either from a human annotator, an automated judge, or a deterministic check. Phoenix's open-source and OpenTelemetry-compatible design means custom success labeling can be integrated without vendor lock-in.

TODO: Confirm whether Phoenix supports custom span-level annotations for success/failure classification.

---

## Connection to agent trajectory evaluation

Phoenix's span-level tracing is well-suited to trajectory evaluation. Each tool call, retrieval step, and model call is a separate span with its own attributes. This means the full agent trajectory is recorded as a structured sequence, and individual steps can be evaluated or filtered independently.

For NiceM, this enables execution overhead decomposition: how many tokens were consumed at each step type (retrieval, tool call, model call, orchestration), and how does this breakdown differ across language conditions?

---

## Risks or limitations for multilingual evaluation

- Phoenix captures raw observability data. Interpreting whether a trajectory represents efficient or inefficient execution requires external analysis — Phoenix itself does not diagnose execution-tax.
- Span attribute naming and structure may vary across agent frameworks, making cross-framework comparison in Phoenix more complex.
- Token cost attribution in Phoenix is based on reported token counts, which may not always be available for all model providers or tool call types.

---

## Notes for NiceM methodology

Phoenix is a strong candidate for NiceM's observability layer, particularly for a proof-of-concept experiment. Its open-source design, OpenTelemetry compatibility, and span-level attribution make it well-suited to a controlled execution-tax measurement setup. The key advantage over proprietary platforms is that the full trace data is accessible for custom analysis — NiceM is not limited to the visualizations Phoenix exposes by default.
