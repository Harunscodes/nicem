# NiceM — AI Execution Intelligence

> Human language is the new code.
> Token-tax is the representation cost.
> Execution-tax is the workflow cost.
> Tokens-per-watt is the infrastructure efficiency question.
> NiceM measures and optimizes how AI systems execute human intent.

---

## What is NiceM?

NiceM is an independent research/startup project exploring how language, tokenization, agent design, retrieval, tool use, latency, cost, quality, and human correction affect the **total workload** required for AI systems to complete human intent.

The project starts from an observation in the academic literature — that different languages are treated unequally by AI tokenization systems — and extends it into a broader hypothesis: that all kinds of AI workflow overhead can be measured, diagnosed, and reduced.

---

## What is token-tax?

Token-tax is the extra representation burden caused by how a language, script, morphology, or tokenizer represents equivalent meaning. The same sentence in different languages can require very different numbers of tokens — and because most AI APIs charge per token, this creates a direct cost and quality inequality.

**This is established in the academic literature:**

- Petrov et al. (NeurIPS 2023) — tokenization parity across 200 languages; Shan requires up to 15× more tokens than English on the same tokenizer
- Ahia et al. (arXiv 2023) — API cost inequality by language; Telugu users pay ~4× more than English users for the same task
- Lundin et al. (arXiv 2025) — fertility (tokens/word) reliably predicts accuracy; higher fertility → lower accuracy; African languages trail English by ~25 accuracy points on average

Token-tax affects not just cost, but also latency, effective context window size, and model accuracy.

---

## What is execution-tax?

Execution-tax is the **extra total AI workflow burden** required to complete the same human intent successfully. It includes not only tokens, but also:

- retrieval calls and retrieval tokens
- tool calls and agent steps
- retries and context expansion
- latency, cost, quality score
- human correction

**This is a NiceM hypothesis.** It extends the token-tax concept from the tokenization layer into the full execution layer of agentic AI workflows. It is not yet proven by existing research — it is the core question NiceM is investigating.

The key research question:

> For the same human intent, do different languages, task types, models, prompts, retrieval strategies, tools, or agent designs create different total AI execution workloads?

---

## Why does this project exist?

The AI industry is moving from discrete model deployments to continuous **AI factories** — infrastructure designed to produce tokens at scale, continuously, efficiently (Jensen Huang, NVIDIA). The primary efficiency metric in this framing is **tokens per watt**.

NiceM's hypothesis is that the meaningful long-term metric is not just tokens per watt, but **successful human intent per watt** — and that execution-tax is the gap between these two numbers.

If execution-tax exists and is measurable, it has consequences for:
- AI infrastructure economics
- Language and accessibility equity
- Agentic AI system design
- Cost attribution and optimization

---

## What is the current stage?

This repository is in the **research and startup-foundation phase.**

The current work is:
- Structuring the thesis
- Mapping the academic literature
- Defining open questions
- Planning validation methodology

**Status:** the v0.1 methodology layer is complete — the documents in `docs/methodology/` cover success definition, task family, retrieval design, language selection (English/Dutch/Turkish), benchmark sizing, logging schema, agent designs, pre-registered falsification rules, token-tax baseline calculation, tokenizer/model decision rules, and evaluation method. The consolidated roadmap is `docs/methodology/validation-plan-v0.1.md`.

No product code has been built yet. No experiments have been run yet. No dataset has been generated yet.

---

## What should not be done yet

- No product code
- No experiments
- No SaaS architecture
- No customer-facing features

The next steps are: validation plan, proof-of-concept benchmark design, and startup positioning — in that order.

---

## Repository structure

```
CLAUDE.md                        — Global working instructions for Claude Code
README.md                        — This file

docs/
  nicem-thesis.md                — Core thesis and argument structure
  token-tax-vs-execution-tax.md  — Canonical definitions and distinction
  research-foundation.md         — Literature base, what is/isn't proven
  source-map.md                  — Which sources support which claims
  industry-context.md            — Jensen Huang / NVIDIA framing (industry context only)
  open-questions.md              — Tracked open and resolved questions

  sources/
    papers/
      petrov-tokenization-parity.md
      ahia-tokenization-fairness-api-pricing.md
      lundin-token-tax.md
      pdf/                       — Original PDF source files
    industry/                    — Industry source notes (in progress)
    notes/                       — Working notes and terminology (in progress)
```

---

## Independence note

NiceM is an independent personal research/startup project. It does not use employer data, customer data, or confidential information. All examples in this project use neutral synthetic scenarios.
