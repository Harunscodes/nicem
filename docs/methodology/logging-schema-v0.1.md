# NiceM Logging Schema v0.1

**Status:** Schema defined — pending implementation and pilot validation
**Addresses:** Framework §12 logging-schema prerequisite; operationalizes the trajectory metrics in framework §6 and the decomposition in framework §7
**Depends on:** `docs/methodology/success-rubric-v0.1.md`, `docs/methodology/benchmark-sizing-v0.1.md`, `docs/methodology/language-selection-v0.1.md`, `docs/methodology/retrieval-design-decision-v0.1.md`
**Feeds into:** Instrumentation platform choice (M9), pilot implementation, M6 counting rules

**Fixed context for this schema:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 synthetic documents, ~75 canonical facts (structured fact-set is the canonical artifact)
- Intents: 36 unique intents
- Languages: English, Dutch, Turkish
- Retrieval: language-matched retrieval
- Success rubric: PASS / FAIL / UNCERTAIN (binary gate with UNCERTAIN as first-class outcome)
- Execution-tax remains a hypothesis — this schema defines what would be measured, not what has been found

---

## 1. Purpose

The logging schema must be defined before any implementation, because:

- **Metrics that are not logged cannot be recovered.** If retrieval calls are not logged per run, the candidate execution-tax decomposition cannot be computed afterwards; the pilot would have to be re-run.
- **The decomposition depends on field separation.** Token-tax and candidate execution-tax can only be separated if representation, generation, retrieval, tool, retry, and correction overhead are logged as distinct fields (framework §7). A single "total tokens" number cannot be decomposed post hoc.
- **Cross-condition comparability requires identical fields.** Every run in every language/agent/model condition must log exactly the same schema, or per-condition comparisons silently break.
- **Pre-defining fields prevents post-hoc metric invention.** Deciding now what will be measured is a guard against finding "patterns" in whatever happened to be logged.

This document is a specification, not code. It defines field names, meanings, and units. The implementation (instrumentation platform, storage format) is decided later under M9.

---

## 2. Unit of observation

**One row = one run:**

> One intent, rendered in one language, executed by one agent design, with one model configuration, against one KB rendering, producing one endpoint outcome and one trajectory trace.

Implications:

- Repetitions of the same intent/language condition are separate rows (distinguished by `run_id`), never averaged at logging time. Aggregation happens at analysis time only.
- A run that crashes or is abandoned is still a row — with `error_events` populated and an endpoint outcome of FAIL or UNCERTAIN. Dropping failed runs from the log would bias cost-per-successful-completion.
- Derived metrics (§10) are computed from rows; they are not themselves rows.

---

## 3. Identifiers

| Field | Type | Meaning |
|---|---|---|
| `run_id` | string (unique) | Globally unique identifier for this run |
| `timestamp` | ISO 8601 | Run start time (UTC) |
| `benchmark_version` | string | Version of the benchmark specification (e.g., `v0.1`) |
| `intent_id` | string | One of the 36 unique intents; stable across languages |
| `task_category` | enum | Category from benchmark-sizing §6 (warranty, return, plan, troubleshooting, shipping, repair, account) |
| `language` | enum | `en` / `nl` / `tr` — the language condition of this run |
| `kb_version` | string | Version of the canonical structured fact-set |
| `kb_rendering_version` | string | Version of the language-specific KB rendering used (per-language; changes when a rendering is revised after review) |
| `expected_fact_set_id` | string | Identifier of the language-neutral expected fact-set for this intent |
| `agent_design_id` | string | Which agent architecture executed the run (framework §12 requires at least two) |
| `prompt_version` | string | Version of the system/task prompt template |
| `model_id` | string | Exact model identifier and version used |
| `retrieval_design_id` | string | `language-matched-v0.1` for all v0.1 runs; future values for v0.2 contrast condition |
| `evaluator_version` | string | Version of the success-evaluation procedure (rubric version + checker version) |

Every identifier is mandatory. A run with a missing identifier cannot be placed in the analysis design and must be discarded — log validation should reject such rows at write time.

---

## 4. Input fields

| Field | Type | Meaning |
|---|---|---|
| `user_query_text` | string | The exact query text sent to the agent (synthetic — see §14) |
| `user_query_token_count` | int | Token count of the query under the measurement tokenizer |
| `query_language` | enum | Language of the query; normally equals `language`, logged separately to catch rendering errors |
| `input_character_count` | int | Character count of the query (tokenizer-independent size measure) |
| `input_word_count` | int | Whitespace-delimited word count (enables fertility F = tokens/words per Lundin; imperfect for agglutinative Turkish — note in analysis) |
| `tokenizer_name` | string | Tokenizer used for all token counts in this row |
| `tokenizer_version` | string | Tokenizer version |

