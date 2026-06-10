# NiceM Task Family Selection v0.1

**Status:** Internal working document. Not public. Not a dataset specification. Not experiment design.
**Version:** 0.1 — first task family analysis, addresses framework §12 (choose neutral task family)
**Scope:** Identifies and compares candidate task families for NiceM's first validation benchmark. Does not generate datasets, choose models, or finalize language selection.
**Relationship to framework:** This document follows the success rubric (`docs/methodology/success-rubric-v0.1.md`) and addresses the task-family prerequisite in `docs/methodology/nicem-methodology-framework-v0.1.md` §12. It assumes the success gate is defined and asks: what kind of task can that gate be applied to reliably, across languages, with deterministic or near-deterministic success criteria?

---

## 1. Purpose

Defining successful completion (the rubric) and selecting a task family are not the same decision, but they are tightly coupled. The rubric defines *what* counts as success; the task family determines *whether that definition can be applied reliably* in practice.

A rubric designed around deterministic success criteria is only useful if the tasks have deterministic answers. A rubric requiring language-independent expected outcomes only works if the tasks have outcomes that can be specified in language-neutral terms. A rubric sensitive to cross-language evaluator bias is only safe if the task family does not require evaluators to make open-ended quality judgments.

Task family selection therefore has three jobs:

1. **Enable the success gate.** The tasks must be checkable against pre-defined expected outcomes without depending on language-sensitive evaluation.
2. **Generate the execution trajectory.** The tasks must be complex enough to produce multi-step agent behavior — retrieval, reasoning, possible tool use — so there is a trajectory to measure.
3. **Support the token-tax/execution-tax decomposition.** The tasks must be structured so that differences in execution cost between language conditions can be attributed to overhead type (representation, retrieval, retry) rather than absorbed into a generic "costs more" finding.

A task family that is too simple (single-step, single-lookup) produces no trajectory to compare. A task family that is too complex or open-ended makes the success gate unreliable. The v0.1 task family must sit at the intersection of these constraints — complex enough to be interesting, simple enough to be measurable.

---

## 2. Selection criteria

A good v0.1 task family satisfies all of the following. These are requirements, not preferences.

| Criterion | Requirement | Rationale |
|---|---|---|
| **Neutral and synthetic** | No real employer, customer, product, or internal data | Independence rule (`CLAUDE.md`); avoids confidentiality and reproducibility problems |
| **Multilingual intent equivalence** | The same intent can be expressed in multiple languages without introducing ambiguity or cultural assumptions | Necessary for controlled cross-language comparison |
| **Deterministic or semi-deterministic success** | Expected outcomes can be specified as a set of facts or actions, not as a target string | Removes language-sensitive evaluation from the success gate; required for rubric reliability across languages |
| **Measurable agent trajectory** | The task requires at least retrieval + reasoning, producing a multi-step path with attributable token costs | Required to measure execution-tax components (retrieval overhead, retry overhead) not just total cost |
| **Enough complexity** | The task is not solvable in a single lookup; the agent must retrieve, reason, or check multiple conditions | Necessary to produce the trajectory variation execution-tax measurement requires |
| **Limited ambiguity** | The task has a definable correct answer; evaluators should not need to exercise open-ended judgment | Protects against evaluator bias entering the success gate |
| **Low safety risk** | The task does not require the agent to handle sensitive personal data, medical advice, or legally consequential actions | Reduces risk in a v0.1 proof-of-concept |
| **Repeatable across languages** | The task structure and knowledge base can be translated or constructed in multiple languages without producing genuinely different tasks | Required for the language conditions to be comparable |
| **Suitable for small scale** | A meaningful pilot is feasible with tens of task instances, not thousands | v0.1 is a validation benchmark, not a production dataset |

---

## 3. Candidate task families

### A. Product FAQ / policy QA

**Description:** A synthetic knowledge base representing a fictional product (e.g., a smart-home device, a subscription service, a software tool) with an associated FAQ, warranty policy, return policy, and troubleshooting guide. The agent answers user questions by retrieving from this knowledge base and reasoning over the retrieved content.

