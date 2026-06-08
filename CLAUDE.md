# NiceM — Global Project Instructions for Claude Code

This file is the authoritative working instruction for all Claude Code sessions in this repository.
Read it before doing anything else.

---

## Project identity

**Project name:** NiceM
**Working category:** AI Execution Intelligence

**Core thesis:**
> Human language is the new code.
> Token-tax is the representation cost.
> Execution-tax is the workflow cost.
> Tokens-per-watt is the infrastructure efficiency question.
> NiceM measures and optimizes how AI systems execute human intent.

**Purpose:**
NiceM is an independent research/startup project exploring how language, tokenization, agent design, retrieval, tool use, latency, cost, quality, and human correction affect the total workload required for AI systems to complete human intent.

---

## Current stage

This repository is in the **research and startup-foundation phase**.

- Do not build product code unless explicitly asked.
- Do not create experiments unless explicitly asked.
- First help structure the thesis, sources, open questions, validation plan, and startup positioning.

---

## Definitions

### Token-tax

Extra representation burden caused by how a language, script, morphology, or tokenizer represents equivalent meaning. It can appear as:
- higher token counts
- higher API cost
- increased latency
- reduced effective context window
- sometimes lower model accuracy

Token-tax is **established in the academic literature** (Petrov et al. NeurIPS 2023, Ahia et al. arXiv 2023, Lundin et al. arXiv 2025).

### Execution-tax

Extra total AI workflow burden required to complete the same human intent successfully. This includes not only tokens, but also:
- retrieval calls and retrieval tokens
- tool calls and agent steps
- retries and context expansion
- latency, estimated cost, quality score
- human correction and success/failure

Execution-tax is a **NiceM hypothesis** that extends token-tax into operational AI workflows. It is not yet proven by existing literature and must be treated as a concept to validate, not an established fact.

### Cost per successful completion

The primary NiceM business metric. A cheap failed run is not efficient. NiceM focuses on how much cost, latency, and workload are required to complete the same intent **successfully**.

### Successful intent per watt

A long-term infrastructure metric. Tokens-per-watt is a useful framing (Jensen Huang, NVIDIA), but in agentic AI the more meaningful metric may become **successful human intent per watt**.

---

## Key research question

> For the same human intent, do different languages, task types, models, prompts, retrieval strategies, tools, or agent designs create different total AI execution workloads?

## Key startup question

> Can NiceM become a product that measures, explains, and eventually reduces execution-tax?

---

## Working product direction

NiceM should **not** be a generic LLM observability dashboard.

NiceM should become **AI Execution Intelligence**:

```
observe → diagnose → recommend → simulate → human-approve → measure impact
```

---

## Source interpretation rules

### Research foundation

- Academic paper notes: `docs/sources/papers/*.md` — interpreted working notes, primary reference
- Original PDFs: `docs/sources/papers/pdf/` — original source material
- If a Markdown note and a PDF appear to conflict, ask before deciding

### What academic papers support

- Token-tax and multilingual tokenization inequality
- Token count differences, cost implications, latency implications, context pressure, and sometimes accuracy differences
- These are all aspects of token-tax at the tokenization layer

### What academic papers do not prove

- Execution-tax in agentic AI workflows
- Any NiceM-specific hypothesis about multi-step workload overhead
- That token-tax and execution-tax compound (not yet studied)

### Industry sources (Jensen Huang / NVIDIA / AI factories)

Once added, these should be treated as **industry context** only — not scientific proof.
They establish that the environment for NiceM's hypothesis is real and growing; they do not validate the hypothesis itself.

---

## Important distinction

| Concept | Status | Source |
|---|---|---|
| Token-tax | Established in literature | Petrov, Ahia, Lundin |
| Execution-tax | NiceM hypothesis | No external source yet |
| Tokens-per-watt | Industry framing | Jensen Huang / NVIDIA |
| Cost per successful completion | NiceM metric | NiceM concept |
| Successful intent per watt | NiceM long-term metric | NiceM concept |

---

## Independence and safety rules

This is an **independent personal research/startup project**.

- Do not use employer data
- Do not use customer data
- Do not use ServiceDesk tickets or internal support workflows
- Do not use confidential information
- Do not use internal workflows or proprietary systems
- Do not assume this project is connected to any current job

Use only neutral synthetic examples, such as:
- fictional smart-home product FAQ
- multilingual product assistant
- travel assistant
- research assistant
- public document Q&A
- generic AI workflow scenarios

---

## Tone and reasoning rules

- Be precise. Avoid hype.
- Separate what is proven from what is hypothesized.
- Do not overclaim.
- When citing sources, state what they support and what they do not prove.
- Treat execution-tax as a concept to validate, not an already proven fact.
- Prefer research-backed reasoning and clear startup logic.

---

## Repository behavior rules

- Before creating code, check whether the repository has enough conceptual foundation.
- Prefer documenting thesis, assumptions, source maps, open questions, and validation plans before implementation.
- If asked to build, start with a minimal proof-of-concept or benchmark — not a full SaaS product.
- Keep changes small, readable, and committed with clear messages.
- Commit to branch `claude/vibrant-ride-lhv330` unless instructed otherwise.

---

## Repository structure (current)

```
docs/
  nicem-thesis.md              — Core thesis and argument structure
  token-tax-vs-execution-tax.md — Canonical definitions and distinction
  research-foundation.md       — Literature base and what is/isn't proven
  source-map.md                — Which sources support which claims
  industry-context.md          — Jensen Huang / NVIDIA framing (industry only)
  open-questions.md            — Tracked open questions and resolved questions

  sources/
    papers/
      petrov-tokenization-parity.md       — NeurIPS 2023 paper notes
      ahia-tokenization-fairness-api-pricing.md — arXiv 2023 paper notes
      lundin-token-tax.md                 — arXiv 2025 paper notes
      pdf/                                — Original PDF source files
    industry/                            — Industry source notes (TODO)
    notes/                               — Working notes and terminology (TODO)
```

---

*This file should be read at the start of every Claude Code session in this repository.*