Character and word counts exist so that token-tax can be expressed relative to tokenizer-independent size measures. The choice of measurement tokenizer is open (LS4, §15).

---

## 5. Retrieval fields

| Field | Type | Meaning |
|---|---|---|
| `retrieval_enabled` | bool | Whether retrieval was active for this run |
| `retrieval_calls` | int | Number of retrieval invocations during the run |
| `retrieved_chunk_ids` | list | IDs of all chunks returned, in order |
| `retrieved_fact_ids` | list | Canonical fact IDs contained in the retrieved chunks (mapped via the fact-set) |
| `retrieved_context_token_count` | int | Total tokens of retrieved context injected into the model |
| `retrieved_context_character_count` | int | Character count of retrieved context |
| `retrieved_context_semantic_units_count` | int | Number of canonical facts retrieved (deduplicated) |
| `irrelevant_retrieval_count` | int | Retrieved chunks containing no fact from the expected fact-set's dependency closure |
| `missing_required_fact_count` | int | Required facts (per expected fact-set) never retrieved during the run |
| `retrieval_latency_ms` | int | Total time spent in retrieval calls |
| `retrieval_notes` | string | Free-text anomalies (e.g., empty results, duplicate chunks) |

**Null-not-omitted convention:** For designs without retrieval (Agent A in `docs/methodology/agent-design-selection-v0.1.md`), `retrieval_enabled` is false and all other retrieval fields are logged as null — never omitted — so every row in every design carries an identical schema.

**Dual-reporting rule (from retrieval-design-decision §8):** retrieval volume must always be reported in both raw tokens (`retrieved_context_token_count`) and semantic units (`retrieved_context_semantic_units_count`). A Turkish chunk carrying the same three facts as an English chunk may cost more tokens — that difference is token-tax (representation overhead), not retrieval overhead. Logging only token counts would double-count token-tax inside the retrieval component.

---

## 6. Agent trajectory fields

| Field | Type | Meaning |
|---|---|---|
| `model_calls` | int | Number of LLM invocations in the run |
| `tool_calls` | int | Number of tool invocations (excluding retrieval, which is logged separately) |
| `agent_steps` | int | Total agent loop iterations |
| `retry_count` | int | Steps re-attempted after a failed or rejected attempt (counting rule per M6 — still open; log raw events so any rule can be applied later) |
| `planning_steps` | int | Steps classified as planning/decomposition (if the agent design distinguishes them; else null) |
| `validation_steps` | int | Steps classified as self-checking/validation (if distinguishable; else null) |
| `fallback_used` | bool | Whether any fallback path was taken |
| `translation_used` | bool | Whether the agent translated content between languages at any point (important confound flag for language-matched retrieval) |
| `human_intervention_used` | bool | Whether a human corrected or steered the run before the endpoint |
| `total_latency_ms` | int | Wall-clock duration of the full run |
| `error_events` | list | Structured list of errors (type, step, recoverable yes/no) |

`translation_used` deserves emphasis: if the agent internally translates a Turkish query to English, retrieves, and translates back, the run no longer measures what the language-matched design intends. Such runs must be flaggable, not invisible.

---

## 7. Token and cost fields

| Field | Type | Meaning |
|---|---|---|
| `input_tokens` | int | Total prompt-side tokens across all model calls |
| `output_tokens` | int | Total completion-side tokens across all model calls |
| `retrieval_tokens` | int | Tokens of retrieved context (equals `retrieved_context_token_count`; duplicated here for cost arithmetic) |
| `total_tokens` | int | input + output tokens across the run |
| `billable_tokens` | int | Tokens actually billed by the provider (may differ from total due to caching or pricing rules) |
| `estimated_model_cost` | decimal | Estimated model API cost for the run |
| `estimated_retrieval_cost` | decimal | Estimated cost of retrieval infrastructure (embedding calls, vector store) |
| `estimated_tool_cost` | decimal | Estimated cost of non-retrieval tool calls |
| `estimated_total_cost` | decimal | Sum of the above |
| `cost_currency` | string | Currency code (e.g., `USD`) |
| `pricing_version` | string | Identifier of the price table used — prices change; without this, costs across runs are not comparable |

All cost fields are estimates and must be labeled as such in reporting. Cross-provider cost precision is an open question (§15).

---

## 8. Output fields

| Field | Type | Meaning |
|---|---|---|
| `final_answer_text` | string | The agent's final answer verbatim |
| `final_answer_token_count` | int | Token count of the final answer |
| `output_language` | enum | Language of the final answer (should equal `language`; mismatch is a failure signal per rubric) |
| `answer_contains_required_facts` | bool/list | Per required fact in the expected fact-set: present or absent |
| `answer_contains_forbidden_claims` | bool/list | Whether the answer asserts facts contradicting the fact-set (hallucination check) |
| `answer_format_valid` | bool | Whether the answer meets the task's format requirements |

