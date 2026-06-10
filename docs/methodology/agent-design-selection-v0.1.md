# NiceM Agent Design Selection v0.1

**Status:** Decision made — Agent A (Direct LLM baseline) and Agent B (Simple RAG agent) for v0.1
**Addresses:** Framework §12 agent-designs prerequisite ("at least two architectures to separate language effects from architecture effects")
**Depends on:** `docs/methodology/logging-schema-v0.1.md`, `docs/methodology/retrieval-design-decision-v0.1.md`, `docs/methodology/benchmark-sizing-v0.1.md`, `docs/methodology/language-selection-v0.1.md`
**Feeds into:** Pilot implementation, M9 instrumentation choice, v0.2 agent-design expansion

**Fixed context for this decision:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 synthetic documents, ~75 canonical facts (structured fact-set canonical)
- Intents: 36 unique intents × English, Dutch, Turkish
- Retrieval: language-matched retrieval
- Success rubric: PASS / FAIL / UNCERTAIN
- Logging: one row per run with endpoint outcome and trajectory trace (logging-schema-v0.1)
- Execution-tax remains a hypothesis

---

## 1. Purpose

Execution-tax — if it exists — is a property of workflows, not of tokenizers alone. The same intent in the same language can produce very different total workloads depending on how the agent is built: whether it retrieves, how often it retries, whether it validates, whether it silently translates.

This makes agent design a measured variable, not an implementation detail:

- With only one agent design, a cross-language cost difference cannot be attributed: it could be token-tax, execution-tax, or an artifact of that one design.
- With at least two designs, NiceM can ask the question that defines the project: **does workflow design amplify or suppress language-related cost per successful completion?**
- The choice of designs also bounds what trajectory data exists at all. A design with no retrieval produces no retrieval overhead to measure; the candidate execution-tax components only become observable when the workflow includes the steps that generate them.

Choosing the wrong designs at v0.1 — too many, or too complex — would make attribution impossible at the pilot's sample size (36 intents). The selection below optimizes for attribution, not realism.

---

## 2. Selection criteria

A design is suitable for v0.1 if it is:

| Criterion | Requirement |
|---|---|
| **Simple enough for v0.1** | Implementable and debuggable without a multi-week engineering effort; failure modes traceable by hand |
| **Measurable with the logging schema** | Every minimal required field in logging-schema §12 can be captured for this design |
| **Produces comparable outputs** | Final answers are judgeable by the same PASS/FAIL/UNCERTAIN gate against the same expected fact-sets |
| **Avoids too many variables** | Differs from the other v0.1 design in one architectural dimension, so differences are attributable |
| **Allows endpoint success comparison** | Success rates per design per language can be computed and compared |
| **Creates enough trajectory information** | At least one design must generate retrieval/step/retry events, or candidate execution-tax has nothing to measure |
| **Compatible with synthetic Product FAQ / Policy QA** | Works against a small fictional KB; no capabilities the task family doesn't need |
| **Independent** | Requires no employer, customer, or internal data; runs entirely on the synthetic benchmark |

---

## 3. Candidate agent designs

### Agent A — Direct LLM baseline

**Definition:** The model receives the user query and either no retrieved context or a minimal provided context, depending on the benchmark condition. One model call, no tools, no retrieval loop.

| Dimension | Assessment |
|---|---|
| What it measures | Pure representation + generation behavior per language: token counts, latency, cost, and success without any workflow machinery |
| Strengths | Maximally simple; cheapest; isolates token-tax-adjacent overhead; establishes the floor against which workflow overhead is measured |
| Weaknesses | Because the product is fictional, a no-context Direct LLM should fail on most intents — which is informative (it confirms tasks require retrieval) but yields few PASS runs for cost-per-successful-completion. A full-KB-in-context variant fixes this but changes what is measured (see open question AD1) |
| Expected trajectory richness | Minimal — `model_calls`=1, no retrieval fields, no retries by design |
| Relationship to token-tax | Direct — input/output token differences across languages on identical intents are the cleanest token-tax measurement this benchmark produces |
| Relationship to execution-tax | None on the retrieval/tool/retry side — that is its role: it is the control condition |
| Suitability for v0.1 | **Suitable — required.** Without it, RAG overhead cannot be separated from baseline language overhead |

