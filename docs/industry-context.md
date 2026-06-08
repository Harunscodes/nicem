# NiceM — Industry Context

This document summarizes the industry trends that make NiceM's research relevant beyond academia. The sources here are industry-facing, not peer-reviewed, and are used for framing and context rather than as proof of NiceM's core claims.

---

## The shift to AI factories

Jensen Huang has described the direction of AI infrastructure as a shift from discrete model deployments to continuous "AI factories" — infrastructure designed to produce tokens at scale, continuously, efficiently.

In this framing:
- The primary output of AI infrastructure is **tokens**
- The primary efficiency metric is **tokens per watt** (and tokens per dollar)
- AI compute becomes a utility, not a discrete service call

**Relevance to NiceM:** If the industry measures AI infrastructure efficiency in tokens-per-watt, then any structural source of token waste — token-tax overhead, execution-tax overhead — is directly relevant to infrastructure economics, not just to end-user pricing fairness.

**Source:** `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md` — TODO: add specific talk/interview reference and direct quotes.

---

## The rise of agentic workloads

NVIDIA's infrastructure work documents the shift toward multi-step, multi-model, orchestrated AI workloads. Rather than a single model responding to a single prompt, production AI systems increasingly involve:
- Multiple models in sequence or in parallel
- Tool use and external API calls
- Memory retrieval and context management
- Multi-turn reasoning and planning loops

**Relevance to NiceM:** This is the architecture in which execution-tax (NiceM hypothesis) becomes visible. Each additional step in an agentic pipeline is a potential source of orchestration overhead. At scale, this overhead accumulates into a measurable cost.

**Source:** `docs/sources/industry/nvidia-agents-infrastructure-notes.md` — TODO: add specific document reference.

---

## Tokens-per-watt as an efficiency metric

The tokens-per-watt metric, surfaced by Jensen Huang, is significant for NiceM because it reframes AI efficiency in terms of token throughput rather than model quality alone. This creates a natural measurement space for NiceM's concepts:

- Token-tax increases the token cost of a semantic unit → reduces effective tokens-per-watt for underrepresented languages
- Execution-tax increases the token cost of a task unit → reduces effective tokens-per-watt for agentic workloads

Both taxes can therefore be expressed in the industry's own efficiency vocabulary.

---

## What the industry context does not prove

- Industry sources are used for **framing**, not as evidence for NiceM's core claims
- Jensen Huang's statements about AI factories do not prove that execution-tax exists or is measurable
- NVIDIA's agentic infrastructure work does not validate the execution-tax hypothesis
- These sources establish that the *context* for NiceM's hypothesis is real and growing — they do not validate the hypothesis itself

---

## Summary

| Industry trend | NiceM relevance |
|---|---|
| AI factories / token throughput at scale | Token waste has infrastructure-level economics |
| Tokens-per-watt as efficiency metric | NiceM's taxes can be expressed in industry terms |
| Agentic, multi-step workloads becoming standard | Execution-tax hypothesis has a real and growing target |
