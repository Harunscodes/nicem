# NiceM — Startup Thesis v0.1

**Status:** Internal working document. Not for public distribution. Not a pitch deck.
**Version:** 0.1 — first coherent thesis draft
**Source boundary:** Academic claims are grounded in Petrov et al. (NeurIPS 2023), Ahia et al. (arXiv 2023), and Lundin et al. (arXiv 2025). Industry claims from NVIDIA sources are marked with their verification status. NiceM hypotheses are labeled as such throughout.

---

## 1. The problem

AI systems are no longer primarily chat systems. They are becoming execution systems.

A user who asks an AI agent to "book the cheapest flight from Amsterdam to Istanbul under €300" is not sending a message. They are initiating a workflow: the agent understands intent, retrieves options, filters by constraint, calls an API, validates the result, and returns an answer or action. That workflow consumes compute, memory, retrieval calls, tool calls, time, and money.

The shift from chat to execution is architectural. Production AI systems increasingly involve multiple models operating in sequence or parallel, tool use and external API calls, memory retrieval and context management, multi-turn reasoning and planning loops, and retry logic when earlier steps fail. NVIDIA explicitly frames this as the production AI workload frontier — its Vera Rubin platform is designed for agentic AI and multi-step problem-solving, and its NeMo Agent Toolkit supports workflow-level profiling at the tool and agent step level. (Sources: NVIDIA Vera Rubin platform page, NeMo Agent Toolkit documentation — links TODO, see source verification checklist.)

In this architecture, the interface between humans and AI is natural language. Humans express intent in language; AI systems translate that intent into computation. The language of the request is not just a communication choice — it is the entry point into the execution path.

**The core observation:** If human language is the interface for AI execution systems, then the properties of that language — how it is tokenized, how long it is, how it interacts with retrieval, how many tokens a model needs to reason about it — affect the total cost of executing that intent. Different languages may not be equally expensive to execute.

---

## 2. The research foundation: token-tax

The academic literature establishes that tokenization — the process of converting text into the token sequences that language models process — is not language-neutral.

### What the research shows

**Petrov et al. (NeurIPS 2023)** studied 200 languages on the FLORES-200 parallel corpus and found that the same text translated into different languages produces drastically different tokenization lengths using the same tokenizer. Shan requires up to 15× more tokens than English on ChatGPT/GPT-4 tokenizers; Bulgarian requires 2.64×; Arabic 3.04×. Even the most efficiently tokenized non-English language (Portuguese) still pays approximately a 50% premium. Since API pricing is per token, this premium translates directly into a cost differential for users working in those languages.

**Ahia et al. (arXiv 2023)** studied 22 languages across five NLP tasks and quantified the API cost inequality. Telugu users pay approximately 4× more than English users for the same task. The context window impact is severe: Telugu and Amharic cannot fit even a single in-context example for the majority of test cases, where English can fit ten or more. The paper also identifies a socio-economic correlation: the languages with the highest fragmentation rates tend to be spoken in countries with the lowest Human Development Index scores. The populations most harmed by token-tax are those least able to absorb the additional cost.

**Lundin et al. (arXiv 2025)** named and formally defined token-tax, and connected it to accuracy — not just cost. Using the AfriMMLU benchmark (9,000 multiple-choice questions across 16 African languages and 5 subjects), the paper shows that fertility (tokens per word) reliably predicts accuracy: a one-unit increase in fertility corresponds to an 8–18 percentage point drop in accuracy depending on model and subject. Fertility explains 20–50% of accuracy variance across the ten models tested. African languages trail English by approximately 25 accuracy points on average. Even reasoning models (DeepSeek R1, o1), which narrow the gap by 8–12 points, do not close it.

### What the research does not address

The token-tax literature focuses on the tokenization layer: how many tokens a piece of text requires, what that costs at the API level, and how it affects single-call inference quality. It does not study:

- Full multi-step agentic workflows
- How token-tax propagates through retrieval, tool use, or multi-turn reasoning
- Whether overhead compounds across agent steps
- Execution cost beyond the token count of a single API call

