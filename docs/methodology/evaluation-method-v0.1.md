# NiceM Evaluation Method v0.1

**Status:** Decision made — deterministic/semi-deterministic fact-set checks primary, project-owner human audit layer, LLM-as-judge optional support only
**Addresses:** M2 (human vs. automated evaluation) from `docs/open-questions.md`; the final unchecked framework §12 prerequisite
**Depends on:** `docs/methodology/success-rubric-v0.1.md`, `docs/methodology/logging-schema-v0.1.md`, `docs/methodology/falsification-and-decision-rules-v0.1.md`
**Feeds into:** Dataset construction (expected fact-set format), pilot execution, rubric calibration

**Fixed context:**
- Task family: fictional Product FAQ / Policy QA
- KB: 8 documents, ~75 canonical facts; intents: 36 × English, Dutch, Turkish
- Agent A: Direct LLM baseline; Agent B: Simple RAG
- Canonical artifact: structured fact-set; expected outcomes are language-neutral fact-sets (TF6)
- Execution-tax remains a hypothesis

---

## 1. Purpose

The evaluation method must be fixed before dataset construction and benchmark runs, for three reasons:

1. **The expected fact-set format depends on the evaluation method.** If evaluation is deterministic, expected outcomes must be authored as machine-checkable structured facts. Deciding this after the intents are written would force rework — or worse, force a retreat to subjective judging.
2. **Every downstream metric is gated by the evaluator.** Cost per successful completion only counts PASS runs; failure rates and uncertainty rates are evaluator outputs. An unreliable evaluator corrupts every number the pilot produces, including the token-tax/execution-tax comparison.
3. **Cross-language evaluator bias is the single most dangerous confound in this design** (framework §11, M3). An evaluator that judges Turkish outputs less reliably than English outputs manufactures a fake "language effect." The defenses against this — language-neutral fact checks, uncertainty tracking by language, calibration gates — must be designed in, not patched on.

## 2. Evaluation goal

The evaluator answers exactly one question per run: **does this run pass the success gate?**

- The evaluator determines PASS / FAIL / UNCERTAIN against the language-neutral expected fact-set.
- The evaluator does **not** decide whether execution-tax exists. That conclusion comes from the pre-registered falsification rules applied to trajectory and cost data across conditions.
- The evaluator judges **endpoint correctness only**. Trajectory cost (retrieval calls, retries, tokens, latency) is measured separately by the logging schema and never enters the success judgment — an expensive PASS is still a PASS; the cost shows up in the cost metrics, not the gate.

This separation (endpoint gate vs. trajectory measurement, framework §3) is what allows NiceM to say "same success, different cost" — the core comparison.

## 3. Recommended v0.1 approach

A hybrid but conservative design with three layers:

**Primary: deterministic / semi-deterministic fact-set checks.**
Every intent's expected outcome is a structured fact-set (TF6, rubric §6). The primary evaluator checks the final answer against that fact-set: required facts present, correct eligibility conclusion, no forbidden claims, format valid. These checks are language-neutral by construction — they test whether the meaning is present, not whether specific words appear.

**Audit layer: project-owner human review.**
- A sample of deterministic PASS/FAIL decisions is human-reviewed to validate the checker itself.
- All UNCERTAIN cases go to human review.
- The project owner reviews English and Dutch outputs directly (native/near-native competence, language-selection §8).
- **Turkish self-review is permitted in v0.1 because Turkish is the project owner's mother tongue** — this is an evaluator-competence fact, recorded as such. (This supersedes the more conservative assumption in language-selection §8 that the owner could only "inspect" Turkish; the bilingual-review requirement for the *KB renderings* still stands as a quality gate, but run-level evaluation can be owner-performed.)
- **Independent bilingual review is recommended before any public or publication-grade claim.** Self-review is acceptable for an internal exploratory pilot; it is not sufficient for claims made to others, because a single evaluator who is also the project's author carries a motivated-reasoning risk that no protocol fully removes.

**LLM-as-judge: optional support only.**
Permitted for triage and consistency checking; never the sole source of truth for any run in v0.1; cross-language judge bias is documented as the key risk (§10; `docs/sources/agent-evals/agent-as-a-judge.md`).

## 4. Evaluation inputs

The evaluator (deterministic checker or human) receives, per run:

