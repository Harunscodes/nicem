# NiceM Mathematical Foundations Roadmap v0.1

**Status:** Theory roadmap — preliminary definitions; not yet formalized
**Role:** Establishes the mathematical framing within which NiceM's token-tax and execution-tax concepts are coherent quantities. Defines what is being measured before measuring it.
**Version:** mf-roadmap-v0.1.0
**Depends on:** `docs/nicem-thesis.md`, `docs/token-tax-vs-execution-tax.md`
**Does not replace:** The v0.1 benchmark and its empirical measurement program
**Last updated:** 2026-06-14

---

## 1. Purpose

NiceM makes a causal claim: that language, tokenization, agent architecture, and retrieval design change the total burden required to complete the same human intent. Making this claim precisely requires more than an experimental design — it requires a theoretical frame that says what token-tax and execution-tax *are*, why they are coherent quantities, and why they should be expected to exist.

The mathematical foundations layer serves three purposes:

1. **Definition.** The benchmark measures specific quantities — token counts, ratios, success rates, cost per completion. The theory defines what those quantities approximate. Without a theoretical frame, the benchmark produces numbers without a model that explains what the numbers mean.

2. **Scope.** The theory specifies under what conditions token-tax and execution-tax should be observable, and under what conditions they might be zero or irrelevant. This limits overclaiming.

3. **Direction.** The theory identifies which directions future NiceM work should go — what to formalize, what to measure, what to control for — and flags where the theory is currently provisional.

What the mathematical foundations layer does **not** do:

- It does not prove that execution-tax exists empirically. That is what the benchmark does.
- It does not replace measurement with derivation. The theory provides conditional results; the empirical program tests whether the conditions hold and what the magnitudes are.
- It does not assume that Turkish, Dutch, or any specific language carries execution-tax. These are empirical questions.

The benchmark measures. The mathematical frame defines what is being measured. The theory should explain why token-tax and execution-tax are coherent quantities. The theory should not replace empirical testing.

---

## 2. Core thesis

The theoretical NiceM thesis, stated informally and then more precisely:

**Informal statement:**

Human intent is transmitted and executed through a tokenized, compute-constrained AI channel. The channel has finite capacity. Representations that require more tokens leave less capacity for other intents. Representations that are harder to process — noisier, more ambiguous, more likely to cause retrieval failure or truncation or retry — impose additional burden beyond the token cost of the representation itself.

**Formal sketch (v0.1 preliminary):**

Let $I$ be a human intent drawn from an intent space $\mathcal{I}$.

Let $L$ be a language/tokenizer pair that maps $I$ to a token sequence $T_L(I)$ with length $|T_L(I)|$.

Let $\mathcal{A}$ be an agent design (retrieval strategy, prompting, tool use) that processes $T_L(I)$ and produces an outcome.

Let $S_L(I, \mathcal{A}) \in \{0, 1\}$ be the success indicator: 1 if the outcome satisfies the intent, 0 otherwise (with UNCERTAIN tracked separately).

Let $C_L(I, \mathcal{A})$ be the total resource cost of one attempt: tokens consumed, API calls, retrieval calls, latency, wall-clock time, or financial cost, depending on the metric.

**Token-tax** for language $L$ relative to baseline language $L_0$ is:

$$\text{TokenTax}(L, I) = \frac{|T_L(I)|}{|T_{L_0}(I)|} - 1$$

**Execution-tax** for language $L$ relative to $L_0$ is:

$$\text{ExecutionTax}(L, I, \mathcal{A}) = \frac{C_L(I, \mathcal{A}) / P(S_L)}{C_{L_0}(I, \mathcal{A}) / P(S_{L_0})} - 1$$

where $P(S_L) = \mathbb{E}[S_L(I, \mathcal{A})]$ is the expected success rate.

This ratio compares cost per successful completion across languages, after normalizing for success rate. If execution-tax is zero, the two languages are equally efficient per successful outcome despite possibly different token counts. If it is positive, language $L$ requires more total resource per successful completion.

**Intent-capacity loss** is the broader umbrella:

$$\text{IntentCapacityLoss}(L) = 1 - \frac{\text{ReliableIntentRate}(L)}{\text{ReliableIntentRate}(L_0)}$$

where ReliableIntentRate is the maximum rate of successfully completed intents per unit resource (tokens, time, cost, or energy). This is the long-run infrastructure metric.

---

## 3. Shannon information theory

Shannon's framework for communication channels provides the most natural framing for NiceM's core claim.

**The communication channel analogy:**

