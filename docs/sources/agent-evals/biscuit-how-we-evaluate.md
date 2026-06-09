# Biscuit — How We Evaluate Agents

## Type

Agent evaluation / methodology source — practitioner blog or documentation.
Methodology context only. Not scientific proof. Does not prove token-tax or execution-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| "How We Evaluate Agents" — Biscuit | Blog post / documentation | TODO | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

Biscuit structures agent evaluation around **scenarios** (concrete task situations the agent must handle), **capabilities** (the distinct skills or behaviors being tested), **automated checks** (programmatic assertions about agent output), **trend tracking** (monitoring performance over time rather than at a single snapshot), and **uncertainty** (acknowledging that agent behavior is non-deterministic and that evaluation must account for variance).

TODO: Verify and add verbatim quotes once source is confirmed.

---

## Relevance to NiceM

Biscuit's framework addresses whether an agent succeeded and how reliably it succeeds across scenarios and capabilities. NiceM borrows the scenario/capability mindset but applies it to a different question:

> Not only whether the agent succeeded, but **how much execution workload was required for success** — and whether that workload differs across languages, task types, models, and agent designs.

In Biscuit's terms: NiceM holds the scenario and capability fixed, then measures the execution cost axis that Biscuit does not track. Biscuit asks "did the agent pass?" NiceM asks "what did passing cost, and is that cost the same for all languages?"

The combination of both questions — correctness and execution cost — is NiceM's cost-per-successful-completion metric.

---

## What this supports

- Agent evaluation can and should be structured around discrete scenarios and capabilities — not just aggregate accuracy
- Automated checks are feasible for agent output at scale — which supports the scalability of NiceM's measurement methodology
- Trend tracking matters: agent performance (and therefore execution cost) is not a fixed number — it varies over time, model versions, and context conditions
- Uncertainty and non-determinism in agent behavior are expected and should be accounted for in evaluation design — NiceM must handle this in its execution-tax benchmarks

---

## What this does not prove

- That execution-tax exists or is quantifiable
- That execution workload varies by language (a NiceM hypothesis, not a Biscuit claim)
- That the scenario/capability framework is sufficient for NiceM's purposes without modification
- Token-tax in the academic sense (Petrov, Ahia, Lundin)

---

## Connection to agent evaluation

Biscuit's structured evaluation approach — scenarios, capabilities, automated checks, trend tracking, uncertainty — provides a practical methodology template for NiceM's execution-tax benchmark design.

Applied to NiceM, the translation would be:

| Biscuit concept | NiceM application |
|---|---|
| Scenario | A fixed human intent (e.g., "answer this FAQ question in language X") |
| Capability | The agent behavior being tested (retrieval, tool use, multi-turn reasoning) |
| Automated check | Did the agent succeed? (success criterion required before cost is meaningful) |
| Trend tracking | Does execution cost change as models, tokenizers, or architectures evolve? |
| Uncertainty | Multiple runs per scenario/language combination; execution cost as a distribution, not a point estimate |

---

## Connection to execution-tax

Biscuit does not define or measure execution-tax. Its relevance is structural: the scenario/capability decomposition is exactly the experimental design NiceM needs to isolate execution-tax.

By holding the scenario fixed and varying the language or agent architecture, NiceM can ask: does the execution workload change? If it does, that variation is consistent with execution-tax. The scenario framework makes the comparison controlled; the capability dimension makes the source of overhead attributable.

Execution-tax remains a NiceM hypothesis. Biscuit's framework is a methodology the hypothesis can be tested within — not evidence that it exists.

---

## Notes for NiceM positioning

Biscuit demonstrates that rigorous, structured agent evaluation is a practical, operational concern — not just an academic one. Teams building real agents are already thinking in terms of scenarios, capabilities, and automated trend tracking.

NiceM's positioning opportunity: existing evaluation frameworks measure whether agents succeed. NiceM adds the execution cost dimension — how much workload was required for that success, and whether the cost is equitable across languages and architectures. This is a natural extension of what practitioners are already doing, not a departure from it.

The scenario/capability mindset also makes NiceM's execution-tax claims more credible: by grounding them in a structured, reproducible evaluation design rather than anecdotal overhead observations.
