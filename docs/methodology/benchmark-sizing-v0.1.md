# NiceM Benchmark Sizing v0.1

**Status:** Decision made — Small KB (Option B) + small validation set (Option B), with a concrete minimum viable benchmark proposal
**Addresses:** TF1 (KB size) and TF2 (task instance count) from `docs/open-questions.md`
**Depends on:** `docs/methodology/task-family-selection-v0.1.md`, `docs/methodology/retrieval-design-decision-v0.1.md`, `docs/methodology/language-selection-v0.1.md`, `docs/methodology/success-rubric-v0.1.md`
**Feeds into:** Dataset construction, M8 (statistical power), pilot run budgeting

**Fixed context for this decision:**
- Task family: fictional Product FAQ / Policy QA (synthetic, controlled)
- Retrieval design: language-matched retrieval (Option A from retrieval-design-decision-v0.1)
- Languages: English, Dutch, Turkish
- Canonical artifact: structured fact-set, not English prose
- Success evaluation: language-neutral expected fact-set, binary PASS/FAIL gate with UNCERTAIN as first-class outcome
- Execution-tax remains a hypothesis — this benchmark exists to test it, not to demonstrate it

---

## 1. Purpose

KB size and task instance count must be decided before any benchmark is built, because they determine:

- **Whether retrieval behavior exists at all.** A KB so small that every document fits in context makes retrieval trivial; trajectory metrics like retrieval_call_count carry no signal.
- **Whether the KB quality-control gate is achievable.** Every fact in every language rendering must pass bilingual review and a pre-run completeness check (retrieval-design-decision §4). KB size multiplies this burden by three language conditions.
- **Whether failure patterns are observable.** Too few task instances and a single anomalous run dominates the results; differences across languages cannot be distinguished from noise.
- **Whether results can be honestly interpreted.** Sizing determines in advance what claims the v0.1 results can and cannot support. Deciding this now prevents post-hoc overclaiming.

Sizing errors are expensive in both directions: too large, and the quality-control prerequisite becomes infeasible (forcing the Turkish fallback or KB shortcuts that introduce confounds); too small, and the entire run produces no interpretable signal.

---

## 2. Sizing principles

The v0.1 benchmark must be:

1. **Small enough to manually inspect.** Every document, every fact, and every expected answer in every language must be human-reviewable before the run. If full manual inspection is infeasible, the benchmark is too large for v0.1.
2. **Large enough to produce retrieval behavior.** The KB must exceed what trivially fits in a single retrieval result, so that retrieval calls, misses, and retries are possible and measurable.
3. **Varied enough to avoid one-off artifacts.** Multiple task categories and difficulty levels, so that a result is not an artifact of one document or one question style.
4. **Structured enough to compare across languages.** Every intent appears in all three language conditions, rendered from the same fact-set, so per-intent cross-language comparison is possible.
5. **Synthetic and controlled.** No employer data, no customer data, no internal workflows, no confidential information. A fictional product (e.g., a fictional smart-home device line) with invented policies.
6. **Suitable for v0.1 validation, not publication-grade claims.** The sizing target is "can we observe whether trajectory differences exist," not "can we estimate effect sizes with confidence intervals suitable for publication."

---

## 3. Knowledge base size options

### Option A — Tiny KB (3–5 documents, 20–40 canonical facts)

| Dimension | Assessment |
|---|---|
| Retrieval richness | Poor — with 3–5 documents, top-k retrieval almost always includes the right document by chance; retrieval_call_count and retrieval misses carry little signal |
| Manual review burden | Very low — fully reviewable in hours per language |
| Translation/rendering burden | Very low — three renderings feasible quickly |
| Risk of trivial retrieval | **High** — the central weakness; an agent could plausibly stuff the entire KB into context, eliminating retrieval as a measured behavior |
| Risk of too much noise | Low at KB level, but trivial retrieval makes trajectory metrics degenerate |
| Suitability for v0.1 | **Not suitable as primary** — useful only as a dry-run smoke test of the pipeline before the real KB is built |

### Option B — Small KB (6–10 documents, 50–100 canonical facts)