| Shannon component | NiceM component |
|---|---|
| Message source | Human intent $I$ |
| Encoder | Language + tokenizer: $I \mapsto T_L(I)$ |
| Channel | LLM / agent stack: processes token sequences |
| Decoder | Output generation, retrieval, tool execution |
| Recovered message | Executed outcome: intent fulfilled or not |
| Noise | Ambiguity, retrieval mismatch, truncation, uncertainty, tool failure, model error |
| Redundancy | Retries, additional retrieval calls, longer prompts, clarifications, human review |
| Channel capacity | Maximum reliable information rate per unit resource |

**Shannon capacity.** For a memoryless channel with input alphabet $\mathcal{X}$, output alphabet $\mathcal{Y}$, and transition probabilities $p(y|x)$, Shannon capacity is:

$$C = \max_{p(x)} I(X; Y)$$

where $I(X; Y)$ is the mutual information between input and output. Capacity bounds the rate at which messages can be reliably transmitted. Exceeding it means irreducible errors.

**NiceM intent capacity.** Analogously, NiceM defines:

$$C_{\text{intent}} = \text{maximum reliable successful-intent rate per unit resource}$$

Token-tax reduces this capacity even in a noiseless channel: if each intent consumes more tokens, fewer intents fit within the same resource budget. Execution-tax is the additional reduction caused when the channel is noisy — when ambiguity, truncation, retrieval failure, or model error force additional recovery steps.

**Key analogy:**
Shannon capacity = maximum reliable information rate.
NiceM intent capacity = maximum reliable successful-intent rate per resource.

The analogy is not exact: human intent is a richer semantic object than a discrete symbol, success is harder to define than bit-error rate, and the "channel" (an LLM agent stack) is vastly more complex than a memoryless channel. But the framing disciplines the thinking: it forces the question "what is the maximum rate at which this system can reliably execute intent, and what reduces it?"

---

## 4. Noiseless vs noisy NiceM channels

**Noiseless NiceM channel:** A channel in which every tokenized intent is correctly interpreted and executed on the first attempt. No retrieval errors, no truncation, no ambiguity, no retries, no model failures. Token-tax can still reduce capacity: if language $L$ requires more tokens per intent than baseline $L_0$, then fewer intents fit in a fixed context window, and more tokens are consumed per successful completion.

Under a noiseless channel, execution-tax from noise sources is zero by definition. Residual cost difference is purely a function of token counts.

**Noisy NiceM channel:** A channel in which execution errors occur — retrieval returns the wrong chunks, the context window is exceeded and key information is truncated, the model generates a hallucination, a tool call fails, or the intent is ambiguous and misinterpreted. Recovery from these errors requires redundancy: additional retrieval calls, retries, longer prompts with more context, human review.

When the noisy-channel error rate is language-dependent — for example, if a higher token count increases the probability of context truncation, or if morphologically complex text is more likely to be misinterpreted — then residual execution-tax (beyond what token counts alone predict) can appear.

**Relationship between the two:**

In the narrow NiceM sense, residual execution-tax is mainly a noisy-channel phenomenon: it is the excess burden that remains after controlling for the token-tax baseline. In the broad capacity sense, token-tax can reduce intent throughput even without noise, because resources are finite. Both matter. NiceM v0.1 measures both, in sequence: Stage 1a establishes the token-tax (noiseless) baseline; Stage 2/3 test whether residual execution burden appears after controlling for it.

---

## 5. Kolmogorov complexity

Kolmogorov complexity provides a second, complementary framing grounded in description length rather than transmission rate.

**Informal definitions:**

The Kolmogorov complexity $K(x)$ of a string $x$ is the length of the shortest program that produces $x$ on a universal Turing machine. It measures the irreducible information content of $x$ — the minimum description length.

**NiceM mappings:**

| Kolmogorov concept | NiceM concept |
|---|---|
| Latent object $x$ | Human intent $I$ — the semantic content to be communicated and executed |
| Description of $x$ | Language rendering: the natural-language expression of $I$ in language $L$ |
| Machine description | Tokenized query $T_L(I)$: the form in which the agent actually processes the intent |
| Description length $|d(x)|$ | Token count $|T_L(I)|$ |
| Excess description length | Token-tax: $|T_L(I)| - |T_{L_0}(I)|$ |
| Program that produces $x$ | Agent trace: the sequence of retrieval, reasoning, tool, and generation steps |
| Program length $|p(x)|$ | Trace length: total token and step count to reach a successful outcome |
| Excess trace length | Execution-tax: the additional trace burden for language $L$ relative to $L_0$ |

**Token-tax as excess description length:**

If intent $I$ has a minimal description length $K(I)$, and language $L$ renders it as a token sequence of length $|T_L(I)|$, then token-tax is the amount by which the rendered description exceeds the minimum:

$$\text{TokenTax}_K(L, I) = |T_L(I)| - K(I)$$

Different tokenizers applied to different languages produce descriptions of different lengths for the same semantic content. The token-tax is the excess over the minimum needed to express the intent.