The three `answer_*` fields are the deterministic inputs to the success gate — they are computed against the language-neutral expected fact-set, never against an English reference answer.

---

## 9. Success evaluation fields

| Field | Type | Meaning |
|---|---|---|
| `endpoint_outcome` | enum | `PASS` / `FAIL` / `UNCERTAIN` — the binary success gate with UNCERTAIN first-class (rubric §4) |
| `quality_band` | enum | `Pass-high` / `Pass-minimal` / `Fail-recoverable` / `Fail-critical` / `Uncertain` (rubric §5; collapsed to PASS/FAIL for v0.1 metrics, logged at full granularity) |
| `failure_type` | enum | One of the nine failure types in rubric §9 (null if PASS) |
| `evaluator_type` | enum | `deterministic` / `semi-deterministic` / `human` / `llm-judge` (llm-judge not used in v0.1 per rubric §8) |
| `evaluator_notes` | string | Free-text rationale, especially for borderline cases |
| `human_review_required` | bool | Whether this run was flagged for human review (all UNCERTAIN runs, plus audit sample) |
| `human_review_outcome` | enum | Result of human review if performed (`PASS` / `FAIL` / `still-uncertain` / null) |
| `uncertainty_reason` | string | Why the evaluator could not decide (mandatory when outcome is UNCERTAIN) |

UNCERTAIN runs are never silently coerced into PASS or FAIL. They are excluded from cost-per-successful-completion and reported via `uncertainty_rate` (§10).

---

## 10. Derived metrics

Derived metrics are computed at analysis time, **not stored per row**. Most are properties of a condition (a language × agent × model cell), not of a single run.

| Metric | Level | Definition |
|---|---|---|
| `cost_per_successful_completion` | condition | Total estimated cost of all runs in the cell ÷ number of PASS runs. **Counting rule for failed-run cost is open (M6, §15)** — log everything so either rule (include/exclude failed-run cost in numerator) can be applied |
| `latency_per_successful_completion` | condition | Analogous, with total latency |
| `tokens_per_successful_completion` | condition | Analogous, with total tokens |
| `failure_rate` | condition | FAIL runs ÷ all decided runs |
| `uncertainty_rate` | condition | UNCERTAIN runs ÷ all runs — a quality signal for the evaluation procedure itself |
| `token_tax_index` | language (vs. baseline) | Ratio of representation+generation tokens per semantic unit, relative to the English condition for the same intents |
| `candidate_execution_tax_index` | condition (vs. baseline) | Ratio of non-token trajectory overhead (retrieval calls, agent steps, retries, corrections) relative to the English condition — explicitly labeled *candidate* because execution-tax is unproven |
| `residual_overhead_after_token_count_control` | condition | Overhead difference remaining after statistically controlling for input/output token counts — the closest thing to an execution-tax signal this design can produce |

**Cautions:**
- Per-run values of these metrics are mostly undefined (a single FAIL run has no cost-per-successful-completion).
- At v0.1 sample sizes (36 intents), index values are exploratory descriptions, not estimates with confidence claims (benchmark-sizing §11).
- The exact formula for the two index metrics should be fixed before analysis begins, to avoid choosing the formula that produces the most interesting number.

---

## 11. Token-tax vs execution-tax decomposition

Mapping of schema fields to the six-component decomposition (framework §7):

| Component | Closest to | Primary fields |
|---|---|---|
| **Representation overhead** | Token-tax | `user_query_token_count`, `input_character_count`, `input_word_count`, `retrieved_context_token_count` vs. `retrieved_context_semantic_units_count` |
| **Generation overhead** | Token-tax | `output_tokens`, `final_answer_token_count` (relative to required facts expressed) |
| **Retrieval overhead** | Candidate execution-tax | `retrieval_calls`, `irrelevant_retrieval_count`, `missing_required_fact_count`, `retrieval_latency_ms` — in semantic-unit terms, not raw tokens |
| **Tool overhead** | Candidate execution-tax | `tool_calls`, `estimated_tool_cost` |
| **Retry overhead** | Candidate execution-tax | `retry_count`, `fallback_used`, `error_events` |
| **Correction/evaluation overhead** | Candidate execution-tax | `human_intervention_used`, `human_review_required`, `human_review_outcome`, `validation_steps` |

**Boundary statement:** Representation and generation overhead are the components closest to established token-tax (Petrov, Ahia, Lundin). Retrieval, tool, retry, and correction overhead are *candidate* execution-tax components — they are what the NiceM hypothesis predicts may vary by language, and what this schema makes measurable. Logging them does not presume the hypothesis is true; a null result (no cross-language difference in these components after token-count control) is a legitimate and reportable outcome (framework §8 falsification criteria).

