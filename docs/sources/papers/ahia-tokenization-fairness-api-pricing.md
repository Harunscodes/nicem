# Ahia et al. — Tokenization, Fairness, and API Pricing

## Type

Academic paper — arXiv preprint, May 2023
Full title: *Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models*
Authors: Orevaoghene Ahia, Sachin Kumar, Hila Gonen, Jungo Kasai, David R. Mortensen, Noah A. Smith, Yulia Tsvetkov
Institutions: University of Washington, Carnegie Mellon University, Allen Institute for Artificial Intelligence

## Source files

- **Original PDF:** `docs/sources/papers/pdf/ahia-tokenization-fairness-api-pricing.pdf`
- **This file:** Interpreted source notes for the NiceM project — the primary working reference
- **Conflict rule:** If this summary and the PDF appear to conflict, flag it before deciding

## Main claim

API vendors charge per token. Because tokenization rates are non-uniform across languages, speakers of languages with high fragmentation rates are systematically overcharged — while also receiving worse service. The paper identifies this as a "doubled unfairness": users who are overcharged also get lower model utility, and they tend to come from regions where the API is less affordable to begin with.

Four research questions are answered:
- **RQ1 (tokens):** Latin-script languages require far fewer tokens than non-Latin scripts; some languages (Telugu, Georgian) require up to 5× more tokens for the same information
- **RQ2 (cost):** API cost disparities directly mirror tokenization disparities; Telugu users pay ~5× more than English users for equivalent usage
- **RQ3 (utility):** High fragmentation languages are limited to zero-shot prompting because they cannot fit even one in-context example within the context window — degrading model performance
- **RQ4 (socio-economics):** Strong negative correlation between fragmentation rate and Human Development Index — the higher the fragmentation, the lower the HDI of the country where the language is spoken

## Key quantitative findings

**Fragmentation by script (ChatGPT tokenizer, FLORES-200):**
- Latin script: lowest average tokens per sentence (~50)
- Cyrillic, Japanese: close to Latin
- Telugu, Georgian: up to 5× more tokens than Latin-script languages
- Burmese: highest fragmentation in the study

**API cost relative to English (XLSUM task, zero-shot):**
- Telugu: ~4× the cost of English
- Amharic: ~4× the cost of English

**Context window impact:**
- Telugu and Amharic: cannot fit even one in-context example for the majority of test examples
- English: can fit 10+ in-context examples

**Socio-economic correlation (Figure 10, Table 1):**
- Negative correlation between HDI and fragmentation rate across all three tasks
- XFACT: Cost-HDI Spearman = −0.41, HDI-Utility Spearman = 0.34
- Pattern: lower HDI → higher fragmentation → higher cost → lower utility

**Models studied:** ChatGPT (gpt-3.5-turbo) and BLOOMZ (175B)
**Tasks:** XNLI, XFACT, XQUAD, CrossSum, XLSUM
**Languages:** 22 typologically diverse languages

## Relevance to NiceM

This is the paper that most directly frames token-tax as an API pricing problem with socio-economic consequences. It moves the argument from "tokenization is technically unequal" (Petrov) to "this inequality has measurable economic and social impact on real users."

Key contributions to NiceM:
- Quantifies the actual dollar-cost differential for API users by language
- Shows that cost inequality and performance inequality stack on the same population
- Demonstrates that the problem is not just pricing but also utility degradation (context window exhaustion)
- Identifies that token-tax disproportionately affects lower-HDI populations

## What this supports

- Token-tax translates directly into API cost inequality (core NiceM claim)
- Token-tax reduces model utility for affected language users, not just cost
- The populations most affected are those with least ability to absorb the excess cost
- The disparity is rooted partly in data imbalance and partly in inherent script properties (two independent causes)
- Byte-level BPE (BBPE) — the standard used in most modern LLMs including ChatGPT — does not solve the problem (Figure 18, appendix)

## What this does not prove

- That execution-tax exists or compounds with token-tax
- That any specific model provider is acting in bad faith
- That the socio-economic correlation implies causation (it is correlational)
- That the problem is fully solvable with current architectures
- That BLOOMZ's data-balancing approach fully resolves the disparity (it improves but does not eliminate it)

## Connection to token-tax, execution-tax, or tokens-per-watt

**Token-tax:** This paper is the primary source for token-tax as a named, quantified, API-level economic phenomenon. The cost-relative-to-English metric (Figures 4, 5, 16) is the direct economic expression of token-tax.

**Execution-tax:** Not addressed. The paper studies single-call API interactions, not multi-step agentic workloads. The context-window exhaustion finding (RQ3) is adjacent — it shows that token inflation degrades the quality of a single call — but it is not execution-tax.

**Tokens-per-watt:** Not directly addressed. However, the finding that high-fragmentation languages exhaust context windows faster implies that effective semantic throughput per token is lower for these languages — which is conceptually aligned with tokens-per-watt degradation.