**Execution-tax as excess trace complexity:**

Let $p_L(I, \mathcal{A})$ be the agent trace (program) that processes intent $I$ under language $L$ and agent design $\mathcal{A}$ and produces a successful outcome. Its length $|p_L|$ captures the total computational burden: token calls, retrieval steps, retries, human review. Execution-tax is then the excess:

$$\text{ExecutionTax}_K(L, I, \mathcal{A}) = |p_L(I, \mathcal{A})| - |p_{L_0}(I, \mathcal{A})|$$

when both traces produce a successful outcome. When one trace fails, the comparison requires conditioning on success.

**Computability caveat:**

True Kolmogorov complexity is uncomputable — no algorithm can compute $K(x)$ for arbitrary $x$. NiceM therefore uses computable proxies:

- Token count as a proxy for description length
- Compressed text length (e.g., gzip ratio) as an alternative description-length proxy
- Trace length (total tokens + steps) as a proxy for execution-program length
- Model calls, retrieval calls, retries, and cost per success as proxy trace-length components

These proxies are empirically measurable. The Kolmogorov framing provides the theoretical motivation for why these proxies are meaningful approximations.

---

## 6. Chaitin and irreducibility

Gregory Chaitin's work on algorithmic information theory establishes that some complexity is irreducible: there is no description shorter than the object itself, and no program that computes the object faster than running it.

**Application to NiceM:**

Not all long prompts are waste. Not all redundancy is bad. Some execution cost is necessary:

- A query that asks about a conditional policy (e.g., "what warranty applies if my replacement device is refurbished?") requires more tokens than a simple lookup query. This is irreducible: the intent is more complex, and the description must be at least as long as the complexity of the intent.
- A retrieval step is not execution overhead if the intent genuinely requires external knowledge that the model cannot reliably recall.
- A validation step is not wasted computation if the task requires checking a fact-dependent condition.
- Some retries are necessary: they are the cost of operating in a noisy channel at acceptable success rates.

**NiceM's distinction:**

NiceM distinguishes three components of execution burden:

1. **Irreducible intent complexity** — the minimum cost to express and execute intent $I$ correctly, regardless of language or agent design. This is a property of the task, not of the language.

2. **Token-tax overhead** — the excess representation cost caused by language and tokenizer choice. Avoidable in principle by using a more efficient representation.

3. **Residual execution-tax** — the excess execution burden (beyond token-tax) caused by agent design, retrieval strategy, or language-induced error patterns. Avoidable in principle by better agent design.

NiceM does not aim to remove necessary complexity; it aims to identify avoidable execution overhead.

This distinction matters for reporting: if Turkish queries require more tokens due to agglutinative morphology, that is token-tax — avoidable by a better tokenizer. If the same Turkish queries also require more retrieval calls because morphological variation increases retrieval mismatch, that is residual execution-tax — avoidable by a better retrieval design. If a query about a complex multi-condition policy requires more tokens, that may be irreducible intent complexity — not avoidable without changing the task.

---

## 7. Rate–distortion theory

Shannon's rate–distortion theory addresses the fundamental tradeoff between compression efficiency (rate) and information loss (distortion).

**Formal statement:**

For a source $X$ with distortion measure $d(x, \hat{x})$, the rate–distortion function $R(D)$ gives the minimum number of bits per symbol needed to represent $X$ with average distortion at most $D$:

$$R(D) = \min_{p(\hat{x}|x): \mathbb{E}[d(X,\hat{X})] \leq D} I(X; \hat{X})$$

The rate–distortion function is monotonically non-increasing: achieving lower distortion requires higher rate (more bits/tokens). Compressing below $R(D)$ for a given $D$ is impossible.

**NiceM application:**

In NiceM terms:
- **Rate** = representation budget: tokens used in the query and context
- **Distortion** = loss of required intent conditions: the degree to which the tokenized/rendered query fails to convey all conditions necessary to produce the correct answer

For a benchmark intent with multiple required conditions (e.g., "what warranty applies if my replacement is refurbished and I am within the original warranty period?"), there is a minimum representation rate below which at least one required condition will be lost.

**Rate–distortion constraints on token-tax measurement:**

Token-tax should be measured at **equivalent intent-preservation quality**. Comparing a full-condition Turkish query to a compressed English query that drops one condition is not a valid comparison — the English query has higher distortion. The NiceM benchmark enforces this through the query rendering quality gates (§9b of quality-gates.md): all conditions must be preserved in all three language renderings.

**Rate–distortion constraints on query variants:**