This gap is the starting point for NiceM.

---

## 3. The gap: from representation cost to execution cost

Token-tax research measures representation cost: how many tokens does this text require to be represented in a model's input sequence?

What it does not measure is execution cost: how much total AI workload — tokens, retrieval calls, tool calls, retries, context expansion, latency, human correction — is required to complete the same human intent successfully?

The distinction matters because in agentic AI systems, the total cost of completing a task is not determined by the input token count alone. It is determined by the entire execution path: how the agent understands the intent, what it retrieves, what tools it calls, how many steps it takes, how often it retries, and whether it succeeds.

A concrete illustration: a user submits a product FAQ question in English and in Turkish. The English version tokenizes compactly; the Turkish version requires more tokens due to morphological richness. In a single-call chat system, this token-tax difference is the entire cost difference. In an agentic FAQ system, there may be additional effects: the Turkish query may retrieve different or fewer relevant documents, may require more model reasoning steps to interpret, may produce a lower-confidence answer that triggers a retry, and may require human correction more often. The total execution workload for the same task, in two languages, may differ by more than the token-tax alone explains.

NiceM hypothesizes that this difference — the total execution cost gap beyond the tokenization-layer token-tax — is real, measurable, and systematic. NiceM calls this execution-tax.

---

## 4. The NiceM hypothesis: execution-tax

**Hypothesis:** For the same human intent, different languages, task types, prompts, retrieval strategies, tools, and agent designs create different total AI execution workloads.

This is the execution-tax hypothesis. It is a NiceM hypothesis. It is not proven by existing literature. It requires empirical validation.

### What execution-tax includes

Execution-tax is the extra total AI workflow burden required to complete the same human intent successfully. Its components are:

- **Token overhead:** tokens consumed by orchestration, scaffolding, repeated context, and system prompt re-injection across steps — beyond the tokens directly required to process the task content
- **Retrieval overhead:** retrieval calls, retrieved tokens, re-ranking steps, and failed retrievals that add latency and cost without contributing to the final answer
- **Tool overhead:** tool calls, API calls, and the tokens required to interpret tool outputs
- **Retry overhead:** repeated attempts when earlier steps produce low-confidence, incorrect, or incomplete results
- **Context expansion:** growing context windows across multi-turn reasoning, which increase attention cost at each step
- **Latency cost:** time cost of sequential agent steps, which may affect end-user experience and infrastructure scheduling
- **Human correction:** cases where the agent fails and a human must intervene — the most expensive form of overhead

### The compounding question

Token-tax and execution-tax may compound. If a language requires more tokens at the tokenization layer, the effects may propagate: longer inputs may result in longer retrieved documents, more model reasoning steps to interpret the query, less room in the context window for in-context examples (as Ahia et al. demonstrate for single calls), and higher failure rates that trigger retries. Whether and how much these effects compound is an open empirical question. It is not assumed.

### What execution-tax is not

- It is not a claim that all languages always perform worse in agentic systems
- It is not a claim that translation eliminates the problem (translation may introduce its own overhead)
- It is not a claim that token-tax is the only or dominant source of execution overhead
- It is not proven by any existing source

---

## 5. The core metric: cost per successful completion

Existing AI efficiency metrics tend to measure either cost (tokens consumed, API spend) or quality (task accuracy, answer correctness) independently.

NiceM proposes that the primary metric should combine both: **cost per successful completion**.

A cheap failed run is not efficient. An expensive successful run may be justified. The question is: how much total workload — cost, latency, tokens, steps — is required to complete the same human intent successfully?

This metric has several components:

| Metric | What it measures |
|---|---|
| Cost per successful completion | Total API and infrastructure cost for runs that succeed |
| Tokens per successful completion | Total tokens consumed across all steps of a successful run |
| Latency per successful completion | End-to-end time for successful runs |
| Retry rate | Proportion of runs that require more than one attempt |
| Human correction rate | Proportion of runs that require human intervention |
| Success rate | Proportion of runs that complete the intent correctly |

