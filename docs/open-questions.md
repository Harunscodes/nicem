# NiceM — Open Questions

This document tracks what is not yet known, not yet proven, and not yet decided. It is a living document. Questions should be moved to resolved when answered with evidence or closed when determined to be out of scope.

---

## Research questions

### On token-tax

- **Q1:** What is the token-tax multiplier for the languages/scripts most relevant to NiceM's target context? (i.e., how many more tokens does an equivalent sentence require in each language compared to English?)
  - *Partially addressed by: Petrov et al., Ahia et al. — TODO: extract specific figures*

- **Q2:** Does token-tax vary across different model providers' tokenizers, or is it consistent across the field?
  - *Status: Open*

- **Q3:** Has token-tax improved over time as newer tokenizers have been released? Is the trend improving or stable?
  - *Status: Open*

---

### On execution-tax (NiceM hypothesis)

- **Q4:** Can execution-tax be measured empirically? What is the methodology?
  - *Status: Open — core hypothesis validation question*

- **Q5:** What share of total tokens in a typical agentic workflow are overhead (orchestration, scaffolding, repeated context) vs. task content?
  - *Status: Open — requires measurement*

- **Q6:** Does execution-tax vary significantly by workload architecture (e.g., single-agent vs. multi-agent, tool-heavy vs. reasoning-heavy)?
  - *Status: Open*

- **Q7:** Is execution-tax reducible without degrading task quality? What architectural changes reduce it?
  - *Status: Open — requires experimentation*

- **Q8:** Do token-tax and execution-tax compound in real workloads? By how much?
  - *Status: Open*

---

### On industry context

- **Q9:** Is tokens-per-watt used as an internal efficiency metric by AI infrastructure operators, or is it primarily a public-facing narrative?
  - *Status: Partially addressed — NVIDIA uses tokens-per-watt and cost-per-token as product comparison metrics across hardware generations (Vera Rubin vs. Blackwell). This is more than a narrative framing; it appears in product specifications and technical blogs. Whether it is used as an internal engineering KPI is not confirmed. See `docs/sources/industry/jensen-huang-ai-factories-tokens-per-watt.md`, S2–S4.*

- **Q10:** Are there existing tools or benchmarks that measure execution overhead in agentic pipelines?
  - *Status: Partially addressed — NVIDIA NeMo Agent Toolkit supports per-step token and timing tracking and bottleneck identification. Langfuse, LangSmith, and Arize Phoenix offer observability at the workflow level. None of these define or measure execution-tax in NiceM's sense — they provide the instrumentation substrate that controlled execution-tax measurement would require. See `docs/sources/industry/nvidia-agents-infrastructure-notes.md` and `docs/sources/agent-evals/`.*

- **Q15:** What are the original NVIDIA / Jensen Huang sources for the following claims that currently appear in chat-derived notes?
  - "Human language is the new programming language" (exact source and quote)
  - "Electrons to tokens" or equivalent AI factory framing (exact source)
  - Performance improvement vs. demand growth argument (exact source and quote)
  - Open-source AI ecosystem framing (exact source)
  - *Status: Open — all four need source verification before citation. See `docs/sources/notes/nvidia-jensen-chat-context.md`.*

---

## Methodology questions before validation

These questions must be answered — or at minimum scoped — before NiceM can run a valid execution-tax measurement experiment. They are not research hypotheses; they are design decisions whose answers determine whether the experiment is sound.

- **M1:** How should NiceM define successful completion?
  - What counts as success: a correct final answer, a completed workflow, a user-approved outcome, or all three? Does partial completion count? The definition must be precise enough to apply consistently across languages and task types.
  - *Status: Open — blocking for any measurement experiment*

- **M2:** Should success be judged by humans, automated judges, deterministic checks, or a hybrid?
  - Each approach has different cost, scalability, and bias profiles. Human annotation is expensive but reliable. Automated LLM judges are scalable but may be biased toward high-resource languages. Deterministic checks are language-neutral where applicable but require tasks with verifiable outputs.
  - *Status: Open — see `docs/sources/agent-evals/agent-as-a-judge.md`*