Query variants (V2 concise natural, V3 context-rich, V4 indirect support-style, V5 alternate phrasing) can be understood in rate–distortion terms. A V2 concise variant uses fewer tokens (lower rate). Whether this increases distortion — whether a condition is lost — determines whether the compressed variant is valid. The query variant equivalence requirements (query-variant-plan.md §5) are the operational form of a distortion constraint: no variant may drop or alter a required condition.

**Over-compression failure mode:**

If a variant compresses below the rate–distortion limit for its intent, it will produce more failures even if the agent and KB are identical. This is not execution-tax — it is a distortion failure in the query encoding. Stage 2 analysis must distinguish: a higher failure rate for concise Turkish variants may reflect Turkish over-compression at the same conditions that English encodes comfortably, OR it may reflect that the variant omitted a condition. These must be separated at evaluation time.

---

## 8. Error-correcting codes and redundancy

Shannon's source-channel coding theorem shows that with the right redundancy in the encoding, messages can be transmitted reliably over a noisy channel at any rate below channel capacity. Error-correcting codes add structured redundancy so that errors can be detected and corrected at the decoder.

**NiceM redundancy analogy:**

Shannon-style redundancy protects messages from noise. NiceM-style redundancy protects intent execution from ambiguity and failure. The correspondence:

| Error-correcting code concept | NiceM execution concept |
|---|---|
| Codeword with redundant bits | Query with explicit conditions, context, and disambiguation |
| Redundancy rate | Extra tokens added to ensure intent survives noisy processing |
| Error detection | Validation step: checking whether the model's answer is consistent with required facts |
| Error correction | Retry: resubmitting with a rephrased or expanded query |
| Parity check | Retrieval: cross-checking against the KB to confirm the generated answer |
| Decoder | Human review of UNCERTAIN outputs |
| Uncorrectable error | FAIL outcome: the intent could not be successfully executed |

Retrieval, validation, retries, clarifications, and human review are execution redundancy — the NiceM analog of error-correcting code redundancy.

**Formal sketch of residual execution-tax via redundancy:**

Define $R_L(\varepsilon)$ as the minimum recovery/redundancy burden needed for language $L$ to reach success probability at least $1 - \varepsilon$:

$$R_L(\varepsilon) = \min \{ \text{redundancy burden} : P(\text{success under language } L) \geq 1 - \varepsilon \}$$

Then residual execution-tax for language $L$ relative to baseline $L_0$ at success threshold $1 - \varepsilon$, after accounting for token-tax, is:

$$\text{ResidualExecutionTax}(L, \varepsilon) = R_L(\varepsilon) - R_{L_0}(\varepsilon)$$

where "accounting for token-tax" means the comparison is made after normalizing for the known token-count difference (so that only the additional redundancy required — beyond what token counts alone would predict — is attributed to execution-tax).

If $R_L(\varepsilon) = R_{L_0}(\varepsilon)$, then residual execution-tax is zero: both languages require the same execution redundancy to achieve the same success rate, even if their token counts differ.

This is the key falsification structure. NiceM's Stage 2/3 test whether $R_L(\varepsilon)$ for Turkish and Dutch differs from $R_{L_0}(\varepsilon)$ for English in a controlled benchmark.

---

## 9. Transformer and computational complexity

Modern LLM agent stacks are built on transformer architectures. While exact computational complexity analysis of production systems is not the goal of v0.1, the general properties of transformers provide a mechanical link between token counts and execution burden.

**Token sequence length and resource use:**

Transformers process sequences of tokens. The key relevant properties for NiceM are:

- **Context window.** Transformers have a finite context window (e.g., 128K tokens). If a language requires more tokens to express the same content, it consumes more of the available context window. In a system near the context limit, higher token counts can cause truncation of earlier context, loss of retrieved chunks, or inability to process the full agent trace.

- **Attention cost.** Standard attention has computational complexity that scales with the square of the sequence length in the naive case, and is improved but still length-sensitive in optimized implementations. Longer sequences increase per-step computation.

- **Generation length.** If the model generates longer outputs in language $L$ than in $L_0$ for the same intent, the output token count increases, raising latency and cost proportionally.

- **KV cache and memory pressure.** Longer sequences require more KV cache memory. Under memory pressure, systems may evict or compress earlier context, potentially discarding retrieved facts needed for correct completion.

**Mechanism connecting token-tax to execution burden:**

The chain is: higher token count → more context consumed → increased probability of truncation or context pressure → higher probability of retrieval failure (key chunks evicted) or generation error (key context missing) → higher probability of needing a retry or human review → higher total execution burden.

This is not an algebraic derivation: the magnitude of each step depends on the specific system, the specific content, and the specific context-window occupancy. But it establishes a plausible causal mechanism through which token-tax at the representation layer can propagate into execution burden.

Avoid overclaiming exact complexity for all modern architectures; keep it general: the mechanism exists and is directionally sound, but the magnitude is an empirical question.