---

## 12. Minimal required fields for v0.1

The smallest set without which the pilot's core questions cannot be answered:

**Identifiers:** `run_id`, `timestamp`, `benchmark_version`, `intent_id`, `task_category`, `language`, `kb_rendering_version`, `expected_fact_set_id`, `agent_design_id`, `model_id`, `retrieval_design_id`, `evaluator_version`

**Input:** `user_query_text`, `user_query_token_count`, `tokenizer_name`

**Retrieval:** `retrieval_calls`, `retrieved_chunk_ids`, `retrieved_fact_ids`, `retrieved_context_token_count`, `retrieved_context_semantic_units_count`, `missing_required_fact_count`

**Trajectory:** `model_calls`, `tool_calls`, `agent_steps`, `retry_count`, `translation_used`, `total_latency_ms`, `error_events`

**Tokens/cost:** `input_tokens`, `output_tokens`, `total_tokens`, `estimated_total_cost`, `pricing_version`

**Output:** `final_answer_text`, `output_language`, `answer_contains_required_facts`

**Success:** `endpoint_outcome`, `failure_type`, `evaluator_type`, `uncertainty_reason` (when UNCERTAIN)

If the instrumentation platform cannot capture any field in this list, that is a blocker for the platform choice (M9), not a field to drop.

## 13. Nice-to-have fields for v0.2

Can wait without compromising the pilot:

- `planning_steps`, `validation_steps` (require step classification the v0.1 agent designs may not support)
- `billable_tokens` and per-component cost split (`estimated_retrieval_cost`, `estimated_tool_cost`) — v0.1 can run on `estimated_total_cost`
- `input_character_count`, `input_word_count` (useful for fertility analysis; recoverable post hoc from `user_query_text` if texts are stored)
- `irrelevant_retrieval_count` (recoverable post hoc from `retrieved_fact_ids` + expected fact-sets)
- `quality_band` at full granularity (v0.1 metrics collapse to PASS/FAIL anyway)
- `retrieval_notes`, `evaluator_notes` beyond UNCERTAIN cases
- Per-step (rather than per-run) token and latency attribution — valuable for v0.2 bottleneck analysis; requires span-level instrumentation (Langfuse/Phoenix candidates, M9)

## 14. Privacy and independence

- No employer data is logged or used.
- No customer data is logged or used.
- No internal/confidential data from any organization is logged or used.
- All queries, documents, facts, and answers are synthetic, invented for this benchmark about a fictional product.
- No personal data is logged. `user_query_text` contains only synthetic queries; no real names, accounts, addresses, or identifiers appear anywhere in the schema. Fictional persona details, if used in intents, must be obviously fictional.

## 15. Open questions (LG1–LG7)

| ID | Question | Status | Notes |
|---|---|---|---|
| LG1 | How precise can cost estimates be across model providers? | Open | Pricing models differ (cache discounts, batch pricing); `pricing_version` mitigates but does not solve cross-provider comparability |
| LG2 | Which tokenizer should define baseline token-tax? | Open | Same as LS4; model-native tokenizer vs. a fixed reference tokenizer give different token-tax numbers; possibly log both |
| LG3 | How should retrieval semantic units be counted? | Open | Current answer: deduplicated canonical fact IDs; edge cases (partial facts in a chunk, paraphrased facts) need a counting rule before implementation |
| LG4 | Should human correction be manually assigned or inferred? | Open | v0.1 leans manual (`human_intervention_used` set by the operator); inference from traces is a v0.2 question |
| LG5 | How should retry events be normalized across agent designs? | Open | Same as M6; one design's "retry" is another's "loop iteration"; log raw `error_events` so counting rules can be applied uniformly later |
| LG6 | Should latency include network time? | Open | Proposal: log wall-clock (`total_latency_ms`) in v0.1 and accept network noise; per-component latency split deferred to v0.2 span-level instrumentation |
| LG7 | How should failed runs affect cost-per-successful-completion? | Open | Same as M6 weighting question; the schema logs all costs for all runs so both conventions (failed-run cost included vs. excluded) can be computed and reported side by side |

---

## Dependencies and update log

| Document | What changes with this schema |
|---|---|
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 checklist: logging-schema item now has a working answer pending implementation |
| `docs/methodology/benchmark-sizing-v0.1.md` | §10 trajectory-logging row now has a concrete field specification |
| `docs/open-questions.md` | LG1–LG7 added; M6 and M9 status notes updated to reference this schema |
| `docs/source-map.md` | logging-schema-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10*
