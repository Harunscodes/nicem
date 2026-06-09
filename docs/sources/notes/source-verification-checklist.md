# NiceM — Source Verification Checklist

This checklist tracks claims from `docs/sources/notes/nvidia-jensen-chat-context.md` that require original source verification before they can appear in a pitch deck, public article, or cited thesis document.

**Rule:** A claim may not be cited publicly until:
1. The original source (talk, interview, keynote, product page, blog) is identified
2. A direct quote or specific paraphrase is confirmed against that source
3. The verified claim is documented in the appropriate industry source file (`jensen-huang-ai-factories-tokens-per-watt.md` or `nvidia-agents-infrastructure-notes.md`)
4. This checklist is updated to reflect completion

---

## Priority 1 — High: Claims likely to appear in pitch deck or thesis introduction

These are framing claims that would naturally appear early in any NiceM pitch or public document. They need verification first.

- [ ] **"Human language is the new programming language"**
  - Attributed to: Jensen Huang
  - Used in NiceM as: the opening framing for the core thesis
  - What to find: original talk or interview where Jensen uses this phrase or equivalent; exact wording; date and event
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Exact quotes section
  - Notes: Widely reported but exact source not yet traced. Do not use as a Jensen quote until confirmed.

- [ ] **"Electrons to tokens" or equivalent AI factory framing**
  - Attributed to: Jensen Huang / NVIDIA (general AI factory framing)
  - Used in NiceM as: energy → intelligence transformation; AI factory as a conceptual anchor
  - What to find: specific keynote, blog, or interview where Jensen or NVIDIA uses this phrase or the electrons-to-intelligence framing; exact wording
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Exact quotes section
  - Notes: The AI factory concept is documented in NVIDIA's token factory blog (S3) but the "electrons to tokens" phrase specifically needs tracing.

- [ ] **Tokens-per-watt as a product specification (not just a narrative)**
  - Attributed to: NVIDIA product pages and technical blogs (S2, S3, S4)
  - Used in NiceM as: evidence that tokens-per-watt is a real, used metric — not invented by NiceM
  - What to find: exact figures or language from Vera Rubin platform page and token factory blog; verbatim product comparison language
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Exact quotes section
  - Notes: Sources are identified (S2, S3, S4) but direct links and verbatim quotes are still TODO. This is lower risk than the Jensen quote claims — the sources are known, just not yet quoted verbatim.

---

## Priority 2 — Medium: Claims likely to appear in supporting sections or investor Q&A

These would appear in context sections, supporting slides, or in response to questions. Important to verify before pitching but not necessarily in the opening slides.

- [ ] **AI demand grows faster than hardware performance**
  - Attributed to: Jensen Huang
  - Used in NiceM as: strategic rationale for why workload efficiency matters even as hardware improves
  - What to find: specific quote or talk where Jensen makes the demand-outpacing-performance argument; date and event
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Exact quotes section
  - Notes: Jensen's January 2026 quote ("AI computing demand for both training and inference is going through the roof," S5) is related but does not directly make the demand-outpaces-performance argument. A separate source may be needed.

- [ ] **GTC 2026 keynote covers agentic systems and AI factories**
  - Attributed to: NVIDIA GTC 2026 official event page (S1)
  - Used in NiceM as: evidence that agentic AI is part of NVIDIA's strategic public framing
  - What to find: direct link to NVIDIA GTC 2026 event/keynote page; confirm the specific framing language
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Source links table
  - Notes: Source is identified but link is TODO.

- [ ] **Vera Rubin delivers more tokens per watt and lower cost per token than Blackwell**
  - Attributed to: NVIDIA Vera Rubin platform page (S2)
  - Used in NiceM as: concrete evidence that tokens-per-watt is a hardware-generation comparison metric
  - What to find: direct link to Vera Rubin platform page; exact product comparison language
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Source links table + Exact quotes section
  - Notes: Source identified, link TODO.