| Dimension | Assessment |
|---|---|
| Retrieval richness | Adequate — enough documents that retrieving the correct chunk is non-trivial; conditional intents requiring facts from two documents are possible |
| Manual review burden | Manageable — roughly 1–2 days of careful review per language rendering; full fact-by-fact completeness check remains feasible |
| Translation/rendering burden | Manageable — three renderings of 6–10 documents is realistic for the project owner plus one Turkish bilingual reviewer |
| Risk of trivial retrieval | Moderate — must be mitigated by chunking design and by intents that require specific facts, not document gist |
| Risk of too much noise | Low — small enough that retrieval failures can be traced to specific KB gaps during error analysis |
| Suitability for v0.1 | **Suitable** — the practical sweet spot between measurable retrieval behavior and achievable quality control |

### Option C — Medium KB (15–25 documents, 150–300 canonical facts)

| Dimension | Assessment |
|---|---|
| Retrieval richness | Good — realistic retrieval difficulty, distractor documents, harder conditional intents |
| Manual review burden | **High** — 150–300 facts × 3 languages = 450–900 fact-rendering reviews; the bilingual completeness check for Turkish becomes a multi-week task |
| Translation/rendering burden | High — likely forces machine-translation-then-review shortcuts, which retrieval-design-decision §4 flags as a quality risk |
| Risk of trivial retrieval | Low |
| Risk of too much noise | Moderate — with this many documents, retrieval failures become harder to attribute to language vs. KB authoring inconsistencies |
| Suitability for v0.1 | **Not suitable for v0.1** — the quality-control prerequisite is the binding constraint; appropriate for v0.2 once authoring and review processes are proven |

**Conclusion:** Option B. The binding constraint is the KB quality-control gate (a hard prerequisite from retrieval-design-decision-v0.1), not retrieval realism. Option B is the largest KB for which full manual inspection across three languages remains honest rather than aspirational.

---

## 4. Task instance count options

"Intent" here means one unique human intent (e.g., "is my device still under warranty given purchase date X and defect type Y"), rendered once per language. "Task instance" means one intent × one language condition.

### Option A — Very small pilot (10–15 intents per language)

| Dimension | Assessment |
|---|---|
| Ability to observe failure patterns | Weak — with ~10 intents, two or three failures in one language could be one bad intent, not a language effect |
| Cost and runtime | Minimal — 30–45 task instances total; runnable in a single session |
| Statistical usefulness | Near zero — no meaningful per-category breakdown possible |
| Human review burden | Trivial |
| Risk of overinterpreting results | **High** — small samples invite seeing patterns in noise |
| Suitability for v0.1 | Not suitable as the validation set — useful as a pipeline smoke test alongside the Tiny KB dry run |

### Option B — Small validation set (30–50 intents per language)

| Dimension | Assessment |
|---|---|
| Ability to observe failure patterns | Adequate for exploration — failures can be grouped by task category and difficulty; recurring per-language patterns become distinguishable from one-off anomalies |
| Cost and runtime | Modest — 90–150 task instances; with 2–3 repetitions, roughly 200–450 runs; affordable for a self-funded pilot |
| Statistical usefulness | Limited but honest — enough to estimate variance for the M8 power calculation, not enough to confirm effects |
| Human review burden | Manageable — every UNCERTAIN and every audited PASS/FAIL can still be human-reviewed |
| Risk of overinterpreting results | Moderate — must be controlled by the reporting boundaries in §11 |
| Suitability for v0.1 | **Suitable** — large enough to see patterns, small enough to fully review |

### Option C — Larger exploratory set (100+ intents per language)

| Dimension | Assessment |
|---|---|
| Ability to observe failure patterns | Good — per-category and per-difficulty breakdowns become robust |
| Cost and runtime | Significant — 300+ task instances; with repetitions, 600–1,000+ runs; cost and runtime become real constraints |
| Statistical usefulness | Better — approaches what a pre-registered effect test would need, but the right sample size cannot be known before pilot variance estimates exist (M8) |
| Human review burden | **High** — full human review of borderline cases becomes infeasible; would force reliance on automated judging that is not yet cross-language validated (M3) |
| Risk of overinterpreting results | Lower statistically, but higher operationally — the temptation to present results as confirmatory grows with sample size |
| Suitability for v0.1 | Not suitable — sizing a confirmatory study before variance is known wastes budget; defer to v0.2 informed by v0.1 variance |

**Conclusion:** Option B. Authoring 100+ good intents before knowing the per-intent variance is premature; 30–50 intents is the smallest set that produces variance estimates useful for the M8 power calculation.

---

## 5. Recommended v0.1 sizing