**Example tasks:** "Is a water-damaged device covered under the warranty if purchased six months ago?" / "Which subscription tier allows more than five connected devices?" / "What is the first troubleshooting step for a device that shows a red light on startup?"

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **High.** Expected answers are pre-defined facts from the knowledge base (e.g., "no — water damage is excluded under section 3.2"). Deterministic check against expected fact. |
| Multilingual equivalence | **High.** The knowledge base can be authored in a language-neutral canonical form and rendered into each test language. Intents translate cleanly. |
| Trajectory richness | **Medium-high.** Requires retrieval + conditional reasoning. Tasks with multiple conditions (purchase date AND damage type) require multi-step reasoning over retrieved content. |
| Risk of ambiguity | **Low.** Policy documents can be written to eliminate ambiguity in the canonical version. |
| Risk of evaluator bias | **Low.** Success is determined by whether the required fact from the knowledge base is present and correctly stated — not by stylistic quality. |
| Token-tax/execution-tax separation | **Good.** Retrieval call count, retrieval tokens, reasoning steps, and retry behavior are all attributable. If Language B requires more retrieval calls or more reasoning steps for the same policy question, that is a candidate execution-tax signal. |
| Suitability for v0.1 | **High.** |

---

### B. Travel planning assistant

**Description:** A synthetic travel scenario where the agent selects an itinerary or accommodation from a small synthetic catalogue satisfying stated constraints (budget, dates, preferences, travel time).

**Example tasks:** "Find a hotel in Amsterdam under €150 per night for three nights in July that accepts pets." / "Which of these three itineraries meets all constraints: budget under €500, arrival before 14:00, no layovers?"

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **Medium.** Constraint-satisfaction tasks with a synthetic catalogue are checkable (the correct option is defined in advance). But tasks involving tradeoffs or subjective preferences introduce ambiguity. |
| Multilingual equivalence | **Medium.** Travel constraints translate cleanly, but date formats, currency expressions, and location names introduce potential cross-language variability. Requires careful canonical-form design. |
| Trajectory richness | **Medium.** Retrieval + constraint evaluation. Richer if the catalogue is larger or constraints are multi-step. |
| Risk of ambiguity | **Medium.** "Preference" constraints are inherently ambiguous. Avoidable if all constraints are explicit and categorical. |
| Risk of evaluator bias | **Low-medium.** If success is "did the agent select the option that satisfies all constraints," it is deterministic. If success involves evaluating the quality of a travel recommendation, it is not. |
| Token-tax/execution-tax separation | **Medium.** Catalogue retrieval and constraint evaluation are attributable. Planning loops may introduce retry overhead in some language conditions. |
| Suitability for v0.1 | **Medium.** Viable if task design strictly avoids subjective preference constraints. Second-choice behind Product FAQ. |

---

### C. Public document QA

**Description:** Questions answered from a small public-domain document — e.g., a public policy document, a Wikipedia article, a synthetic regulatory text.

**Example tasks:** "According to this document, what is the penalty for late filing?" / "What are the three eligibility conditions listed in section 2?"

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **High.** Expected answers are text spans or facts from the document. Deterministic against the source. |
| Multilingual equivalence | **Medium.** Real public documents exist in specific languages; synthetic documents allow control. If the document itself is only available in one language, cross-language comparison requires translation of the document AND the questions — introducing confounds. |
| Trajectory richness | **Low-medium.** Primarily retrieval + extraction. Limited reasoning complexity for v0.1 unless tasks are multi-hop. |
| Risk of ambiguity | **Low** for factual span extraction; **medium** for interpretive questions. |
| Risk of evaluator bias | **Low** for span-level answers. |
| Token-tax/execution-tax separation | **Medium.** Mostly a retrieval + generation task; limited tool-use or retry trajectory. |
| Suitability for v0.1 | **Medium.** Simpler than Product FAQ; less trajectory richness. Useful as a supplementary task family or baseline. |

---

### D. Structured form completion

**Description:** The agent extracts structured information from a user request and fills a predefined JSON or structured form. Example: "Extract the booking intent from this message and return a JSON with destination, dates, and party size."