### Agent B — Simple RAG agent

**Definition:** The agent embeds the query, retrieves top-k chunks from the language-matched KB rendering, and answers using the retrieved context. Single retrieval pass by default; no planner, no router, no translation step.

| Dimension | Assessment |
|---|---|
| What it measures | Retrieval overhead per language on top of representation/generation: retrieval calls, retrieved tokens vs. semantic units, missed facts, irrelevant chunks, retrieval latency |
| Strengths | The minimal design that makes candidate execution-tax observable at all; one architectural step away from Agent A, so A-vs-B differences are attributable to retrieval; matches the retrieval-design decision exactly |
| Weaknesses | Does not produce the full agentic repertoire (multi-tool use, planning, long loops); retrieval quality depends on embedding model and chunking choices, which become confounds if not held constant |
| Expected trajectory richness | Moderate — all retrieval fields populated; retries only if the design permits them (open question AD4) |
| Relationship to token-tax | Inherits Agent A's representation/generation overhead, plus retrieved-context token counts that must be dual-reported in semantic units to avoid double-counting (logging-schema §5) |
| Relationship to execution-tax | The primary probe — if Turkish conditions need more retrieval calls or miss more required facts than English conditions for the same intents, that is the first candidate execution-tax signal |
| Suitability for v0.1 | **Suitable — required.** |

### Agent C — Translation-first RAG

**Definition:** The agent translates the query into an internal working language (typically English), retrieves, answers, and optionally translates the answer back into the query language.

- **Why it may reduce overhead:** if English retrieval and generation are cheaper and more accurate, paying a fixed translation cost up front could lower total cost per successful completion for non-English queries — this is a commercially important possibility.
- **Why it may increase overhead:** translation adds model calls, tokens, latency, and a new error source (translation mistakes propagate into retrieval and the final answer); for languages close to English the translation cost may exceed the savings.
- **Why defer to v0.2:** it is the natural *intervention* arm — the design you test once the measurement instrument is validated. Running it before A-vs-B baselines exist would mean testing a remedy before the disease is measured. It also conflicts with the v0.1 language-matched retrieval design (it would retrieve from the English rendering for Turkish queries, which is the pre-registered v0.2 contrast territory).
- **Logging requirement:** when it runs, `translation_used` must be true by construction, and translation calls must be counted in `model_calls` and token/cost fields. Note the related risk that Agents A/B may translate *covertly* inside the model — see §8 and AD6.

### Agent D — Language-aware RAG

**Definition:** The agent detects the query language and applies language-specific retrieval parameters, chunking, or prompting.

- **Why it is strategically important:** it is the seed of NiceM's product direction — `observe → diagnose → recommend` implies eventually recommending language-aware execution. If language-aware design measurably reduces candidate execution-tax, that is the core product claim.
- **Why it is too complex for v0.1:** every language-specific adaptation is a new variable (per-language chunk sizes, per-language prompts, detection errors). At 36 intents, attribution across that many degrees of freedom is hopeless, and tuning per-language parameters on the same data used for measurement would invalidate the comparison.
- **Defer to v0.2+**, after A-vs-B establishes what the unadapted baseline looks like.

### Agent E — Prompt-compressed RAG

**Definition:** The agent uses compressed prompts and/or aggressively reduced retrieved context to cut token volume.

- **Why it may reduce token cost:** smaller prompts and contexts directly cut input tokens — a candidate mitigation for token-tax-driven cost.
- **Why it may affect success:** compression can drop required facts or instructions; the cost saving is only real if the success rate holds — which is precisely why cost-per-*successful*-completion, not cost-per-run, is NiceM's metric.
- **Why defer:** like Agent C, it is an intervention arm. It also interacts with language (compression may harm morphologically dense languages differently), which is interesting but unmeasurable before baselines exist.

### Agent F — Model-router agent

**Definition:** The system routes each query to a different model based on language, task category, or estimated complexity.

