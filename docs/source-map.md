# NiceM — Source Map

This document maps every source in `docs/sources/` to the claims it supports, the concepts it connects to, and its role in the NiceM argument chain.

---

## Academic Papers

### Petrov et al. — Tokenization Parity
- **File:** `docs/sources/papers/petrov-tokenization-parity.md`
- **Supports:** Token-tax hypothesis — that tokenization systems systematically produce more tokens for certain languages, scripts, or writing systems than for others, for equivalent semantic content.
- **Key concept:** Tokenization parity / tokenization disparity
- **Role in argument:** Establishes that the number of tokens consumed per unit of meaning is not neutral — it varies by language and script. This is the empirical foundation for token-tax.
- **Status:** TODO — fill in specific findings, dataset, and quantitative claims from the paper.

### Ahia et al. — Tokenization, Fairness, and API Pricing
- **File:** `docs/sources/papers/ahia-tokenization-fairness-api-pricing.md`
- **Supports:** Token-tax hypothesis — that tokenization disparity translates directly into pricing disparity at the API level.
- **Key concept:** Token-tax, API cost inequality
- **Role in argument:** Connects the technical tokenization problem to an economic consequence: users working in underrepresented languages pay more per unit of meaning. This is the clearest existing framing of token-tax as a cost concept.
- **Status:** TODO — fill in specific findings, languages studied, and cost differential data.

### Lundin — The Token Tax
- **File:** `docs/sources/papers/lundin-token-tax.md`
- **Supports:** Token-tax as a named, defined concept.
- **Key concept:** Token-tax (named)
- **Role in argument:** Provides or consolidates the term "token-tax" as an analytical category. Central reference for NiceM's use of the term.
- **Status:** TODO — fill in definition, scope, and any proposed remedies.

---

## Industry Sources

### Jensen Huang — AI Factories and Tokens per Watt
- **File:** `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md`
- **Supports:** Infrastructure framing — that AI compute is shifting toward factory-scale continuous token production, measured in throughput per watt.
- **Key concept:** Tokens-per-watt, AI factories, inference at scale
- **Role in argument:** Establishes the industry direction: AI infrastructure is being optimized around token throughput efficiency. This is the context in which execution-tax becomes a meaningful concept.
- **Status:** TODO — identify specific talk or interview, extract direct quotes or paraphrased claims.

### NVIDIA — Agents and Infrastructure Notes
- **File:** `docs/sources/industry/nvidia-agents-infrastructure-notes.md`
- **Supports:** Agentic workload framing — that AI workloads are becoming multi-step, multi-model, and infrastructure-intensive.
- **Key concept:** Agentic execution, inference infrastructure, orchestration overhead
- **Role in argument:** Shows that token production is no longer a single isolated API call but a chained, orchestrated process. This is where execution-tax (NiceM hypothesis) becomes visible — overhead accumulates across steps.
- **Status:** TODO — identify specific document (whitepaper, blog, product page), extract relevant claims.

---

## Internal Notes

### NiceM Chat Summary
- **File:** `docs/sources/notes/nicem-chat-summary.md`
- **Role:** Running log of key decisions, framings, and directions that emerged through project development sessions.
- **Status:** TODO — populate with session summaries as the project evolves.

### Terminology
- **File:** `docs/sources/notes/terminology.md`
- **Role:** Canonical definitions for all load-bearing terms used in NiceM. Prevents conceptual drift between thesis, code, and communication.
- **Status:** TODO — see `docs/token-tax-vs-execution-tax.md` for initial definitions.

---

## Concept-to-Source Index

| Concept | Source(s) |
|---|---|
| Token-tax (named) | Lundin; Ahia et al. |
| Tokenization disparity | Petrov et al.; Ahia et al. |
| API cost inequality | Ahia et al. |
| Tokens-per-watt | Jensen Huang |
| AI factories / inference at scale | Jensen Huang |
| Agentic workloads / orchestration | NVIDIA |
| Execution-tax | **NiceM hypothesis** — no external source yet |
