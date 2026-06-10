# NiceM — Research Foundation

This document summarizes the academic basis for NiceM's core claims. It distinguishes what is established in the literature from what NiceM proposes as new hypothesis.

---

## Established: Tokenization is not language-neutral

Multiple studies have shown that standard subword tokenization systems (BPE, WordPiece, SentencePiece) produce significantly more tokens for equivalent content in lower-resource languages compared to high-resource languages — primarily English.

The technical cause: vocabulary construction favors languages with large training corpora. Characters and subwords from underrepresented scripts are split into more pieces, producing longer token sequences for the same meaning.

**Sources:**
- Petrov et al. — quantifies tokenization disparity across languages (`docs/sources/papers/petrov-tokenization-parity.md`) — TODO: add specific figures
- Ahia et al. — connects disparity to API pricing inequality (`docs/sources/papers/ahia-tokenization-fairness-api-pricing.md`) — TODO: add specific figures

---

## Established: Tokenization disparity creates pricing disparity

Because LLM APIs price per token, tokenization inequality becomes cost inequality. A user writing in a script that tokenizes inefficiently pays more per unit of meaning than a user writing the semantically equivalent content in English.

This is the token-tax: a structural cost premium on certain languages, scripts, and input types that is invisible in the pricing model but real in the invoice.

**Sources:**
- Ahia et al. — primary source for token-tax as an API pricing problem
- Lundin — names and frames token-tax as an analytical concept (`docs/sources/papers/lundin-token-tax.md`) — TODO: confirm scope and definitions

---

## Established: The industry is moving toward agentic, multi-step workloads

NVIDIA's infrastructure work and Jensen Huang's public statements describe a shift from single-call LLM inference toward orchestrated, multi-model, agentic pipelines running continuously at scale.

In this model, AI compute is not measured in individual API calls but in sustained token throughput — tokens per second, tokens per watt, tokens per dollar.

**Sources:**
- Jensen Huang / NVIDIA — tokens-per-watt framing (`docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md`) — TODO: add specific source
- NVIDIA agents and infrastructure (`docs/sources/industry/nvidia-agents-infrastructure-notes.md`) — TODO: add specific document

---

## Hypothesis: Agentic workloads generate structural overhead (execution-tax)

This is NiceM's proposed contribution. The claim is that multi-step agentic workflows generate tokens that do not carry semantic payload — orchestration overhead, repeated context, scaffolding, formatting — and that this overhead is measurable, varies by architecture, and is reducible.

This is not yet supported by external research. It is a testable hypothesis.

**Status:** NiceM hypothesis. See `docs/open-questions.md` for what needs to be proven.

---

## What the research does not yet show

| Claim | Status |
|---|---|
| Token-tax exists and is measurable | Supported (Petrov, Ahia, Lundin) |
| Token-tax creates API cost inequality | Supported (Ahia) |
| Agentic workloads dominate AI infrastructure direction | Supported (NVIDIA, Jensen Huang) |
| Agentic workloads generate measurable execution overhead | **Hypothesis — not yet proven** |
| Execution-tax is architecturally reducible | **Hypothesis — not yet proven** |
| Token-tax and execution-tax compound in real workloads | **Hypothesis — not yet proven** |

---

## How the foundation is applied

The token-tax literature above is operationalized in `docs/methodology/baseline-token-tax-calculation-v0.1.md`: NiceM adapts Petrov's tokenization parity ratio to per-intent measurements, Ahia's pricing/context-pressure framing to its cost reporting, and Lundin's fertility metric as a supporting measure. The purpose is twofold: align NiceM's numbers with the literature, and ensure that token-count effects — which the literature predicts — are never mislabeled as execution-tax, which the literature does not address. Execution-tax remains a NiceM hypothesis to validate.

---

## Gaps to fill

- TODO: Extract specific quantitative claims from Petrov et al.
- TODO: Extract cost differential figures from Ahia et al.
- TODO: Confirm Lundin's definition of token-tax and whether it overlaps with NiceM's use
- TODO: Identify the specific Jensen Huang source (talk, interview, earnings call)
- TODO: Identify the specific NVIDIA document on agentic infrastructure
