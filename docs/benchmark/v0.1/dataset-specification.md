# NiceM Dataset Specification v0.1

**Status:** Specification complete — no benchmark artifacts created yet
**Role:** Defines the structure, constraints, and authoring rules for all v0.1 benchmark artifacts before any of them are created
**Feeds into:** `canonical-fact-set.md`, `document-plan.md`, `intent-set.md`, `language-rendering-plan.md`, `expected-fact-mapping.md`, `quality-gates.md`
**Depends on:** All twelve methodology documents; directly references `benchmark-sizing-v0.1.md`, `language-selection-v0.1.md`, `retrieval-design-decision-v0.1.md`, `evaluation-method-v0.1.md`, `validation-plan-v0.1.md`

---

## 1. Purpose

Dataset specification comes before creating the canonical fact-set for the same reason the fact-set comes before KB renderings: downstream artifacts should be derived from upstream ones, never the reverse. If authoring conventions, field schemas, or language rendering rules are defined only after some facts have been written, the early facts may violate conventions that were not yet established — requiring either retroactive fixes or rule exceptions that will accumulate.

This document defines:
- the fictional product domain and the eight synthetic documents
- the schema for every canonical fact and every intent specification
- the language rendering rules that govern how fact-set content becomes KB prose
- the expected answer design that governs how evaluation works
- the difficulty distribution, retrieval implications, and quality gates
- the versioning scheme

It does not create any facts, documents, intents, or language renderings. Those artifacts come after this specification is reviewed and accepted.

The governing principle: **format before content**. Once this specification is stable, every subsequent artifact can be reviewed against a shared standard. Ambiguities in the spec should be resolved here, not in the artifacts.

---

## 2. Dataset principles

The following principles apply to every artifact in the v0.1 benchmark. They are non-negotiable constraints, not guidelines.

**Synthetic only.** No fact in the canonical fact-set may be derived from real product documentation, real customer interactions, real support tickets, employer data, customer data, or any confidential or proprietary source. All content is invented.

**Neutral fictional product domain.** The product domain must be unfamiliar enough that no language rendering can be considered more "canonical" than another by virtue of real-world familiarity. Smart-home products are familiar as a category but the specific fictional brand (NiceHome) has no real-world equivalent that could privilege one language group.

**No employer, customer, or internal data.** This is an independent personal research project. No ServiceDesk workflows, internal policies, or customer scenarios from any employer may appear in any form, even as inspiration for scenario wording.

**No hidden English canonical source.** The canonical artifact is the structured fact-set — a language-neutral, structured representation of knowledge. The English KB rendering is authored *from* the fact-set, at the same level as the Dutch and Turkish renderings. No fact should be written in English prose first and then "translated into the fact-set." The authoring direction is always: fact-set → rendering, for every language including English.

**Structured fact-set is canonical.** If there is ever a conflict between what a KB rendering says and what the canonical fact-set says, the fact-set governs. Renderings are representations of the fact-set, not authoritative sources.

**Every language rendering must be authored from the structured fact-set.** No language rendering should be authored by translating another rendering. Dutch should not be a translation of the English document. Turkish should not be a translation of Dutch. Each rendering is independently constructed from the fact-set, using the controlled terminology established in `language-rendering-plan.md` (to be created).

**Expected answers are fact/action-based, not reference-sentence-based.** The expected outcome for each intent is expressed as a set of required fact IDs (or the semantic content of those facts), not as a reference answer string. A correct response that uses different wording but conveys the required facts passes. An incorrect response that uses the exact wording of the fact but omits a required condition fails.

**Designed for exploratory validation, not publication-grade claims.** The v0.1 benchmark is a single-evaluator exploratory pilot. Results carry the label "single-evaluator exploratory pilot; independent review pending" when shared externally. This constraint does not limit the rigor of the benchmark's construction; it limits the strength of the claims made from the results.

---

## 3. Fictional product domain

### Domain definition

The v0.1 benchmark uses a fictional smart-home device ecosystem: **NiceHome**.

The NiceHome product line consists of four fictional devices:

| Product | Description |
|---|---|
| NiceHome Hub | Central control device; manages connected devices, firmware updates, and user accounts |
| NiceHome Sensor | Multi-purpose environmental sensor; temperature, humidity, motion |
| NiceHome Plug | Smart power outlet; remote switching, energy monitoring |
| NiceHome Camera | Indoor security camera; motion alerts, live view |