These metrics together define the execution efficiency of an AI system for a given task, in a given language, under a given architecture. They are the measurement space for execution-tax.

The long-term infrastructure expression of this is **successful intent per watt**: how much useful human intent is completed per unit of energy consumed. This is NiceM's proposed extension of NVIDIA's tokens-per-watt metric — adding the outcome dimension. (Tokens-per-watt is a verified NVIDIA product metric; successful intent per watt is a NiceM concept.)

---

## 6. The industry context: why execution efficiency matters now

Three converging industry trends make execution efficiency economically important at the infrastructure level.

### AI factories and token throughput

NVIDIA frames AI infrastructure as "AI factories" — purpose-built infrastructure producing tokens at scale, continuously, efficiently. The primary efficiency metric is tokens per watt and cost per token. NVIDIA states that its Vera Rubin platform delivers more tokens per watt and lower cost per token than its Blackwell predecessor, and frames this as a key competitive specification. A NVIDIA technical blog frames AI factory economics around revenue per megawatt. (Sources: NVIDIA Vera Rubin platform page, *Scaling Token Factory Revenue* blog — links TODO, see source verification checklist.)

**NiceM relevance:** If the industry measures AI infrastructure efficiency in tokens-per-watt, then any structural source of token waste — token-tax overhead, execution-tax overhead — degrades that metric and has infrastructure-level economic consequences. This is not a developer-pricing problem; it is a factory-efficiency problem.

### Agentic workloads as the production frontier

NVIDIA's GTC 2026 keynote covers the full AI stack including agentic systems, and NVIDIA's product materials explicitly frame Vera Rubin as built for the era of agentic AI and multi-step reasoning. The NeMo Agent Toolkit documentation describes support for profiling entire agent workflows down to the tool and agent level, tracking input and output tokens and timings, and identifying bottlenecks. (Sources: NVIDIA GTC 2026, Vera Rubin platform page, NeMo Agent Toolkit — links TODO.)

**NiceM relevance:** Agentic workloads are the architecture in which execution-tax becomes visible. Single-call inference has no inter-step overhead to measure; multi-step agentic workflows accumulate overhead at every step. NVIDIA's acknowledgment that this is the production workload frontier means execution-tax — if it exists — applies to a growing share of AI compute.

### KV-cache and long-context overhead

The Vera Rubin newsroom discusses storage and retrieval of massive key-value cache data generated by LLMs and agentic AI workflows as an infrastructure concern. This is an acknowledgment of the memory and retrieval overhead that agentic systems generate at scale — directly adjacent to the components NiceM hypothesizes contribute to execution-tax. (Source: NVIDIA Vera Rubin newsroom — link TODO.)

### The demand growth context

Jensen Huang has been quoted: *"AI computing demand for both training and inference is going through the roof."* (NVIDIA Rubin newsroom, January 2026 — direct link TODO, verbatim quote pending confirmation.) If demand grows faster than hardware efficiency improvements, workload management becomes more important over time, not less. Enterprises that understand where their AI compute is going — which workflows are expensive, which languages create more overhead, which agent designs are inefficient — will have a structural cost advantage.

**Unverified framing (do not cite publicly):** The conversation has also surfaced the idea that Jensen Huang frames human language as the new programming language, and that AI factories convert electrons to intelligence. These framings are consistent with NVIDIA's publicly reported positions but have not yet been traced to specific primary sources. See `docs/sources/notes/source-verification-checklist.md`, Priority 1.

---

## 7. The product direction: AI Execution Intelligence

NiceM is not a generic LLM observability dashboard.

Existing observability tools (Langfuse, LangSmith, Arize Phoenix, Braintrust) measure whether agents succeed and how much they cost. They are excellent at what they do. NiceM's contribution is not to replace them but to answer a different question: does execution cost vary systematically by language, task type, and agent design for the same human intent?

NiceM is **AI Execution Intelligence**:

