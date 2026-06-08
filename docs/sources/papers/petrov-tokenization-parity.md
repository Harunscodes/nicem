# Petrov et al. — Tokenization Parity

## Type

Academic paper — NeurIPS 2023
Full title: *Language Model Tokenizers Introduce Unfairness Between Languages*
Authors: Aleksandar Petrov, Emanuele La Malfa, Philip H.S. Torr, Adel Bibi (University of Oxford)

## Source files

- **Original PDF:** `docs/sources/papers/pdf/petrov-tokenization-parity.pdf`
- **This file:** Interpreted source notes for the NiceM project — the primary working reference
- **Conflict rule:** If this summary and the PDF appear to conflict, flag it before deciding

## Main claim

The same text translated into different languages produces drastically different tokenization lengths — up to 15× longer for some languages (e.g., Shan) compared to English, using the same tokenizer. This disparity arises at the tokenization stage, before the model is even invoked, and persists even in tokenizers explicitly designed for multilingual support.

Three fairness consequences follow:
1. **Cost** — users of some languages pay at least 2.5× more for the same task
2. **Latency** — processing time is linear in token length; some languages take twice as long
3. **Long context** — users of high-premium languages can process an order of magnitude less content in a fixed context window

## Key quantitative findings

| Language | GPT-2/RoBERTa premium | ChatGPT/GPT-4 premium |
|---|---|---|
| English | 1.00 | 1.00 |
| French | 2.00 | 1.60 |
| German | 2.14 | 1.37 |
| Arabic | 4.40 | 3.04 |
| Japanese | 3.00 | 2.30 |
| Bulgarian | 5.51 | 2.64 |
| Burmese | 16.89 | 11.70 |
| Shan | 18.76 | 15.05 |

Even the most efficient non-English language (Portuguese, Pangasinan) still pays a ~50% premium on ChatGPT/GPT-4.

Byte-level models (ByT5, CANINE) also fail to achieve parity — ByT5 ranges from 0.87× (Yue Chinese) to 3.94× (Shan). Character/byte-level tokenization is not a solution.

Multilingual models (XLM-R, NLLB, mT5, M2M100, BLOOM) improve parity but none achieve it uniformly across all languages.

Dataset: FLORES-200 parallel corpus (2000 sentences, 200 languages, human-translated from Wikipedia).

## Relevance to NiceM

This is the primary empirical foundation for the token-tax concept as it applies to API pricing. It establishes with quantitative precision that:
- Tokenization disparity is not anecdotal — it is systematic and measurable across 200 languages
- The disparity translates directly into cost inequality because APIs charge per token
- The problem is structural, not correctable by simple vocabulary fixes
- Even multilingual tokenizers do not solve it

## What this supports

- Token-tax exists and is measurable (core NiceM claim)
- Token-tax arises at the tokenization layer, before inference
- Token-tax varies by script and language, with non-Latin scripts most affected
- Token-tax creates latency inequality in addition to cost inequality
- Token-tax reduces effective context window for high-premium language users
- A multilingually fair subword tokenizer is technically feasible (the paper proposes a two-stage merging approach)

## What this does not prove

- That execution-tax exists (this paper does not address agentic or multi-step workloads)
- That token-tax and execution-tax compound (out of scope)
- That the disparity is intentional
- That any single fix (separate pricing tokenizer, byte-level encoding) fully resolves the problem — the paper shows these are insufficient

## Connection to token-tax, execution-tax, or tokens-per-watt

**Token-tax:** This is the foundational empirical paper for token-tax as a cost concept. The premium ratio (|t(sA)| / |t(sB)|) is the direct measurement of token-tax for language A relative to language B.

**Execution-tax:** Not addressed. The paper focuses on static text tokenization, not on multi-step agentic workloads.

**Tokens-per-watt:** The paper notes that processing time is linear in tokenization length (Figure 2, RoBERTa experiments). This means token-tax directly degrades tokens-per-watt efficiency for affected languages — more compute per unit of semantic meaning.