---

## 10. Decision theory and cost per successful completion

**Definition:**

$$\text{CostPerSuccess}(L) = \frac{\mathbb{E}[C_L]}{P(S_L)}$$

where $C_L$ is the cost of one run in language $L$ and $S_L \in \{0, 1\}$ is the success indicator. This is the expected cost per unit of useful output — the business-facing metric for AI execution efficiency.

**Why this metric is the right one:**

A cheap failed run is not efficient. A system that achieves a very low per-run cost by failing on 80% of intents is not better than a system that costs twice as much per run but succeeds 95% of the time. Cost per successful completion captures this: both the cost and the success rate enter the denominator.

The Shannon analogy: channel capacity is not bits transmitted, but reliable bits transmitted. Cost per successful completion is not cost per run, but cost per correctly completed intent.

**Decomposition:**

Suppose language $L$ has per-run cost $\mathbb{E}[C_L] = \alpha \cdot \mathbb{E}[C_{L_0}]$ and success probability $P(S_L) = \beta \cdot P(S_{L_0})$, for $\alpha, \beta > 0$. Then:

$$\frac{\text{CPS}(L)}{\text{CPS}(L_0)} = \frac{\alpha}{\beta}$$

If $\alpha = \beta$ (cost and success rate both increase proportionally), CPS is unchanged. If $\alpha > \beta$ (cost increases more than success rate), CPS increases — language $L$ is less efficient. If $\beta < 1$ (success rate decreases while cost stays the same or increases), CPS increases.

**Compounding:**

The compounding case is the one NiceM is most concerned with: both $\alpha > 1$ (higher per-run cost from token-tax) and $\beta < 1$ (lower success rate from execution overhead). In this case CPS grows as $\alpha / \beta$, which can be substantially larger than either factor alone. A 30% cost increase ($\alpha = 1.3$) combined with a 20% success rate decrease ($\beta = 0.8$) produces a CPS ratio of $1.3 / 0.8 = 1.625$ — a 62.5% increase in effective cost.

Whether this compounding occurs is an empirical question that Stage 2/3 will test.

---

## 11. Control theory and agent loops

Modern AI agents are feedback systems. A retrieval-augmented agent retrieves evidence, evaluates the evidence against the query, generates an answer, and may retry if the answer is unsatisfactory. This is a feedback control loop.

**Control theory framing:**

Let the "error signal" be the gap between the current agent state and a successful completion. The agent acts to reduce this error: retrieving more relevant documents, rephrasing the query, using a different tool. The number of steps to convergence (to a successful outcome) is the execution trace length.

Key properties:
- If the error signal is larger for language $L$ than for $L_0$ at equivalent stages, more control steps may be needed to converge.
- If the feedback signal itself is noisier in language $L$ (e.g., the model is less reliable at assessing its own output quality in Turkish), convergence may require more iterations.
- If the agent has a hard step limit (e.g., maximum 5 retrieval calls), a system that requires more steps may fail to converge within the budget — producing a failure where the baseline language would have succeeded.

**Execution-tax as convergence overhead:**

Execution-tax, in control terms, is the excess number of control steps required to converge to a successful outcome for language $L$ relative to $L_0$, at the same success probability threshold.

$$\text{ControlOverhead}(L) = \mathbb{E}[\text{steps to success} | S_L = 1] - \mathbb{E}[\text{steps to success} | S_{L_0} = 1]$$

If this is positive, the agent requires more iterations in language $L$ even when it eventually succeeds.

Future NiceM work can formalize this framing using stochastic control or Markov decision process models of agent execution, where the state space includes retrieval quality, generation confidence, and success probability, and the control policy determines when to retry, when to escalate, and when to return an answer.

---

## 12. Queueing and infrastructure

At the infrastructure level, AI agent execution is a service: requests arrive, are processed, and produce outcomes. Queueing theory characterizes the relationship between service time, arrival rate, utilization, and latency.

**Little's Law and utilization:**

For a queueing system with arrival rate $\lambda$ and mean service time $\bar{s}$, utilization is $\rho = \lambda \bar{s}$. As utilization approaches 1, mean queue length grows without bound (for M/M/1 queues). Slightly elevated service times can dramatically increase effective latency under load.

**NiceM implication:**

Per-run execution overhead — whether from longer token sequences, more retrieval calls, more retries, or higher failure rates requiring resubmission — increases mean service time $\bar{s}$. Under load, this:

1. Increases per-intent latency at the system level
2. Increases GPU/compute utilization for the same throughput
3. Reduces the maximum reliable intent throughput at fixed infrastructure
4. Increases infrastructure cost per delivered successful completion

**Tokens-per-watt → successful-intents-per-watt:**