```
observe → diagnose → recommend → simulate → human-approve → measure impact
```

- **Observe:** Measure total execution workload across agent runs — tokens, steps, latency, cost, retry rate, success rate — broken down by language, task type, and architecture
- **Diagnose:** Identify where execution-tax accumulates — which step types, which language conditions, which architectural choices create overhead
- **Recommend:** Propose architectural changes — retrieval strategy, prompt design, model choice, context management — that reduce execution overhead without degrading task quality
- **Simulate:** Model the projected cost and quality impact of proposed changes before deployment
- **Human-approve:** Surface the tradeoff clearly so a human can decide whether the efficiency gain is worth the change
- **Measure impact:** Confirm that the change reduced execution overhead in practice

This pipeline distinguishes NiceM from observability tools (which stop at observe) and from model evaluation tools (which focus on quality, not execution efficiency). NiceM's value is the full loop: measure, understand, improve, confirm.

The primary audience is AI infrastructure operators and enterprise AI teams who need to understand the execution cost of their agentic workloads — not just whether the agent answered correctly.

---

## 8. What NiceM is not

**Not a generic LLM observability dashboard.** Observability is a prerequisite, not the product. NiceM's value is in the diagnosis and recommendation loop, not in the trace collection.

**Not a tokenizer replacement.** NiceM does not propose to fix token-tax by redesigning tokenizers. The academic literature suggests that even purpose-built multilingual tokenizers do not fully solve the problem. NiceM measures and optimizes the execution layer — it works with existing tokenizers.

**Not a claim that all languages always perform worse.** Token-tax and execution-tax vary by language, script, task type, model, and architecture. Some language-task-model combinations may show no significant execution overhead. The hypothesis is that the overhead is real and systematic in aggregate — not that it applies universally and uniformly.

**Not a claim that execution-tax is already proven.** Execution-tax is a NiceM hypothesis. It requires empirical validation. Nothing in the existing literature directly proves that multi-step agentic workflows have systematically higher execution costs for certain languages or task types.

**Not connected to employer, customer, or internal data.** NiceM is an independent personal research project. All examples and experiments use neutral synthetic tasks. No employer data, customer data, or proprietary workflows are used.

---

## 9. First validation path

Before building a SaaS product, NiceM should validate the execution-tax hypothesis. The validation question is:

> For the same human intent, expressed in different languages, does a controlled agentic workflow require measurably different total execution workloads?

### Proposed validation design

**Task:** A fixed set of synthetic tasks with equivalent semantic content across 4–6 languages. Candidate: a multilingual product FAQ assistant, a travel assistant, or a research assistant — all using publicly available, non-proprietary content. Languages should include English (baseline), at least one high-token-tax language (e.g., Turkish, Arabic, or a language studied in Petrov/Ahia), and at least one lower-token-tax language (e.g., Portuguese or Dutch).

**Agent design:** A controlled multi-step agentic pipeline — intent understanding, retrieval, answer generation, validation. Architecture held constant across languages; only the input language varies in the first experiment.

**Measurement:** For each run, record total tokens consumed (across all steps), number of agent steps, latency, cost, retry count, and success/failure. Success defined by a rubric-based scorer (automated judge or human annotation — methodology TBD, see agent-evals sources).

**Comparison:** Compare cost-per-successful-completion, tokens-per-successful-completion, retry rate, and step count across language conditions. If these metrics differ systematically across languages for the same task, that is evidence of execution-tax.

**What a positive result looks like:** The high-token-tax language conditions require more total tokens, more agent steps, or higher retry rates to successfully complete the same tasks. The overhead is not fully explained by the tokenization difference alone (i.e., it is not just the input being longer — the execution path itself is longer or less reliable).

**What a null result means:** If execution workloads are equivalent across language conditions after controlling for input length, execution-tax in this form does not exist in this architecture. That is a meaningful finding — it would refine the hypothesis rather than invalidate NiceM entirely.

### Methodology dependencies