- **M3:** How can NiceM avoid evaluator bias toward English or high-resource languages?
  - An automated judge that rates Turkish agent outputs less reliably than English outputs will produce biased success classifications, making any execution-tax signal untrustworthy. The evaluator's cross-language reliability must be characterized before results are valid.
  - *Status: Open — critical for multilingual validity*

- **M4:** How can NiceM distinguish execution-tax from token-tax in a measurement?
  - If a Turkish-language run uses more total tokens than an English run, is that token-tax (the input was longer), execution-tax (the agent took more steps), or both? NiceM needs a decomposition method to attribute overhead to its source — otherwise token-tax and execution-tax cannot be separately quantified.
  - *Status: Open — methodological design question*

- **M5:** Which metrics belong to agent trajectory evaluation, and which to output evaluation?
  - Trajectory metrics (steps taken, tool calls made, retries, tokens per step) measure the execution path. Output metrics (answer correctness, task completion, quality score) measure the endpoint. NiceM needs both, but they require different evaluation methods and must not be conflated.
  - *Status: Open — see `docs/sources/agent-evals/tau-bench.md` and `biscuit-agent-evaluation.md`*

- **M6:** How should retries, tool calls, retrieval calls, and human correction be counted toward execution-tax?
  - A retry that succeeds on the second attempt is more expensive than one that succeeds on the first — but by how much? Should failed intermediate steps count at full weight, half weight, or be excluded from cost-per-successful-completion? The counting rule must be defined before the metric is computed.
  - *Status: Open — design decision with significant metric impact*

- **M7:** What would falsify the execution-tax hypothesis?
  - A well-formed hypothesis must be falsifiable. A candidate falsification condition: if cost-per-successful-completion is statistically equivalent across language conditions after controlling for input token count, execution-tax in the agentic sense does not exist in that architecture. NiceM should specify this condition precisely before running any experiment.
  - *Status: Open — important for scientific credibility*

- **M8:** What is the minimum number of languages, tasks, and runs needed for a statistically meaningful execution-tax measurement?
  - Agent behavior is non-deterministic. A single run per language condition is not sufficient. How many runs per cell, how many task types, and how many language conditions are needed to detect an execution-tax effect of a given size?
  - *Status: Open — statistical design question*

- **M9:** Which instrumentation platform should NiceM use for the proof-of-concept measurement?
  - Candidates: Langfuse (open-source, span-level), Arize Phoenix (open-source, OpenTelemetry), LangSmith (LangChain-native), NeMo Agent Toolkit (NVIDIA). The choice depends on the agent framework used and the granularity of per-step attribution needed.
  - *Status: Open — see `docs/sources/agent-evals/` for platform notes*

---

## Definitional questions

- **Q11:** Is NiceM's definition of execution-tax consistent with any existing concept in the literature (e.g., inference overhead, KV cache cost, prompt engineering waste)?
  - *Status: Open — literature review needed*

- **Q12:** Should token-tax in NiceM's framing be restricted to language/script disparity, or expanded to include input modality (code vs. prose, structured vs. unstructured)?
  - *Status: Open — scoping decision*

---

## Strategic questions

- **Q13:** Who is the primary audience for NiceM — AI infrastructure operators, end users, policymakers, or model developers?
  - *Status: Open — affects thesis framing and product direction*

- **Q14:** Is NiceM's contribution primarily a measurement framework, a cost attribution tool, an architectural recommendation, or something else?
  - *Status: Open*

---

## Resolved questions

*(Move questions here when answered, with a brief note on the resolution and the source.)*

| Question | Resolution | Source |
|---|---|---|
| Does token-tax exist? | Yes — established in literature | Petrov et al., Ahia et al., Lundin |
| Is token-tax an API cost problem, not just a tokenization problem? | Yes — pricing is per-token | Ahia et al. |
| Is agentic infrastructure a real and growing industry direction? | Yes — confirmed by NVIDIA and Jensen Huang | Industry sources |