Jensen Huang's tokens-per-watt framing (the industry efficiency metric for AI infrastructure) implicitly assumes that tokens translate directly to useful output. NiceM's hypothesis is that this assumption breaks down when execution overhead — token-tax plus residual execution-tax — varies across workloads.

The long-run NiceM infrastructure metric is:

$$\text{SuccessfulIntentsPerWatt} = \frac{\text{ReliableIntentRate}}{\text{Power}} = \frac{\lambda \cdot P(S)}{\text{Power}}$$

If execution-tax is positive for language $L$, the same infrastructure delivers fewer successful intents per watt when processing language-$L$ workloads. The gap between tokens-per-watt and successful-intents-per-watt is the infrastructure-level manifestation of execution-tax.

Small per-intent overhead can create larger system-level cost. A 30% increase in execution burden does not simply cost 30% more at scale — it also shifts the queueing system to higher utilization, increasing latency nonlinearly for other users and workloads sharing the infrastructure.

---

## 13. Proposed formal quantities

The following definitions are preliminary v0.1 theory. They are intended to be precise enough to guide empirical measurement and to be refined as the theory matures.

**Intent:** A human communicative act that specifies an information need or action to be taken, together with all conditions necessary to correctly respond. Formally: $I \in \mathcal{I}$, where $\mathcal{I}$ is the intent space for a given task family. In the NiceM v0.1 benchmark, intents are operationalized as the 36 intent specifications in `intent-set.md`, with expected outcomes in `expected-fact-mapping.md`.

**Language rendering:** A function $r_L : \mathcal{I} \to \mathcal{Q}_L$ that maps an intent to a natural-language expression in language $L$, preserving all required conditions. The rendering must satisfy: for any evaluator $E$ with correct knowledge, $E(r_L(I))$ recovers the correct answer. (This is the rate–distortion zero-distortion constraint for the rendering.)

**Tokenizer:** A function $\tau : \mathcal{Q}_L \to \mathcal{V}^*$ that maps a natural-language string to a sequence of tokens from vocabulary $\mathcal{V}$. Token count $|T_L(I)| = |\tau(r_L(I))|$.

**Intent-execution channel:** The triple $(r_L, \tau, \mathcal{A})$ where $r_L$ is the rendering, $\tau$ is the tokenizer, and $\mathcal{A}$ is the agent design. Together they map an intent $I$ to an outcome $O$ via: $I \xrightarrow{r_L} q \xrightarrow{\tau} T \xrightarrow{\mathcal{A}} O$.

**Execution burden:** $B_L(I, \mathcal{A}) = C_L(I, \mathcal{A})$, the total resource cost of one execution attempt (tokens, API calls, latency, or financial cost, depending on context).

**Token-tax** (per-intent, relative): $\text{TT}(L, I) = |T_L(I)| / |T_{L_0}(I)| - 1$.

**Residual execution-tax** (per-intent, after token-tax baseline): The portion of $\text{ExecutionTax}(L, I, \mathcal{A})$ that remains after subtracting the component attributable to token-tax alone. Measured by the residual-overhead method in `baseline-token-tax-calculation-v0.1.md` §9.

**Intent capacity** (for channel $(r_L, \tau, \mathcal{A})$): The maximum rate of successfully completed intents per unit resource, over the distribution of intents $\mathcal{I}$.

**Reliable intent rate:** The rate of intent completions that satisfy the success gate (PASS per evaluation-method), as distinct from total completions including FAIL and UNCERTAIN.

**Cost per successful completion (CPS):** $\text{CPS}(L, \mathcal{A}) = \mathbb{E}[C_L] / P(S_L)$.

**Successful intents per watt:** $\text{SIPW} = (\lambda \cdot P(S)) / W$ where $\lambda$ is the intent arrival rate, $P(S)$ is the success probability, and $W$ is the infrastructure power draw. This is the long-run NiceM infrastructure efficiency metric.

All definitions above are marked **v0.1 theory** — preliminary and subject to revision as the empirical program produces results and the theory is refined.

---

## 14. What can be proven mathematically

The following are conditional results that follow from the definitions above, without empirical measurement. They hold whenever the stated conditions are met.

**Theorem 14.1 (Token-tax and capacity):**
If the intent-execution channel has a finite resource budget $B$, and $|T_L(I)| > |T_{L_0}(I)|$ for intent $I$, then language $L$ can process at most $\lfloor B / |T_L(I)| \rfloor$ instances of intent $I$ per budget unit, while $L_0$ can process $\lfloor B / |T_{L_0}(I)| \rfloor$ instances. Since $|T_L| > |T_{L_0}|$, language $L$ achieves strictly lower intent throughput per budget unit for this intent, even if the success rate is identical.

