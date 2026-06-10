# NiceM — Source Map

This document maps every source in `docs/sources/` to the claims it supports, the concepts it connects to, and its role in the NiceM argument chain.

**Related internal documents (not sources, but where sources are applied):**
- `docs/startup/nicem-startup-thesis-v0.1.md` — first coherent startup thesis
- `docs/methodology/nicem-methodology-framework-v0.1.md` — measurement framework that turns methodology questions M1–M9 into a structured approach for measuring execution-tax; consumes the agent-evaluation sources below
- `docs/methodology/success-rubric-v0.1.md` — operationalizes M1 (define successful completion): binary success gate, seven minimum criteria, quality bands, multilingual equivalence requirements, nine failure types, evaluation method comparison, evaluator uncertainty protocol. Prerequisite before any benchmark run.
- `docs/methodology/task-family-selection-v0.1.md` — addresses framework §12 task-family prerequisite: compares six candidate families (Product FAQ, travel planning, public doc QA, structured form, scheduling, arithmetic/lookup) and recommends Product FAQ / policy QA as the primary v0.1 family; backup is calendar scheduling. Explains why open-ended tasks are excluded. Defines five task skeletons, expected trajectory components, relationship to success rubric, token-tax/execution-tax decomposition, and seven open questions (TF1–TF7) before dataset construction.
- `docs/methodology/retrieval-design-decision-v0.1.md` — resolves TF5 (retrieval design): analyzes language-matched retrieval (Option A), language-neutral/canonical retrieval (Option B), and a two-condition comparison (Option C). Decision: v0.1 uses language-matched retrieval with KB quality control as a hard prerequisite; Option B pre-registered as the v0.2 contrast condition testing whether execution-tax is architecture-dependent; structured-fact-store fallback if KB quality control is infeasible. Documents which trajectory metrics are sensitive to retrieval design and warns against double-counting token-tax in retrieval-token measurements.
- `docs/methodology/language-selection-v0.1.md` — resolves TF3 (language selection): recommends English, Dutch, Turkish for v0.1; English as high-resource analytic baseline (structured fact-set is canonical, not English); Dutch as near-baseline Latin-script comparison; Turkish as agglutinative Latin-script probe; v0.2 expansion candidates ranked (Arabic, Hindi, Swahili, Korean, Japanese, Finnish); quality-control requirements per language; Turkish bilingual-review prerequisite; reporting boundaries; six open questions LS1–LS6.
- `docs/methodology/benchmark-sizing-v0.1.md` — resolves TF1 and TF2 (exploratory sizing): recommends a Small KB (6–10 documents, 50–100 canonical facts) and a small validation set (30–50 unique intents × 3 languages); minimum viable benchmark proposal of 8 documents / ~75 facts / 36 intents / 108 language-condition task instances with 2–3 repetitions if budget allows. Compares Tiny/Small/Medium KB and pilot/small/large instance options; defines intent design principles; explains why M8 (statistical power) cannot be resolved before pilot variance estimates exist; states reporting boundaries (patterns, not proof). Seven open questions BS1–BS7.

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

## Agent Evaluation Methodology Sources

These sources are methodology context for how to measure execution-tax. They do not prove that execution-tax exists. They inform the design of NiceM's validation experiment, success criteria, instrumentation choices, and trajectory evaluation approach.

### Biscuit — Agent Evaluation
- **File:** `docs/sources/agent-evals/biscuit-agent-evaluation.md`
- **Role:** Scenario/capability evaluation framework. Provides the experimental design structure NiceM needs: scenarios (fixed human intent), capabilities (agent behaviors tested), automated checks (success criterion), trend tracking, uncertainty handling.
- **Key NiceM application:** Scenario = fixed human intent; capability = agent behavior; automated check = success criterion before cost attribution.

### τ-bench (Tau-Bench) — Agent Benchmark
- **File:** `docs/sources/agent-evals/tau-bench.md`
- **Role:** Multi-step, multi-turn, tool-using agent benchmark with defined task success criteria. Most rigorous existing benchmark for the architecture NiceM needs to measure. Candidate template for execution-tax experiment design.
- **Key NiceM application:** Multi-step success definition; trajectory evaluation model; per-turn token cost (confirm availability).

### Agent-as-a-Judge
- **File:** `docs/sources/agent-evals/agent-as-a-judge.md`
- **Role:** Scalable automated success scoring methodology. Relevant to NiceM's success criterion at scale — but requires cross-language reliability validation before use in multilingual execution-tax measurement.
- **Key risk:** LLM judges may be biased toward high-resource languages, introducing confounds into NiceM's success classifications.

### LangSmith — Agent Evaluation
- **File:** `docs/sources/agent-evals/langsmith-agent-evaluation.md`
- **Role:** Dataset-based evaluation and run comparison for LangChain-based agents. Relevant to NiceM's controlled experiment design and regression tracking across model versions.

### Langfuse — Agent Evaluation
- **File:** `docs/sources/agent-evals/langfuse-agent-evaluation.md`
- **Role:** Open-source, span-level observability platform. Strong candidate for NiceM's instrumentation layer — captures per-step token counts, latency, and cost across full agent traces.

### Braintrust — Evals
- **File:** `docs/sources/agent-evals/braintrust-evals.md`
- **Role:** Scorer-first evaluation and experiment tracking. Relevant to NiceM's longitudinal question: does execution-tax change as models and frameworks improve over time?

### Arize Phoenix — Agent Observability
- **File:** `docs/sources/agent-evals/arize-phoenix-agent-observability.md`
- **Role:** Open-source, OpenTelemetry-compatible observability platform. Strong candidate for NiceM's instrumentation layer. Span-level attribution enables execution overhead decomposition by step type.

### NVIDIA — Agent Evaluation
- **File:** `docs/sources/agent-evals/nvidia-agent-evaluation.md`
- **Role:** NVIDIA-specific evaluation tooling and methodology for agentic workloads. Most relevant if NiceM's proof-of-concept uses NVIDIA infrastructure or NeMo Agent Toolkit.
- **Status:** Sources not yet verified — links and specific claims TODO.

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