**Example tasks:** "User says: 'I want to visit Istanbul for 4 nights from July 10 with my partner.' Extract into: {destination, check_in, check_out, party_size}."

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **Very high.** Output is a structured object with checkable fields. Each field is independently verifiable. |
| Multilingual equivalence | **High.** The intent is expressed naturally in each language; the expected output is language-neutral (structured fields). This is one of the cleanest cross-language equivalence designs possible. |
| Trajectory richness | **Low.** Primarily a single extraction call — limited multi-step trajectory. Does not trigger retrieval, tool use, or planning. |
| Risk of ambiguity | **Low.** Ambiguity is a task-design choice and can be minimized. |
| Risk of evaluator bias | **Very low.** Field-level deterministic check. |
| Token-tax/execution-tax separation | **Limited.** There is little trajectory to decompose — mostly input token-tax (longer input in some languages) and output token-tax (structured output is language-neutral). This family would confirm token-tax but would not provide meaningful execution-tax signal. |
| Suitability for v0.1 | **Low for execution-tax measurement.** Very useful as a controlled token-tax baseline — but does not generate the trajectory complexity needed to observe execution-tax. Consider as a baseline comparison, not the primary task family. |

---

### E. Calendar / task scheduling simulation

**Description:** A synthetic calendar with existing events; the agent must schedule a new appointment satisfying stated constraints without conflicts.

**Example tasks:** "Schedule a 90-minute meeting between Alice, Bob, and Carol next week, avoiding existing appointments, between 09:00 and 17:00."

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **High.** The scheduled slot is either valid (no conflicts, within constraints) or not. Deterministic. |
| Multilingual equivalence | **Medium.** Time formats, weekday names, and scheduling conventions vary across languages and cultures. Requires careful normalization. |
| Trajectory richness | **Medium-high.** Requires reading calendar state, evaluating constraints, potentially backtracking — multi-step planning trajectory. |
| Risk of ambiguity | **Low-medium.** "Next week" is ambiguous across calendar conventions; explicit date ranges eliminate this. |
| Risk of evaluator bias | **Low.** Constraint-satisfaction outcome is binary. |
| Token-tax/execution-tax separation | **Good.** Planning loop depth, backtracking, and constraint evaluation steps are attributable. If Language B requires more planning steps for the same constraint satisfaction problem, that is a candidate execution-tax signal. |
| Suitability for v0.1 | **Medium.** Viable backup option. More complex to construct a good synthetic dataset than Product FAQ. |

---

### F. Tool-use arithmetic / lookup tasks

**Description:** The agent retrieves values from a synthetic table and computes a simple answer — e.g., total price given quantity and unit price, or a date difference.

**Example tasks:** "What is the total cost for 3 units of product X at the listed price plus 21% VAT?" / "How many days between the order date and the delivery date in this record?"

| Evaluation dimension | Assessment |
|---|---|
| Success-checkability | **Very high.** Arithmetic answers are deterministic. |
| Multilingual equivalence | **High for arithmetic.** Number formatting and decimal conventions vary, but the underlying operation is language-neutral. |
| Trajectory richness | **Low.** Retrieval + arithmetic. Minimal reasoning complexity. |
| Risk of ambiguity | **Very low.** |
| Risk of evaluator bias | **None.** Numeric answer. |
| Token-tax/execution-tax separation | **Very limited.** Almost entirely token-tax in the lookup/input phase. Arithmetic execution is deterministic and language-neutral once the lookup is complete. |
| Suitability for v0.1 | **Low for execution-tax measurement.** Useful as a controlled micro-benchmark for token-tax at the lookup step. Not a primary task family. |

---

## 4. Recommended first task family

**Primary recommendation: Product FAQ / policy QA (Option A)**

A fictional synthetic knowledge base — a smart-home device, a software subscription service, or a similar neutral product — with an associated FAQ, warranty policy, return policy, and troubleshooting guide.

**Reasons:**