**Knowledge base: Small KB (Option B)**
- 6–10 synthetic policy/FAQ documents about a fictional product
- 50–100 canonical facts in the structured fact-set
- Three language renderings (English, Dutch, Turkish), each authored from the fact-set, each passing bilingual review and the pre-run completeness check

**Task instances: small validation set (Option B)**
- 30–50 unique intents
- Each intent rendered in English, Dutch, and Turkish (from the intent's fact-level specification, not translated from English prose)
- Each intent paired with one language-neutral expected fact-set

**Framing:** This is exploratory validation. Its purpose is to (a) test whether the pipeline works end to end, (b) produce first trajectory-difference observations across language conditions, and (c) generate the variance estimates that M8 needs. It is not a publication-grade benchmark and its results must not be presented as one.

---

## 6. Task categories

Candidate policy/FAQ categories for the fictional product KB (each maps to roughly one document):

| Category | Example intent type |
|---|---|
| Warranty eligibility | Is a device with purchase date X and defect Y covered? |
| Return eligibility | Can an item bought N days ago in condition Z be returned? |
| Subscription plan rules | Does plan A include feature B? What happens on downgrade? |
| Troubleshooting steps | What is the prescribed first step for symptom X? |
| Shipping or delivery rules | What is the delivery window for region/option X? |
| Repair/replacement policy | When is repair offered vs. full replacement? |
| Account access or device reset policy | What is required to reset a device or recover an account? |

Seven categories × one document each, plus one general-terms document, lands inside the 6–10 document range. The five task skeletons T1–T5 from task-family-selection-v0.1 map onto these categories (T1 warranty, T2 plan eligibility, T3 troubleshooting, T4 return eligibility, T5 feature lookup).

---

## 7. Intent design principles

1. **One expected fact-set per intent.** Every intent has exactly one language-neutral expected fact-set against which PASS/FAIL is judged (rubric §6, TF6).
2. **Graded fact requirements.** Some intents require a single fact (simple lookup); some require combining two or more conditions (e.g., warranty period AND defect type AND proof-of-purchase rule). Both must be present so trajectory differences can be related to reasoning load.
3. **No ambiguous wording.** If two careful readers could reasonably expect different fact-sets, the intent is rewritten or dropped.
4. **No cultural assumptions.** Intents must not depend on region-specific norms, holidays, currencies-as-knowledge, or idioms that render unevenly across English, Dutch, and Turkish.
5. **No open-ended advice.** "What should I do about my device?" is excluded; "what does the policy prescribe for symptom X?" is included. Open-ended tasks were already excluded at task-family selection.
6. **Checkable outputs.** Every expected answer must be verifiable against the fact-set deterministically or near-deterministically, without a language-sensitive judge.
7. **Mix of simple and conditional questions.** The intent set should be roughly balanced between single-fact and multi-condition intents, with the balance recorded per intent so results can be broken down by difficulty (see open question BS3).

---

## 8. Relationship to retrieval

- **The KB must make retrieval non-trivial.** With 6–10 documents chunked into sections, top-k retrieval can return wrong or partial chunks — which is precisely the behavior (retrieval calls, misses, retries) that execution-tax measurement needs to observe.
- **Tasks must require retrieval, not model memory.** Because the product and its policies are fictional and invented for this benchmark, the model cannot answer from pretraining. This is a deliberate design property, not a side effect — it guarantees that correct answers route through retrieval.
- **Expected answers live outside the prose KB.** Expected fact-sets are stored as a separate structured artifact (per TF6), never embedded in the documents the agent retrieves. Otherwise the success check could be gamed by verbatim retrieval.
- **Retrieval quality is checked in semantic units, not only tokens.** Per retrieval-design-decision §8, retrieval_tokens must be dual-reported (raw tokens and facts/semantic units retrieved). A Turkish chunk with more tokens is not "worse retrieval" — that is token-tax, and conflating it with retrieval quality would double-count.

---

## 9. Relationship to statistical power

v0.1 is exploratory. **M8 — the formal power calculation — remains unresolved**, and it cannot be resolved honestly before this pilot, because a power calculation requires variance estimates that do not yet exist:

- per-intent variance in trajectory metrics (run-to-run nondeterminism)
- between-intent variance within a language condition
- a plausible effect-size range for cross-language trajectory differences

The v0.1 run produces these estimates as a primary deliverable. Until then:

- Do not compute or report p-values as if the study were confirmatory.
- Do not present cross-language differences from this sample as proof of execution-tax.
- Do report observed distributions, variance estimates, and qualitative failure patterns — these are the legitimate outputs of an exploratory pilot.

---

## 10. Minimum viable benchmark proposal

A concrete sizing plan within the recommended ranges. This is a sizing specification, not a dataset — no documents, facts, or intents are authored yet.

| Component | Size | Notes |
|---|---|---|
| Synthetic documents | 8 | Covering the seven categories in §6 plus one general-terms document |
| Canonical facts | ~75 | In the structured fact-set; roughly 8–12 facts per document |
| Unique intents | 36 | Spread across categories; mix of single-fact and multi-condition per §7 |
| Languages | 3 | English, Dutch, Turkish |
| Language-condition task instances | 108 | 36 intents × 3 languages |
| Repetitions per condition | 2–3, only if cost allows | Repetitions capture run-to-run nondeterminism; if budget forces a choice, prefer 36 intents × 1 run over 18 intents × 2 runs (between-intent variance is the scarcer information) |
| Total runs | 108–324 | Depending on repetitions |
| Success logging | PASS / FAIL / UNCERTAIN per run | Per success-rubric-v0.1; UNCERTAIN is first-class, never silently coerced |
| Trajectory logging | Full metric set per run | All trajectory metrics from framework §6, including the six-component token-tax/execution-tax decomposition inputs |

If the Turkish bilingual review prerequisite cannot be met (language-selection §8 fallback), the same plan runs as 36 intents × 2 languages = 72 task instances.

---

## 11. Reporting boundaries

Results from a benchmark of this size are valid only within the following limits:

- They can **suggest patterns**: e.g., "in this setup, Turkish conditions showed more retrieval retries than English conditions on multi-condition intents."
- They can **calibrate the next study**: variance estimates feed M8; failure patterns feed intent and KB design for v0.2.
- They **cannot prove universal language-level effects**. 36 intents on one fictional KB, one task family, one retrieval architecture, and one (to-be-chosen) model do not generalize to languages, task families, architectures, or models not tested.
- They **cannot confirm or refute the execution-tax hypothesis**. At best they show whether the hypothesized trajectory differences are observable and large enough to justify a properly powered v0.2 study.

All v0.1 reporting must carry these boundaries explicitly, consistent with language-selection §9 and the project-wide rule against overclaiming.

---

## 12. Open questions (BS1–BS7)

| ID | Question | Status | Notes |
|---|---|---|---|
| BS1 | Is 36 intents enough to observe trajectory differences? | Open | Answered empirically by the pilot itself; if observed variance swamps between-language differences, v0.2 needs more intents or repetitions |
| BS2 | How many repetitions are needed per intent/language? | Open | Depends on run-to-run nondeterminism, unknown until first runs; 2–3 is a budget-bounded starting point |
| BS3 | Should simple and conditional tasks be balanced 50/50, or weighted? | Open | Affects whether difficulty-stratified analysis is possible at n=36 |
| BS4 | How many facts per document are ideal? | Open | ~8–12 assumed in §10; too few makes retrieval trivial per document, too many makes chunks noisy |
| BS5 | How much manual review is feasible for the project owner plus one Turkish reviewer? | Open | Bounds the real upper limit of KB and intent counts; should be estimated before authoring begins (relates to LS1) |
| BS6 | What budget is acceptable for pilot runs? | Open | Determines repetition count (BS2) and model choice (LS4) |
| BS7 | What variance estimate does M8 need, and does this pilot produce it? | Open | The pilot is designed to produce per-intent and between-intent variance estimates; whether they suffice for a formal power calculation is checked after the pilot |

---

## Dependencies and update log

| Document | What changes with this decision |
|---|---|
| `docs/open-questions.md` | TF1 and TF2 updated from Open to Decision made (exploratory); BS1–BS7 added |
| `docs/source-map.md` | benchmark-sizing-v0.1.md added to related internal documents |
| `docs/methodology/task-family-selection-v0.1.md` | TF1/TF2 entries point here |
| `docs/methodology/language-selection-v0.1.md` | No change required — sizing is consistent with its quality-control requirements and Turkish fallback |
| `docs/methodology/nicem-methodology-framework-v0.1.md` | §12 pre-validation checklist: KB-size and instance-count items now have a working answer pending dataset construction |

---

*v0.1 — 2026-06-10*