*Interpretation:* If tokenized burden increases under fixed finite capacity, reliable intent throughput cannot increase and may decrease. No empirical measurement is needed to establish this; it follows from the definition of token counts and finite budgets.

**Theorem 14.2 (CPS monotonicity in success rate):**
If $P(S_L) < P(S_{L_0})$ and $\mathbb{E}[C_L] \geq \mathbb{E}[C_{L_0}]$, then $\text{CPS}(L) > \text{CPS}(L_0)$.

*Interpretation:* If success probability decreases while per-run cost remains the same or increases, cost per successful completion increases. The magnitude of the increase depends on empirical values of $P(S)$ and $\mathbb{E}[C]$.

**Theorem 14.3 (Redundancy definition of positive execution-tax):**
If $R_L(\varepsilon) > R_{L_0}(\varepsilon)$ for some $\varepsilon \in (0, 1)$ — that is, if language $L$ requires strictly more recovery redundancy to reach success probability $1 - \varepsilon$ — then residual execution-tax is positive by definition of $R_L(\varepsilon)$.

*Interpretation:* The existence of positive residual execution-tax is guaranteed if the conditions hold. Whether the conditions hold in a specific AI system for specific languages is an empirical question.

**Theorem 14.4 (Context window truncation):**
If a fixed context window of size $W$ tokens is used, and $|T_L(I)| + |K_L| > W$ while $|T_{L_0}(I)| + |K_{L_0}| \leq W$ — where $K_L$ is the token count of retrieved context in language $L$ — then language $L$ cannot be processed without truncation in this window, while $L_0$ can. Reliable execution may require either a larger budget or a recovery mechanism for language $L$ that is not needed for $L_0$.

*Interpretation:* If a fixed context window is exceeded by one encoding but not another, reliable execution may require truncation, recovery, or a larger budget. This is a necessary consequence of token counts and finite window size.

---

## 15. What must be measured empirically

The mathematical theorems in §14 are conditional: they hold when stated conditions are met. Determining whether the conditions hold, and measuring the magnitudes, requires empirical work. The following quantities cannot be derived from the theory alone:

- **Actual token ratios.** The theory says token-tax affects throughput; the benchmark measures how large the token ratio is for Turkish and Dutch vs English, on the specific synthetic KB and query set.
- **Actual retrieval behavior.** Whether token-tax propagates into retrieval failure depends on how the retrieval system handles morphological variation, context pressure, and chunk boundaries. This is system-specific and must be measured.
- **Actual model success rate.** Whether the LLM correctly extracts required facts and applies conditions correctly depends on the model's multilingual competence, its handling of agglutinative morphology, and its calibration on the specific task family.
- **Actual retry behavior.** Whether the agent retries, how often, and whether retries succeed in language $L$ vs $L_0$ is a measurement from the instrumented run, not a derivation.
- **Actual latency and cost.** Per-run costs depend on provider pricing, model tier, input/output token counts, and retrieval infrastructure. These vary by system and time.
- **Whether residual execution-tax appears after token-tax baseline.** This is the core NiceM empirical question: after controlling for the token-count difference (Stage 1a baseline), does language $L$ still require more execution burden to achieve the same success rate? Stages 2 and 3 test this.
- **Whether effects are language-specific, task-specific, model-specific, or agent-design-specific.** The same language may show execution-tax under one model and not under another. The same model may show execution-tax on one task family and not another. Separating these requires controlled variation, which is the purpose of the A/B agent design comparison.

---

## 16. Relationship to the v0.1 benchmark

The mathematical foundations layer and the benchmark are complementary, not competing.

**Stage 1a** (complete as of 2026-06-13) measures the token-tax baseline: the ratio $|T_L(I)| / |T_{L_0}(I)|$ for all 36 intents and 39 KB chunks across EN/NL/TR. This corresponds to the noiseless-channel capacity analysis (§4) and the Kolmogorov description-length proxy (§5). It produces the token-tax component of the execution burden decomposition.

**Stage 2/3** (planned) will measure whether the token-tax baseline propagates into actual execution behavior: whether retrieval call counts, retry rates, success probabilities, and cost per successful completion differ across languages after controlling for the token-count baseline. This corresponds to the noisy-channel redundancy analysis (§8), the CPS decomposition (§10), and the control-loop convergence framing (§11).

**Query variants** (planned, post-Stage 1a) can be used to test rate–distortion predictions (§7): do compressed-phrasing variants (V2) produce lower success rates in Turkish than in English at equivalent compression, suggesting that Turkish over-compresses below the rate–distortion limit for its intent?

**Important scope statement:** The benchmark does not prove universal execution-tax; it tests the theory in a controlled, synthetic, single-task-family, two-agent-design setting. Results are specific to the GPT-4.1 model family, the NiceHome synthetic Product FAQ / Policy QA task family, language-matched retrieval, and the 36-intent v0.1 benchmark. Generalizing requires additional conditions from the theory and additional empirical scope from future benchmark iterations.