- [ ] **NeMo Agent Toolkit tracks per-step input/output tokens, timings, and bottlenecks**
  - Attributed to: NVIDIA NeMo Agent Toolkit documentation (S6)
  - Used in NiceM as: evidence that per-step execution observability exists at the industry level — NiceM does not need to build it from scratch
  - What to find: direct link to NeMo Agent Toolkit documentation; confirm profiling and token-tracking capabilities are documented as described
  - Where to document when verified: `nvidia-agents-infrastructure-notes.md` → Source links table + Exact quotes section
  - Notes: This is the most methodology-relevant source for NiceM's execution-tax measurement approach. Verification is important.

- [ ] **Jensen Huang January 2026 quote: "AI computing demand for both training and inference is going through the roof"**
  - Attributed to: NVIDIA Rubin newsroom, January 2026 (S5)
  - Used in NiceM as: evidence of demand growth framing in Jensen's own words
  - What to find: direct link to the January 2026 NVIDIA newsroom article; confirm exact wording of the quote in context
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Exact quotes section
  - Notes: Source is identified but full quote context and direct link are TODO. Currently marked "(Full quote context TODO — verify against original.)" in the source file.

---

## Priority 3 — Lower: Background framing; useful but not pitch-critical

These would appear in background sections, appendices, or deeper research notes. Verify before any public use, but not blocking for an early pitch.

- [ ] **NVIDIA frames open-source AI as important (Linux / Kubernetes / PyTorch analogy)**
  - Attributed to: Jensen Huang (general public statements)
  - Used in NiceM as: context for positioning NiceM as potentially an open benchmark/standard
  - What to find: specific talk or interview where Jensen makes the open-source-in-AI comparison
  - Where to document when verified: `nvidia-agents-infrastructure-notes.md` or a new note
  - Notes: Widely reported characterization — but "widely reported" is not a citation. Trace to a primary source.

- [ ] **NVIDIA Agentic AI Blueprints: agents that reason, plan, and take action**
  - Attributed to: NVIDIA Agentic AI Blueprints blog (S7)
  - Used in NiceM as: confirmation that multi-step, reasoning-and-planning agents are NVIDIA's production framing
  - What to find: direct link to the Agentic AI Blueprints blog post; confirm the "reason, plan, and take action" language
  - Where to document when verified: `nvidia-agents-infrastructure-notes.md` → Source links table

- [ ] **NVIDIA Build Blueprints: Multi-Agent Intelligent Warehouse example**
  - Attributed to: NVIDIA Build Blueprints page (S8)
  - Used in NiceM as: a concrete example of deployed multi-agent systems that would be subject to execution-tax
  - What to find: direct link to the NVIDIA Build Blueprints page; confirm the warehouse example and its description
  - Where to document when verified: `nvidia-agents-infrastructure-notes.md` → Source links table

- [ ] **Revenue per megawatt as an AI factory economics metric**
  - Attributed to: NVIDIA *Scaling Token Factory Revenue* technical blog (S3)
  - Used in NiceM as: support for framing token waste as an infrastructure-economics problem, not just a developer inconvenience
  - What to find: direct link to the technical blog; confirm the revenue-per-megawatt framing and any specific figures
  - Where to document when verified: `jensen-huang-ai-factories-tokens-per-watt.md` → Source links table + Exact quotes section

---

## Claims that do NOT require external verification

These appear in `nvidia-jensen-chat-context.md` but are NiceM concepts or technically grounded descriptions — not attributed statements.

| Claim | Reason no verification needed |
|---|---|
| Language → tokens → tensors → chips → energy transformation stack | Technical description of LLM inference, not an attributed quote |
| Successful intent per watt | NiceM concept — must be labeled as such, not attributed externally |
| Cost per successful completion | NiceM concept — same |
| Execution-tax definition and components | NiceM hypothesis — same |
| Agentic workflow step structure (understand → plan → retrieve → …) | Descriptive characterization consistent with public documentation; not an attributed quote |

---

## Verification log

*Move completed items here with source details.*

| Claim | Source confirmed | Date verified | Documented in |
|---|---|---|---|
| *(none yet)* | | | |