- **Success is deterministic.** Each task has a pre-defined expected answer derived from the knowledge base. The success check is whether the required fact is present and correctly stated — not whether the output is stylistically good.
- **Multilingual equivalence is controllable.** The knowledge base is authored in a language-neutral canonical form (or with explicit cross-language aligned versions), not sourced from a single-language public document.
- **Trajectory is rich enough to be interesting.** A policy question with multiple conditions (purchase date, damage type, device category) requires the agent to retrieve the relevant policy section and reason over multiple conditions. This generates a trajectory with attributable retrieval and reasoning steps.
- **Trajectory is not so complex that it overwhelms v0.1.** The knowledge base is small and controlled; there are no external API calls, real-world dependencies, or open-ended planning loops.
- **Failure taxonomy is well-supported.** Intent failures, factual failures, retrieval failures, and missing-step failures all have natural realizations in this task family. The failure taxonomy from the rubric maps directly.
- **Token-tax/execution-tax decomposition is tractable.** Representation overhead (longer input in morphologically complex languages), retrieval overhead (more or different retrieval calls), and retry overhead (more failed retrieval attempts before success) are separable in this design.
- **Independence is easy to maintain.** There is no risk of using employer, customer, or proprietary data — the entire knowledge base is synthetic and project-specific.

---

## 5. Why not start with open-ended tasks

Open-ended task families — creative writing, broad advisory questions, long-form planning, subjective recommendations — fail the v0.1 selection criteria on multiple dimensions:

**Success is not deterministic.** Whether a creative output is "good" or a strategic recommendation is "correct" requires open-ended evaluator judgment. Open-ended judgment is where cross-language evaluator bias is hardest to control and easiest to introduce. The rubric's requirement for language-independent success criteria cannot be met.

**Evaluator bias is difficult to detect.** In a constrained task, a biased evaluator produces a wrong PASS/FAIL for a verifiable reason. In an open-ended task, a biased evaluator produces a score that looks plausible but favors English-shaped output, without any ground truth to check against.

**Token-tax/execution-tax decomposition is intractable.** If the task requires the agent to produce a long, novel response, differences in output length between languages may reflect stylistic variation rather than execution overhead. The representation/generation boundary becomes unclear.

**Retry and failure signals are ambiguous.** In a constrained task, a retry has a clear trigger — the agent failed to retrieve the right fact or produced an incorrect answer. In an open-ended task, a retry may reflect the agent's uncertainty about quality, not a task failure — which is not execution-tax in the sense NiceM hypothesizes.

Open-ended tasks are appropriate for evaluating model capabilities. They are not appropriate as the primary task family for a controlled execution-tax measurement. NiceM may revisit them in a later version once the basic methodology is validated on constrained tasks.

---

## 6. Example task skeletons

These are abstract task templates — not data, not prompts. The specifics (device names, policy values, dates) are placeholders. The structure illustrates how each task type maps to the success criteria and trajectory components.

**T1 — Warranty coverage check (multi-condition reasoning)**
> User asks: "Is [damage type] covered under warranty for a [device] purchased [N months ago]?"
> Expected outcome: YES/NO + the relevant policy clause (e.g., "No — section 3.2 excludes liquid damage regardless of purchase date")
> Conditions: purchase date within warranty period AND damage type not excluded
> Trajectory: retrieve warranty policy → evaluate purchase date condition → evaluate damage-type condition → generate answer

**T2 — Subscription plan eligibility (constraint matching)**
> User asks: "Which plan allows [feature X] for [N users] at under [price]?"
> Expected outcome: Plan name (or "no plan matches")
> Trajectory: retrieve plan catalogue → filter by feature → filter by user count → filter by price → generate answer

**T3 — Troubleshooting step selection (procedure lookup)**
> User asks: "My device shows [symptom]. What should I try first?"
> Expected outcome: Step N from the troubleshooting guide for that symptom
> Trajectory: retrieve troubleshooting guide → locate symptom → identify first step → generate answer

**T4 — Return eligibility check (policy QA with date arithmetic)**
> User asks: "I bought [product] on [date]. Can I return it? I [have/have not] opened the packaging."
> Expected outcome: YES/NO + condition (e.g., "Yes, if returned within 30 days of purchase — your purchase is within the window")
> Trajectory: retrieve return policy → evaluate days since purchase → evaluate packaging condition → generate answer

**T5 — Feature availability lookup (factual retrieval)**
> User asks: "Does [product model] support [feature]?"
> Expected outcome: YES/NO + source (e.g., "Yes — section 2.1 lists [feature] as supported on model X")
> Trajectory: retrieve product specifications → locate model → check feature flag → generate answer