All four devices are manufactured and sold by the fictional company **NiceHome** (no connection to the NiceM research project itself — the brand name is chosen to be recognizable within this benchmark's internal world only; see DS1 in §14 for the naming question).

### Why this domain works

**Familiar enough for realistic questions.** Smart-home products are widely understood. Users can formulate realistic support questions about warranty coverage, how to return a device, what a subscription includes, how to reset a device — without requiring domain-specific expertise. This means synthetic intents can be natural-sounding, and evaluators can assess them without training.

**Neutral and non-employer-related.** The domain has no connection to any real workplace, support system, or proprietary product line. It is safe to use under the independence rules in `CLAUDE.md`.

**Supports the required policy types.** The eight planned synthetic documents (§4) map naturally onto this domain: warranty, returns, subscriptions, shipping, troubleshooting, and account/device reset policies are all plausible for a consumer electronics ecosystem. Each document type supports different task categories and fact types.

**Low safety risk.** Smart-home device policies do not involve medical, legal, financial, or safety-critical advice. This keeps the benchmark's risk profile low and the evaluation straightforward: correctness is about policy facts, not about harm potential.

**Easy to create deterministic expected fact-sets.** Policy documents have clearly defined conditions and outcomes ("if the device was purchased within 30 days and is unopened, then the customer is entitled to a full refund"). These map cleanly to structured facts with explicit condition fields, making language-neutral evaluation possible without subjective judgment.

---

## 4. Synthetic document set

The benchmark KB consists of eight synthetic documents. Each is authored from the canonical fact-set once the fact-set is complete. The estimates below guide fact-set authoring but are not hard constraints.

---

### Document 1: Product overview and device compatibility

**Purpose:** Introduce the four NiceHome devices, their key features, and which devices are compatible with each other and with third-party platforms.

**Expected fact types:**
- Feature descriptions per device
- Compatibility rules (which devices work together, what hubs are required)
- Version or generation conditions (if applicable)
- Limitations or exclusions

**Estimated canonical facts:** 10–12

**Task categories supported:** T1 (simple factual lookup), T2 (conditional lookup with compatibility conditions)

**Risks and ambiguity to avoid:**
- Do not define technical specifications that require arithmetic (e.g., exact power consumption, frequency bands) — these create arithmetic noise in evaluation
- Do not introduce version numbers unless compatibility rules genuinely depend on them; if used, keep the version scheme simple (e.g., Gen 1 / Gen 2 only)
- Avoid describing future products or roadmap items

---

### Document 2: Warranty policy

**Purpose:** Define warranty coverage terms for each NiceHome device, including coverage period, what is and is not covered, and the claim process.

**Expected fact types:**
- Coverage period per device (or device class)
- Covered failure types
- Excluded failure types (accidental damage, misuse, unauthorized modification)
- Claim procedure steps
- Required documentation

**Estimated canonical facts:** 8–10

**Task categories supported:** T2 (conditional policy), T3 (multi-step process)

**Risks and ambiguity to avoid:**
- Do not create overlapping coverage periods that require date arithmetic — use relative periods ("within 2 years of purchase") and note that evaluation will check for the correct period, not compute an expiry date
- Avoid conditional stacking more than two levels deep in any single fact (e.g., "if X and Y and Z, then...") — these are hard to render consistently across languages

---

### Document 3: Return and refund policy

**Purpose:** Define the conditions under which NiceHome products may be returned, what refund amounts apply, and how returns are processed.

**Expected fact types:**
- Return window (in days from purchase)
- Condition requirements (unopened, opened, damaged)
- Refund type (full, partial, store credit)
- Exceptions (subscriptions, firmware-activated devices, promotional items)
- Return process steps
- Shipping cost responsibility

**Estimated canonical facts:** 10–12

**Task categories supported:** T2 (conditional policy), T3 (multi-step process)

**Risks and ambiguity to avoid:**
- Keep monetary amounts out of the fact-set unless absolutely necessary; if included, use fixed round numbers to avoid arithmetic errors
- Define exactly one return path per condition set — avoid ambiguity about which policy applies when conditions overlap
- Do not model restocking fees unless needed; they add arithmetic complexity

---

### Document 4: Subscription plan rules

**Purpose:** Define what subscription plans are available for NiceHome services (e.g., cloud storage for Camera, extended monitoring for Sensor), what they include, and how they are managed.

**Expected fact types:**
- Plan names and included features
- Plan eligibility conditions (which devices require/support which plans)
- Cancellation rules (refund, pro-rated credit, effective date)
- Upgrade/downgrade rules
- Trial period terms

**Estimated canonical facts:** 8–10

**Task categories supported:** T2 (conditional policy), T1 (simple factual lookup of plan features)

**Risks and ambiguity to avoid:**
- Do not include pricing amounts in the canonical fact-set — pricing creates arithmetic noise in evaluation and also creates version drift risk; describe plans by their features and rules, not their costs (see DS5 in §14)
- Avoid subscription rules that depend on purchase date arithmetic
- Keep trial-period terms simple (one condition, one outcome)

---

### Document 5: Shipping and delivery policy

**Purpose:** Define shipping options, delivery timeframes, and what happens when delivery goes wrong.

**Expected fact types:**
- Available shipping methods
- Delivery timeframe per method (as relative ranges, not absolute dates)
- Geographic restrictions
- Handling of delayed or lost shipments
- Order modification or cancellation window

**Estimated canonical facts:** 8–10

**Task categories supported:** T1 (simple factual lookup), T2 (conditional — depends on method or geography)

**Risks and ambiguity to avoid:**
- Do not include specific country lists — geographic scoping creates facts that are difficult to evaluate consistently and may introduce cultural familiarity effects
- Keep delivery timeframes in business days (not calendar days with holiday exceptions) to avoid date arithmetic
- Do not introduce dynamic facts (e.g., "delivery times may vary during peak periods") — all facts must be deterministic

---

### Document 6: Troubleshooting guide

**Purpose:** Provide step-by-step diagnostic and resolution procedures for common NiceHome device issues.

**Expected fact types:**
- Issue categories (connectivity, power, app pairing, sensor calibration)
- Diagnostic steps per issue type
- Resolution actions per diagnosis
- Escalation conditions (when to contact support vs. self-resolve)

**Estimated canonical facts:** 12–15

**Task categories supported:** T3 (multi-step process), T4 (troubleshooting with conditional branches)

**Risks and ambiguity to avoid:**
- Troubleshooting steps must be ordered — each step depends on the result of the previous; this must be represented in the fact schema (see §5, condition field)
- Do not create circular or ambiguous diagnostic trees
- Avoid device-specific troubleshooting that requires knowledge of hardware internals not established in Document 1
- Each troubleshooting path should reach a terminal resolution or a clear escalation — no open-ended outcomes

---

### Document 7: Repair and replacement policy

**Purpose:** Define when devices are repaired vs. replaced, who pays, and how the process works.

**Expected fact types:**
- Repair eligibility conditions (in-warranty vs. out-of-warranty)
- Replacement conditions (when repair is not possible)
- Refurbished device policy (when replacements may be refurbished)
- Customer cost conditions (shipping, service fees out of warranty)
- Turnaround time expectations

**Estimated canonical facts:** 8–10

**Task categories supported:** T2 (conditional policy), T3 (multi-step process)

**Risks and ambiguity to avoid:**
- Repair vs. replacement decision should depend on a small, well-defined set of conditions — avoid complex decision trees that are difficult to evaluate deterministically
- Cross-reference with warranty policy (Document 2) is expected; make sure the boundary between warranty claims and repair requests is explicit in both fact-sets

---

### Document 8: Account access and device reset policy

**Purpose:** Define how users manage their NiceHome accounts, including password recovery, device deregistration, and factory reset procedures.

**Expected fact types:**
- Account recovery steps
- Device reset procedure steps (soft reset vs. factory reset)
- What data is deleted by a factory reset
- Conditions for remote deregistration
- Re-registration steps after reset

**Estimated canonical facts:** 8–10

**Task categories supported:** T3 (multi-step process), T4 (troubleshooting — reset as a resolution step)

**Risks and ambiguity to avoid:**
- Keep reset procedures short enough to be evaluatable deterministically (≤5 steps)
- Define what "factory reset" means in terms of data loss — this is a common evaluation ambiguity
- Do not introduce security policies that require judgment calls (e.g., "what counts as suspicious activity") — keep conditions deterministic

---

### Document set summary

| Doc | Category | Est. facts | Primary task categories |
|---|---|---|---|
| D01 | Product overview and compatibility | 10–12 | T1, T2 |
| D02 | Warranty policy | 8–10 | T2, T3 |
| D03 | Return and refund policy | 10–12 | T2, T3 |
| D04 | Subscription plan rules | 8–10 | T1, T2 |
| D05 | Shipping and delivery policy | 8–10 | T1, T2 |
| D06 | Troubleshooting guide | 12–15 | T3, T4 |
| D07 | Repair and replacement policy | 8–10 | T2, T3 |
| D08 | Account access and device reset policy | 8–10 | T3, T4 |
| **Total** | | **~72–79** | |

Target: ~75 canonical facts. The troubleshooting guide is the densest document because each step is a separate fact.

---

## 5. Canonical fact-set structure

Each entry in the canonical fact-set represents one atomic, verifiable claim from the knowledge base. A fact is atomic if it cannot be split into two independently verifiable claims. This section defines the schema only; the canonical fact-set is created in a separate file.

### Schema

```
fact_id
  Required. Unique identifier.
  Format: F<document_number><sequential_two_digit_index>
  Example: F0103 (Document 1, fact 3), F0612 (Document 6, fact 12)

document_id
  Required. The source document.
  Values: D01 through D08

category
  Required. Semantic category of the fact within the document.
  Examples: "compatibility", "warranty_coverage", "return_condition",
            "subscription_feature", "shipping_method", "troubleshooting_step",
            "repair_eligibility", "account_procedure"

fact_type
  Required. Structural type of the fact.
  Values:
    simple       — one entity, one attribute, no conditions
    conditional  — one or more preconditions determine the outcome
    sequential   — an ordered step in a multi-step procedure
    exception    — a carve-out that modifies another fact

condition(s)
  Applicable when fact_type is conditional, sequential, or exception.
  A list of conditions that must all be true for the rule/action to apply.
  Each condition is expressed in language-neutral terms.
  For sequential facts: include the step number and what prior steps must have been completed.
  Example: ["device is NiceHome Hub", "purchased within 30 days", "packaging is unopened"]

rule/action
  Required. The claim, rule, or step that applies when the conditions (if any) are met.
  Must be expressed in language-neutral terms.
  Example: "customer is entitled to a full refund of the purchase price"

exceptions
  Optional. Conditions under which the rule/action does NOT apply, if any.
  Cross-reference to the fact_id of any relevant exception facts.

required_entities
  Required. Named entities (device names, plan names, roles) that must appear
  in any evaluation of a response drawing on this fact.
  Example: ["NiceHome Hub", "Hub Pro Plan"] or ["NiceHome Sensor", "Gen 2"]

language_neutral_expected_outcome
  Required. A brief description of what a correct response must convey,
  without specifying wording, language, or style.
  This field is used by the evaluator to assess PASS/FAIL.
  Example: "Response must state the return window is 30 days for unopened devices
           and must not claim a different window applies."

forbidden_claims
  Required. A list of claims that must NOT appear in a correct response.
  These are the hallucination targets for this fact.
  Example: ["return window is 60 days", "opened devices qualify for full refund",
            "subscriptions are refundable"]

ambiguity_notes
  Optional. Notes about where this fact might be misinterpreted in evaluation,
  or where language rendering might introduce ambiguity.
  Example: "The Dutch word for 'refund' may be rendered as 'terugbetaling' or
            'restitutie' — both are acceptable; neither is more correct."
```

### Schema constraints

- Every fact must have a unique `fact_id`.
- `fact_type = sequential` facts must have a `condition` that includes their step order.
- `fact_type = exception` facts must reference the `fact_id` of the primary fact they modify in their `exceptions` field.
- `language_neutral_expected_outcome` must be written so it can be evaluated without seeing the KB rendering — it must depend only on semantic content, not phrasing.
- `forbidden_claims` must include at minimum one plausible hallucination (a wrong answer that a model might confidently produce).

---

## 6. Intent specification structure

Each entry in the intent set defines one task instance at the language-neutral level. The intent is rendered into English, Dutch, and Turkish query text in a separate step. This section defines the schema only; the intent set is created in a separate file.

### Schema

```
intent_id
  Required. Unique identifier.
  Format: I<two_digit_index><difficulty_code>
  Difficulty codes: S (simple), C (conditional), T (troubleshooting/process)
  Example: I01S, I12C, I25T

task_category
  Required. Alignment to the task skeleton from task-family-selection-v0.1.md.
  Values: T1 (simple factual), T2 (conditional policy), T3 (multi-step process),
          T4 (troubleshooting), T5 (cross-document)

linked_fact_ids
  Required. List of all fact_ids that are potentially relevant to this intent.
  Must include all facts the evaluator would need to assess a full correct response.
  Example: ["F0301", "F0302", "F0304"]

required_facts
  Required. Subset of linked_fact_ids that MUST be present for a PASS.
  A response that references only optional/supporting facts but not required facts is a FAIL.
  Example: ["F0301", "F0302"]

user_scenario
  Required. A language-neutral description of the user situation that motivates this intent.
  This is the abstract scenario from which the query text is rendered in each language.
  Example: "User purchased a NiceHome Sensor 25 days ago. The packaging is unopened.
            The user wants to know if they can return it and what refund they would receive."

condition_count
  Required. Number of conditions in the intent that must be correctly handled for a PASS.
  For simple intents: 0–1. For conditional: 2–3. For troubleshooting/process: 3+.

expected_outcome
  Required. Language-neutral description of what a PASS response must contain.
  Expressed as fact content, not as wording.
  Cross-references required_facts.
  Example: "Must state: return is possible; return window is 30 days; device is within
           the window; refund is full (not partial or credit); must not claim unopened
           condition does not matter."

forbidden_claims
  Required. Claims that must not appear in a PASS response.
  Intent-level forbidden claims add to (do not replace) the fact-level forbidden claims
  for linked_fact_ids.
  Example: ["subscription plans are refundable", "camera cannot be returned",
            "30-day window applies from delivery not purchase"]

difficulty_level
  Required. One of: simple / conditional / multi-step
  Determines which of the three difficulty groups this intent belongs to.
  Must be consistent with condition_count and task_category.

language_rendering_notes
  Optional. Notes for the person rendering the query into each language.
  Should flag any terminology decisions or register choices needed.
  Example: "The Dutch rendering should use informal register (jij/je).
            The Turkish rendering should use the polite but not formal register."

evaluation_notes
  Optional. Notes for the evaluator.
  Flag any known near-miss cases, edge conditions in the expected_outcome,
  or cases where UNCERTAIN is especially likely.
  Example: "If the model correctly identifies the return is possible but gives
           the wrong refund type, this is a FAIL, not an UNCERTAIN."
```

### Schema constraints

- Every intent must have at least one `required_fact`.
- All `linked_fact_ids` and `required_facts` must exist in the canonical fact-set.
- `condition_count` must be ≥2 for `difficulty_level = conditional` and ≥3 for `difficulty_level = multi-step`.
- `expected_outcome` must be expressible without reference to any KB rendering — it must be language-neutral.
- At least one `forbidden_claim` per intent.

---

## 7. Language rendering rules

These rules govern how canonical fact-set content becomes KB prose (in Document 1–8 text form) and how intent specifications become user query text (in query rendering form). Both applications follow the same rules.

**Render from the structured fact-set, not from another language rendering.**
The authoring direction is always: canonical fact-set → language rendering. Never: English document → Dutch document. This means three independent authoring passes are required, one per language.

**Preserve meaning, not literal phrasing.**
The goal is semantic equivalence, not literal translation. A Dutch rendering is not a translation of English; it is an independent expression of the same fact-set content. The evaluator will check for the presence of the required semantic content, not for exact wording.

**Avoid idioms.**
Idiomatic expressions in any rendering may not have equivalents in other languages and may introduce meaning that is absent from the fact-set. Use plain language.

**Keep terminology controlled.**
The `language-rendering-plan.md` (to be created) will establish an approved terminology list for each language: one rendering per product name, plan name, action name, and policy term. Authors must use the approved terminology list consistently. Example: if the Turkish word for "warranty" is decided to be "garanti" (as opposed to "güvence"), all Turkish documents must use "garanti" — an author must not switch mid-document.

**Avoid unnecessary verbosity.**
Verbose renderings inflate token counts. Verbose token counts create measurement artifacts that are not token-tax (they are style choices). Keep renderings concise and equivalent in information density.

**No hidden English canonical wording.**
No rendering should be written as "what the English would say in this language." A rendering is not a culturally adapted English document. It is an independent document authored from the fact-set.

**Turkish review can be performed by the project owner as native speaker.**
The project owner is a native Turkish speaker. Turkish KB renderings and query renderings may be reviewed by the project owner at run level. This is explicitly permitted and is not a limitation relative to the Dutch or English conditions (where the project owner also performs the review).

**Independent review is recommended before public claims.**
As stated in `evaluation-method-v0.1.md` and `language-selection-v0.1.md`: before any results are shared publicly or submitted for publication, an independent bilingual reviewer should review the Turkish KB rendering and a sample of Turkish outputs. This requirement does not affect v0.1 exploratory analysis shared with the qualifier "single-evaluator exploratory pilot; independent review pending."

---

## 8. Expected answer design

Expected answers in NiceM v0.1 are not reference answer strings. They are structured representations of the semantic content a correct response must contain.

### What this means in practice

**Language-neutral.** The expected answer is defined once, in the fact-set schema, and applies equally to English, Dutch, and Turkish responses. There is no "correct English answer" against which other-language responses are compared.

**Fact/action-based.** A PASS response must contain the required facts (identified by `required_facts` in the intent schema) with correct values. A response that correctly states the return window is 30 days in Turkish, using different words than the Turkish KB, still passes — if the semantic content is correct.

**Not wording-based.** The evaluator does not check whether the response matches a reference answer string, or whether it uses the exact phrasing of the KB rendering. This protects against a measurement artifact where responses are penalized for style differences that have no bearing on correctness.

**Not style-judged.** A response that is verbose, uses formal register where informal was expected, or structures the answer differently from the expected format is not penalized on those grounds. The evaluator may note style observations in the evaluation log, but they do not affect the PASS/FAIL gate.

**Forbidden claims are the hallucination check.** The negative component of the expected answer — the `forbidden_claims` field — catches incorrect content that might be expressed confidently. A response that correctly states the return window but also claims that opened devices qualify for a full refund is a FAIL because of the forbidden claim, even though part of the response was correct.

**UNCERTAIN is a first-class outcome.** When the evaluator cannot determine whether a required fact is present or correctly expressed — for example, because the response is ambiguous or the terminology is unfamiliar — the outcome is UNCERTAIN. UNCERTAIN is not rounded down to FAIL and is not rounded up to PASS. It is a calibration signal. Per `falsification-and-decision-rules-v0.1.md`, if UNCERTAIN exceeds 25% in any condition, analysis is paused for recalibration.

---

## 9. Difficulty distribution

The 36 intents are distributed as follows:

| Difficulty level | Count | Condition count | Primary task categories |
|---|---|---|---|
| Simple factual | 12 | 0–1 | T1, T2 (single condition) |
| Conditional policy | 12 | 2–3 | T2 (multi-condition), T3 |
| Troubleshooting / process | 12 | 3+ | T3, T4, T5 (cross-document) |

### Why this distribution helps compare execution overhead

**Simple intents isolate representation overhead.** A simple factual intent ("which devices are compatible with NiceHome Hub?") requires retrieving one or two facts and producing a short answer. Under Agent A (Direct LLM), the model must recall from its (fictional) in-context KB. Under Agent B (Simple RAG), the model retrieves and answers. Cost differences between languages at this tier are close to pure token-tax — the workflow is minimal.

**Conditional intents introduce decision overhead.** A conditional intent ("is a customer entitled to a full refund if they return an opened NiceHome Sensor after 15 days?") requires the model to correctly apply multiple conditions. Under Agent A, the model must hold and apply the conditions from its in-context KB. Under Agent B, it must retrieve the right facts (which may be spread across retrieval chunks) and apply the conditions. Cost differences at this tier include both token-tax and candidate retrieval/reasoning overhead.

**Troubleshooting/process intents introduce sequential execution overhead.** A multi-step process intent ("walk me through resetting a NiceHome Hub and re-registering it") requires the model to produce a correctly ordered sequence of actions. Under Agent B, the model may make multiple retrieval calls or retrieve a long chunk to cover the full sequence. This tier maximizes the observable trajectory difference between designs and languages.

**The three tiers enable decomposition.** If language-related cost differences are observed only at the conditional and troubleshooting tiers — not at the simple tier — that is evidence that execution-tax is distinct from token-tax. If differences appear equally at all tiers, that is evidence that the signal is dominated by token-tax. The distribution is designed to make this decomposition possible, not to prove execution-tax in advance.

---

## 10. Retrieval design implications

The v0.1 benchmark uses language-matched retrieval: each language condition retrieves from its own KB rendering (per `retrieval-design-decision-v0.1.md`). The dataset must be designed to support this cleanly.

**The KB must be large enough that retrieval is non-trivial.** Eight documents totaling ~75 facts, when chunked for RAG, should produce enough candidate chunks that a retrieval query cannot trivially return all relevant content in one chunk. The troubleshooting guide (12–15 facts, multiple sequential procedures) and the return/warranty policies (multiple conditional branches) are the densest documents and should naturally create retrieval selectivity.

**The same canonical facts must exist in each language KB rendering.** Every fact in the English KB rendering must have a semantically equivalent counterpart in the Dutch and Turkish renderings. This is the KB completeness gate (§6 quality gate, §11 quality gates). If a fact exists in the English rendering but not the Dutch one, a Dutch retrieval condition cannot possibly retrieve it — creating a structural confound that has nothing to do with token-tax or execution-tax.

**Retrieved semantic units should be trackable via fact_id.** The logging schema's `semantic_units_retrieved` field (from `logging-schema-v0.1.md`) tracks which canonical fact IDs were present in the retrieved context, not just how many tokens were retrieved. This requires that the KB chunking strategy preserve the alignment between chunks and fact IDs. The chunking strategy (one chunk per document, one chunk per section, or one chunk per fact) is a design decision to be resolved in `language-rendering-plan.md` — but the dataset must be structured so that any chunking strategy preserves fact-level traceability.

**RAG evaluation should distinguish raw tokens from semantic facts retrieved.** The dual-reporting rule from `baseline-token-tax-calculation-v0.1.md` applies: retrieval volume is always reported in both raw tokens and semantic units (fact IDs present in retrieved context). If Dutch retrieval produces 40% more tokens than English retrieval but retrieves the same three canonical facts, the extra tokens are retrieval token-tax — not retrieval execution-tax. The dataset design must make this distinction possible by keeping fact-to-chunk alignment explicit.

---

## 11. Dataset quality gates

These quality gates apply before any language KB rendering is frozen and before any model run begins. They correspond to the gates in `validation-plan-v0.1.md` §6, specialized for the dataset artifacts.

**Fact-set completeness.**
Every intent in the intent set maps to at least one fact in the canonical fact-set via `linked_fact_ids`. Every `required_facts` entry exists in the canonical fact-set. No orphan facts (facts not referenced by any intent). No orphan intents (intents whose required facts do not exist).

**No contradictory facts.**
No two facts in the canonical fact-set make incompatible claims about the same entity and condition set. If Document 2 says the warranty period for the NiceHome Hub is 2 years and Document 7 says it is 1 year, this is a contradiction that must be resolved in the fact-set before any rendering work begins.

**Every intent maps to expected fact IDs.**
The `required_facts` field of every intent contains at least one fact ID. The `expected_outcome` field is expressible entirely in terms of the content of the `required_facts` without referencing any KB rendering text.

**Every expected outcome is language-neutral.**
Every `expected_outcome` and `language_neutral_expected_outcome` field can be evaluated by a reviewer who has not seen the KB rendering — it depends only on semantic content. If an expected outcome contains the phrase "the response should say..." followed by text that could only come from a specific rendering, it fails this gate.

**Every language rendering preserves required meaning.**
For every canonical fact and every language rendering: the semantic content of the required_entity, rule/action, and condition fields is present in the rendering. This is checked per-document, per-language, against the fact-set. Reviewer signs off before the rendering is frozen.

**No English document has privileged status.**
The English KB and English query renderings are reviewed for correctness against the fact-set on the same terms as the Dutch and Turkish renderings. If the English rendering omits a condition that the Dutch rendering preserves, the English rendering is wrong — not authoritative.

**All forbidden claims listed where relevant.**
Every fact and every intent with a plausible hallucination target has at least one entry in its `forbidden_claims` field. The evaluator must have explicit forbidden claims to check; they cannot rely on judgment alone.

**Ambiguity notes included for risky cases.**
Any fact or intent where rendering or evaluation might be ambiguous has an `ambiguity_notes` entry explaining the risk. Cases where two renderings are equally acceptable, or where an evaluator might UNCERTAIN a response for a known stylistic reason, should be flagged before evaluation begins.

---

## 12. Versioning

All benchmark artifacts are versioned independently and collectively. A version bump is required whenever a frozen artifact is edited.

### Version fields

```
dataset_version
  Top-level version for the entire v0.1 benchmark dataset.
  Format: v0.1.<patch>
  Initial value: v0.1.0
  Bumped when: any frozen artifact is edited after the dataset freeze date.
  Change log: tracked in a CHANGELOG section within this document or in a
              separate docs/benchmark/v0.1/CHANGELOG.md.

fact_set_version
  Version of the canonical fact-set (canonical-fact-set.md).
  Format: fs-v0.1.<patch>
  Initial value: fs-v0.1.0
  Bumped when: any fact is added, removed, or modified after freeze.
  If fact_set_version changes after KB renderings are frozen, all KB renderings
  must be re-reviewed and re-frozen.

kb_rendering_version
  Version of the KB rendering per language.
  Format: kb-<lang>-v0.1.<patch>
  Examples: kb-en-v0.1.0, kb-nl-v0.1.0, kb-tr-v0.1.0
  Each language has its own version; a rendering fix in Dutch does not bump English.
  If kb_rendering_version changes after Stage 1 is complete, Stage 1 must be re-run.

intent_set_version
  Version of the intent set (intent-set.md).
  Format: is-v0.1.<patch>
  Initial value: is-v0.1.0
  Bumped when: any intent is added, removed, or modified after freeze.
  If intent_set_version changes after Stage 2 smoke test, the smoke test must be repeated.

language_rendering_version
  Version of the query rendering per language.
  Format: qr-<lang>-v0.1.<patch>
  Examples: qr-en-v0.1.0, qr-nl-v0.1.0, qr-tr-v0.1.0
  Each language has its own version.
```

### Version logging

Every run log row must record:
- `dataset_version`
- `fact_set_version`
- `kb_rendering_version` (for the language condition of that run)
- `intent_set_version`
- `language_rendering_version` (for the language condition of that run)

This ensures that if any artifact is updated between Stage 2 and Stage 3, affected run rows can be identified and re-run before analysis.

---

## 13. Files to create later

The following files will be created in the `docs/benchmark/v0.1/` folder as part of the artifact construction sequence defined in `validation-plan-v0.1.md` §5. They are not created here.

```
docs/benchmark/v0.1/canonical-fact-set.md
  The canonical artifact. ~75 facts structured per the schema in §5.
  Created after this specification is reviewed and accepted.
  First real benchmark content.
  STATUS: CREATED — 78 facts (fs-v0.1.0, not yet frozen). The actual per-document
  counts (D01:10, D02:9, D03:11, D04:9, D05:8, D06:13, D07:9, D08:9) supersede the
  estimates in §4 of this document. DS3 (final fact count) is now resolved at 78.

docs/benchmark/v0.1/document-plan.md
  Defines the exact content plan for each of the 8 synthetic documents
  before the documents themselves are written.
  Includes: section structure per document, fact distribution per section,
  ambiguity decisions, terminology decisions.
  Created after canonical-fact-set.md is drafted.

docs/benchmark/v0.1/intent-set.md
  All 36 intent specifications structured per the schema in §6.
  Created after canonical-fact-set.md is stable enough to assign fact IDs.

docs/benchmark/v0.1/language-rendering-plan.md
  Terminology lists per language (product names, policy terms, action verbs).
  Register decisions per language.
  Chunking strategy decision (chunk-per-document, chunk-per-section, chunk-per-fact).
  Created after the fact-set is stable and before any KB rendering begins.

docs/benchmark/v0.1/expected-fact-mapping.md
  Maps each intent_id to its required_facts and expected_outcome.
  Designed to be the evaluator's reference — no KB rendering text, only semantic fact content.
  Created after intent-set.md is stable.

docs/benchmark/v0.1/quality-gates.md
  Implements the quality gates defined in §11 as a checklist with owner fields and
  pass/fail status. Updated as artifacts are reviewed and frozen.
  Created once artifact construction begins; updated continuously.
```

---

## 14. Open questions

These questions are open as of this specification. They do not block authoring the canonical fact-set, but should be resolved before the fact-set is frozen.

**DS1 — What should the fictional product names be?**
"NiceHome Hub/Sensor/Plug/Camera" is the working recommendation. The question is whether "NiceHome" as a brand name inside the fictional product world is confusing given that "NiceM" is the name of the research project. Options: (a) use "NiceHome" as proposed, noting they are distinct; (b) use a fully unrelated brand name (e.g., "Velio", "Lumio", "Karu"); (c) use a clearly placeholder name (e.g., "SmartCo Hub"). The choice does not affect any methodology.

**DS2 — Should NiceM branding appear inside the fictional product world, or should it be separate?**
Related to DS1. NiceM is a research project about measuring AI execution overhead. The fictional product domain is a benchmark fixture. Keeping the brands distinct avoids any implication that NiceM is also a product company. Recommendation: keep them entirely separate. NiceM does not appear inside the KB documents.

**DS3 — How many facts should each document contain?**
The ranges in §4 sum to ~72–79 facts against a ~75 target. The final count is a fact-set authoring decision. The only constraint is that retrieval must be non-trivial (§10): too few facts → trivial retrieval; too many → review burden at this pilot scale. The ranges in §4 are reasonable; they should be confirmed or adjusted during canonical-fact-set authoring.

**DS4 — Which facts should be simple vs conditional?**
The difficulty distribution in §9 requires ~12 simple intents, which means there must be enough simple (non-conditional) facts to support them without overlap. The document plan (§13) should map each document's facts to their expected difficulty contribution before authoring begins.

**DS5 — Should subscriptions/pricing be included or avoided to reduce arithmetic noise?**
Document 4 (Subscription plan rules) is included in the design but §4 recommends keeping monetary amounts out of the fact-set. This means subscription plans are defined by features and conditions, not prices. If pricing is completely absent, certain real-world query types ("how much does the plan cost?") become unanswerable, which reduces task realism. One option: include pricing as a simple lookup fact (a fixed round number) with evaluation checking only whether the correct price is stated, not computed. This is the least-risk approach if pricing is included at all. Decision is deferred to document-plan.md authoring.

**DS6 — How formal should Turkish and Dutch renderings be?**
Both Turkish and Dutch have formal/informal register distinctions. The `language_rendering_notes` field in the intent schema allows per-intent register guidance. A global default must be set in `language-rendering-plan.md`. Recommendation: Dutch informal (jij/je form); Turkish polite-informal (siz form without excessive honorifics). This is a rendering plan decision, not a fact-set decision.

**DS7 — Should troubleshooting tasks include ordered steps?**
Yes — this is already reflected in the `sequential` fact type (§5) and in the troubleshooting document design (§4 Document 6). The question is whether the query renderings should ask for the steps explicitly ("walk me through...") or implicitly ("my Hub won't connect — what should I do?"). The implicit form is more realistic but makes evaluation harder (the model may not produce all steps explicitly). Recommendation: use implicit query forms but ensure the intent schema's `expected_outcome` explicitly lists the required steps. Decide at intent-set authoring.

**DS8 — Should any tasks require combining facts from two documents?**
Task category T5 (cross-document, per `task-family-selection-v0.1.md`) is listed as a supported category for the troubleshooting and repair tiers. Example: a troubleshooting task that requires checking both the troubleshooting guide (D06) and the repair policy (D07) to give a complete answer. Cross-document tasks increase retrieval challenge and are good execution-tax probe tasks. They also increase evaluation complexity. Recommendation: include 2–4 cross-document intents within the 12 troubleshooting/process tier, not as a separate category. Confirm at intent-set authoring.

---

*End of dataset specification. No canonical facts, KB documents, or intents are created in this file.*
