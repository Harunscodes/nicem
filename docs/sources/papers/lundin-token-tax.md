# Lundin et al. — The Token Tax

## Type

Academic paper — arXiv preprint, September 2025 (under review)
Full title: *The Token Tax: Systematic Bias in Multilingual Tokenization*
Authors: Jessica M. Lundin (Gates Foundation / Institute for Disease Modeling), Ada Zhang, Nihal Karim, Hamza Louzan, Victor Wei, Cody Carroll (University of San Francisco), David Adelani (McGill University)

## Source files

- **Original PDF:** `docs/sources/papers/pdf/lundin-token-tax.pdf`
- **This file:** Interpreted source notes for the NiceM project — the primary working reference
- **Conflict rule:** If this summary and the PDF appear to conflict, flag it before deciding

## Main claim

Tokenization inefficiency ("token tax") is not just a cost problem — it is a systematic accuracy problem. Using AfriMMLU (9,000 multiple-choice questions across 5 subjects in 16 African languages), the paper shows that **fertility (tokens per word) reliably predicts accuracy**: higher fertility consistently predicts lower accuracy across all 10 models tested. A doubling in tokens produces a 4× increase in training cost and time (due to O(n²) attention scaling), making token inflation an existential economic barrier for low-resource language AI development.

## Key quantitative findings

**Fertility-accuracy regression (across 10 models, 5 subjects):**
- Slopes range from −0.08 to −0.18 per token/word increase
- Fertility explains 20–50% of variance in accuracy (R²)
- Statistically significant results: Llama-3.1-405B on Microeconomics (slope = −0.185, p = 0.002), Qwen-2.5-32B on Geography (slope = −0.155, p = 0.006)
- African languages trail English by ~25 accuracy points on average

**Reasoning models narrow but do not close the gap:**
- DeepSeek R1 and o1 outperform non-reasoning models by 8–12 points on African languages
- In Global Facts, the English–African gap narrows from 25 points to 12–14 points under reasoning models
- The structural tokenization disadvantage persists even with reasoning capabilities

**Economic consequences of token inflation (O(n²) training scaling):**

| Model | English training cost | Language X (2× fertility) cost |
|---|---|---|
| LLaMA 2 (69B) | $5M | $20M |
| LLaMA 3 (70B) | $24M | $96M |
| LLaMA 3.1 (405B) | $105M | $420M |

**Inference cost (per 1M English-equivalent tokens):**

| Provider | Model | English | Language X (2× fertility) |
|---|---|---|---|
| OpenAI | GPT-4o | $5/$20 | $10/$40 |
| Anthropic | Claude 4 Sonnet | $3/$15 | $6/$30 |
| Google | Gemini 2.5 Flash | $0.30/$2.50 | $0.60/$5.00 |

**Definition of fertility:** F = T/W (tokens divided by words). Higher F → longer sequences → more compute.

**Definition of parity (from Petrov et al., cited):** Parity = |t(sA)| / |t(sB)|. Scores above 1 indicate language A tokenizes less efficiently than language B (English baseline).

## Relevance to NiceM

This is the most recent paper in the token-tax literature (2025) and provides the most direct economic quantification. Key contributions to NiceM:

1. **Names and formalizes "token tax"** as an established concept, not just a colloquial description
2. **Connects token inflation to accuracy degradation** — not just cost, but measurable performance harm
3. **Quantifies the O(n²) scaling consequence** — the 4× cost multiplier for 2× fertility is a concrete number NiceM can use
4. **Extends the analysis to reasoning models** — shows that improved reasoning reduces but does not eliminate the structural disadvantage
5. **The fertility metric** (tokens/word) is directly usable as a measurement methodology for NiceM's token-tax measurement work

## What this supports

- Token-tax is a named, formally defined concept in the NLP literature (confirms NiceM's use of the term)
- Token-tax degrades accuracy, not just cost — the harm is dual
- The O(n²) training scaling means token-tax is not just an API pricing quirk but a fundamental compute barrier
- Fertility (tokens/word) is a reliable and validated proxy metric for token-tax impact
- Reasoning capabilities improve but cannot structurally eliminate the tokenization disadvantage
- Token inflation is an existential barrier to language-equitable AI development

## What this does not prove

- That execution-tax exists (this paper does not address agentic or multi-step workloads)
- That token-tax and execution-tax compound (out of scope)
- That the 4× training cost multiplier applies at inference for NiceM's use cases (it applies to training; inference scales approximately linearly)
- That morphologically aware tokenization fully solves the problem (proposed but not demonstrated)
- That the AfriMMLU findings generalize beyond African languages (though prior work suggests they do)

## Connection to token-tax, execution-tax, or tokens-per-watt

**Token-tax:** This paper names and formally defines the concept. The fertility metric (F = T/W) and the O(n²) cost scaling together explain why token-tax is not just a pricing issue but a structural compute barrier. The paper's economic tables (Tables 2–3) give NiceM concrete numbers to cite.

**Execution-tax:** Not addressed. All analysis is on single-call inference and static text tokenization.

**Tokens-per-watt:** The paper's core economic argument is directly expressible in tokens-per-watt terms: if language X requires 2× more tokens for equivalent content, and training cost scales as O(n²), then language X requires 4× more energy per unit of semantic output. Tokens-per-watt is inversely proportional to fertility — high fertility languages have lower tokens-per-watt efficiency.
