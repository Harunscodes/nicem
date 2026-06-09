# NiceM — Source Map

This document maps every source in `docs/sources/` to the claims it supports, the concepts it connects to, and its role in the NiceM argument chain.

---

## Academic Papers

### Petrov et al. — Tokenization Parity
- **File:** `docs/sources/papers/petrov-tokenization-parity.md`
- **Supports:** Token-tax hypothesis — that tokenization systems systematically produce more tokens for certain languages, scripts, or writing systems than for others, for equivalent semantic content.
- **Key concept:** Tokenization parity / tokenization disparity
- **Role in argument:** Establishes that the number of tokens consumed per unit of meaning is not neutral — it varies by language and script. This is the empirical foundation for token-tax.
- **Status:** Populated — see paper notes file for full quantitative findings, dataset, and premium table across 200 languages.

### Ahia et al. — Tokenization, Fairness, and API Pricing
- **File:** `docs/sources/papers/ahia-tokenization-fairness-api-pricing.md`
- **Supports:** Token-tax hypothesis — that tokenization disparity translates directly into pricing disparity at the API level.
- **Key concept:** Token-tax, API cost inequality
- **Role in argument:** Connects the technical tokenization problem to an economic consequence: users working in underrepresented languages pay more per unit of meaning. This is the clearest existing framing of token-tax as a cost concept.
- **Status:** Populated — see paper notes file for full quantitative findings, 22 languages, cost-relative-to-English figures, and HDI correlation data.

### Lundin — The Token Tax
- **File:** `docs/sources/papers/lundin-token-tax.md`
- **Supports:** Token-tax as a named, defined concept.
- **Key concept:** Token-tax (named)
- **Role in argument:** Provides or consolidates the term "token-tax" as an analytical category. Central reference for NiceM's use of the term.
- **Status:** Populated — see paper notes file for fertility metric definition, regression slopes, accuracy gap findings, economic cost tables, and reasoning model comparison.

---

## Industry Sources

### Jensen Huang / NVIDIA — AI Factories and Tokens per Watt
- **File:** `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md`
- **Supports:** Infrastructure framing — tokens-per-watt and cost-per-token are real, actively used product metrics; AI infrastructure is being designed and measured around token throughput efficiency; agentic AI and long-context inference are the recognized production workload frontier.
- **Key concepts:** Tokens-per-watt, cost per token, AI factories, revenue per megawatt, agentic inference at scale
- **Key sources:** GTC 2026 keynote (S1); Vera Rubin platform page (S2); *Scaling Token Factory Revenue* technical blog (S3); Vera Rubin newsroom (S4); Rubin newsroom January 2026 with Jensen Huang quote (S5)
- **Role in argument:** Establishes that NiceM's core efficiency concepts (tokens-per-watt, cost per token) are already in use by the industry. Token-tax and execution-tax both degrade these metrics — NiceM works within the industry's own vocabulary, not alongside it. The KV-cache and long-context overhead acknowledgment (S4) is adjacent to execution-tax components.
- **Status:** Source claims documented. Direct links and verbatim quotes TODO — verify before citing.

### NVIDIA — Agents and Infrastructure Notes
- **File:** `docs/sources/industry/nvidia-agents-infrastructure-notes.md`
- **Supports:** Agentic workload framing — multi-step, tool-using, retrieval-augmented AI workflows are a real production architecture; per-step token and timing observability already exists in NVIDIA tooling; workflow-level bottleneck identification is an acknowledged engineering concern.
- **Key concepts:** Agentic execution, multi-step reasoning, NeMo Agent Toolkit, workflow profiling, per-step token tracking, bottleneck identification
- **Key sources:** NeMo Agent Toolkit documentation (S6); Agentic AI Blueprints blog (S7); Build Blueprints page (S8)
- **Role in argument:** NeMo Agent Toolkit (S6) is the most methodology-relevant source — it establishes that per-step token and timing tracking already exists at the industry level. The agentic blueprints (S7, S8) confirm that multi-step, multi-agent systems are production-grade, not research scenarios. Together these establish that the architecture and instrumentation for execution-tax measurement exist — what NiceM adds is the controlled language/design comparison.
- **Status:** Source claims documented. Direct links and verbatim quotes TODO — verify before citing.

---

## Internal Notes

### NVIDIA / Jensen — Chat-Derived Strategic Context
- **File:** `docs/sources/notes/nvidia-jensen-chat-context.md`
- **Role:** Captures Jensen Huang / NVIDIA / AI infrastructure ideas developed through a ChatGPT conversation. Shapes NiceM's thesis framing and strategic synthesis.
- **Key concepts documented:** Human language as the new code; language → tokens → tensors → chips → energy; AI factories / electrons to tokens; tokens-per-watt vs. successful intent per watt; demand growing faster than performance; agentic workload irregularity; full infrastructure stack for agents; open-source ecosystem context; NiceM strategic synthesis
- **⚠ Verification status:** **Conversation-derived — not citation-ready.** All claims must be traced to original NVIDIA / keynote / interview sources before use in thesis documents or pitch materials. Verified claims should be migrated to `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md` or `docs/sources/industry/nvidia-agents-infrastructure-notes.md`.

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
| Human language as the new code | Jensen Huang (TODO: verify source) — via `nvidia-jensen-chat-context.md` |
| Successful intent per watt | NiceM concept — derived from tokens-per-watt framing |
| AI factory / electrons to tokens | Jensen Huang / NVIDIA (TODO: verify exact source) — via `nvidia-jensen-chat-context.md` |