- **Why it is commercially interesting:** routing is the most direct lever on cost per successful completion in production systems, and "route by language" is a plausible NiceM recommendation type.
- **Why it adds too many variables for v0.1:** it multiplies the model dimension into the design dimension. A router's results conflate routing policy quality, per-model language ability, and per-model pricing — none separable at pilot scale. v0.1 has not even chosen its single model yet (LS4).
- **Defer to v0.2+.**

---

## 4. Recommended v0.1 designs

**Agent A (Direct LLM baseline) and Agent B (Simple RAG agent).**

- **Agent A establishes the non-retrieval baseline.** Per-language token, latency, cost, and success numbers with zero workflow machinery — the floor that defines what "overhead" means.
- **Agent B introduces exactly one architectural addition: retrieval.** This is the minimal design that makes the candidate execution-tax components (retrieval calls, missed facts, irrelevant retrievals, retrieval latency) observable. Because A and B differ in one dimension, the A-to-B delta per language is attributable.
- **Everything more complex is deferred** until the measurement instrument itself is validated. Agents C–F are interventions or product prototypes; testing interventions before the baseline instrument is trusted would produce uninterpretable results. This mirrors the project-wide pattern: validate the measurement first, optimize second.

This satisfies the framework §12 requirement of at least two architectures, at the minimum complexity that requirement permits.

---

## 5. What each design can and cannot prove

- **Agent A cannot measure retrieval-side execution-tax.** It has no retrieval. Its role is control, not probe.
- **Agent B can reveal retrieval overhead but not all agentic overhead.** Tool-use overhead, planning overhead, and long-loop retry dynamics are absent from a single-pass RAG design. A null result on Agent B does not rule out execution-tax in richer architectures.
- **v0.1 as a whole cannot prove broad agentic execution-tax.** Two designs, one task family, three languages, one model, 36 intents — every result is bounded by those choices (benchmark-sizing §11).
- **What v0.1 *can* test:** whether the measurement framework detects meaningful, reproducible trajectory differences at all — across languages within a design, and between designs within a language. That is the pilot's actual claim scope.

## 6. Relationship to token-tax vs execution-tax

- **Agent A mostly exposes representation and generation overhead** — the components closest to established token-tax. Cross-language differences in Agent A runs are, to first order, token-tax measurements.
- **Agent B exposes retrieval overhead in addition.** Its retrieval fields (in semantic units, per the dual-reporting rule) populate the candidate execution-tax bucket of the framework §7 decomposition.
- **The A-vs-B delta, compared across languages, is the pilot's key contrast.** If the cost gap between English and Turkish is the same under A and B, workflow design neither amplifies nor suppresses language cost in this setup. If the gap *widens* under B (e.g., Turkish retrieval misses more facts, forcing more context or failures), that is the first evidence that workflow design amplifies language-related cost — the heart of the execution-tax hypothesis. If it *narrows*, retrieval may actually compensate. All three outcomes are informative; none is assumed.

## 7. Required logging fields per design

Both designs log the full minimal field set of logging-schema §12. Design-specific emphasis:

**Agent A — Direct LLM:**
- `model_calls` (=1 by design; deviations are anomalies worth catching)
- `input_tokens`, `output_tokens`, `total_tokens`
- `total_latency_ms`
- `estimated_total_cost`, `pricing_version`
- `endpoint_outcome`, `failure_type`, `uncertainty_reason`
- `retrieval_enabled` = false; all retrieval fields null (logged as null, not omitted — schema uniformity across designs)
- `translation_used` (hidden-translation flag still applies — see AD6)

**Agent B — Simple RAG:**
- All Agent A fields, plus:
- `retrieval_calls`
- `retrieved_chunk_ids`, `retrieved_fact_ids`
- `retrieved_context_token_count`, `retrieved_context_semantic_units_count`
- `missing_required_fact_count`, `irrelevant_retrieval_count`
- `retrieval_latency_ms`
- `retry_count` and `error_events` (if retries are permitted — AD4)

`agent_design_id` distinguishes the designs in every row; analysis must never pool across designs.

## 8. Risks