| Input | Purpose |
|---|---|
| `intent_id` | Which intent this run executed |
| `language` | The language condition |
| User query text | What was asked |
| Final answer text | What is being judged |
| `expected_fact_set_id` + expected required facts/actions | The language-neutral correctness target |
| Forbidden claims (if defined for this intent) | Hallucination check targets |
| Output format requirements (if any) | Format validity check |
| Retrieved facts/chunks | **Optional, error analysis only** — the endpoint judgment must not depend on how the answer was produced; retrieval data is consulted only when classifying *why* a FAIL occurred (failure_type), never to upgrade or downgrade the endpoint outcome |

The evaluator does **not** receive cost, latency, token counts, or the agent design identifier where avoidable — endpoint judgment should be blind to trajectory expense, and ideally blind to condition, to prevent expectation bias.

## 5. PASS criteria

A run is PASS if **all** of the following hold (operationalizing rubric §4's necessary conditions):

1. All required facts/actions from the expected fact-set are present in the final answer.
2. No critical factual error is present (no statement contradicting the canonical fact-set on a point material to the intent).
3. The intended task is completed — the question asked is the question answered.
4. Meaning is preserved — the answer expresses the required facts accurately in the run's language; wording, order, and style are free.
5. The output is usable — a customer reading it would receive the correct policy answer without needing to guess or re-ask.

## 6. FAIL criteria

A run is FAIL if **any** necessary condition is violated, including:

- A required fact or action is missing.
- The policy conclusion is wrong (e.g., "covered" when the fact-set says not covered).
- A forbidden claim is asserted (hallucinated policy, invented clause, fabricated product feature).
- The response is unsafe, off-task, or irrelevant to the intent.
- The output is unusable (wrong language, incomprehensible, empty, or format-invalid where format is required).

The failure is classified into one of the nine failure types (rubric §9) and logged as `failure_type`. FAIL decisions always record *which* condition was violated — an unexplained FAIL is a logging defect.

## 7. UNCERTAIN criteria

A run is UNCERTAIN if the evaluator cannot confidently determine PASS or FAIL, due to:

- Ambiguity in the answer (it can be read as correct or incorrect).
- Unclear or garbled output that is not clearly unusable.
- Translation/meaning uncertainty — the evaluator cannot confidently judge whether a phrasing in the run's language expresses the required fact.
- Incomplete evidence (e.g., a logging gap truncated the final answer).
- Evaluator limitation — the evaluator recognizes the judgment exceeds their confidence.

`uncertainty_reason` is mandatory for every UNCERTAIN outcome (logging-schema §9).

**UNCERTAIN is a measurement/calibration signal, not proof of language failure.** A high Turkish uncertainty rate means the rubric, the fact-sets, or the evaluator need calibration for Turkish — it must never be reported as "Turkish performs worse." This boundary is enforced by the falsification rules (§13 below).

## 8. Human review policy

| Situation | Policy |
|---|---|
| UNCERTAIN outcome from deterministic check | **Mandatory human review**, every case |
| FAIL outcome | Review strongly recommended for all FAILs in v0.1 (n is small enough); at minimum every FAIL that drives a cross-language gap, since failure-rate gaps trigger the falsification §7 failure-analysis threshold |
| PASS outcome | **Sampled review** — a fixed audit fraction per language condition, drawn before results are analyzed (sampling rate is EV1, open) |
| Checker validation | Before the full run, the deterministic checker's decisions on the smoke-test outputs are human-verified end to end |

**Labeling:** every human review is logged with `evaluator_type` = `human`, plus a reviewer identifier in `evaluator_notes` (`project-owner` in v0.1). Reviews that overturn the deterministic checker are explicitly flagged — a high overturn rate means the checker, not the runs, needs fixing.

**Turkish self-review:** performed by the project owner as a native speaker; labeled identically to English/Dutch reviews. The limitation — single non-independent evaluator — applies to all three languages equally, which is itself a fairness property: no language gets a *different* evaluator in v0.1.

**Independent review for public claims:** before any result is shared beyond the project (publication, pitch, public post), an independent bilingual reviewer should re-judge a sample spanning all languages and both agent designs. Until then, claims are limited accordingly (EV7).

**Disagreements:** if human review and the deterministic check disagree, the human decision becomes `human_review_outcome`, the original stays in `endpoint_outcome`'s history via the checker record, and the disagreement is logged in `evaluator_notes`. If the project owner is uncertain after review, the run stays UNCERTAIN — uncertainty is never resolved by coin-flip or by defaulting to PASS.

## 9. Multilingual fairness rules

1. **Judge meaning and correctness, not style.** Sentence structure, formality, length, and idiom are not scored.
2. **No English wording as hidden target.** The correctness target is the structured fact-set; there is no reference answer text in any language, including English (BT3).
3. **Expected outcomes are language-neutral facts/actions.** A Turkish answer expressing `{covered: false, reason: liquid-damage-exclusion}` in any natural phrasing passes the same check as an English one.
4. **No penalty for valid linguistic variation.** Morphological richness, different information order, or culturally normal phrasing differences are never failure grounds.
5. **Track uncertainty rate by language.** `uncertainty_rate` per language condition is a first-class quality metric of the *evaluation procedure*.
6. **Recalibrate before interpreting.** If uncertainty is materially higher in one language (falsification §7: >25% in any condition), the rubric and fact-sets are recalibrated for that language **before** any execution-tax interpretation proceeds. An uneven uncertainty rate is treated as an instrument defect until shown otherwise.

## 10. LLM-as-judge policy

- **Permitted uses in v0.1:** triage (pre-sorting likely-PASS vs. likely-FAIL to prioritize human attention), consistency checks (flagging runs where the deterministic check and an LLM judgment disagree), and drafting failure-type classifications for human confirmation.
- **Prohibited use in v0.1:** being the sole source of truth for any run's `endpoint_outcome`. Every outcome traces to a deterministic check, a human review, or both.
- **If used, log:** the judge's `model_id`, `prompt_version`, `evaluator_version`, and the `language` of the judged output — without these, judge behavior cannot be audited.
- **Risk posture:** LLM judges may be less reliable on Turkish than English outputs (`docs/sources/agent-evals/agent-as-a-judge.md`). An LLM judge whose agreement with human review differs by language is itself exhibiting the kind of language-sensitive behavior NiceM studies — interesting, but disqualifying for judging. Cross-language judge reliability must be validated (human-scored subset spanning all languages) before any v0.2 promotion of the judge to a primary role.

## 11. Deterministic fact-set checks

The Product FAQ / Policy QA task family was chosen partly because it admits deterministic checks (task-family-selection; rubric §8). For each intent, the expected fact-set makes the following machine-checkable or near-machine-checkable:

- **Required facts present** — each fact in the expected set is expressed in the answer (matching on meaning; for v0.1's short policy answers this is largely decidable from key values: dates, day-counts, plan names, yes/no eligibility).
- **Correct eligibility decision** — the answer's bottom-line conclusion (covered / not covered, eligible / not eligible) matches the fact-set's decision field. This is the most deterministic check and the most important one.
- **Correct condition applied** — for conditional intents, the answer invokes the right condition (e.g., the 30-day window, not the 14-day window).
- **No forbidden claim** — none of the intent's listed forbidden claims appear.
- **Output format valid** — where the intent requires a format (e.g., a step list for troubleshooting), it is present.

"Semi-deterministic" acknowledges honestly that fact-presence in free text requires some matching tolerance (paraphrase, morphology). Matching rules must be written per fact type before the run, applied identically across languages, and validated against the smoke-test outputs (tokenizer-model-choice §5 Stage 2). Where matching confidence is low, the checker outputs UNCERTAIN rather than guessing — routing the case to human review by design.

## 12. Relationship to logging schema

| Evaluation output | Logging field (logging-schema §9) |
|---|---|
| Gate decision | `endpoint_outcome` (PASS / FAIL / UNCERTAIN) |
| Granular quality | `quality_band` (logged at full granularity; collapsed to PASS/FAIL for v0.1 metrics) |
| Why it failed | `failure_type` (one of nine rubric types; null on PASS) |
| Who/what judged | `evaluator_type` (`deterministic` / `semi-deterministic` / `human`; `llm-judge` only as secondary annotation in v0.1) |
| Rationale | `evaluator_notes` (mandatory for borderline cases, overturns, and all human reviews) |
| Review routing | `human_review_required` (true for all UNCERTAIN + audit sample) |
| Review result | `human_review_outcome` (PASS / FAIL / still-uncertain / null) |
| Why undecidable | `uncertainty_reason` (mandatory when UNCERTAIN) |

No schema change is required — the schema anticipated this method.

## 13. Relationship to falsification rules

The evaluation method is the load-bearing wall under the falsification rules:

- **A result cannot support or weaken the execution-tax hypothesis unless endpoint evaluation is reliable.** Cross-language cost-per-successful-completion comparisons presuppose that PASS means the same thing in every language.
- **High uncertainty triggers inconclusive status, not H0 or H1.** Falsification §5 already lists >25% UNCERTAIN in any condition as an inconclusiveness condition; this document supplies the mechanism (recalibrate rubric/fact-sets, re-evaluate, only then analyze).
- **Biased judging triggers inconclusive status too.** If the audit layer reveals that the deterministic checker's human-overturn rate differs materially by language, the affected conditions are inconclusive until the checker is fixed — the difference is an instrument artifact, not evidence.
- **Failure-rate gaps route through failure analysis first.** Falsification §7's failure-rate threshold (>20pp gap) requires failure-type analysis before cost interpretation; the `failure_type` classifications this method produces are what make that analysis possible.

## 14. Minimum v0.1 evaluation procedure

1. **Run the deterministic/semi-deterministic fact-set check** on every run's final answer, producing a provisional PASS / FAIL / UNCERTAIN with `evaluator_type` = `deterministic` or `semi-deterministic`.
2. **Accept clear decisions:** checker-confident PASS and FAIL outcomes stand, subject to the audit sample.
3. **Route to human review:** all UNCERTAIN cases (mandatory), all FAILs (recommended at v0.1 scale), and the pre-committed audit sample of PASSes per language condition. Human outcomes recorded in `human_review_outcome`; overturns flagged.
4. **Track uncertainty and overturn rates by language** throughout — not only at the end — so a calibration problem is caught after the first runs, not after the full budget is spent.
5. **Gate the analysis:** if uncertainty exceeds the falsification threshold in any condition, or overturn rates differ materially by language, stop — recalibrate the rubric/fact-sets/checker, re-evaluate affected runs, and only then proceed to cost and trajectory interpretation. **Do not interpret cost metrics over an evaluation layer known to be unreliable.**

## 15. Open questions (EV1–EV7)

| ID | Question | Status | Notes |
|---|---|---|---|
| EV1 | What percentage of outputs should receive human review? | Open — audit fraction must be fixed before analysis | At v0.1 scale (108–324 runs), reviewing all FAILs + all UNCERTAINs + ~20% of PASSes per condition looks feasible; confirm against BS5 (review capacity) |
| EV2 | Should all Turkish outputs be reviewed by the project owner in v0.1? | Open, leaning yes at base scale | 36–108 Turkish runs is reviewable; full review of the highest-risk condition would also calibrate the checker's Turkish matching rules |
| EV3 | Should all FAIL and UNCERTAIN cases be reviewed? | UNCERTAIN: yes (mandatory). FAIL: leaning yes at v0.1 scale | Becomes a sampling question only at v0.2 scale |
| EV4 | Should LLM-as-judge be used at all in v0.1? | Open, leaning minimal | Triage value is modest at this scale; the cross-language bias risk and added moving parts may outweigh it; decide at implementation |
| EV5 | How should partial success be handled? | Direction set — no partial credit at the gate | The binary gate stands (rubric §4); partial information is preserved in `quality_band` and `failure_type` (Fail-recoverable vs. Fail-critical) for analysis, but cost-per-successful-completion counts only PASS |
| EV6 | What evaluator agreement threshold is needed for v0.2? | Open | Requires a second rater; define inter-rater agreement (e.g., on a shared sample) before v0.2 scales up or promotes an LLM judge |
| EV7 | How should public claims be limited without independent review? | Open — interim rule | Until independent bilingual review exists: all externally shared results carry the label "single-evaluator exploratory pilot; independent review pending," in addition to the standard scope limits (falsification §9) |

---

## Dependencies and update log

| Document | What changes with this decision |
|---|---|
| `docs/methodology/success-rubric-v0.1.md` | §7/§8 evaluation-method comparison now resolved into a concrete v0.1 procedure; pointer added |
| `docs/methodology/nicem-methodology-framework-v0.1.md` | Final §12 item (human vs. automated evaluation) checked off — the §12 pre-validation checklist is now fully addressed at the methodology level |
| `docs/methodology/falsification-and-decision-rules-v0.1.md` | No rule changes; §5/§7 uncertainty and failure-analysis conditions now have their operational mechanism here |
| `docs/methodology/logging-schema-v0.1.md` | No schema change — §9 fields map one-to-one to this method |
| `docs/open-questions.md` | M2 resolved; M3 status updated (mechanism now defined, validation pending); EV1–EV7 added |
| `docs/source-map.md` | evaluation-method-v0.1.md added to related internal documents |

---

*v0.1 — 2026-06-10*
