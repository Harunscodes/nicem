# Biscuit — Agent Evaluation

## Type

Agent evaluation / methodology source — practitioner blog or documentation.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| "How We Evaluate Agents" — Biscuit | Blog post / documentation | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

Biscuit structures agent evaluation around **scenarios** (concrete task situations the agent must handle), **capabilities** (the distinct skills or behaviors being tested), **automated checks** (programmatic assertions about agent output), **trend tracking** (monitoring performance over time, not only at a single snapshot), and **uncertainty** (acknowledging that agent behavior is non-deterministic and evaluation must account for variance).

TODO: Verify and add verbatim quotes once source is confirmed.

---

## Relevance to NiceM

Biscuit's framework addresses whether an agent succeeded and how reliably it succeeds across scenarios and capabilities. NiceM borrows the scenario/capability mindset but applies it to a different question:

> Not only whether the agent succeeded, but **how much execution workload was required for success** — and whether that workload differs across languages, task types, models, and agent designs.

Biscuit asks "did the agent pass?" NiceM asks "what did passing cost, and is that cost the same for all languages?"

The combination of both questions — correctness and execution cost — is NiceM's cost-per-successful-completion metric.

---

## What this supports

- Agent evaluation can be structured around discrete scenarios and capabilities — not just aggregate accuracy
- Automated checks are feasible for agent output at scale, supporting the scalability of NiceM's measurement methodology
- Trend tracking matters: execution cost is not a fixed number — it varies over time, model versions, and context conditions
- Uncertainty and non-determinism in agent behavior must be accounted for in evaluation design — NiceM should treat execution cost as a distribution, not a point estimate

---

## What this does not prove

- That execution-tax exists or is quantifiable
- That execution workload varies by language (a NiceM hypothesis, not a Biscuit claim)
- That the scenario/capability framework is sufficient for NiceM's purposes without modification
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to successful completion

Biscuit's automated checks define what counts as a successful run. This is the prerequisite for NiceM's cost-per-successful-completion metric — a run must be classified as successful or failed before its cost can be meaningfully compared across language conditions.

The Biscuit framework's separation of scenario (task situation) from capability (skill being evaluated) also clarifies what success means: it is not just "produced output" but "demonstrated the specific capability the scenario was designed to test." NiceM must define success at this level of specificity to avoid measuring cost against an ambiguous or inconsistently applied criterion.

---

## Connection to agent trajectory evaluation

Biscuit's scenario/capability structure implicitly requires evaluating the agent's path, not only its output. Whether a capability was demonstrated depends on what the agent did — which tools it called, whether it retrieved the right information, how it reasoned. This is trajectory evaluation: judging the sequence of agent actions, not only the final answer.

NiceM needs trajectory evaluation because execution-tax is a property of the path (how many steps, how many tokens, how many retries) — not only the endpoint. Biscuit's framework provides the scenario structure within which trajectory evaluation would operate.

---

## Connection to execution-tax

Biscuit does not define or measure execution-tax. Its relevance is structural: the scenario/capability decomposition is exactly the experimental design NiceM needs to isolate execution-tax.

By holding the scenario fixed and varying the language or agent architecture, NiceM can ask: does the execution workload change? If it does, that variation is consistent with execution-tax. The scenario framework makes the comparison controlled; the capability dimension makes the source of overhead attributable.

Execution-tax remains a NiceM hypothesis. Biscuit's framework is a methodology the hypothesis can be tested within — not evidence that it exists.

---

## Risks or limitations for multilingual evaluation

- Automated checks designed for English outputs may not generalize to other languages. Lexical matching, named-entity checks, and format validation may behave differently across scripts and morphologies.
- Scenario equivalence across languages is not guaranteed. A task described identically in two languages may not be genuinely equivalent in difficulty, ambiguity, or retrieval tractability.
- Trend tracking across model versions may conflate model improvement with tokenizer changes, making it difficult to isolate the language-driven component of execution cost over time.

---

## Notes for NiceM methodology

- The Biscuit scenario/capability framework is a strong organizational template for NiceM's benchmark design. Each scenario = a fixed human intent; each capability = the agent behavior being measured; each check = the success criterion before cost attribution.
- Uncertainty handling is critical: NiceM should run multiple trials per scenario/language combination and report execution cost as a distribution with variance, not a single-run figure.
- The trend-tracking dimension is relevant for NiceM's long-term question: does execution-tax change as tokenizers, models, and agentic frameworks improve?

*Note: An earlier version of this source note exists at `docs/sources/agent-evals/biscuit-how-we-evaluate.md`. This file supersedes it with the updated template structure.*