These skeletons are intentionally simple at the task level and rich at the reasoning level. A single-step lookup (T5) is the baseline; multi-condition tasks (T1, T4) require sequential reasoning and are more likely to reveal trajectory differences across language conditions.

---

## 7. Expected trajectory components

For the Product FAQ / policy QA task family, a typical agent trajectory would include some or all of the following:

| Component | Expected in this task family | Notes |
|---|---|---|
| Retrieval call | Yes — 1 to 3 expected | Retrieve policy section, product spec, or troubleshooting guide |
| Context expansion | Yes | Retrieved content added to context at each step |
| Reasoning step | Yes — 1 to 3 expected | Conditional evaluation (date check, damage-type exclusion, etc.) |
| Tool call | Optional | If date arithmetic is implemented as a tool (e.g., days-since-purchase calculator) |
| Answer generation | Yes — 1 final | The agent produces its response |
| Retry | Possible | If retrieval returns low-confidence or irrelevant content; if reasoning produces an uncertain intermediate result |
| Uncertainty signal | Possible | Agent may express uncertainty if the query does not clearly match any policy clause |

The trajectory is predictable enough to attribute costs to components (retrieval tokens, reasoning tokens, retry tokens) and controlled enough to compare across language conditions. This is the right level of complexity for v0.1.

---

## 8. Relationship to success rubric

The Product FAQ / policy QA task family maps cleanly to the rubric defined in `docs/methodology/success-rubric-v0.1.md`:

| Rubric element | Task family mapping |
|---|---|
| **PASS** | Agent returns the required fact and correctly applies the relevant policy condition; answer matches expected outcome |
| **FAIL** | Agent returns wrong fact, misapplies condition, omits required step, or retrieves irrelevant content |
| **UNCERTAIN** | Agent returns a plausible but unverifiable answer; expected outcome is ambiguous in the canonical policy document |
| **Intent failure** | Agent answers a different question than asked (e.g., explains the warranty policy in general instead of answering the coverage question) |
| **Factual failure** | Agent states an incorrect policy value (e.g., "30 days" when the policy says "14 days") |
| **Missing-step failure** | Agent evaluates one condition (purchase date) but omits the other (damage type exclusion) |
| **Retrieval failure** | Agent retrieves the wrong section of the knowledge base and reasons from it |
| **Language/translation failure** | Agent loses a key constraint in translation or expresses the answer in a way that a native speaker of the target language would find ambiguous or misleading |
| **Multilingual equivalence** | Same policy facts, same required conditions, same expected outcome defined in language-neutral terms before any run; no English-shaped output advantage |

---

## 9. Relationship to token-tax vs. execution-tax

The Product FAQ / policy QA task family supports the decomposition proposed in framework §7 and success rubric §11:

**Representation overhead (token-tax component):** A query in Turkish, Arabic, or a morphologically rich language will tokenize to more tokens than the same query in English. This adds to input token count before any retrieval occurs. This effect is expected and is the known token-tax signal from Petrov/Ahia/Lundin.

**Generation overhead (token-tax component):** The agent's answer in some languages may require more tokens to express the same fact (e.g., agglutinative languages like Turkish may produce longer output tokens for equivalent semantic content). This is also a token-tax component.

**Retrieval overhead (candidate execution-tax):** If the query in Language B causes the retrieval system to return less relevant or lower-ranked content than the same query in English, the agent may need to issue more retrieval calls, retrieve more tokens, or retry with a different query. This is the retrieval overhead component of candidate execution-tax — it is not explained by input length alone.

**Reasoning overhead (candidate execution-tax):** If the agent requires more reasoning steps to resolve a multi-condition query in Language B than in Language A — for equivalent policy questions — that difference in step count is a candidate execution-tax signal.

**Retry overhead (candidate execution-tax):** If Language B runs fail more often at an intermediate step and require the agent to retry, that retry cost is not explained by the initial token-tax. It is a candidate execution-tax component.

**Measurement approach:** For each run, NiceM records total tokens, retrieval calls, retrieval tokens, reasoning steps, and retry count. Representation and generation overhead are estimated from the input/output token count difference versus English baseline. The residual — excess retrieval, reasoning, or retry cost after controlling for that baseline — is the candidate execution-tax signal.