---

## 17. Future theory documents

The following documents are planned for the `docs/theory/` directory. Each would develop one component of the mathematical foundations in more detail.

| Document | Content |
|---|---|
| `docs/theory/shannon-intent-channel-model-v0.1.md` | Formal channel model: intent space, rendering function, tokenizer, agent as channel, noise model, capacity bounds. Shannon capacity analog for intent-execution systems. |
| `docs/theory/kolmogorov-description-trace-complexity-v0.1.md` | Description-length framing: intent as latent object, rendering as description, agent trace as program. Proxy measures for Kolmogorov complexity. Relationship between description length and token count. |
| `docs/theory/chaitin-irreducible-execution-complexity-v0.1.md` | Irreducibility analysis: separating necessary complexity from avoidable execution overhead. How to bound irreducible task complexity. When is redundancy necessary vs. avoidable? |
| `docs/theory/rate-distortion-intent-preservation-v0.1.md` | Rate–distortion analysis: intent-preservation distortion measure, rate–distortion function for query compression, implications for query variant design, over-compression failure mode. |
| `docs/theory/execution-tax-capacity-theorem-sketch-v0.1.md` | Formal sketch of conditional theorems: token-tax and capacity loss, redundancy definition of execution-tax, CPS decomposition, context-window truncation bound. Intended audience: technically rigorous; to be refined after Stage 2 empirical results. |
| `docs/theory/control-theory-agent-execution-v0.1.md` | Control-theoretic framing: agent as feedback controller, convergence steps as execution burden, excess convergence iterations as execution-tax. Markov decision process formulation. |
| `docs/theory/intent-capacity-infrastructure-model-v0.1.md` | Infrastructure-layer analysis: queueing model, Little's Law, utilization vs. latency, tokens-per-watt vs. successful-intents-per-watt, business case for reducing execution overhead. |

None of these documents should be created until Stage 2 empirical results are available. The theory documents should be informed by what the benchmark actually finds, not written in advance of any empirical constraint.

---

## 18. Open questions

The following questions are open at v0.1 theory stage. They require theoretical analysis, empirical grounding, or both.

**Definitional:**

- **TH1:** What is the best formal definition of intent? Intent should be language-neutral (the same intent expressed in Turkish and English should have the same theoretical object $I$), but how to formalize this invariance precisely — especially for intents with complex conditional structure — is non-trivial.

- **TH2:** Should execution-tax include token-tax or remain residual beyond token-tax? The current definition separates them (residual execution-tax after token-tax baseline). But in infrastructure terms (e.g., cost per successful completion), they compound. The right accounting may depend on the specific question being asked.

- **TH3:** What is the right unit for intent capacity: per token, per second, per euro, per watt? Different units are appropriate for different stakeholders (model researchers: per token; operators: per second or per euro; infrastructure designers: per watt).

**Measurement:**

- **TH4:** How should semantic distortion be measured? The rate–distortion framing (§7) requires a distortion measure. For NiceM intents, distortion can be operationalized as the fraction of required conditions that are lost in compression. But measuring this requires evaluating each compressed rendering against the expected fact mapping, which is expensive.

- **TH5:** Can a useful lower-bound theorem be stated without assuming too much about the model? A theorem of the form "for any model with context window $W$, if $|T_L(I)| > W/2$ then reliable execution requires retrieval" would be useful, but requires strong assumptions about model behavior.

- **TH6:** How should irreducible task complexity be estimated? If intent $I_1$ is inherently more complex than $I_2$ (e.g., a multi-condition policy query vs. a simple factual lookup), how do we separate the task-complexity component from the language-induced overhead component in the execution burden?

**Scope and calibration:**

- **TH7:** How should redundancy be separated into necessary vs. avoidable? The Chaitin framing (§6) distinguishes necessary from avoidable overhead, but operationalizing this distinction requires knowing what the minimum-redundancy execution of an intent looks like. This is empirically inaccessible for complex tasks.

- **TH8:** Which theory document should be formalized first? The most valuable next formalization is likely the rate–distortion analysis (§7), because it directly connects to query variant design and the over-compression failure mode that Stage 2 may surface. Alternatively, the execution-tax capacity theorem sketch (§14 extended) is highest leverage for the research claim.

---

*This document is the v0.1 mathematical foundations roadmap. It defines what NiceM is measuring and why the quantities are coherent, without replacing empirical measurement. All definitions are preliminary (v0.1 theory) and subject to revision. Execution-tax is a NiceM hypothesis; this document frames why it is a coherent hypothesis, not why it has been proven. Version: mf-roadmap-v0.1.0.*
