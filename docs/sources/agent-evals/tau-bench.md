# τ-bench (Tau-Bench) — Agent Benchmark

## Type

Agent evaluation / methodology source — academic benchmark for tool-use and multi-step agent evaluation.
Methodology context only. Not scientific proof of execution-tax. Does not directly address token-tax.

## Source files

- **This file:** Working notes for the NiceM project — methodology reference
- **Conflict rule:** If this summary and the original source appear to conflict, flag it before deciding

## Source links

| Source | Type | Date | Link |
|---|---|---|---|
| τ-bench paper / repository | Academic paper / benchmark | TODO: confirm date | TODO: add link |

*All links are TODO until confirmed.*

---

## Main claim

TODO: Add once source is read and verified.

---

## Relevance to NiceM

TODO: Add once source is read and verified.

τ-bench is a benchmark designed to evaluate LLM agents on realistic, multi-step, tool-using tasks — particularly in retail and airline domains. Its evaluation methodology is relevant to NiceM because it measures agent task completion across multiple turns and tool calls, not just single-shot accuracy. This multi-step structure is the architecture in which execution-tax (NiceM hypothesis) would be measurable.

τ-bench is also relevant because it defines what "task success" means in a multi-step agent context — a prerequisite for NiceM's cost-per-successful-completion metric.

---

## What this supports

TODO: Add once source is read and verified.

Anticipated support: τ-bench likely demonstrates that multi-step agent tasks have variable completion costs (different numbers of turns, tool calls, and retries across runs and models) — which is the behavioral foundation that execution-tax measurement would build on.

---

## What this does not prove

- That execution-tax exists as a systematic, measurable overhead (τ-bench measures task performance, not overhead decomposition)
- That token-tax contributes to multi-step task difficulty (not addressed in τ-bench's design)
- That token-tax and execution-tax compound
- Any NiceM-specific claim about overhead attribution

---

## Connection to agent evaluation

TODO: Add once source is read and verified.

Anticipated connection: τ-bench is one of the more rigorous existing benchmarks for multi-step tool-using agents. Its task design, success criteria, and evaluation protocol are directly relevant to how NiceM would design a controlled execution-tax experiment.

---

## Connection to execution-tax

TODO: Add once source is read and verified.

Anticipated connection: τ-bench's multi-turn structure makes it a candidate methodology for NiceM's execution-tax measurement: the same task, run across different languages or agent architectures, with total turn count and token cost as outcome variables. If performance varies by language or architecture, that variation is consistent with execution-tax.

Note: τ-bench does not measure or define execution-tax. It provides a task structure in which execution-tax could be observed if it exists.

---

## Notes for NiceM positioning

TODO: Add once source is read and verified.

Anticipated positioning note: τ-bench establishes that rigorous multi-step agent evaluation is feasible and reproducible. NiceM's execution-tax measurement methodology could be designed as an extension of τ-bench-style evaluation — same task success criteria, but with added overhead attribution across step types and languages.