| Risk | Consequence | Mitigation |
|---|---|---|
| Direct LLM hallucinates without context | Agent A produces confident wrong answers about the fictional product | Expected and informative — the `answer_contains_forbidden_claims` field and failure taxonomy capture it; confirms tasks are retrieval-dependent |
| RAG quality depends on KB rendering and embedding model | A weak Turkish rendering or an English-biased embedding model masquerades as language execution-tax | KB quality-control gate (hard prerequisite); same embedding model across languages (AD2); report per `kb_rendering_version` |
| Too many agent designs | Attribution impossible at 36 intents | Resolved by this decision: two designs only |
| Model differences dominate agent-design effects | If A and B used different models, nothing is attributable | One model for both designs in v0.1 (model TBD under LS4); model is held constant, design varies |
| Hidden internal translation | The model may internally reason in English on Turkish inputs, blurring what "language condition" means | Log `translation_used` where detectable; acknowledge that covert in-model translation is not fully detectable (AD6) — a stated limitation, not a solved problem |
| Simple RAG produces too few retries/tool calls | Several candidate execution-tax components stay near zero, limiting what the pilot can observe | Accepted for v0.1 — a near-empty retry column is itself a finding; richer designs are the v0.2 path |

## 9. v0.2 expansion

Candidates, in rough priority order:

1. **Translation-first RAG (Agent C)** — the most direct test of whether routing through a working language reduces cost per successful completion; pairs naturally with the pre-registered language-neutral retrieval contrast.
2. **Language-aware RAG (Agent D)** — the product-direction prototype: does language-specific adaptation reduce candidate execution-tax?
3. **Prompt-compressed RAG (Agent E)** — token-cost mitigation with success-rate guardrails.
4. **Model-router agent (Agent F)** — routing by language/task/complexity; requires multi-model cost and quality baselines first.
5. **Multi-step validation agent** — adds self-checking/validation steps; tests whether paying validation overhead buys enough success-rate improvement to lower cost per successful completion.

The framing for all of v0.2: **v0.1 measures whether candidate execution-tax is observable; v0.2 tests whether agent design can reduce it.** That ordering is what separates a measurement project from a collection of demos.

## 10. Open questions (AD1–AD7)

| ID | Question | Status | Notes |
|---|---|---|---|
| AD1 | Should Direct LLM receive full KB context or no KB context? | Open | No-context measures the retrieval-dependence floor (mostly FAILs expected); full-KB-in-context measures long-context cost without retrieval and yields PASS runs for cost comparison. Possibly run both as A0/A1 sub-conditions — but that adds a condition at fixed budget (BS6) |
| AD2 | Should Simple RAG use the same embedding model across languages? | Open, leaning yes | Same multilingual embedding model across all three renderings keeps the design constant; its possibly uneven per-language quality is then a measured property, not a confound introduced by the experimenter |
| AD3 | How many chunks should Simple RAG retrieve (top-k)? | Open | Fixed k across languages is required; the value interacts with chunk size and BS4 (facts per document) |
| AD4 | Should retries be allowed in v0.1? | Open | A single-pass design is cleaner but empties the retry column; one bounded retry on retrieval failure would populate it. Must be identical across languages either way |
| AD5 | Should the RAG agent include a validation step? | Open, leaning no for v0.1 | Validation belongs to the v0.2 multi-step validation agent; adding it to Agent B blurs the one-dimension A/B contrast |
| AD6 | How can hidden translation by the model/provider be detected? | Open | Output-language checks and reasoning-trace inspection catch some cases; covert in-model translation may be undetectable and must be stated as a limitation in all v0.1 reporting |
| AD7 | How are prompts kept equivalent across languages? | Open | Same instruction set rendered from a language-neutral prompt specification (the fact-set principle applied to prompts); rendering review parallels the KB quality-control gate; relates to LS2 (Turkish register) |

---

## Dependencies and update log

| Document | What changes with this decision |
|---|---|
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 agent-designs checklist item resolved: Agent A + Agent B |
| `docs/methodology/logging-schema-v0.1.md` | No schema change required — both designs are covered; null-not-omitted convention for retrieval fields in Agent A runs noted here |
| `docs/open-questions.md` | AD1–AD7 added; framework checklist status reflected |
| `docs/source-map.md` | agent-design-selection-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10*