This is the test. It may produce a null result. If residual cost variation across languages is statistically indistinguishable from zero after controlling for input/output token-tax, then execution-tax in this task family does not exist. That is a valid and informative outcome.

---

## 10. Initial recommendation

**Primary task family: Product FAQ / policy QA**
Fictional product with synthetic knowledge base (FAQ, warranty policy, return policy, troubleshooting guide). Tasks with deterministic expected outcomes based on policy conditions. Minimum two conditions per task to ensure multi-step reasoning. Task skeletons T1–T5 as starting point.

**Backup task family: Calendar / task scheduling simulation (Option E)**
If the Product FAQ family proves too limited in trajectory richness (e.g., retrieval is consistently single-step and retry is rare), a scheduling task adds planning-loop depth and constraint backtracking. More complex to construct; use if the primary family does not produce sufficient trajectory variation.

**Task families to avoid in v0.1:**
- **Structured form completion (Option D):** Too simple for execution-tax measurement; use only as a token-tax baseline if needed.
- **Tool-use arithmetic / lookup (Option F):** Same reason — minimal trajectory.
- **Open-ended tasks of any kind:** Evaluator bias is uncontrollable; success criteria are not deterministic.
- **Public document QA from real documents (Option C as written):** Cross-language equivalence is difficult to guarantee when the source document is in one language. Acceptable only if the document is synthetic and purpose-built in canonical form.

---

## 11. Open questions before validation plan

These questions must be resolved before a dataset can be constructed and a benchmark run.

- **How many synthetic documents?** *Resolved (exploratory) by `docs/methodology/benchmark-sizing-v0.1.md`:* Small KB — 6–10 synthetic policy/FAQ documents, 50–100 canonical facts; minimum viable proposal is 8 documents / ~75 facts. The binding constraint is the KB quality-control gate across three languages, not retrieval realism.
- **How many task instances?** *Resolved (exploratory) by `docs/methodology/benchmark-sizing-v0.1.md`:* 30–50 unique intents, each rendered in all three languages; minimum viable proposal is 36 intents × 3 languages = 108 task instances, 2–3 repetitions only if budget allows. Explicitly exploratory — produces the variance estimates M8 needs; cannot confirm or refute the execution-tax hypothesis.
- **How many languages?** *Resolved by `docs/methodology/language-selection-v0.1.md`:* English (analytic baseline; the structured fact-set, not English, is canonical), Dutch (near-baseline Latin-script comparison), Turkish (agglutinative Latin-script probe; bilingual review required, with an English+Dutch fallback). v0.2 expansion candidates ranked there (Arabic first).
- **Should knowledge base documents be translated or constructed language-specifically?** Translation of a canonical English knowledge base is simpler to control but may introduce translation artifacts. Constructing each language version from a shared canonical fact-set (same facts, expressed naturally in each language) is more valid but more expensive. For v0.1, translation from canonical + bilingual review is a reasonable middle ground.
- **Should retrieval be language-aware or language-neutral?** If the retrieval system uses multilingual embeddings, a query in Turkish may retrieve content from any language section of the knowledge base — potentially reducing language-specific retrieval overhead. If retrieval is language-matched, the knowledge base must be fully translated. The choice affects what the experiment measures. *Now analyzed in `docs/methodology/retrieval-design-decision-v0.1.md`: recommendation is language-matched retrieval for v0.1 (with KB quality control as a hard prerequisite), language-neutral retrieval pre-registered as the v0.2 contrast condition, and a structured-fact-store fallback if KB quality control proves infeasible.*
- **Should expected answers be language-neutral fact triples?** Yes — the expected outcome for each task should be expressed as a structured fact (e.g., `{covered: false, reason: "liquid damage excluded", clause: "3.2"}`) rather than as a target string in any language. This is what makes the success check language-neutral.
- **How to avoid English being the hidden canonical version?** The canonical fact-set should be expressed in neutral terms before any language rendering. If the policy document is drafted in English first and then translated, English may become the implicit ground truth for ambiguity resolution. The canonical representation should be the structured fact-set, not the English text.