Before running this experiment, NiceM needs to resolve nine methodology questions. These are tracked in `docs/open-questions.md` under **Methodology questions before validation** (M1–M9). The most critical are:

- **Success criterion (M1, M2, M3):** How is task completion defined and scored, and can that scoring method be validated for cross-language reliability? An evaluator biased toward English will produce biased success classifications, making any execution-tax signal untrustworthy. (See `docs/sources/agent-evals/agent-as-a-judge.md`.)
- **Decomposition method (M4):** How does NiceM separate token-tax (longer input) from execution-tax (longer path) in the measurement? Without a decomposition method, the two effects cannot be distinguished.
- **Instrumentation choice (M9):** Which observability platform captures per-step token and timing data at the granularity NiceM needs? Candidates: Langfuse, Arize Phoenix, NeMo Agent Toolkit. (See `docs/sources/agent-evals/`.)
- **Falsification condition (M7):** What result would falsify the execution-tax hypothesis? This must be specified before the experiment runs. (See agent-evals sources and `docs/sources/agent-evals/tau-bench.md` for benchmark design reference.)

---

## 10. Open risks

### Empirical risks

**Execution-tax may be small or negligible in some architectures.** If retrieval is language-agnostic (e.g., vector similarity search on multilingual embeddings), the retrieval step may not amplify token-tax. The execution overhead may exist only in certain pipeline designs.

**Translation may remove some effects.** If users translate their queries into English before submission, or if the AI system internally translates, the token-tax and any downstream execution effects may be reduced. Whether translation is a valid solution or introduces its own overhead is an open question.

**Model choice may dominate language effects.** Newer models with better multilingual training may reduce or eliminate the execution overhead across languages. If so, execution-tax is a function of current model limitations, not a structural property of agentic AI.

**Evaluation quality may be hard.** Defining and measuring task success consistently across languages is a non-trivial methodological challenge. The success criterion must not itself be biased toward high-resource languages. Automated evaluation (Agent-as-a-Judge) introduces its own biases and costs.

### Economic risks

**Token cost may decline over time.** If inference becomes significantly cheaper, the economic impact of execution-tax declines even if the overhead persists. NiceM's relevance depends partly on token cost remaining meaningful.

**Context window growth may absorb some effects.** If context windows expand to the point where token-tax no longer causes context exhaustion (the effect Ahia et al. document), one of the performance mechanisms of token-tax may weaken.

### Competitive and strategic risks

**Competitors may frame this as agent evaluation or observability.** Existing observability and evaluation platforms could add language-disaggregated metrics without building a full execution-tax measurement methodology. NiceM needs a clear positioning moat.

**The problem may be solved at the tokenizer layer.** If model providers adopt morphologically aware tokenizers that achieve parity across languages, token-tax — and any downstream execution-tax — may be significantly reduced. (Lundin et al. propose this but note it is not yet demonstrated.)

### Source and credibility risks

**Public claims require source verification.** Several claims currently in NiceM's working materials are conversation-derived and have not been traced to primary sources. Before any public use of these claims, verification is required. See `docs/sources/notes/source-verification-checklist.md` for the full list.

---

## Thesis summary

| Element | Status |
|---|---|
| Token-tax exists and creates cost, quality, and latency inequality | Established — Petrov, Ahia, Lundin |
| Execution-tax hypothesis | NiceM hypothesis — not yet validated |
| AI factories / tokens-per-watt as industry context | Supported by NVIDIA sources — links TODO |
| Cost per successful completion as primary metric | NiceM concept — logical extension of existing metrics |
| Successful intent per watt | NiceM concept — extension of NVIDIA's tokens-per-watt |
| Validation methodology is feasible | Plausible — instrumentation exists; experiment not yet run |
| Product direction (AI Execution Intelligence) | Directional — pre-validation |

---

*Next version (v0.2) should incorporate: resolution of methodology questions M1–M9 (see `docs/open-questions.md`), first validation experiment design, refined audience definition, and competitive landscape analysis.*
